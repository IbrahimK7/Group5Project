document.addEventListener("DOMContentLoaded", () => {
  loadConversation();
  wireComposer();
});

async function loadConversation() {
  const box = document.getElementById("chatMessages");
  const withEl = document.getElementById("conversationWith");

  try {
    const res = await fetch(`/api/threads/${encodeURIComponent(THREAD_ID)}`);
    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(err.error || `Request failed (${res.status})`);
    }

    const data = await res.json();
    const me = data.me;
    const messages = data.messages || [];

    // show who you're chatting with
    const parts = THREAD_ID.split(":");
    const other = parts[0] === me ? parts[1] : parts[0];
    withEl.textContent = `With ${other}`;

    if (!messages.length) {
      box.innerHTML = `<div class="text-muted small text-center py-3">No messages yet.</div>`;
      return;
    }

    box.innerHTML = messages.map(m => renderBubble(m, me)).join("");

    // scroll to bottom
    box.scrollTop = box.scrollHeight;

  } catch (e) {
    box.innerHTML = `<div class="text-danger small text-center py-3">${escapeHtml(e.message)}</div>`;
  }
}

function wireComposer() {
  const form = document.getElementById("messageForm");
  const input = document.getElementById("messageInput");

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const content = input.value.trim();
    if (!content) return;

    // optimistic UI: disable while sending
    input.disabled = true;

    try {
      const res = await fetch("/api/messages", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ thread_id: THREAD_ID, content })
      });

      if (!res.ok) {
        const err = await res.json().catch(() => ({}));
        throw new Error(err.error || `Send failed (${res.status})`);
      }

      input.value = "";
      await loadConversation(); // simple refresh after send

    } catch (e) {
      alert(`Failed to send: ${e.message}`);
    } finally {
      input.disabled = false;
      input.focus();
    }
  });
}

function renderBubble(m, me) {
  const isMe = (m.sender === me);
  const bubbleClass = isMe ? "bubble bubble-me" : "bubble bubble-them";
  const meta = isMe ? "You" : escapeHtml(m.sender || "Unknown");
  const text = escapeHtml(m.content || "");

  return `
    <div class="bubble-row ${isMe ? "row-me" : "row-them"}">
      <div class="${bubbleClass}">
        <div class="bubble-meta">${meta}</div>
        <div class="bubble-text">${text}</div>
      </div>
    </div>
  `;
}

function escapeHtml(text) {
  if (text === undefined || text === null) return "";
  return String(text).replace(/[&<>"']/g, c => ({
    "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#039;"
  }[c]));
}
