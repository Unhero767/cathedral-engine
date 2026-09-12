from pymongo import MongoClient

# 1. Connect to your Atlas cluster
client = MongoClient("your-connection-string-here")
db = client["movies_db"]
movies = db["movies"]

# 2. Update: change the year field
result = movies.update_one(
    {"title": "Interstellar"},
    {"$set": {"year": 2015}}
)
print(f"Matched: {result.matched_count}, Modified: {result.modified_count}")

# 3. Verify the change with find_one
doc = movies.find_one({"title": "Interstellar"})
print(f"Updated Year: {doc['year']}")

# 4. Delete: remove the document to finish the CRUD cycle
delete_result = movies.delete_one({"title": "Interstellar"})
print(f"Deleted count: {delete_result.deleted_count}")

