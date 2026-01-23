from pymongo import MongoClient
import certifi
import os


class LeaderboardModel:
    def __init__(self):
        """
        Initialize the LeaderboardModel by connecting to MongoDB
        and selecting the appropriate database and collection.
        """
        # Read the MongoDB connection string from environment variables
        uri = os.getenv("MONGO_URI")
        if uri is None:
            # Fail fast if the application is misconfigured
            raise RuntimeError("MONGO_URI missing")

        # Create a MongoDB client
        self.client = MongoClient(
            uri,
            tls=True,
            tlsCAFile=certifi.where()
        )

        # Select the database
        self.db = self.client["Group5Project"]

        # Select the collection that stores leaderboard documents
        # (Collection name kept as "LeaderBoard" to match the database)
        self.boards = self.db["LeaderBoard"]

    # -------------------- HELPERS --------------------
    def _clean_id(self, doc):
        """
        Convert MongoDB ObjectId to string so it can be safely returned as JSON.
        """
        if doc and "_id" in doc:
            doc["_id"] = str(doc["_id"])
        return doc

    # -------------------- READ --------------------
    def get_all_leaderboards(self):
        """
        Retrieve all leaderboard documents from the collection.

        Returns:
            list: A list of leaderboard documents with stringified _id fields.
        """
        boards = list(self.boards.find())
        for board in boards:
            self._clean_id(board)
        return boards

    def get_leaderboard_for_game(self, game):
        """
        Retrieve the leaderboard for a specific game.

        Args:
            game (str): Name of the game.

        Returns:
            dict or None: The leaderboard document for the game,
            or None if no leaderboard exists.
        """
        board = self.boards.find_one({"game": game})
        return self._clean_id(board)

    # -------------------- CREATE / UPDATE --------------------
    def insert_leaderboard(self, game, leaderboard):
        """
        Insert a new leaderboard document into the collection.

        Args:
            game (str): Name of the game.
            leaderboard (list): Leaderboard data (e.g., players and scores).

        Returns:
            str: The inserted document's ID as a string.
        """
        result = self.boards.insert_one({
            "game": game,
            "leaderboard": leaderboard
        })
        return str(result.inserted_id)

    def update_leaderboard_for_game(self, game, leaderboard):
        """
        Update the leaderboard for a given game.
        If no leaderboard exists for the game, create one (upsert).

        Args:
            game (str): Name of the game.
            leaderboard (list): Updated leaderboard data.

        Returns:
            tuple:
                - modified_count (int): Number of documents updated (0 or 1).
                - upserted_id (str or None): ID of the inserted document if
                  an upsert occurred, otherwise None.
        """
        result = self.boards.update_one(
            {"game": game},
            {"$set": {"leaderboard": leaderboard}},
            upsert=True
        )

        # Convert upserted_id to string if a new document was created
        upserted_id = str(result.upserted_id) if result.upserted_id else None
        return result.modified_count, upserted_id

    # -------------------- CLEANUP --------------------
    def close(self):
        """
        Close the MongoDB client connection.
        """
        self.client.close()
