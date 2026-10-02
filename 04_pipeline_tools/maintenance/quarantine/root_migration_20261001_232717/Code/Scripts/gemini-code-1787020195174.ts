import * as THREE from 'three';
import vertexShader from './shaders/nanoweave.vert.glsl';
import fragmentShader from './shaders/nanoweave.frag.glsl';

export function createAmberGoldLatticeMaterial(
  overrides: Partial<typeof AMBER_GOLD_LATTICE_PRESET.uniforms> = {}
): THREE.ShaderMaterial {
  const config = { ...AMBER_GOLD_LATTICE_PRESET.uniforms, ...overrides };

  return new THREE.ShaderMaterial({
    vertexShader,
    fragmentShader,
    uniforms: {
      u_time: { value: 0 },
      u_lattice_tensile_rating: { value: config.u_lattice_tensile_rating },
      u_dialetheic_cushion: { value: config.u_dialetheic_cushion },
      u_somatic_phase_mask: { value: config.u_somatic_phase_mask },
      u_spectral_constant_color: {
        value: new THREE.Color(...config.u_spectral_constant_dominant),
      },
    },
    transparent: AMBER_GOLD_LATTICE_PRESET.renderBehavior.transparent,
    depthWrite: AMBER_GOLD_LATTICE_PRESET.renderBehavior.depthWrite,
    side: AMBER_GOLD_LATTICE_PRESET.renderBehavior.cullFace
      ? THREE.FrontSide
      : THREE.DoubleSide,
  });
}