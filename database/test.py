from pymongo import MongoClient
import os
from dotenv import load_dotenv

# Load the .env file
load_dotenv()

# Access the PASSWORD environment variable
PASSWORD = os.getenv('PASSWORD')

cluster = f"mongodb+srv://sbeck7:{PASSWORD}@daviddb.qdeltty.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(cluster)
print(client.list_database_names())

db = client.test

print(db.list_collection_names())
