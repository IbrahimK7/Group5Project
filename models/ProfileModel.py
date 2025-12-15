from pymongo import MongoClient
from bson import ObjectId
import os
from dotenv import load_dotenv

load_dotenv()


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
