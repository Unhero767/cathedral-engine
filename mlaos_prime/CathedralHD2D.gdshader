// ====================================================================
// MLAOS-Prime :: 32-bit HD-2D Cathedral Shader 
// Features: Bayer 2x2 Dithering, Somatic Cadence, Lumen Emission
// ====================================================================
shader_type canvas_item;

uniform float ego_density = 8.30;
uniform float spectral_coherence = 0.98;
uniform vec4 emission_color : source_color = vec4(0.0, 1.0, 0.8, 1.0); // Teal default

const float bayer2x2[4] = float[](
    0.0, 0.5,
    0.75, 0.25
);

void fragment() {
    vec4 tex_color = texture(TEXTURE, UV);
    
    // Bayer 2x2 Dither coordinates
    int x = int(FRAGCOORD.x) % 2;
    int y = int(FRAGCOORD.y) % 2;
    float dither_val = bayer2x2[x + y * 2];
    
    // Calculate luminance
    float lum = dot(tex_color.rgb, vec3(0.299, 0.587, 0.114));
    
    // Apply ego_density thresholding for crunch
    float threshold = (ego_density / 10.0) * dither_val;
    if (lum < threshold && tex_color.a > 0.0) {
        tex_color.rgb *= spectral_coherence; // Darken based on loss of coherence
    }
    
    // Lumen Emission on high values
    if (lum > 0.8) {
        tex_color.rgb += emission_color.rgb * (1.0 - spectral_coherence);
    }
    
    COLOR = tex_color;
}
