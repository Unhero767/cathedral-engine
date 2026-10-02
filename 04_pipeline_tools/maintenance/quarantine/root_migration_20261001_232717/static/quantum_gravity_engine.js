/**
 * ================================================================================
 * CATHEDRAL-ENGINE :: CLIENT-SIDE QUANTUM GRAVITY SCHRÖDINGER-NEWTON ENGINE (JS)
 * ================================================================================
 * Browser-compatible Split-Step Fourier & FFT Poisson Solver for Web Altar
 * ================================================================================
 */

class BrowserSchrodingerNewtonSolver {
  constructor(gridSize = 32, dx = 1.0e-15, mass = 1.0e-20) {
    this.n = gridSize;
    this.dx = dx;
    this.mass = mass;
    this.hbar = 1.054571817e-34;
    this.G = 6.67430e-11;
    this.c = 299792458.0;

    const numCells = this.n * this.n;
    this.psi = {
      real: new Float64Array(numCells),
      imag: new Float64Array(numCells),
      size: numCells
    };
    this.potentialPhi = new Float64Array(numCells);
    this.strainField = new Float64Array(numCells);
    this.totalSelfEnergy = 0;

    this.kx = new Float64Array(this.n);
    this.ky = new Float64Array(this.n);
    this.laplacianKernel = new Float64Array(numCells);

    this.initializeKSpace();
    this.initializeGaussian();
    this.updateGravitationalSelfPotential();
  }

  initializeKSpace() {
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
        this.laplacianKernel[idx] = kSq === 0 ? 0 : -1.0 / kSq;
      }
    }
  }

  initializeGaussian(sigmaFactor = 4.0) {
    const center = this.n / 2.0;
    const sigma = (this.n * this.dx) / sigmaFactor;
    const numCells = this.n * this.n;

    for (let y = 0; y < this.n; y++) {
      const ry = (y - center) * this.dx;
      for (let x = 0; x < this.n; x++) {
        const rx = (x - center) * this.dx;
        const rSq = rx * rx + ry * ry;
        const val = Math.exp(-rSq / (2.0 * sigma * sigma));
        const idx = y * this.n + x;
        this.psi.real[idx] = val;
        this.psi.imag[idx] = 0.0;
      }
    }
    this.normalize();
  }

  updateGravitationalSelfPotential() {
    const numCells = this.n * this.n;
    const densityReal = new Float64Array(numCells);
    const densityImag = new Float64Array(numCells);

    for (let i = 0; i < numCells; i++) {
      const r = this.psi.real[i];
      const im = this.psi.imag[i];
      densityReal[i] = this.mass * (r * r + im * im);
      densityImag[i] = 0.0;
    }

    this.fft2D(densityReal, densityImag, false);

    const factor = 4.0 * Math.PI * this.G;
    for (let i = 0; i < numCells; i++) {
      densityReal[i] *= factor * this.laplacianKernel[i];
      densityImag[i] *= factor * this.laplacianKernel[i];
    }

    this.fft2D(densityReal, densityImag, true);

    let selfEnergySum = 0;
    const cSq = this.c * this.c;
    for (let i = 0; i < numCells; i++) {
      this.potentialPhi[i] = densityReal[i];
      this.strainField[i] = Math.min(0.999, Math.abs(2.0 * densityReal[i] / cSq));
      const prob = this.psi.real[i] ** 2 + this.psi.imag[i] ** 2;
      selfEnergySum += 0.5 * this.mass * densityReal[i] * prob * (this.dx * this.dx);
    }
    this.totalSelfEnergy = selfEnergySum;
  }

  timeStep(dt = 1.0e-18) {
    const numCells = this.n * this.n;
    const hbar = this.hbar;

    // 1. Half-step in position space: V = m * Phi
    for (let i = 0; i < numCells; i++) {
      const phase = (-this.mass * this.potentialPhi[i] * (dt * 0.5)) / hbar;
      this.rotatePhase(i, phase);
    }

    // 2. Full-step in momentum space: T = hbar^2 k^2 / 2m
    this.fft2D(this.psi.real, this.psi.imag, false);
    for (let y = 0; y < this.n; y++) {
      for (let x = 0; x < this.n; x++) {
        const idx = y * this.n + x;
        const kSq = this.kx[x] * this.kx[x] + this.ky[y] * this.ky[y];
        const kineticEnergy = (hbar * hbar * kSq) / (2.0 * this.mass);
        const kPhase = (-kineticEnergy * dt) / hbar;
        this.rotatePhase(idx, kPhase);
      }
    }
    this.fft2D(this.psi.real, this.psi.imag, true);

    // 3. Update self-gravitational potential
    this.updateGravitationalSelfPotential();

    // 4. Final half-step in position space
    for (let i = 0; i < numCells; i++) {
      const phase = (-this.mass * this.potentialPhi[i] * (dt * 0.5)) / hbar;
      this.rotatePhase(i, phase);
    }

    // 5. Normalization
    this.normalize();
  }

  rotatePhase(idx, theta) {
    const cosT = Math.cos(theta);
    const sinT = Math.sin(theta);
    const r = this.psi.real[idx];
    const im = this.psi.imag[idx];
    this.psi.real[idx] = r * cosT - im * sinT;
    this.psi.imag[idx] = r * sinT + im * cosT;
  }

  normalize() {
    let norm = 0;
    const numCells = this.n * this.n;
    for (let i = 0; i < numCells; i++) {
      norm += (this.psi.real[i] * this.psi.real[i] + this.psi.imag[i] * this.psi.imag[i]) * (this.dx * this.dx);
    }
    if (norm > 0) {
      const invSqrt = 1.0 / Math.sqrt(norm);
      for (let i = 0; i < numCells; i++) {
        this.psi.real[i] *= invSqrt;
        this.psi.imag[i] *= invSqrt;
      }
    }
  }

  fft2D(re, im, inverse) {
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

  fft1D(re, im, inverse) {
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

  computeDiosiPenroseDecoherence(displacementDx) {
    const effectiveR = Math.max(this.dx, displacementDx);
    const deltaEG = (2.0 * this.G * (this.mass ** 2)) / effectiveR;
    const tauDecay = this.hbar / Math.max(1e-50, deltaEG);
    return {
      massKg: this.mass,
      displacementM: displacementDx,
      deltaEGJoules: deltaEG,
      tauDecaySeconds: tauDecay
    };
  }
}

if (typeof window !== 'undefined') {
  window.BrowserSchrodingerNewtonSolver = BrowserSchrodingerNewtonSolver;
}
