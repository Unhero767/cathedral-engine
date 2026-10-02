import sqlite3

# 1. Connect to the database
conn = sqlite3.connect("movies.db")

# 2. Create table
conn.execute("""
CREATE TABLE IF NOT EXISTS movies (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    director TEXT NOT NULL,
    year INTEGER NOT NULL,
    watched INTEGER NOT NULL DEFAULT 0
)
""")

# 3. Insert rows
conn.execute("INSERT INTO movies (title, director, year, watched) VALUES ('Inception', 'Christopher Nolan', 2010, 1)")
conn.execute("INSERT INTO movies (title, director, year, watched) VALUES ('The Matrix', 'Lana Wachowski, Lilly Wachowski', 1999, 1)")
conn.execute("INSERT INTO movies (title, director, year, watched) VALUES ('Interstellar', 'Christopher Nolan', 2014, 0)")
conn.execute("INSERT INTO movies (title, director, year, watched) VALUES ('The Grand Budapest Hotel', 'Wes Anderson', 2014, 0)")
conn.execute("INSERT INTO movies (title, director, year, watched) VALUES ('Parasite', 'Bong Joon-ho', 2019, 1)")

# 4. CRITICAL: Save changes to disk!
conn.commit()

# 5. Close connection
conn.close()

print("Seeded successfully!")
