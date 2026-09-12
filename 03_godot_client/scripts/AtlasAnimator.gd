extends Sprite2D

@export var frame_size: int = 128
@export var total_frames: int = 32
@export var animation_fps: float = 8.0

var current_frame: float = 0.0

func _ready() -> void:
    # Load the PNG directly at runtime, bypassing static import cache errors
    var img := Image.new()
    var path := "res://assets/portraits/master_atlas_strip.png"
    if not FileAccess.file_exists(path) and FileAccess.file_exists("res://aurelia9_atlas_strip.png"):
        path = "res://aurelia9_atlas_strip.png"
    if img.load(path) == OK:
        texture = ImageTexture.create_from_image(img)
        region_enabled = true
        region_rect = Rect2(0, 0, frame_size, frame_size)
    else:
        print("ERROR: Failed to load atlas strip at runtime from: ", path)

func _process(delta: float) -> void:
    current_frame = fmod(current_frame + animation_fps * delta, float(total_frames))
    var f_idx = int(current_frame)
    region_rect = Rect2(f_idx * frame_size, 0, frame_size, frame_size)
