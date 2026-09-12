import sqlite3

# Connect to the database
conn = sqlite3.connect("movies.db")
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

print("--- 1. INSERT OPERATION ---")
# Insert a new movie using ? placeholders
cursor.execute(
    "INSERT INTO movies (title, year, director, watched) VALUES (?, ?, ?, ?)",
    ("Interstellar", 2014, "Christopher Nolan", 0)
)
conn.commit()

# Verify insertion
cursor.execute("SELECT * FROM movies WHERE title = ?", ("Interstellar",))
print(dict(cursor.fetchone()))

print("\n--- 2. UPDATE OPERATION ---")
# Update the movie's watched column to 1 using ? placeholders
cursor.execute(
    "UPDATE movies SET watched = ? WHERE title = ?",
    (1, "Interstellar")
)
conn.commit()

# Verify update
cursor.execute("SELECT title, watched FROM movies WHERE title = ?", ("Interstellar",))
print(dict(cursor.fetchone()))

print("\n--- 3. DELETE OPERATION ---")
# Delete that movie using ? placeholders
cursor.execute(
    "DELETE FROM movies WHERE title = ?",
    ("Interstellar",)
)
conn.commit()

# Verify deletion
cursor.execute("SELECT * FROM movies WHERE title = ?", ("Interstellar",))
row = cursor.fetchone()
print("Record found after delete:", row)

conn.close()
