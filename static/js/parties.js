// Run when the page is fully loaded
document.addEventListener("DOMContentLoaded", function () {
  loadParties();
});

// -------------------- LOAD PARTIES --------------------
async function loadParties() {
  const list = document.getElementById("partyList");
  if (!list) {
    return;
  }

  try {
    // 1) Request parties from the server
    const response = await fetch("/api/parties");

    if (!response.ok) {
      throw new Error("Failed to load parties (" + response.status + ")");
    }

    // 2) Parse JSON response
    const parties = await response.json();

    // 3) Clear list
    list.innerHTML = "";

    // 4) If there are no parties
    if (!parties || parties.length === 0) {
      list.innerHTML =
        '<div class="text-muted">No parties available.</div>';
      return;
    }

    // 5) Loop through parties
    for (let i = 0; i < parties.length; i++) {
      const party = parties[i];

      // Card container
      const card = document.createElement("div");
      card.className = "card mb-3 p-3";

      // Party title
      const title = document.createElement("div");
      title.className = "fw-semibold";
      title.textContent = party.name || "Unnamed party";

      // Party description (optional)
      const description = document.createElement("div");
      description.className = "text-muted small";
      description.textContent = party.description || "";

      card.appendChild(title);
      card.appendChild(description);

      list.appendChild(card);
    }

  } catch (error) {
    console.error("Error loading parties:", error);

    list.innerHTML =
      '<div class="text-danger">Failed to load parties.</div>';
  }
}
