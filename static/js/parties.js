document.addEventListener("DOMContentLoaded", () => {
    loadParties();
});

async function loadParties() {
    try {
        const response = await fetch("/api/parties");
        const parties = await response.json();

        const list = document.getElementById("partyList");
        list.innerHTML = "";  // Clear any existing content before appending new data

        parties.forEach(party => {
            const card = document.createElement("div");
            card.className = "card mb-3 p-3";

            card.innerHTML = `
                <h5>${party.partyName}</h5>
                <p>Game: ${party.game}</p>
                <p>Players: ${party.currentPlayers}/${party.maxPlayers}</p>
                <button class="btn btn-primary btn-sm">
                    Join Party
                </button>
            `;

            list.appendChild(card);
        });
    } catch (err) {
        console.error("Error loading parties:", err);
    }
}
