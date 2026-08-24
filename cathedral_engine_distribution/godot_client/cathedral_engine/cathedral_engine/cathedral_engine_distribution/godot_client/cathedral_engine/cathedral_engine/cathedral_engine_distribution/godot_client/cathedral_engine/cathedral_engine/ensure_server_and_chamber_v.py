import re
import subprocess
import time
import urllib.request
import json
import sys

SERVER_FILE = "server.py"

with open(SERVER_FILE, "r", encoding="utf-8") as f:
    code = f.read()

# Define Chamber V manifest dictionary structure if not already present
CHAMBER_V_SNIPPET = '''
            5: {
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
            },
'''

# Check if chamber 5 is missing in the chambers dictionary
if "5: {" not in code and '"chamber_id": 5' not in code:
    # Inject before the end of self.chambers dict or default dictionary
    pattern = r'(4:\s*\{[\s\S]*?\},)'
    if re.search(pattern, code):
        code = re.sub(pattern, r'\1' + CHAMBER_V_SNIPPET, code, count=1)
        print("[+] Registered Chamber V manifest in self.chambers dictionary.")
    
with open(SERVER_FILE, "w", encoding="utf-8") as f:
    f.write(code)

# Verify compilation
try:
    compile(code, SERVER_FILE, "exec")
    print("[+] server.py syntax validated successfully.")
except Exception as e:
    print(f"[-] Syntax error in server.py: {e}")
    sys.exit(1)

# Kill any existing processes on 5050 and relaunch server.py
subprocess.run("lsof -ti:5050 | xargs kill -9 2>/dev/null || true", shell=True)
proc = subprocess.Popen([sys.executable, SERVER_FILE], stdout=open("server.log", "a"), stderr=subprocess.STDOUT)
print(f"[+] server.py launched with PID {proc.pid}. Waiting for socket initialization...")
time.sleep(2.0)
