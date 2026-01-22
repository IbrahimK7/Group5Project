// Run this code only after the HTML page is fully loaded.
// This ensures all DOM elements exist before we try to access them.
document.addEventListener("DOMContentLoaded", function () {
  loadThreads(); // Load the list of message threads
});

// -------------------- LOAD THREADS --------------------

// Asynchronous function because it performs a network request using `fetch`
async function loadThreads() {

  // Get the container where the thread list will be displayed
  const list = document.getElementById("threadList");

  // If the element does not exist, stop execution
  if (!list) {
    return;
  }

  try {
    // 1) Send a request to the server to fetch all conversation threads
    const response = await fetch("/threads");

    // If the HTTP response status indicates an error (4xx / 5xx)
    if (!response.ok) {

      // Try to read an error message from the response body
      let err = {};
      try {
        err = await response.json();
      } catch (_) {
        // Ignore JSON parsing errors
      }

      // Throw an error so it is handled by the catch block below
      throw new Error(
        err.error || "Request failed (" + response.status + ")"
      );
    }

    // 2) Parse the successful response body as JSON
    const threads = await response.json();

    // 3) If there are no conversation threads, show a placeholder message
    if (!threads || threads.length === 0) {
      list.innerHTML =
        '<p class="text-muted m-0">No conversations yet.</p>';
      return;
    }

    // 4) Clear the list before inserting new thread entries
    list.innerHTML = "";

    // 5) Loop through each thread returned by the server
    for (let i = 0; i < threads.length; i++) {
      const thread = threads[i];

      // Determine the other user's name in the conversation
      let otherUser = "Unknown";
      if (thread.other_user) {
        otherUser = thread.other_user;
      }

      // Extract the last message of the thread (if any)
      let lastMessage = {};
      if (thread.last_message) {
        lastMessage = thread.last_message;
      }

      // Preview text for the last message
      let previewText = "";
      if (lastMessage.content) {
        previewText = lastMessage.content;
      }

      // Read / unread badge (visual indicator)
      let badgeHtml = "";
      if (lastMessage.read === false) {
        badgeHtml = '<span class="badge bg-success">Unread</span>';
      } else {
        badgeHtml = '<span class="badge bg-secondary">Read</span>';
      }

      // Create a clickable link for the entire thread row
      const link = document.createElement("a");
      link.className = "thread-row text-decoration-none text-dark";

      // Link to the message page for this thread
      link.href =
        "/messages/" + encodeURIComponent(thread.thread_id);

      // -------------------- LEFT SIDE (user + preview) --------------------

      // Container for the left side of the thread row
      const left = document.createElement("div");
      left.className = "thread-left";

      // Display the other user's name
      const name = document.createElement("div");
      name.className = "thread-name";
      name.textContent = otherUser;

      // Preview of the last message
      const preview = document.createElement("div");
      preview.className = "thread-preview";

      // If a message exists, show its content
      if (previewText !== "") {
        preview.textContent = previewText;
      } else {
        // Otherwise, show a placeholder
        preview.innerHTML =
          "<span class='text-muted'>No messages</span>";
      }

      // Add name and preview to the left side
      left.appendChild(name);
      left.appendChild(preview);

      // -------------------- RIGHT SIDE (read/unread badge) --------------------

      // Container for the right side of the thread row
      const right = document.createElement("div");
      right.className = "thread-right";

      // Insert badge HTML (safe because content is controlled)
      right.innerHTML = badgeHtml;

      // -------------------- ASSEMBLE THREAD ROW --------------------

      // Combine left and right sections into the link
      link.appendChild(left);
      link.appendChild(right);

      // Add the completed thread row to the list
      list.appendChild(link);
    }

  } catch (error) {
    // If any error occurs (network error, server error, parsing error),
    // display an error message to the user
    list.innerHTML =
      '<p class="text-danger m-0">Failed to load: ' +
      escapeHtml(error.message) +
      "</p>";
  }
}

// -------------------- HTML ESCAPING --------------------

// Escapes HTML special characters to prevent XSS attacks
// This is used when inserting text into innerHTML
function escapeHtml(text) {

  // Handle null or undefined input safely
  if (text === undefined || text === null) {
    return "";
  }

  // Replace dangerous characters with safe HTML entities
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
