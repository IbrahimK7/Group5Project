from models.messages_model import MessageModel
from flask import request, jsonify, render_template

message_model = MessageModel()


def register_inbox_routes(app):

    @app.route('/inbox')
    def inbox():
        return render_template("messages.html")
    
    @app.route('/api/messages', methods=['GET'])
    def api_messages():
        # demo: /api/messages?user=user001
        username = "user001"
        messages = message_model.get_inbox_for_user(username)
        return jsonify(messages)
