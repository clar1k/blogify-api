from pymongo import MongoClient
from config.config import Config

conn = MongoClient(Config.MONGO_CONNECTION)
db = conn["blogify"]
