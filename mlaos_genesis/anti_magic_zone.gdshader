shader_type spatial;
render_mode unshaded, cull_disabled;

uniform vec3 nullification_color : source_color = vec3(0.1, 0.1, 0.15);
uniform float static_intensity : hint_range(0.0, 1.0) = 0.8;

void fragment() {
    vec2 grid_uv = fract(UV * 10.0);
    float boundary = step(0.9, grid_uv.x) + step(0.9, grid_uv.y);
    float distortion = sin(TIME * 5.0 + UV.y * 20.0) * 0.5 + 0.5;
    vec3 base_render = mix(nullification_color, vec3(0.0), distortion * static_intensity);
    ALBEDO = base_render + (vec3(boundary) * 0.2);
    ALPHA = 0.85;
}
