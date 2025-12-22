const express = require("express");
const cors = require("cors");

const harvestRoutes = require("./routes/harvest");

const app = express();
app.use(cors());
app.use(express.json());

app.use("/harvest", harvestRoutes);

const PORT = 3000;
app.listen(PORT, () => {
  console.log(`✅ Harvest API running on http://localhost:${PORT}`);
});
