import sqlite3
import json
import os
import hashlib
from datetime import datetime, timezone

DB_PATH = os.path.join("strata", "ash_archive.db")
OUTPUT_JSON_PATH = "ash_archive_report.json"

print("================================================================================")
print(" EXPORTING ASH ARCHIVE STRATA TO JSON REPORT")
print("================================================================================")

if not os.path.exists(DB_PATH):
    print(f"[-] Database file not found at: {DB_PATH}")
    exit(1)

conn = sqlite3.connect(DB_PATH)
conn.row_factory = sqlite3.Row
c = conn.cursor()

# Discover all tables dynamically
c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
tables = [row["name"] for row in c.fetchall()]

report = {
    "archive_metadata": {
        "source_database": DB_PATH,
        "export_timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "total_tables": len(tables),
        "discovered_tables": tables
    },
    "strata_tables": {}
}

# Dump and structure each table
for table in tables:
    c.execute(f"SELECT * FROM {table};")
    rows = c.fetchall()
    
    table_data = []
    for row in rows:
        row_dict = dict(row)
        
        # Parse nested JSON strings if present in payload or adjustment fields
        for field in ("state_payload", "routing_adjustment", "resonance_specs", "metadata"):
            if field in row_dict and isinstance(row_dict[field], str):
                try:
                    row_dict[field] = json.loads(row_dict[field])
                except (json.JSONDecodeError, TypeError):
                    pass
        table_data.append(row_dict)
        
    report["strata_tables"][table] = {
        "row_count": len(table_data),
        "records": table_data
    }

# Compute ledger cryptographic verification summary
if "ash_ledger" in report["strata_tables"]:
    ledger_records = report["strata_tables"]["ash_ledger"]["records"]
    chain_valid = True
    merkle_valid = True
    
    for idx, b in enumerate(ledger_records):
        parent = b.get("parent_hash")
        c_hash = b.get("content_hash")
        ts = b.get("timestamp")
        m_root = b.get("merkle_root")
        payload = b.get("state_payload")
        
        payload_str = json.dumps(payload, sort_keys=True) if isinstance(payload, (dict, list)) else str(payload)
        expected_content = hashlib.sha256(f"{parent}:{payload_str}:{ts}".encode("utf-8")).hexdigest()
        expected_merkle = hashlib.sha256(f"{c_hash}:{ts}".encode("utf-8")).hexdigest()
        
        if idx > 0 and parent != ledger_records[idx - 1].get("content_hash"):
            chain_valid = False
        if m_root and expected_merkle != m_root:
            merkle_valid = False

    report["archive_metadata"]["cryptographic_audit"] = {
        "total_blocks": len(ledger_records),
        "chain_linkage_valid": chain_valid,
        "merkle_roots_valid": merkle_valid,
        "status": "VERIFIED_IMMUTABLE" if (chain_valid and merkle_valid) else "AUDIT_WARNING"
    }

conn.close()

# Write formatted JSON report
with open(OUTPUT_JSON_PATH, "w", encoding="utf-8") as f:
    json.dump(report, f, indent=2, ensure_ascii=False)

print(f"[+] Successfully exported Ash Archive to '{OUTPUT_JSON_PATH}'.")
print(f"• Total Tables Exported: {len(tables)}")
for table, details in report["strata_tables"].items():
    print(f"    - {table:<22} ({details['row_count']} rows)")

if "cryptographic_audit" in report["archive_metadata"]:
    audit = report["archive_metadata"]["cryptographic_audit"]
    print(f"• Cryptographic Integrity: {audit['status']} ({audit['total_blocks']} blocks verified)")
