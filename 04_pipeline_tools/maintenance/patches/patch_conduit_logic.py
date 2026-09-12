import re
import sys

SERVER_FILE = "server.py"

with open(SERVER_FILE, "r", encoding="utf-8") as f:
    code = f.read()

CONDUIT_LOGIC = '''        elif action in ("ENGAGE_CONDUIT", "ENGAGE_COLLECTOR", "ACTIVATE_CONDUIT"):
            if hasattr(self, "action_log"):
                self.action_log.append(f"[CONDUIT] Engaged Aureate Gold Collector {target_uid} at ({x}, {y}) [104.8 Hz].")
            return {
                "status": "CONDUIT_ACTIVATED",
                "target_uid": target_uid,
                "coordinates": {"x": x, "y": y},
                "resonance_hz": 104.8,
                "spectral_constant": "Gold / Joy / Revelatory Synthesis",
                "flux_density": "88.4 W/m²",
                "power_grid_state": "SYNCHRONIZED_WITH_APEX_GATEWAY",
                "insight_reward": 200,
                "apex_gateway_charge": "100%"
            }
'''

if 'elif action in ("ENGAGE_CONDUIT", "ENGAGE_COLLECTOR", "ACTIVATE_CONDUIT"):' not in code:
    target = 'return {\n            "status": "INTERACTION_RECORDED"'
    if target in code:
        code = code.replace(target, CONDUIT_LOGIC + '        ' + target)
        print("[+] Injected ENGAGE_CONDUIT logic into GameLoopEngine.")
    else:
        idx = code.find("class CathedralHTTPHandler")
        if idx != -1:
            code = code[:idx] + CONDUIT_LOGIC + "\n\n" + code[idx:]
            print("[+] Appended CONDUIT_LOGIC before CathedralHTTPHandler.")

try:
    compile(code, SERVER_FILE, "exec")
    with open(SERVER_FILE, "w", encoding="utf-8") as f:
        f.write(code)
    print("[+] server.py verified and saved.")
except Exception as e:
    print(f"[-] Compilation error: {e}")
    sys.exit(1)
