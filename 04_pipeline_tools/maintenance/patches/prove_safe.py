import sqlite3

# Connect to the database
conn = sqlite3.connect("movies.db")
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

# The injection payload we want to test
payload = "' OR '1'='1"

print(f"Testing parameterized search with malicious payload: {payload}\n")

# Use the secure parameterized query structure (? placeholder + parameter tuple)
cursor.execute(
    "SELECT * FROM movies WHERE title = ?", 
    (payload,)
)

rows = cursor.fetchall()

print(f"Total rows returned: {len(rows)}")
for row in rows:
    print(dict(row))

conn.close()
