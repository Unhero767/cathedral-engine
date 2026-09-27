shader_type spatial;
render_mode unshaded, blend_mix;

uniform float u_strain_glow_gain : hint_range(0.0, 10.0) = 4.5;
uniform vec3 u_spectral_base_color : source_color = vec3(0.12, 0.05, 0.22);

void fragment() {
    vec3 emission = u_spectral_base_color * u_strain_glow_gain;
    ALBEDO = emission * 0.2;
    EMISSION = emission;
}
