precision highp float;

uniform vec3 u_baseColor;
uniform vec3 u_emissiveColor;
uniform float u_fresnelPower;
uniform float u_subsurfaceDepth;
uniform float u_time;

varying vec3 v_normal;
varying vec3 v_viewPosition;

void main() {
    vec3 normal = normalize(v_normal);
    vec3 viewDir = normalize(v_viewPosition);
    
    // Fresnel Rim Calculation
    float fresnel = pow(1.0 - max(dot(viewDir, normal), 0.0), u_fresnelPower);
    
    // Subsurface Scattering Approximation
    float sss = max(0.0, dot(-normal, viewDir)) * u_subsurfaceDepth;
    
    // Cel / Anime Banding Simulation
    float lighting = max(dot(normal, vec3(0.0, 1.0, 0.5)), 0.0);
    float celShade = smoothstep(0.2, 0.25, lighting);
    
    vec3 finalColor = (u_baseColor * celShade) + (u_emissiveColor * fresnel) + vec3(sss * 0.2);
    gl_FragColor = vec4(finalColor, 1.0);
}
