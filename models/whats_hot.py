from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

class WhatsHotModel:
    def __init__(self):
        mongodb_uri = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/')
        database_name = 'whats_hot'   # ✅ NO SPACES
        
        self.client = MongoClient(mongodb_uri)
        self.db = self.client[database_name]
        self.collection = self.db['games']

    def get_all_games(self):
        """Get all games"""
        games = list(self.collection.find())
        for game in games:
            game['_id'] = str(game['_id'])
        return games

    def get_game_by_name(self, name):
        """Get a single game by name"""
        game = self.collection.find_one({"name": name})
        if game:
            game['_id'] = str(game['_id'])
        return game

    def close_connection(self):
        """Close MongoDB connection"""
        self.client.close()
