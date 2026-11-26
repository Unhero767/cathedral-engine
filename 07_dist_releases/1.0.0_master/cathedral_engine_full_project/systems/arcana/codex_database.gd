# CodexDatabase.gd
# 40-Book Catalog Manager across 4 Strata (Prime Foundations, Inner Mandala, Outer Choirs, Inner Shadow Canon)
class_name CodexDatabase extends Node

signal codex_loaded(total_books: int)
signal book_unlocked(book_id: int, title: String)

const DATABASE_PATH: String = "res://data/codex_database.json"

var books: Array = []
var book_by_id: Dictionary = {} # int -> Dictionary
var book_by_stratum: Dictionary = {
	"Prime Foundations": [],
	"Inner Mandala": [],
	"Outer Choirs": [],
	"Inner Shadow Canon": []
}

func _ready() -> void:
	load_codex()

func load_codex() -> bool:
	if not FileAccess.file_exists(DATABASE_PATH):
		push_warning("[CodexDatabase] JSON file not found at " + DATABASE_PATH)
		return false
		
	var file = FileAccess.open(DATABASE_PATH, FileAccess.READ)
	var content = file.get_as_text()
	file.close()
	
	var json = JSON.new()
	var err = json.parse(content)
	if err != OK:
		push_error("[CodexDatabase] Failed to parse JSON: " + json.get_error_message())
		return false
		
	var data = json.get_data()
	if typeof(data) == TYPE_ARRAY:
		books = data
	elif typeof(data) == TYPE_DICTIONARY and data.has("books"):
		books = data["books"]
		
	# Index books
	book_by_id.clear()
	for s in book_by_stratum.keys():
		book_by_stratum[s].clear()
		
	for b in books:
		var id = int(b.get("id", 0))
		book_by_id[id] = b
		var stratum = b.get("stratum", "Prime Foundations")
		if book_by_stratum.has(stratum):
			book_by_stratum[stratum].append(b)
			
	emit_signal("codex_loaded", books.size())
	print("[CodexDatabase] Loaded ", books.size(), " books across 4 strata.")
	return true

func get_book(book_id: int) -> Dictionary:
	if book_by_id.has(book_id):
		return book_by_id[book_id]
	return {}

func get_books_by_stratum(stratum: String) -> Array:
	if book_by_stratum.has(stratum):
		return book_by_stratum[stratum]
	return []

func get_all_books() -> Array:
	return books
