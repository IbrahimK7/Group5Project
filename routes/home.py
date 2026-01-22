from flask import render_template, jsonify
from models.whats_hot import WhatsHotModel
from models.games_model import GamesModel
from models.leaderboard_model import LeaderboardModel

whats_hot_model = WhatsHotModel()
games_model = GamesModel()
leaderboard_model = LeaderboardModel()


def register_home_routes(app):

    # Home page
    @app.route("/home")
    def home():
        return render_template("home.html")

    # Whats hot data (used by homepage)
    @app.route("/whats-hot")
    def whats_hot():
        games = whats_hot_model.get_all_games()
        return jsonify(games)

    # All games API
    @app.route("/api/games")
    def api_games():
        games = games_model.get_all_games()
        return jsonify(games)

    # Leaderboards API
    @app.route("/api/leaderboards")
    def api_leaderboards():
        boards = leaderboard_model.get_all_leaderboards()
        return jsonify(boards)
