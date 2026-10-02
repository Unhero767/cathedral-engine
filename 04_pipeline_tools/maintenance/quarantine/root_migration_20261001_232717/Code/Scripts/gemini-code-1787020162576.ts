// Core Asset Registry: Preset ID: "MATERIAL_AMBER_GOLD_LATTICE_DEFAULT"
// Verified WebGL/Three.js Shader Uniforms for Character & Procedural Environments

export const AMBER_GOLD_LATTICE_PRESET = {
  id: "MATERIAL_AMBER_GOLD_LATTICE_DEFAULT",
  classification: "Adaptive Resonance Armor",
  description: "Opaque Amber-Gold Bio-Metallic Cellular Nanoweave Substrate",
  uniforms: {
    // Vertex Displacement Dynamics
    u_lattice_tensile_rating: 0.82,     // Octet Truss Planar Hardening
    u_dialetheic_cushion: 0.35,         // Kelvin Foam Viscous Dissipation
    displacement_coefficient: 0.063,     // Resulting Mesh Wave Amplitude
    
    // Fragment & Optical Surface Properties
    u_somatic_phase_mask: 0.18,         // Phase Permeability / Low Translucency
    fresnel_coefficient: 0.642,         // Cybernetic Latex Surface Sheen
    phase_alpha: 0.846,                 // Visual Solidity with Visible Interior Process
    
    // Chromatic Spectral Isolation
    u_spectral_constant_dominant: [0.84, 0.62, 0.12], // Gold/Joy (Organizing/Cohesive)
    u_spectral_constant_inertia:  [0.08, 0.22, 0.74], // Blue/Sorrow (Memory Gravity)
    
    // Edge Detection Thresholds
    voronoi_edge_min: 0.05,
    voronoi_edge_max: 0.12,
  },
  renderBehavior: {
    transparent: true,
    depthWrite: true,
    cullFace: false, // DoubleSide for cellular depth
  }
} as const;