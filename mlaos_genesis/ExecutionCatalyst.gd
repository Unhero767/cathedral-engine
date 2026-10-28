extends Node

var ui_state_manager: Node = null

func _ready() -> void:
    # Attempt to resolve UIStateManager relative to root
    ui_state_manager = get_node_or_null("/root/CathedralRoot/UIStateManager")
    
    if ui_state_manager == null:
        print("[EXECUTION CATALYST]: UIStateManager node not found in scene tree. Queuing deferred fallback instance...")
        ui_state_manager = Node.new()
        ui_state_manager.name = "UIStateManager"
        
        # Safely queue child addition to avoid tree-setup locking errors
        var root_node = get_node("/root/CathedralRoot")
        if root_node:
            root_node.call_deferred("add_child", ui_state_manager)
            print("[EXECUTION CATALYST]: Fallback UIStateManager successfully queued via call_deferred.")

    # Safe call verification
    if ui_state_manager and ui_state_manager.has_method("transition_to"):
        ui_state_manager.transition_to("INITIALIZED")
    else:
        print("[EXECUTION CATALYST]: Cathedral-Engine operational loop active. Ready for IPC telemetry.")
