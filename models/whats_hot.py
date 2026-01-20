import certifi
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

class WhatsHotModel:
    def __init__(self):
        uri = os.getenv("MONGO_URI")
        if not uri:
            raise RuntimeError("MONGO_URI missing")

        self.client = MongoClient(
            uri,
            tls=True,
            tlsCAFile=certifi.where(),
            serverSelectionTimeoutMS=5000
        )

        self.db = self.client["Group5Project"]
        self.collection = self.db["Whats_hot"]

    def get_all_games(self):
        games = list(self.collection.find())
        for game in games:
            game["_id"] = str(game["_id"])  # convert ObjectId for JSON
        return games
