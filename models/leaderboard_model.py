from pymongo import MongoClient
import certifi
import os


class LeaderboardModel:
    def __init__(self):
        uri = os.getenv("MONGO_URI")
        if uri is None:
            raise RuntimeError("MONGO_URI missing")

        self.client = MongoClient(
            uri,
            tls=True,
            tlsCAFile=certifi.where()
        )

        self.db = self.client["Group5Project"]
        self.boards = self.db["LeaderBoard"]  # keep this name if that's your collection

    # -------------------- HELPERS --------------------
    def _clean_id(self, doc):
        if doc and "_id" in doc:
            doc["_id"] = str(doc["_id"])
        return doc

    # -------------------- READ --------------------
    def get_all_leaderboards(self):
        boards = list(self.boards.find())
        for b in boards:
            self._clean_id(b)
        return boards

    def get_leaderboard_for_game(self, game):
        board = self.boards.find_one({"game": game})
        return self._clean_id(board)

    # -------------------- CREATE / UPDATE --------------------
    def insert_leaderboard(self, game, leaderboard):
        doc = {"game": game, "leaderboard": leaderboard}
        result = self.boards.insert_one(doc)
        return str(result.inserted_id)

    def update_leaderboard_for_game(self, game, leaderboard):
        result = self.boards.update_one(
            {"game": game},
            {"$set": {"leaderboard": leaderboard}},
            upsert=True
        )

        # upserted_id is an ObjectId or None
        upserted_id = str(result.upserted_id) if result.upserted_id else None
        return result.modified_count, upserted_id

    # -------------------- CLEANUP --------------------
    def close(self):
        self.client.close()
