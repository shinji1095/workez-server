// ⚠️ TEMPORARY MOCK DATA

const PERIOD_LENGTH = {
  daily: 7,
  weekly: 4,
  monthly: 12
};

function randomSeries(period) {
  const length = PERIOD_LENGTH[period];

  return Array.from({ length }, (_, i) => ({
    date:
      period === "daily" ? `Day ${i + 1}` :
      period === "weekly" ? `Week ${i + 1}` :
      `Month ${i + 1}`,
    amount: Math.floor(Math.random() * 100 + 20)
  }));
}

function randomSeriesWithRatio(period) {
  const length = PERIOD_LENGTH[period];

  return Array.from({ length }, (_, i) => ({
    date:
      period === "daily" ? `Day ${i + 1}` :
      period === "weekly" ? `Week ${i + 1}` :
      `Month ${i + 1}`,
    count: Math.floor(Math.random() * 10),
    ratio: Number(Math.random().toFixed(2))
  }));
}

/* =========================
   EXPORTS
========================= */

module.exports = {
  /* Harvest totals */
  daily: randomSeries("daily"),
  weekly: randomSeries("weekly"),
  monthly: randomSeries("monthly"),

  category(period, categoryId) {
    return randomSeries(period).map(d => ({
      ...d,
      categoryId
    }));
  },

  /* Defects */
  defects: {
    daily: randomSeriesWithRatio("daily"),
    weekly: randomSeriesWithRatio("weekly"),
    monthly: randomSeriesWithRatio("monthly")
  },

  /* Targets */
  targets: {
    daily: 500,
    weekly: 3000,
    monthly: 12000
  }
};