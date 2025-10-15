import sqlite3
import os
 
def create_database():
    # Correctly locate the database file in the backend directory
    script_dir = os.path.dirname(os.path.realpath(__file__))
    db_file = os.path.join(script_dir, 'taxi_trips.db')
 
    conn = sqlite3.connect(db_file)
    c = conn.cursor()

    # --- NEW: Tell SQLite to enforce foreign key constraints ---
    c.execute('PRAGMA foreign_keys = ON;')

    # --- First, ensure the vendors table exists so trips can reference it ---
    c.execute('''
        CREATE TABLE IF NOT EXISTS vendors (
            id INTEGER PRIMARY KEY,
            fullname TEXT NOT NULL
        )
    ''')
    
    # --- MODIFIED: Added the FOREIGN KEY constraint to the trips table ---
    c.execute('''
        CREATE TABLE IF NOT EXISTS trips (
            id TEXT,
            vendor_id INTEGER,
            pickup_datetime TEXT,
            dropoff_datetime TEXT,
            passenger_count INTEGER,
            trip_distance REAL,
            pickup_longitude REAL,
            pickup_latitude REAL,
            dropoff_longitude REAL,
            dropoff_latitude REAL,
            fare_amount REAL,
            tip_amount REAL,
            trip_duration REAL,
            trip_speed REAL,
            fare_per_km REAL,
            idle_time REAL,
            FOREIGN KEY (vendor_id) REFERENCES vendors (id)
        )
    ''')
    
    c.execute('CREATE UNIQUE INDEX IF NOT EXISTS idx_trips_id ON trips (id)')

    conn.commit()
    conn.close()
    print("Database and tables (trips, vendors) with relationship created successfully.")

if __name__ == '__main__':
    create_database()