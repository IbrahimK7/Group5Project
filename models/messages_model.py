from pymongo import MongoClient
from bson import ObjectId
import certifi
import os
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables from .env file
load_dotenv()


class MessageModel:
    def __init__(self):
        """
        Initialize the MessageModel by connecting to MongoDB
        and selecting the Messages collection.
        """
        # Read the MongoDB connection string from environment variables
        uri = os.getenv("MONGO_URI")
        if uri is None:
            # Fail fast if the application is misconfigured
            raise RuntimeError("MONGO_URI missing")

        # Create a MongoDB client
        # TLS is enabled to securely connect to MongoDB Atlas
        # certifi provides trusted CA certificates for validation
        self.client = MongoClient(
            uri,
            tls=True,
            tlsCAFile=certifi.where()
        )

        # Select the database
        self.db = self.client["Group5Project"]

        # Select the collection that stores message documents
        self.messages = self.db["Messages"]

    # -------------------- HELPERS --------------------
    def _thread_id(self, user_a, user_b):
        """
        Generate a deterministic thread ID for two users.

        Sorting ensures that:
        - userA:userB and userB:userA produce the same thread_id
        - both users see the same conversation thread
        """
        return ":".join(sorted([user_a, user_b]))

    def _clean_id(self, doc):
        """
        Convert MongoDB ObjectId to string so it can be safely returned as JSON.
        """
        if doc and "_id" in doc:
            doc["_id"] = str(doc["_id"])
        return doc

    # -------------------- CREATE --------------------
    def send_message(self, sender, receiver, content):
        """
        Insert a new message into the Messages collection.

        Args:
            sender (str): Username of the sender.
            receiver (str): Username of the receiver.
            content (str): Message text.

        Returns:
            str: The inserted message ID as a string.
        """
        doc = {
            # Thread identifier shared between sender and receiver
            "thread_id": self._thread_id(sender, receiver),

            # Message metadata
            "sender": sender,
            "receiver": receiver,
            "content": content,

            # Read status (false by default for new messages)
            "read": False,

            # Timestamp for ordering and display
            "created_at": datetime.utcnow()
        }

        result = self.messages.insert_one(doc)
        return str(result.inserted_id)

    # -------------------- READ --------------------
    def get_thread_messages(self, user_a, user_b):
        """
        Retrieve all messages in a conversation thread between two users.

        Messages are sorted by insertion order (_id),
        which corresponds to chronological order.

        Args:
            user_a (str): First username.
            user_b (str): Second username.

        Returns:
            list: List of message documents with stringified _id fields.
        """
        thread_id = self._thread_id(user_a, user_b)

        msgs = list(
            self.messages
            .find({"thread_id": thread_id})
            .sort("_id", 1)  # Ascending order (oldest -> newest)
        )

        for m in msgs:
            self._clean_id(m)

        return msgs

    def get_threads_for_user(self, username):
        """
        Retrieve a list of conversation threads for a given user,
        including the latest message in each thread.

        This uses a MongoDB aggregation pipeline to:
        - filter messages involving the user
        - group messages by thread_id
        - extract the most recent message per thread
        - sort threads by recency

        Args:
            username (str): Username whose threads are requested.

        Returns:
            list: List of thread summaries containing:
                  - thread_id
                  - other_user
                  - last_message
        """
        pipeline = [
            # Only messages where the user is sender or receiver
            {"$match": {"$or": [
                {"sender": username},
                {"receiver": username}
            ]}},

            # Sort messages so newest messages come first
            {"$sort": {"_id": -1}},

            # Group by thread_id and keep the first (newest) message
            {"$group": {
                "_id": "$thread_id",
                "last": {"$first": "$$ROOT"}
            }},

            # Sort threads by most recent activity
            {"$sort": {"last._id": -1}},
        ]

        rows = list(self.messages.aggregate(pipeline))
        threads = []

        for row in rows:
            last = row["last"]
            self._clean_id(last)

            # Determine the "other" user in the thread
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
        """
        Mark a single message as read.

        Args:
            message_id (str): MongoDB message ID.

        Returns:
            bool: True if the message was updated, False otherwise.
        """
        result = self.messages.update_one(
            {"_id": ObjectId(message_id)},
            {"$set": {"read": True}}
        )
        return result.modified_count > 0

    def mark_thread_read(self, thread_id, username):
        """
        Mark all unread messages in a thread as read
        where the given user is the receiver.

        Args:
            thread_id (str): Conversation thread ID.
            username (str): User who has read the messages.

        Returns:
            int: Number of messages updated.
        """
        result = self.messages.update_many(
            {
                "thread_id": thread_id,
                "receiver": username,
                "read": False
            },
            {"$set": {"read": True}}
        )
        return result.modified_count

    # -------------------- CLEANUP --------------------
    def close(self):
        """
        Close the MongoDB client connection.
        """
        self.client.close()
