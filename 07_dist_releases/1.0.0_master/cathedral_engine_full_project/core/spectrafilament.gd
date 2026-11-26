# Spectrafilament.gd
# Unit Cell Phase Storage & Tendon-Cable Dynamics (Young's Modulus & Transductive Tension)
class_name Spectrafilament extends Node2D

# Structural Properties
@export var anchor_a: Vector2 = Vector2.ZERO
@export var anchor_b: Vector2 = Vector2(0, 100)
@export var spectral_constant: String = SpectralConstants.THETA
@export var rest_length: float = 100.0
@export var damping: float = 0.85

var current_length: float = 100.0
var tension: float = 0.0
var strain: float = 0.0
var phase_angle: float = 0.0
var unit_cell_vertices: PackedVector2Array = []

func _ready() -> void:
	_generate_unit_cell_geometry()

func _generate_unit_cell_geometry() -> void:
	unit_cell_vertices.clear()
	var steps = 8
	var radius = 6.0
	for i in range(steps):
		var angle = (float(i) / float(steps)) * TAU
		unit_cell_vertices.append(Vector2(cos(angle) * radius, sin(angle) * radius))

func _physics_process(delta: float) -> void:
	var diff = anchor_b - anchor_a
	current_length = diff.length()
	strain = (current_length - rest_length) / maxf(rest_length, 1.0)
	
	# Young's Modulus Y(rho) calculation via SpectralConstants
	var mat_props = SpectralConstants.calculate_material_property({spectral_constant: 1.0})
	var youngs_modulus: float = mat_props["rigidity"] * 100.0
	
	# Stress sigma = Y * strain
	var stress = youngs_modulus * strain
	tension = maxf(0.0, stress * damping)
	
	# Phase accumulation
	phase_angle = fmod(phase_angle + (tension * 0.05 + 1.0) * delta, TAU)
	queue_redraw()

func _draw() -> void:
	var color = SpectralConstants.get_spectral_color(spectral_constant)
	var glow_color = color
	glow_color.a = clampf(0.4 + tension * 0.01, 0.4, 0.95)
	
	# Draw main tension cable
	draw_line(anchor_a, anchor_b, glow_color, 2.5, true)
	
	# Draw unit cells along the cable
	var mid = (anchor_a + anchor_b) * 0.5
	var normal = (anchor_b - anchor_a).normalized().orthogonal()
	var wave_offset = normal * sin(phase_angle) * (4.0 + tension * 0.05)
	
	draw_circle(mid + wave_offset, 3.5, color)
	draw_line(mid, mid + wave_offset, Color(1, 1, 1, 0.6), 1.0)

func apply_impulse(force_vector: Vector2) -> void:
	anchor_b += force_vector
