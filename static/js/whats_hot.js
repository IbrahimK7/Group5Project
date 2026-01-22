// Run this code only after the HTML page is fully loaded.
// This ensures all DOM elements exist before we try to access them.
document.addEventListener("DOMContentLoaded", function () {
  loadWhatsHot(); // Fetch and display the "What's Hot" games
});

// -------------------- LOAD WHAT'S HOT --------------------

// Asynchronous function because it uses `await` for network requests
async function loadWhatsHot() {

  // Get the grid container where game cards will be displayed
  const grid = document.getElementById("whatsHotGrid");

  // If the element does not exist on this page, stop early
  if (!grid) {
    return;
  }

  try {
    // 1) Send a request to the backend to retrieve "What's Hot" data
    const response = await fetch("/whats-hot");

    // If the HTTP status indicates an error (4xx / 5xx),
    // throw an error to be handled by the catch block
    if (!response.ok) {
      throw new Error("API error " + response.status);
    }

    // 2) Parse the response body as JSON
    // Expected to be an array of game objects
    const games = await response.json();

    // 3) If no games are returned, show a placeholder message
    if (!games || games.length === 0) {
      grid.innerHTML =
        '<p class="text-muted">No games found.</p>';
      return;
    }

    // 4) Clear the grid before inserting new content
    // This avoids duplicating cards if the function is called again
    grid.innerHTML = "";

    // 5) Loop through each game and create a card for it
    for (let i = 0; i < games.length; i++) {
      const game = games[i];

      // Bootstrap column for responsive layout
      const col = document.createElement("div");
      col.className = "col-12 col-sm-6 col-md-4 col-lg-3";

      // Card container
      const card = document.createElement("div");
      card.className = "card h-100 shadow-sm";

      // Card body using flex layout
      const body = document.createElement("div");
      body.className = "card-body d-flex flex-column";

      // -------------------- GAME TITLE --------------------

      // Create the game title element
      const title = document.createElement("h5");
      title.className = "card-title mb-2";

      // Determine which property contains the game name
      // (defensive programming against inconsistent API data)
      let name = "Unknown";
      if (game.name) {
        name = game.name;
      } else if (game.gameName) {
        name = game.gameName;
      }

      // Insert title safely using textContent
      title.textContent = name;
      body.appendChild(title);

      // -------------------- YEAR BADGE (OPTIONAL) --------------------

      // If the game has a release year, display it as a badge
      if (game.year) {
        const badge = document.createElement("span");
        badge.className = "badge bg-secondary align-self-start";
        badge.textContent = game.year;
        body.appendChild(badge);
      }

      // -------------------- BUTTON / FOOTER --------------------

      // Footer pushed to the bottom of the card using flexbox
      const footer = document.createElement("div");
      footer.className = "mt-auto pt-3";

      // Button linking to the party search page
      const button = document.createElement("a");
      button.className = "btn btn-primary btn-sm w-100";
      button.href = "/joinparty";
      button.textContent = "Find Parties";

      // Assemble footer
      footer.appendChild(button);
      body.appendChild(footer);

      // Assemble card
      card.appendChild(body);
      col.appendChild(card);

      // Add the card to the grid
      grid.appendChild(col);
    }

  } catch (error) {
    // If any error occurs (network failure, server error, JSON parsing issue),
    // display an error message to the user
    grid.innerHTML =
      '<p class="text-danger">Failed to load: ' +
      escapeHtml(error.message) +
      "</p>";
  }
}

// -------------------- HTML ESCAPING --------------------

// Escapes special HTML characters to prevent XSS when using innerHTML
function escapeHtml(text) {

  // Safely handle null or undefined input
  if (text === undefined || text === null) {
    return "";
  }

  // Replace potentially dangerous characters with HTML entities
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
