import os

PROJECT_ROOT = "./godot_client"

FILES = {
    "project.godot": """[application]

config/name="MLAOS Isometric Cathedral"
run/main_scene="res://scenes/MainWorld.tscn"
config/features=PackedStringArray("4.3", "Compatibility")
config/icon="res://icon.svg"

[autoload]

MrLaos="*res://scripts/core/mr_laos.gd"
AshArchive="*res://scripts/core/ash_archive.gd"
AshSanctity="*res://scripts/core/ash_sanctity.gd"

[display]

window/size/viewport_width=640
window/size/viewport_height=360
window/stretch/mode="canvas_items"

[rendering]

textures/canvas_textures/default_texture_filter=0
renderer/rendering_method="compatibility"
2d/snap/use_pixel_snap=true
""",

    "scripts/core/mr_laos.gd": """extends Node

enum SpectralConstant { GOLD_JOY, BLUE_SORROW, TEAL_CURIOSITY, RED_ANGER, VIOLET_FEAR, EMERALD_LOVE, BRONZE_NULL }

var current_frequency: SpectralConstant = SpectralConstant.TEAL_CURIOSITY

func _ready() -> void:
    print("MrLaos: Sovereign Interface online. Frequency set to Teal/Curiosity.")

func register_harmonic_scar(context: String) -> void:
    print("MrLaos [Harmonic Scar Crystallized]: %s" % context)
    if Engine.has_singleton("AshArchive") or get_node_or_null("/root/AshArchive"):
        var archive = get_node_or_null("/root/AshArchive")
        if archive and archive.has_method("append_entry"):
            archive.append_entry({"type": "harmonic_scar", "context": context})
""",

    "scenes/MainWorld.tscn": """[gd_scene load_steps=3 format=3]

[ext_resource type="PackedScene" path="res://scenes/CatPlayer.tscn" id="1_player"]

[node name="MainWorld" type="Node2D"]
y_sort_enabled = true

[node name="CatPlayer" parent="." instance=ExtResource("1_player")]
position = Vector2(320, 180)
""",

    "scenes/CatPlayer.tscn": """[gd_scene load_steps=4 format=3]

[ext_resource type="Script" path="res://scripts/entities/cat_player.gd" id="1_cat"]

[sub_resource type="PlaceholderTexture2D" id="PlaceholderTexture2D_cat"]
size = Vector2(16, 16)

[sub_resource type="CapsuleShape2D" id="CapsuleShape2D_1"]
radius = 4.0
height = 12.0

[node name="CatPlayer" type="CharacterBody2D"]
y_sort_enabled = true
script = ExtResource("1_cat")

[node name="Sprite2D" type="Sprite2D" parent="."]
position = Vector2(0, -8)
texture = SubResource("PlaceholderTexture2D_cat")

[node name="CollisionShape2D" type="CollisionShape2D" parent="."]
rotation = 1.5708
shape = SubResource("CapsuleShape2D_1")
""",

    "scripts/entities/cat_player.gd": """extends CharacterBody2D

@export var speed: float = 100.0
@onready var sprite: Sprite2D = $Sprite2D

func _physics_process(_delta: float) -> void:
    var direction := Vector2.ZERO
    direction.x = Input.get_axis("ui_left", "ui_right")
    direction.y = Input.get_axis("ui_up", "ui_down")
    
    if direction != Vector2.ZERO:
        direction = direction.normalized()
        velocity = direction * speed
    else:
        velocity = velocity.move_toward(Vector2.ZERO, speed)
        
    move_and_slide()
"""
}

def main():
    for rel_path, content in FILES.items():
        full_path = os.path.join(PROJECT_ROOT, rel_path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, "w") as f:
            f.write(content)
        print(f"[BOOTSTRAP] Injected -> {full_path}")
    print("\n[COMPLETE] Foundation generated. Open './godot_client' inside the Godot 4 Project Manager.")

if __name__ == "__main__":
    main()
