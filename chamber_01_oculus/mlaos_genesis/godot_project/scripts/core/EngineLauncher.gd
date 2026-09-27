extends SceneTree

func _initialize() -> void:
    print("[CATHE-LAUNCHER] Initializing Cathedral-Engine Headless/Windowed Runtime...")
    var root_node = Node.new()
    root_node.name = "RootManifold"
    root.add_child(root_node)
    
    var bootstrap_script = load("res://scripts/core/CathedralSceneBootstrap.gd")
    if bootstrap_script:
        var bootstrap_node = bootstrap_script.new()
        root_node.add_child(bootstrap_node)
        print("[CATHE-LAUNCHER] CathedralSceneBootstrap attached successfully.")
    else:
        printerr("[CATHE-LAUNCHER] Failed to load CathedralSceneBootstrap.gd")
