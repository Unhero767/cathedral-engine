shader_type spatial;
render_mode blend_mix, depth_draw_opaque, cull_back, diffuse_burley, specular_schlick_ggx;

uniform float scar_intensity : hint_range(0.0, 10.0) = 0.0;
uniform vec4 scar_color : source_color = vec4(0.8, 0.1, 0.9, 1.0);
uniform float time_scale = 4.0;

void vertex() {
    // Dynamic vertex displacement driven by dialetheic strain and simulation time
    float structural_fracture = sin(VERTEX.x * 12.0 + TIME * time_scale) * cos(VERTEX.z * 12.0 + TIME * time_scale);
    VERTEX += NORMAL * structural_fracture * scar_intensity * 0.15;
}

void fragment() {
    // Fragment color warping and high-frequency emissive pulse during State B collision
    vec3 base_substrate = vec3(0.02, 0.02, 0.05);
    float pulse = abs(sin(TIME * time_scale * 2.5)) * scar_intensity;
    
    ALBEDO = base_substrate + (scar_color.rgb * pulse * 0.5);
    EMISSION = scar_color.rgb * pulse * 2.5;
    ROUGHNESS = 0.15;
    METALLIC = 0.8;
}
