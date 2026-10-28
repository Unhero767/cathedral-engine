shader_type canvas_item;

uniform float u_d_phi_dt : hint_range(0.0, 10.0) = 0.0;
uniform vec2 u_truth_vector = vec2(0.0, 0.0);
uniform float u_scar_load_index : hint_range(0.0, 1.0) = 0.0;

const vec3 SPECTRAL_BRONZE_NULL = vec3(0.18, 0.14, 0.12);
const vec3 SPECTRAL_TEAL_CURIOSITY = vec3(0.08, 0.68, 0.72);
const vec3 SPECTRAL_BLUE_SORROW = vec3(0.12, 0.28, 0.68);
const vec3 SPECTRAL_GOLD_SYNTHESIS = vec3(0.96, 0.78, 0.22);

void fragment() {
    vec2 uv = UV * 2.0 - 1.0;
    float r = length(uv);
    
    vec3 base_color = SPECTRAL_BRONZE_NULL;
    if (u_truth_vector.x > 0.5 && u_truth_vector.y < 0.5) {
        base_color = SPECTRAL_TEAL_CURIOSITY;
    } else if (u_truth_vector.x < 0.5 && u_truth_vector.y > 0.5) {
        base_color = SPECTRAL_BLUE_SORROW;
    } else if (u_truth_vector.x > 0.5 && u_truth_vector.y > 0.5) {
        float phase = sin(r * 16.0 - TIME * u_d_phi_dt) * 0.5 + 0.5;
        base_color = mix(SPECTRAL_BLUE_SORROW, SPECTRAL_GOLD_SYNTHESIS, phase * u_scar_load_index);
    }
    
    float ring_freq = max(1.0, u_d_phi_dt * 2.5);
    float resonance = smoothstep(0.75, 0.0, abs(sin(r * ring_freq - TIME * 2.0)));
    
    vec3 final_lumen = base_color + (SPECTRAL_GOLD_SYNTHESIS * resonance * (u_d_phi_dt / 10.0));
    COLOR = vec4(final_lumen, smoothstep(1.0, 0.85, r));
}
