// Run this code only after the HTML page is fully loaded.
// This ensures the elements we query from the DOM actually exist.
document.addEventListener("DOMContentLoaded", function () {
  loadParties(); // Fetch parties from the server and render them on the page
});

// -------------------- LOAD PARTIES --------------------

// This function is async because it uses `await` for the network request (fetch)
// and for reading/parsing the JSON response.
async function loadParties() {

  // Get the container element where party cards will be inserted
  const list = document.getElementById("partyList");

  // If the element doesn't exist on this page, stop early
  if (!list) {
    return;
  }

  try {
    // 1) Send a request to the server to retrieve parties
    // This returns an HTTP response object (status code, headers, body, etc.)
    const response = await fetch("/api/parties");

    // If the server responded with an error status code (4xx / 5xx),
    // throw an error so the catch block will handle it.
    if (!response.ok) {
      throw new Error("Failed to load parties (" + response.status + ")");
    }

    // 2) Parse the response body as JSON
    // The server is expected to return a JSON array of parties
    const parties = await response.json();

    // 3) Clear the list before adding new content
    // This prevents duplicates if the function is called again
    list.innerHTML = "";

    // 4) If the server returned no parties, show a placeholder message
    if (!parties || parties.length === 0) {
      list.innerHTML =
        '<div class="text-muted">No parties available.</div>';
      return;
    }

    // 5) Loop through each party and create a "card" in the DOM
    for (let i = 0; i < parties.length; i++) {
      const party = parties[i];

      // Create the main card container for one party
      const card = document.createElement("div");
      card.className = "card mb-3 p-3"; // Bootstrap classes for styling

      // Party title element
      const title = document.createElement("div");
      title.className = "fw-semibold"; // Bold-ish text
      title.textContent = party.name || "Unnamed party"; // Safe text insert

      // Party description element (optional)
      const description = document.createElement("div");
      description.className = "text-muted small"; // Lighter smaller text
      description.textContent = party.description || ""; // Safe text insert

      // Put title + description into the card
      card.appendChild(title);
      card.appendChild(description);

      // Add the card to the list container in the page
      list.appendChild(card);
    }

  } catch (error) {
    // If anything fails (network issue, server error, JSON parsing issue),
    // log details for debugging
    console.error("Error loading parties:", error);

    // Show a generic error message to the user
    list.innerHTML =
      '<div class="text-danger">Failed to load parties.</div>';
  }
}
