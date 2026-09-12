import certifi
from pymongo import MongoClient

# 1. Connect to your Atlas cluster
client = MongoClient(
    "mongodb+srv://kennethdallmier_db_user:zBUTZnte0X1aqDaM@cluster0.13qd2x0.mongodb.net/?retryWrites=true&w=majority",
    tlsCAFile=certifi.where()
)

db = client["movies_db"]
movies = db["movies"]

# 2. Find by title using a Python dict filter
result = movies.find({"title": "Interstellar"})

for doc in result:
    print(doc)
# Update: change the year field
result = movies.update_one(
    {"title": "Interstellar"},
    {"$set": {"year": 2015}}
)
print(f"Matched: {result.matched_count}, Modified: {result.modified_count}")

# Verify the change with find_one
doc = movies.find_one({"title": "Interstellar"})
print(doc["year"])# Update: change the year field
result = movies.update_one(
    {"title": "Interstellar"},
    {"$set": {"year": 2015}}
)
print(f"Matched: {result.matched_count}, Modified: {result.modified_count}")

# Verify the change with find_one
doc = movies.find_one({"title": "Interstellar"})
print(doc["year"])
# Delete the document
result = movies.delete_one({"title": "Interstellar"})
print(f"Deleted: {result.deleted_count}")

# Verify it's gone
doc = movies.find_one({"title": "Interstellar"})
print(doc)
