document.addEventListener("DOMContentLoaded", () => {
    loadWhatsHot();
});

async function loadWhatsHot() {
    try {
        const res = await fetch("/api/whats-hot");

        if (!res.ok) {
            console.error("API error:", res.status);
            return;
        }

        const games = await res.json();

        const container = document.getElementById("whatsHotList");
        container.innerHTML = "";

        if (games.length === 0) {
            container.innerHTML = "<p>No trending games yet.</p>";
            return;
        }

        games.forEach(game => {
            const div = document.createElement("div");
            div.className = "hot-game";

            div.innerHTML = `
                <strong>${game.name}</strong>
                <span class="text-muted"> (${game.year})</span>
            `;

            container.appendChild(div);
        });

    } catch (err) {
        console.error("Failed to load What's Hot:", err);
    }
}
