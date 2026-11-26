shader_type canvas_item;
// Harmonic Scar Fracture Shader: Obsidian Dermis & Cymatic Gold Veins
// Petrifaction of dialetheic paradox collisions (A and not A) into load-bearing geometry

uniform float scar_intensity : hint_range(0.0, 2.0) = 1.0;
uniform vec4 obsidian_core : source_color = vec4(0.02, 0.02, 0.02, 1.0);
uniform vec4 gold_vein : source_color = vec4(0.855, 0.647, 0.125, 1.0);
uniform vec4 emerald_healing : source_color = vec4(0.314, 0.784, 0.471, 1.0);

// Simple hash / noise function
float hash(vec2 p) {
	return fract(sin(dot(p, vec2(127.1, 311.7))) * 43758.5453);
}

void fragment() {
	vec2 uv = UV * 8.0;
	vec2 g = floor(uv);
	vec2 f = fract(uv);
	
	// Voronoi crack pattern
	float min_dist = 1.0;
	for (int y = -1; y <= 1; y++) {
		for (int x = -1; x <= 1; x++) {
			vec2 lattice = vec2(float(x), float(y));
			vec2 offset = vec2(hash(g + lattice), hash(g + lattice + vec2(3.14, 2.71)));
			vec2 r = lattice + offset - f;
			float d = dot(r, r);
			min_dist = min(min_dist, d);
		}
	}
	
	float crack = smoothstep(0.04, 0.0, min_dist);
	float pulse = sin(TIME * 3.0) * 0.5 + 0.5;
	
	vec3 base = obsidian_core.rgb;
	vec3 vein = mix(gold_vein.rgb, emerald_healing.rgb, pulse);
	
	vec3 final_color = mix(base, vein, crack * scar_intensity);
	COLOR = vec4(final_color, 1.0);
}
