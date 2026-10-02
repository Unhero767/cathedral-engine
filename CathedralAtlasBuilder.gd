# ==============================================================================
# CathedralAtlasBuilder.gd
# Programmatic 4096x128 Master Strip Slicer into 6 Liturgical SpriteFrames
# Governed by: Book VIII (EAS-03 Master Texture Strip Architecture)
# ==============================================================================
class_name CathedralAtlasBuilder
extends RefCounted

const FRAME_WIDTH: int = 128
const FRAME_HEIGHT: int = 128
const TOTAL_FRAMES: int = 32

const LITURGICAL_CYCLES: Dictionary = {
	"liturgical_idle": {"start_col": 0, "count": 4, "fps": 6.0, "loop": true},
	"lumen_pulse": {"start_col": 4, "count": 6, "fps": 8.0, "loop": true},
	"ocular_surge": {"start_col": 10, "count": 6, "fps": 10.0, "loop": true},
	"harmonic_resonance": {"start_col": 16, "count": 8, "fps": 8.0, "loop": true},
	"dialetheic_shift": {"start_col": 24, "count": 4, "fps": 6.0, "loop": true},
	"penitent_recitation": {"start_col": 28, "count": 4, "fps": 8.0, "loop": true}
}

static func build_sprite_frames(master_strip: Texture2D) -> SpriteFrames:
	assert(master_strip != null, "Master strip texture cannot be null.")
	var frames: SpriteFrames = SpriteFrames.new()

	for anim_name in LITURGICAL_CYCLES.keys():
		var cfg: Dictionary = LITURGICAL_CYCLES[anim_name]
		var start_col: int = cfg["start_col"]
		var count: int = cfg["count"]
		var fps: float = cfg["fps"]
		var loop: bool = cfg["loop"]

		if not frames.has_animation(anim_name):
			frames.add_animation(anim_name)

		frames.set_animation_speed(anim_name, fps)
		frames.set_animation_loop(anim_name, loop)

		for i in range(count):
			var col_idx: int = start_col + i
			var atlas_tex: AtlasTexture = AtlasTexture.new()
			atlas_tex.atlas = master_strip
			atlas_tex.region = Rect2(col_idx * FRAME_WIDTH, 0, FRAME_WIDTH, FRAME_HEIGHT)
			atlas_tex.filter_clip = true
			frames.add_frame(anim_name, atlas_tex)

	print("[CathedralAtlasBuilder] Built SpriteFrames with 6 liturgical animations from 4096x128 master strip.")
	return frames
