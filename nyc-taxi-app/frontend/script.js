let allTrips = [];
let tripDistanceChart = null;
let passengerCountChart = null;

document.addEventListener('DOMContentLoaded', () => {
    // Fetch and display general trips
    fetch('http://127.0.0.1:5011/api/trips')
        .then(response => response.json())
        .then(data => {
            allTrips = data;
            populateTable(allTrips);
            createTripDistanceChart(allTrips);
            createPassengerCountChart(allTrips);
        })
        .catch(error => console.error('Error fetching data:', error));

    // Add event listener for the filter button
    document.getElementById('filterBtn').addEventListener('click', () => {
        const minDistance = parseFloat(document.getElementById('minDistance').value);
        
        const filteredTrips = allTrips.filter(trip => trip.trip_distance >= minDistance);
        
        populateTable(filteredTrips);
        createTripDistanceChart(filteredTrips);
        createPassengerCountChart(filteredTrips);
    });
});

function populateTable(trips) {
    const tableBody = document.querySelector('#tripsTable tbody');
    tableBody.innerHTML = ''; // Clear existing data
    trips.forEach(trip => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${trip.id}</td>
            <td>${trip.pickup_datetime}</td>
            <td>${trip.trip_distance}</td>
        `;
        tableBody.appendChild(row);
    });
}

function createTripDistanceChart(trips) {
    if (tripDistanceChart) {
        tripDistanceChart.destroy();
    }

    const ctx = document.getElementById('tripDistanceChart').getContext('2d');
    
    tripDistanceChart = new Chart(ctx, {
        type: 'scatter',
        data: {
            datasets: [{
                label: 'Trip Distance vs. Trip Duration',
                data: trips.map(t => ({x: t.trip_distance, y: t.trip_duration})),
                backgroundColor: 'rgba(75, 192, 192, 0.6)'
            }]
        },
        options: {
            scales: {
                x: {
                    type: 'linear',
                    position: 'bottom',
                    title: {
                        display: true,
                        text: 'Trip Distance (miles)'
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: 'Trip Duration (seconds)'
                    }
                }
            }
        }
    });
}

function createPassengerCountChart(trips) {
    if (passengerCountChart) {
        passengerCountChart.destroy();
    }

    const ctx = document.getElementById('passengerCountChart').getContext('2d');

    const passengerCounts = trips.reduce((acc, trip) => {
        acc[trip.passenger_count] = (acc[trip.passenger_count] || 0) + 1;
        return acc;
    }, {});

    passengerCountChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: Object.keys(passengerCounts),
            datasets: [{
                label: 'Number of Trips by Passenger Count',
                data: Object.values(passengerCounts),
                backgroundColor: 'rgba(153, 102, 255, 0.6)'
            }]
        },
        options: {
            scales: {
                x: {
                    title: {
                        display: true,
                        text: 'Passenger Count'
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: 'Number of Trips'
                    },
                    beginAtZero: true
                }
            }
        }
    });
}