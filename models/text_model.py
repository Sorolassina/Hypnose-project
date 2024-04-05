# models/text_model.py
from pymongo import MongoClient
from bson.objectid import ObjectId

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017")  # Replace the connection string with your MongoDB URI
db = client["your_database_name"]  # Replace "your_database_name" with the name of your MongoDB database
text_collection = db["text_files"]  # Collection for storing text files

class TextFile:
    @staticmethod
    def create(file_name, content):
        document = {
            "file_name": file_name,
            "content": content
        }
        result = text_collection.insert_one(document)
        return result.inserted_id

    @staticmethod
    def read(file_id):
        document = text_collection.find_one({"_id": ObjectId(file_id)})
        return document["file_name"], document["content"] if document else None

    @staticmethod
    def update(file_id, updated_content):
        result = text_collection.update_one({"_id": ObjectId(file_id)}, {"$set": {"content": updated_content}})
        return result.modified_count > 0

    @staticmethod
    def delete(file_id):
        result = text_collection.delete_one({"_id": ObjectId(file_id)})
        return result.deleted_count > 0
