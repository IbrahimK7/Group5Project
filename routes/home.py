from flask import render_template, jsonify

from models.whats_hot import WhatsHotModel
from models.games_model import GamesModel
from models.leaderboard_model import LeaderboardModel


whats_hot_model = WhatsHotModel()
games_model = GamesModel()
leaderboard_model = LeaderboardModel()



def register_home_routes(app):
    @app.route("/home")
    def home():
        return render_template("home.html")

    @app.route("/whats-hot")
    def whats_hot():
        return jsonify(whats_hot_model.get_all_games())

    @app.route("/api/games")
    def api_games():
        return jsonify(games_model.get_all_games())

    @app.route("/api/leaderboards")
    def api_leaderboards():
        return jsonify(leaderboard_model.get_all_leaderboards())

