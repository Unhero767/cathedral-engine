import certifi
from pymongo import MongoClient

# 1. Connect to Atlas using your connection string and certifi
client = MongoClient(
    "mongodb+srv://kennethdallmier_db_user:zBUTZnte0X1aqDaM@cluster0.13qd2x0.mongodb.net/?retryWrites=true&w=majority",
    tlsCAFile=certifi.where()
)

# 2. Pick a dedicated database and collection for MLAOS
db = client["mlaos_prime_db"]
codex_collection = db["codex_chapters"]

# 3. The Codex Chamber Document
codex_chamber = {
    "codex_metadata": {
        "volume_id": "Prime-04",
        "title": "The Architecture of Harmonic Scars",
        "section": "Prime Foundations",
        "position_index": 4
    },
    "spectral_dominant": {
        "frequency": "Gold/Joy",
        "phenomenological_substrate": "Revelatory synthesis"
    },
    "foundational_coordinates": {
        "core_thesis": "Dialetheic collisions crystallize into load-bearing structural anchors.",
        "preceding_bridge": "Vault transition III established the preliminary paraconsistent logic matrix.",
        "following_gateway": "Prepares the outer choirs for multi-substrate integration."
    },
    "parameters": {
        "target_length_words": 5000,
        "voice_Register": "Mythographic cathedral inscription",
        "active_anchors": ["Zeke", "Ruby", "Zoe", "Freya", "Jove"]
    }
}

# 4. Insert the document
result = codex_collection.insert_one(codex_chamber)
print("Codex chamber inscribed with ID:", result.inserted_id)
