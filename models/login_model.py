import certifi
from pymongo import MongoClient
from bson import ObjectId
import os
from dotenv import load_dotenv
import bcrypt

load_dotenv()


class LoginModel:
    def __init__(self):
        uri = os.getenv("MONGO_URI")
        if not uri:
            raise RuntimeError("MONGO_URI missing")

        self.client = MongoClient(
            uri,
            tls=True,
            tlsCAFile=certifi.where(),
            serverSelectionTimeoutMS=5000
        )

        self.db = self.client["Group5Project"]
        self.collection = self.db["Users"]

    def create_user(self, user_data):
        """Create a new user with hashed password"""
        # Hash the password before storing
        if 'password' in user_data:
            password = user_data['password']
            hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            user_data['password'] = hashed

        result = self.collection.insert_one(user_data)
        return str(result.inserted_id)

    def get_user_by_id(self, user_id):
        """Get a user by ID"""
        try:
            user = self.collection.find_one({'_id': ObjectId(user_id)})
            if user:
                user['_id'] = str(user['_id'])
            return user
        except:
            return None

    def update_user(self, user_id, user_data):
        """Update a user by ID"""
        try:
            user_data.pop('_id', None)
            result = self.collection.update_one(
                {'_id': ObjectId(user_id)},
                {'$set': user_data}
            )
            return result.modified_count > 0
        except:
            return False

    def delete_user(self, user_id):
        """Delete a user by ID"""
        try:
            result = self.collection.delete_one({'_id': ObjectId(user_id)})
            return result.deleted_count > 0
        except:
            return False

    def authenticate(self, email, password):
        """Authenticate user with email and password using bcrypt"""
        user = self.collection.find_one({"email": email})

        if not user:
            return None

        # Check if password matches using bcrypt
        stored_password = user.get('password')
        if stored_password and bcrypt.checkpw(password.encode('utf-8'), stored_password):
            user["_id"] = str(user["_id"])
            return user

        return None

    def get_user_summary(self, user_id):
        """Return selected user fields: _id, username, gamertag, email, rating, favourite_game, last_played_games"""
        try:
            proj = {
                "username": 1,
                "gamertag": 1,
                "email": 1,
                "rating": 1,
                "favourite_game": 1,
                "last_played_games": 1
            }
            user = self.collection.find_one({'_id': ObjectId(user_id)}, proj)
            if user:
                user['_id'] = str(user['_id'])
            return user
        except:
            return None

    def get_last_played_games(self, user_id):
        """Return the last_played_games array for a user (empty list if not present)"""
        try:
            doc = self.collection.find_one({'_id': ObjectId(user_id)}, {
                                           'last_played_games': 1})
            if doc and 'last_played_games' in doc:
                return doc['last_played_games']
            return []
        except:
            return []

    def get_field(self, user_id, field_name):
        """Return a single field value for a user (or None if missing)"""
        try:
            doc = self.collection.find_one(
                {'_id': ObjectId(user_id)}, {field_name: 1})
            if doc and field_name in doc:
                return doc[field_name]
            return None
        except:
            return None

    def get_user_by_email(self, email, include_password=False):
        """Get user by email. By default excludes password unless include_password=True"""
        try:
            proj = {"password": 0} if not include_password else None
            user = self.collection.find_one({"email": email}, proj)
            if user:
                user["_id"] = str(user["_id"])
            return user
        except:
            return None

    def close_connection(self):
        """Close MongoDB connection"""
        self.client.close()
