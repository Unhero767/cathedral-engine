import re

SERVER_FILE = "server.py"

with open(SERVER_FILE, "r", encoding="utf-8") as f:
    code = f.read()

# 1. Clean out previously broken injections of handle_interaction
code = re.sub(r'def handle_interaction\(self, params\):[\s\S]*?(?=\n\n(?:def|class|$))', '', code)

# 2. Define clean method with 4-space indentation
CLEAN_HANDLE_INTERACTION = '''    def handle_interaction(self, params):
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

# 3. Inject inside GameLoopEngine right after __init__
init_match = re.search(r'(class GameLoopEngine[\s\S]*?def __init__\(self[^\)]*\):[\s\S]*?\n(?=    def |\nclass ))', code)
if init_match:
    idx = init_match.end()
    code = code[:idx] + "\n" + CLEAN_HANDLE_INTERACTION + "\n" + code[idx:]
    print("[+] Placed handle_interaction inside GameLoopEngine.")
else:
    # Append to end of class GameLoopEngine before CathedralHTTPHandler
    handler_idx = code.find("class CathedralHTTPHandler")
    if handler_idx != -1:
        code = code[:handler_idx] + CLEAN_HANDLE_INTERACTION + "\n\n" + code[handler_idx:]
        print("[+] Inserted handle_interaction before CathedralHTTPHandler.")

# 4. Verify syntax
try:
    compile(code, "server.py", "exec")
    with open(SERVER_FILE, "w", encoding="utf-8") as f:
        f.write(code)
    print("[+] Syntax verified. server.py saved successfully.")
except Exception as e:
    print("[-] Syntax check failed:", e)
    # Save debug copy
    with open("server.py.err", "w", encoding="utf-8") as f:
        f.write(code)
