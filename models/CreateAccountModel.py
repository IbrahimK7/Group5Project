from pymongo import MongoClient
from bson import ObjectId
import os
from dotenv import load_dotenv

load_dotenv()


class CreateAccountModel:
    def __init__(self):
        mongo_uri = os.getenv("MONGO_URI")
        self.client = MongoClient(mongo_uri)
        self.db = self.client['user_database']
        self.collection = self.db['users']

    def create_account(self, username, email, password):
        if self.collection.find_one({"email": email}):
            return {"success": False, "message": "Email already exists."}

        user_data = {
            "username": username,
            "email": email,
            "password": password  # In a real application, ensure to hash the password
        }

        result = self.collection.insert_one(user_data)
        if result.inserted_id:
            return {"success": True, "message": "Account created successfully.", "user_id": str(result.inserted_id)}
        else:
            return {"success": False, "message": "Failed to create account."}

    # -----------------------
    # Read: find / find_one
    # -----------------------
    def get_account_by_email(self, email):
        """Return account document by email (as dict)"""
        doc = self.collection.find_one({"email": email})
        if not doc:
            return {"success": False, "message": "Not found."}
        doc["user_id"] = str(doc.get("_id"))
        return {"success": True, "account": doc}

    def get_account_by_id(self, user_id):
        """Return account document by _id (accepts string or ObjectId)"""
        try:
            oid = ObjectId(user_id) if not isinstance(
                user_id, ObjectId) else user_id
        except Exception:
            return {"success": False, "message": "Invalid id format."}
        doc = self.collection.find_one({"_id": oid})
        if not doc:
            return {"success": False, "message": "Not found."}
        doc["user_id"] = str(doc.get("_id"))
        return {"success": True, "account": doc}

    def list_accounts(self, filter=None, limit=0):
        """Return list of accounts matching filter"""
        filter = filter or {}
        cursor = self.collection.find(filter)
        if limit and isinstance(limit, int) and limit > 0:
            cursor = cursor.limit(limit)
        docs = []
        for d in cursor:
            d["user_id"] = str(d.get("_id"))
            docs.append(d)
        return {"success": True, "accounts": docs}

    # -----------------------
    # Update: updateOne
    # -----------------------
    def update_account(self, user_id, update_fields):
        """
        Partial update using $set.
        update_fields should be a dict of fields to change.
        """
        try:
            oid = ObjectId(user_id) if not isinstance(
                user_id, ObjectId) else user_id
        except Exception:
            return {"success": False, "message": "Invalid id format."}
        if not isinstance(update_fields, dict) or not update_fields:
            return {"success": False, "message": "Nothing to update."}
        res = self.collection.update_one({"_id": oid}, {"$set": update_fields})
        return {"success": True, "matched": res.matched_count, "modified": res.modified_count}

    # -----------------------
    # Delete: deleteOne
    # -----------------------
    def delete_account(self, user_id):
        try:
            oid = ObjectId(user_id) if not isinstance(
                user_id, ObjectId) else user_id
        except Exception:
            return {"success": False, "message": "Invalid id format."}
        res = self.collection.delete_one({"_id": oid})
        if res.deleted_count == 1:
            return {"success": True, "deleted": 1}
        return {"success": False, "deleted": 0, "message": "No document deleted."}
