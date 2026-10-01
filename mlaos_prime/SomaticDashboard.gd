extends CanvasLayer
# ====================================================================
# MLAOS-Prime :: Somatic Telemetry Dashboard Controller
# ====================================================================

@onready var ego_val = $MarginContainer/PanelContainer/VBoxContainer/MarginContainer/GridContainer/EgoValue
@onready var coherence_val = $MarginContainer/PanelContainer/VBoxContainer/MarginContainer/GridContainer/CoherenceValue
@onready var scars_val = $MarginContainer/PanelContainer/VBoxContainer/MarginContainer/GridContainer/ScarsValue

func _ready() -> void:
    # Connect to the SomaticStateMachine signals
    var state_machine = get_tree().root.get_node_or_null("MasterWorld/SomaticController")
    if state_machine:
        state_machine.telemetry_updated.connect(_on_telemetry_updated)
        state_machine.ledger_updated.connect(_on_ledger_updated)

func _on_telemetry_updated(density: float, coherence: float) -> void:
    ego_val.text = "%.2f kg/m³" % density
    coherence_val.text = "%.2f" % coherence

func _on_ledger_updated(scar_count: int) -> void:
    scars_val.text = str(scar_count)
