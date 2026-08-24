/*
===============================================================================
ResonanceScreen.gdshader - Godot 4.x Audio-Reactive & Flux Screen Shader
Drives visual feedback using live carrier_hz (130.81 Hz) and dPhi/dt flux
Strata: Books I–XL (Prime Foundations & Outer Choirs)
===============================================================================
*/
shader_type canvas_item;

uniform sampler2D screen_texture : hint_screen_texture, repeat_disable, filter_nearest;
uniform float carrier_hz : hint_range(20.0, 500.0) = 130.81;
uniform float flux_dphi_dt : hint_range(0.0, 2.0) = 0.428;
uniform float ego_density : hint_range(0.0, 10.0) = 8.3;
uniform float systemic_coherence : hint_range(0.0, 1.0) = 0.72;
uniform vec4 active_spectral_color : source_color = vec4(0.88, 0.42, 0.46, 1.0); // Crimson default

void fragment() {
	vec2 uv = SCREEN_UV;
	
	// Carrier wave temporal frequency modulation (C3 = 130.81 Hz normalized)
	float wave_time = TIME * (carrier_hz * 0.05);
	
	// Bi-directional A-Field wave interference
	float wave_x = sin(uv.x * 64.0 + wave_time * 1.5) * 0.5 + 0.5;
	float wave_y = cos(uv.y * 64.0 - wave_time * 1.2) * 0.5 + 0.5;
	float a_field_interference = wave_x * wave_y;
	
	// Chromatic dispersion driven by dPhi/dt flux
	vec2 dispersion_offset = vec2(flux_dphi_dt * 0.008 * sin(wave_time + uv.y * 10.0), 0.0);
	
	// Multi-channel spectral sampling
	float r_channel = texture(screen_texture, uv + dispersion_offset).r;
	float g_channel = texture(screen_texture, uv).g;
	float b_channel = texture(screen_texture, uv - dispersion_offset).b;
	vec3 base_color = vec3(r_channel, g_channel, b_channel);
	
	// 1.5 Hz Somatic Baseline Thermal Sink Scanline
	float somatic_pulse = sin(TIME * 1.5 * 6.28318530718);
	float scanline = sin(uv.y * 320.0 + somatic_pulse) * 0.035;
	base_color -= scanline;
	
	// Harmonic Scar X-Pillar Grid Alignment Overlay
	vec2 grid_uv = fract(uv * 8.0) - vec2(0.5);
	float diag_a = abs(grid_uv.x - grid_uv.y);
	float diag_b = abs(grid_uv.x + grid_uv.y);
	float x_scar_metric = smoothstep(0.04, 0.01, min(diag_a, diag_b));
	float scar_intensity = x_scar_metric * (1.0 - systemic_coherence) * 0.25;
	
	// Spectral tint infusion
	vec3 spectral_tint = active_spectral_color.rgb * (a_field_interference * 0.15 + scar_intensity);
	vec3 final_color = base_color + spectral_tint;
	
	// Fresnel vignette boundary
	float dist_from_center = distance(uv, vec2(0.5));
	float vignette = smoothstep(0.75, 0.35, dist_from_center);
	final_color *= vignette;

	COLOR = vec4(final_color, 1.0);
}
