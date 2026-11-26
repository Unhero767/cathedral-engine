shader_type canvas_item;
// Real-Time 4-Way Material Blending Shader
// Blends Obsidian, Gold Laminate, Liquid Mercury, and Crystalline Quartz

uniform vec4 mat0_obsidian : source_color = vec4(0.03, 0.03, 0.03, 1.0);
uniform vec4 mat1_gold : source_color = vec4(0.855, 0.647, 0.125, 1.0);
uniform vec4 mat2_mercury : source_color = vec4(0.75, 0.82, 0.88, 1.0);
uniform vec4 mat3_quartz : source_color = vec4(0.0, 0.898, 1.0, 1.0);

uniform sampler2D splatmap : hint_default_black;

void fragment() {
	vec4 weights = texture(splatmap, UV);
	float total_w = weights.r + weights.g + weights.b + weights.a;
	if (total_w < 0.001) {
		weights = vec4(1.0, 0.0, 0.0, 0.0);
		total_w = 1.0;
	}
	weights /= total_w;
	
	vec4 blended = mat0_obsidian * weights.r +
	               mat1_gold * weights.g +
	               mat2_mercury * weights.b +
	               mat3_quartz * weights.a;
	               
	COLOR = blended;
}
