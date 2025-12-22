const express = require("express");
const router = express.Router();
const data = require("../data/mockdata");

/**
 * デバイス → バックエンド
 * POST /harvest/amount/add
 */
router.post("/amount/add", (req, res) => {
  // 🔴 PLACEHOLDER:
  // Replace this with real device payload handling
  console.log("📡 Device data received:", req.body);

  res.json({ message: "Harvest amount uploaded (mock)" });
});

/**
 * 日間 / 週間 / 月間収穫量
 */
router.get("/amount/daily", (req, res) => {
  res.json(data.daily);
});

router.get("/amount/weekly", (req, res) => {
  res.json(data.weekly);
});

router.get("/amount/monthly", (req, res) => {
  res.json(data.monthly);
});

/**
 * 仕分けサイズごと（GET）
 */
router.get("/amount/:period/category/:categoryId", (req, res) => {
  const { period, categoryId } = req.params;

  res.json(data.category(period, categoryId));
});

/**
 * 仕分けサイズごと（PATCH）
 * 管理者用
 */
router.patch("/amount/:period/category/:categoryId", (req, res) => {
  // 🔴 PLACEHOLDER:
  // Validate admin role
  // Update DB instead of mock
  console.log("✏️ Admin update:", req.body);

  res.json({ message: "Category harvest updated (mock)" });
});

/**
 * 目標収穫量設定
 */
router.put("/target/daily", (req, res) => {
  data.targets.daily = req.body.value;
  res.json({ message: "Daily target updated", value: data.targets.daily });
});

router.put("/target/weekly", (req, res) => {
  data.targets.weekly = req.body.value;
  res.json({ message: "Weekly target updated", value: data.targets.weekly });
});

router.put("/target/monthly", (req, res) => {
  data.targets.monthly = req.body.value;
  res.json({ message: "Monthly target updated", value: data.targets.monthly });
});

router.get("/defects/:period", (req, res) => {
  const { period } = req.params;
  res.json(data.defects[period]);
});
router.get("/amount/:period/all", (req, res) => {
  const { period } = req.params;

  res.json({
    large: data.category(period, 1),
    medium: data.category(period, 2),
    small: data.category(period, 3)
  });
});

module.exports = router;
