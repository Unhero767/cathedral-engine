import os
import shutil
import glob

base_dir = os.getcwd()
if os.path.basename(base_dir) == "cathedral_integration_pipeline":
    base_dir = os.path.dirname(base_dir)

print(f"[Fixer] Working in root: {base_dir}")

# 1. Find the actual godot_client directory
found_dirs = glob.glob(os.path.join(base_dir, "**/godot_client"), recursive=True)
target_root_client = os.path.join(base_dir, "godot_client")

src_dir = None
for d in found_dirs:
    if d != target_root_client and os.path.isdir(d):
        src_dir = d
        break

if src_dir and os.path.exists(src_dir):
    print(f"[Fixer] Found source client at: {src_dir}")
    os.makedirs(target_root_client, exist_ok=True)
    for item in os.listdir(src_dir):
        # Do not copy nested project.godot to avoid conflicting project definitions
        if item == "project.godot":
            continue
        s_path = os.path.join(src_dir, item)
        d_path = os.path.join(target_root_client, item)
        if os.path.isdir(s_path):
            shutil.copytree(s_path, d_path, dirs_exist_ok=True)
        else:
            shutil.copy2(s_path, d_path)
    print(f"[Fixer] Copied client assets to root: {target_root_client}")
else:
    # If not found in subfolder, search for individual scripts
    print("[Fixer] Searching for individual missing scripts...")
    os.makedirs(target_root_client, exist_ok=True)
    for fname in ["CathedralSync.gd", "ChamberV.gd", "ResonanceScreen.gdshader"]:
        matches = glob.glob(os.path.join(base_dir, f"/**/{fname}"), recursive=True)
        if matches:
            shutil.copy2(matches[0], os.path.join(target_root_client, fname))
            print(f"  * Linked {fname} -> godot_client/{fname}")

# 2. Ensure placeholder fallbacks exist if any file is still missing
placeholders = {
    "CathedralSync.gd": """extends Node
# Autoload singleton for Cathedral Engine state synchronization
func _ready():
    print("[CathedralSync] Substrate synchronized.")
""",
    "ChamberV.gd": """extends Node
# Chamber V Narrative and Quest State Controller
func _ready():
    print("[ChamberV] Controller active.")
""",
    "ResonanceScreen.gdshader": """shader_type canvas_item;
render_mode blend_mix, unshaded;
uniform float u_resonance_gain : hint_range(0.0, 2.0) = 1.0;
void fragment() {
    vec4 color = texture(TEXTURE, UV);
    COLOR = color;
}
"""
}

for fname, default_code in placeholders.items():
    fpath = os.path.join(target_root_client, fname)
    if not os.path.exists(fpath):
        with open(fpath, "w", encoding="utf-8") as f:
            f.write(default_code)
        print(f"[Fixer] Created fallback asset: godot_client/{fname}")

# 3. Remove nested project.godot in subfolders to stop Godot from ignoring folders
for pfile in glob.glob(os.path.join(base_dir, "**/project.godot"), recursive=True):
    if pfile != os.path.join(base_dir, "project.godot"):
        bak_file = pfile + ".disabled"
        os.rename(pfile, bak_file)
        print(f"[Fixer] Disabled conflicting sub-project file: {pfile}")

print("\n[Fixer] Godot project structure repaired successfully.")
