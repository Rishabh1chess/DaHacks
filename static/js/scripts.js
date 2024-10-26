document.addEventListener('DOMContentLoaded', function() {
    const playButton = document.getElementById('playButton');
    const ctx = document.getElementById('simulationChart').getContext('2d');
    let chart = null; // To store the Chart instance

    playButton.addEventListener('click', function() {
        // Disable the Play button to prevent multiple clicks
        playButton.disabled = true;
        playButton.textContent = 'Running...';

        fetch('/simulate')
            .then(response => response.json())
            .then(data => {
                // If a chart already exists, destroy it before creating a new one
                if (chart) {
                    chart.destroy();
                }

                chart = new Chart(ctx, {
                    type: 'line',
                    data: {
                        labels: data.time,
                        datasets: [{
                            label: 'Mass Over Time',
                            data: data.mass,
                            borderColor: 'rgba(255, 0, 0, 1)',
                            backgroundColor: 'rgba(255, 0, 0, 0.2)',
                            fill: true
                        }]
                    },
                    options: {
                        scales: {
                            x: {
                                title: {
                                    display: true,
                                    text: 'Time'
                                }
                            },
                            y: {
                                title: {
                                    display: true,
                                    text: 'Mass'
                                }
                            }
                        },
                        plugins: {
                            title: {
                                display: true,
                                text: 'Black Hole Mass Simulation'
                            }
                        }
                    }
                });

                // Re-enable the Play button after simulation completes
                playButton.disabled = false;
                playButton.textContent = 'Play';
            })
            .catch(error => {
                console.error('Error fetching simulation data:', error);
                alert('Failed to run the simulation. Please try again.');

                // Re-enable the Play button in case of error
                playButton.disabled = false;
                playButton.textContent = 'Play';
            });
    });
});

