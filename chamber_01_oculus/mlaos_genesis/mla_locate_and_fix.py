import os

# Define an explicit path in your Home directory so it is instantly findable
home_dir = os.path.expanduser("~")
project_root = os.path.join(home_dir, "godot_client")

print(f"[NAVIGATE] Target project directory: {project_root}")

os.makedirs(project_root, exist_ok=True)

# Quick validation file to ensure the folder is registered
marker_path = os.path.join(project_root, "project.godot")
if os.path.exists(marker_path):
    print("[STATUS] project.godot found inside target directory.")
else:
    print("[STATUS] project.godot missing. Re-run bootstrap in this directory.")

print(f"\nCopy this exact path for the Godot Project Manager:\n{project_root}")
