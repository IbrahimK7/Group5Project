from models.messages_model import MessageModel
from flask import request, jsonify, render_template, session, redirect, url_for

message_model = MessageModel()

def register_inbox_routes(app):

    @app.route('/inbox')
    def inbox():
        if "username" not in session:
            return redirect(url_for("login"))
        return render_template("messages.html")

    # inbox list (messages.js calls GET /threads)
    @app.route('/threads', methods=['GET'])
    def api_threads():
        if "username" not in session:
            return jsonify({"error": "Not logged in"}), 401

        username = session["username"]
        threads = message_model.get_threads_for_user(username)
        return jsonify(threads), 200

    # conversation page (clicking a thread goes to /messages/<thread_id>)
    @app.route("/messages/<path:thread_id>")
    def thread(thread_id):
        if "username" not in session:
            return redirect(url_for("login"))
        return render_template("conversation.html", thread_id=thread_id)

    # ✅ conversation data (conversation.js calls GET /api/threads/<thread_id>)
    @app.route("/api/threads/<path:thread_id>", methods=["GET"])
    def api_thread(thread_id):
        if "username" not in session:
            return jsonify({"error": "Not logged in"}), 401

        me = session["username"]

        parts = thread_id.split(":")
        if len(parts) != 2:
            return jsonify({"error": "Invalid thread_id"}), 400

        a, b = parts
        if me not in (a, b):
            return jsonify({"error": "Forbidden"}), 403

        messages = message_model.get_thread_messages(a, b)

        # optional: mark messages sent TO me as read
        message_model.mark_thread_read(thread_id, me)

        return jsonify({"me": me, "messages": messages}), 200

    # ✅ send message (conversation.js should POST /api/messages)
    @app.route("/api/messages", methods=["POST"])
    def api_messages():
        if "username" not in session:
            return jsonify({"error": "Not logged in"}), 401

        me = session["username"]
        data = request.get_json(silent=True) or {}

        thread_id = (data.get("thread_id") or "").strip()
        content = (data.get("content") or "").strip()

        if not thread_id or ":" not in thread_id:
            return jsonify({"error": "Invalid thread_id"}), 400
        if not content:
            return jsonify({"error": "Message content required"}), 400

        parts = thread_id.split(":")
        if len(parts) != 2:
            return jsonify({"error": "Invalid thread_id"}), 400

        a, b = parts
        if me not in (a, b):
            return jsonify({"error": "Forbidden"}), 403

        other = b if me == a else a

        message_id = message_model.send_message(me, other, content)
        return jsonify({"ok": True, "message_id": message_id}), 201
