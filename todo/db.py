from pymongo import MongoClient
from django.conf import settings

# Connect to MongoDB
client = MongoClient(settings.MONGODB_URI)
db = client[settings.MONGODB_DB_NAME]
col = db['todo']