shader_type spatial;
render_mode blend_mix, depth_draw_opaque, cull_back, diffuse_burley, specular_schlick_ggx;

// ==============================================================================
// 32-BIT HD-2D HIGH-CONTRAST CHIAROSCURO & DITHERING FRAGMENT PIPELINE
// ==============================================================================

uniform sampler2D albedo_texture : source_color, filter_nearest;
uniform sampler2D normal_texture : hint_normal;
uniform vec4 primary_substrate : source_color = vec4(0.05, 0.05, 0.07, 1.0); // #0D0D11
uniform vec4 neon_accent : source_color = vec4(0.0, 1.0, 0.8, 1.0);       // Teal/Curiosity Flare
uniform float color_bit_depth : hint_range(4.0, 32.0) = 16.0;
uniform float dithering_strength : hint_range(0.0, 0.1) = 0.03;

// Bayer 4x4 Dithering Matrix for retro 32-bit hardware constraints modernized
const float bayer_matrix[16] = {
    0.0/16.0,  8.0/16.0,  2.0/16.0, 10.0/16.0,
   12.0/16.0,  4.0/16.0, 14.0/16.0,  6.0/16.0,
    3.0/16.0, 11.0/16.0,  1.0/16.0,  9.0/16.0,
   15.0/16.0,  7.0/16.0, 13.0/16.0,  5.0/16.0
};

void fragment() {
    vec2 uv = UV;
    
    // Sample base textures with hard pixel snapping (HD-2D visual clarity)
    vec4 tex_color = texture(albedo_texture, uv);
    
    // Apply 2.5D planar parallax / normal mapping
    NORMAL_MAP = texture(normal_texture, uv).rgb;
    
    // Quantize color depth to emulate 32-bit hardware palettes
    vec3 quantized = floor(tex_color.rgb * color_bit_depth) / color_bit_depth;
    
    // Apply Bayer dithering pattern across shadow gradients
    int x = int(mod(FRAGCOORD.x, 4.0));
    int y = int(mod(FRAGCOORD.y, 4.0));
    int index = x + y * 4;
    float limit = bayer_matrix[index];
    
    quantized += (limit - 0.5) * dithering_strength;
    
    // Chiaroscuro high-contrast crush
    vec3 final_color = mix(primary_substrate.rgb, quantized, max(tex_color.a, 0.2));
    
    // Inject Neon Spectral Flare (Teal/Crimson Biomechanical Highlights)
    float luminance = dot(final_color, vec3(0.299, 0.587, 0.114));
    if (luminance < 0.15) {
        final_color = mix(final_color, neon_accent.rgb, step(0.92, texture(albedo_texture, uv).r) * 0.7);
    }

    ALBEDO = final_color;
    ROUGHNESS = 0.85;
    SPECULAR = 0.1;
}
// ==============================================================================
// END OF FILE: HD2DPixelShader.gdshader
// ==============================================================================
