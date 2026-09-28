shader_type spatial;
render_mode unshaded; // <-- Add this line

uniform float z_active : hint_range(0.0, 20.0) = 6.5;

void vertex() {
    float wave = sin(TIME * 3.0 + VERTEX.y * 2.0) * 0.05 * z_active;
    VERTEX += NORMAL * wave;
}

void fragment() {
    vec3 gold_base = vec3(0.85, 0.65, 0.2);
    ALBEDO = gold_base;
}