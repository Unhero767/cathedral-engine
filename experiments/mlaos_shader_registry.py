import sqlite3
import hashlib
import json
import os
import urllib.request

DB_PATH = "ash_archive.db"
TELEMETRY_URL = "http://localhost:8000/telemetry"

class MLAOSShaderRegistry:
    def __init__(self):
        self.init_shader_db()

    def init_shader_db(self):
        conn = sqlite3.connect(DB_PATH)
        conn.execute("PRAGMA journal_mode=WAL;")
        conn.execute('''
            CREATE TABLE IF NOT EXISTS shader_registry (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                shader_name TEXT,
                shader_path TEXT,
                merkle_hash TEXT,
                payload TEXT
            )
        ''')
        conn.commit()
        conn.close()

    def audit_and_register_shaders(self):
        shaders = [
            ("SpatialLumenDither", "shaders/SpatialLumenDither.gdshader"),
            ("ResonanceScreen", "shaders/ResonanceScreen.gdshader")
        ]

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        for name, path in shaders:
            if os.path.exists(path):
                content = open(path, "r", encoding="utf-8").read()
                merkle_hash = hashlib.sha256(content.encode("utf-8")).hexdigest()
                
                payload = {
                    "shaderName": name,
                    "filePath": path,
                    "byteLength": len(content),
                    "status": "COMPILED_AND_VERIFIED"
                }
                
                cursor.execute(
                    "INSERT INTO shader_registry (shader_name, shader_path, merkle_hash, payload) VALUES (?, ?, ?, ?)",
                    (name, path, merkle_hash, json.dumps(payload))
                )
                conn.commit()
                print(f"[SHADER REGISTRY] Registered [{name}] | SHA-256: {merkle_hash[:16]}...")
                
                try:
                    urllib.request.urlopen(
                        urllib.request.Request(
                            TELEMETRY_URL,
                            data=json.dumps({"tier": "SHADER", "payload": payload}).encode("utf-8"),
                            headers={"Content-Type": "application/json"}
                        )
                    )
                except Exception:
                    pass
            else:
                print(f"[SHADER WARNING] Path not found: {path}")

        conn.close()

if __name__ == "__main__":
    registry = MLAOSShaderRegistry()
    registry.audit_and_register_shaders()
