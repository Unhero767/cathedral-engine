extends Control

@export var portrait_path: NodePath = NodePath("PortraitViewportContainer/CathedralAvatarPortrait")

func _ready() -> void:
	var portrait = get_node_or_null(portrait_path)
	if not portrait:
		# Fallback search if direct path fails
		portrait = find_child("CathedralAvatarPortrait", true, false)
		
	if portrait and portrait.has_method("setup_from_texture"):
		var default_tex = null
		if ResourceLoader.exists("res://assets/default_avatar.png"):
			default_tex = load("res://assets/default_avatar.png")
		else:
			# Generate a 64x64 procedural placeholder texture to prevent null errors
			var img = Image.create(64, 64, false, Image.FORMAT_RGBA8)
			img.fill(Color(0.2, 0.15, 0.25, 1.0))
			default_tex = ImageTexture.create_from_image(img)
			
		portrait.setup_from_texture(default_tex)
		print("[✓] CathedralAvatarHarness initialized portrait successfully.")
