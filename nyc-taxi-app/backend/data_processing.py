import pandas as pd
import sqlite3
import os
import math
 
def haversine_distance(lon1, lat1, lon2, lat2):
    """
    Calculate the great-circle distance between two points
    on the earth (specified in decimal degrees).
    """
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(math.radians, [lon1, lat1, lon2, lat2])
 
    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    r = 3956 # Radius of earth in miles.
    return c * r

# --- NEW FUNCTION ---
def populate_vendors(conn, csv_file):
    """
    Extracts unique vendors from the CSV and populates the vendors table.
    This function runs once at the start for maximum efficiency.
    """
    print("Populating vendors table...")
    # Map vendor IDs to the desired full name format
    vendor_mapping = {
        1: 'Vendor_1',
        2: 'Vendor_2'
    }

    try:
        # Efficiently read only the 'vendor_id' column to find unique values
        vendor_ids = pd.read_csv(csv_file, usecols=['vendor_id']).squeeze('columns').unique()
        
        # Prepare data for insertion, converting ID to integer to prevent errors
        vendors_to_insert = [
            (int(vid), vendor_mapping.get(int(vid), f'Unknown_Vendor_{int(vid)}'))
            for vid in vendor_ids if pd.notna(vid)
        ]

        if vendors_to_insert:
            c = conn.cursor()
            # Use 'INSERT OR IGNORE' to safely insert without creating duplicates
            c.executemany("INSERT OR IGNORE INTO vendors (id, fullname) VALUES (?, ?)", vendors_to_insert)
            conn.commit()
            print(f"Successfully populated/verified {len(vendors_to_insert)} vendors.")
    except Exception as e:
        print(f"Could not populate vendors table: {e}")
# --- END NEW FUNCTION ---

def clean_and_insert_data(chunk, conn):
    script_dir = os.path.dirname(os.path.realpath(__file__))
    log_file = os.path.join(script_dir, 'excluded_records.log')
 
    # Calculate trip_distance from coordinates
    chunk['trip_distance'] = chunk.apply(
        lambda row: haversine_distance(
            row['pickup_longitude'],
            row['pickup_latitude'],
            row['dropoff_longitude'],
            row['dropoff_latitude']
        ),
        axis=1
    )

    # (The rest of this function remains unchanged)
    
    # Identify records to be excluded
    original_count = len(chunk)
    
    # Identify rows with nulls in critical columns
    null_mask = chunk['trip_duration'].isnull() | chunk['trip_distance'].isnull() | chunk['id'].isnull()
    
    # Identify duplicates (after handling nulls)
    non_null_chunk = chunk[~null_mask]
    dup_mask = non_null_chunk.duplicated(subset=['id'], keep='first')
 
    # Identify invalid trip data (duration or distance <= 0)
    invalid_mask = (non_null_chunk['trip_duration'] <= 0) | (non_null_chunk['trip_distance'] <= 0)

    # Log records that will be dropped
    with open(log_file, 'a', encoding='utf-8') as f:
        # Log nulls
        excluded_by_null = chunk[null_mask]
        if not excluded_by_null.empty:
            f.write("--- Excluded due to NULL values ---\n")
            f.write(excluded_by_null.to_string() + '\n')
        
        # Log duplicates
        excluded_by_dup = non_null_chunk[non_null_chunk.duplicated(subset=['id'], keep=False)]
        if not excluded_by_dup.empty:
            f.write("--- Excluded due to duplicate ID ---\n")
            f.write(excluded_by_dup.to_string() + '\n')
 
        # Log invalid
        excluded_by_invalid = non_null_chunk[invalid_mask]
        if not excluded_by_invalid.empty:
            f.write("--- Excluded due to invalid trip data ---\n")
            f.write(excluded_by_invalid.to_string() + '\n')
 
    # Perform the cleaning
    chunk.dropna(subset=['trip_duration', 'trip_distance', 'id'], inplace=True)
    chunk.drop_duplicates(subset=['id'], inplace=True)
    chunk = chunk[chunk['trip_duration'] > 0]
    chunk = chunk[chunk['trip_distance'] > 0]
    
    if chunk.empty:
        return # No valid data to process
 
    # Derived features
    chunk['trip_distance_km'] = chunk['trip_distance'] * 1.60934
    chunk['trip_speed_kph'] = chunk['trip_distance_km'] / (chunk['trip_duration'] / 3600)
    chunk['fare_amount'] = 2.50 + (chunk['trip_distance'] * 2.50) + (chunk['trip_duration'] / 60 * 0.50)
    chunk['fare_per_km'] = chunk['fare_amount'] / chunk['trip_distance_km']
    chunk['fare_per_km'].fillna(0, inplace=True)
    chunk = chunk[chunk['fare_per_km'] >= 0]
    chunk['idle_time'] = 0
 
    # Select and rename columns
    db_columns = {
        'id': 'id',
        'vendor_id': 'vendor_id',
        'pickup_datetime': 'pickup_datetime',
        'dropoff_datetime': 'dropoff_datetime',
        'passenger_count': 'passenger_count',
        'trip_distance': 'trip_distance',
        'pickup_longitude': 'pickup_longitude',
        'pickup_latitude': 'pickup_latitude',
        'dropoff_longitude': 'dropoff_longitude',
        'dropoff_latitude': 'dropoff_latitude',
        'fare_amount': 'fare_amount',
        'trip_duration': 'trip_duration',
        'trip_speed_kph': 'trip_speed',
        'fare_per_km': 'fare_per_km',
        'idle_time': 'idle_time'
    }
    existing_cols = {k: v for k, v in db_columns.items() if k in chunk.columns}
    chunk = chunk[list(existing_cols.keys())].rename(columns=existing_cols)
 
    # Insert data into the database
    try:
        chunk.to_sql('trips', conn, if_exists='append', index=False)
    except sqlite3.IntegrityError:
        pass

def process_data():
    script_dir = os.path.dirname(os.path.realpath(__file__))
    csv_file = os.path.join(script_dir, '..', '..', 'train.csv')
    db_file = os.path.join(script_dir, 'taxi_trips.db')
 
    if not os.path.exists(csv_file):
        print(f"Error: {csv_file} not found.")
        return
 
    conn = sqlite3.connect(db_file)
    
    # --- MODIFIED ---
    # Call the new function to populate vendors before processing trips
    populate_vendors(conn, csv_file)
    # --- END MODIFIED ---
    
    chunk_size = 100000
    total_rows = 0
    
    print("\nStarting trip data processing...")
    for i, chunk in enumerate(pd.read_csv(csv_file, chunksize=chunk_size)):
        clean_and_insert_data(chunk, conn)
        total_rows += len(chunk)
        print(f"Processed chunk {i+1}, total rows processed: {total_rows}")
 
    conn.close()
    print("Data processing complete.")

if __name__ == '__main__':
    # First, ensure the database and table are created
    script_dir = os.path.dirname(os.path.realpath(__file__))
    db_script_path = os.path.join(script_dir, 'database.py')
    os.system(f'python {db_script_path}')
    
    process_data()