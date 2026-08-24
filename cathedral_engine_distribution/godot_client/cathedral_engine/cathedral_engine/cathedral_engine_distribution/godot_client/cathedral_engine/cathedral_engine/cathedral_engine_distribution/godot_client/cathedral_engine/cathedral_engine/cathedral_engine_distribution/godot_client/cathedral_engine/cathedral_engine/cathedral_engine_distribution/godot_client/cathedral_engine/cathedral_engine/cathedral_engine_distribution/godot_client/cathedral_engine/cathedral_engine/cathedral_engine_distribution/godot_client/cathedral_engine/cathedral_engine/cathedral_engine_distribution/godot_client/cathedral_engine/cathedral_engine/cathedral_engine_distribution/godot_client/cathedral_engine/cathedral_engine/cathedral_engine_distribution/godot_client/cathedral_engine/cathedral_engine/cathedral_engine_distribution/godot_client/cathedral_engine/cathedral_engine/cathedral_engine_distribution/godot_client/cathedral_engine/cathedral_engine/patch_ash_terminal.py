import re
import sys

SERVER_FILE = "server.py"

with open(SERVER_FILE, "r", encoding="utf-8") as f:
    code = f.read()

TERMINAL_LOGIC = '''        elif action in ("ENGAGE_ASH_TERMINAL", "ACCESS_TERMINAL", "EXAMINE_TERMINAL", "ENGAGE_TERMINAL"):
            if hasattr(self, "action_log"):
                self.action_log.append(f"[ASH_TERMINAL] Synchronized Deep Stratum Repository at ({x}, {y}) [130.81 Hz].")
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
'''

if 'elif action in ("ENGAGE_ASH_TERMINAL", "ACCESS_TERMINAL", "EXAMINE_TERMINAL", "ENGAGE_TERMINAL"):' not in code:
    target = 'return {\n            "status": "INTERACTION_RECORDED"'
    if target in code:
        code = code.replace(target, TERMINAL_LOGIC + '        ' + target)
        print("[+] Injected ENGAGE_ASH_TERMINAL logic into GameLoopEngine.")
    else:
        idx = code.find("class CathedralHTTPHandler")
        if idx != -1:
            code = code[:idx] + TERMINAL_LOGIC + "\n\n" + code[idx:]
            print("[+] Appended TERMINAL_LOGIC before CathedralHTTPHandler.")

try:
    compile(code, SERVER_FILE, "exec")
    with open(SERVER_FILE, "w", encoding="utf-8") as f:
        f.write(code)
    print("[+] server.py verified and saved.")
except Exception as e:
    print(f"[-] Compilation error: {e}")
    sys.exit(1)
