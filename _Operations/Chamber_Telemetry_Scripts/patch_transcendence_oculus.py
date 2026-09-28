import re
import sys

SERVER_FILE = "server.py"

with open(SERVER_FILE, "r", encoding="utf-8") as f:
    code = f.read()

OCULUS_LOGIC = '''        elif action in ("ENGAGE_OCULUS", "ENTER_OCULUS", "ACTIVATE_OCULUS"):
            if hasattr(self, "action_log"):
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
'''

if 'elif action in ("ENGAGE_OCULUS", "ENTER_OCULUS", "ACTIVATE_OCULUS"):' not in code:
    target = 'return {\n            "status": "INTERACTION_RECORDED"'
    if target in code:
        code = code.replace(target, OCULUS_LOGIC + '        ' + target)
        print("[+] Injected ENGAGE_OCULUS logic into GameLoopEngine.")
    else:
        idx = code.find("class CathedralHTTPHandler")
        if idx != -1:
            code = code[:idx] + OCULUS_LOGIC + "\n\n" + code[idx:]
            print("[+] Appended OCULUS_LOGIC before CathedralHTTPHandler.")

try:
    compile(code, SERVER_FILE, "exec")
    with open(SERVER_FILE, "w", encoding="utf-8") as f:
        f.write(code)
    print("[+] server.py verified and saved.")
except Exception as e:
    print(f"[-] Compilation error: {e}")
    sys.exit(1)
