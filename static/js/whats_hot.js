document.addEventListener("DOMContentLoaded", loadWhatsHot);

async function loadWhatsHot() {
  const grid = document.getElementById("whatsHotGrid");
  if (!grid) return;

  try {
    const res = await fetch("/whats-hot");
    if (!res.ok) throw new Error(`API error ${res.status}`);
    const games = await res.json();

    if (!games.length) {
      grid.innerHTML = `<p class="text-muted">No games found.</p>`;
      return;
    }

    grid.innerHTML = games.map(g => `
      <div class="col-12 col-sm-6 col-md-4 col-lg-3">
        <div class="card h-100 shadow-sm">
          <div class="card-body d-flex flex-column">
            <h5 class="card-title mb-2">${escapeHtml(g.name ?? g.gameName ?? "Unknown")}</h5>
            ${g.year ? `<span class="badge bg-secondary align-self-start">${escapeHtml(g.year)}</span>` : ""}
            <div class="mt-auto pt-3">
              <a class="btn btn-primary btn-sm w-100" href="/joinparty">
                Find Parties
              </a>
            </div>
          </div>
        </div>
      </div>
    `).join("");

  } catch (e) {
    grid.innerHTML = `<p class="text-danger">Failed to load: ${escapeHtml(e.message)}</p>`;
  }
}

function escapeHtml(text) {
  if (text === undefined || text === null) return "";
  return String(text).replace(/[&<>"']/g, c => ({
    "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#039;"
  }[c]));
}
