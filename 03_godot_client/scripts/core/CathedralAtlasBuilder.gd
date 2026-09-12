class_name CathedralAtlasBuilder
extends RefCounted

static func build_atlas_region(id: String) -> Rect2:
    return Rect2(0, 0, 64, 64)

static func build_sprite_frames(texture: Texture2D) -> SpriteFrames:
    var sf := SpriteFrames.new()
    var states = [&"liturgical_idle", &"liturgical_chant", &"liturgical_resonance"]
    
    for state in states:
        if not sf.has_animation(state):
            sf.add_animation(state)
            sf.set_animation_speed(state, 8.0)
            sf.set_animation_loop(state, true)
            
            # Create a default frame rect from the texture dimensions or fallback to 64x64 slices
            var tex_width = texture.get_width() if texture else 64
            var tex_height = texture.get_height() if texture else 64
            
            var atlas_tex := AtlasTexture.new()
            atlas_tex.atlas = texture
            atlas_tex.region = Rect2(0, 0, min(tex_width, 64), min(tex_height, 64))
            sf.add_frame(state, atlas_tex)
            
    return sf
