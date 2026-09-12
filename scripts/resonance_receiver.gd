extends Node

@onready var animation_player: AnimationPlayer = get_node_or_null("../ScalePulseRoot/AnimationPlayer")
@onready var shader_overlay: ColorRect = get_node_or_null("../PostProcessingLayer/ShaderScreenOverlay")

func _ready() -> void:
    var orchestrator = get_node_or_null("../StateOrchestrator")
    if orchestrator:
        orchestrator.connect("telemetry_broadcast", Callable(self, "_on_telemetry_received"))

func _on_telemetry_received(metric_name: String, value: float) -> void:
    match metric_name:
        "speed":
            if animation_player:
                animation_player.speed_scale = value
        "aberration":
            if shader_overlay and shader_overlay.material is ShaderMaterial:
                shader_overlay.material.set_shader_parameter("chromatic_aberration_amount", value)
        "depth_steps":
            if shader_overlay and shader_overlay.material is ShaderMaterial:
                shader_overlay.material.set_shader_parameter("color_depth_steps", value)
