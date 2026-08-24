import re

SERVER_FILE = "server.py"

with open(SERVER_FILE, "r", encoding="utf-8") as f:
    code = f.read()

# Logic to inject terminal access
TERMINAL_LOGIC = '''        elif action == "ACCESS_TERMINAL":
            if hasattr(self, "action_log"):
                self.action_log.append(f"[ARCHIVE] Decrypting blue strata data from {target_uid}.")
            return {
                "status": "ARCHIVE_DECRYPTED",
                "data_stream": "STRATA_BLUE_01",
                "content": "PNEUMATIC_VALVE_SEQUENCE_ALPHA_BETA_SYNC",
                "insight_reward": 150,
                "access_level": "BLUE_CONSTANT_GRANTED"
            }'''

if 'elif action == "ACCESS_TERMINAL"' not in code:
    # Insert before the final return statement of handle_interaction
    code = re.sub(r'(\s+return \{\n\s+"status": "INTERACTION_RECORDED")', TERMINAL_LOGIC + r'\1', code)
    
    with open(SERVER_FILE, "w", encoding="utf-8") as f:
        f.write(code)
    print("[+] Patched server.py with terminal access logic.")
else:
    print("[+] Terminal logic already present.")
