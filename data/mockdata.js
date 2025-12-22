// ⚠️ TEMPORARY MOCK DATA

function randomSeries(length = 7) {
  return Array.from({ length }, (_, i) => ({
    date: `Day ${i + 1}`,
    amount: Math.floor(Math.random() * 100 + 20)
  }));
}

module.exports = {
  daily: randomSeries(7),
  weekly: randomSeries(4),
  monthly: randomSeries(12),

  category(categoryId) {
    return randomSeries(7).map(d => ({
      ...d,
      categoryId
    }));
  },

  targets: {
    daily: 500,
    weekly: 3000,
    monthly: 12000
  }
};

function randomSeriesWithRatio(length = 7) {
  return Array.from({ length }, (_, i) => ({
    date: `Day ${i + 1}`,
    count: Math.floor(Math.random() * 10),
    ratio: Math.random().toFixed(2)
  }));
}

module.exports = {
  daily: randomSeries(7),
  weekly: randomSeries(4),
  monthly: randomSeries(12),

  category(categoryId) {
    return randomSeries(7).map(d => ({
      ...d,
      categoryId
    }));
  },

  defects: {
    daily: randomSeriesWithRatio(7),
    weekly: randomSeriesWithRatio(4),
    monthly: randomSeriesWithRatio(12)
  },

  targets: {
    daily: 500,
    weekly: 3000,
    monthly: 12000
  }
};
