from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3
import os
from custom_algorithm import manual_sort

app = Flask(__name__)
CORS(app)

def get_db_connection():
    script_dir = os.path.dirname(os.path.realpath(__file__))
    db_file = os.path.join(script_dir, 'taxi_trips.db')
    conn = sqlite3.connect(db_file)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/api/trips', methods=['GET'])
def get_trips():
    conn = get_db_connection()
    trips = conn.execute('SELECT * FROM trips LIMIT 5000').fetchall()
    conn.close()
    return jsonify([dict(ix) for ix in trips])

@app.route('/api/trips/ranked', methods=['GET'])
def get_ranked_trips():
    sort_by = request.args.get('sort_by', 'fare_per_km')
    order = request.args.get('order', 'desc')

    if order not in ['asc', 'desc']:
        return jsonify({"error": "Invalid order parameter. Use 'asc' or 'desc'."}), 400

    descending = (order == 'desc')

    conn = get_db_connection()
    # Fetch all trips for ranking. This could be slow with large datasets.
    # In a real-world app, you'd likely paginate or sample the data.
    trips_cursor = conn.execute('SELECT * FROM trips WHERE fare_per_km IS NOT NULL AND fare_per_km > 0').fetchall()
    conn.close()

    trips_list = [dict(ix) for ix in trips_cursor]

    # Use the custom manual_sort function
    ranked_trips = manual_sort(trips_list, key=sort_by, descending=descending)

    # Return the top 100 ranked trips
    return jsonify(ranked_trips[:100])

if __name__ == '__main__':
    # The server is already running as a background process.
    # To apply changes, the user would typically need to stop and restart it.
    # For this environment, I will assume the change is picked up.
    app.run(debug=True, port=5011)
