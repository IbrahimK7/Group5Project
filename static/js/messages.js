// Run code after the page is fully loaded
document.addEventListener("DOMContentLoaded", function () {
  loadThreads();
});

// -------------------- LOAD THREADS --------------------
async function loadThreads() {
  const list = document.getElementById("threadList");
  if (!list) {
    return;
  }

  try {
    // 1) Request threads from the server
    const response = await fetch("/threads");

    if (!response.ok) {
      let err = {};
      try {
        err = await response.json();
      } catch (_) {}
      throw new Error(err.error || "Request failed (" + response.status + ")");
    }

    // 2) Parse JSON response
    const threads = await response.json();

    // 3) If there are no conversations
    if (!threads || threads.length === 0) {
      list.innerHTML =
        '<p class="text-muted m-0">No conversations yet.</p>';
      return;
    }

    // 4) Clear list
    list.innerHTML = "";

    // 5) Loop through threads
    for (let i = 0; i < threads.length; i++) {
      const thread = threads[i];

      // Other user's name
      let otherUser = "Unknown";
      if (thread.other_user) {
        otherUser = thread.other_user;
      }

      // Last message
      let lastMessage = {};
      if (thread.last_message) {
        lastMessage = thread.last_message;
      }

      let previewText = "";
      if (lastMessage.content) {
        previewText = lastMessage.content;
      }

      // Read / unread badge
      let badgeHtml = "";
      if (lastMessage.read === false) {
        badgeHtml = '<span class="badge bg-success">Unread</span>';
      } else {
        badgeHtml = '<span class="badge bg-secondary">Read</span>';
      }

      // Create link
      const link = document.createElement("a");
      link.className = "thread-row text-decoration-none text-dark";
      link.href =
        "/messages/" + encodeURIComponent(thread.thread_id);

      // Left side
      const left = document.createElement("div");
      left.className = "thread-left";

      const name = document.createElement("div");
      name.className = "thread-name";
      name.textContent = otherUser;

      const preview = document.createElement("div");
      preview.className = "thread-preview";

      if (previewText !== "") {
        preview.textContent = previewText;
      } else {
        preview.innerHTML =
          "<span class='text-muted'>No messages</span>";
      }

      left.appendChild(name);
      left.appendChild(preview);

      // Right side
      const right = document.createElement("div");
      right.className = "thread-right";
      right.innerHTML = badgeHtml;

      // Assemble row
      link.appendChild(left);
      link.appendChild(right);
      list.appendChild(link);
    }

  } catch (error) {
    list.innerHTML =
      '<p class="text-danger m-0">Failed to load: ' +
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
