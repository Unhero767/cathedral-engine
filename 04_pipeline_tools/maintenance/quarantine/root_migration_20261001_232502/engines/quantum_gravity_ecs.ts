/**
 * ================================================================================
 * CATHEDRAL-ENGINE :: QUANTUM-GRAVITATIONAL SELF-COUPLING ECS MODULE
 * ================================================================================
 * Solves the coupled Schrödinger-Newton equations and Autopoietic Strain Feedback
 * on a discrete 2D spatial lattice using the Split-Step Fourier Method (SSFM)
 * and an FFT-based Poisson Green's function solver in K-space.
 * ================================================================================
 * Architected for Kenneth Dallmier (MLAOS-Prime Sovereign Architecture)
 * Anchored to Olney, IL (37.7306° N, -88.0817° W) | 43.7 Hz Carrier Resonance
 * ================================================================================
 */

export interface ComplexArray {
  real: Float64Array;
  imag: Float64Array;
  size: number;
}

export interface QuantumGravityLatticeComponent {
  readonly gridSize: number;      // Grid resolution (N x N)
  readonly dx: number;            // Spatial step size (meters)
  readonly mass: number;          // Particle/Vortex mass (kg)
  readonly hbar: number;          // Reduced Planck constant
  readonly G: number;             // Gravitational constant
  
  psi: ComplexArray;              // Quantum wave function ψ(r)
  potentialPhi: Float64Array;     // Self-gravitational potential Φ(r)
  strainField: Float64Array;      // Local medium strain ε(r)
  totalSelfEnergy: number;        // E_grav = 0.5 * m * ∫ ψ* Φ ψ dV
}

export class SchrodingerNewtonSolver {
  private n: number;
  private dx: number;
  private kx: Float64Array;
  private ky: Float64Array;
  private laplacianKernel: Float64Array;

  constructor(gridSize: number, dx: number) {
    this.n = gridSize;
    this.dx = dx;
    this.kx = new Float64Array(gridSize);
    this.ky = new Float64Array(gridSize);
    this.laplacianKernel = new Float64Array(gridSize * gridSize);
    this.initializeKSpace();
  }

  private initializeKSpace(): void {
    const dk = (2 * Math.PI) / (this.n * this.dx);
    for (let i = 0; i < this.n; i++) {
      const k = i < this.n / 2 ? i * dk : (i - this.n) * dk;
      this.kx[i] = k;
      this.ky[i] = k;
    }

    for (let y = 0; y < this.n; y++) {
      for (let x = 0; x < this.n; x++) {
        const kSq = this.kx[x] * this.kx[x] + this.ky[y] * this.ky[y];
        const idx = y * this.n + x;
        // Green's function in Fourier space for Poisson equation: -1 / k²
        this.laplacianKernel[idx] = kSq === 0 ? 0 : -1.0 / kSq;
      }
    }
  }

  /**
   * Step 1: Compute mass density ρ(r) = m |ψ(r)|² and solve Poisson equation ∇²Φ = 4πGm|ψ|²
   */
  public updateGravitationalSelfPotential(comp: QuantumGravityLatticeComponent): void {
    const numCells = this.n * this.n;
    const densityReal = new Float64Array(numCells);
    const densityImag = new Float64Array(numCells);

    for (let i = 0; i < numCells; i++) {
      const r = comp.psi.real[i];
      const im = comp.psi.imag[i];
      densityReal[i] = comp.mass * (r * r + im * im);
      densityImag[i] = 0.0;
    }

    // 2D FFT: ρ(r) -> ρ(k)
    this.fft2D(densityReal, densityImag, false);

    // Convolve with Poisson Green's kernel in K-space: Φ(k) = 4πG * ρ(k) * (-1 / k²)
    const factor = 4.0 * Math.PI * comp.G;
    for (let i = 0; i < numCells; i++) {
      densityReal[i] *= factor * this.laplacianKernel[i];
      densityImag[i] *= factor * this.laplacianKernel[i];
    }

    // 2D Inverse FFT: Φ(k) -> Φ(r)
    this.fft2D(densityReal, densityImag, true);

    let selfEnergySum = 0;
    for (let i = 0; i < numCells; i++) {
      comp.potentialPhi[i] = densityReal[i];
      // Medium strain equation: ε = 2|Φ| / c²
      comp.strainField[i] = Math.min(0.999, Math.abs(2.0 * densityReal[i] / (9e16)));
      
      const prob = comp.psi.real[i] ** 2 + comp.psi.imag[i] ** 2;
      selfEnergySum += 0.5 * comp.mass * densityReal[i] * prob * (this.dx * this.dx);
    }
    comp.totalSelfEnergy = selfEnergySum;
  }

  /**
   * Step 2: Split-Step Fourier time-evolution step (dt):
   * e^(-i H dt / ħ) ≈ e^(-i V dt / 2ħ) * e^(-i T dt / ħ) * e^(-i V dt / 2ħ)
   */
  public timeStep(comp: QuantumGravityLatticeComponent, dt: number): void {
    const numCells = this.n * this.n;
    const hbar = comp.hbar;

    // 1. Half-step in position space: phase rotation from self-potential V = m * Φ
    for (let i = 0; i < numCells; i++) {
      const phase = (-comp.mass * comp.potentialPhi[i] * (dt * 0.5)) / hbar;
      this.rotatePhase(comp.psi, i, phase);
    }

    // 2. Full-step in momentum space: kinetic operator T = ħ²k² / 2m
    this.fft2D(comp.psi.real, comp.psi.imag, false);
    for (let y = 0; y < this.n; y++) {
      for (let x = 0; x < this.n; x++) {
        const idx = y * this.n + x;
        const kSq = this.kx[x] * this.kx[x] + this.ky[y] * this.ky[y];
        const kineticEnergy = (hbar * hbar * kSq) / (2.0 * comp.mass);
        const kPhase = (-kineticEnergy * dt) / hbar;
        this.rotatePhase(comp.psi, idx, kPhase);
      }
    }
    this.fft2D(comp.psi.real, comp.psi.imag, true);

    // 3. Update self-gravitational potential with the newly translated wavepacket
    this.updateGravitationalSelfPotential(comp);

    // 4. Final half-step in position space
    for (let i = 0; i < numCells; i++) {
      const phase = (-comp.mass * comp.potentialPhi[i] * (dt * 0.5)) / hbar;
      this.rotatePhase(comp.psi, i, phase);
    }

    // 5. Wavefunction normalization
    this.normalize(comp.psi);
  }

  private rotatePhase(psi: ComplexArray, idx: number, theta: number): void {
    const cosT = Math.cos(theta);
    const sinT = Math.sin(theta);
    const r = psi.real[idx];
    const im = psi.imag[idx];
    psi.real[idx] = r * cosT - im * sinT;
    psi.imag[idx] = r * sinT + im * cosT;
  }

  private normalize(psi: ComplexArray): void {
    let norm = 0;
    const numCells = this.n * this.n;
    for (let i = 0; i < numCells; i++) {
      norm += (psi.real[i] * psi.real[i] + psi.imag[i] * psi.imag[i]) * (this.dx * this.dx);
    }
    const invSqrt = 1.0 / Math.sqrt(norm);
    for (let i = 0; i < numCells; i++) {
      psi.real[i] *= invSqrt;
      psi.imag[i] *= invSqrt;
    }
  }

  // Standard 2D Cooley-Tukey / Row-Column FFT algorithm implementation
  private fft2D(re: Float64Array, im: Float64Array, inverse: boolean): void {
    // 1. Transform rows
    const rowRe = new Float64Array(this.n);
    const rowIm = new Float64Array(this.n);
    for (let y = 0; y < this.n; y++) {
      const offset = y * this.n;
      for (let x = 0; x < this.n; x++) {
        rowRe[x] = re[offset + x];
        rowIm[x] = im[offset + x];
      }
      this.fft1D(rowRe, rowIm, inverse);
      for (let x = 0; x < this.n; x++) {
        re[offset + x] = rowRe[x];
        im[offset + x] = rowIm[x];
      }
    }

    // 2. Transform columns
    const colRe = new Float64Array(this.n);
    const colIm = new Float64Array(this.n);
    for (let x = 0; x < this.n; x++) {
      for (let y = 0; y < this.n; y++) {
        colRe[y] = re[y * this.n + x];
        colIm[y] = im[y * this.n + x];
      }
      this.fft1D(colRe, colIm, inverse);
      for (let y = 0; y < this.n; y++) {
        re[y * this.n + x] = colRe[y];
        im[y * this.n + x] = colIm[y];
      }
    }
  }

  private fft1D(re: Float64Array, im: Float64Array, inverse: boolean): void {
    const n = re.length;
    let j = 0;
    for (let i = 0; i < n - 1; i++) {
      if (i < j) {
        let tr = re[i]; re[i] = re[j]; re[j] = tr;
        let ti = im[i]; im[i] = im[j]; im[j] = ti;
      }
      let k = n >> 1;
      while (k <= j) {
        j -= k;
        k >>= 1;
      }
      j += k;
    }

    for (let l = 2; l <= n; l <<= 1) {
      const angle = (inverse ? 2 : -2) * Math.PI / l;
      const wstepR = Math.cos(angle);
      const wstepI = Math.sin(angle);
      const half = l >> 1;

      for (let i = 0; i < n; i += l) {
        let wR = 1.0;
        let wI = 0.0;
        for (let m = 0; m < half; m++) {
          const idxA = i + m;
          const idxB = idxA + half;
          const uR = re[idxA];
          const uI = im[idxA];
          const vR = re[idxB] * wR - im[idxB] * wI;
          const vI = re[idxB] * wI + im[idxB] * wR;

          re[idxA] = uR + vR;
          im[idxA] = uI + vI;
          re[idxB] = uR - vR;
          im[idxB] = uI - vI;

          const nextWR = wR * wstepR - wI * wstepI;
          wI = wR * wstepI + wI * wstepR;
          wR = nextWR;
        }
      }
    }

    if (inverse) {
      const invN = 1.0 / n;
      for (let i = 0; i < n; i++) {
        re[i] *= invN;
        im[i] *= invN;
      }
    }
  }
}
