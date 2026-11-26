# ArcanaEngine.gd
# Living Tarot & Narrative Pressure Modulator (22 Major Arcana + 18 Extended Cathedral Arcana)
class_name ArcanaEngine extends Node

signal card_drawn(card: Dictionary, narrative_pressure: float)
signal fate_spread_resolved(cards: Array, destiny_alignment: String)

var narrative_pressure: float = 0.5 # [0.0 - 1.0]
var active_spread: Array = []

# Draw a single Tarot Card based on dynamic K-Index and Somatic Phase
func draw_card() -> Dictionary:
	var books_pool = []
	if CodexDatabase:
		books_pool = CodexDatabase.get_all_books()
		
	if books_pool.is_empty():
		return {"title": "The Fool of Kenoma", "arcana": 0, "pressure": 0.5}
		
	var idx = randi() % books_pool.size()
	var selected_book = books_pool[idx]
	
	var card = {
		"id": selected_book.get("id", idx + 1),
		"title": selected_book.get("title", "Unknown Arcana"),
		"arcana": selected_book.get("arcana", idx),
		"stratum": selected_book.get("stratum", "Prime Foundations"),
		"spectral_constant": selected_book.get("spectral_constant", "THETA"),
		"primary_axiom": selected_book.get("primary_axiom", ""),
		"drawn_pressure": narrative_pressure
	}
	
	# Modulate narrative pressure
	narrative_pressure = clampf(narrative_pressure + (randf() - 0.5) * 0.1, 0.0, 1.0)
	emit_signal("card_drawn", card, narrative_pressure)
	return card

# Draw a 3-Card Trinity Spread (Origin, Paradox, Synthesis)
func draw_trinity_spread() -> Array:
	active_spread.clear()
	for i in range(3):
		active_spread.append(draw_card())
	
	var alignment = "COHERENT_SYNTHESIS"
	if narrative_pressure > 0.75:
		alignment = "DIALETHEIC_COLLISION"
	elif narrative_pressure < 0.25:
		alignment = "LITHIC_PERMINERALIZATION"
		
	emit_signal("fate_spread_resolved", active_spread, alignment)
	return active_spread
