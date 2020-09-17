from pymongo import MongoClient
from pprint import pprint
from dotenv import load_dotenv
import os

load_dotenv()

class EzDb():
    def __init__(self):
        username = os.getenv("MONGO_USR")
        password = os.getenv("MONGO_PWD")
        mongo_url = os.getenv("MONGO_URL")
        print(username, password)
        # connect to MongoDB, change the << MONGODB URL >> to reflect your own connection string
        MURL=f'mongodb+srv://{username}:{password}@{mongo_url}?retryWrites=true&w=majority'
        client = MongoClient(MURL)
        self.db=client.stg
        self.posts = self.db.posts
        print(self.db.list_collection_names())

    def db(self):
        return self.db
    def post(self):
        self.posts = self.db.posts
        pprint(self.posts.find_one())

    def create_post(self, post):
        self.posts = self.db.posts
        self.posts.insert_one(post)

    def get_sources(self):
        s = []
        cursor = self.db.posts.find({}, {'source':1, '_id':0})
        for document in cursor:
            for k in document:
                s.append(document[k])
        return s

if __name__ == "__main__":
    print(EzDb().get_sources())

# EzDB().posts()
