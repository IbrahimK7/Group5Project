// Run code after the HTML page is fully loaded
document.addEventListener("DOMContentLoaded", function () {
  loadLeaderboards();
  loadGames();
});

// -------------------- LEADERBOARDS --------------------
async function loadLeaderboards() {
  const panel = document.getElementById("leaderboardPanel");
  if (!panel) return;

  try {
    // 1) Ask the server for leaderboard data
    const response = await fetch("/api/leaderboards");
    const data = await response.json();

    // 2) If the server responded with an error, show it
    if (!response.ok) {
      throw new Error(data.error || "Failed to load leaderboards");
    }

    // 3) If there is no data, show an empty message
    if (!data || data.length === 0) {
      panel.innerHTML = '<div class="text-muted small">No leaderboards yet.</div>';
      return;
    }

    // 4) Clear panel before adding new content
    panel.innerHTML = "";

    // 5) Show only the first 3 games
    const howManyBoards = Math.min(3, data.length);

    for (let i = 0; i < howManyBoards; i++) {
      const board = data[i];

      // Container for one game's leaderboard
      const section = document.createElement("div");
      section.className = "mb-3";

      // Game name/title
      const gameTitle = document.createElement("div");
      gameTitle.className = "fw-semibold mb-1";
      gameTitle.textContent = board.game || "Unknown game";
      section.appendChild(gameTitle);

      const leaderboard = board.leaderboard || [];

      // If no entries for that game
      if (leaderboard.length === 0) {
        const empty = document.createElement("div");
        empty.className = "text-muted small";
        empty.textContent = "No entries.";
        section.appendChild(empty);
        panel.appendChild(section);
        continue;
      }

      // Show top 3 players for that game
      const howManyPlayers = Math.min(3, leaderboard.length);

      for (let j = 0; j < howManyPlayers; j++) {
        const player = leaderboard[j];

        const row = document.createElement("div");
        row.className = "d-flex justify-content-between py-1 border-bottom";

        const name = document.createElement("div");
        const tag = player.gamertag || player.username || "Unknown";
        const rank = player.rank != null ? player.rank : (j + 1);
        name.textContent = rank + ". " + tag;

        const score = document.createElement("div");
        score.className = "text-muted small";
        score.textContent = player.score != null ? player.score : "";

        row.appendChild(name);
        row.appendChild(score);
        section.appendChild(row);
      }

      panel.appendChild(section);
    }
  } catch (error) {
    panel.innerHTML = '<div class="text-danger small">' + escapeHtml(error.message) + "</div>";
  }
}

// -------------------- GAMES --------------------
async function loadGames() {
  const panel = document.getElementById("gamesPanel");
  if (!panel) return;

  try {
    // 1) Ask the server for games
    const response = await fetch("/api/games");
    const data = await response.json();

    // 2) If the server responded with an error, show it
    if (!response.ok) {
      throw new Error(data.error || "Failed to load games");
    }

    // 3) If there is no data, show an empty message
    if (!data || data.length === 0) {
      panel.innerHTML = '<div class="text-muted small">No games yet.</div>';
      return;
    }

    // 4) Clear panel before adding new content
    panel.innerHTML = "";

    // 5) Create a bootstrap row
    const row = document.createElement("div");
    row.className = "row g-2";

    // 6) Show only the first 8 games
    const howManyGames = Math.min(8, data.length);

    for (let i = 0; i < howManyGames; i++) {
      const game = data[i];

      // Column
      const col = document.createElement("div");
      col.className = "col-12 col-md-6 col-lg-3";

      // Card
      const card = document.createElement("div");
      card.className = "border rounded-3 p-2";

      const title = document.createElement("div");
      title.className = "fw-semibold";
      title.textContent = game.title || "Unknown";

      const date = document.createElement("div");
      date.className = "text-muted small";
      date.textContent = game.release_date || "";

      card.appendChild(title);
      card.appendChild(date);
      col.appendChild(card);
      row.appendChild(col);
    }

    panel.appendChild(row);
  } catch (error) {
    panel.innerHTML = '<div class="text-danger small">' + escapeHtml(error.message) + "</div>";
  }
}

// -------------------- SAFETY: ESCAPE HTML --------------------
// We keep this in case you ever put text into innerHTML.
// In this beginner version we mostly use textContent, which is already safe.
function escapeHtml(text) {
  if (text === undefined || text === null) return "";
  return String(text).replace(/[&<>"']/g, function (c) {
    return {
      "&": "&amp;",
      "<": "&lt;",
      ">": "&gt;",
      '"': "&quot;",
      "'": "&#039;"
    }[c];
  });
}
