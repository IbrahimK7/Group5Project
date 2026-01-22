// Run code after the page is fully loaded
document.addEventListener("DOMContentLoaded", function () {
  loadConversation();
  wireComposer();
});

// -------------------- LOAD CONVERSATION --------------------
async function loadConversation() {
  const box = document.getElementById("chatMessages");
  const withEl = document.getElementById("conversationWith");

  if (!box || !withEl) {
    return;
  }

  try {
    // 1) Request conversation data
    const response = await fetch(
      "/api/threads/" + encodeURIComponent(THREAD_ID)
    );

    if (!response.ok) {
      let err = {};
      try {
        err = await response.json();
      } catch (_) {}
      throw new Error(err.error || "Request failed (" + response.status + ")");
    }

    // 2) Read JSON response
    const data = await response.json();
    const me = data.me;
    const messages = data.messages || [];

    // 3) Show who the conversation is with
    const parts = THREAD_ID.split(":");
    let otherUser;

    if (parts[0] === me) {
      otherUser = parts[1];
    } else {
      otherUser = parts[0];
    }

    withEl.textContent = "With " + otherUser;

    // 4) No messages yet
    if (messages.length === 0) {
      box.innerHTML =
        '<div class="text-muted small text-center py-3">No messages yet.</div>';
      return;
    }

    // 5) Clear message box
    box.innerHTML = "";

    // 6) Render each message
    for (let i = 0; i < messages.length; i++) {
      const message = messages[i];
      const bubbleHtml = renderBubble(message, me);

      box.insertAdjacentHTML("beforeend", bubbleHtml);
    }

    // 7) Scroll to bottom
    box.scrollTop = box.scrollHeight;

  } catch (error) {
    box.innerHTML =
      '<div class="text-danger small text-center py-3">' +
      escapeHtml(error.message) +
      "</div>";
  }
}

// -------------------- MESSAGE COMPOSER --------------------
function wireComposer() {
  const form = document.getElementById("messageForm");
  const input = document.getElementById("messageInput");

  if (!form || !input) {
    return;
  }

  form.addEventListener("submit", async function (event) {
    event.preventDefault();

    const content = input.value.trim();
    if (content === "") {
      return;
    }

    // Disable input while sending
    input.disabled = true;

    try {
      const response = await fetch("/api/messages", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          thread_id: THREAD_ID,
          content: content
        })
      });

      if (!response.ok) {
        let err = {};
        try {
          err = await response.json();
        } catch (_) {}
        throw new Error(err.error || "Send failed (" + response.status + ")");
      }

      // Clear input and reload conversation
      input.value = "";
      await loadConversation();

    } catch (error) {
      alert("Failed to send: " + error.message);
    } finally {
      input.disabled = false;
      input.focus();
    }
  });
}

// -------------------- MESSAGE BUBBLE --------------------
function renderBubble(message, me) {
  const isMe = message.sender === me;

  const rowClass = isMe ? "row-me" : "row-them";
  const bubbleClass = isMe ? "bubble bubble-me" : "bubble bubble-them";

  const senderName = isMe
    ? "You"
    : escapeHtml(message.sender || "Unknown");

  const text = escapeHtml(message.content || "");

  return (
    '<div class="bubble-row ' + rowClass + '">' +
      '<div class="' + bubbleClass + '">' +
        '<div class="bubble-meta">' + senderName + "</div>" +
        '<div class="bubble-text">' + text + "</div>" +
      "</div>" +
    "</div>"
  );
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
