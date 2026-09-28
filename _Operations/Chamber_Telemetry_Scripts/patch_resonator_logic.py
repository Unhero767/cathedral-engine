import re
import sys

SERVER_FILE = "server.py"

with open(SERVER_FILE, "r", encoding="utf-8") as f:
    code = f.read()

RESONATOR_LOGIC = '''        elif action in ("TUNE_DIALETHEIC_LATTICE", "COUPLE_RESONATOR", "TUNE_RESONATOR"):
            if hasattr(self, "action_log"):
                self.action_log.append(f"[LATTICE] Coupled Dialetheic Resonator {target_uid} at ({x}, {y}) to Violet-Gold dual carrier.")
            return {
                "status": "DIALETHEIC_LATTICE_COUPLED",
                "target_uid": target_uid,
                "coordinates": {"x": x, "y": y},
                "coupled_frequencies": {
                    "primary_violet_hz": 78.2,
                    "secondary_gold_hz": 104.8
                },
                "dialetheic_state": "SUPERPOSITION_LOCKED",
                "truth_value": "BOTH",
                "harmonic_efficiency": 1.0,
                "insight_reward": 175,
                "conduit_alpha": "ACTIVE_RESONANCE"
            }
'''

if 'elif action in ("TUNE_DIALETHEIC_LATTICE", "COUPLE_RESONATOR", "TUNE_RESONATOR"):' not in code:
    target = 'return {\n            "status": "INTERACTION_RECORDED"'
    if target in code:
        code = code.replace(target, RESONATOR_LOGIC + '        ' + target)
        print("[+] Injected TUNE_DIALETHEIC_LATTICE logic.")
    else:
        idx = code.find("class CathedralHTTPHandler")
        if idx != -1:
            code = code[:idx] + RESONATOR_LOGIC + "\n\n" + code[idx:]
            print("[+] Appended RESONATOR_LOGIC.")

try:
    compile(code, SERVER_FILE, "exec")
    with open(SERVER_FILE, "w", encoding="utf-8") as f:
        f.write(code)
    print("[+] server.py verified and saved.")
except Exception as e:
    print(f"[-] Compilation error: {e}")
    sys.exit(1)
