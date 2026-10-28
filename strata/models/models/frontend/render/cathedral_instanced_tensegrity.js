import * as THREE from 'three';

export class InstancedTensegritySystem {
  constructor(scene, elementCount = 119) {
    this.scene = scene;
    this.elementCount = elementCount;

    const baseGeometry = new THREE.CylinderGeometry(0.1, 0.1, 2.0, 8);
    
    this.lumenArray = new Float32Array(elementCount).fill(0.0);
    this.lumenAttribute = new THREE.InstancedBufferAttribute(this.lumenArray, 1);
    baseGeometry.setAttribute('a_lumen_emission', this.lumenAttribute);

    const material = new THREE.MeshStandardMaterial({
      color: 0x11161B,
      roughness: 0.2,
      metalness: 0.85
    });

    material.onBeforeCompile = (shader) => {
      shader.vertexShader = `
        attribute float a_lumen_emission;
        varying float v_lumen;
        ${shader.vertexShader}
      `.replace(
        '#include <begin_vertex>',
        `#include <begin_vertex>
         v_lumen = a_lumen_emission;`
      );

      shader.fragmentShader = `
        varying float v_lumen;
        ${shader.fragmentShader}
      `.replace(
        '#include <dithering_fragment>',
        `#include <dithering_fragment>
         vec3 lumenColor = mix(vec3(0.0, 0.8, 0.7), vec3(0.95, 0.75, 0.2), v_lumen);
         gl_FragColor.rgb += lumenColor * v_lumen * 1.5;`
      );
    };

    this.instancedMesh = new THREE.InstancedMesh(baseGeometry, material, elementCount);
    this.instancedMesh.instanceMatrix.setUsage(THREE.DynamicDrawUsage);
    this.scene.add(this.instancedMesh);

    this.dummy = new THREE.Object3D();
    this.initElementTransforms();
  }

  initElementTransforms() {
    for (let i = 0; i < this.elementCount; i++) {
      const angle = (i / this.elementCount) * Math.PI * 2.0;
      const radius = 12.0 + Math.sin(i * 0.5) * 3.0;
      this.dummy.position.set(Math.cos(angle) * radius, (i % 6) * 1.5 - 4.5, Math.sin(angle) * radius);
      this.dummy.rotation.set(0.2 * Math.sin(angle), angle, 0.2 * Math.cos(angle));
      this.dummy.updateMatrix();
      this.instancedMesh.setMatrixAt(i, this.dummy.matrix);
    }
    this.instancedMesh.instanceMatrix.needsUpdate = true;
  }

  pulseElement(index, intensity = 1.0) {
    if (index >= 0 && index < this.elementCount) {
      this.lumenArray[index] = intensity;
      this.lumenAttribute.needsUpdate = true;
    }
  }

  updateDecay(delta) {
    let needsUpdate = false;
    for (let i = 0; i < this.elementCount; i++) {
      if (this.lumenArray[i] > 0.001) {
        this.lumenArray[i] = Math.max(0.0, this.lumenArray[i] - delta * 1.8);
        needsUpdate = true;
      }
    }
    if (needsUpdate) {
      this.lumenAttribute.needsUpdate = true;
    }
  }
}
