import re

SERVER_FILE = "server.py"
with open(SERVER_FILE, "r", encoding="utf-8") as f:
    code = f.read()

# Add handle_interaction method to GameLoopEngine if not present
if "def handle_interaction" not in code:
    method_code = '''    def handle_interaction(self, params):
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
        return {"status": "INTERACTION_RECORDED", "action": action, "target_uid": target_uid}
'''
    # Insert right before class CathedralHTTPHandler
    idx = code.find("class CathedralHTTPHandler")
    if idx != -1:
        code = code[:idx] + method_code + "\n\n" + code[idx:]
        print("[+] Injected handle_interaction into GameLoopEngine.")

# Ensure route dispatch in do_GET matches /api/rpg/interact
if 'parsed_path.path == "/api/rpg/interact"' not in code and 'path == "/api/rpg/interact"' not in code:
    route_handler = '''        elif parsed_path.path == "/api/rpg/interact" or path == "/api/rpg/interact":
            import urllib.parse
            qs = parsed_path.query if "parsed_path" in locals() else (self.path.split("?", 1)[1] if "?" in self.path else "")
            q_dict = {k: v[0] for k, v in urllib.parse.parse_qs(qs).items()}
            res = GAME_LOOP.handle_interaction(q_dict) if hasattr(GAME_LOOP, "handle_interaction") else {"status": "SUCCESS"}
            self._send_json(res)
            return
'''
    # Find insertion anchor
    if "elif parsed_path.path ==" in code:
        code = re.sub(r'(elif parsed_path\.path == "[^"]+":)', route_handler + r'\1', code, count=1)
    elif "elif path ==" in code:
        code = re.sub(r'(elif path == "[^"]+":)', route_handler + r'\1', code, count=1)
    print("[+] Mapped /api/rpg/interact endpoint.")

with open(SERVER_FILE, "w", encoding="utf-8") as f:
    f.write(code)

print("[+] server.py updated.")
