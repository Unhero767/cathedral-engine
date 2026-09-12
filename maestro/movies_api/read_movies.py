import sqlite3

# Open connection to movies.db
conn = sqlite3.connect("movies.db")

# Create a cursor object
cursor = conn.cursor()

# Execute SELECT query
cursor.execute("SELECT * FROM movies")

# Iterate through the cursor and print each row
for row in cursor:
    print(row)

# Clean up connection
conn.close()
