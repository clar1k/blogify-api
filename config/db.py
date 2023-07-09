from os import environ as env
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv('.env')
conn = MongoClient(env.get('MONGO_CONNECTION'))
db = conn['blogify']