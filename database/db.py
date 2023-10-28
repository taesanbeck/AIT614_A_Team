# db.py
import pymongo
from osgeo import gdal
import io
import os
from PIL import Image


class David_db:
    def __init__(self):
        self.client = pymongo.MongoClient("mongodb+srv://sbeck7:dr7STMRpAltywfwz@cluster0.whcpnp8.mongodb.net/?retryWrites=true&w=majority")
        self.db = self.client["daviddb"]
        self.col = self.db["metadata"]



    def insert_metadata(self, meta_data, raw_results, image_data):
        try:
            image_input = Image.open(io.BytesIO(image_data))
            predictions = self.extract_prediction_data(raw_results, image_input)
            doc = {
                "meta_data": meta_data,
                "predictions": predictions
            }
            self.col.insert_one(doc)
        except Exception as e:
            raise ValueError(f"Error inserting metadata to the database: {str(e)}")

    def close_connection(self):
        self.client.close()
