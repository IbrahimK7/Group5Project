document.addEventListener("DOMContentLoaded", () => {
  loadLeaderboards();
  loadGames();
});

async function loadLeaderboards() {
  const el = document.getElementById("leaderboardPanel");
  if (!el) return;

  try {
    const res = await fetch("/api/leaderboards");
    const data = await res.json();
    if (!res.ok) throw new Error(data.error || "Failed to load leaderboards");

    if (!data.length) {
      el.innerHTML = `<div class="text-muted small">No leaderboards yet.</div>`;
      return;
    }

    // show first 3 games
    const topBoards = data.slice(0, 3);

    el.innerHTML = topBoards.map(b => {
      const top3 = (b.leaderboard || []).slice(0, 3);
      const rows = top3.map(p => `
        <div class="d-flex justify-content-between py-1 border-bottom">
          <div>${p.rank}. ${escapeHtml(p.gamertag || p.username)}</div>
          <div class="text-muted small">${p.score ?? ""}</div>
        </div>
      `).join("");

      return `
        <div class="mb-3">
          <div class="fw-semibold mb-1">${escapeHtml(b.game)}</div>
          <div>${rows || `<div class="text-muted small">No entries.</div>`}</div>
        </div>
      `;
    }).join("");

  } catch (e) {
    el.innerHTML = `<div class="text-danger small">${escapeHtml(e.message)}</div>`;
  }
}

async function loadGames() {
  const el = document.getElementById("gamesPanel");
  if (!el) return;

  try {
    const res = await fetch("/api/games");
    const data = await res.json();
    if (!res.ok) throw new Error(data.error || "Failed to load games");

    if (!data.length) {
      el.innerHTML = `<div class="text-muted small">No games yet.</div>`;
      return;
    }

    // show first 8 games
    const games = data.slice(0, 8);

    el.innerHTML = `
      <div class="row g-2">
        ${games.map(g => `
          <div class="col-12 col-md-6 col-lg-3">
            <div class="border rounded-3 p-2">
              <div class="fw-semibold">${escapeHtml(g.title || "Unknown")}</div>
              <div class="text-muted small">${escapeHtml(g.release_date || "")}</div>
            </div>
          </div>
        `).join("")}
      </div>
    `;

  } catch (e) {
    el.innerHTML = `<div class="text-danger small">${escapeHtml(e.message)}</div>`;
  }
}

function escapeHtml(text) {
  if (text === undefined || text === null) return "";
  return String(text).replace(/[&<>"']/g, c => ({
    "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#039;"
  }[c]));
}
