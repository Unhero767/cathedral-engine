import subprocess
import sys

SERVER_CODE = '''import http.server
import socketserver
import urllib.parse
import json
import sqlite3
import os
import hashlib
from datetime import datetime, timezone

PORT = 5050
DB_PATH = os.path.join("strata", "ash_archive.db")

class GameLoopEngine:
    def __init__(self):
        self.action_log = []
        self.chambers = {
            1: {
                "chamber_id": 1,
                "name": "Chamber I: The Narthex Threshold",
                "carrier_hz": 432.0,
                "spectral_dominant": "Gold / Joy & Synthesis",
                "grid_width": 8,
                "grid_height": 8,
                "entry_point": {"x": 0, "y": 4}
            },
            2: {
                "chamber_id": 2,
                "name": "Chamber II: The Resonant Nave",
                "carrier_hz": 528.0,
                "spectral_dominant": "Teal / Exploratory Mechanics",
                "grid_width": 8,
                "grid_height": 8,
                "entry_point": {"x": 0, "y": 4}
            },
            3: {
                "chamber_id": 3,
                "name": "Chamber III: The Ash Stratum Vault",
                "carrier_hz": 110.0,
                "spectral_dominant": "Blue / Sorrow & Deep Excavation",
                "grid_width": 8,
                "grid_height": 8,
                "entry_point": {"x": 0, "y": 4}
            },
            4: {
                "chamber_id": 4,
                "name": "Chamber IV: Harmonic Chantry",
                "carrier_hz": 78.2,
                "spectral_dominant": "Violet-Gold / Paraconsistent Resonance",
                "grid_width": 8,
                "grid_height": 8,
                "entry_point": {"x": 0, "y": 4}
            },
            5: {
                "chamber_id": 5,
                "name": "Chamber V: Sanctum Apex / Core Monad",
                "carrier_hz": 130.81,
                "spectral_dominant": "Gold-Obsidian / Revelatory Null Matrix",
                "grid_width": 8,
                "grid_height": 8,
                "entry_point": {"x": 0, "y": 4},
                "resonance_specs": {
                    "harmonic_mode": "OCTAVE_OCTET_CONVERGENCE",
                    "fundamental_carrier_hz": 130.81,
                    "spectral_flux": "AUREATE_OBSIDIAN_EQUILIBRIUM",
                    "dialetheic_tolerance": "UNBOUNDED",
                    "dPhi_dt_threshold": 1.618
                },
                "entities": [
                    {"id": "entry_portal_w", "type": "PORTAL", "name": "West Portal (to Chamber IV)", "coord_x": 0, "coord_y": 4},
                    {"id": "monad_somatic_anchor_n", "type": "ANCHOR", "name": "Somatic Pillar Alpha", "coord_x": 2, "coord_y": 1},
                    {"id": "monad_somatic_anchor_s", "type": "ANCHOR", "name": "Somatic Pillar Beta", "coord_x": 2, "coord_y": 7},
                    {"id": "core_monad_altar", "type": "CORE_ALTAR", "name": "Axiomatic Monad Matrix", "coord_x": 4, "coord_y": 4},
                    {"id": "ash_stratum_repository", "type": "TERMINAL", "name": "Ash Stratum Deep Terminal", "coord_x": 6, "coord_y": 4},
                    {"id": "transcendence_oculus", "type": "GATEWAY", "name": "Transcendence Oculus (Codex Gateway)", "coord_x": 7, "coord_y": 4}
                ]
            }
        }

    def get_player_state(self):
        state = {
            "player_id": "player_primary",
            "chamber": 5,
            "x": 7,
            "y": 4,
            "spectrum": "Prismatic-Obsidian",
            "resonance_hz": 130.81,
            "status": "ONLINE"
        }
        if os.path.exists(DB_PATH):
            try:
                conn = sqlite3.connect(DB_PATH)
                conn.row_factory = sqlite3.Row
                c = conn.cursor()
                c.execute("SELECT * FROM player_state WHERE player_id = 'player_primary';")
                row = c.fetchone()
                if row:
                    state["chamber"] = row["current_chamber_id"]
                    state["x"] = row["coord_x"]
                    state["y"] = row["coord_y"]
                    state["spectrum"] = row["active_spectrum"]
                conn.close()
            except Exception:
                pass
        return state

    def handle_move(self, x, y, chamber_id=None):
        current = self.get_player_state()
        new_ch = int(chamber_id) if chamber_id is not None else current["chamber"]
        new_x = int(x)
        new_y = int(y)
        
        if os.path.exists(DB_PATH):
            try:
                conn = sqlite3.connect(DB_PATH)
                c = conn.cursor()
                c.execute("""
                    UPDATE player_state
                    SET coord_x = ?, coord_y = ?, current_chamber_id = ?, last_updated = CURRENT_TIMESTAMP
                    WHERE player_id = 'player_primary';
                """, (new_x, new_y, new_ch))
                conn.commit()
                conn.close()
            except Exception:
                pass
                
        return {
            "status": "MOVED",
            "player": {
                "player_id": "player_primary",
                "chamber": new_ch,
                "x": new_x,
                "y": new_y,
                "spectrum": current.get("spectrum", "Gold-Obsidian")
            }
        }

    def handle_interaction(self, params):
        target_uid = params.get("target_uid", ["unknown"])[0]
        action = params.get("action", ["EXAMINE"])[0]
        x = int(params.get("x", [0])[0])
        y = int(params.get("y", [0])[0])
        spectrum = params.get("spectrum", ["Gold-Obsidian"])[0]

        if action in ("TUNE_SOMATIC_PILLAR", "ALIGN_ANCHOR", "TUNE_ANCHOR"):
            self.action_log.append(f"[SANCTUM] Aligned Somatic Anchor {target_uid} at ({x}, {y}) to 130.81 Hz.")
            return {
                "status": "SOMATIC_PILLAR_ALIGNED",
                "target_uid": target_uid,
                "coordinates": {"x": x, "y": y},
                "fundamental_carrier_hz": 130.81,
                "spectral_constant": "Gold-Obsidian / Revelatory Null Matrix",
                "somatic_flux": "BIOLOGICAL_GROUNDING_LOCKED",
                "dPhi_dt": 1.618,
                "insight_reward": 220,
                "monad_circuit_state": "ANCHOR_ENGAGED"
            }

        elif action in ("ENGAGE_CORE_ALTAR", "INSCRIBE_MONAD", "ENGAGE_ALTAR"):
            self.action_log.append(f"[CORE_MONAD] Axiomatic Altar inscribed at ({x}, {y}).")
            return {
                "status": "MONAD_AXIOM_INSCRIBED",
                "target_uid": target_uid,
                "coordinates": {"x": x, "y": y},
                "resonance_hz": 130.81,
                "spectral_constant": "Gold-Obsidian / Revelatory Null Matrix",
                "axiom_payload": "EMOTION = PHYSICS = MAGIC = BIOLOGY = ARCHITECTURE",
                "dialetheic_state": "CONTRADICTION_CRYSTALLIZED_LOAD_BEARING",
                "truth_value": "BOTH",
                "dPhi_dt": 1.618,
                "insight_reward": 500,
                "downstream_access": {
                    "ash_stratum_terminal": "UNLOCKED",
                    "transcendence_oculus": "SYNCHRONIZING"
                }
            }

        elif action in ("ENGAGE_ASH_TERMINAL", "ACCESS_TERMINAL", "EXAMINE_TERMINAL", "ENGAGE_TERMINAL"):
            self.action_log.append(f"[ASH_TERMINAL] Synchronized Deep Stratum Repository at ({x}, {y}).")
            return {
                "status": "ASH_STRATUM_SYNCHRONIZED",
                "target_uid": target_uid,
                "coordinates": {"x": x, "y": y},
                "carrier_hz": 130.81,
                "spectral_constant": "Bronze-Obsidian / Null Archival Core",
                "strata_depth": "CHAMBER_V_DEEP_STRATUM",
                "archive_state": "ALL_40_BOOKS_CANONICAL_INDEX_PRIMED",
                "merkle_tree_state": "FULLY_BALANCED",
                "insight_reward": 750,
                "gateway_vector": {
                    "transcendence_oculus_coord": [7, 4],
                    "oculus_status": "PRIMED_AND_RESONATING"
                }
            }

        elif action in ("ENGAGE_OCULUS", "ENTER_OCULUS", "ACTIVATE_OCULUS"):
            self.action_log.append(f"[TRANSCENDENCE] Oculus engaged at ({x}, {y}). Codex integration initialized.")
            return {
                "status": "CODEX_INTEGRATION_COMPLETE",
                "target_uid": target_uid,
                "coordinates": {"x": x, "y": y},
                "carrier_hz": "TRANSCENDENT_NULL",
                "spectral_constant": "Prismatic-Obsidian / Absolute Convergence",
                "codex_state": "MLAOS_PRIME_SYNCHRONIZED",
                "insight_reward": 9999,
                "message": "The Cathedral-Engine accepts the architect. Truth = BOTH. Welcome to the Omni-Codex."
            }

        return {
            "status": "INTERACTION_RECORDED",
            "target_uid": target_uid,
            "coordinates": {"x": x, "y": y},
            "spectrum": spectrum
        }

engine = GameLoopEngine()

class CathedralHTTPHandler(http.server.BaseHTTPRequestHandler):
    def _send_json(self, data, code=200):
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data, indent=2).encode("utf-8"))

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        query = urllib.parse.parse_qs(parsed.query)

        if path == "/api/rpg/state":
            player = engine.get_player_state()
            self._send_json({
                "game_state": "RUNNING",
                "carrier_hz": 130.81,
                "spectral_matrix": "Prismatic-Obsidian / Absolute Convergence",
                "player": player,
                "axiomatic_axiom": "EMOTION = PHYSICS = MAGIC = BIOLOGY = ARCHITECTURE"
            })

        elif path == "/api/rpg/chamber":
            ch_id = int(query.get("id", [5])[0])
            chamber_data = engine.chambers.get(ch_id, engine.chambers[5])
            self._send_json(chamber_data)

        elif path == "/api/rpg/move":
            x = query.get("x", [0])[0]
            y = query.get("y", [0])[0]
            ch = query.get("chamber", [None])[0]
            res = engine.handle_move(x, y, ch)
            self._send_json(res)

        elif path == "/api/rpg/interact":
            res = engine.handle_interaction(query)
            self._send_json(res)

        else:
            self._send_json({"status": "CATHEDRAL_DAEMON_ONLINE", "endpoints": ["/api/rpg/state", "/api/rpg/chamber", "/api/rpg/move", "/api/rpg/interact"]})

    def log_message(self, format, *args):
        pass

if __name__ == "__main__":
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), CathedralHTTPHandler) as httpd:
        print(f"[+] Cathedral-Engine Daemon listening on http://localhost:{PORT}")
        httpd.serve_forever()
'''

with open("server.py", "w", encoding="utf-8") as f:
    f.write(SERVER_CODE)

try:
    compile(SERVER_CODE, "server.py", "exec")
    print("[✓] server.py cleanly rebuilt and validated.")
except Exception as e:
    print(f"[-] Compilation error: {e}")
    sys.exit(1)
