/* ================================
   Config
================================ */
let monthlyChart = null;
let yearlyChart = null;

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
   Load Revenue (Admin Only)
================================ */
async function loadRevenue() {
  try {
    const [monthlyRaw, yearlyRaw] = await Promise.all([
      apiFetch("/analytics/revenue/monthly"),
      apiFetch("/analytics/revenue/yearly")
    ]);

    renderMonthly(monthlyRaw.data.items);
    renderYearly(yearlyRaw.data.items);

    hideConfidential();
  } catch (err) {
    renderConfidentialCharts();
    showConfidential();
  }
}

/* ================================
   Monthly Chart
================================ */
function renderMonthly(items) {
  const labels = items.map(d => d.period);
  const values = items.map(d => Number(d.revenue_yen));

  if (monthlyChart) monthlyChart.destroy();

  monthlyChart = new Chart(
    document.getElementById("monthlyRevenueChart"),
    {
      type: "bar",
      data: {
        labels,
        datasets: [{ label: "収益 (¥)", data: values }]
      },
      options: {
        responsive: true,
        scales: { y: { beginAtZero: true } }
      }
    }
  );
}

/* ================================
   Yearly Chart
================================ */
function renderYearly(items) {
  const labels = items.map(d => d.period);
  const values = items.map(d => Number(d.revenue_yen));

  if (yearlyChart) yearlyChart.destroy();

  yearlyChart = new Chart(
    document.getElementById("yearlyRevenueChart"),
    {
      type: "bar",
      data: {
        labels,
        datasets: [{ label: "収益 (¥)", data: values }]
      },
      options: {
        responsive: true,
        scales: { y: { beginAtZero: true } }
      }
    }
  );
}

/* ================================
   CONFIDENTIAL MODE
================================ */
function renderConfidentialCharts() {
  const fakeLabels = ["2024", "2025", "2026"];
  const fakeValues = fakeLabels.map(() => Math.random() * 100);

  if (monthlyChart) monthlyChart.destroy();
  if (yearlyChart) yearlyChart.destroy();

  monthlyChart = new Chart(
    document.getElementById("monthlyRevenueChart"),
    {
      type: "bar",
      data: { labels: fakeLabels, datasets: [{ data: fakeValues }] },
      options: { plugins: { legend: { display: false } } }
    }
  );

  yearlyChart = new Chart(
    document.getElementById("yearlyRevenueChart"),
    {
      type: "bar",
      data: { labels: fakeLabels, datasets: [{ data: fakeValues }] },
      options: { plugins: { legend: { display: false } } }
    }
  );
}

/* ================================
   Overlay + Modal
================================ */
function showConfidential() {
  const content = document.getElementById("revenueContent");
  const overlay = document.getElementById("confidentialOverlay");

  content.classList.add("blurred");
  overlay.classList.remove("hidden");
  overlay.onclick = openAdminModal;
}

function hideConfidential() {
  document.getElementById("revenueContent")
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
   Init
================================ */
document.addEventListener("DOMContentLoaded", loadRevenue);
