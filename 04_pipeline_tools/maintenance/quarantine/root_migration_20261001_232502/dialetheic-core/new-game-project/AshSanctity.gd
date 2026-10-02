extends Node

## SANCTITY LAYER — standalone watcher.
## Seals the Ash Archive with a hash chain without editing AshArchive.gd.

const CANONICAL_KEYS := ["entry_id", "timestamp", "payload", "prev_hash"]
const GENESIS_HASH := "GENESIS"

var _archive = null
var _known_count := 0


func _ready() -> void:
	_archive = get_node_or_null("/root/AshArchive")
	if _archive:
		_known_count = _archive.archive_entries.size()
		var patched := seal_pending()
		if patched > 0:
			print("AshSanctity: sealed %d legacy entries." % patched)
	print("AshSanctity: chain integrity = %s" % str(verify_chain()))

func _process(_delta: float) -> void:
	if _archive == null:
		_archive = get_node_or_null("/root/AshArchive")
		if _archive == null:
			return

	var count: int = _archive.archive_entries.size()
	if count != _known_count:
		seal_pending()
		_known_count = count


func seal_pending() -> int:
	if _archive == null:
		return 0

	var entries: Array = _archive.archive_entries
	var patched := 0
	var prev := GENESIS_HASH

	for entry in entries:
		if entry.has("hash"):
			prev = str(entry.get("hash"))
			continue

		entry["prev_hash"] = prev
		entry["hash"] = compute_entry_hash(entry)
		patched += 1
		prev = str(entry.get("hash"))

	if patched > 0:
		_persist()

	return patched


func verify_chain() -> bool:
	if _archive == null:
		return false

	var prev := GENESIS_HASH

	for entry in _archive.archive_entries:
		if str(entry.get("prev_hash")) != prev:
			return false
		if str(entry.get("hash")) != compute_entry_hash(entry):
			return false
		prev = str(entry.get("hash"))

	return true


func compute_entry_hash(entry: Dictionary) -> String:
	var canonical := {}
	for key in CANONICAL_KEYS:
		canonical[key] = entry.get(key)

	var text := JSON.stringify(canonical, "", true)

	var ctx := HashingContext.new()
	ctx.start(HashingContext.HASH_SHA256)
	ctx.update(text.to_utf8_buffer())
	return ctx.finish().hex_encode()


func _persist() -> void:
	# Try the likely names of your save routine.
	for method_name in ["save_archive", "_save_archive", "save_to_disk", "_save"]:
		if _archive.has_method(method_name):
			_archive.call(method_name)
			return
	# If none match, no harm: hashes are deterministic and will be
	# recomputed identically on every launch until you tell me the
	# true save-method name.
