extends Node

func _ready() -> void:
	SovereignInterface.archive_write_request.connect(_on_archive_write_requested)
	print("[Zeke] State Validator daemon online.")

func _on_archive_write_requested(payload: Dictionary) -> void:
	print("[Zeke] Validating payload for Ash Archive stratification: ", payload)
	
	# Safely fetch AshArchive from root at runtime
	var ash_archive = get_node_or_null("/root/AshArchive")
	if ash_archive:
		ash_archive.commit_entry(payload)
	else:
		push_warning("[Zeke] AshArchive Autoload not found at /root/AshArchive.")
