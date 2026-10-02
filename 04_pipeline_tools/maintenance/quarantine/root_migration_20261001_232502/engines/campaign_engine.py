import sqlite3
import os
import random
import hashlib
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional

class CampaignEngine:
    """
    SQLite Tactical Campaign & Relic Engine
    Manages party rosters, attuned relic strain tracking, and combat resolution logging.
    """
    def __init__(self, db_path: Optional[str] = None):
        if db_path is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            db_path = os.path.join(base_dir, "strata", "campaign.db")
        self.db_path = db_path
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self.init_db()

    def _get_conn(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def init_db(self):
        with self._get_conn() as conn:
            conn.executescript("""
                CREATE TABLE IF NOT EXISTS party (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    designation TEXT NOT NULL,
                    emotional_state TEXT NOT NULL,
                    paradox INTEGER NOT NULL DEFAULT 0,
                    hp INTEGER NOT NULL DEFAULT 20
                );

                CREATE TABLE IF NOT EXISTS inventory (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    owner_id INTEGER,
                    item_name TEXT NOT NULL,
                    item_class TEXT NOT NULL,
                    attuned BOOLEAN NOT NULL DEFAULT 0,
                    strain_weight REAL NOT NULL DEFAULT 1.0,
                    FOREIGN KEY(owner_id) REFERENCES party(id)
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
            """)
            conn.commit()

            # Seed default party if empty
            cur = conn.cursor()
            cur.execute("SELECT COUNT(*) as cnt FROM party")
            if cur.fetchone()["cnt"] == 0:
                self.seed_default_party()

    def seed_default_party(self):
        with self._get_conn() as conn:
            conn.execute("INSERT INTO party (name, designation, emotional_state, paradox, hp) VALUES (?, ?, ?, ?, ?)",
                         ("Kiri Vespera", "Void Walker", "Sapphire/Strain", 1, 18))
            kiri_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
            conn.execute("INSERT INTO party (name, designation, emotional_state, paradox, hp) VALUES (?, ?, ?, ?, ?)",
                         ("Aurelia-9", "Cybernetic Synthete", "Gold/Joy", 0, 22))
            aurelia_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]

            # Relics
            conn.execute("INSERT INTO inventory (owner_id, item_name, item_class, attuned, strain_weight) VALUES (?, ?, ?, ?, ?)",
                         (kiri_id, "HGASE Resonator Prism", "Relic", 1, 2.5))
            conn.execute("INSERT INTO inventory (owner_id, item_name, item_class, attuned, strain_weight) VALUES (?, ?, ?, ?, ?)",
                         (aurelia_id, "High-Frequency Monoblade", "Weapon", 1, 1.8))
            conn.commit()

    def get_party(self) -> List[Dict[str, Any]]:
        with self._get_conn() as conn:
            cur = conn.execute("SELECT * FROM party")
            return [dict(r) for r in cur.fetchall()]

    def get_inventory(self) -> List[Dict[str, Any]]:
        with self._get_conn() as conn:
            cur = conn.execute("""
                SELECT i.*, p.name as owner_name 
                FROM inventory i 
                LEFT JOIN party p ON i.owner_id = p.id
            """)
            return [dict(r) for r in cur.fetchall()]

    def calculate_total_strain(self, party_member_id: int) -> float:
        with self._get_conn() as conn:
            cur = conn.execute("SELECT SUM(strain_weight) as total FROM inventory WHERE owner_id = ? AND attuned = 1", (party_member_id,))
            row = cur.fetchone()
            return row["total"] or 0.0

    def record_combat_turn(self, actor: str, action_type: str, stat_mod: int = 1) -> Dict[str, Any]:
        d1 = random.randint(1, 6)
        d2 = random.randint(1, 6)
        raw_sum = d1 + d2
        total_roll = raw_sum + stat_mod

        if total_roll >= 10:
            outcome = "Critical Hit / Harmonic Resonance"
            p_delta = 0
        elif 7 <= total_roll <= 9:
            outcome = "Partial Strike / Minor Strain"
            p_delta = 1
        else:
            outcome = "Fumble / Paraconsistent Overload"
            p_delta = 2

        ts = datetime.now(timezone.utc).isoformat()
        ledger_hash = "0x" + hashlib.sha256(f"{ts}_{actor}_{action_type}_{total_roll}".encode()).hexdigest()[:24].upper()

        with self._get_conn() as conn:
            conn.execute("""
                INSERT INTO combat_log (timestamp, actor, action_type, roll_result, outcome, paradox_delta, ledger_hash)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (ts, actor, action_type, total_roll, outcome, p_delta, ledger_hash))
            
            # Update actor paradox if in party
            if p_delta > 0:
                conn.execute("UPDATE party SET paradox = paradox + ? WHERE name = ?", (p_delta, actor))
            conn.commit()

        return {
            "timestamp": ts,
            "actor": actor,
            "action_type": action_type,
            "dice": [d1, d2],
            "roll_result": total_roll,
            "outcome": outcome,
            "paradox_delta": p_delta,
            "ledger_hash": ledger_hash
        }

if __name__ == "__main__":
    camp = CampaignEngine()
    print("[CAMPAIGN ENGINE] Initialized. Party roster:")
    for p in camp.get_party():
        print(f"  - {p['name']} ({p['designation']}) | HP: {p['hp']}, Paradox: {p['paradox']}, Strain: {camp.calculate_total_strain(p['id'])}")
