import sqlite3

conn = sqlite3.connect("movies.db")
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

# Enable Foreign Key enforcement
cursor.execute("PRAGMA foreign_keys = ON;")

# 1. Drop existing table to ensure idempotent/clean execution
cursor.execute("DROP TABLE IF EXISTS ratings;")

# 2. Create table schema
cursor.execute("""
CREATE TABLE ratings (
    id INTEGER PRIMARY KEY,
    movie_id INTEGER NOT NULL,
    score INTEGER NOT NULL,
    FOREIGN KEY (movie_id) REFERENCES movies(id)
);
""")

# 3. Seed rating records
cursor.executemany("""
INSERT INTO ratings (movie_id, score) VALUES (?, ?);
""", [
    (1, 9),
    (2, 10),
    (3, 8)
])

conn.commit()

# 4. Perform INNER JOIN query
cursor.execute("""
SELECT movies.title, ratings.score
FROM movies
INNER JOIN ratings ON movies.id = ratings.movie_id;
""")

# 5. Output clean dict results
for row in cursor:
    print(dict(row))

conn.close()
