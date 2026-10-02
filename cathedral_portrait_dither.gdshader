shader_type canvas_item;
render_mode blend_mix, unshaded;

// =============================================================================
// cathedral_portrait_dither.gdshader
// EAS-03 Bio-Semantic CanvasItem Shader // MLAOS-Prime / Cathedral-Engine
// Governed by: Book VIII (EAS-03 Somatic Layering & Lithography)
// =============================================================================

uniform float u_afield_potency : hint_range(0.0, 2.0) = 1.0;
uniform float u_lumen_emission_gain : hint_range(0.0, 3.0) = 1.0;
uniform float u_bayer_dither_intensity : hint_range(0.0, 1.0) = 0.12;
uniform float u_shadow_depth_ramp : hint_range(0.0, 1.0) = 0.35;
uniform vec3 u_spectral_matte_teal = vec3(0.0, 0.85, 0.78);
uniform vec3 u_spectral_sovereign_gold = vec3(1.0, 0.82, 0.28);

// Ordered Bayer 2x2 dithering matrix
const float BAYER_2X2[4] = float[](
	0.00, 0.50,
	0.75, 0.25
);

void fragment() {
	vec4 base_color = texture(TEXTURE, UV);
	if (base_color.a < 0.01) {
		discard;
	}

	// 1. 128x128 pixel-grid snap for consistent dither alignment
	ivec2 pixel_coord = ivec2(floor(UV * 128.0));
	int bayer_index = (pixel_coord.x % 2) + (pixel_coord.y % 2) * 2;
	float dither_offset = (BAYER_2X2[bayer_index] - 0.5) * u_bayer_dither_intensity;

	// 2. Luminance calculation modulated by Bayer dither
	float luminance = dot(base_color.rgb, vec3(0.299, 0.587, 0.114)) + dither_offset;

	// 3. Shadow depth ramping
	vec3 lit_color = base_color.rgb;
	if (luminance < u_shadow_depth_ramp) {
		float shadow_factor = smoothstep(0.0, u_shadow_depth_ramp, luminance);
		lit_color = mix(base_color.rgb * 0.45, base_color.rgb, shadow_factor);
	}

	// 4. Dual Lumen Wavelength Isolation
	// Channel A: Secondary Lumen (Cyan / Matte Teal Ocular Cognition: lambda = 495 nm / 639 Hz)
	if (base_color.b > 0.55 && base_color.r < 0.40) {
		vec3 teal_emission = u_spectral_matte_teal * u_lumen_emission_gain;
		lit_color += teal_emission * 0.45;
	}

	// Channel B: Sovereign Constant (Theta / Burnished Gold: lambda = 580 nm / 528 Hz)
	if (base_color.r > 0.65 && base_color.g > 0.50 && base_color.b < 0.40) {
		vec3 gold_emission = u_spectral_sovereign_gold * u_afield_potency;
		lit_color += gold_emission * 0.35;
	}

	COLOR = vec4(clamp(lit_color, 0.0, 1.0), base_color.a);
}
