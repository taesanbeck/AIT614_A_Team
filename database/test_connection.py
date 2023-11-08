from pymongo import MongoClient
import os
from dotenv import load_dotenv

# Load the .env file
load_dotenv()

# Access the PASSWORD environment variable
PASSWORD = os.getenv('PASSWORD')
try:
    # my connection to db and collections
    client = MongoClient(f"mongodb+srv://sbeck7:{PASSWORD}@davidDB.qdeltty.mongodb.net/?retryWrites=true&w=majority")
    db = client.test
    print("Connected to MongoDB")
    collection = db['daviddb']
    
    # Create a dictionary to be inserted as a document
    doc1 = {"name": "John Doe",
            "email": "johndoe@example.com"}
    doc2 = {"name": "Sid Doe",
            "email":"siddoe@example.com"}
    docs = [doc1,doc2]

    # Insert the document into daviddb collection
    collection.insert_many(docs)
    print("Document inserted")

except Exception as e:
    print(f"An error occurred: {e}")




