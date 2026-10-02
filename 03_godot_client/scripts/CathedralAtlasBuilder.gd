class_name CathedralAtlasBuilder
extends RefCounted

const FRAME_SIZE := Vector2(128, 128)
const TOTAL_FRAMES := 32

const ANIMATION_DEFINITIONS: Dictionary = {
	&"liturgical_idle": {"start": 0, "count": 4, "fps": 6.0, "loop": true},
	&"lumen_pulse": {"start": 4, "count": 6, "fps": 8.0, "loop": true},
	&"ocular_surge": {"start": 10, "count": 6, "fps": 10.0, "loop": true},
	&"harmonic_resonance": {"start": 16, "count": 8, "fps": 8.0, "loop": true},
	&"dialetheic_shift": {"start": 24, "count": 4, "fps": 6.0, "loop": true},
	&"penitent_recitation": {"start": 28, "count": 4, "fps": 8.0, "loop": true}
}

static func build_sprite_frames(master_texture: Texture2D) -> SpriteFrames:
	var sf := SpriteFrames.new()
	if sf.has_animation(&"default"):
		sf.remove_animation(&"default")
		
	for anim_name: StringName in ANIMATION_DEFINITIONS:
		var def: Dictionary = ANIMATION_DEFINITIONS[anim_name]
		sf.add_animation(anim_name)
		sf.set_animation_speed(anim_name, def["fps"])
		sf.set_animation_loop(anim_name, def["loop"])
		
		var start_idx: int = def["start"]
		var count: int = def["count"]
		for i in range(count):
			var atlas_tex := AtlasTexture.new()
			atlas_tex.atlas = master_texture
			atlas_tex.region = Rect2((start_idx + i) * FRAME_SIZE.x, 0.0, FRAME_SIZE.x, FRAME_SIZE.y)
			atlas_tex.filter_clip = true
			sf.add_frame(anim_name, atlas_tex)
			
	return sf
