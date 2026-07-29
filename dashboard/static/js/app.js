// =========================================
// BrowserManager v2.2 Dashboard + Chart.js
// dashboard/static/js/app.js
// =========================================

// ----------------------------
// Chart Data
// ----------------------------

const labels = [];
const cpuHistory = [];
const ramHistory = [];

// ----------------------------
// CPU Chart
// ----------------------------

const cpuChart = new Chart(
    document.getElementById("cpuChart"),
    {
        type: "line",
        data: {
            labels: labels,
            datasets: [{
                label: "CPU %",
                data: cpuHistory,
                borderWidth: 3,
                tension: 0.35,
                fill: false
            }]
        },
        options: {
            responsive: true,
            animation: false,
            plugins: {
                legend: {
                    display: true
                }
            },
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    }
);

// ----------------------------
// RAM Chart
// ----------------------------

const ramChart = new Chart(
    document.getElementById("ramChart"),
    {
        type: "line",
        data: {
            labels: labels,
            datasets: [{
                label: "RAM (MB)",
                data: ramHistory,
                borderWidth: 3,
                tension: 0.35,
                fill: false
            }]
        },
        options: {
            responsive: true,
            animation: false,
            plugins: {
                legend: {
                    display: true
                }
            },
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    }
);

// ----------------------------
// Update Charts
// ----------------------------

function updateCharts(summary) {

    const now = new Date().toLocaleTimeString();

    labels.push(now);
    cpuHistory.push(summary.total_cpu);
    ramHistory.push(summary.total_ram);

    if (labels.length > 20) {
        labels.shift();
        cpuHistory.shift();
        ramHistory.shift();
    }

    cpuChart.update();
    ramChart.update();
}

// ----------------------------
// Refresh Dashboard
// ----------------------------

async function refreshDashboard() {

    try {

        const response = await fetch("/api/stats");

        if (!response.ok) {
            throw new Error("Failed to fetch dashboard data.");
        }

        const data = await response.json();

        document.getElementById("runningCount").innerHTML=data.summary.running;

        document.getElementById("totalBrowsers").innerHTML=data.summary.running;

        document.getElementById("ramUsage").innerHTML=data.summary.total_ram+" MB";

        document.getElementById("cpuUsage").innerHTML=data.summary.total_cpu+"%";

        // Summary Cards

        const running = document.getElementById("running");
        const totalRam = document.getElementById("total_ram");
        const totalCpu = document.getElementById("total_cpu");

        if (running) {
            running.textContent = data.summary.running;
        }

        if (totalRam) {
            totalRam.textContent =
                data.summary.total_ram + " MB";
        }

        if (totalCpu) {
            totalCpu.textContent =
                data.summary.total_cpu + " %";
        }

        // Update Charts

        updateCharts(data.summary);

    }
    catch (error) {

        console.error("Dashboard Update Error:", error);

    }

}

// ----------------------------
// Initial Load
// ----------------------------

refreshDashboard();

// ----------------------------
// Auto Refresh Every 2 Seconds
// ----------------------------

setInterval(refreshDashboard, 2000);

function updateClock(){

    const now=new Date();

    document.getElementById("liveTime").innerHTML=
        now.toLocaleTimeString();

    document.getElementById("liveDate").innerHTML =
    now.toLocaleDateString("en-GB", {
        day: "2-digit",
        month: "long",
        year: "numeric"
    });

}

updateClock();

setInterval(updateClock,1000);

document.getElementById("refreshBtn").addEventListener("click", () => {

    refreshDashboard();

});

document.getElementById("startBtn").addEventListener("click", () => {

    alert("Start button clicked");

});

document.getElementById("stopBtn").addEventListener("click", () => {

    alert("Stop button clicked");

});

document.getElementById("restartBtn").addEventListener("click", () => {

    alert("Restart button clicked");

});