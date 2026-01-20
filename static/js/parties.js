document.addEventListener("DOMContentLoaded", () => {
    loadParties();
});

async function loadParties() {
    try {
        const response = await fetch("/api/parties");
        const parties = await response.json();

        const list = document.getElementById("partyList");
        list.innerHTML = "";  

        parties.forEach(party => {
            const card = document.createElement("div");
            card.className = "card mb-3 p-3";

            

            list.appendChild(card);
        });
    } catch (err) {
        console.error("Error loading parties:", err);
    }
}
