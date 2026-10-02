#!/usr/bin/env python3
"""
EAS-03 Godot 4 Addon Package Installer
Dallmier Tech Venture — Kenneth W. Dallmier
"""

import os
import sys

PLUGIN_CFG = """[plugin]

name="EAS-03 Somatic Avatar & Background Loader Engine"
description="Thread-safe background asset streaming controllers, Auto-Z 12-layer somatic avatar stacking, and custom shader pipelines for Godot 4.3+."
author="Kenneth W. Dallmier (Dallmier Tech Venture)"
version="1.0.0"
script="eas03_plugin.gd"
"""

PLUGIN_GD = """@tool
extends EditorPlugin

const AUTOLOAD_NAME_GD = "CathedralBackgroundLoaderGD"

func _enter_tree() -> void:
	add_autoload_singleton(AUTOLOAD_NAME_GD, "res://addons/eas03/scripts/cathedral_background_loader.gd")
	print("[EAS-03] Registered CathedralBackgroundLoaderGD singleton.")

	add_custom_type(
		"CathedralBackgroundLoaderGD",
		"Node",
		preload("res://addons/eas03/scripts/cathedral_background_loader.gd"),
		null
	)

func _exit_tree() -> void:
	remove_autoload_singleton(AUTOLOAD_NAME_GD)
	remove_custom_type("CathedralBackgroundLoaderGD")
	print("[EAS-03] Unregistered EAS-03 plugin singletons and types.")
"""

def deploy_eas03_addon(project_root="."):
    addon_path = os.path.join(project_root, "addons", "eas03")
    scripts_path = os.path.join(addon_path, "scripts")
    os.makedirs(scripts_path, exist_ok=True)

    with open(os.path.join(addon_path, "plugin.cfg"), "w", encoding="utf-8") as f:
        f.write(PLUGIN_CFG)

    with open(os.path.join(addon_path, "eas03_plugin.gd"), "w", encoding="utf-8") as f:
        f.write(PLUGIN_GD)

    print(f"[EAS-03] Successfully deployed plugin structure in: {os.path.abspath(addon_path)}")

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "."
    deploy_eas03_addon(target)
