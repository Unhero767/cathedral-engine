@tool
extends TextureRect

@export var avatar_name: String = "Aurelia-9"
@export var sprite_frames: SpriteFrames:
    set(value):
        sprite_frames = value
        _update_frames()

var current_frame: int = 0
var timer: float = 0.0
@export var fps: float = 8.0

func _ready() -> void:
    if sprite_frames and sprite_frames.has_animation("default"):
        _update_frames()

func _process(delta: float) -> void:
    if not sprite_frames or not sprite_frames.has_animation("default"):
        return
    
    timer += delta
    if timer >= (1.0 / fps):
        timer = 0.0
        var frame_count = sprite_frames.get_frame_count("default")
        if frame_count > 0:
            current_frame = (current_frame + 1) % frame_count
            texture = sprite_frames.get_frame_texture("default", current_frame)

func _update_frames() -> void:
    if sprite_frames and sprite_frames.has_animation("default") and sprite_frames.get_frame_count("default") > 0:
        texture = sprite_frames.get_frame_texture("default", 0)

static func load_texture_safe(path: String) -> Texture2D:
    if ResourceLoader.exists(path):
        return load(path) as Texture2D
    return null

func setup_from_texture(tex: Texture2D) -> void:
    if tex:
        texture = tex
