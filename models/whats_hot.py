from pymongo import MongoClient
import certifi
import os


class WhatsHotModel:
    def __init__(self):
        # Read the MongoDB connection string from environment variables
        uri = os.getenv("MONGO_URI")
        if not uri:
            # Fail fast if the application is misconfigured
            raise RuntimeError("MONGO_URI missing")

        # Create a MongoDB client
        self.client = MongoClient(
            uri,
            tls=uri.startswith("mongodb+srv"),
            tlsCAFile=certifi.where() if uri.startswith("mongodb+srv") else None,
            serverSelectionTimeoutMS=5000
        )

        # Select the database
        self.db = self.client["Group5Project"]

        # Select the collection that stores "What's Hot" game documents
        self.collection = self.db["Whats_hot"]

    # -------------------- READ --------------------
    def get_all_games(self):
        """
        Retrieve all game documents from the Whats_hot collection.

        Returns:
            list: A list of game documents with stringified _id fields
                  so they are safe to return as JSON.
        """
        games = list(self.collection.find())

        # Convert ObjectId to string for JSON compatibility
        for game in games:
            game["_id"] = str(game["_id"])

        return games
