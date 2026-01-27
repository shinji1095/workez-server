/* ================================
   Global State
================================ */
let currentPeriod = "daily";
let currentLot = "1a";

let harvestChart = null;
let rankCountChart = null;
let lotChart = null;

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
   Data Normalization (CRITICAL)
================================ */
function normalizeHarvestResponse(response) {
  const items = response?.data?.items;

  if (!Array.isArray(items)) {
    throw new Error("Invalid harvest response");
  }

  return {
    labels: items.map(d => d.period).reverse(),
    values: items.map(d => Number(d.total_count)).reverse(),
    meta: items[0]?.size_name || "ALL"
  };
}


/* ================================
   Load Period
================================ */
async function loadPeriod(event, period) {
  event?.preventDefault();
  currentPeriod = period;

  try {
    // Harvest main chart
    const raw = await apiFetch(`/harvest/amount/${period}`);
    const { labels, values } = normalizeHarvestResponse(raw);

    renderHarvestChart(labels, values);

    // Reload active lot
    await loadLot(null, currentLot);
  } catch (err) {
    console.error(err);
    alert("Failed to load period data");
  }
}


async function loadCategory(event, sizeId) {
  event?.preventDefault();
  currentCategory = sizeId;

  let endpoint = `/harvest/amount/${currentPeriod}`;

  if (sizeId) {
    endpoint += `/size/${sizeId}`;
  }

  const raw = await apiFetch(endpoint);
  const items = raw.data.items;
  renderHarvestChart(
    items.map(d => d.period),
    items.map(d => d.total_count)
  );

  if (sizeId) {
    await loadRankCharts(currentPeriod, sizeId);
  }
}




async function fetchRankData(period, sizeId, rankId) {
  const res = await apiFetch(
    `/harvest/amount/${period}/size/${sizeId}/rank/${rankId}`
  );
  return res.data.items;
}


async function loadRankCharts(period, sizeId) {
  const ranks = ["A", "B", "C", "小", "廃棄"];

  const results = await Promise.all(
    ranks.map(rank =>
      fetchRankData(period, sizeId, rank)
    )
  );

  // Flatten + tag rank explicitly
  const merged = results.flatMap((items, idx) =>
    items.map(d => ({
      ...d,
      rank_id: ranks[idx]
    }))
  );

  renderRankCountChart(merged);
  renderLotChart(merged);
}


async function loadLot(event, lotName) {
  event?.preventDefault();
  currentLot = lotName;

  try {
    const raw = await apiFetch(
      `/harvest/amount/${currentPeriod}/lot/${lotName}`
    );

    const items = raw?.data?.items;
    if (!Array.isArray(items)) {
      throw new Error("Invalid lot response");
    }

    // Ensure chronological order
    items.sort((a, b) => a.period.localeCompare(b.period));

    const labels = items.map(d => d.period);
    const values = items.map(d => Number(d.total_count));

    renderLotChart(labels, values, lotName, currentPeriod);
  } catch (err) {
    console.error(err);
    alert("Failed to load lot data");
  }
}



function aggregateByRank(items) {
  const map = {};

  items.forEach(d => {
    const rank = d.rank_id;
    map[rank] = (map[rank] || 0) + Number(d.total_count);
  });

  return {
    labels: Object.keys(map),
    values: Object.values(map)
  };
}


function renderRankCountChart(items) {
  const { labels, values } = aggregateByRank(items);

  if (rankCountChart) rankCountChart.destroy();

  rankCountChart = new Chart(
    document.getElementById("rankCountChart"),
    {
      type: "bar",
      data: {
        labels,
        datasets: [{
          label: "階級別収穫",
          data: values
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: true,
        plugins: {
          legend: { display: false }
        }
      }
    }
  );
}


function renderLotChart(labels, values, lotName, period) {
  if (lotChart) lotChart.destroy();

  lotChart = new Chart(
    document.getElementById("lotChart"),
    {
      type: "line",
      data: {
        labels,
        datasets: [{
          label: `ロット ${lotName} ${period} 収穫`,
          data: values,
          tension: 0.3,
          fill: true
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
   Chart Renderer
================================ */
function renderHarvestChart(labels, values) {
  if (harvestChart) harvestChart.destroy();

  harvestChart = new Chart(
    document.getElementById("harvestChart"),
    {
      type: "line",
      data: {
        labels,
        datasets: [
          {
            data: values,
            tension: 0.3,
            fill: true
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: true,
        scales: {
          y: {
            beginAtZero: true
          }
        }
      }
    }
  );
}

/* ================================
   Init
================================ */
document.addEventListener("DOMContentLoaded", () => {
  loadPeriod(null, currentPeriod);
  loadLot(null, currentPeriod);
});