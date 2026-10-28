#[compute]
#version 450

// Spectral Constant: Teal (Curiosity / Exploration)
// Calculates the Voronoi distance fields for civilization seed nodes.

layout(local_size_x = 16, local_size_y = 16, local_size_z = 1) in;

struct SeedNode {
    vec2 position;
    float cultural_weight;
    float alignment_hash; // Paraconsistent identifier
};

layout(set = 0, binding = 0, std430) restrict readonly buffer SeedBuffer {
    SeedNode nodes[];
} seed_buffer;

layout(set = 0, binding = 1, rgba8) restrict writeonly uniform image2D output_image;

layout(push_constant, std430) uniform Params {
    int node_count;
    vec2 resolution;
} params;

void main() {
    ivec2 texel_coords = ivec2(gl_GlobalInvocationID.xy);
    vec2 uv = vec2(texel_coords) / params.resolution;
    
    if (texel_coords.x >= int(params.resolution.x) || texel_coords.y >= int(params.resolution.y)) {
        return;
    }

    float min_dist = 999999.0;
    float second_min_dist = 999999.0;
    int closest_node = -1;

    for (int i = 0; i < params.node_count; i++) {
        SeedNode node = seed_buffer.nodes[i];
        
        float dist = distance(uv, node.position) / max(node.cultural_weight, 0.001);
        
        if (dist < min_dist) {
            second_min_dist = min_dist;
            min_dist = dist;
            closest_node = i;
        } else if (dist < second_min_dist) {
            second_min_dist = dist;
        }
    }

    float border_friction = second_min_dist - min_dist;
    vec4 color = vec4(0.0, 0.0, 0.0, 1.0);
    
    if (border_friction < 0.02) {
        color = vec4(0.8, 0.1, 0.2, 1.0); // Contested red/bronze
    } else {
        float hash_val = seed_buffer.nodes[closest_node].alignment_hash;
        color = vec4(mod(hash_val, 1.0), mod(hash_val * 2.0, 1.0), mod(hash_val * 3.0, 1.0), 1.0);
    }

    imageStore(output_image, texel_coords, color);
}
