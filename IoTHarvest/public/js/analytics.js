/* ================================
   Config
================================ */
let harvestPredictionChart = null;

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
   Load Monthly Harvest Prediction
================================ */
async function loadHarvestPrediction() {
  const raw = await apiFetch("/analytics/harvest/monthly");
  const items = raw?.data?.items;

  if (!Array.isArray(items)) {
    throw new Error("Invalid analytics response");
  }

  const labels = items.map(d => d.period);
  const values = items.map(d => Number(d.predicted_count));

  renderPredictionChart(labels, values);
}

/* ================================
   Render Chart
================================ */
function renderPredictionChart(labels, values) {
  const ctx = document.getElementById("harvestPredictionChart");

  if (harvestPredictionChart) {
    harvestPredictionChart.destroy();
  }

  harvestPredictionChart = new Chart(ctx, {
    type: "bar",
    data: {
      labels,
      datasets: [
        {
          label: "予測収穫量 (kg)",
          data: values
        }
      ]
    },
    options: {
      responsive: true,
      scales: {
        y: {
          beginAtZero: true
        }
      }
    }
  });
}

/* ================================
   Access Control (Admin Only)
================================ */
function blockAccess() {
  const content = document.querySelector(".content");
  content.classList.add("blocked");

  const overlay = document.createElement("div");
  overlay.className = "access-overlay";

  overlay.innerHTML = `
    <div class="access-popup">
      <h3>CONFIDENTIAL</h3>
      <p>管理者権限が必要です</p>
      <p style="opacity:0.7;font-size:0.9rem">
        クリックしてダッシュボードへ戻る
      </p>
    </div>
  `;

  overlay.addEventListener("click", () => {
    window.location.href = "index";
  });

  document.body.appendChild(overlay);
}


/* ================================
   Download Helpers
================================ */

/**
 * Read filter values from input fields
 */
function getDownloadParams() {
  const params = new URLSearchParams();

  const start = document.getElementById("startDate")?.value;
  const end = document.getElementById("endDate")?.value;
  const lot = document.getElementById("lotName")?.value?.trim();
  const size = document.getElementById("sizeId")?.value;
  const rank = document.getElementById("rankId")?.value;

  if (start) params.set("start_date", start);
  if (end) params.set("end_date", end);
  if (lot) params.set("lot", lot);
  if (size) params.set("size", size);
  if (rank) params.set("rank", rank);

  return params.toString();
}


/**
 * Generic downloader (CSV / PDF)
 */
async function exportCSV() {
  const query = getDownloadParams();
  const url = `${BASE_URL}/harvest/records/export/csv?${query}`;

  const res = await fetch(url, {
    headers: {
      "Content-Type": "application/json",
      ...(ACCESS_TOKEN && { Authorization: `Bearer ${ACCESS_TOKEN}` })
    }
  });

  if (!res.ok) {
    throw new Error(`CSV download failed: ${res.status}`);
  }

  // ⚠️ CSV should be read as TEXT
  const text = await res.text();

  const blob = new Blob([text], { type: "text/csv;charset=utf-8;" });
  triggerDownload(blob, "harvest_records.csv");
}


async function exportPDF() {
  const query = getDownloadParams();

  const url = `${BASE_URL}/harvest/records/report/pdf?${query}`;

  const res = await fetch(url, {
    headers: {
        Authorization: `Bearer ${ACCESS_TOKEN}`
    }
  });

  // ⚠️ PDF MUST be blob
  const blob = await res.blob();

  // sanity check
  console.log("PDF size:", blob.size);

  triggerDownload(blob, "harvest_report.pdf");
}

function triggerDownload(blob, filename) {
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = filename;
  document.body.appendChild(a);
  a.click();
  a.remove();
  URL.revokeObjectURL(url);
}



/* ================================
   Init
================================ */
document.addEventListener("DOMContentLoaded", async () => {
  document
  .getElementById("downloadCsvBtn")
  ?.addEventListener("click", downloadCSV);

document
  .getElementById("downloadPdfBtn")
  ?.addEventListener("click", downloadPDF);

  try {
    await loadHarvestPrediction();
  } catch (err) {
    console.warn("Analytics access denied:", err);
    blockAccess();
  }
});