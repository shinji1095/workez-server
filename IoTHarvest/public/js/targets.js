/* ================================
   Config
================================ */

const PERIODS = ["daily", "weekly", "monthly"];

/* ================================
   Elements
================================ */
const mainContent = document.querySelector(".content");
const cards = document.querySelectorAll(".card");

let isAdmin = false;

/* ================================
   Admin Check (API truth)
================================ */
async function checkAdminAccess() {
  try {
    const res = await fetch(`/api${endpoint}`, {
    credentials: "include",
    ...options
  });;

    if (!res.ok) throw new Error();
    isAdmin = true;

  } catch {
    isAdmin = false;
    blurContent();
  }
}

/* ================================
   Blur Only Main Content
================================ */
function blurContent() {
  mainContent.classList.add("blocked");

  const overlay = document.createElement("div");
  overlay.className = "access-overlay";

  overlay.innerHTML = `
    <div class="access-popup">
      <h3>機密</h3>
      <p>管理者アクセスが必要です</p>
      <p class="click-hint">クリックしてダッシュボードに戻る</p>
    </div>
  `;

  // 👉 Redirect on click
  overlay.addEventListener("click", () => {
    window.location.href = "index";
  });

  document.body.appendChild(overlay);
}

/* ================================
   Fetch Target Value
================================ */
async function fetchTarget(period) {
  try {
    const res = await fetch(`${BASE_URL}/harvest/target/${period}`, {
      headers: {
        Authorization: `Bearer ${ACCESS_TOKEN}`
      }
    });

    if (!res.ok) throw new Error();

    const json = await res.json();
    return json.value;

  } catch {
    return "---";
  }
}

/* ================================
   Enable PUT (Admin only)
================================ */
function enableEditing(card, period) {
  const valueEl = card.querySelector(".card-value");

  valueEl.style.cursor = "pointer";
  valueEl.title = "Click to update";

  valueEl.addEventListener("click", async () => {
    const newValue = prompt(`Update ${period} target (kg):`);

    if (!newValue || isNaN(newValue)) return;

    try {
      const res = await fetch(`${BASE_URL}/harvest/target/${period}`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${TOKEN}`
        },
        body: JSON.stringify({ value: Number(newValue) })
      });

      if (!res.ok) throw new Error();

      valueEl.textContent = `${newValue} kg`;

    } catch {
      alert("Update failed");
    }
  });
}

/* ================================
   Load All Targets
================================ */
async function loadTargets() {
  for (const card of cards) {
    const period = card.dataset.period;
    const valueEl = card.querySelector(".card-value");

    const value = await fetchTarget(period);
    valueEl.textContent = `${value} kg`;

    if (isAdmin) {
      enableEditing(card, period);
    }
  }
}

/* ================================
   Init
================================ */
document.addEventListener("DOMContentLoaded", async () => {
  await checkAdminAccess();
  loadTargets();
});