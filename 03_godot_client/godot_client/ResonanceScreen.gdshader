shader_type canvas_item;
uniform float resonance : hint_range(0.0, 2.0) = 1.0;
void fragment() {
    vec4 col = texture(TEXTURE, UV);
    COLOR = col * vec4(resonance, resonance * 0.9, 1.0, 1.0);
}
