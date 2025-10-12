# NYC Taxi Trip Analysis Full-Stack Application

This project is a full-stack web application for analyzing and visualizing the NYC Taxi Trip dataset. It was built to demonstrate data processing, database design, backend API development, and frontend data visualization.

## Project Structure

- `/backend`: Contains the Flask backend application, data processing scripts, and the SQLite database.
- `/frontend`: Contains the vanilla HTML, CSS, and JavaScript frontend application.

## Setup and Installation

### Prerequisites

- Python 3.x
- pip (Python package installer)
- A web browser

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

## Video Walkthrough

[Link to your 5-minute video walkthrough will go here.]

## Documentation

This project also includes a detailed PDF documentation report that covers:
- Problem Framing and Dataset Analysis
- System Architecture and Design Decisions
- Algorithmic Logic and Data Structures (including an analysis of the manually implemented Quick Sort algorithm)
- Insights and Interpretation from the data
- Reflection and Future Work
