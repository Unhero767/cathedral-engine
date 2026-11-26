# SanctuaryDefenses.gd
# Vesper Decoys, Filigree Severance, and Harmonic Scar Barriers
class_name SanctuaryDefenses extends Node2D

signal decoy_deployed(position: Vector2, duration: float)
signal filigree_severed(lattice_id: String)
signal barrier_reinforced(barrier_id: String, health_added: float)

var active_decoys: Array = []
var active_barriers: Array = []

func deploy_vesper_decoy(pos: Vector2, duration: float = 8.0) -> Dictionary:
	var decoy = {
		"position": pos,
		"duration": duration,
		"time_left": duration,
		"attraction_radius": 150.0
	}
	active_decoys.append(decoy)
	emit_signal("decoy_deployed", pos, duration)
	return decoy

func sever_filigree(lattice_id: String) -> void:
	emit_signal("filigree_severed", lattice_id)
	if AFieldManager:
		AFieldManager.stabilize_field(0.8)

func _physics_process(delta: float) -> void:
	for i in range(active_decoys.size() - 1, -1, -1):
		active_decoys[i]["time_left"] -= delta
		if active_decoys[i]["time_left"] <= 0.0:
			active_decoys.remove_at(i)
