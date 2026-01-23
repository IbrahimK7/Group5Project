import certifi
from pymongo import MongoClient
from bson import ObjectId
import os
from dotenv import load_dotenv

load_dotenv()


class PartyModel:
    def __init__(self):
        """
        Initialize the PartyModel by connecting to MongoDB
        and selecting the Parties collection.
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

        # Select the Parties collection
        self.parties = self.db["Parties"]

        # Alias kept for compatibility / readability
        self.collection = self.parties

    # -------------------- HELPERS --------------------
    def _to_object_id(self, party_id):
        """
        Safely convert a party_id string to a MongoDB ObjectId.

        Args:
            party_id (str): Party ID as a string.

        Returns:
            ObjectId or None: Converted ObjectId if valid, otherwise None.
        """
        try:
            return ObjectId(party_id)
        except Exception:
            # Return None if the ID is not a valid ObjectId
            return None

    # -------------------- READ --------------------
    def get_all_parties(self):
        """
        Retrieve all party documents from the Parties collection.

        Returns:
            list: A list of party documents with stringified _id fields.
        """
        parties = list(self.parties.find())
        for p in parties:
            # Convert ObjectId to string for JSON compatibility
            p["_id"] = str(p["_id"])
        return parties

    # -------------------- CREATE --------------------
    def add_party(self, party_data):
        """
        Insert a new party document into the Parties collection.

        Args:
            party_data (dict): Dictionary containing party information.

        Returns:
            str: The inserted party ID as a string.
        """
        result = self.parties.insert_one(party_data)
        return str(result.inserted_id)

    # -------------------- DELETE --------------------
    def remove_party(self, party_id):
        """
        Delete a party document by its ID.

        Args:
            party_id (str): Party ID as a string.

        Returns:
            bool: True if a party was deleted, False otherwise.
        """
        # Convert string ID to ObjectId safely
        oid = self._to_object_id(party_id)
        if oid is None:
            # Invalid ObjectId string
            return False

        # Attempt to delete the document
        result = self.parties.delete_one({"_id": oid})

        # deleted_count > 0 means a document was actually removed
        return result.deleted_count > 0

    # -------------------- CLEANUP --------------------
    def close(self):
        """
        Close the MongoDB client connection.
        """
        self.client.close()
