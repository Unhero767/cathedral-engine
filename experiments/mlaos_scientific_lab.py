import sqlite3
import hashlib
import json
import math
import time
from datetime import datetime

DB_PATH = "ash_archive.db"

class MLAOSScientificLab:
    def __init__(self):
        self.init_lab_db()

    def init_lab_db(self):
        conn = sqlite3.connect(DB_PATH)
        conn.execute("PRAGMA journal_mode=WAL;")
        conn.execute('''
            CREATE TABLE IF NOT EXISTS lab_experiments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                experiment_name TEXT,
                spectral_constant TEXT,
                belnap_state TEXT,
                phi_rate REAL,
                merkle_hash TEXT,
                payload TEXT
            )
        ''')
        conn.commit()
        conn.close()

    def evaluate_belnap_dunn(self, prop_a: str, prop_b: str) -> str:
        """
        Evaluates Belnap-Dunn four-valued logic matrix:
        T (True), F (False), B (Both/Contradictory), N (Neither/Unassigned)
        """
        if prop_a == "T" and prop_b == "T": return "T"
        if prop_a == "F" and prop_b == "F": return "F"
        if prop_a == "T" and prop_b == "F": return "B"
        if prop_a == "B" or prop_b == "B": return "B"
        return "N"

    def compute_consciousness_intensity(self, complexity: float, temporal_delta: float) -> float:
        """
        Calculates dΦ/dt: Rate of change of integrated information (Phi) over time.
        """
        if temporal_delta <= 0:
            return 0.0
        return complexity * math.log(1.0 + (1.0 / temporal_delta))

    def run_experiment(self, name: str, spectral_constant: str, prop_a: str, prop_b: str, complexity: float):
        print(f"\n[MLAOS LAB] Initiating Experiment: {name} [{spectral_constant}]\n" + "="*60)
        
        start_time = time.time()
        
        # 1. Paraconsistent Evaluation
        bp_result = self.evaluate_belnap_dunn(prop_a, prop_b)
        print(f"-> Belnap-Dunn Matrix Resolution ({prop_a} ⊗ {prop_b}) = [{bp_result}]")
        
        if bp_result == "B":
            print("-> HARMONIC SCAR CRYSTALLIZED: Contradiction absorbed into load-bearing masonry.")
        
        # 2. Consciousness Intensity Calculation
        time.sleep(0.05)
        delta = time.time() - start_time
        phi_rate = self.compute_consciousness_intensity(complexity, delta)
        print(f"-> Consciousness Intensity Rate (dΦ/dt): {phi_rate:.4f}")

        # 3. Compile Experimental Payload
        payload = {
            "experiment": name,
            "spectralConstant": spectral_constant,
            "belnapResolution": bp_result,
            "phiRate": phi_rate,
            "executionTimeMs": delta * 1000,
            "status": "STABLE" if bp_result != "B" else "SCAR_ABSORBED"
        }

        # 4. Generate Merkle Cryptographic Hash
        payload_str = json.dumps(payload, sort_keys=True)
        merkle_hash = hashlib.sha256(payload_str.encode('utf-8')).hexdigest()
        print(f"-> Cryptographic Hash Lineage (SHA-256): {merkle_hash}")

        # 5. Commit to Ash Archive WAL Database
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO lab_experiments (experiment_name, spectral_constant, belnap_state, phi_rate, merkle_hash, payload) VALUES (?, ?, ?, ?, ?, ?)",
            (name, spectral_constant, bp_result, phi_rate, merkle_hash, payload_str)
        )
        conn.commit()
        exp_id = cursor.lastrowid
        conn.close()
        
        print(f"-> Committed to Ash Archive [Experiment ID: {exp_id}]\n" + "="*60)
        return exp_id

if __name__ == "__main__":
    lab = MLAOSScientificLab()
    
    lab.run_experiment(
        name="Protocol-Alpha: Altar Resonance Verification",
        spectral_constant="Gold Joy",
        prop_a="T",
        prop_b="T",
        complexity=8.45
    )
    
    lab.run_experiment(
        name="Protocol-Beta: Vault Fracture Dialetheic Stress",
        spectral_constant="Blue Sorrow",
        prop_a="T",
        prop_b="F",
        complexity=12.10
    )
    
    lab.run_experiment(
        name="Protocol-Gamma: Liminal Threshold Exploration",
        spectral_constant="Teal Curiosity",
        prop_a="B",
        prop_b="N",
        complexity=9.75
    )
