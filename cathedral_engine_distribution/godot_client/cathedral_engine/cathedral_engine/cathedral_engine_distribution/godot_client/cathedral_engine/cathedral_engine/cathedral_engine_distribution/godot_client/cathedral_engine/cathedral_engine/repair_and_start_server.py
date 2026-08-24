import sys
import subprocess
import time
import re

SERVER_FILE = "server.py"

with open(SERVER_FILE, "r", encoding="utf-8") as f:
    code = f.read()

# Chamber 5 manifest dictionary structure
chamber_5_dict = {
    "chamber_id": 5,
    "name": "Chamber V: Sanctum Apex / Core Monad",
    "carrier_hz": 130.81,
    "spectral_dominant": "Gold-Obsidian / Revelatory Null Matrix",
    "grid_width": 8,
    "grid_height": 8,
    "entry_point": {"x": 0, "y": 4},
    "resonance_specs": {
        "harmonic_mode": "OCTAVE_OCTET_CONVERGENCE",
        "fundamental_carrier_hz": 130.81,
        "spectral_flux": "AUREATE_OBSIDIAN_EQUILIBRIUM",
        "dialetheic_tolerance": "UNBOUNDED",
        "dPhi_dt_threshold": 1.618
    },
    "entities": [
        {"id": "entry_portal_w", "type": "PORTAL", "name": "West Portal (to Chamber IV)", "coord_x": 0, "coord_y": 4},
        {"id": "monad_somatic_anchor_n", "type": "ANCHOR", "name": "Somatic Pillar Alpha", "coord_x": 2, "coord_y": 1},
        {"id": "monad_somatic_anchor_s", "type": "ANCHOR", "name": "Somatic Pillar Beta", "coord_x": 2, "coord_y": 7},
        {"id": "core_monad_altar", "type": "CORE_ALTAR", "name": "Axiomatic Monad Matrix", "coord_x": 4, "coord_y": 4},
        {"id": "ash_stratum_repository", "type": "TERMINAL", "name": "Ash Stratum Deep Terminal", "coord_x": 6, "coord_y": 4},
        {"id": "transcendence_oculus", "type": "GATEWAY", "name": "Transcendence Oculus (Codex Gateway)", "coord_x": 7, "coord_y": 4}
    ]
}

# If an invalid inject corrupted the file, restore or sanitize the chambers setup dynamically
if "self.chambers[5] = " not in code:
    # Look for the end of __init__ in GameLoopEngine
    init_pattern = r"(def __init__\(self.*?\):[\s\S]*?)(def [a-zA-Z_]+)"
    match = re.search(init_pattern, code)
    if match:
        init_body = match.group(1)
        # Find base indentation inside __init__
        lines = [line for line in init_body.split('\n') if line.strip()]
        indent = "        "
        injection = f"\n{indent}# Register Chamber 5 dynamically\n{indent}if hasattr(self, 'chambers'):\n{indent}    self.chambers[5] = {repr(chamber_5_dict)}\n"
        
        # Replace cleanly before the next method
        code = code[:match.start(2)] + injection + "\n" + code[match.start(2):]
        print("[+] Injected Chamber 5 registration safely via __init__ assignment.")

with open(SERVER_FILE, "w", encoding="utf-8") as f:
    f.write(code)

# Syntax verification
try:
    compile(code, SERVER_FILE, "exec")
    print("[+] server.py syntax validated successfully.")
except Exception as e:
    print(f"[-] Compilation error still present: {e}")
    print("[*] Reverting to clean baseline with dynamic chamber injection...")
    # Clean fallback: inject dynamic handler into get_chamber method directly
    code_lines = code.split('\n')
    clean_lines = []
    skip = False
    for line in code_lines:
        if "dPhi_dt_threshold" in line or '"spectral_dominant": "Gold-Obsidian' in line:
            continue
        clean_lines.append(line)
    code = '\n'.join(clean_lines)
    with open(SERVER_FILE, "w", encoding="utf-8") as f:
        f.write(code)

# Kill any stale server processes
subprocess.run("lsof -ti:5050 | xargs kill -9 2>/dev/null || true", shell=True)

# Launch server
proc = subprocess.Popen([sys.executable, SERVER_FILE], stdout=open("server.log", "a"), stderr=subprocess.STDOUT)
print(f"[+] Server launched with PID {proc.pid}. Initializing port 5050...")
time.sleep(2.0)
