shader_type canvas_item;
// 32-Bit HGASE Hard Noir Physical Boundary Shader
// High-contrast ink shadow quantization, crisp edge thresholding, and sacred geometric glow

uniform float shadow_threshold : hint_range(0.0, 1.0) = 0.45;
uniform float edge_sharpness : hint_range(1.0, 50.0) = 24.0;
uniform vec4 ink_black : source_color = vec4(0.02, 0.02, 0.02, 1.0);
uniform vec4 highlight_gold : source_color = vec4(0.855, 0.647, 0.125, 1.0);
uniform vec4 cyan_edge : source_color = vec4(0.0, 0.898, 1.0, 1.0);

void fragment() {
	vec4 base_color = texture(TEXTURE, UV);
	float luminance = dot(base_color.rgb, vec3(0.299, 0.587, 0.114));
	
	// Step quantization for pure hard noir chiaroscuro
	float shadow_mask = clamp((luminance - shadow_threshold) * edge_sharpness, 0.0, 1.0);
	
	// High-contrast thresholding with gold/cyan fringe
	vec3 noir_output = mix(ink_black.rgb, highlight_gold.rgb, shadow_mask);
	
	// Edge detection for geometric rim illumination
	float edge = fwidth(luminance) * 3.0;
	noir_output = mix(noir_output, cyan_edge.rgb, clamp(edge * (1.0 - shadow_mask), 0.0, 1.0));
	
	COLOR = vec4(noir_output, base_color.a);
}
