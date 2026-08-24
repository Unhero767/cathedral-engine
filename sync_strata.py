import sqlite3
import json
import os

DB_PATH = os.path.join("strata", "ash_archive.db")

def sync_game_loop(gl, db_path=DB_PATH, player_id="player_primary"):
    if not os.path.exists(db_path):
        return {"error": f"Database not found at {db_path}"}

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    try:
        # 1. Fetch persistent player state from player_state
        c.execute("""
            SELECT player_id, current_chamber_id, coord_x, coord_y, active_spectrum, health, max_health, inventory_json
            FROM player_state
            WHERE player_id = ?;
        """, (player_id,))
        p_row = c.fetchone()

        if p_row:
            try:
                inv = json.loads(p_row["inventory_json"] or "{}")
            except Exception:
                inv = {}

            if isinstance(gl.player, dict):
                gl.player["hp"] = p_row["health"]
                gl.player["max_hp"] = p_row["max_health"]
                gl.player["x"] = p_row["coord_x"]
                gl.player["y"] = p_row["coord_y"]
                gl.player["chamber"] = p_row["current_chamber_id"]
                gl.player["spectrum"] = p_row["active_spectrum"]
                gl.player["inventory"] = inv
            else:
                gl.player.hp = p_row["health"]
                gl.player.max_hp = p_row["max_health"]
                gl.player.x = p_row["coord_x"]
                gl.player.y = p_row["coord_y"]
                gl.player.chamber = p_row["current_chamber_id"]
                gl.player.spectrum = p_row["active_spectrum"]
                gl.player.inventory = inv

        # 2. Inspect ash_ledger for completed quest events
        completed_quests = set()
        try:
            c.execute("""
                SELECT state_payload FROM ash_ledger
                WHERE state_payload LIKE '%COMBAT_VICTORY%' OR state_payload LIKE '%quest_resolved%';
            """)
            for row in c.fetchall():
                try:
                    payload = json.loads(row["state_payload"])
                    q_id = payload.get("rewards", {}).get("quest_resolved")
                    if q_id:
                        completed_quests.add(q_id)
                except Exception:
                    continue
        except sqlite3.OperationalError:
            pass

        # 3. Synchronize active_quests in memory
        if hasattr(gl, "active_quests") and isinstance(gl.active_quests, list):
            for q in gl.active_quests:
                qid = q.get("quest_id") if isinstance(q, dict) else getattr(q, "quest_id", None)
                if qid in completed_quests:
                    if isinstance(q, dict):
                        q["is_completed"] = True
                        q["current_stage"] = q.get("max_stages", 1)
                    else:
                        q.is_completed = True
                        q.current_stage = getattr(q, "max_stages", 1)

        chamber_val = gl.player.get("chamber") if isinstance(gl.player, dict) else getattr(gl.player, "chamber", 1)
        log_msg = f"[SYNC] Ingested SQLite strata: Chamber {chamber_val}, Completed: {list(completed_quests)}"
        if hasattr(gl, "action_log"):
            gl.action_log.append(log_msg)

        return {
            "success": True,
            "chamber": chamber_val,
            "inventory": gl.player.get("inventory") if isinstance(gl.player, dict) else getattr(gl.player, "inventory", {}),
            "completed_quests": list(completed_quests)
        }

    except Exception as e:
        return {"error": f"Synchronization failed: {str(e)}"}
    finally:
        conn.close()

if __name__ == "__main__":
    import server
    print("=== EXECUTING STANDALONE STRATA SYNC ===")
    res = sync_game_loop(server.GAME_LOOP)
    print(json.dumps(res, indent=2))
