/*
==============================================================================
          NYX AURELIA: SYSTEMIC SCREEN-SPACE CHROMATIC ABERRATION SHADER
                      FILE: heart-oculus-aberration.gdshader
==============================================================================
  This shader integrates directly with the HeartOculusCamera's active trauma 
  value. It generates frame-independent, organic chromatic splitting, radial 
  aberration, and space-time wave distortion that scales in lockstep with the 
  physical camera screenshake.
==============================================================================
*/

shader_type canvas_item;

// Screen texture coordinate sampler
uniform sampler2D screen_texture : hint_screen_texture, filter_linear_mipmap;

@export_group("Spacetime Trauma Interfacing")
## Direct trauma value hook [0.0 to 1.0], usually bound directly to camera screenshake trauma.
uniform float trauma : hint_range(0.0, 1.0) = 0.0;
## Exponent applied to trauma to control the non-linear curve of visual splitting.
uniform float trauma_exponent : hint_range(1.0, 4.0) = 2.0;

@export_group("Aberration Constants")
## Base color splitting offset at maximum trauma.
uniform float max_aberration_offset : hint_range(0.0, 0.1) = 0.04;
## Radial multiplier. Higher values cause aberration to stretch dramatically towards screen borders.
uniform float radial_stretch : hint_range(0.1, 5.0) = 1.8;
## Static background aberration level when trauma is zero.
uniform float baseline_chromatic : hint_range(0.0, 0.01) = 0.001;

@export_group("A-Field Wave Distortion")
## Maximum coordinate ripple displacement under full trauma.
uniform float max_distortion_strength : hint_range(0.0, 0.1) = 0.015;
## The spatial frequency of the spacetime distortion ripples.
uniform float wave_frequency : hint_range(1.0, 100.0) = 35.0;
## The velocity of the temporal distortion waves.
uniform float temporal_speed : hint_range(0.1, 20.0) = 8.0;

// Hardcoded physical spectral coordinates for Nyx's Core Resonance: Violet (410nm) / Obsidian
const vec3 SPECTRAL_DOMINANT_VIOLET = vec3(0.60, 0.36, 0.82);
const vec3 SPECTRAL_SECONDARY_OBSIDIAN = vec3(0.12, 0.08, 0.18);

// Pseudo-random noise function to create organic, non-linear pixel variance
float random_scalar(vec2 co) {
	return fract(sin(dot(co.xy, vec2(12.9898, 78.233))) * 43758.5453);
}

// Low-cost organic value noise approximation for spatial warping
float value_noise(vec2 uv) {
	vec2 ip = floor(uv);
	vec2 fp = fract(uv);
	fp = fp * fp * (3.0 - 2.0 * fp); // Smooth Hermite interpolation
	
	float d00 = random_scalar(ip);
	float d10 = random_scalar(ip + vec2(1.0, 0.0));
	float d01 = random_scalar(ip + vec2(0.0, 1.0));
	float d11 = random_scalar(ip + vec2(1.0, 1.0));
	
	return mix(mix(d00, d10, fp.x), mix(d01, d11, fp.x), fp.y);
}

void fragment() {
	vec2 uv = SCREEN_UV;
	
	// Translate UV coordinates to center-relative radial space
	vec2 center_offset = uv - vec2(0.5);
	float radial_distance = length(center_offset);
	
	// Calculate the active, non-linear trauma intensity: active_trauma = trauma^exponent
	float active_trauma = pow(trauma, trauma_exponent);
	
	// --------------------------------------------------------------------------
	// 1. ORGANIC SPACETIME WARPING (A-FIELD RIPPLES)
	// --------------------------------------------------------------------------
	// Generates dynamic, undulating waves that distort underlying geometry prior to color splitting
	float noise_sample = value_noise(uv * wave_frequency + vec2(TIME * temporal_speed));
	float wave_factor = sin(radial_distance * wave_frequency - TIME * temporal_speed) * noise_sample;
	
	// Only apply distortion in proportion to the active system trauma
	float active_distortion = active_trauma * max_distortion_strength;
	vec2 distorted_uv = uv + (center_offset * wave_factor * active_distortion);
	
	// --------------------------------------------------------------------------
	// 2. CHROMATIC CHROMOSPECTRAL SPLITTING (ABERRATION)
	// --------------------------------------------------------------------------
	// Splits the incoming light into distinct red, green, and blue components.
	// Splitting vector grows radially outward from the center, scaling exponentially near the borders.
	float split_scale = baseline_chromatic + (active_trauma * max_aberration_offset);
	float border_amplification = pow(radial_distance, radial_stretch);
	vec2 split_vector = center_offset * split_scale * border_amplification;
	
	// Sample distinct channels with radial and noise-modulated displacement vectors
	float r_channel = texture(screen_texture, distorted_uv + split_vector * (1.0 + noise_sample * 0.15)).r;
	float g_channel = texture(screen_texture, distorted_uv).g;
	float b_channel = texture(screen_texture, distorted_uv - split_vector * (1.0 - noise_sample * 0.15)).b;
	
	vec3 composed_color = vec3(r_channel, g_channel, b_channel);
	
	// --------------------------------------------------------------------------
	// 3. VIOLET / OBSIDIAN TINTING (THE SERAPH'S SPECTRAL SIGNATURE)
	// --------------------------------------------------------------------------
	// Under high trauma, the edges bleed into a dark violet-obsidian vignette, 
	// signifying the active intervention of the paraconsistent field.
	float vignette_strength = smoothstep(0.35, 0.75 + (1.0 - active_trauma * 0.4), radial_distance);
	
	// Mix base colors into the Seraph's violet dominant spectral coordinate
	vec3 chromatic_vignette = mix(composed_color, SPECTRAL_DOMINANT_VIOLET, vignette_strength * active_trauma * 0.55);
	
	// Apply dark, dense obsidian depth around extreme screen borders
	float border_darkening = smoothstep(0.55, 0.95, radial_distance);
	vec3 final_output = mix(chromatic_vignette, SPECTRAL_SECONDARY_OBSIDIAN, border_darkening * active_trauma * 0.45);
	
	COLOR = vec4(final_output, 1.0);
}
