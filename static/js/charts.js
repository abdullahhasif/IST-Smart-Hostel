// Charts for the Smart Hostel System

// Initialize all charts when document is ready
document.addEventListener('DOMContentLoaded', function() {
    // Check if we're on the stats page
    if (document.getElementById('roomTypeChart')) {
        initializeRoomCharts();
    }
    
    if (document.getElementById('complaintStatusChart')) {
        initializeComplaintCharts();
    }
    
    if (document.getElementById('hostelOccupancyChart')) {
        initializeHostelCharts();
    }
});

// Room statistics charts
function initializeRoomCharts() {
    // Fetch room statistics data
    fetch('/api/room-stats')
        .then(response => response.json())
        .then(data => {
            // Room types chart
            const roomTypeCtx = document.getElementById('roomTypeChart').getContext('2d');
            new Chart(roomTypeCtx, {
                type: 'pie',
                data: {
                    labels: data.room_types.labels,
                    datasets: [{
                        data: data.room_types.data,
                        backgroundColor: [
                            'rgba(75, 192, 192, 0.7)',
                            'rgba(153, 102, 255, 0.7)',
                            'rgba(255, 159, 64, 0.7)'
                        ],
                        borderColor: [
                            'rgba(75, 192, 192, 1)',
                            'rgba(153, 102, 255, 1)',
                            'rgba(255, 159, 64, 1)'
                        ],
                        borderWidth: 1
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: {
                            position: 'right',
                        },
                        title: {
                            display: true,
                            text: 'Room Distribution by Type'
                        }
                    }
                }
            });
            
            // Room availability chart
            const availabilityCtx = document.getElementById('roomAvailabilityChart').getContext('2d');
            new Chart(availabilityCtx, {
                type: 'doughnut',
                data: {
                    labels: data.availability.labels,
                    datasets: [{
                        data: data.availability.data,
                        backgroundColor: [
                            'rgba(40, 167, 69, 0.7)',
                            'rgba(220, 53, 69, 0.7)'
                        ],
                        borderColor: [
                            'rgba(40, 167, 69, 1)',
                            'rgba(220, 53, 69, 1)'
                        ],
                        borderWidth: 1
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: {
                            position: 'right',
                        },
                        title: {
                            display: true,
                            text: 'Room Availability Status'
                        }
                    }
                }
            });
        })
        .catch(error => console.error('Error fetching room stats:', error));
}

// Complaint statistics charts
function initializeComplaintCharts() {
    // Fetch complaint statistics data
    fetch('/api/complaint-stats')
        .then(response => response.json())
        .then(data => {
            // Complaint status chart
            const statusCtx = document.getElementById('complaintStatusChart').getContext('2d');
            new Chart(statusCtx, {
                type: 'pie',
                data: {
                    labels: data.status.labels,
                    datasets: [{
                        data: data.status.data,
                        backgroundColor: [
                            'rgba(0, 123, 255, 0.7)',
                            'rgba(102, 16, 242, 0.7)',
                            'rgba(40, 167, 69, 0.7)'
                        ],
                        borderColor: [
                            'rgba(0, 123, 255, 1)',
                            'rgba(102, 16, 242, 1)',
                            'rgba(40, 167, 69, 1)'
                        ],
                        borderWidth: 1
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: {
                            position: 'right',
                        },
                        title: {
                            display: true,
                            text: 'Complaints by Status'
                        }
                    }
                }
            });
            
            // Complaint category chart
            const categoryCtx = document.getElementById('complaintCategoryChart').getContext('2d');
            new Chart(categoryCtx, {
                type: 'bar',
                data: {
                    labels: data.category.labels,
                    datasets: [{
                        label: 'Number of Complaints',
                        data: data.category.data,
                        backgroundColor: 'rgba(0, 123, 255, 0.7)',
                        borderColor: 'rgba(0, 123, 255, 1)',
                        borderWidth: 1
                    }]
                },
                options: {
                    responsive: true,
                    scales: {
                        y: {
                            beginAtZero: true,
                            ticks: {
                                precision: 0
                            }
                        }
                    },
                    plugins: {
                        legend: {
                            display: false
                        },
                        title: {
                            display: true,
                            text: 'Complaints by Category'
                        }
                    }
                }
            });
        })
        .catch(error => console.error('Error fetching complaint stats:', error));
}

// Hostel statistics charts
function initializeHostelCharts() {
    // Fetch hostel statistics data
    fetch('/api/hostel-stats')
        .then(response => response.json())
        .then(data => {
            // Hostel occupancy chart
            const hostelCtx = document.getElementById('hostelOccupancyChart').getContext('2d');
            new Chart(hostelCtx, {
                type: 'bar',
                data: {
                    labels: data.labels,
                    datasets: [
                        {
                            label: 'Occupied Rooms',
                            data: data.occupied,
                            backgroundColor: 'rgba(220, 53, 69, 0.7)',
                            borderColor: 'rgba(220, 53, 69, 1)',
                            borderWidth: 1
                        },
                        {
                            label: 'Available Rooms',
                            data: data.available,
                            backgroundColor: 'rgba(40, 167, 69, 0.7)',
                            borderColor: 'rgba(40, 167, 69, 1)',
                            borderWidth: 1
                        }
                    ]
                },
                options: {
                    responsive: true,
                    scales: {
                        x: {
                            stacked: true,
                        },
                        y: {
                            stacked: true,
                            beginAtZero: true,
                            ticks: {
                                precision: 0
                            }
                        }
                    },
                    plugins: {
                        title: {
                            display: true,
                            text: 'Hostel Occupancy Status'
                        }
                    }
                }
            });
        })
        .catch(error => console.error('Error fetching hostel stats:', error));
    
    // If student occupancy data is available, create that chart
    if (document.getElementById('studentOccupancyChart')) {
        // For this MVP, we'll create a simple demo chart with placeholder data
        const studentCtx = document.getElementById('studentOccupancyChart').getContext('2d');
        new Chart(studentCtx, {
            type: 'line',
            data: {
                labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July'],
                datasets: [{
                    label: 'Student Occupancy Rate (%)',
                    data: [65, 70, 80, 85, 75, 50, 70],
                    backgroundColor: 'rgba(0, 123, 255, 0.2)',
                    borderColor: 'rgba(0, 123, 255, 1)',
                    borderWidth: 2,
                    tension: 0.4,
                    fill: true
                }]
            },
            options: {
                responsive: true,
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 100,
                        ticks: {
                            callback: function(value) {
                                return value + '%';
                            }
                        }
                    }
                },
                plugins: {
                    title: {
                        display: true,
                        text: 'Student Occupancy Trend'
                    }
                }
            }
        });
    }
}
