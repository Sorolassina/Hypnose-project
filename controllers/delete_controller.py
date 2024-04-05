from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017")  # Replace the connection string with your MongoDB URI
db = client["your_database_name"]  # Replace "your_database_name" with the name of your MongoDB database
pdf_collection = db["pdf_files"]  # Collection for storing PDF files
text_collection = db["text_files"]  # Collection for storing text files
csv_collection = db["csv_files"]  # Collection for storing CSV files

def delete_file(file_id, file_type):
    # Determine collection based on file type
    collection = None
    if file_type == "pdf":
        collection = pdf_collection
    elif file_type == "text":
        collection = text_collection
    elif file_type == "csv":
        collection = csv_collection

    if collection:
        # Delete file from MongoDB
        result = collection.delete_one({"_id": file_id})
        return result.deleted_count > 0
    else:
        return False
