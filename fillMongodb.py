import json
from pymongo import MongoClient

MONGO_URI = "mongodb://localhost:27017"
DB_NAME = "WEB"
COLLECTION_NAME = "BonsPlans"
JSON_FILE = "events.json"

# --- Connexion MongoDB ---
client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

with open(JSON_FILE, 'r', encoding='utf-8') as f:
    data = json.load(f)

collection.delete_many({}) 
collection.insert_many(data)

print(f"{len(data) if isinstance(data, list) else 1} document(s) inséré(s) dans {COLLECTION_NAME}.")
