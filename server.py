import http.server
import socketserver
import urllib.parse
import json
import sqlite3
import os

PORT = 5050
DB_PATH = os.path.join("strata", "ash_archive.db")

class CathedralHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        super().end_headers()

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        query = urllib.parse.parse_qs(parsed.query)

        if path in ("/", "/index.html"):
            try:
                with open("index.html", "rb") as f:
                    content = f.read()
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(content)))
                self.end_headers()
                self.wfile.write(content)
                return
            except Exception as e:
                self.send_error(500, f"Error reading index.html: {e}")
                return

        elif path == "/api/rpg/state":
            state = {
                "game_state": "RUNNING",
                "carrier_hz": 130.81,
                "player": {"chamber": 5, "x": 7, "y": 4, "spectrum": "Prismatic-Obsidian"}
            }
            if os.path.exists(DB_PATH):
                try:
                    conn = sqlite3.connect(DB_PATH)
                    conn.row_factory = sqlite3.Row
                    c = conn.cursor()
                    c.execute("SELECT * FROM player_state WHERE player_id = 'player_primary';")
                    p = c.fetchone()
                    if p:
                        state["player"]["chamber"] = p["current_chamber_id"]
                        state["player"]["x"] = p["coord_x"]
                        state["player"]["y"] = p["coord_y"]
                        state["player"]["spectrum"] = p["active_spectrum"]
                    conn.close()
                except Exception:
                    pass
            self._send_json(state)

        elif path == "/api/rpg/move":
            x = int(query.get("x", [7])[0])
            y = int(query.get("y", [4])[0])
            ch = int(query.get("chamber", [5])[0])
            if os.path.exists(DB_PATH):
                try:
                    conn = sqlite3.connect(DB_PATH)
                    c = conn.cursor()
                    c.execute("""
                        UPDATE player_state
                        SET coord_x = ?, coord_y = ?, current_chamber_id = ?, last_updated = CURRENT_TIMESTAMP
                        WHERE player_id = 'player_primary';
                    """, (x, y, ch))
                    conn.commit()
                    conn.close()
                except Exception:
                    pass
            self._send_json({"status": "MOVED", "x": x, "y": y, "chamber": ch})

        elif path == "/api/rpg/interact":
            target = query.get("target_uid", ["unknown"])[0]
            self._send_json({"status": "INTERACTION_RECORDED", "target": target})

        else:
            super().do_GET()

    def _send_json(self, data, code=200):
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data, indent=2).encode("utf-8"))

    def log_message(self, format, *args):
        pass

class ReusableServer(socketserver.TCPServer):
    allow_reuse_address = True

if __name__ == "__main__":
    with ReusableServer(("", PORT), CathedralHandler) as httpd:
        print(f"[+] Server started on http://localhost:{PORT}")
        httpd.serve_forever()
