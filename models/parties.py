from pymongo import MongoClient
from bson import ObjectId
import os
from dotenv import load_dotenv

load_dotenv()

class PartyModel:
    def __init__(self):
        mongodb_uri = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/')
        database_name = "Group5Project" 
        
        self.client = MongoClient(mongodb_uri)
        self.db = self.client[database_name]
        self.collection = self.db['Parties']

    def add_party(self, party_data):
        """
        Add a new party document to the database.
        Example data:
        {
            "partyName": "Toxic Lobby",
            "game": "CS:GO",
            "maxPlayers": 10,
            "currentPlayers": 8,
            "players": ["Ryan", "Leo", ...]
        }
        """
        result = self.collection.insert_one(party_data)
        return str(result.inserted_id)

    def remove_party(self, party_id):
        """
        Remove a party by ID.
        Returns True if deleted, False if not.
        """
        try:
            result = self.collection.delete_one({"_id": ObjectId(party_id)})
            return result.deleted_count > 0
        except:
            return False

    def close_connection(self):
        """Close MongoDB connection"""
        self.client.close()
