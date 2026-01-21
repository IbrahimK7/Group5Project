document.addEventListener("DOMContentLoaded", loadThreads);

async function loadThreads() {
  const list = document.getElementById("threadList");
  if (!list) return;

  try {
    const res = await fetch("/threads");
    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(err.error || `Request failed (${res.status})`);
    }

    const threads = await res.json();

    if (!threads.length) {
      list.innerHTML = `<p class="text-muted m-0">No conversations yet.</p>`;
      return;
    }

    list.innerHTML = threads.map(t => {
      const other = escapeHtml(t.other_user ?? "Unknown");
      const last = t.last_message ?? {};
      const preview = escapeHtml(last.content ?? "");
      const unread = last.read === false;
      const badge = unread
        ? `<span class="badge bg-success">Unread</span>`
        : `<span class="badge bg-secondary">Read</span>`;

      return `
        <a class="thread-row text-decoration-none text-dark"
           href="/messages/${encodeURIComponent(t.thread_id)}">
          <div class="thread-left">
            <div class="thread-name">${other}</div>
            <div class="thread-preview">${preview || "<span class='text-muted'>No messages</span>"}</div>
          </div>
          <div class="thread-right">
            ${badge}
          </div>
        </a>
      `;
    }).join("");

  } catch (e) {
    list.innerHTML = `<p class="text-danger m-0">Failed to load: ${escapeHtml(e.message)}</p>`;
  }
}

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
