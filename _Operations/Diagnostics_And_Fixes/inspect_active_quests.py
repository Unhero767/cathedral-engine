import server
import json
import sqlite3
import os

gl = getattr(server, "GAME_LOOP", None)

print("==================================================")
print(" 1. IN-MEMORY GAME_LOOP QUEST LEDGER")
print("==================================================")

if gl and hasattr(gl, "active_quests"):
    quests = gl.active_quests
    print(f"Total Tracked Quests: {len(quests)}\n")
    for q in quests:
        if isinstance(q, dict):
            qid = q.get("quest_id", q.get("id", "UNKNOWN"))
            title = q.get("title", q.get("name", "Untitled Objective"))
            stage = q.get("current_stage", q.get("stage", 1))
            max_stg = q.get("max_stages", q.get("total_stages", 1))
            completed = q.get("is_completed", q.get("completed", False))
            desc = q.get("description", q.get("objective", ""))
            chamber = q.get("chamber_id", q.get("chamber", "All"))
        else:
            qid = getattr(q, "quest_id", getattr(q, "id", "UNKNOWN"))
            title = getattr(q, "title", getattr(q, "name", "Untitled Objective"))
            stage = getattr(q, "current_stage", getattr(q, "stage", 1))
            max_stg = getattr(q, "max_stages", getattr(q, "total_stages", 1))
            completed = getattr(q, "is_completed", getattr(q, "completed", False))
            desc = getattr(q, "description", getattr(q, "objective", ""))
            chamber = getattr(q, "chamber_id", getattr(q, "chamber", "All"))

        status_flag = "[COMPLETED]" if completed else f"[STAGE {stage}/{max_stg}]"
        print(f"► {status_flag} {qid}: {title} (Chamber: {chamber})")
        if desc:
            print(f"   Objective: {desc}")
else:
    print("[-] No active_quests structure found on GAME_LOOP.")

print("\n==================================================")
print(" 2. ASH ARCHIVE PERSISTED QUEST STRATA (SQLite)")
print("==================================================")

db_path = os.path.join("strata", "ash_archive.db")
if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    
    # Inspect ash_ledger for quest resolutions
    c.execute("""
        SELECT timestamp, content_hash, state_payload 
        FROM ash_ledger 
        WHERE state_payload LIKE '%quest%' OR state_payload LIKE '%COMBAT_VICTORY%'
        ORDER BY id DESC LIMIT 5;
    """)
    rows = c.fetchall()
    if rows:
        for r in rows:
            ts, chash, payload_raw = r
            try:
                pl = json.loads(payload_raw)
                evt = pl.get("event", "STATE_EVENT")
                res_quest = pl.get("rewards", {}).get("quest_resolved", "N/A")
                print(f"• [{ts}] {evt} -> Resolved: {res_quest} | Ref: {chash[:16]}...")
            except Exception:
                print(f"• [{ts}] Hash: {chash[:16]}... | Data: {payload_raw[:50]}")
    else:
        print("[*] No quest completion entries recorded in ash_ledger yet.")
    conn.close()
else:
    print(f"[-] Database not found at {db_path}")

print("\n==================================================")
print(" 3. ACTIVE OBJECTIVES FOR CHAMBER II")
print("==================================================")
print("• Primary Carrier Frequency:  52.8 Hz (Teal / Somatic Constant)")
print("• Sub-System Pressure Status: 2.1 bar (Liquid N2 Regulated)")
print("• Somatic Bridge Gateway:     Cryo-Sink Equilibrium -> Valve Alignment")
