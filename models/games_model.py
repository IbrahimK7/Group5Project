from pymongo import MongoClient
from bson import ObjectId
import certifi
import os

class GamesModel:
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
        self.collection = self.db["Games"]  # change if your collection name differs

    def get_all_games(self):
        games = list(self.collection.find())
        for g in games:
            g["_id"] = str(g["_id"])
        return games

    def get_game_by_id(self, game_id: str):
        game = self.collection.find_one({"_id": ObjectId(game_id)})
        if not game:
            return None
        game["_id"] = str(game["_id"])
        return game

    def get_game_by_title(self, title: str):
        game = self.collection.find_one({"title": title})
        if not game:
            return None
        game["_id"] = str(game["_id"])
        return game

    def insert_game(self, title: str, release_date: str):
        doc = {"title": title, "release_date": release_date}
        res = self.collection.insert_one(doc)
        return str(res.inserted_id)

    def close_connection(self):
        self.client.close()
