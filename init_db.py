import sqlite3

conn = sqlite3.connect("ash_archive.db", isolation_level=None)
conn.execute("PRAGMA journal_mode=WAL;")
conn.execute("PRAGMA synchronous=NORMAL;")
print("[ASH ARCHIVE] SQLite WAL mode initialized successfully.")
