from pymongo import MongoClient
from bson import ObjectId
import os
from dotenv import load_dotenv

load_dotenv()

class ProfileModel:
    def __init__(self):
        mongo_uri = os.getenv("MONGO_URI")
        self.client = MongoClient(mongo_uri)
        self.db = self.client['user_database']
        self.collection = self.db['profiles']

    def _serialize(self, doc):
        if not doc:
            return None
        doc = dict(doc)
        if '_id' in doc:
            doc['_id'] = str(doc['_id'])
        if 'user_id' in doc and isinstance(doc['user_id'], ObjectId):
            doc['user_id'] = str(doc['user_id'])
        return doc

    def get_profile(self, user_id):
        # try as ObjectId first, then fallback to string match
        profile = None
        try:
            profile = self.collection.find_one({"user_id": ObjectId(user_id)})
        except Exception:
            profile = self.collection.find_one({"user_id": user_id})
        if profile:
            return {"success": True, "profile": self._serialize(profile)}
        else:
            return {"success": False, "message": "Profile not found."}

    def update_profile(self, user_id, profile_data):
        try:
            query = {"user_id": ObjectId(user_id)}
        except Exception:
            query = {"user_id": user_id}
        result = self.collection.update_one(query, {"$set": profile_data})
        if result.modified_count > 0:
            return {"success": True, "message": "Profile updated successfully."}
        else:
            return {"success": False, "message": "No changes made to the profile."}

class Rank:
    def __init__(self, rank_name, permissions):
        self.rank_name = rank_name
        self.permissions = permissions


class Rating:
    def __init__(self, score, reviews):
        self.score = score
        self.reviews = reviews


class GamesOwned:
    def __init__(self, game_list):
        self.game_list = game_list
