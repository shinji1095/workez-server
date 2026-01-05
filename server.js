const express = require("express");
const cors = require("cors");
const path = require("path");

const harvestRoutes = require("./routes/harvest");

const app = express();
app.use(cors());
app.use(express.json());

app.use("/harvest", harvestRoutes);

const API_ORIGIN = process.env.API_ORIGIN || "http://127.0.0.1:8000";

app.all("/tablet/harvest/:date", async (req, res) => {
  const targetUrl = new URL(req.originalUrl, API_ORIGIN);
  const headers = {};

  const authorization = req.get("Authorization");
  if (authorization) headers.Authorization = authorization;

  if (req.method !== "GET" && req.method !== "HEAD") {
    headers["Content-Type"] = "application/json";
  }

  try {
    const apiRes = await fetch(targetUrl.toString(), {
      method: req.method,
      headers,
      body:
        req.method === "GET" || req.method === "HEAD"
          ? undefined
          : JSON.stringify(req.body ?? {}),
    });

    const text = await apiRes.text();
    const contentType = apiRes.headers.get("content-type");
    if (contentType) res.set("Content-Type", contentType);
    res.status(apiRes.status).send(text);
  } catch (err) {
    console.error("Proxy error:", err);
    res.status(502).json({ error: "Bad Gateway", detail: String(err?.message || err) });
  }
});

app.use(express.static(path.join(__dirname)));

const PORT = 3000;
app.listen(PORT, () => {
  console.log(`✅ Harvest API running on http://localhost:${PORT}`);
});
