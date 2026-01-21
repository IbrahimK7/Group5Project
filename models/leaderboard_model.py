from pymongo import MongoClient
from bson import ObjectId
import certifi
import os

class LeaderboardModel:
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
        self.collection = self.db["LeaderBoard"]  # change if your collection name differs

    def get_all_leaderboards(self):
        boards = list(self.collection.find())
        for b in boards:
            b["_id"] = str(b["_id"])
        return boards

    def get_leaderboard_for_game(self, game: str):
        board = self.collection.find_one({"game": game})
        if not board:
            return None
        board["_id"] = str(board["_id"])
        return board

    def insert_leaderboard(self, game: str, leaderboard: list):
        """
        leaderboard should be a list like:
        [
          {"rank": 1, "username": "...", "gamertag": "...", "score": 1234},
          ...
        ]
        """
        doc = {"game": game, "leaderboard": leaderboard}
        res = self.collection.insert_one(doc)
        return str(res.inserted_id)

    def update_leaderboard_for_game(self, game: str, leaderboard: list):
        res = self.collection.update_one(
            {"game": game},
            {"$set": {"leaderboard": leaderboard}},
            upsert=True
        )
        return res.modified_count, res.upserted_id

    def close_connection(self):
        self.client.close()
