from pymongo import MongoClient
from bson import ObjectId
import certifi
import os
from dotenv import load_dotenv

load_dotenv()

class MessageModel:
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

        self.client.admin.command("ping")  # should now work
        print("✅ Connected to Atlas")

        self.db = self.client["Group5Project"]
        self.collection = self.db["Messages"]


    def get_inbox_for_user(self, username: str):
        """Get messages received by a user (newest first)"""
        messages = list(self.collection.find({"receiver": username}).sort("_id", -1))
        for m in messages:
            m["_id"] = str(m["_id"])
        return messages

    def get_conversation(self, user_a: str, user_b: str):
        """Get all messages between two users"""
        messages = list(self.collection.find({
            "$or": [
                {"sender": user_a, "receiver": user_b},
                {"sender": user_b, "receiver": user_a},
            ]
        }).sort("_id", 1))

        for m in messages:
            m["_id"] = str(m["_id"])
        return messages

    def mark_read(self, message_id: str):
        """Mark a message as read"""
        result = self.collection.update_one(
            {"_id": ObjectId(message_id)},
            {"$set": {"read": True}}
        )
        return result.modified_count > 0

    def close_connection(self):
        """Close MongoDB connection"""
        self.client.close()
