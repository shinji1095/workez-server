/* ================================
   Config
================================ */
let defectCountChart = null;
let defectRatioChart = null;
let currentPeriod = "weekly";

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
   Main Loader
================================ */
async function loadDefects(period) {
  currentPeriod = period;
  updatePeriodButtons(period);

  try {
    const [amountRaw, ratioRaw] = await Promise.all([
      apiFetch(`/defects/amount/${period}`),
      apiFetch(`/defects/ratio/${period}`)
    ]);

    renderDefectCount(amountRaw.data.items);
    renderDefectRatio(ratioRaw.data.items);
  } catch (err) {
    console.error(err);
    alert("Failed to load defects data");
  }
}

/* ================================
   Chart: Defect Count
================================ */
function renderDefectCount(items) {
  const labels = items.map(d => d.period);
  const values = items.map(d => Number(d.total_defects));

  if (defectCountChart) defectCountChart.destroy();

  defectCountChart = new Chart(
    document.getElementById("defectCountChart"),
    {
      type: "bar",
      data: {
        labels,
        datasets: [{
          label: "不良品総数",
          data: values
        }]
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
   Chart: Defect Ratio
================================ */
function renderDefectRatio(items) {
  const labels = items.map(d => d.period);
  const values = items.map(d => Number(d.defects_ratio_percent));

  if (defectRatioChart) defectRatioChart.destroy();

  defectRatioChart = new Chart(
    document.getElementById("defectRatioChart"),
    {
      type: "line",
      data: {
        labels,
        datasets: [{
          label: "不良率（％）",
          data: values,
          tension: 0.3,
          fill: true
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: true,
        scales: {
          y: {
            beginAtZero: true,
            ticks: {
              callback: v => `${v}%`
            }
          }
        }
      }
    }
  );
}

/* ================================
   UI Helpers
================================ */
function updatePeriodButtons(active) {
  document
    .querySelectorAll(".period button")
    .forEach(btn => {
      btn.classList.toggle(
        "active",
        btn.innerText.toLowerCase() === active
      );
    });
}

/* ================================
   Init
================================ */
document.addEventListener("DOMContentLoaded", () => {
  loadDefects("weekly");
});
