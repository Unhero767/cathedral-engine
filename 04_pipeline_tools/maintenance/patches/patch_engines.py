import os
import re
import ast
import shutil

TARGET_FILES = [
    "engines/campaign_engine.py",
    "engines/ledger_engine.py",
    "engines/character_creation_engine.py",
    "engines/save_manager.py",
    "engines/progression_engine.py",
    "engines/dialogue_engine.py",
    "tests/test_rpg_systems.py"
]

def patch_file(filepath):
    if not os.path.exists(filepath):
        print(f"[-] Skipping (file not found): {filepath}")
        return

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Create safe backup
    shutil.copyfile(filepath, filepath + ".bak")

    lines = content.splitlines()
    out = []
    
    has_closing = "from contextlib import closing" in content
    added_closing = False
    
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # Ensure contextlib.closing is imported
        if not has_closing and not added_closing and line.strip().startswith("import sqlite3"):
            out.append(line)
            out.append("from contextlib import closing")
            added_closing = True
            i += 1
            continue
            
        # Match 'conn = sqlite3.connect(...)'
        m = re.match(r'^(\s*)conn\s*=\s*sqlite3\.connect\((.+)\)\s*$', line)
        if m and "closing(" not in line:
            indent = m.group(1)
            target = m.group(2)
            out.append(f"{indent}with closing(sqlite3.connect({target})) as conn:")
            
            # Indent all subsequent statements in this function scope by 4 spaces
            i += 1
            while i < len(lines):
                next_line = lines[i]
                if not next_line.strip():
                    out.append(next_line)
                    i += 1
                    continue
                
                next_indent_len = len(next_line) - len(next_line.lstrip())
                if next_indent_len <= len(indent) and (next_line.strip().startswith("def ") or next_line.strip().startswith("class ") or next_line.strip().startswith("@")):
                    # Reached next function/class boundary
                    break
                
                out.append("    " + next_line)
                i += 1
            continue
        else:
            out.append(line)
            i += 1
            
    patched_code = "\n".join(out) + "\n"

    # Validate syntax before saving
    try:
        ast.parse(patched_code)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(patched_code)
        print(f"[+] Successfully patched: {filepath}")
    except SyntaxError as e:
        print(f"[!] Syntax validation failed for {filepath}: {e}. Restoring backup.")
        shutil.copyfile(filepath + ".bak", filepath)

if __name__ == "__main__":
    print("=== Patching SQLite Connection Handles in Cathedral Engines ===")
    for path in TARGET_FILES:
        patch_file(path)
    print("=== Patching Complete ===")
