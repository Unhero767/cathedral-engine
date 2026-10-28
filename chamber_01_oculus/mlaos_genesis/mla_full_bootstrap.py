import os

# Explicitly target the Home directory for effortless discovery in Godot
PROJECT_ROOT = os.path.expanduser("~/godot_client")

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
    var archive = get_node_or_null("/root/AshArchive")
    if archive and archive.has_method("append_entry"):
        archive.append_entry({"type": "harmonic_scar", "context": context})
""",

    "scripts/core/ash_archive.gd": """extends Node

var archive_entries: Array = []

func append_entry(payload: Dictionary) -> void:
    var entry := {
        "entry_id": archive_entries.size(),
        "timestamp": Time.get_unix_time_from_system(),
        "payload": payload
    }
    archive_entries.append(entry)
    print("AshArchive: Recorded entry #%d" % entry["entry_id"])

func save_archive() -> void:
    var file = FileAccess.open("user://ash_archive.save", FileAccess.WRITE)
    if file:
        file.store_string(JSON.stringify(archive_entries))
        print("AshArchive: State persisted to disk.")
""",

    "scripts/core/ash_sanctity.gd": """extends Node

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
    for method_name in ["save_archive", "_save_archive", "save_to_disk", "_save"]:
        if _archive.has_method(method_name):
            _archive.call(method_name)
            return
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
"""
}

def main():
    print(f"[BOOTSTRAP] Constructing project root at: {PROJECT_ROOT}")
    for rel_path, content in FILES.items():
        full_path = os.path.join(PROJECT_ROOT, rel_path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, "w") as f:
            f.write(content)
        print(f" -> Injected: {rel_path}")

    print("\n==================================================")
    print("SUCCESS: Full Cathedral architecture bootstrapped.")
    print(f"Directory path to import in Godot: {PROJECT_ROOT}")
    print("==================================================")

if __name__ == "__main__":
    main()
