// Wait until the HTML document is fully loaded
// This ensures all DOM elements exist before we access them
document.addEventListener("DOMContentLoaded", function () {
  loadConversation(); // Load and display existing messages
  wireComposer();     // Enable the message input + send button
});

// -------------------- LOAD CONVERSATION --------------------
function loadConversation() {

  // Get the main message container (where chat bubbles go)
  const box = document.getElementById("chatMessages");

  // Get the element that shows who the conversation is with
  const withEl = document.getElementById("conversationWith");

  // If required elements do not exist, stop early
  if (!box || !withEl) return;

  // Send a GET request to the backend to fetch the conversation
  fetch("/api/threads/" + encodeURIComponent(THREAD_ID))

    // First .then(): check if the HTTP response is valid
    .then(function (response) {

      // If the server responded with an error status (4xx / 5xx)
      if (!response.ok) {

        // Try to read the error body as JSON (if possible)
        return response.json().catch(function () {
          return {}; // Fallback if the body is not JSON
        }).then(function (err) {

          // Throw an error so it is caught in the .catch() below
          throw new Error(
            err.error || "Request failed (" + response.status + ")"
          );
        });
      }

      // If the response is OK, parse it as JSON
      return response.json();
    })

    // Second .then(): handle the parsed JSON data
    .then(function (data) {

      // Username of the currently logged-in user
      const me = data.me;

      // Array of messages in this conversation
      const messages = data.messages || [];

      // THREAD_ID looks like "alice:bob"
      const parts = THREAD_ID.split(":");

      // Determine who the other user is
      const otherUser = (parts[0] === me) ? parts[1] : parts[0];

      // Display who the conversation is with
      withEl.textContent = "With " + otherUser;

      // If there are no messages yet, show a placeholder
      if (messages.length === 0) {
        box.innerHTML =
          '<div class="text-muted small text-center py-3">No messages yet.</div>';
        return;
      }

      // Clear the message container
      box.innerHTML = "";

      // Render each message as a chat bubble
      for (let i = 0; i < messages.length; i++) {
        box.insertAdjacentHTML(
          "beforeend",
          renderBubble(messages[i], me)
        );
      }

      // Scroll to the bottom so the latest message is visible
      box.scrollTop = box.scrollHeight;
    })

    // Catch any errors from fetch, JSON parsing, or thrown errors
    .catch(function (error) {
      box.innerHTML =
        '<div class="text-danger small text-center py-3">' +
        escapeHtml(error.message) +
        "</div>";
    });
}

// -------------------- MESSAGE COMPOSER --------------------
function wireComposer() {

  // Get the message form and input field
  const form = document.getElementById("messageForm");
  const input = document.getElementById("messageInput");

  // If elements are missing, do nothing
  if (!form || !input) return;

  // Listen for form submission (pressing Enter or clicking Send)
  form.addEventListener("submit", function (event) {

    // Prevent the browser’s default form submission (page reload)
    event.preventDefault();

    // Read and trim the message text
    const content = input.value.trim();

    // Do not send empty messages
    if (!content) return;

    // Disable input to prevent double sending
    input.disabled = true;

    // Send the message to the backend
    fetch("/api/messages", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        thread_id: THREAD_ID,
        content: content
      })
    })

      // Check if the send request succeeded
      .then(function (response) {
        if (!response.ok) {
          return response.json().catch(function () {
            return {};
          }).then(function (err) {
            throw new Error(
              err.error || "Send failed (" + response.status + ")"
            );
          });
        }

        // We don’t really need the response body here
        return response.json().catch(function () {
          return null;
        });
      })

      // On successful send
      .then(function () {

        // Clear the input field
        input.value = "";

        // Reload the conversation to show the new message
        loadConversation();
      })

      // Handle any send errors
      .catch(function (error) {
        alert("Failed to send: " + error.message);
      })

      // Always re-enable input and refocus
      .finally(function () {
        input.disabled = false;
        input.focus();
      });
  });
}

// -------------------- MESSAGE BUBBLE RENDERING --------------------
function renderBubble(message, me) {

  // Check if this message was sent by the current user
  const isMe = message.sender === me;

  // Choose CSS classes based on message ownership
  const rowClass = isMe ? "row-me" : "row-them";
  const bubbleClass = isMe ? "bubble bubble-me" : "bubble bubble-them";

  // Display "You" for your own messages
  const senderName = isMe
    ? "You"
    : escapeHtml(message.sender || "Unknown");

  // Escape message text to prevent HTML injection
  const text = escapeHtml(message.content || "");

  // Return the HTML string for the chat bubble
  return (
    '<div class="bubble-row ' + rowClass + '">' +
      '<div class="' + bubbleClass + '">' +
        '<div class="bubble-meta">' + senderName + '</div>' +
        '<div class="bubble-text">' + text + '</div>' +
      '</div>' +
    '</div>'
  );
}

// -------------------- HTML ESCAPING (SECURITY) --------------------
function escapeHtml(text) {

  // Handle null or undefined values safely
  if (text === undefined || text === null) return "";

  // Replace dangerous characters with safe HTML entities
  // This prevents XSS (cross-site scripting) attacks
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
