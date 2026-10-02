import sqlite3, hashlib, json

conn = sqlite3.connect("ash_archive.db")
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

cursor.execute("SELECT rowid, id, timestamp, node_type, state_payload FROM ash_ledger ORDER BY rowid ASC;")
rows = cursor.fetchall()

prev_hash = "0" * 64
for row in rows:
    rowid = row["id"]
    record_data = {
        "node_id": row["id"],
        "timestamp": row["timestamp"],
        "node_type": row["node_type"],
        "state_payload": row["state_payload"]
    }
    
    payload = f"{rowid}:{prev_hash}:{json.dumps(record_data, sort_keys=True, default=str)}"
    computed_hash = hashlib.sha256(payload.encode("utf-8")).hexdigest()
    
    cursor.execute(
        "UPDATE ash_ledger SET parent_hash = ?, current_hash = ? WHERE id = ?;",
        (prev_hash, computed_hash, rowid)
    )
    prev_hash = computed_hash

conn.commit()
conn.close()
print("Ash ledger successfully restitched.")
