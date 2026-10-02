shader_type spatial;
render_mode blend_mix, depth_draw_opaque, cull_back, diffuse_burley, specular_schlick_ggx;

uniform sampler2D albedo_texture : source_color, filter_nearest;
uniform vec4 spectral_tint : source_color = vec4(0.83, 0.68, 0.21, 1.0);
uniform float lumen_intensity : hint_range(0.0, 5.0) = 1.2;

float bayer4x4(vec2 coord) {
    int x = int(mod(coord.x, 4.0));
    int y = int(mod(coord.y, 4.0));
    int index = x + y * 4;
    float matrix[16] = float[16](
        0.0/16.0,  8.0/16.0,  2.0/16.0, 10.0/16.0,
       12.0/16.0,  4.0/16.0, 14.0/16.0,  6.0/16.0,
        3.0/16.0, 11.0/16.0,  1.0/16.0,  9.0/16.0,
       15.0/16.0,  7.0/16.0, 13.0/16.0,  5.0/16.0
    );
    return matrix[index];
}

void fragment() {
    vec4 tex_color = texture(albedo_texture, UV) * spectral_tint;
    vec2 screen_pixel = FRAGCOORD.xy;
    float dither = bayer4x4(screen_pixel);
    float quantized = floor(tex_color.r * 8.0 + dither) / 8.0;
    ALBEDO = tex_color.rgb * lumen_intensity;
    EMISSION = ALBEDO * 0.3 * (quantized > 0.5 ? 1.0 : 0.2);
}
