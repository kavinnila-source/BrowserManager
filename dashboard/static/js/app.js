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

    addActivity("Start Button Clicked");

    alert("Start button clicked");

});

document.getElementById("stopBtn").addEventListener("click", () => {

    addActivity("Stop Button Clicked");

    alert("Stop button clicked");

});

document.getElementById("restartBtn").addEventListener("click", () => {

    alert("Restart button clicked");

});

function addActivity(message){

const log=document.getElementById("activityLog");

if(!log) return;

const item=document.createElement("div");

item.className="activity-item";

item.innerHTML=new Date().toLocaleTimeString()+" - "+message;

log.prepend(item);

}

document.getElementById("refreshBtn").addEventListener("click",()=>{

addActivity("Dashboard Refreshed");

});

const themeBtn = document.getElementById("themeToggle");

if (themeBtn) {

    if (localStorage.getItem("theme") === "light") {
        document.body.classList.add("light-theme");
        themeBtn.innerHTML = "☀ Dark Theme";
    } else {
        themeBtn.innerHTML = "🌙 Light Theme";
    }

    themeBtn.addEventListener("click", () => {

        document.body.classList.toggle("light-theme");

        const light = document.body.classList.contains("light-theme");

        localStorage.setItem("theme", light ? "light" : "dark");

        themeBtn.innerHTML = light ? "☀ Dark Theme" : "🌙 Light Theme";

    });

}

// ===== Step 9 =====
document.addEventListener("DOMContentLoaded",()=>{
const settingsForm=document.getElementById("settingsForm");
if(settingsForm){
 const saved=JSON.parse(localStorage.getItem("bm_settings")||"{}");
 Object.keys(saved).forEach(k=>{
   const el=document.getElementById(k);
   if(el){
     if(el.type==="checkbox") el.checked=saved[k];
     else el.value=saved[k];
   }
 });
 settingsForm.addEventListener("submit",e=>{
   e.preventDefault();
   const data={
     browserCount:document.getElementById("browserCount")?.value,
     defaultUrl:document.getElementById("defaultUrl")?.value,
     refreshInterval:document.getElementById("refreshInterval")?.value,
     autoRefresh:document.getElementById("autoRefresh")?.checked
   };
   localStorage.setItem("bm_settings",JSON.stringify(data));
   addActivity("Settings Saved");
   alert("Settings saved successfully.");
 });
}
});


async function refreshNotifications(){
    try{
        const res=await fetch("/api/notifications");
        const data=await res.json();
        const box=document.getElementById("notificationBox");
        if(!box) return;
        const badge=document.getElementById("notificationCount");
        if(badge){
            badge.textContent=(data.notifications||[]).length;
        }
        box.innerHTML="";
        (data.notifications||[]).slice(0,10).forEach(n=>{
            const div=document.createElement("div");
            div.className="alert alert-"+(
                n.level==="error"?"danger":
                n.level==="warning"?"warning":
                n.level==="success"?"success":"info"
            )+" mb-2";
            div.textContent=`${n.time} - ${n.title}: ${n.message}`;
            box.appendChild(div);
        });
    }catch(e){
        console.error(e);
    }
}
setInterval(refreshNotifications,2000);
refreshNotifications();
