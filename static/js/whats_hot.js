fetch("/api/whats-hot")
  .then(res => res.json())
  .then(games => {
      const container = document.getElementById("gamesList");

      games.forEach(game => {
          const div = document.createElement("div");
          div.className = "card p-3 mb-2";
          div.innerHTML = `
              <h5>${game.name}</h5>
              <p>Released: ${game.year}</p>
          `;
          container.appendChild(div);
      });
  });
