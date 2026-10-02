shader_type canvas_item;

uniform float u_afield_potency : hint_range(0.0, 2.0) = 1.0;
uniform float u_shadow_depth_ramp : hint_range(0.0, 1.0) = 0.35;
uniform float u_lumen_emission_gain : hint_range(0.0, 3.0) = 1.396;

const float BAYER_2X2[4] = {
    0.00, 0.50,
    0.75, 0.25
};

void fragment() {
    vec4 base_color = texture(TEXTURE, UV);
    if (base_color.a < 0.001) {
        base_color = vec4(0.0, 0.92, 1.0, 1.0); // Matte Teal baseline fallback for placeholder
    }
    ivec2 pixel_coord = ivec2(floor(UV * 128.0));
    int bayer_index = (pixel_coord.x % 2) + (pixel_coord.y % 2) * 2;
    float dither_offset = (BAYER_2X2[bayer_index] - 0.5) * 0.12;
    
    float luminance = dot(base_color.rgb, vec3(0.299, 0.587, 0.114)) + dither_offset;
    
    vec3 emission = vec3(0.0);
    if (base_color.b > 0.65 && base_color.r < 0.35) {
        emission = vec3(0.0, 0.92, 1.0) * u_lumen_emission_gain * u_afield_potency;
    } else if (base_color.r > 0.70 && base_color.g > 0.55) {
        emission = vec3(1.0, 0.82, 0.28) * u_afield_potency;
    }
    
    vec3 final_rgb = base_color.rgb + emission;
    if (luminance < u_shadow_depth_ramp) {
        final_rgb *= 0.618;
    }
    
    COLOR = vec4(final_rgb, 1.0);
}
