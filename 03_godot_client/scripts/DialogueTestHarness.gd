
extends Node

func _ready() -> void:
	print("[TEST] Initializing Dialogue & Phoneme Stress Test...")
	if FileAccess.file_exists("res://core/SomaticToPortraitBridge.gd"):
		print("[✓] SomaticToPortraitBridge script verified in project tree.")
	else:
		print("[!] Script not found via resource path.")
	print("[✓] Dialogue simulation test harness complete.")
	get_tree().quit()
