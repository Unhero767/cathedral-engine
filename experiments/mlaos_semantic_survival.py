import sqlite3
import hashlib
import json
import math
import urllib.request

DB_PATH = "ash_archive.db"
TELEMETRY_URL = "http://localhost:8000/telemetry"

class MLAOSSemanticSurvivalEngine:
    def __init__(self):
        self.init_survival_db()

    def init_survival_db(self):
        conn = sqlite3.connect(DB_PATH)
        conn.execute("PRAGMA journal_mode=WAL;")
        conn.execute('''
            CREATE TABLE IF NOT EXISTS survival_simulations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                spectral_state TEXT,
                ego_density REAL,
                mortar_integrity REAL,
                merkle_hash TEXT,
                payload TEXT
            )
        ''')
        conn.commit()
        conn.close()

    def simulate_lattice(self, spectral_state: str, emotional_charge: float):
        print(f"[SURVIVAL ENGINE] Simulating Spectrafilament Lattice [{spectral_state}] (Charge: {emotional_charge})")
        ego_density = emotional_charge * 3.14159 / 2.0
        mortar_integrity = max(0.0, 100.0 - (ego_density * 4.5))
        
        payload = {
            "engine": "Bio-Semantic Survival v3.1",
            "spectralState": spectral_state,
            "egoDensity": round(ego_density, 4),
            "mortarIntegrity": round(mortar_integrity, 2),
            "metamorphicSqueeze": "RESOLVED" if mortar_integrity > 20.0 else "CRITICAL_COLLAPSE"
        }
        
        payload_str = json.dumps(payload, sort_keys=True)
        merkle_hash = hashlib.sha256(payload_str.encode("utf-8")).hexdigest()
        
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO survival_simulations (spectral_state, ego_density, mortar_integrity, merkle_hash, payload) VALUES (?, ?, ?, ?, ?)",
            (spectral_state, ego_density, mortar_integrity, merkle_hash, payload_str)
        )
        conn.commit()
        conn.close()
        
        print(f"-> Ego Density: {ego_density:.2f} | Mortar Integrity: {mortar_integrity:.1f}% | SHA: {merkle_hash[:12]}...")
        try:
            urllib.request.urlopen(
                urllib.request.Request(
                    TELEMETRY_URL,
                    data=json.dumps({"tier": "SURVIVAL", "payload": payload}).encode("utf-8"),
                    headers={"Content-Type": "application/json"}
                )
            )
        except Exception:
            pass

if __name__ == "__main__":
    engine = MLAOSSemanticSurvivalEngine()
    engine.simulate_lattice("Teal Curiosity", 7.82)
