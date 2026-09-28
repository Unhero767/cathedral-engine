import re
import sys

SERVER_FILE = "server.py"

with open(SERVER_FILE, "r", encoding="utf-8") as f:
    lines = f.readlines()

# 1. Strip any corrupted handle_interaction lines
clean_lines = []
skip = False
for line in lines:
    if "def handle_interaction" in line:
        skip = True
        continue
    if skip:
        # Check if we exited the method definition (new class or top-level def)
        if line.startswith("class ") or (line.startswith("def ") and not line.startswith("    ")):
            skip = False
        elif line.startswith("    def ") or line.startswith("    class "):
            skip = False
        else:
            continue
    clean_lines.append(line)

code = "".join(clean_lines)

# 2. Add handle_interaction method to GameLoopEngine class with proper indentation
method_code = '''
    def handle_interaction(self, params):
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

# Find the end of GameLoopEngine definition (right before CathedralHTTPHandler)
pos = code.find("class CathedralHTTPHandler")
if pos != -1:
    code = code[:pos] + method_code + "\n\n" + code[pos:]
else:
    code += "\n" + method_code

# 3. Test compilation
try:
    compile(code, SERVER_FILE, "exec")
    with open(SERVER_FILE, "w", encoding="utf-8") as f:
        f.write(code)
    print("[+] server.py syntax is valid and successfully saved!")
except Exception as e:
    print(f"[-] Compilation error: {e}")
    # Print lines around the error
    lines_err = code.split("\n")
    for i, l in enumerate(lines_err[440:480], start=441):
        print(f"{i:4d}: {l}")
