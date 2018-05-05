from pymongo import MongoClient

client = MongoClient('mongo', 27017)
db = client['url_shorter']

mapping = db['mapping']
counter = db['counter']
