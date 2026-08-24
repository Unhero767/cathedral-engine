import re

SERVER_FILE = "server.py"

with open(SERVER_FILE, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Add interact handler to GameLoopEngine if missing
INTERACT_METHOD = '''    def handle_interaction(self, params):
        action = params.get("action", "EXAMINE")
        target_uid = params.get("target_uid", "unknown")
        x = int(params.get("x", 2))
        y = int(params.get("y", 4))
        spectrum = params.get("spectrum", "Blue")

        if action in ("EXAMINE_CONSTRUCT", "EXAMINE"):
            return {
                "status": "CONSTRUCT_EXAMINED",
                "target_uid": target_uid,
                "coordinates": {"x": x, "y": y},
                "resonance_hz": 65.4,
                "state": "UNLOCKED_AEROSTATIC_CORE",
                "description": "Massive aerostatic manifold column humming at 65.4 Hz (Blue Constant). Dampeners standing by for alignment."
            }
        elif action in ("ENGAGE_COLUMN_REGULATOR", "ENGAGE"):
            if hasattr(self, "action_log"):
                self.action_log.append(f"[CONSTRUCT] Aerostatic Manifold {target_uid} calibrated to 65.4 Hz.")
            return {
                "status": "AEROSTATIC_COLUMN_ENGAGED",
                "target_uid": target_uid,
                "duct_pressure_psi": 14.7,
                "damping_ratio": 1.0,
                "resonance_phase": "SYNCHRONIZED_65.4_HZ",
                "carrier_hz": 65.4,
                "insight_reward": 80,
                "corridor_east": "PRESSURIZED",
                "terminal_strata_blue": "ACCESSIBLE"
            }
        return {
            "status": "INTERACTION_RECORDED",
            "action": action,
            "target_uid": target_uid
        }
'''

if "def handle_interaction" not in content:
    match = re.search(r"(class GameLoopEngine[\s\S]*?def __init__[\s\S]*?\n\n)", content)
    if match:
        content = content[:match.end()] + INTERACT_METHOD + "\n" + content[match.end():]
        print("[+] Added handle_interaction to GameLoopEngine.")
    else:
        content = content.replace("class CathedralHTTPHandler", INTERACT_METHOD + "\n\nclass CathedralHTTPHandler")
        print("[+] Appended handle_interaction before CathedralHTTPHandler.")

# 2. Add route mapping in CathedralHTTPHandler do_GET
ROUTE_BLOCK = '''        elif path == "/api/rpg/interact":
            query_dict = {k: v[0] for k, v in query_components.items()} if "query_components" in locals() else {}
            if not query_dict and "?" in self.path:
                import urllib.parse
                qs = self.path.split("?", 1)[1]
                query_dict = {k: v[0] for k, v in urllib.parse.parse_qs(qs).items()}
            res = GAME_LOOP.handle_interaction(query_dict) if hasattr(GAME_LOOP, "handle_interaction") else {"status": "SUCCESS", "action": "INTERACT"}
            self._send_json(res)
            return
'''

if 'elif path == "/api/rpg/interact":' not in content:
    content = content.replace('elif path == "/api/rpg/move":', ROUTE_BLOCK + '        elif path == "/api/rpg/move":')
    print("[+] Registered /api/rpg/interact route in CathedralHTTPHandler.")

with open(SERVER_FILE, "w", encoding="utf-8") as f:
    f.write(content)

print("[+] server.py patched successfully.")
