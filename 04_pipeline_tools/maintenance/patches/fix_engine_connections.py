import os
import re
import ast
import shutil

ENGINE_CONFIGS = [
    ("engines/campaign_engine.py", "_get_conn"),
    ("engines/character_creation_engine.py", "_get_conn"),
    ("engines/dialogue_engine.py", "_get_conn"),
    ("engines/progression_engine.py", "_get_conn"),
    ("engines/save_manager.py", "_get_conn"),
    ("engines/ledger_engine.py", "_get_connection"),
]

def restore_and_patch(filepath, conn_func_name):
    # 1. Restore from original backup if available
    bak_path = filepath + ".bak"
    if os.path.exists(bak_path):
        shutil.copyfile(bak_path, filepath)
    elif not os.path.exists(filepath):
        print(f"[-] File not found: {filepath}")
        return

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # 2. Add contextmanager import
    if "from contextlib import contextmanager" not in content:
        if "import sqlite3" in content:
            content = content.replace("import sqlite3", "import sqlite3\nfrom contextlib import contextmanager")
        else:
            content = "from contextlib import contextmanager\n" + content

    # 3. Replace _get_conn / _get_connection with the generator context manager
    pattern = rf'def {conn_func_name}\(self.*?\):.*?(?=\n    def |\n\s*$|\Z)'
    replacement = f"""@contextmanager
    def {conn_func_name}(self):
        conn = sqlite3.connect(str(self.db_path), timeout=30.0)
        try:
            yield conn
            conn.commit()
        finally:
            conn.close()"""

    patched = re.sub(pattern, replacement, content, flags=re.DOTALL)

    try:
        ast.parse(patched)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(patched)
        print(f"[+] Successfully patched @contextmanager: {filepath} ({conn_func_name})")
    except SyntaxError as e:
        print(f"[!] AST parse failed for {filepath}: {e}")

if __name__ == "__main__":
    print("=== Restoring & Applying @contextmanager to Cathedral Engines ===")
    for path, func in ENGINE_CONFIGS:
        restore_and_patch(path, func)
    print("=== Patching Complete ===")
