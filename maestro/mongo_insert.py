import certifi
from pymongo import MongoClient

# Connect using certifi for SSL verification
client = MongoClient(
    "mongodb+srv://kennethdallmier_db_user:zBUTZnte0X1aqDaM@cluster0.13qd2x0.mongodb.net/?retryWrites=true&w=majority",
    tlsCAFile=certifi.where(),
)

db = client["movies_db"]
movies = db["movies"]

interstellar_doc = {
    "title": "Interstellar",
    "year": 2014,
    "genres": ["Sci-Fi", "Drama", "Adventure"],
    "director": {
        "name": "Christopher Nolan",
        "birth_year": 1970,
        "nationality": "British-American",
    },
    "cast": [
        {"actor": "Matthew McConaughey", "role": "Cooper"},
        {"actor": "Anne Hathaway", "role": "Brand"},
        {"actor": "Jessica Chastain", "role": "Murph"},
    ],
    "ratings": {"imdb": 8.7, "rotten_tomatoes": "73%", "metacritic": 74},
}

result = movies.insert_one(interstellar_doc)
print("Inserted document _id:", result.inserted_id)
