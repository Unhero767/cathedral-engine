import re
import sys

SERVER_FILE = "server.py"

with open(SERVER_FILE, "r", encoding="utf-8") as f:
    code = f.read()

ANCHOR_LOGIC = '''        elif action in ("TUNE_SOMATIC_PILLAR", "ALIGN_ANCHOR", "TUNE_ANCHOR"):
            if hasattr(self, "action_log"):
                self.action_log.append(f"[SANCTUM] Aligned Somatic Anchor {target_uid} at ({x}, {y}) to 130.81 Hz Gold-Obsidian carrier.")
            return {
                "status": "SOMATIC_PILLAR_ALIGNED",
                "target_uid": target_uid,
                "coordinates": {"x": x, "y": y},
                "fundamental_carrier_hz": 130.81,
                "spectral_constant": "Gold-Obsidian / Revelatory Null Matrix",
                "somatic_flux": "BIOLOGICAL_GROUNDING_LOCKED",
                "dPhi_dt": 1.618,
                "harmonic_mode": "OCTAVE_OCTET_NORTH_POLAR",
                "insight_reward": 220,
                "monad_circuit_state": "NORTH_POLAR_ANCHOR_ENGAGED"
            }
'''

if 'elif action in ("TUNE_SOMATIC_PILLAR", "ALIGN_ANCHOR", "TUNE_ANCHOR"):' not in code:
    target = 'return {\n            "status": "INTERACTION_RECORDED"'
    if target in code:
        code = code.replace(target, ANCHOR_LOGIC + '        ' + target)
        print("[+] Injected TUNE_SOMATIC_PILLAR logic into GameLoopEngine.")
    else:
        idx = code.find("class CathedralHTTPHandler")
        if idx != -1:
            code = code[:idx] + ANCHOR_LOGIC + "\n\n" + code[idx:]
            print("[+] Appended ANCHOR_LOGIC before CathedralHTTPHandler.")

try:
    compile(code, SERVER_FILE, "exec")
    with open(SERVER_FILE, "w", encoding="utf-8") as f:
        f.write(code)
    print("[+] server.py syntax validated and saved.")
except Exception as e:
    print(f"[-] Compilation error: {e}")
    sys.exit(1)
