import certifi
from pymongo import MongoClient
from bson import ObjectId
import os
from dotenv import load_dotenv

load_dotenv()


class PartyModel:
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
        self.parties = self.db["Parties"]
        self.collection = self.parties  

    # -------------------- HELPERS --------------------
    def _to_object_id(self, party_id):
        try:
            return ObjectId(party_id)
        except Exception:
            return None

    # -------------------- READ --------------------
    def get_all_parties(self):
        parties = list(self.parties.find())
        for p in parties:
            p["_id"] = str(p["_id"])
        return parties

    # -------------------- CREATE --------------------
    def add_party(self, party_data):
        result = self.parties.insert_one(party_data)
        return str(result.inserted_id)

    # -------------------- DELETE --------------------
    def remove_party(self, party_id):
        oid = self._to_object_id(party_id)
        if oid is None:
            return False

        result = self.parties.delete_one({"_id": oid})
        return result.deleted_count > 0

    # -------------------- CLEANUP --------------------
    def close(self):
        self.client.close()
