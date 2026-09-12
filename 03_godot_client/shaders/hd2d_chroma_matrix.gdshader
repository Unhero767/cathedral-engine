shader_type canvas_item;

uniform sampler2D screen_texture : hint_screen_texture, filter_nearest;
uniform float chromatic_aberration_amount : hint_range(0.0, 0.05) = 0.005;
uniform float color_depth_steps : hint_range(4.0, 32.0) = 16.0;

// Resonance state color weighting vectors
uniform vec3 primary_substrate = vec3(0.12, 0.14, 0.18); // Bronze-Obsidian Base
uniform vec3 resonance_flare = vec3(0.0, 0.85, 0.85);     // Teal/Cyan Glow
uniform vec3 aggressive_accent = vec3(0.9, 0.15, 0.15);   // Red/Crimson Accent
uniform float thermal_intensity : hint_range(0.0, 1.0) = 0.2;

void fragment() {
    vec2 uv = SCREEN_UV;
    
    // Multi-pass chromatic aberration offset
    vec4 red_channel = texture(screen_texture, uv + vec2(chromatic_aberration_amount, 0.0));
    vec4 green_channel = texture(screen_texture, uv);
    vec4 blue_channel = texture(screen_texture, uv - vec2(chromatic_aberration_amount, 0.0));
    
    vec4 final_color = vec4(red_channel.r, green_channel.g, blue_channel.b, 1.0);
    
    // Luminance extraction for volumetric chiaroscuro contrast mapping
    float luminance = dot(final_color.rgb, vec3(0.299, 0.587, 0.114));
    
    // Chiaroscuro high-contrast push (crushing shadows, boosting thermal highlights)
    if (luminance < 0.3) {
        final_color.rgb = mix(final_color.rgb, primary_substrate, 0.6);
    } else if (luminance > 0.7) {
        final_color.rgb = mix(final_color.rgb, resonance_flare, thermal_intensity);
    }
    
    // Aggressive Accent injection for high-threat states (Warning/Overload)
    float alert_mask = step(0.85, luminance) * thermal_intensity;
    final_color.rgb = mix(final_color.rgb, aggressive_accent, alert_mask);

    // 32-bit HD-2D quantization pass
    final_color.rgb = floor(final_color.rgb * color_depth_steps) / color_depth_steps;
    
    COLOR = final_color;
}
