from pymongo import MongoClient
from bson import ObjectId
import os
from dotenv import load_dotenv

load_dotenv()

class LoginModel:
    def __init__(self):
        mongodb_uri = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/')
        database_name = os.getenv('DATABASE_NAME', 'users_db')
        
        self.client = MongoClient(mongodb_uri)
        self.db = self.client[database_name]
        self.collection = self.db['users']
    
    def create_user(self, user_data):
        """Create a new user"""
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

    def close_connection(self):
        """Close MongoDB connection"""
        self.client.close()

    def authenticate(self, email, password):
        user = self.collection.find_one({
            "email": email,
            "password": password
        })
        if user:
            user["_id"] = str(user["_id"])
        return user

