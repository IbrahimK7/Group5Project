from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

class WhatsHotModel:
    def __init__(self):
        mongodb_uri = os.getenv("MONGODB_URI", "mongodb://localhost:27017/")
        database_name = "Group5Project"   # ✅ correct DB

        self.client = MongoClient(mongodb_uri)
        self.db = self.client[database_name]
        self.collection = self.db["whats_hot"]  # ✅ correct collection

    def get_all_games(self):
        games = list(self.collection.find())
        for game in games:
            game["_id"] = str(game["_id"])  # convert ObjectId for JSON
        return games
