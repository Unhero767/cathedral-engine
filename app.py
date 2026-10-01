from flask import Flask, jsonify, request
from flasgger import Swagger

import json
from engine.core.lex_i_adapter import LexIAdapter
lex_adapter = LexIAdapter()


app = Flask(__name__)
Swagger(app)

# In-memory database stratum for movies
movies_db = [
    {"id": 1, "title": "Blade Runner 2049", "genre": "Sci-Fi", "year": 2017},
    {"id": 2, "title": "Stalker", "genre": "Sci-Fi", "year": 1979}
]

@app.route('/')
def home():
    """API Root Handshake
    ---
    responses:
      200:
        description: Returns API welcome message
    """
    return jsonify({"message": "Movies API"})

@app.route('/movies', methods=['GET'])
def get_movies():
    """Retrieve full movie catalog
    ---
    responses:
      200:
        description: A list of movie records
        examples:
          application/json: [{"id": 1, "title": "Blade Runner 2049", "genre": "Sci-Fi", "year": 2017}]
    """
    return jsonify(movies_db)

@app.route('/movies', methods=['POST'])
def add_movie():
    """Ingest a new film entry
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            title:
              type: string
            genre:
              type: string
            year:
              type: integer
    responses:
      201:
        description: Movie successfully created
    """
    data = request.get_json()
    if not data or 'title' not in data:
        return jsonify({"error": "Invalid payload"}), 400
    
    new_movie = {
        "id": len(movies_db) + 1,
        "title": data.get("title"),
        "genre": data.get("genre", "Unknown"),
        "year": data.get("year", 2026)
    }
    movies_db.append(new_movie)
    return jsonify(new_movie), 201

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False, port=5001)


@app.route("/recipes/<int:recipe_id>", methods=["PUT"])
@token_required
def update_recipe_put(current_user, recipe_id):
    data = request.get_json()
    if not data or not data.get("title") or not data.get("ingredients") or not data.get("instructions"):
        return jsonify({"error": "Missing required fields"}), 400

    db = get_db()
    cursor = db.cursor()

    # 1) Load the recipe by ID only to check existence
    cursor.execute(
        "SELECT id, user_id FROM recipes WHERE id = ?",
        (recipe_id,),
    )
    recipe = cursor.fetchone()

    if not recipe:
        return jsonify({"error": "Recipe not found"}), 404

    # 2) Authorization: owner OR admin
    is_owner = (recipe["user_id"] == current_user["id"])
    is_admin = (current_user.get("role") == "admin")

    if not (is_owner or is_admin):
        return jsonify({"error": "Forbidden"}), 403

    # 3) Execute the update
    cursor.execute(
        "UPDATE recipes SET title = ?, ingredients = ?, instructions = ? WHERE id = ?",
        (data["title"], data["ingredients"], data["instructions"], recipe_id),
    )
    db.commit()

    return jsonify({"message": "Recipe updated successfully"}), 200


@app.route("/recipes/<int:recipe_id>", methods=["DELETE"])
@token_required
def delete_recipe(current_user, recipe_id):
    db = get_db()
    cursor = db.cursor()

    # 1) Load the recipe by ID only to check existence
    cursor.execute(
        "SELECT id, user_id FROM recipes WHERE id = ?",
        (recipe_id,),
    )
    recipe = cursor.fetchone()

    if not recipe:
        return jsonify({"error": "Recipe not found"}), 404

    # 2) Authorization: owner OR admin
    is_owner = (recipe["user_id"] == current_user["id"])
    is_admin = (current_user.get("role") == "admin")

    if not (is_owner or is_admin):
        return jsonify({"error": "Forbidden"}), 403

    # 3) Execute the deletion
    cursor.execute("DELETE FROM recipes WHERE id = ?", (recipe_id,))
    db.commit()

    return "", 204


@app.post("/api/v1/telemetry/ingress")
async def ingress_telemetry(payload: dict):
    """
    Lex I Decoupled Ingress:
      - Continuous volatile logging
      - Threshold-triggered Merkle block inscription
    """
    temp = float(payload.get("afield_temp", 300.0))
    flux = float(payload.get("flux", 0.0))
    chamber = int(payload.get("chamber_id", 1))
    strain = float(payload.get("strain", 0.0))

    result = lex_adapter.record_volatile_telemetry(
        afield_temp=temp,
        flux=flux,
        chamber_id=chamber,
        strain_delta=strain
    )
    return result
