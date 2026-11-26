# ChoirGland.gd
# Law of Texture: Cymatic Acoustic Resonance & Terrain Material Projections
class_name ChoirGland extends Node2D

signal terrain_material_projected(material_type: String, world_radius: float)
signal cymatic_frequency_emitted(frequency_hz: float, spectral_constant: String)

enum MaterialProjection {
	OBSIDIAN_SLATE, # High density, zero friction, reflection
	MERCURY_FLUID,   # Ultra-low friction, slip acceleration
	BRONZE_STATIC,   # Maximum poise, high traction
	GOLD_LAMINATE    # Coherent sacred ground, healing
}

var current_material: MaterialProjection = MaterialProjection.GOLD_LAMINATE
var active_projection_radius: float = 64.0

func project_material(material: MaterialProjection, radius: float = 64.0) -> void:
	current_material = material
	active_projection_radius = radius
	
	var mat_name = "GOLD_LAMINATE"
	var freq = 580.0
	var spec = SpectralConstants.THETA
	
	match material:
		MaterialProjection.OBSIDIAN_SLATE:
			mat_name = "OBSIDIAN_SLATE"
			freq = 0.0
			spec = SpectralConstants.NULL_CONST
		MaterialProjection.MERCURY_FLUID:
			mat_name = "MERCURY_FLUID"
			freq = 510.0
			spec = SpectralConstants.PSI
		MaterialProjection.BRONZE_STATIC:
			mat_name = "BRONZE_STATIC"
			freq = 460.0
			spec = SpectralConstants.DELTA
		MaterialProjection.GOLD_LAMINATE:
			mat_name = "GOLD_LAMINATE"
			freq = 580.0
			spec = SpectralConstants.THETA
			
	emit_signal("terrain_material_projected", mat_name, radius)
	emit_signal("cymatic_frequency_emitted", freq, spec)
	queue_redraw()

func _draw() -> void:
	var col = Color(0.855, 0.647, 0.125, 0.2)
	draw_circle(Vector2.ZERO, active_projection_radius, col)
	draw_arc(Vector2.ZERO, active_projection_radius, 0, TAU, 32, col * 2.0, 1.5)
