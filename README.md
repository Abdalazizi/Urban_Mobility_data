# NYC Taxi Trip Analysis Full-Stack Application

This is a full-stack web application for analyzing and visualizing the NYC Taxi Trip dataset. It provides a user-friendly interface to filter, sort, and explore taxi trip data, offering insights into trip durations, distances, fares, and popular pickup locations.

## Live Demo

[Link to a live demo of the application]

## Features

### Frontend

*   **Interactive Dashboard:** A modern and responsive dashboard to visualize taxi trip data.
*   **Data Filtering:** Filter trips by date range, fare amount, and trip distance.
*   **Data Sorting:** Sort trips by pickup time, distance, fare, and total amount.
*   **Data Visualization:**
    *   A bar chart showing the number of trips by hour.
    *   A scatter plot visualizing the geographic distribution of pickup locations.
*   **Pagination:** Paginate through the trip records for efficient browsing.
*   **Real-time Statistics:** View key statistics such as total trips, total revenue, average distance, and average fare.
*   **Toast Notifications:** User-friendly notifications for loading status and errors.

### Backend

*   **RESTful API:** A Flask-based backend that exposes a RESTful API to the frontend.
*   **Data Processing:** A script to process the raw CSV data, clean it, and insert it into a database.
*   **Database Integration:** Uses SQLite to store and manage the taxi trip data.
*   **Custom Sorting Algorithm:** Implements a manual quicksort algorithm for ranking trips.
*   **Efficient Data Handling:** Processes large datasets in chunks to manage memory usage.
*   **Foreign Key Relationships:** Enforces data integrity between `trips` and `vendors` tables.

## System Architecture

The application is divided into two main components:

*   **Frontend:** A vanilla JavaScript, HTML, and CSS application that runs in the browser. It communicates with the backend via HTTP requests to fetch and display data.
*   **Backend:** A Python Flask application that serves the data to the frontend. It includes a data processing pipeline to clean and populate the database from a raw CSV file.

## Technologies Used

*   **Frontend:**
    *   HTML5
    *   CSS3
    *   JavaScript (ES6+)
    *   [Chart.js](https://www.chartjs.org/) for data visualization
*   **Backend:**
    *   Python 3
    *   [Flask](https://flask.palletsprojects.com/) for the web framework
    *   [Pandas](https://pandas.pydata.org/) for data manipulation
    *   [SQLite](https://www.sqlite.org/) for the database
*   **Development Tools:**
    *   [VS Code](https://code.visualstudio.com/)
    *   [Git](https://git-scm.com/) & [GitHub](https://github.com/)

## Getting Started

To get a local copy up and running, follow these simple steps.

### Prerequisites

*   Python 3.x
*   pip (Python package installer)
*   A web browser

### Backend Setup

1.  **Navigate to the backend directory:**
    ```bash
    cd nyc-taxi-app/backend
    ```

2.  **Install Python dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the data processing script:**
    This script will clean the raw `train.csv` data, create a SQLite database (`taxi_trips.db`), and populate it. This is a one-time setup process and may take a significant amount of time.
    *Note: Make sure the `train.csv` file is located in the root directory of the project (`/home/abdalazizi/Desktop/assignment_01`).*
    ```bash
    python3 data_processing.py
    ```

4.  **Start the backend server:**
    ```bash
    python3 app.py &
    ```
    The backend server will be running at `http://127.0.0.1:5001`.

### Frontend Setup

1.  **Navigate to the frontend directory:**
    ```bash
    cd nyc-taxi-app/frontend
    ```

2.  **Start a simple web server:**
    ```bash
    python3 -m http.server 8080 &
    ```

3.  **Access the application:**
    Open your web browser and navigate to `http://localhost:8080`.

## API Endpoints

The backend provides the following API endpoints:

*   `GET /api/trips`: Fetches a paginated list of trips.
    *   **Query Parameters:**
        *   `page`: The page number to retrieve.
        *   `limit`: The number of trips per page.
        *   `date_from`, `date_to`: Filter by pickup date.
        *   `min_fare`, `max_fare`: Filter by fare amount.
        *   `min_distance`, `max_distance`: Filter by trip distance.
*   `GET /api/trips/count`: Returns the total number of trips that match the applied filters.
*   `GET /api/trips/ranked`: Returns the top 100 trips ranked by a specified field.
    *   **Query Parameters:**
        *   `sort_by`: The field to sort by (e.g., `fare_per_km`).
        *   `order`: The sort order (`asc` or `desc`).

## Database Schema

The application uses a SQLite database with two tables:

*   **`vendors`**: Stores information about the taxi vendors.
    *   `id` (INTEGER, PRIMARY KEY)
    *   `fullname` (TEXT)
*   **`trips`**: Stores the taxi trip data.
    *   `id` (TEXT, UNIQUE)
    *   `vendor_id` (INTEGER, FOREIGN KEY to `vendors.id`)
    *   `pickup_datetime` (TEXT)
    *   `dropoff_datetime` (TEXT)
    *   `passenger_count` (INTEGER)
    *   `trip_distance` (REAL)
    *   `pickup_longitude` (REAL)
    *   `pickup_latitude` (REAL)
    *   `dropoff_longitude` (REAL)
    *   `dropoff_latitude` (REAL)
    *   `fare_amount` (REAL)
    *   `tip_amount` (REAL)
    *   `trip_duration` (REAL)
    *   `trip_speed` (REAL)
    *   `fare_per_km` (REAL)
    *   `idle_time` (REAL)

## Custom Algorithm

The backend includes a custom implementation of the **Quick Sort** algorithm (`manual_sort` in `custom_algorithm.py`) to rank trips. This function can sort a list of dictionaries by a specified key in either ascending or descending order. It is used by the `/api/trips/ranked` endpoint to provide a ranked list of trips based on criteria like fare per kilometer.

### Time Complexity

The Quick Sort algorithm has the following time complexity:

*   **Best Case:** O(n log n)
*   **Average Case:** O(n log n)
*   **Worst Case:** O(n^2)

In our implementation, the worst-case scenario is unlikely to occur with the given dataset, so we can expect an average time complexity of O(n log n).

#### Visualizing Time Complexity

To see how the execution time of the `manual_sort` function scales with the input size, you can run the `time_complexity_test.py` script:

```bash
cd nyc-taxi-app/backend
python3 time_complexity_test.py
```

This will run the sort algorithm on datasets of increasing sizes and print the execution time for each. You should observe that the execution time does not grow quadratically, which is consistent with the O(n log n) average time complexity.

**Example Output:**

```
Running time complexity test for manual_sort...

Input size: 100        | Execution time: 0.000123 seconds
Input size: 1000       | Execution time: 0.001512 seconds
Input size: 10000      | Execution time: 0.019865 seconds
Input size: 50000      | Execution time: 0.124581 seconds
```

### Custom Algorithm in Action

You can see the custom sorting algorithm in action by calling the `/api/trips/ranked` endpoint. For example, to get the top trips with the highest fare per kilometer, you can use the following `curl` command:

```bash
curl "http://127.0.0.1:5001/api/trips/ranked?sort_by=fare_per_km&order=desc"
```

This will return a JSON response with the top 100 trips, sorted by `fare_per_km` in descending order. Here is a sample of the output:

```json
[
  {
    "dropoff_datetime": "2016-03-14 17:32:26",
    "fare_amount": 20.8,
    "fare_per_km": 5.2,
    "id": "id2875421",
    "idle_time": 0,
    "passenger_count": 1,
    "pickup_datetime": "2016-03-14 17:24:55",
    "pickup_latitude": 40.767937,
    "pickup_longitude": -73.982155,
    "tip_amount": 0.0,
    "trip_distance": 4.0,
    "trip_duration": 451,
    "trip_speed": 32.0,
    "vendor_id": 1
  },
  {
    "dropoff_datetime": "2016-03-14 17:32:26",
    "fare_amount": 18.4,
    "fare_per_km": 4.6,
    "id": "id2875422",
    "idle_time": 0,
    "passenger_count": 1,
    "pickup_datetime": "2016-03-14 17:24:55",
    "pickup_latitude": 40.767937,
    "pickup_longitude": -73.982155,
    "tip_amount": 0.0,
    "trip_distance": 4.0,
    "trip_duration": 451,
    "trip_speed": 32.0,
    "vendor_id": 1
  }
]
```

## Contributing

Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1.  Fork the Project
2.  Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3.  Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4.  Push to the Branch (`git push origin feature/AmazingFeature`)
5.  Open a Pull Request

## License

This project is licensed under the MIT License. See the `LICENSE` file for more information.
