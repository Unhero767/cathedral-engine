extends Node
# AshArchive.gd - Persistent Stratified Ledger

const SAVE_PATH := "user://ash_archive.json"

var archive_entries: Array = []

func _ready() -> void:
	name = "AshArchive"
	_load_archive_from_disk()

## Commits a validated payload to the persistent ledger file
func commit_entry(payload: Dictionary) -> void:
	var entry := {
		"id": archive_entries.size() + 1,
		"timestamp": Time.get_unix_time_from_system(),
		"datetime": Time.get_datetime_string_from_system(true),
		"payload": payload
	}
	
	archive_entries.append(entry)
	_save_archive_to_disk()
	print("[AshArchive] Stratified Entry #%d committed to disk." % entry["id"])

func _save_archive_to_disk() -> void:
	var file := FileAccess.open(SAVE_PATH, FileAccess.WRITE)
	if file:
		var json_string := JSON.stringify(archive_entries, "\t")
		file.store_string(json_string)
		file.close()
	else:
		push_error("[AshArchive] Failed to open %s for writing." % SAVE_PATH)

func _load_archive_from_disk() -> void:
	if not FileAccess.file_exists(SAVE_PATH):
		print("[AshArchive] No existing ledger found. Initializing new Ash Archive.")
		return
		
	var file := FileAccess.open(SAVE_PATH, FileAccess.READ)
	if file:
		var content := file.get_as_text()
		file.close()
		
		var json := JSON.new()
		var parse_result := json.parse(content)
		if parse_result == OK and json.data is Array:
			archive_entries = json.data
			print("[AshArchive] Loaded %d entries from disk." % archive_entries.size())
		else:
			push_error("[AshArchive] Failed to parse JSON archive from disk.")
