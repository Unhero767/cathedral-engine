import re
import sys

SERVER_FILE = "server.py"

with open(SERVER_FILE, "r", encoding="utf-8") as f:
    code = f.read()

ALTAR_LOGIC = '''        elif action in ("ENGAGE_CORE_ALTAR", "INSCRIBE_MONAD", "ENGAGE_ALTAR"):
            if hasattr(self, "action_log"):
                self.action_log.append(f"[CORE_MONAD] Axiomatic Altar inscribed at ({x}, {y}) [130.81 Hz].")
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
'''

if 'elif action in ("ENGAGE_CORE_ALTAR", "INSCRIBE_MONAD", "ENGAGE_ALTAR"):' not in code:
    target = 'return {\n            "status": "INTERACTION_RECORDED"'
    if target in code:
        code = code.replace(target, ALTAR_LOGIC + '        ' + target)
        print("[+] Injected ENGAGE_CORE_ALTAR logic into GameLoopEngine.")
    else:
        idx = code.find("class CathedralHTTPHandler")
        if idx != -1:
            code = code[:idx] + ALTAR_LOGIC + "\n\n" + code[idx:]
            print("[+] Appended ALTAR_LOGIC before CathedralHTTPHandler.")

try:
    compile(code, SERVER_FILE, "exec")
    with open(SERVER_FILE, "w", encoding="utf-8") as f:
        f.write(code)
    print("[+] server.py verified and saved.")
except Exception as e:
    print(f"[-] Compilation error: {e}")
    sys.exit(1)
