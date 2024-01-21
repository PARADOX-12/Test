import os
from pymongo import MongoClient

db = MongoClient(os.getenv("MONGO_URI"),
                 authSource='admin',
                 maxPoolSize=50,
                 wtimeoutMS=2500)["QR_Scanner"]