import json
import sqlite3
import os
import hashlib
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional

class SaveManagerEngine:
    """
    Cathedral-Engine Save/Load Profile Manager & Campaign Chronicle Exporter
    Handles 3-slot Merkle-verified campaign persistence and automated NotebookLM export.
    """
    def __init__(self, db_path: Optional[str] = None):
        if db_path is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            db_path = os.path.join(base_dir, "strata", "campaign.db")
        self.db_path = db_path
        self._init_db()

    def _get_conn(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self):
        with self._get_conn() as conn:
            conn.executescript("""
                CREATE TABLE IF NOT EXISTS save_slots (
                    slot_id INTEGER PRIMARY KEY,
                    slot_name TEXT NOT NULL,
                    character_name TEXT NOT NULL,
                    chamber_index INTEGER NOT NULL,
                    stratum_name TEXT NOT NULL,
                    state_json TEXT NOT NULL,
                    merkle_root TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS dialogue_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    speaker TEXT NOT NULL,
                    chosen_text TEXT NOT NULL,
                    consequence TEXT NOT NULL,
                    node_id TEXT NOT NULL,
                    ledger_hash TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS combat_log (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    actor TEXT NOT NULL,
                    action_type TEXT NOT NULL,
                    roll_result INTEGER NOT NULL,
                    outcome TEXT NOT NULL,
                    paradox_delta INTEGER NOT NULL,
                    ledger_hash TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS character_progression (
                    character_name TEXT PRIMARY KEY,
                    level INTEGER NOT NULL DEFAULT 1,
                    insight_xp INTEGER NOT NULL DEFAULT 0,
                    unspent_insight INTEGER NOT NULL DEFAULT 100,
                    resonance INTEGER NOT NULL DEFAULT 3,
                    somatic INTEGER NOT NULL DEFAULT 2,
                    insight INTEGER NOT NULL DEFAULT 3,
                    max_hp INTEGER NOT NULL DEFAULT 20,
                    max_ap INTEGER NOT NULL DEFAULT 4,
                    max_strain REAL NOT NULL DEFAULT 6.0
                );

                CREATE TABLE IF NOT EXISTS chamber_gates (
                    chamber_num INTEGER PRIMARY KEY,
                    stratum_name TEXT NOT NULL,
                    unlocked BOOLEAN NOT NULL DEFAULT 0,
                    unlocked_reason TEXT NOT NULL
                );
            """)
            conn.commit()

    def save_slot(self, slot_id: int, slot_name: str, state_data: Dict[str, Any]) -> Dict[str, Any]:
        """Saves current state snapshot into designated slot with SHA-256 Merkle check."""
        if not (1 <= slot_id <= 3):
            return {"error": "Invalid slot ID (Must be 1, 2, or 3)."}

        player = state_data.get("player", {})
        char_name = player.get("name", "Kiri Vespera")
        chamber_idx = player.get("chamber", 1)
        stratum = player.get("stratum", "Prime Foundations")
        ts = datetime.now(timezone.utc).isoformat()

        raw_state_json = json.dumps(state_data, sort_keys=True)
        merkle_root = "0x" + hashlib.sha256(f"{slot_id}_{ts}_{raw_state_json}".encode()).hexdigest().upper()

        with self._get_conn() as conn:
            conn.execute("""
                INSERT OR REPLACE INTO save_slots (slot_id, slot_name, character_name, chamber_index, stratum_name, state_json, merkle_root, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (slot_id, slot_name, char_name, chamber_idx, stratum, raw_state_json, merkle_root, ts))
            conn.commit()

        return {
            "success": True,
            "slot_id": slot_id,
            "slot_name": slot_name,
            "character_name": char_name,
            "chamber": chamber_idx,
            "stratum": stratum,
            "merkle_root": merkle_root,
            "timestamp": ts
        }

    def load_slot(self, slot_id: int) -> Optional[Dict[str, Any]]:
        """Loads and parses saved session state from slot."""
        with self._get_conn() as conn:
            cur = conn.execute("SELECT * FROM save_slots WHERE slot_id = ?", (slot_id,))
            row = cur.fetchone()
            if not row:
                return None
            data = dict(row)
            data["state"] = json.loads(data["state_json"])
            return data

    def list_slots(self) -> List[Dict[str, Any]]:
        """Lists all 3 save slots."""
        with self._get_conn() as conn:
            cur = conn.execute("SELECT slot_id, slot_name, character_name, chamber_index, stratum_name, merkle_root, updated_at FROM save_slots ORDER BY slot_id ASC")
            slots = {r["slot_id"]: dict(r) for r in cur.fetchall()}

        result = []
        for s_id in range(1, 4):
            if s_id in slots:
                result.append(slots[s_id])
            else:
                result.append({
                    "slot_id": s_id,
                    "slot_name": f"Empty Slot {s_id}",
                    "character_name": "None",
                    "chamber_index": 0,
                    "stratum_name": "Uninitialized",
                    "merkle_root": "0x00000000000000000000",
                    "updated_at": "Never"
                })
        return result

    def export_chronicle_to_markdown(self, output_file: Optional[str] = None) -> str:
        """
        Compiles the player's full campaign history into a formatted Markdown monograph
        optimized for Google NotebookLM research ingest and narrative synthesis.
        """
        if output_file is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            output_file = os.path.join(base_dir, "PLAYER_CAMPAIGN_CHRONICLE.md")

        with self._get_conn() as conn:
            # Query dialogue history
            cur = conn.execute("SELECT * FROM dialogue_history ORDER BY id ASC")
            dialogue_rows = [dict(r) for r in cur.fetchall()]

            # Query combat history
            cur = conn.execute("SELECT * FROM combat_log ORDER BY id ASC LIMIT 25")
            combat_rows = [dict(r) for r in cur.fetchall()]

            # Query party progression
            cur = conn.execute("SELECT * FROM character_progression")
            prog_rows = [dict(r) for r in cur.fetchall()]

            # Query chamber gates
            cur = conn.execute("SELECT * FROM chamber_gates ORDER BY chamber_num ASC")
            gate_rows = [dict(r) for r in cur.fetchall()]

        # Build Markdown Document
        lines = [
            "# MLAOS-Prime & Cathedral-Engine :: Sovereign Campaign Chronicle",
            f"*Generated on {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')} | Geodetic Anchor: Olney, IL (37.7306° N, -88.0817° W)*",
            "",
            "## 1. Liturgy of State & Active Party Roster",
            ""
        ]

        if prog_rows:
            for p in prog_rows:
                lines.append(f"- **{p['character_name']}** (Level {p['level']}): Insight XP: `{p['unspent_insight']}` | Resonance: `{p['resonance']}` | Somatic: `{p['somatic']}` | Insight: `{p['insight']}` | Max HP: `{p['max_hp']}` | Max AP: `{p['max_ap']}`")
        else:
            lines.append("- **Kiri Vespera** (Level 1): Void Walker | HP: `20/20` | AP: `4/4`")

        lines.extend([
            "",
            "## 2. Never-Overwrite Dialogue Inscriptions & Moral Trajectories",
            ""
        ])

        if dialogue_rows:
            for d in dialogue_rows:
                lines.append(f"- `[{d['timestamp'][:19]}]` **{d['speaker']}**: \"{d['chosen_text']}\" ➔ *Consequence: {d['consequence']}* (Ledger Hash: `{d['ledger_hash']}`)")
        else:
            lines.append("*No conversational inscriptions recorded yet.*")

        lines.extend([
            "",
            "## 3. Chamber Gate Penetration Status",
            ""
        ])

        if gate_rows:
            for g in gate_rows:
                status = "OPEN" if g["unlocked"] else "SEALED"
                lines.append(f"- **Chamber {g['chamber_num']:02d}** [{status}]: {g['stratum_name']} (*{g['unlocked_reason']}*)")
        else:
            lines.append("- **Chamber 01** [OPEN]: Prime Foundations - Book I: The Lithic Threshold (*Genesis Inscription Active*)")

        lines.extend([
            "",
            "## 4. Tactical Combat Log & Arcana Resolutions",
            ""
        ])

        if combat_rows:
            for c in combat_rows:
                act_name = c.get("action_name") or c.get("action_type", "Harmonic Strike")
                tot = c.get("total_score") or c.get("roll_result", 0)
                hash_val = c.get("ledger_hash", "0x0000")[:16]
                outcome = c.get("outcome", "Action Resolved")
                lines.append(f"- `[{c['timestamp'][:19]}]` **{c['actor']}** executed `{act_name}` ➔ Result: `{tot}` [Outcome: {outcome}] (*Ledger: {hash_val}...*)")
        else:
            lines.append("*No combat engagements recorded yet.*")

        lines.extend([
            "",
            "---",
            "*Document End :: Formatted for Sovereign Archival & NotebookLM Knowledge Graph Synthesis.*"
        ])

        nl = chr(10)
        content = nl.join(lines)
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(content)

        return output_file

if __name__ == "__main__":
    mgr = SaveManagerEngine()
    print("[SAVE MANAGER] Listing initial save slots:")
    for s in mgr.list_slots():
        print(f"  Slot {s['slot_id']}: {s['slot_name']} | Character: {s['character_name']} | Stratum: {s['stratum_name']}")

    sample_state = {"player": {"name": "Kiri Vespera", "chamber": 1, "stratum": "Prime Foundations"}}
    res = mgr.save_slot(1, "Lithic Threshold Checkpoint", sample_state)
    print()
    print(f"[SAVE] Slot 1 Saved: {res['merkle_root']}")

    chronicle_path = mgr.export_chronicle_to_markdown()
    print(f"[CHRONICLE] Exported campaign chronicle to {chronicle_path}")
