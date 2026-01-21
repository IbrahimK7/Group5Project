from flask import render_template, jsonify

from models.whats_hot import WhatsHotModel

whats_hot_model = WhatsHotModel()

def register_home_routes(app):
    @app.route("/home")
    def home():
        return render_template("home.html")

    @app.route("/whats-hot")
    def whats_hot():
        return jsonify(whats_hot_model.get_all_games())
