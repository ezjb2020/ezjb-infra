from pymongo import MongoClient
# pprint library is used to make the output look more pretty
from pprint import pprint
import pprint
from dotenv import load_dotenv
load_dotenv()

import os


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
pprint.pprint(posts.find_one())
