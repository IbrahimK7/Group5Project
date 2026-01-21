from pymongo import MongoClient
from bson import ObjectId
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

class PlayerStatsModel:
    def __init__(self):
        mongo_uri = os.getenv("MONGO_URI")
        self.client = MongoClient(mongo_uri)
        self.db = self.client['Group5Project']
        self.collection = self.db['playerstats']

    def join_party(self, user_id, party_id):
        """Add user to party"""
        # Check if user is already in a party
        existing = self.collection.find_one({"user_id": user_id})
        if existing:
            return {"success": False, "message": "User already in a party"}

        doc = {
            "user_id": user_id,
            "party_id": party_id,
            "joined_at": datetime.utcnow(),
            "status": "active"
        }
        result = self.collection.insert_one(doc)
        return {"success": True, "inserted_id": str(result.inserted_id)}

    def leave_party(self, user_id):
        """Remove user from party"""
        result = self.collection.delete_one({"user_id": user_id})
        if result.deleted_count > 0:
            return {"success": True, "message": "Left party successfully"}
        return {"success": False, "message": "User not in any party"}

    def get_user_party(self, user_id):
        """Get user's current party"""
        doc = self.collection.find_one({"user_id": user_id})
        if doc:
            doc["_id"] = str(doc["_id"])
            doc["party_id"] = str(doc["party_id"])
        return doc

    def get_party_members(self, party_id):
        """Get all members of a party"""
        members = list(self.collection.find({"party_id": party_id}))
        for member in members:
            member["_id"] = str(member["_id"])
            member["user_id"] = str(member["user_id"])
        return members