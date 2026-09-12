shader_type canvas_item;
render_mode blend_mix, unshaded;

// =============================================================================
// Cathedral Spatial Lumen & Bio-Semantic Dither CanvasItem Shader
// System Classification: MLAOS-PRIME // EAS-03 // LIVED-SPACE-LUMEN
// Prime Isomorphism Axiom: Emotion == Physics == Magic == Biology == Architecture
// =============================================================================

// --- Volumetric Chiaroscuro & Dither Uniforms ---
uniform float u_shadow_depth_ramp : hint_range(0.0, 1.0) = 0.65;
uniform float u_shadow_crush_floor : hint_range(0.0, 0.5) = 0.35;
uniform float u_specular_rim_factor : hint_range(0.5, 3.0) = 1.35;
uniform float u_dither_pixel_size : hint_range(16.0, 512.0) = 128.0;
uniform bool u_enable_dither = true;

// --- Bio-Semantic Lumen & A-Field Kinetics Uniforms ---
uniform float u_lumen_emission_gain : hint_range(0.0, 4.0) = 1.00;
uniform float u_afield_potency : hint_range(0.0, 3.0) = 1.00;
uniform int u_active_spectral_constant : hint_range(0, 6) = 1; // 0=Gold, 1=Teal, 2=Blue, 3=Red, 4=Violet, 5=Emerald, 6=Obsidian
uniform bool u_enable_multichannel_lumen = true;
uniform bool u_enable_spectral_dominance = true;

// --- Dialetheic Refraction & Harmonic Scarring Uniforms ---
uniform float u_dialetheic_refraction_intensity : hint_range(0.0, 1.0) = 0.0;
uniform float u_harmonic_scar_resonance : hint_range(0.0, 2.0) = 0.0;

// --- Optional External Spectral Color Ramp Texture ---
uniform sampler2D u_spectral_ramp_texture : hint_default_black, filter_nearest;
uniform bool u_use_ramp_texture = false;

// -----------------------------------------------------------------------------
// 2x2 Bayer Ordered Dithering Matrix normalized to [0.0, 1.0]
// -----------------------------------------------------------------------------
const float BAYER_2X2[4] = float[](
	0.00, 0.50,
	0.75, 0.25
);

// -----------------------------------------------------------------------------
// Six Spectral Constants (Canonical RGB Vectors)
// -----------------------------------------------------------------------------
const vec3 SPECTRAL_THETA_GOLD   = vec3(1.00, 0.82, 0.28); // Joy / Law (580 THz)
const vec3 SPECTRAL_PSI_TEAL     = vec3(0.00, 0.92, 1.00); // Curiosity / Recursion (510 THz)
const vec3 SPECTRAL_DELTA_BLUE   = vec3(0.12, 0.32, 0.78); // Sorrow / Archiving (450 THz)
const vec3 SPECTRAL_PHI_RED      = vec3(0.95, 0.16, 0.20); // Anger / Entropy (680 THz)
const vec3 SPECTRAL_OMEGA_VIOLET = vec3(0.62, 0.18, 0.88); // Fear / Adaptation (720 THz)
const vec3 SPECTRAL_EPSILON_EMR  = vec3(0.10, 0.88, 0.48); // Love / Binding (540 THz)
const vec3 SPECTRAL_NULL_VOID    = vec3(0.04, 0.04, 0.06); // Obsidian / Anti-Resonance

vec3 get_spectral_dominant_color(int constant_id) {
	switch (constant_id) {
		case 0: return SPECTRAL_THETA_GOLD;
		case 1: return SPECTRAL_PSI_TEAL;
		case 2: return SPECTRAL_DELTA_BLUE;
		case 3: return SPECTRAL_PHI_RED;
		case 4: return SPECTRAL_OMEGA_VIOLET;
		case 5: return SPECTRAL_EPSILON_EMR;
		case 6: return SPECTRAL_NULL_VOID;
		default: return SPECTRAL_PSI_TEAL;
	}
}

void fragment() {
	vec2 uv_coord = UV;
	
	// 1. Dialetheic Paraconsistent Refraction Distortion (when contradiction active)
	if (u_dialetheic_refraction_intensity > 0.001) {
		float wave = sin(UV.y * 32.0 + TIME * 8.0) * cos(UV.x * 24.0 - TIME * 6.0);
		uv_coord.x += wave * (0.015 * u_dialetheic_refraction_intensity);
	}
	
	vec4 base_color = texture(TEXTURE, uv_coord);
	
	// Discard transparent fragment pixels
	if (base_color.a < 0.01) {
		discard;
	}
	
	// 2. Bio-Semantic Ordered Bayer 2x2 Dithering & Volumetric Chiaroscuro
	if (u_enable_dither) {
		ivec2 pixel_coord = ivec2(floor(uv_coord * u_dither_pixel_size));
		int bayer_index = (pixel_coord.x % 2) + (pixel_coord.y % 2) * 2;
		float dither_offset = (BAYER_2X2[bayer_index] - 0.5) * 0.12;
		
		// Standard ITU-R BT.601 perceptual luminance formula
		float luminance = dot(base_color.rgb, vec3(0.299, 0.587, 0.114)) + dither_offset;
		
		if (luminance < u_shadow_depth_ramp) {
			float ramp_factor = luminance / max(u_shadow_depth_ramp, 0.001);
			float shadow_multiplier = mix(u_shadow_crush_floor, 0.90, ramp_factor);
			
			// Modulate shadow with deep Obsidian/Delta indigo tint
			vec3 shadow_tint = mix(SPECTRAL_DELTA_BLUE * 0.4, vec3(1.0), ramp_factor);
			base_color.rgb *= shadow_multiplier * shadow_tint;
		}
	}
	
	// 3. Multi-Channel Spectral Lumen Emission Pipeline
	if (u_enable_multichannel_lumen) {
		vec3 total_emission = vec3(0.0);
		
		// Channel 1: Gold Constant (Theta - Joy / Law / Gilded Tri-Key Halo)
		// Trigger: High Red + Moderate-to-High Green + Low-to-Moderate Blue
		if (base_color.r > 0.70 && base_color.g > 0.52 && base_color.b < 0.45) {
			float intensity = (base_color.r + base_color.g) * 0.5;
			total_emission += SPECTRAL_THETA_GOLD * (intensity * u_afield_potency * u_specular_rim_factor);
		}
		
		// Channel 2: Teal Constant (Psi - Curiosity / Cognitive Ocular Surge)
		// Trigger: High Blue + High Green + Low Red
		else if (base_color.b > 0.65 && base_color.g > 0.50 && base_color.r < 0.35) {
			float intensity = base_color.b;
			total_emission += SPECTRAL_PSI_TEAL * (intensity * u_lumen_emission_gain * u_specular_rim_factor);
		}
		
		// Channel 3: Red Constant (Phi - Anger / Entropy / Kinetic Rupture)
		// Trigger: High Red + Low Green + Low Blue
		else if (base_color.r > 0.75 && base_color.g < 0.30 && base_color.b < 0.30) {
			float intensity = base_color.r;
			total_emission += SPECTRAL_PHI_RED * (intensity * u_afield_potency * 1.2);
		}
		
		// Channel 4: Blue Constant (Delta - Sorrow / Ash Archive Inscription)
		// Trigger: High Blue + Low Red + Low Green
		else if (base_color.b > 0.70 && base_color.r < 0.25 && base_color.g < 0.40) {
			float intensity = base_color.b;
			total_emission += SPECTRAL_DELTA_BLUE * (intensity * 1.1);
		}
		
		// Channel 5: Violet Constant (Omega - Fear / Adaptation / Shadow Density)
		// Trigger: High Red + High Blue + Low Green
		else if (base_color.r > 0.55 && base_color.b > 0.60 && base_color.g < 0.30) {
			float intensity = (base_color.r + base_color.b) * 0.5;
			total_emission += SPECTRAL_OMEGA_VIOLET * (intensity * u_afield_potency);
		}
		
		// Channel 6: Emerald Constant (Epsilon - Love / Dynamic Binding Network)
		// Trigger: High Green + Low Red + Low Blue
		else if (base_color.g > 0.70 && base_color.r < 0.30 && base_color.b < 0.45) {
			float intensity = base_color.g;
			total_emission += SPECTRAL_EPSILON_EMR * (intensity * u_lumen_emission_gain);
		}
		
		// 4. Global Spectral Dominance & Ambient Resonance
		if (u_enable_spectral_dominance) {
			vec3 dominant_spectral_color = get_spectral_dominant_color(u_active_spectral_constant);
			float ambient_edge = max(0.0, dot(base_color.rgb, vec3(0.333)) - 0.75);
			total_emission += dominant_spectral_color * (ambient_edge * u_afield_potency * 0.45);
		}
		
		// 5. External Spectral Ramp Modulation (if enabled)
		if (u_use_ramp_texture) {
			float ramp_sample_pos = clamp(dot(base_color.rgb, vec3(0.299, 0.587, 0.114)), 0.0, 1.0);
			vec4 ramp_color = texture(u_spectral_ramp_texture, vec2(ramp_sample_pos, 0.5));
			base_color.rgb = mix(base_color.rgb, ramp_color.rgb, ramp_color.a * 0.65);
		}
		
		// 6. Harmonic Scar Resonance Pulse
		if (u_harmonic_scar_resonance > 0.001) {
			float pulse = abs(sin(TIME * 4.0)) * u_harmonic_scar_resonance;
			vec3 scar_color = mix(SPECTRAL_THETA_GOLD, SPECTRAL_PSI_TEAL, 0.5);
			total_emission += scar_color * pulse * 0.35;
		}
		
		// Additive injection of computed lumen radiance
		base_color.rgb += total_emission;
	}
	
	COLOR = base_color;
}
