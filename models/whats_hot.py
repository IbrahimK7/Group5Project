from pymongo import MongoClient
import certifi
import os

class WhatsHotModel:
    def __init__(self):
        uri = os.getenv("MONGO_URI")
        if not uri:
            raise RuntimeError("MONGO_URI missing")

        self.client = MongoClient(
            uri,
            tls=uri.startswith("mongodb+srv"),
            tlsCAFile=certifi.where() if uri.startswith("mongodb+srv") else None,
            serverSelectionTimeoutMS=5000
        )

        self.db = self.client["Group5Project"]
        self.collection = self.db["Whats_hot"]

    def get_all_games(self):
        games = list(self.collection.find())
        for game in games:
            game["_id"] = str(game["_id"])
        return games
