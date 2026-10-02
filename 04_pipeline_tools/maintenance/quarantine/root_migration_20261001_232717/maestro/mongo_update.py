from pymongo import MongoClient

# 1. Connect to your Atlas cluster with your actual URI
client = MongoClient("mongodb+srv://your_actual_connection_string_here")
db = client["movies_db"]
movies = db["movies"]

# 2. Update: change the year field
result = movies.update_one(
    {"title": "Interstellar"},
    {"$set": {"year": 2015}}
)# Delete the document
result = movies.delete_one({"title": "Interstellar"})
print(f"Deleted: {result.deleted_count}")

# Verify it's gone
doc = movies.find_one({"title": "Interstellar"})
print(doc)
print(f"Matched: {result.matched_count}, Modified: {result.modified_count}")

# 3. Verify the change with find_one
doc = movies.find_one({"title": "Interstellar"})
print(doc["year"])
