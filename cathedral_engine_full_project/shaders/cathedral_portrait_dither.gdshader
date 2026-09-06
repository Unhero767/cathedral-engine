shader_type canvas_item;
render_mode blend_mix, unshaded;

uniform float u_shadow_depth_ramp : hint_range(0.0, 1.0) = 0.65;
uniform float u_specular_rim_factor : hint_range(0.5, 3.0) = 1.35;
uniform float u_lumen_emission_gain : hint_range(0.0, 4.0) = 1.00;
uniform float u_afield_potency : hint_range(0.0, 2.0) = 0.87;
uniform bool u_enable_dither = true;
uniform bool u_enable_dual_lumen = true;

const float BAYER_2X2[4] = float[](0.00, 0.50, 0.75, 0.25);

void fragment() {
    vec4 base_color = texture(TEXTURE, UV);
    if (base_color.a < 0.05) {
        discard;
    }
    
    // Bayer 2x2 Retro Dither & Shadow Ramp
    if (u_enable_dither) {
        ivec2 pixel_coord = ivec2(floor(UV * 128.0));
        int bayer_index = (pixel_coord.x % 2) + (pixel_coord.y % 2) * 2;
        float dither_offset = (BAYER_2X2[bayer_index] - 0.5) * 0.12;
        float luminance = dot(base_color.rgb, vec3(0.299, 0.587, 0.114)) + dither_offset;
        if (luminance < u_shadow_depth_ramp) {
            float ramp_factor = luminance / max(u_shadow_depth_ramp, 0.001);
            base_color.rgb *= mix(0.40, 0.85, ramp_factor);
        }
    }
    
    // Dual-Lumen Shader Triggers
    if (u_enable_dual_lumen) {
        vec3 emissive_output = vec3(0.0);
        if (base_color.b > 0.65 && base_color.r < 0.35) {
            emissive_output += vec3(0.0, 0.92, 1.0) * (u_lumen_emission_gain * u_specular_rim_factor);
        }
        if (base_color.r > 0.70 && base_color.g > 0.55) {
            emissive_output += vec3(1.0, 0.82, 0.28) * (u_afield_potency * u_specular_rim_factor);
        }
        base_color.rgb += emissive_output;
    }
    
    COLOR = base_color;
}
