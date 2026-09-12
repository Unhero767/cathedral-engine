shader_type canvas_item;

uniform vec4 obsidian_color : source_color = vec4(0.04, 0.04, 0.04, 0.95);
uniform vec4 resonance_vein_color : source_color = vec4(0.83, 0.68, 0.21, 1.0);
uniform float scar_intensity : hint_range(0.0, 1.0) = 1.0;

void fragment() {
    vec2 uv = UV - vec2(0.5);
    float d1 = abs(uv.x - uv.y);
    float d2 = abs(uv.x + uv.y);
    float x_cross = min(d1, d2);
    
    float core = 1.0 - smoothstep(0.0, 0.06, x_cross);
    float glow = 1.0 - smoothstep(0.0, 0.25, x_cross);
    
    vec4 base = obsidian_color;
    vec4 vein = resonance_vein_color * (core + glow * 0.4) * scar_intensity;
    
    COLOR = mix(base, vein, vein.a);
}
