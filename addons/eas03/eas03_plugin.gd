@tool
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
