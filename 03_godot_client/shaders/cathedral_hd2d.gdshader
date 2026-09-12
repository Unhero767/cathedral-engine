shader_type canvas_item;

uniform sampler2D SCREEN_TEXTURE : hint_screen_texture, filter_nearest;
uniform vec4 gold_halo_color : source_color = vec4(1.0, 0.82, 0.28, 1.0);
uniform vec4 cyan_eye_color : source_color = vec4(0.0, 0.92, 1.0, 1.0);

uniform float shadow_depth_exponent : hint_range(1.0, 5.0) = 2.4;
uniform float edge_luminance_boost : hint_range(1.0, 2.5) = 1.6;

uniform bool enable_volumetric_rays = true;
uniform int ray_samples : hint_range(4, 32) = 16;
uniform float ray_decay : hint_range(0.80, 0.99) = 0.95;
uniform float ray_density : hint_range(0.1, 2.0) = 0.8;

const float bayer_matrix_4x4[16] = float[](
    0.0/16.0, 12.0/16.0,  3.0/16.0, 15.0/16.0,
    8.0/16.0,  4.0/16.0, 11.0/16.0,  7.0/16.0,
    2.0/16.0, 14.0/16.0,  1.0/16.0, 13.0/16.0,
    10.0/16.0, 6.0/16.0,  9.0/16.0,  5.0/16.0
);

float get_bayer_value(vec2 frag_coord) {
    int x = int(mod(frag_coord.x, 4.0));
    int y = int(mod(frag_coord.y, 4.0));
    return bayer_matrix_4x4[y * 4 + x];
}

void fragment() {
    vec2 uv = UV;
    vec4 base_color = texture(SCREEN_TEXTURE, uv);
    
    float lum = dot(base_color.rgb, vec3(0.299, 0.587, 0.114));
    float adjusted_lum = pow(lum, shadow_depth_exponent);
    float grad_magnitude = length(fwidth(base_color.rgb));
    float edge_mask = smoothstep(0.01, 0.05, grad_magnitude);
    float final_lum = mix(adjusted_lum, lum * edge_luminance_boost, edge_mask);
    
    vec3 shaded_rgb = base_color.rgb * (final_lum / max(lum, 0.001));

    if (enable_volumetric_rays) {
        vec2 light_pos_screen = vec2(0.5, 0.35);
        vec2 delta_text_coord = (uv - light_pos_screen) * (ray_density / float(ray_samples));
        vec2 text_coord = uv;
        float illumination_decay = 1.0;
        vec3 ray_sum = vec3(0.0);

        for (int i = 0; i < 32; i++) {
            if (i >= ray_samples) break;
            text_coord -= delta_text_coord;
            vec4 sample_col = texture(SCREEN_TEXTURE, text_coord);
            float emission_mask = dot(sample_col.rgb, vec3(0.33)) > 0.7 ? 1.0 : 0.0;
            sample_col.rgb *= illumination_decay * ray_decay * emission_mask;
            ray_sum += sample_col.rgb;
            illumination_decay *= ray_decay;
        }
        shaded_rgb += (ray_sum / float(ray_samples)) * (gold_halo_color.rgb * 0.5 + cyan_eye_color.rgb * 0.5);
    }

    vec2 frag_coord = FRAGCOORD.xy;
    float dither_val = (get_bayer_value(frag_coord) - 0.5) * (1.0 / 32.0);
    vec3 quantized = floor(shaded_rgb * 16.0 + vec3(dither_val)) / 16.0;

    COLOR = vec4(quantized, base_color.a);
}
