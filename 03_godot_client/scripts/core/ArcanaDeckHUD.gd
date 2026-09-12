extends CanvasLayer

@onready var container: HBoxContainer = $ScrollContainer/HBoxContainer
@export var active_hand_ids: Array[int] = [1, 2, 11, 12, 15, 21, 25, 31, 35, 40]

func _ready() -> void:
	_populate_hand()

func _populate_hand() -> void:
	if not container:
		return
	for child in container.get_children():
		child.queue_free()
		
	for cid in active_hand_ids:
		var card_btn = ArcanaCardUI.new()
		card_btn.card_id = cid
		container.add_child(card_btn)
