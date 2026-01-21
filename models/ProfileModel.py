from pymongo import MongoClient
from bson import ObjectId
import os
from dotenv import load_dotenv

load_dotenv()


class ProfileModel:
    def __init__(self):
        mongo_uri = os.getenv("MONGO_URI")
        self.client = MongoClient(mongo_uri)
        self.db = self.client['Group5Project']
        self.collection = self.db['Users']

    def _serialize(self, doc):
        if not doc:
            return None
        doc = dict(doc)
        if '_id' in doc:
            doc['_id'] = str(doc['_id'])
        if 'user_id' in doc and isinstance(doc['user_id'], ObjectId):
            doc['user_id'] = str(doc['user_id'])
        # ensure we expose a string form for convenience
        if 'user_id_str' not in doc and 'user_id' in doc:
            doc['user_id_str'] = str(doc.get('user_id'))
        return doc

    # -----------------------
    # Create: insertOne({})
    # -----------------------
    def create_profile(self, profile_data):
        """
        Insert a new profile document. profile_data is a dict.
        If profile_data contains a user_id string that looks like an ObjectId hex,
        store both ObjectId and user_id_str for compatibility.
        """
        doc = dict(profile_data)
        uid = doc.get('user_id')
        if uid is not None:
            # normalize user id storage
            if isinstance(uid, str) and len(uid) == 24 and ObjectId is not None:
                try:
                    doc['user_id'] = ObjectId(uid)
                    doc['user_id_str'] = uid
                except Exception:
                    doc['user_id_str'] = str(uid)
            else:
                doc['user_id_str'] = str(uid)
        result = self.collection.insert_one(doc)
        if result.inserted_id:
            return {"success": True, "profile_id": str(result.inserted_id)}
        return {"success": False, "message": "Failed to insert profile."}

    # -----------------------
    # Read: find / findOne
    # -----------------------
    def get_profile(self, user_id):
        # try as ObjectId first, then fallback to string match
        profile = None
        try:
            profile = self.collection.find_one({"user_id": ObjectId(user_id)})
        except Exception:
            profile = self.collection.find_one({"user_id": user_id})
            if not profile:
                # try matching user_id_str or _id
                profile = self.collection.find_one({"user_id_str": str(user_id)}) or self.collection.find_one(
                    {"_id": ObjectId(user_id)}) if ObjectId and isinstance(user_id, str) and len(user_id) == 24 else profile
        if profile:
            return {"success": True, "profile": self._serialize(profile)}
        else:
            return {"success": False, "message": "Profile not found."}

    def list_profiles(self, filter=None, limit=0):
        """
        Return list of profiles. filter is an optional dict.
        If filter contains a user_id as a 24-char hex string, try converting it for query.
        """
        q = dict(filter or {})
        if 'user_id' in q and isinstance(q['user_id'], str) and len(q['user_id']) == 24 and ObjectId is not None:
            try:
                q['user_id'] = ObjectId(q['user_id'])
            except Exception:
                pass
        cursor = self.collection.find(q)
        if isinstance(limit, int) and limit > 0:
            cursor = cursor.limit(limit)
        docs = [self._serialize(d) for d in cursor]
        return {"success": True, "profiles": docs}

    # -----------------------
    # Update: updateOne({})
    # -----------------------
    def update_profile(self, user_id, profile_data):
        

        result = self.collection.update_one(
            {"user_id": user_id},
            {"$set": profile_data}
        )
        
        if result.matched_count > 0:
            return {"success": True}
        return {"success": False, "message": "Profile not found."}

        

        
    
    


class Rank:
    def __init__(self, rank_name, permissions):
        self.rank_name = rank_name
        self.permissions = permissions


class Rating:
    def __init__(self, score, reviews):
        self.score = score
        self.reviews = reviews


class GamesOwned:
    def __init__(self, game_list):
        self.game_list = game_list
