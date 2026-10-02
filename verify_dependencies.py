#!/usr/bin/env python3
import os
import sys
import importlib
import re

REPO_ROOT = "/users/kennethdallmier/cathedral_engine"
LOGIC_DIR = os.path.join(REPO_ROOT, "02_engine_core", "logic_engines")
GODOT_DIR = os.path.join(REPO_ROOT, "03_godot_client")
GODOT_PROJECT = os.path.join(GODOT_DIR, "project.godot")

print("=" * 65)
print("CATHEDRAL-ENGINE DEPENDENCY INTEGRITY AUDIT")
print("=" * 65)

# ---------------------------------------------------------
# 1. AUDIT PYTHON LOGIC ENGINES
# ---------------------------------------------------------
print("\n[1/3] Testing Python Logic Engines (02_engine_core/logic_engines)...")
sys.path.insert(0, LOGIC_DIR)
sys.path.insert(0, os.path.join(REPO_ROOT, "02_engine_core"))

engine_modules = [
    "arcana_engine", "campaign_engine", "chamber_generator",
    "character_creation_engine", "codex_engine", "dialogue_engine",
    "eas03_engine", "emotional_physics_engine", "enemy_engine",
    "game_loop_engine", "ledger_engine", "manifest_engine",
    "oracle_engine", "paraconsistent_engine", "progression_engine",
    "quantum_gravity_engine", "save_manager", "universe_atlas_engine"
]

passed_py = 0
for mod_name in engine_modules:
    py_path = os.path.join(LOGIC_DIR, f"{mod_name}.py")
    if not os.path.exists(py_path):
        print(f"  ❌ Missing file: {py_path}")
        continue
    try:
        importlib.import_module(mod_name)
        passed_py += 1
        print(f"  ✓ {mod_name}.py imported cleanly")
    except Exception as e:
        print(f"  ❌ {mod_name}.py import error: {e}")

print(f"-> Logic Engines Passed: {passed_py}/{len(engine_modules)}")

# ---------------------------------------------------------
# 2. AUDIT GODOT AUTOLOADS & RES:// PATHS
# ---------------------------------------------------------
print("\n[2/3] Testing Godot 4 Autoloads in 03_godot_client/project.godot...")
if not os.path.exists(GODOT_PROJECT):
    print(f"  ❌ project.godot not found at {GODOT_PROJECT}")
else:
    with open(GODOT_PROJECT, "r", encoding="utf-8") as f:
        content = f.read()

    autoload_section = re.search(r"\[autoload\](.*?)(?=\n\[|\Z)", content, re.DOTALL)
    if not autoload_section:
        print("  ⚠️ No [autoload] section located in project.godot")
    else:
        autoloads = re.findall(r'(\w+)=\"\*?res://([^\"]+)\"', autoload_section.group(1))
        passed_al = 0
        for name, rel_path in autoloads:
            full_path = os.path.join(GODOT_DIR, rel_path)
            if os.path.exists(full_path):
                passed_al += 1
                print(f"  ✓ Autoload '{name}' -> res://{rel_path} resolved")
            else:
                print(f"  ❌ Autoload '{name}' -> res://{rel_path} NOT FOUND at {full_path}")
        print(f"-> Autoloads Resolved: {passed_al}/{len(autoloads)}")

# ---------------------------------------------------------
# 3. AUDIT SCENE EXT_RESOURCE REFERENCES
# ---------------------------------------------------------
print("\n[3/3] Testing Scene ExtResource Script Dependencies...")
scene_dir = os.path.join(GODOT_DIR, "scenes")
scene_files = []
for root, _, files in os.walk(scene_dir):
    for f in files:
        if f.endswith(".tscn"):
            scene_files.append(os.path.join(root, f))

missing_ext = 0
scanned_ext = 0
for sc in scene_files:
    rel_sc = os.path.relpath(sc, GODOT_DIR)
    with open(sc, "r", encoding="utf-8", errors="ignore") as f:
        sc_text = f.read()
    
    matches = re.findall(r'path=\"res://([^\"]+)\"', sc_text)
    for res_path in matches:
        scanned_ext += 1
        target_path = os.path.join(GODOT_DIR, res_path)
        if not os.path.exists(target_path):
            print(f"  ❌ In {rel_sc}: Missing ExtResource -> res://{res_path}")
            missing_ext += 1

if missing_ext == 0:
    print(f"  ✓ All {scanned_ext} ExtResource dependencies in scenes resolve cleanly.")
else:
    print(f"  ⚠️ {missing_ext}/{scanned_ext} ExtResources need path updating.")

print("=" * 65)
print("AUDIT EXECUTION COMPLETE")
print("=" * 65)
