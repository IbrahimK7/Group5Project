from pymongo import MongoClient
from bson import ObjectId
import certifi
import os


class GamesModel:
    def __init__(self):
        uri = os.getenv("MONGO_URI")
        if uri is None:
            raise RuntimeError("MONGO_URI missing")

        # Connect to MongoDB
        self.client = MongoClient(
            uri,
            tls=uri.startswith("mongodb+srv"),
            tlsCAFile=certifi.where() if uri.startswith("mongodb+srv") else None
        )

        self.db = self.client["Group5Project"]
        self.games = self.db["Games"]

    # -------------------- HELPERS --------------------
    def _clean_id(self, doc):
        if doc and "_id" in doc:
            doc["_id"] = str(doc["_id"])
        return doc

    # -------------------- QUERIES --------------------
    def get_all_games(self):
        games = list(self.games.find())
        for game in games:
            self._clean_id(game)
        return games

    def get_game_by_id(self, game_id):
        game = self.games.find_one({"_id": ObjectId(game_id)})
        return self._clean_id(game)

    def get_game_by_title(self, title):
        game = self.games.find_one({"title": title})
        return self._clean_id(game)

    # -------------------- INSERT --------------------
    def insert_game(self, title, release_date):
        result = self.games.insert_one({
            "title": title,
            "release_date": release_date
        })
        return str(result.inserted_id)

    # -------------------- CLEANUP --------------------
    def close(self):
        self.client.close()
