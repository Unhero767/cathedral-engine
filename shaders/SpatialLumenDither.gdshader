shader_type spatial;
render_mode blend_mix, depth_draw_opaque, cull_back, diffuse_burley, specular_schlick_ggx;

uniform vec4 base_albedo : source_color = vec4(0.1, 0.1, 0.12, 1.0);
uniform float u_strain_glow_gain : hint_range(0.0, 10.0) = 1.0;
uniform sampler2D texture_albedo : source_color, filter_nearest, repeat_enable;

const float BAYER_2X2[4] = {
	0.0, 2.0,
	3.0, 1.0
};

float bayer_dither(vec2 pos) {
	int x = int(mod(pos.x, 2.0));
	int y = int(mod(pos.y, 2.0));
	int index = x + y * 2;
	return BAYER_2X2[index] / 4.0 - 0.5;
}

void fragment() {
	vec2 base_uv = UV;
	vec4 albedo_tex = texture(texture_albedo, base_uv);
	ALBEDO = albedo_tex.rgb * base_albedo.rgb * (1.0 + (u_strain_glow_gain * 0.2));
	
	float dither = bayer_dither(FRAGCOORD.xy);
	ALPHA = clamp(albedo_tex.a + dither * 0.05, 0.0, 1.0);
	
	EMISSION = ALBEDO * u_strain_glow_gain * 0.15;
	ROUGHNESS = 0.85;
	SPECULAR = 0.1;
}
