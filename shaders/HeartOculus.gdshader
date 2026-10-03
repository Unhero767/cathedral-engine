// File: shaders/HeartOculus.gdshader
// Cathedral-Engine: HeartOculus Telemetry Spatial Shader
// Implements 2x2 Bayer Bio-Semantic Dithering, Lumen Emission, and Fresnel Strain.
shader_type spatial;
render_mode blend_mix, depth_draw_opaque, cull_back;

uniform vec4 u_albedo : source_color = vec4(0.85, 0.75, 0.45, 1.0); // Gold Joy baseline
uniform vec4 u_emission_color : source_color = vec4(1.0, 0.8, 0.3, 1.0);
uniform float u_emission_multiplier : hint_range(0.0, 16.0) = 8.5;
uniform float u_strain_glow_gain : hint_range(0.0, 5.0) = 1.0;
uniform float kenomic_entropy : hint_range(0.0, 100.0) = 0.0;
uniform int belnap_fog_level : hint_range(0, 2) = 0;
uniform float fresnel_power : hint_range(0.5, 8.0) = 3.0;

// Canonical Bayer 2x2 Dithering Matrix
const mat2 BAYER_2X2 = mat2(
    vec2(0.00, 0.50),
    vec2(0.75, 0.25)
);

void fragment() {
    // 1. Base Albedo & Normal Calculations
    vec3 normal = normalize(NORMAL);
    vec3 view = normalize(VIEW);
    
    // 2. Fresnel Strain Calculation
    float fresnel = pow(1.0 - clamp(dot(normal, view), 0.0, 1.0), fresnel_power);
    
    // 3. Screen-Space Bayer Dithering Attenuation
    vec2 screen_pos = mod(floor(FRAGCOORD.xy), 2.0);
    float dither = BAYER_2X2[int(screen_pos.x)][int(screen_pos.y)];
    
    float entropy_ratio = clamp(kenomic_entropy / 100.0, 0.0, 1.0);
    vec3 base_color = u_albedo.rgb;
    
    // Attenuate base surface by Fog and Dither Matrix
    if (belnap_fog_level > 0) {
        float fog_factor = float(belnap_fog_level) * 0.35;
        base_color = mix(base_color, base_color * dither, fog_factor * entropy_ratio);
    }
    
    ALBEDO = base_color;
    ROUGHNESS = 0.25 + (entropy_ratio * 0.4);
    METALLIC = 0.85 - (entropy_ratio * 0.3);
    
    // 4. Lumen Emission Driven by Telemetry Strain Multipliers
    float strain_boost = 1.0 + (fresnel * u_strain_glow_gain);
    vec3 final_emission = u_emission_color.rgb * u_emission_multiplier * strain_boost;
    
    // Obscure emission fringes under high Belnap Fog
    if (belnap_fog_level == 2) {
        final_emission *= mix(0.7, 1.0, dither);
    }
    
    EMISSION = final_emission;
}
