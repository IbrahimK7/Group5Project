// Run this code only after the HTML document has been fully loaded.
// This guarantees that all DOM elements exist before we try to access them.
document.addEventListener("DOMContentLoaded", function () {
  loadLeaderboards(); // Load and display leaderboard data
  loadGames();        // Load and display game cards
});

// -------------------- LEADERBOARDS --------------------

// Asynchronous function because we use `await` to fetch data from the server
async function loadLeaderboards() {

  // Get the container where leaderboards will be displayed
  const panel = document.getElementById("leaderboardPanel");

  // If the element does not exist, stop early
  if (!panel) return;

  try {
    // 1) Send a GET request to the backend API
    const response = await fetch("/api/leaderboards");

    // Parse the HTTP response body as JSON
    const data = await response.json();

    // 2) If the HTTP status is not OK (4xx or 5xx), treat it as an error
    if (!response.ok) {
      throw new Error(data.error || "Failed to load leaderboards");
    }

    // 3) If the server returned no leaderboard data, show a placeholder
    if (!data || data.length === 0) {
      panel.innerHTML =
        '<div class="text-muted small">No leaderboards yet.</div>';
      return;
    }

    // 4) Clear the panel before inserting new content
    panel.innerHTML = "";

    // 5) Display only the first 3 leaderboards
    const howManyBoards = Math.min(3, data.length);

    // Loop over each leaderboard
    for (let i = 0; i < howManyBoards; i++) {
      const board = data[i];

      // Create a container for one game's leaderboard
      const section = document.createElement("div");
      section.className = "mb-3";

      // Create and display the game title
      const gameTitle = document.createElement("div");
      gameTitle.className = "fw-semibold mb-1";
      gameTitle.textContent = board.game || "Unknown game";
      section.appendChild(gameTitle);

      // Get the list of players for this leaderboard
      const leaderboard = board.leaderboard || [];

      // If there are no players, show an empty message
      if (leaderboard.length === 0) {
        const empty = document.createElement("div");
        empty.className = "text-muted small";
        empty.textContent = "No entries.";
        section.appendChild(empty);
        panel.appendChild(section);
        continue; // Move to the next game
      }

      // Show only the top 3 players
      const howManyPlayers = Math.min(3, leaderboard.length);

      for (let j = 0; j < howManyPlayers; j++) {
        const player = leaderboard[j];

        // Row containing player name and score
        const row = document.createElement("div");
        row.className = "d-flex justify-content-between py-1 border-bottom";

        // Player name and rank
        const name = document.createElement("div");
        const tag = player.gamertag || player.username || "Unknown";
        const rank = player.rank != null ? player.rank : (j + 1);
        name.textContent = rank + ". " + tag;

        // Player score
        const score = document.createElement("div");
        score.className = "text-muted small";
        score.textContent = player.score != null ? player.score : "";

        // Add name and score to the row
        row.appendChild(name);
        row.appendChild(score);

        // Add row to this leaderboard section
        section.appendChild(row);
      }

      // Add the full leaderboard section to the main panel
      panel.appendChild(section);
    }

  } catch (error) {
    // If any error occurs (network, parsing, server error),
    // show an error message to the user
    panel.innerHTML =
      '<div class="text-danger small">' +
      escapeHtml(error.message) +
      "</div>";
  }
}

// -------------------- GAMES --------------------

// Asynchronous function to load game information
async function loadGames() {

  // Get the container where games will be displayed
  const panel = document.getElementById("gamesPanel");

  // If the element does not exist, stop early
  if (!panel) return;

  try {
    // 1) Fetch the list of games from the backend
    const response = await fetch("/api/games");

    // Parse response body as JSON
    const data = await response.json();

    // 2) Handle HTTP errors
    if (!response.ok) {
      throw new Error(data.error || "Failed to load games");
    }

    // 3) If no games exist, show a placeholder
    if (!data || data.length === 0) {
      panel.innerHTML =
        '<div class="text-muted small">No games yet.</div>';
      return;
    }

    // 4) Clear the panel before inserting content
    panel.innerHTML = "";

    // 5) Create a Bootstrap row to hold game cards
    const row = document.createElement("div");
    row.className = "row g-2";

    // 6) Display only the first 8 games
    const howManyGames = Math.min(8, data.length);

    for (let i = 0; i < howManyGames; i++) {
      const game = data[i];

      // Bootstrap column for responsiveness
      const col = document.createElement("div");
      col.className = "col-12 col-md-6 col-lg-3";

      // Card container
      const card = document.createElement("div");
      card.className = "border rounded-3 p-2";

      // Game title
      const title = document.createElement("div");
      title.className = "fw-semibold";
      title.textContent = game.title || "Unknown";

      // Game release date
      const date = document.createElement("div");
      date.className = "text-muted small";
      date.textContent = game.release_date || "";

      // Assemble card
      card.appendChild(title);
      card.appendChild(date);
      col.appendChild(card);
      row.appendChild(col);
    }

    // Add the row of game cards to the panel
    panel.appendChild(row);

  } catch (error) {
    // Display any errors that occur
    panel.innerHTML =
      '<div class="text-danger small">' +
      escapeHtml(error.message) +
      "</div>";
  }
}

// -------------------- SAFETY: ESCAPE HTML --------------------
// This function prevents HTML injection (XSS) when inserting text into innerHTML.
// In this file we mostly use textContent (which is already safe),
// but this function is kept as a safety net.
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
