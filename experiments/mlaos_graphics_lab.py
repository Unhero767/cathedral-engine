import sqlite3
import hashlib
import json
import math
import os
import urllib.request

DB_PATH = "ash_archive.db"
TELEMETRY_URL = "http://localhost:8000/telemetry"

class MLAOSGraphicsLab:
    def __init__(self):
        self.init_graphics_db()

    def init_graphics_db(self):
        conn = sqlite3.connect(DB_PATH)
        conn.execute("PRAGMA journal_mode=WAL;")
        conn.execute('''
            CREATE TABLE IF NOT EXISTS graphics_experiments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                experiment_type TEXT,
                spectral_constant TEXT,
                metric_summary TEXT,
                merkle_hash TEXT,
                payload TEXT
            )
        ''')
        conn.commit()
        conn.close()

    def generate_bayer_matrix(self, n: int) -> list:
        if n == 1:
            return [[0]]
        half = self.generate_bayer_matrix(n // 2)
        size = len(half)
        matrix = [[0 for _ in range(n)] for _ in range(n)]
        
        for r in range(size):
            for c in range(size):
                val = half[r][c]
                matrix[r][c]             = 4 * val
                matrix[r][c + size]      = 4 * val + 2
                matrix[r + size][c]      = 4 * val + 3
                matrix[r + size][c + size] = 4 * val + 1
        return matrix

    def broadcast_to_gateway(self, tier: str, payload: dict):
        data = {"tier": tier, "payload": payload}
        req = urllib.request.Request(
            TELEMETRY_URL,
            data=json.dumps(data).encode("utf-8"),
            headers={"Content-Type": "application/json"}
        )
        try:
            with urllib.request.urlopen(req) as response:
                res = json.loads(response.read().decode("utf-8"))
                print(f"-> [Telemetry Bridge] Streamed Tier [{tier}] successfully (ID: {res.get('id')})")
        except Exception as e:
            print(f"-> [Telemetry Bridge Warning] Gateway offline or unreachable: {e}")

    def run_bayer_dither_experiment(self, threshold_divisor: float = 16.0):
        print("\n[GRAPHICS LAB] Executing Bayer 4x4 Ordered Dithering Pipeline")
        print("="*60)
        matrix_4x4 = self.generate_bayer_matrix(4)
        normalized = [[val / threshold_divisor for val in row] for row in matrix_4x4]
        
        payload = {
            "experimentType": "Bayer Dithering",
            "matrixSize": 4,
            "matrix": normalized,
            "shaderApplication": "SpatialLumenDither.gdshader"
        }
        
        payload_str = json.dumps(payload, sort_keys=True)
        merkle_hash = hashlib.sha256(payload_str.encode("utf-8")).hexdigest()
        
        self.commit_and_broadcast("GRAPHICS", "Teal Curiosity", "Bayer Dithering", "4x4 Matrix Generated", merkle_hash, payload_str, payload)

    def run_sprite_atlas_experiment(self, frame_count: int = 32, tile_size: int = 128):
        print("\n[GRAPHICS LAB] Executing Sprite Atlas & Somatic Layer Generator")
        print("="*60)
        
        total_width = frame_count * tile_size
        total_height = tile_size
        
        payload = {
            "experimentType": "Sprite Atlas Strip",
            "atlasName": "EAS-03_Cathedral_Master_Strip",
            "tileSize": tile_size,
            "frameCount": frame_count,
            "masterWidth": total_width,
            "masterHeight": total_height,
            "spectralResonance": "Gold Joy",
            "layers": 12
        }

        payload_str = json.dumps(payload, sort_keys=True)
        merkle_hash = hashlib.sha256(payload_str.encode("utf-8")).hexdigest()

        self.commit_and_broadcast("GRAPHICS", "Gold Joy", "Sprite Atlas", f"{frame_count} Frames / {total_width}x{total_height}px", merkle_hash, payload_str, payload)

    def run_vector_field_experiment(self, resolution: int = 8):
        print("\n[GRAPHICS LAB] Executing Vector Field & Resonance Gradient Simulator")
        print("="*60)
        
        vectors = []
        for x in range(resolution):
            for y in range(resolution):
                nx = (x / resolution) - 0.5
                ny = (y / resolution) - 0.5
                angle = math.atan2(ny, nx)
                magnitude = math.sqrt(nx**2 + ny**2)
                vectors.append({"coord": [x, y], "gradientAngle": round(angle, 4), "harmonicAttraction": round(1.0 - magnitude, 4)})

        payload = {
            "experimentType": "Vector Field Gradient",
            "resolution": resolution,
            "sampleVectors": vectors[:4]
        }
        
        payload_str = json.dumps(payload, sort_keys=True)
        merkle_hash = hashlib.sha256(payload_str.encode("utf-8")).hexdigest()

        self.commit_and_broadcast("GRAPHICS", "Blue Sorrow", "Vector Field", f"{resolution}x{resolution} Harmonic Gradient", merkle_hash, payload_str, payload)

    def commit_and_broadcast(self, tier: str, spectral: str, exp_type: str, summary: str, merkle: str, payload_str: str, payload_dict: dict):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO graphics_experiments (experiment_type, spectral_constant, metric_summary, merkle_hash, payload) VALUES (?, ?, ?, ?, ?)",
            (exp_type, spectral, summary, merkle, payload_str)
        )
        conn.commit()
        conn.close()
        print(f"-> Committed to Ash Archive [Type: {exp_type} | SHA: {merkle[:12]}...]")

        self.broadcast_to_gateway(tier, payload_dict)
        print("="*60)

if __name__ == "__main__":
    lab = MLAOSGraphicsLab()
    lab.run_bayer_dither_experiment()
    lab.run_sprite_atlas_experiment()
    lab.run_vector_field_experiment()
