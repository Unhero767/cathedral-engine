class_name CathedralAvatarHarness
extends Node

const PortraitScript = preload("res://CathedralAvatarPortrait.gd")

@onready var somatic_engine = $CathedralSomaticEngine
@onready var portrait_controller = $PortraitViewportContainer/CathedralAvatarPortrait
@onready var somatic_bridge = $SomaticToPortraitBridge

func _ready() -> void:
	var atlas_tex := PortraitScript.load_texture_safe("res://assets/portraits/master_atlas_strip.png")
	if atlas_tex and portrait_controller:
		portrait_controller.setup_from_texture(atlas_tex)
		
	var dna_path := "res://archetypes/crucible_templar.dna"
	if FileAccess.file_exists(dna_path) and somatic_engine:
		var f := FileAccess.open(dna_path, FileAccess.READ)
		somatic_engine.load_dna_buffer(f.get_buffer(512))
		
	if somatic_bridge:
		somatic_bridge.synchronize_bridge()
