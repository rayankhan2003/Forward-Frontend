document.addEventListener('DOMContentLoaded', function () {

    /* ── Enrollment Trends bar chart ── */
    const barCtx = document.getElementById('enrollmentChart');
    if (barCtx && typeof trendsData !== 'undefined') {
        new Chart(barCtx.getContext('2d'), {
            type: 'bar',
            data: trendsData,
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true,
                        grid: { color: '#E2E8F0', drawBorder: false },
                        ticks: { font: { family: 'Inter', size: 11 } }
                    },
                    x: {
                        grid: { display: false },
                        ticks: {
                            font: { family: 'Inter', size: 11, weight: '700' },
                            color: '#0F172A'
                        }
                    }
                },
                plugins: {
                    legend: {
                        position: 'top',
                        align: 'end',
                        labels: {
                            usePointStyle: true,
                            pointStyle: 'circle',
                            padding: 20,
                            font: { family: 'Inter', size: 12, weight: '600' }
                        }
                    }
                },
                barPercentage: 0.45,
                categoryPercentage: 0.6
            }
        });
    }

    /* ── Student Demographics donut ── */
    // Removed as per UI update: Demographics card is no longer part of the dashboard.

    /* ── Campus performance mini-donuts ── */
    document.querySelectorAll('.donut-chart').forEach(function (canvas) {
        const perf = parseInt(canvas.getAttribute('data-performance'), 10);
        new Chart(canvas.getContext('2d'), {
            type: 'doughnut',
            data: {
                datasets: [{
                    data: [perf, 100 - perf],
                    backgroundColor: ['#1D4ED8', '#E2E8F0'],
                    borderWidth: 0
                }]
            },
            options: {
                responsive: false,
                cutout: '68%',
                plugins: { legend: { display: false }, tooltip: { enabled: false } }
            }
        });
    });

    /* ── Reports: Attendance Trends line chart ── */
    const attCtx = document.getElementById('attendanceChart');
    if (attCtx && typeof attendanceData !== 'undefined') {
        new Chart(attCtx.getContext('2d'), {
            type: 'line',
            data: attendanceData,
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: { beginAtZero: false, min: 75, max: 100, grid: { color: '#E2E8F0' }, ticks: { font: { family: 'Inter', size: 11 } } },
                    x: { grid: { display: false }, ticks: { font: { family: 'Inter', size: 11 } } }
                },
                plugins: {
                    legend: { position: 'top', align: 'end', labels: { usePointStyle: true, pointStyle: 'circle', padding: 20, font: { family: 'Inter', size: 12, weight: '600' } } }
                }
            }
        });
    }

    /* ── Reports: Grade Distribution bar chart ── */
    const gradeCtx = document.getElementById('gradeChart');
    if (gradeCtx && typeof gradeData !== 'undefined') {
        new Chart(gradeCtx.getContext('2d'), {
            type: 'bar',
            data: gradeData,
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: { beginAtZero: true, grid: { color: '#E2E8F0' }, ticks: { font: { family: 'Inter', size: 11 } } },
                    x: { grid: { display: false }, ticks: { font: { family: 'Inter', size: 12, weight: '700' }, color: '#0F172A' } }
                },
                plugins: { legend: { display: false } },
                barPercentage: 0.55
            }
        });
    }
});

