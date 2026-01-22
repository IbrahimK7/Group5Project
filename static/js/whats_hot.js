// Run when the page is fully loaded
document.addEventListener("DOMContentLoaded", function () {
  loadWhatsHot();
});

// -------------------- LOAD WHAT'S HOT --------------------
async function loadWhatsHot() {
  const grid = document.getElementById("whatsHotGrid");
  if (!grid) {
    return;
  }

  try {
    // 1) Request data from the server
    const response = await fetch("/whats-hot");

    if (!response.ok) {
      throw new Error("API error " + response.status);
    }

    // 2) Parse JSON response
    const games = await response.json();

    // 3) If no games found
    if (!games || games.length === 0) {
      grid.innerHTML =
        '<p class="text-muted">No games found.</p>';
      return;
    }

    // 4) Clear grid
    grid.innerHTML = "";

    // 5) Loop through games
    for (let i = 0; i < games.length; i++) {
      const game = games[i];

      // Column
      const col = document.createElement("div");
      col.className = "col-12 col-sm-6 col-md-4 col-lg-3";

      // Card
      const card = document.createElement("div");
      card.className = "card h-100 shadow-sm";

      const body = document.createElement("div");
      body.className = "card-body d-flex flex-column";

      // Game title
      const title = document.createElement("h5");
      title.className = "card-title mb-2";

      let name = "Unknown";
      if (game.name) {
        name = game.name;
      } else if (game.gameName) {
        name = game.gameName;
      }
      title.textContent = name;

      body.appendChild(title);

      // Year badge (optional)
      if (game.year) {
        const badge = document.createElement("span");
        badge.className = "badge bg-secondary align-self-start";
        badge.textContent = game.year;
        body.appendChild(badge);
      }

      // Button container
      const footer = document.createElement("div");
      footer.className = "mt-auto pt-3";

      const button = document.createElement("a");
      button.className = "btn btn-primary btn-sm w-100";
      button.href = "/joinparty";
      button.textContent = "Find Parties";

      footer.appendChild(button);
      body.appendChild(footer);

      card.appendChild(body);
      col.appendChild(card);
      grid.appendChild(col);
    }

  } catch (error) {
    grid.innerHTML =
      '<p class="text-danger">Failed to load: ' +
      escapeHtml(error.message) +
      "</p>";
  }
}

// -------------------- HTML ESCAPING --------------------
function escapeHtml(text) {
  if (text === undefined || text === null) {
    return "";
  }

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
