shader_type canvas_item;

global uniform float global_z_active : hint_range(0.0, 10.0) = 1.0;
global uniform float global_contradiction_flag : hint_range(0.0, 1.0) = 0.0;

uniform float u_afield_potency : hint_range(0.0, 2.0) = 0.87;
uniform float u_lumen_emission_gain : hint_range(0.0, 5.0) = 1.0;

void fragment() {
    vec4 col = texture(TEXTURE, UV);
    
    // Modulate lumen emission and impedance state
    col.rgb *= u_lumen_emission_gain * global_z_active;
    
    // Apply Harmonic Scar channel inversion during dialetheic collision (B = <1, 1>)
    if (global_contradiction_flag > 0.5) {
        col.r = 1.0 - col.r;
        col.g = col.g * 0.8;
    }
    
    COLOR = col;
}