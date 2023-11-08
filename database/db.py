# db.py
import pymongo
from pymongo import MongoClient
import pandas as pd
from datetime import datetime
from geopy.distance import geodesic
from dotenv import load_dotenv
import os
import time

# Load the .env file
load_dotenv()

class David_db:
    def __init__(self):
        password = os.getenv('PASSWORD')
        uri = f"mongodb+srv://sbeck7:{password}@daviddb.nnjdfya.mongodb.net/?retryWrites=true&w=majority"
        self.client = MongoClient(uri)
        self.davidDB = self.client["davidDB"]
        self.collection = self.davidDB['daviddb']
        self.collection.create_index([("location", pymongo.GEOSPHERE)])
        try:
            self.client.admin.command('ping')
        except Exception as e:
            raise ConnectionError(f"Failed to connect to MongoDB: {e}")

    def insert_dataframe(self, df):
        # Insert dataframe into the collection
        try:
            data_dict = df.to_dict("records")
            self.collection.insert_many(data_dict)
        except Exception as e:
            raise Exception(f"Failed to insert DataFrame: {e}")

    def fetch_all_data(self):
        # Fetch all data from the collection
        try:
            docs = self.collection.find({})
            return list(docs)
        except Exception as e:
            raise ValueError(f"Error fetching data from the database: {str(e)}")

    def is_within_tolerance(self, entry_lat, entry_lon, centroid_lat, centroid_lon, tolerance):
        distance = geodesic((entry_lat, entry_lon), (centroid_lat, centroid_lon)).meters
        print(f"Distance: {distance}, Tolerance: {tolerance}")
        return distance <= tolerance


    def fetch_nearby_entries(self, class_name, centroid_lon, centroid_lat, tolerance):
        # Convert tolerance to meters for the $maxDistance parameter
        query = {
            'class_name': class_name,
            "location": {
                "$nearSphere": {
                    "$geometry": {
                        "type": "Point",
                        "coordinates": [centroid_lon, centroid_lat]
                    },
                    "$maxDistance": tolerance
                }
            }
        }
        return list(self.collection.find(query))

    def check_and_insert_data(self, selected_df):
        inserted_count = 0
        duplicate_count = 0

        # Reset the index to ensure that each row has a unique identifier
        selected_df = selected_df.reset_index(drop=True)

        # Add 'location' field
        selected_df['location'] = selected_df.apply(
            lambda row: {"type": "Point", "coordinates": [float(row['centroid_longitude']), float(row['centroid_latitude'])]},
            axis=1
        )

        # Convert the dataframe to a list of dictionaries for easier processing
        records = selected_df.to_dict(orient='records')

        for record in records:
            class_name = record['class_name']
            centroid = record['location']['coordinates']
            tolerance = 5.0  # Meters tolerance for duplicate checking

            # Fetch nearby entries from the database that could be potential duplicates
            potential_duplicates = self.fetch_nearby_entries(class_name, centroid[0], centroid[1], tolerance)

            # Check if the current record is a duplicate based on class and location
            is_duplicate = any(
                self.is_within_tolerance(
                    potential_duplicate['location']['coordinates'][1],
                    potential_duplicate['location']['coordinates'][0],
                    centroid[1],
                    centroid[0],
                    tolerance
                ) for potential_duplicate in potential_duplicates if potential_duplicate['class_name'] == class_name
            )

            if is_duplicate:
                duplicate_count += 1
            else:
                # Prepare the record for insertion, ensure '_id' is not copied over to avoid conflicts
                data_to_insert = {k: v for k, v in record.items() if k != '_id'}
                # Insert the new record into the database
                self.collection.insert_one(data_to_insert)
                inserted_count += 1

        print(f"Insertion complete. {inserted_count} new entries added, {duplicate_count} duplicates skipped.")
        return inserted_count, duplicate_count





    def close_connection(self):
        self.client.close()

# Instantiate the David_db class right here and assign it to a variable (e.g., david_db_instance)
db_instance = David_db()
