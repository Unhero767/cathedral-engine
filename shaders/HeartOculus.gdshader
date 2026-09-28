shader_type spatial;
render_mode blend_mix, depth_draw_opaque, cull_back, diffuse_burley, specular_schlick_ggx;

// --- Telemetry-Driven Uniforms ---
// These are dynamically manipulated by the CathedralRuntimeBridge.gd
uniform vec4 u_albedo : source_color = vec4(0.1, 0.1, 0.1, 1.0);
uniform vec4 u_emission_color : source_color = vec4(0.1, 0.1, 0.1, 1.0);
uniform float u_emission_multiplier = 1.0;
uniform float u_strain_glow_gain = 0.0;

// --- Biomechanical Lithic Properties ---
uniform float u_metallic : hint_range(0.0, 1.0) = 0.85;
uniform float u_roughness : hint_range(0.0, 1.0) = 0.25;

// --- 2x2 Bayer Dithering Matrix ---
// Canonical ordering for 32-bit retro texturing
const float BAYER_MATRIX[4] = float[](
    0.00, 0.50,
    0.75, 0.25
);

void fragment() {
    // 1. Dither Threshold Calculation
    // Map the screen-space pixel coordinates to the 2x2 grid
    int dither_x = int(FRAGCOORD.x) % 2;
    int dither_y = int(FRAGCOORD.y) % 2;
    float dither_threshold = BAYER_MATRIX[dither_x + dither_y * 2];

    // 2. Base Material Application
    ALBEDO = u_albedo.rgb;
    METALLIC = u_metallic;
    ROUGHNESS = u_roughness;

    // 3. Volumetric Strain (Dialetheic Friction)
    // Calculate a Fresnel rim light to represent the structural strain.
    // As u_strain_glow_gain ramps up during a BOTH collision, the edges of the 
    // geometry will "burn" inward toward the core.
    float fresnel = pow(1.0 - clamp(dot(NORMAL, VIEW), 0.0, 1.0), 2.5);
    float strain_intensity = fresnel * u_strain_glow_gain;

    // 4. Raw Emission Synthesis
    // Combine the baseline telemetry output with the structural strain flare.
    vec3 base_glow = u_emission_color.rgb * u_emission_multiplier;
    vec3 strain_glow = u_emission_color.rgb * strain_intensity * 2.5;
    vec3 total_emission = base_glow + strain_glow;

    // 5. HD-2D Quantization & ordered Dithering
    // Instead of a smooth digital gradient, we crush the emission into distinct bands.
    // The dither threshold pushes borderline pixels into the next band, creating the classic pattern.
    float banding_steps = 6.0; 
    vec3 dithered_emission = floor(total_emission * banding_steps + dither_threshold) / banding_steps;

    // 6. Final Output
    EMISSION = dithered_emission;
}
