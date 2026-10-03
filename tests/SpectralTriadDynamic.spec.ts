import { describe, it, expect } from 'vitest';

export type BelnapFour = 'TRUE' | 'FALSE' | 'BOTH' | 'NEITHER';

export interface BraidEnvironmentState {
  pressure: number;      // P in [0, 1]
  contradiction: number; // B in [0, 1]
  evidence: number;      // E in [0, 1]
  stability: number;     // S in [0, 1]
  hasTrueClaim: boolean;
  hasFalseClaim: boolean;
}

export interface SpectralTriadOutput {
  psi_m: number;           // Mercury 650nm (Kinetic Fracture / Thrust)
  psi_g: number;           // Gemini 580nm (Dialectic Arbitration)
  psi_a: number;           // Apollo 400nm (Trajectory Coherence)
  belnap: BelnapFour;
  mercuryParticles: number;
  upperApseStability: number;
  fogWidth: number;
}

export interface AshLedgerEntry {
  storyIndex: number;
  bpStamp: number;
  merkleHash: string;
}

export class InversionBraidSimulation {
  private currentCycle = 0;
  public ledger: AshLedgerEntry[] = [];

  public resolveBelnap(hasTrue: boolean, hasFalse: boolean): BelnapFour {
    if (hasTrue && hasFalse) return 'BOTH';
    if (hasTrue) return 'TRUE';
    if (hasFalse) return 'FALSE';
    return 'NEITHER';
  }

  public step(state: BraidEnvironmentState): SpectralTriadOutput {
    this.currentCycle++;

    // 1. Mercury Evaluation (P-driven kinetic ignition)
    const psi_m = Math.tanh(state.pressure * 1.5);
    const mercuryParticles = Math.floor(psi_m * 100);

    // 2. Gemini Evaluation (Dialetheic containment & counter-cadence)
    const belnap = this.resolveBelnap(state.hasTrueClaim, state.hasFalseClaim);
    let dialetheicMultiplier = 1.0;
    if (belnap === 'BOTH') {
      // Inversion Braid: Dialetheic collision converts contradiction into stable containment tension
      dialetheicMultiplier = 1.0 + (state.contradiction * 0.2);
    }
    const psi_g = Math.min(1.0, state.contradiction * state.stability * dialetheicMultiplier);

    // Upper apse stability remains strictly decoupled from lower exhaust pressure
    const upperApseStability = state.stability * (1.0 - (1.0 - psi_g) * 0.1);

    // 3. Apollo Evaluation (Evidence & Stability narrow fog into trajectory filaments)
    const psi_a = (state.evidence * state.stability) / (1.0 + state.pressure * 0.5);
    // Proposition 4: Fog width narrows strictly as Evidence increases
    const fogWidth = Math.max(0.05, 1.0 - (state.evidence * 0.9));

    // 4. Inscription Step: Strict t_bp = t_story + 1 adjacency
    const storyIndex = this.currentCycle * 2 - 1;
    const bpStamp = storyIndex + 1;
    const merkleHash = `0x${((this.currentCycle * 31337) ^ 0xDEADBEEF).toString(16).toUpperCase()}`;

    this.ledger.push({ storyIndex, bpStamp, merkleHash });

    return {
      psi_m,
      psi_g,
      psi_a,
      belnap,
      mercuryParticles,
      upperApseStability,
      fogWidth
    };
  }
}

describe('Ω-ONT-001 Inversion Braid Dynamic Verifications', () => {
  // TEST 1: Mercury Layer Isolation
  it('Mercury Layer (Base): spikes kinetic fracture count with P without destabilizing the upper apse', () => {
    const sim = new InversionBraidSimulation();

    // Baseline low pressure
    const baseline = sim.step({
      pressure: 0.1,
      contradiction: 0.5,
      evidence: 0.8,
      stability: 0.95,
      hasTrueClaim: true,
      hasFalseClaim: false
    });

    // High pressure spike
    const spiked = sim.step({
      pressure: 0.95,
      contradiction: 0.5,
      evidence: 0.8,
      stability: 0.95,
      hasTrueClaim: true,
      hasFalseClaim: false
    });

    // Fracture count must surge with pressure
    expect(spiked.mercuryParticles).toBeGreaterThan(baseline.mercuryParticles * 3);
    expect(spiked.psi_m).toBeGreaterThan(baseline.psi_m);

    // Crucial Invariant: Base exhaust pressure MUST NOT degrade upper apse stability
    expect(spiked.upperApseStability).toBeCloseTo(baseline.upperApseStability, 2);
    expect(spiked.upperApseStability).toBeGreaterThan(0.90);
  });

  // TEST 2: Gemini Core Paraconsistent Containment
  it('Gemini Core (Mid): toggling A ∧ ¬A resolves to BOTH, preserving continuous counter-cadence without crash', () => {
    const sim = new InversionBraidSimulation();

    const output = sim.step({
      pressure: 0.5,
      contradiction: 0.95,
      evidence: 0.7,
      stability: 0.9,
      hasTrueClaim: true,
      hasFalseClaim: true // Dialetheic collision active
    });

    // Zero crash, state is preserved as BOTH
    expect(output.belnap).toBe('BOTH');
    expect(output.psi_g).toBeGreaterThan(0.80);
    // Dialetheic tension holds structural integrity
    expect(output.upperApseStability).toBeGreaterThan(0.85);
  });

  // TEST 3: Apollo Crown & Proposition 4
  it('Apollo Crown (Pinnacle): high Evidence and Stability narrow downstream fog into vertical laser filaments', () => {
    const sim = new InversionBraidSimulation();

    // Low evidence condition (high fog)
    const foggedState = sim.step({
      pressure: 0.3,
      contradiction: 0.2,
      evidence: 0.1,
      stability: 0.5,
      hasTrueClaim: true,
      hasFalseClaim: false
    });

    // High evidence & stability condition (distinguishability crystallized)
    const clearState = sim.step({
      pressure: 0.3,
      contradiction: 0.2,
      evidence: 0.95,
      stability: 0.95,
      hasTrueClaim: true,
      hasFalseClaim: false
    });

    // Fog width collapses toward zero (laser filament)
    expect(clearState.fogWidth).toBeLessThan(foggedState.fogWidth * 0.2);
    // Trajectory coherence maximizes
    expect(clearState.psi_a).toBeGreaterThan(foggedState.psi_a * 4);
    expect(clearState.psi_a).toBeGreaterThan(0.60);
  });

  // TEST 4: Ash Archive Merkle Adjacency
  it('Ash Archive Ledger: confirms strict t_bp = t_story + 1 adjacency across all step operations', () => {
    const sim = new InversionBraidSimulation();

    for (let i = 0; i < 10; i++) {
      sim.step({
        pressure: 0.4 + (i * 0.05),
        contradiction: 0.5,
        evidence: 0.8,
        stability: 0.9,
        hasTrueClaim: i % 2 === 0,
        hasFalseClaim: true
      });
    }

    expect(sim.ledger.length).toBe(10);

    // Verify adjacency invariant for every single recorded entry
    for (const record of sim.ledger) {
      expect(record.bpStamp).toBe(record.storyIndex + 1);
      expect(record.merkleHash.startsWith('0x')).toBe(true);
    }
  });
});
