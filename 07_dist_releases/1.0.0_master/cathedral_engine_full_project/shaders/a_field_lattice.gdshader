shader_type canvas_item;
// Architectonic Field (A-Field) Dynamic Lattice Line Tension & Wave Overlay Shader
// Calculates spatial gravitational curvature C_l = ∇·L and renders dynamic tension lines

uniform float grid_spacing : hint_range(8.0, 128.0) = 32.0;
uniform float line_thickness : hint_range(0.5, 5.0) = 1.2;
uniform float tension_warp : hint_range(0.0, 2.0) = 0.6;
uniform float k_index : hint_range(0.0, 9.0) = 1.2;
uniform float time_speed : hint_range(0.0, 10.0) = 1.5;
uniform vec4 lattice_color : source_color = vec4(0.0, 0.898, 1.0, 0.35);

void fragment() {
	vec2 screen_coord = FRAGCOORD.xy;
	
	// Gravitational curvature distortion
	float pulse = sin(TIME * time_speed + screen_coord.x * 0.02 + screen_coord.y * 0.02);
	vec2 warped_coord = screen_coord + vec2(sin(screen_coord.y * 0.05 + TIME), cos(screen_coord.x * 0.05 + TIME)) * (tension_warp * (1.0 + k_index * 0.2));
	
	// Compute grid lines
	vec2 grid = abs(fract(warped_coord / grid_spacing - 0.5) - 0.5) / fwidth(warped_coord / grid_spacing);
	float line_val = min(grid.x, grid.y);
	float c = 1.0 - min(line_val, 1.0);
	
	// Dynamic glow modulation based on K-index
	vec4 col = lattice_color;
	if (k_index > 5.0) {
		col = mix(lattice_color, vec4(0.863, 0.078, 0.235, 0.6), (k_index - 5.0) / 4.0);
	}
	
	COLOR = vec4(col.rgb, c * col.a * (0.8 + pulse * 0.2));
}
