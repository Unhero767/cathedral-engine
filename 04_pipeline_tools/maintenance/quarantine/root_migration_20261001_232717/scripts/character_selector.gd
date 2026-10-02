extends Control

@onready var orchestrator = get_node_or_null("../StateOrchestrator")
@onready var avatar_rect: TextureRect = $AvatarRect
@onready var name_label: Label = $NameLabel
@onready var select_button: Button = $SelectButton

func _ready() -> void:
    set_anchors_preset(Control.PRESET_LEFT_WIDE)
    custom_minimum_size = Vector2(300, 600)
    
    if select_button and not select_button.pressed.is_connected(_on_select_button_pressed):
        select_button.pressed.connect(_on_select_button_pressed)
        
    if orchestrator:
        orchestrator.transition_to(orchestrator.SystemState.ARMED)

func _on_select_button_pressed() -> void:
    if orchestrator:
        orchestrator.transition_to(orchestrator.SystemState.ACTIVE)
        print("SELECTOR: Entity Mr. Laos / Sovereign Interface selected. Resonance frequency locked.")
