from pymongo import MongoClient
from bson import ObjectId
import certifi
import os


class GamesModel:
    def __init__(self):
        # Read the MongoDB connection string from environment variables
        uri = os.getenv("MONGO_URI")
        if uri is None:
            # Fail fast if the app is misconfigured
            raise RuntimeError("MONGO_URI missing")

        # Create a MongoDB client
        self.client = MongoClient(
            uri,
            tls=uri.startswith("mongodb+srv"),
            tlsCAFile=certifi.where() if uri.startswith("mongodb+srv") else None
        )

        # Select the database
        self.db = self.client["Group5Project"]

        # Select the collection that stores game documents
        self.games = self.db["Games"]

    # -------------------- HELPERS --------------------
    def _clean_id(self, doc):
        """
        Convert MongoDB ObjectId to string so it can be safely returned as JSON.

        """
        if doc and "_id" in doc:
            doc["_id"] = str(doc["_id"])
        return doc

    # -------------------- QUERIES --------------------
    def get_all_games(self):
        """
        Return all games in the collection as a Python list.
        Also converts each document's _id into a string for JSON compatibility.
        """
        games = list(self.games.find())
        for game in games:
            self._clean_id(game)
        return games

    def get_game_by_id(self, game_id):
        """
        Return a single game by its MongoDB _id.
        """
        game = self.games.find_one({"_id": ObjectId(game_id)})
        return self._clean_id(game)

    def get_game_by_title(self, title):
        """
        Return a game document by exact title match.
        """
        game = self.games.find_one({"title": title})
        return self._clean_id(game)

    # -------------------- INSERT --------------------
    def insert_game(self, title, release_date):
        """
        Insert a new game document into the Games collection.
        Returns the inserted document id as a string.
        """
        result = self.games.insert_one({
            "title": title,
            "release_date": release_date
        })
        return str(result.inserted_id)

    # -------------------- CLEANUP --------------------
    def close(self):
        """
        Close the MongoDB client connection.
        """
        self.client.close()
