async function loadMessages() {
  const messageBox = document.getElementById("messageBox");

  const currentUser = "user001";

  try {
    const res = await fetch(`/api/messages?user=${encodeURIComponent(currentUser)}`);
    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(err.error || `Request failed (${res.status})`);
    }

    const messages = await res.json();

    if (!messages.length) {
      messageBox.innerHTML = `<p>No messages yet.</p>`;
      return;
    }

    messageBox.innerHTML = messages.map(m => `
      <div class="card mb-2">
        <div class="card-body">
          <div class="d-flex justify-content-between align-items-center">
            <strong>${escapeHtml(m.sender)}</strong>
            <span class="badge ${m.read ? "bg-secondary" : "bg-success"}">
              ${m.read ? "Read" : "Unread"}
            </span>
          </div>
          <p class="mb-0 mt-2">${escapeHtml(m.content)}</p>
        </div>
      </div>
    `).join("");

  } catch (e) {
    messageBox.innerHTML =
      `<p class="text-danger">Error loading messages: ${escapeHtml(e.message)}</p>`;
  }
}

// basic XSS-safe escaping
function escapeHtml(text) {
  if (text === undefined || text === null) return "";
  return String(text).replace(/[&<>"']/g, (c) => ({
    "&": "&amp;",
    "<": "&lt;",
    ">": "&gt;",
    '"': "&quot;",
    "'": "&#039;"
  }[c]));
}

document.addEventListener("DOMContentLoaded", loadMessages);
