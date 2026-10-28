shader_type canvas_item;
render_mode blend_mix;

// 16-byte aligned uniforms
uniform vec4 u_spectral_constants_1; // x: Theta, y: Psi, z: Delta, w: Phi
uniform vec4 u_spectral_constants_2; // x: Omega, y: Epsilon, z: Carrier Hz, w: Friction Fs
uniform float u_lumen_emission_gain;
uniform float u_dialogue_cadence_scalar;

const float BAYER_2X2[4] = float[4](
    0.0 / 4.0, 2.0 / 4.0,
    3.0 / 4.0, 1.0 / 4.0
);

void fragment() {
    vec4 tex_color = texture(TEXTURE, UV);
    
    // Integer bitwise 2x2 Bayer indexing
    ivec2 screen_coord = ivec2(FRAGCOORD.xy) & 1;
    int dither_idx = screen_coord.x | (screen_coord.y << 1);
    float dither_threshold = BAYER_2X2[dither_idx];

    float lum = dot(tex_color.rgb, vec3(0.299, 0.587, 0.114));
    float dithered_lum = step(dither_threshold * 0.35, lum);

    float speech_boost = 1.0 + (0.45 * u_dialogue_cadence_scalar);
    vec3 gold_law = vec3(0.95, 0.75, 0.20) * tex_color.r * u_lumen_emission_gain * speech_boost;
    vec3 cyan_cognition = vec3(0.00, 0.85, 0.75) * tex_color.g * u_lumen_emission_gain;

    COLOR.rgb = (tex_color.rgb * dithered_lum) + gold_law + cyan_cognition;
    COLOR.a = tex_color.a;
}
