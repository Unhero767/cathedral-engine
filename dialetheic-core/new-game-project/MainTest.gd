extends Node

var arcana: ArcanaEngine

func _ready() -> void:
	print("\n--- CHAPTER X: ARCANA ENGINE TEST ---")
	
	arcana = ArcanaEngine.new()
	add_child(arcana)
	
	# Execute Arcana I (The First Cantor - Gold Constant)
	arcana.draw_card("I_THE_FIRST_CANTOR")
	
	# Execute Arcana XXXII (The Fossilized Paradox - Null Constant)
	arcana.draw_card("XXXII_FOSSILIZED_PARADOX")
	
	print("--- CHAPTER X TEST COMPLETE ---\n")
