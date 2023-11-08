
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

import os
from dotenv import load_dotenv

# Load the .env file
load_dotenv()

# Access the PASSWORD environment variable
PASSWORD = os.getenv('PASSWORD')


uri = f"mongodb+srv://sbeck7:{PASSWORD}@daviddb.qdeltty.mongodb.net/?retryWrites=true&w=majority"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)