"""
GDScript injector for updating the 32-frame atlas region rect dynamically.
"""

script_content = """extends Sprite2D

@export var frame_size: int = 128
@export var total_frames: int = 32
@export var animation_fps: float = 8.0

var current_frame: float = 0.0

func _process(delta: float) -> void:
    current_frame = fmod(current_frame + animation_fps * delta, float(total_frames))
    var f_idx = int(current_frame)
    region_rect = Rect2(f_idx * frame_size, 0, frame_size, frame_size)
"""

print("Atlas animator script template prepared for Godot integration.")
