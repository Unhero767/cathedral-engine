import re
import sys

SERVER_FILE = "server.py"

with open(SERVER_FILE, "r", encoding="utf-8") as f:
    code = f.read()

INSCRIPTION_LOGIC = '''        elif action in ("ENGAGE_INSCRIPTION_NODE", "INSCRIPTION"):
            if hasattr(self, "action_log"):
                self.action_log.append(f"[SANCTUM] Inscribed Harmonic Scar Matrix at ({x}, {y}) [78.2 Hz].")
            return {
                "status": "SCAR_CALIBRATED",
                "target_uid": target_uid,
                "coordinates": {"x": x, "y": y},
                "resonance_hz": 78.2,
                "data_stream": "STRATA_VIOLET_GOLD_04",
                "content": "PARACONSISTENT_LOGIC_MATRIX_ALIGNMENT_COMPLETE",
                "insight_reward": 250,
                "scar_alignment": "LOCKED",
                "spectral_constant": "Violet-Gold",
                "apex_gateway": "UNSEALED"
            }
'''

if 'elif action in ("ENGAGE_INSCRIPTION_NODE", "INSCRIPTION"):' not in code and 'elif action == "ENGAGE_INSCRIPTION_NODE":' not in code:
    # Anchor before the final fallback return in handle_interaction
    target = 'return {\n            "status": "INTERACTION_RECORDED"'
    if target in code:
        code = code.replace(target, INSCRIPTION_LOGIC + '        ' + target)
        print("[+] Injected ENGAGE_INSCRIPTION_NODE logic.")
    else:
        # Fallback anchor before CathedralHTTPHandler
        idx = code.find("class CathedralHTTPHandler")
        if idx != -1:
            code = code[:idx] + INSCRIPTION_LOGIC + "\n\n" + code[idx:]
            print("[+] Appended INSCRIPTION_LOGIC.")

try:
    compile(code, SERVER_FILE, "exec")
    with open(SERVER_FILE, "w", encoding="utf-8") as f:
        f.write(code)
    print("[+] server.py syntax validated and saved successfully.")
except Exception as e:
    print(f"[-] Compilation error: {e}")
    sys.exit(1)
