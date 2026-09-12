extends Node

@onready var viewport_container: SubViewportContainer =get_node("../SubViewportContainer")

func _ready() -> void:
    if viewport_container:
        # Enforce strict Nearest-neighbor scaling for monastic pixel preservation
        viewport_container.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
