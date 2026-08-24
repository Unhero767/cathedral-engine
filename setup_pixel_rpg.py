import os

print("\n" + "="*70)
print(" CATHEDRAL-ENGINE: CONFIGURING 16-BIT PIXEL ART RPG")
print("="*70 + "\n")

# 1. Update project.godot configuration
project_godot_content = """; Engine configuration file.
; Cathedral-Engine Master Architecture: 16-Bit HD-2D Pixel Art RPG

config_version=5

[application]

config/name="Cathedral Engine - Pixel RPG"
config/description="EAS-03 Cathedral Engine 16-bit Top-Down Action RPG."
config/version="1.0.0"
run/main_scene="res://world/sanctuary_arvonlae.tscn"
config/features=PackedStringArray("4.3", "Forward Plus")
boot_splash/bg_color=Color(0.02, 0.02, 0.03, 1)

[autoload]

SpectralConstants="*res://core/spectral_constants.gd"
DialetheicBuffer="*res://core/dialetheic_buffer.gd"
AFieldManager="*res://core/a_field_manager.gd"
SomaticBaseline="*res://core/somatic_baseline.gd"
AshArchive="*res://core/ash_archive.gd"
HeartOculus="*res://core/heart_oculus.gd"
TriKeyController="*res://systems/tri_key_controller.gd"
CodexDatabase="*res://systems/arcana/codex_database.gd"
ArcanaEngine="*res://systems/arcana/arcana_engine.gd"
CarrierSynthesizer="*res://audio/carrier_synthesizer.gd"

[display]

window/size/viewport_width=1280
window/size/viewport_height=720
window/size/mode=0
window/size/resizable=true
window/stretch/mode="canvas_items"
window/stretch/aspect="keep"

[rendering]

textures/canvas_textures/default_texture_filter=0
renderer/rendering_method="forward_plus"
environment/defaults/default_clear_color=Color(0.02, 0.02, 0.03, 1)

[physics]

common/physics_ticks_per_second=60
common/max_physics_steps_per_frame=8
2d/default_gravity=0.0
2d/default_gravity_vector=Vector2(0, 0)
"""

# Search for the directory containing project.godot
target_dir = None
for root, _, files in os.walk('.'):
    if 'project.godot' in files:
        target_dir = root
        break

if not target_dir:
    target_dir = './godot_client'
    os.makedirs(target_dir, exist_ok=True)

pg_path = os.path.join(target_dir, 'project.godot')
with open(pg_path, 'w', encoding='utf-8') as f:
    f.write(project_godot_content)

print(f"[✓] Successfully configured project file at: {pg_path}")
print("[✓] Main Scene set to: res://world/sanctuary_arvonlae.tscn")
print("[✓] Texture filter locked to Nearest-Neighbor (16-bit crisp pixels)")
print("[✓] 10 Core Singletons wired under [autoload]")
print("\n" + "="*70 + "\n")
