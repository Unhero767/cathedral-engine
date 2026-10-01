// ====================================================================
// MLAOS-Prime :: Quake-Style Console Glassmorphism Shader
// ====================================================================
shader_type canvas_item;

uniform sampler2D screen_texture : hint_screen_texture, filter_linear_mipmap;
uniform float blur_amount : hint_range(0.0, 5.0) = 2.5;
uniform vec4 tint_color : source_color = vec4(0.047, 0.051, 0.063, 0.85); // Obsidian Dark

void fragment() {
    // Sample the screen texture with a mipmap LOD for optimized blurring
    vec3 blurred = textureLod(screen_texture, SCREEN_UV, blur_amount).rgb;
    
    // Mix the blurred background with the Cathedral Obsidian tint
    COLOR.rgb = mix(blurred, tint_color.rgb, tint_color.a);
    COLOR.a = 1.0;
}
