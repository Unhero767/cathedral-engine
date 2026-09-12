from pymongo import MongoClient

# 1. Connect to your Atlas cluster
client = MongoClient("your-connection-string-here")
db = client["movies_db"]
movies = db["movies"]

# Update: change the year field
result = movies.update_one(
    {"title": "Interstellar"},
    {"$set": {"year": 2015}}
)
print(f"Matched: {result.matched_count}, Modified: {result.modified_count}")

# Verify the change
doc = movies.find_one({"title": "Interstellar"})
print(doc["year"])

