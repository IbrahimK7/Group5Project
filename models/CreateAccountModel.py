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
