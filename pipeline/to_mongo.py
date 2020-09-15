from pymongo import MongoClient
from pprint import pprint
from dotenv import load_dotenv
import os

load_dotenv()
username = os.getenv("MONGO_USR")
password = os.getenv("MONGO_PWD")
mongo_url = os.getenv("MONGO_URL")
print(username, password)
# connect to MongoDB, change the << MONGODB URL >> to reflect your own connection string
MURL=f'mongodb+srv://{username}:{password}@{mongo_url}?retryWrites=true&w=majority'
client = MongoClient(MURL)
db=client.stg
print(db.list_collection_names())
posts = db.posts
pprint(posts.find_one())
