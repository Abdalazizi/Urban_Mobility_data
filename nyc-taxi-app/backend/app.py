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
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 100, type=int)
    offset = (page - 1) * limit

    
    date_from = request.args.get('date_from')
    date_to = request.args.get('date_to')
    min_fare = request.args.get('min_fare', type=float)
    max_fare = request.args.get('max_fare', type=float)
    min_distance = request.args.get('min_distance', type=float)
    max_distance = request.args.get('max_distance', type=float)

    query = 'SELECT * FROM trips'
    filters = []
    params = []

    if date_from:
        filters.append('pickup_datetime >= ?')
        params.append(date_from)
    if date_to:
        filters.append('pickup_datetime <= ?')
        params.append(date_to)
    if min_fare is not None:
        filters.append('fare_amount >= ?')
        params.append(min_fare)
    if max_fare is not None:
        filters.append('fare_amount <= ?')
        params.append(max_fare)
    if min_distance is not None:
        filters.append('trip_distance >= ?')
        params.append(min_distance)
    if max_distance is not None:
        filters.append('trip_distance <= ?')
        params.append(max_distance)

    if filters:
        query += ' WHERE ' + ' AND '.join(filters)

    query += ' LIMIT ? OFFSET ?'
    params.extend([limit, offset])

    conn = get_db_connection()
    trips = conn.execute(query, tuple(params)).fetchall()
    conn.close()
    return jsonify([dict(ix) for ix in trips])

@app.route('/api/trips/count', methods=['GET'])
def get_trips_count():
    
    date_from = request.args.get('date_from')
    date_to = request.args.get('date_to')
    min_fare = request.args.get('min_fare', type=float)
    max_fare = request.args.get('max_fare', type=float)
    min_distance = request.args.get('min_distance', type=float)
    max_distance = request.args.get('max_distance', type=float)

    query = 'SELECT COUNT(*) FROM trips'
    filters = []
    params = []

    if date_from:
        filters.append('pickup_datetime >= ?')
        params.append(date_from)
    if date_to:
        filters.append('pickup_datetime <= ?')
        params.append(date_to)
    if min_fare is not None:
        filters.append('fare_amount >= ?')
        params.append(min_fare)
    if max_fare is not None:
        filters.append('fare_amount <= ?')
        params.append(max_fare)
    if min_distance is not None:
        filters.append('trip_distance >= ?')
        params.append(min_distance)
    if max_distance is not None:
        filters.append('trip_distance <= ?')
        params.append(max_distance)

    if filters:
        query += ' WHERE ' + ' AND '.join(filters)

    conn = get_db_connection()
    count = conn.execute(query, tuple(params)).fetchone()[0]
    conn.close()
    return jsonify({'count': count})

@app.route('/api/trips/ranked', methods=['GET'])
def get_ranked_trips():
    sort_by = request.args.get('sort_by', 'fare_per_km')
    order = request.args.get('order', 'desc')

    if order not in ['asc', 'desc']:
        return jsonify({"error": "Invalid order parameter. Use 'asc' or 'desc'."}), 400

    descending = (order == 'desc')

    conn = get_db_connection()
   
    trips_cursor = conn.execute('SELECT * FROM trips WHERE fare_per_km IS NOT NULL AND fare_per_km > 0').fetchall()
    conn.close()    

    trips_list = [dict(ix) for ix in trips_cursor]

    
    ranked_trips = manual_sort(trips_list, key=sort_by, descending=descending)

    return jsonify(ranked_trips[:100])

if __name__ == '__main__':
   
    app.run(debug=True, port=5011)
    print(app.url_map)