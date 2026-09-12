from flask import Flask, jsonify, request
from flasgger import Swagger

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
