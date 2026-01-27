
/* ================================
   Config
================================ */
let harvestPieChart = null;
let revenueChart = null;

/* ================================
   API Helper
================================ */
/* ================================
   API Helper (NO TOKEN HERE)
================================ */
async function apiFetch(endpoint, options = {}) {
  const res = await fetch(`/api${endpoint}`, {
    credentials: "include",
    ...options
  });

  if (!res.ok) {
    const text = await res.text();
    throw new Error(`API ${res.status}: ${text}`);
  }

  // Caller decides how to read response
  return res.json();
}



/* ================================
   Date Helper
================================ */
function todayISO() {
  return new Date().toISOString().split("T")[0];
  //return "2026-01-05"
}

/* ================================
   Load Today's Harvest (Top Card)
================================ */
async function loadTodayHarvest() {
  const raw = await apiFetch("/harvest/amount/daily");
  const items = raw?.data?.items;

  if (!Array.isArray(items)) {
    throw new Error("Invalid daily harvest response");
  }

  const today = todayISO();

  const total = items
    .filter(d => d.period === today)
    .reduce((sum, d) => sum + Number(d.total_count), 0);

  document.getElementById("today_har").innerText =
    `${total.toFixed(1)} Kg`;
}

/* ================================
   Aggregate by Size (Pie Chart)
================================ */
function aggregateBySize(items) {
  const map = {};

  items.forEach(d => {
    const size = d.size_name || "Unknown";
    map[size] = (map[size] || 0) + Number(d.total_count);
  });

  return {
    labels: Object.keys(map),
    values: Object.values(map)
  };
}

/* ================================
   Harvest Summary Pie Chart
================================ */
async function loadharvestPieChart() {
  const today = todayISO();
  const SIZES = ["L", "M", "S", "SS", "3S", "小"];

  const results = await Promise.all(
    SIZES.map(async sizeId => {
      const raw = await apiFetch(
        `/harvest/amount/daily/size/${sizeId}`
      );

      const items = raw?.data?.items || [];

      const todayTotal = items
        .filter(d => d.period === today)
        .reduce((sum, d) => sum + Number(d.total_count), 0);

      return {
        size: sizeId,
        value: todayTotal
      };
    })
  );

  const labels = results.map(r => r.size);
  const values = results.map(r => r.value);

  if (harvestPieChart) harvestPieChart.destroy();

  harvestPieChart = new Chart(
    document.getElementById("harvestChart"),
    {
      type: "pie",
      data: {
        labels,
        datasets: [
          {
            data: values
          }
        ]
      },
      options: {
        responsive: true,
        plugins: {
          legend: {
            position: "bottom"
          }
        }
      }
    }
  );
}


/* ================================
   Load Revenue Chart
================================ */
async function loadRevenueChart() {
  try {
    const raw = await apiFetch("/analytics/revenue/monthly");
    const items = raw?.data?.items;

    if (!Array.isArray(items)) {
      throw new Error("Invalid revenue data");
    }

    const labels = items.map(d => d.period);
    const values = items.map(d => Number(d.revenue_yen));

    renderRevenueChart(labels, values);
  } catch (err) {
    renderConfidentialRevenue();
  }
}

/* ================================
   Render REAL chart
================================ */
function renderRevenueChart(labels, values) {
  hideConfidentialOverlay();

  if (revenueChart) revenueChart.destroy();

  revenueChart = new Chart(
    document.getElementById("revenueChart"),
    {
      type: "bar",
      data: {
        labels,
        datasets: [
          {
            label: "収益 (¥)",
            data: values
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: true,
        scales: {
          y: { beginAtZero: true }
        }
      }
    }
  );
}

/* ================================
   Render CONFIDENTIAL chart
================================ */
function renderConfidentialRevenue() {
  const ctx = document.getElementById("revenueChart");

  if (revenueChart) revenueChart.destroy();

  // Fake random data
  const labels = ["2025-11", "2025-12", "2026-01"];
  const values = labels.map(() => Math.random() * 100);

  revenueChart = new Chart(ctx, {
    type: "bar",
    data: {
      labels,
      datasets: [{ data: values }]
    },
    options: {
      plugins: { legend: { display: false } },
      scales: {
        x: { display: false },
        y: { display: false }
      }
    }
  });

  showConfidentialOverlay();
}

/* ================================
   Overlay + Modal
================================ */
function showConfidentialOverlay() {
  document.getElementById("revenueWrapper")
    .classList.add("blurred");

  document.getElementById("confidentialOverlay")
    .classList.remove("hidden");
}


function hideConfidentialOverlay() {
  document.getElementById("revenueWrapper")
    .classList.remove("blurred");

  document.getElementById("confidentialOverlay")
    .classList.add("hidden");
}

function openAdminModal() {
  document.getElementById("adminModal").classList.remove("hidden");
}

function closeAdminModal() {
  document.getElementById("adminModal").classList.add("hidden");
}

/* ================================
   Defect Week
================================ */

function getISOYearWeek(date = new Date()) {
  const d = new Date(Date.UTC(
    date.getFullYear(),
    date.getMonth(),
    date.getDate()
  ));

  const dayNum = d.getUTCDay() || 7;
  d.setUTCDate(d.getUTCDate() + 4 - dayNum);

  const isoYear = d.getUTCFullYear();
  const yearStart = new Date(Date.UTC(isoYear, 0, 1));
  const weekNo = Math.ceil(((d - yearStart) / 86400000 + 1) / 7);

  return `${isoYear}-W${String(weekNo).padStart(2, "0")}`;
  //return "2026-W03"
}


async function loadWeeklyDefects() {
  const raw = await apiFetch("/defects/amount/weekly");
  const items = raw?.data?.items;

  if (!Array.isArray(items)) {
    throw new Error("Invalid defects response");
  }

  const currentWeek = getISOYearWeek();

  const match = items.find(d => d.period === currentWeek);

  const value = match
    ? Number(match.total_defects)
    : 0;

  document.getElementById("weekly_defects").innerText =
    `${value.toFixed(1)} Kg`;
}


/* ================================
   Init
================================ */
document.addEventListener("DOMContentLoaded", async () => {
  try {
    await loadTodayHarvest();
    await loadharvestPieChart();
    await loadRevenueChart();
    await loadWeeklyDefects();
  } catch (err) {
    console.error(err);
    alert("Failed to load dashboard data");
  }
});