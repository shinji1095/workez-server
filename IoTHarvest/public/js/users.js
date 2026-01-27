/* ================================
   Config
================================ */
/* ================================
   Elements
================================ */
const tableBody = document.getElementById("usersTableBody");
const mainContent = document.querySelector(".content");


/* ================================
   API Helper (NO TOKEN HERE)
================================ */
async function fetchUsers(endpoint, options = {}) {
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
   Render Users
================================ */
function renderUsers(items) {
  tableBody.innerHTML = "";

  if (!items.length) {
    tableBody.innerHTML = `
      <tr>
        <td colspan="4">No users found</td>
      </tr>
    `;
    return;
  }

  items.forEach(user => {
    const tr = document.createElement("tr");

    tr.innerHTML = `
      <td>${user.email}</td>
      <td>${user.name}</td>
      <td>${user.role}</td>
      <td>${formatDate(user.created_at)}</td>
    `;

    tableBody.appendChild(tr);
  });
}

/* ================================
   Helpers
================================ */
function formatDate(iso) {
  return new Date(iso).toLocaleString();
}

/* ================================
   Blur if No Access
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
   Init
================================ */
document.addEventListener("DOMContentLoaded", async () => {
  try {
    const json = await fetchUsers();
    renderUsers(json.data.items);
  } catch (err) {
    console.error(err);
    blurContent();
  }
});
