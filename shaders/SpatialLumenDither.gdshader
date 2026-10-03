// File: shaders/SpatialLumenDither.gdshader
// Spatial Display Shader bound to read-only projection parameters.
shader_type spatial;
render_mode unshaded, blend_mix, depth_draw_opaque, cull_back;

uniform vec4 u_albedo : source_color = vec4(0.85, 0.75, 0.45, 1.0); // Gold Joy baseline
uniform float kenomic_entropy : hint_range(0.0, 100.0) = 0.0;
uniform int belnap_fog_level : hint_range(0, 2) = 0;
uniform float u_emission_multiplier = 8.5;

// Bayer 2x2 Matrix for Bio-Semantic Dithering
const mat2 BAYER_2X2 = mat2(
    vec2(0.00, 0.50),
    vec2(0.75, 0.25)
);

void fragment() {
    vec2 screen_pos = mod(floor(FRAGCOORD.xy), 2.0);
    float dither_val = BAYER_2X2[int(screen_pos.x)][int(screen_pos.y)];
    
    float entropy_factor = clamp(kenomic_entropy / 100.0, 0.0, 1.0);
    vec3 base_lum = u_albedo.rgb * (u_emission_multiplier * 0.15);
    
    if (belnap_fog_level > 0) {
        base_lum *= mix(1.0, dither_val, float(belnap_fog_level) * 0.4 * entropy_factor);
    }
    
    ALBEDO = base_lum;
}
