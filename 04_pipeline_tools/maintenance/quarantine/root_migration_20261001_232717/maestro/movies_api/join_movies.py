import sqlite3

# 1. Connect and configure row factory
conn = sqlite3.connect("movies.db")
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

# 2. Enable Foreign Key constraints
cursor.execute("PRAGMA foreign_keys = ON;")

# 3. Create the ratings table
cursor.execute("""
CREATE TABLE IF NOT EXISTS ratings (
    id INTEGER PRIMARY KEY,
    movie_id INTEGER NOT NULL,
    score INTEGER NOT NULL,
    FOREIGN KEY (movie_id) REFERENCES movies(id)
);
""")

# 4. Seed sample ratings data
cursor.executemany("""
INSERT INTO ratings (movie_id, score) VALUES (?, ?);
""", [
    (1, 9),  # Inception
    (2, 10), # The Matrix
    (3, 8)   # Interstellar
])

conn.commit()

# 5. Execute INNER JOIN query
cursor.execute("""
SELECT movies.title, ratings.score
FROM movies
INNER JOIN ratings ON movies.id = ratings.movie_id;
""")

# 6. Output dict results for JSON readiness
for row in cursor:
    print(dict(row))

conn.close()
