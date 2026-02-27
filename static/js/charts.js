/*
 * charts.js - Chart rendering functions using Chart.js
 * Used by dashboard.html and reports/analysis.html
 */

// Color palette
const CHART_COLORS = [
    '#1e3a5f', '#2d5a8e', '#4a90d9', '#64b5f6',
    '#81c784', '#ffb74d', '#e57373', '#ba68c8',
    '#4db6ac', '#f06292'
];

/**
 * Render a Line Chart (monthly revenue trend)
 */
function renderLineChart(canvasId, labels, data, label) {
    const ctx = document.getElementById(canvasId);
    if (!ctx) return;
    if (ctx._chartInstance) ctx._chartInstance.destroy();

    ctx._chartInstance = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: label,
                data: data,
                borderColor: '#2d5a8e',
                backgroundColor: 'rgba(45, 90, 142, 0.1)',
                borderWidth: 2.5,
                pointBackgroundColor: '#1e3a5f',
                pointRadius: 5,
                pointHoverRadius: 7,
                fill: true,
                tension: 0.4
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: { display: false },
                tooltip: {
                    callbacks: {
                        label: ctx => '\u20B9' + ctx.raw.toLocaleString('en-IN')
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: { callback: value => '\u20B9' + value.toLocaleString('en-IN') },
                    grid: { color: 'rgba(0,0,0,0.05)' }
                },
                x: { grid: { display: false } }
            }
        }
    });
}

/**
 * Render a Doughnut / Pie Chart (category breakdown)
 */
function renderPieChart(canvasId, labels, data) {
    const ctx = document.getElementById(canvasId);
    if (!ctx) return;
    if (ctx._chartInstance) ctx._chartInstance.destroy();

    ctx._chartInstance = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: labels,
            datasets: [{
                data: data,
                backgroundColor: CHART_COLORS,
                borderWidth: 2,
                borderColor: '#fff'
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: { font: { size: 11 } }
                },
                tooltip: {
                    callbacks: {
                        label: ctx => `${ctx.label}: \u20B9${ctx.raw.toLocaleString('en-IN')}`
                    }
                }
            }
        }
    });
}

/**
 * Render a Bar Chart (top products by revenue)
 */
function renderBarChart(canvasId, labels, data, label) {
    const ctx = document.getElementById(canvasId);
    if (!ctx) return;
    if (ctx._chartInstance) ctx._chartInstance.destroy();

    ctx._chartInstance = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: label,
                data: data,
                backgroundColor: CHART_COLORS,
                borderRadius: 6,
                borderSkipped: false
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: { display: false },
                tooltip: {
                    callbacks: {
                        label: ctx => '\u20B9' + ctx.raw.toLocaleString('en-IN')
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: { callback: value => '\u20B9' + value.toLocaleString('en-IN') },
                    grid: { color: 'rgba(0,0,0,0.05)' }
                },
                x: {
                    grid: { display: false },
                    ticks: { maxRotation: 30, font: { size: 10 } }
                }
            }
        }
    });
}

// Sidebar toggle for mobile
document.addEventListener('DOMContentLoaded', function () {
    const toggleBtn = document.getElementById('sidebarToggle');
    const sidebar = document.getElementById('sidebar-wrapper');
    if (toggleBtn && sidebar) {
        toggleBtn.addEventListener('click', () => sidebar.classList.toggle('active'));
    }
});
