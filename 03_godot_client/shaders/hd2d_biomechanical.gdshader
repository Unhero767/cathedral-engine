shader_type canvas_item;

uniform sampler2D screen_texture : hint_screen_texture, filter_nearest;
uniform float chromatic_aberration_amount : hint_range(0.0, 0.05) = 0.005;
uniform float color_depth_steps : hint_range(4.0, 32.0) = 16.0;

void fragment() {
    vec2 uv = SCREEN_UV;
    vec4 red_channel = texture(screen_texture, uv + vec2(chromatic_aberration_amount, 0.0));
    vec4 green_channel = texture(screen_texture, uv);
    vec4 blue_channel = texture(screen_texture, uv - vec2(chromatic_aberration_amount, 0.0));
    vec4 final_color = vec4(red_channel.r, green_channel.g, blue_channel.b, 1.0);
    final_color.rgb = floor(final_color.rgb * color_depth_steps) / color_depth_steps;
    COLOR = final_color;
}
