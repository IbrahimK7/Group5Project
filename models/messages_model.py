from pymongo import MongoClient
from bson import ObjectId
import certifi
import os
from dotenv import load_dotenv
from datetime import datetime

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

        self.db = self.client["Group5Project"]
        self.collection = self.db["Messages"]  # case-sensitive

    def _thread_id(self, a: str, b: str) -> str:
        return ":".join(sorted([a, b]))

    def send_message(self, sender: str, receiver: str, content: str) -> str:
        doc = {
            "thread_id": self._thread_id(sender, receiver),
            "sender": sender,
            "receiver": receiver,
            "content": content,
            "read": False,
            "created_at": datetime.utcnow()
        }
        result = self.collection.insert_one(doc)
        return str(result.inserted_id)

    def get_threads_for_user(self, username: str):
        pipeline = [
            {"$match": {"$or": [{"sender": username}, {"receiver": username}]}},
            {"$sort": {"_id": -1}},
            {"$group": {"_id": "$thread_id", "last": {"$first": "$$ROOT"}}},
            {"$sort": {"last._id": -1}},
        ]
        rows = list(self.collection.aggregate(pipeline))
        threads = []
        for r in rows:
            m = r["last"]
            m["_id"] = str(m["_id"])
            other = m["receiver"] if m["sender"] == username else m["sender"]
            threads.append({
                "thread_id": r["_id"],
                "other_user": other,
                "last_message": m
            })
        return threads

    def get_thread_messages(self, user_a: str, user_b: str):
        thread_id = self._thread_id(user_a, user_b)
        messages = list(self.collection.find({"thread_id": thread_id}).sort("_id", 1))
        for m in messages:
            m["_id"] = str(m["_id"])
        return messages

    def mark_read(self, message_id: str) -> bool:
        result = self.collection.update_one(
            {"_id": ObjectId(message_id)},
            {"$set": {"read": True}}
        )
        return result.modified_count > 0

    def mark_thread_read(self, thread_id: str, username: str) -> int:
        result = self.collection.update_many(
            {"thread_id": thread_id, "receiver": username, "read": False},
            {"$set": {"read": True}}
        )
        return result.modified_count

    def close_connection(self):
        self.client.close()
