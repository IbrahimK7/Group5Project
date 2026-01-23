from flask import request, jsonify, render_template, session, redirect, url_for
from models.messages_model import MessageModel

# Create a single instance of the MessageModel
# This handles all database operations related to messages/threads
message_model = MessageModel()


def register_inbox_routes(app):
    """
    Register inbox / messaging-related routes on the Flask application.

    This includes:
    - Inbox HTML page
    - Thread list API used by the inbox page
    - Conversation HTML page
    - Conversation data API used by conversation.js
    - Send-message API used by conversation.js
    """

    # -------------------- INBOX PAGE --------------------
    @app.route("/inbox")
    def inbox():
        """
        Render the inbox page (messages.html).

        Requires the user to be logged in (session must contain "username").
        """
        # Require login
        if "username" not in session:
            return redirect(url_for("login"))

        # Return the HTML page; JS on this page will call /threads to load data
        return render_template("messages.html")

    # -------------------- THREAD LIST API --------------------
    # Used by messages.js (GET /threads)
    @app.route("/threads")
    def api_threads():
        """
        Return all conversation threads for the logged-in user.

        This is an API endpoint (returns JSON).
        """
        # Require login (API style: return JSON error instead of redirect)
        if "username" not in session:
            return jsonify({"error": "Not logged in"}), 401

        # Current logged-in username from session
        username = session["username"]

        # Query DB: get latest message per thread for this user
        threads = message_model.get_threads_for_user(username)

        # Return thread list as JSON
        return jsonify(threads)

    # -------------------- CONVERSATION PAGE --------------------
    @app.route("/messages/<path:thread_id>")
    def thread(thread_id):
        """
        Render the conversation page (conversation.html) for a given thread_id.
        """
        # Require login
        if "username" not in session:
            return redirect(url_for("login"))

        # Pass thread_id into template so frontend JS knows what to fetch
        return render_template("conversation.html", thread_id=thread_id)

    # -------------------- CONVERSATION DATA API --------------------
    # Used by conversation.js (GET /api/threads/<thread_id>)
    @app.route("/api/threads/<path:thread_id>")
    def api_thread(thread_id):
        """
        Return all messages in a thread (conversation) as JSON.

        Also marks messages addressed to the logged-in user as read.
        """
        # Require login
        if "username" not in session:
            return jsonify({"error": "Not logged in"}), 401

        # Logged-in user's username
        me = session["username"]

        # Validate thread_id format (expected: "userA:userB")
        parts = thread_id.split(":")
        if len(parts) != 2:
            return jsonify({"error": "Invalid thread_id"}), 400

        a, b = parts

        # Security check: make sure the logged-in user is part of this thread
        # Prevents users from reading conversations that aren't theirs
        if me not in (a, b):
            return jsonify({"error": "Forbidden"}), 403

        # Fetch all messages between user a and b
        messages = message_model.get_thread_messages(a, b)

        # Mark messages in this thread as read if they were sent TO the logged-in user
        message_model.mark_thread_read(thread_id, me)

        # Return the conversation payload
        return jsonify({
            "me": me,              # used by frontend to render "me" vs "them"
            "messages": messages   # list of message documents
        })

    # -------------------- SEND MESSAGE API --------------------
    # Used by conversation.js (POST /api/messages)
    @app.route("/api/messages", methods=["POST"])
    def api_messages():
        """
        Send a message in a conversation thread.

        Expects JSON body:
        {
          "thread_id": "userA:userB",
          "content": "Hello"
        }
        """
        # Require login
        if "username" not in session:
            return jsonify({"error": "Not logged in"}), 401

        me = session["username"]

        # Read JSON body safely (silent=True avoids exceptions if body isn't valid JSON)
        data = request.get_json(silent=True) or {}

        # Extract and clean inputs
        thread_id = (data.get("thread_id") or "").strip()
        content = (data.get("content") or "").strip()

        # Validate input: thread_id must exist and contain ":"
        if not thread_id or ":" not in thread_id:
            return jsonify({"error": "Invalid thread_id"}), 400

        # Validate input: message content must not be empty
        if not content:
            return jsonify({"error": "Message content required"}), 400

        # Validate thread_id structure (must be exactly 2 usernames)
        parts = thread_id.split(":")
        if len(parts) != 2:
            return jsonify({"error": "Invalid thread_id"}), 400

        # Validate that the current user belongs to this thread
        a, b = parts
        if me not in (a, b):
            return jsonify({"error": "Forbidden"}), 403

        # Determine the other participant in the conversation
        other = b if me == a else a

        # Insert the message into the database
        message_id = message_model.send_message(me, other, content)

        # Return success response and the new message ID
        return jsonify({
            "ok": True,
            "message_id": message_id
        }), 201
