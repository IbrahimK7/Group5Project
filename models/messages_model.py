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
        if uri is None:
            raise RuntimeError("MONGO_URI missing")

        self.client = MongoClient(
            uri,
            tls=True,
            tlsCAFile=certifi.where()
        )

        self.db = self.client["Group5Project"]
        self.messages = self.db["Messages"]

    # -------------------- HELPERS --------------------
    def _thread_id(self, user_a, user_b):
        # Ensure both users get the same thread_id order
        return ":".join(sorted([user_a, user_b]))

    def _clean_id(self, doc):
        if doc and "_id" in doc:
            doc["_id"] = str(doc["_id"])
        return doc

    # -------------------- CREATE --------------------
    def send_message(self, sender, receiver, content):
        doc = {
            "thread_id": self._thread_id(sender, receiver),
            "sender": sender,
            "receiver": receiver,
            "content": content,
            "read": False,
            "created_at": datetime.utcnow()
        }

        result = self.messages.insert_one(doc)
        return str(result.inserted_id)

    # -------------------- READ --------------------
    def get_thread_messages(self, user_a, user_b):
        thread_id = self._thread_id(user_a, user_b)

        msgs = list(
            self.messages.find({"thread_id": thread_id}).sort("_id", 1)
        )

        for m in msgs:
            self._clean_id(m)

        return msgs

    def get_threads_for_user(self, username):
        # Get latest message per thread for this user
        pipeline = [
            {"$match": {"$or": [{"sender": username}, {"receiver": username}]}},
            {"$sort": {"_id": -1}},
            {"$group": {"_id": "$thread_id", "last": {"$first": "$$ROOT"}}},
            {"$sort": {"last._id": -1}},
        ]

        rows = list(self.messages.aggregate(pipeline))
        threads = []

        for row in rows:
            last = row["last"]
            self._clean_id(last)

            if last.get("sender") == username:
                other = last.get("receiver")
            else:
                other = last.get("sender")

            threads.append({
                "thread_id": row["_id"],
                "other_user": other,
                "last_message": last
            })

        return threads

    # -------------------- UPDATE (READ STATUS) --------------------
    def mark_read(self, message_id):
        result = self.messages.update_one(
            {"_id": ObjectId(message_id)},
            {"$set": {"read": True}}
        )
        return result.modified_count > 0

    def mark_thread_read(self, thread_id, username):
        # Mark messages sent TO this user in that thread as read
        result = self.messages.update_many(
            {"thread_id": thread_id, "receiver": username, "read": False},
            {"$set": {"read": True}}
        )
        return result.modified_count

    # -------------------- CLEANUP --------------------
    def close(self):
        self.client.close()
