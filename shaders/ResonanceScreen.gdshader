shader_type canvas_item;

uniform sampler2D screen_texture : hint_screen_texture, repeat_disable, filter_nearest;
uniform float dissonance_distortion : hint_range(0.0, 1.0) = 0.0;

void fragment() {
    vec4 col = texture(screen_texture, SCREEN_UV);
    if (dissonance_distortion > 0.5) {
        col.rgb = vec3(col.r * 1.2, col.g * 0.8, col.b * 1.3);
    } else {
        col.r *= 1.05;
        col.b *= 1.15;
    }
    COLOR = col;
}
