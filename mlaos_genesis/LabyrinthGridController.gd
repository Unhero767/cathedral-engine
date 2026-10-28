extends Node3D
class_name LabyrinthGridController

var spatial_matrix = {}

func register_hazard(grid_x: int, grid_z: int, hazard_type: String) -> void:
    var coordinate = Vector2(grid_x, grid_z)
    spatial_matrix[coordinate] = hazard_type
    
func evaluate_traversal(target_x: int, target_z: int, asset_class: String) -> bool:
    var target = Vector2(target_x, target_z)
    if spatial_matrix.has(target):
        var hazard = spatial_matrix[target]
        if hazard == "ANTI_MAGIC_ZONE" and asset_class in ["Sorcerer", "Wizard"]:
            push_error("Traversal Lock: Arcane integrity compromised.")
            return false
    return true
