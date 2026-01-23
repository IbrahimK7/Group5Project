from flask import render_template, jsonify
from models.whats_hot import WhatsHotModel
from models.games_model import GamesModel
from models.leaderboard_model import LeaderboardModel

# Create model instances
# Each model handles database access for a specific feature
whats_hot_model = WhatsHotModel()
games_model = GamesModel()
leaderboard_model = LeaderboardModel()


def register_home_routes(app):
    """
    Register home-page-related routes on the Flask application.

    This includes:
    - the home page HTML
    - API endpoints used by the homepage (What's Hot, Games, Leaderboards)
    """

    # -------------------- HOME PAGE --------------------
    @app.route("/home")
    def home():
        """
        Render the main home page.
        """
        return render_template("home.html")

    # -------------------- WHAT'S HOT API --------------------
    @app.route("/whats-hot")
    def whats_hot():
        """
        Return "What's Hot" game data as JSON.
        """
        games = whats_hot_model.get_all_games()
        return jsonify(games)

    # -------------------- ALL GAMES API --------------------
    @app.route("/api/games")
    def api_games():
        """
        Return all games as JSON.
        """
        games = games_model.get_all_games()
        return jsonify(games)

    # -------------------- LEADERBOARDS API --------------------
    @app.route("/api/leaderboards")
    def api_leaderboards():
        """
        Return all leaderboards as JSON.
        """
        boards = leaderboard_model.get_all_leaderboards()
        return jsonify(boards)
