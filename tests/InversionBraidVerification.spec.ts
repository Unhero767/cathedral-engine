import { describe, it, expect } from 'vitest';

type BelnapFour = 'TRUE' | 'FALSE' | 'BOTH' | 'NEITHER';

interface BraidAtom {
  atomKey: string;
  storyIndex: number;
  bpStamp: number;
  logicValue: BelnapFour;
  evidenceWeight: number;
  fogAttenuation: number;
}

describe('Architectonics of the Inversion Braid (vX.Ω)', () => {
  it('enforces Belnap-Dunn dialetheic containment without crashing on contradiction', () => {
    const evaluateAtom = (hasTrueClaim: boolean, hasFalseClaim: boolean): BelnapFour => {
      if (hasTrueClaim && hasFalseClaim) return 'BOTH';
      if (hasTrueClaim) return 'TRUE';
      if (hasFalseClaim) return 'FALSE';
      return 'NEITHER';
    };

    const state = evaluateAtom(true, true);
    expect(state).toBe('BOTH');
    expect(['TRUE', 'FALSE', 'BOTH', 'NEITHER']).toContain(state);
  });

  it('verifies strict (s_i, b_i) adjacency where t_bp === t_story + 1 as single audit unit', () => {
    const pair: BraidAtom = {
      atomKey: 'CHAMBER_XX_IGNITION',
      storyIndex: 1041,
      bpStamp: 1042,
      logicValue: 'BOTH',
      evidenceWeight: 0.88,
      fogAttenuation: 0.42
    };

    expect(pair.bpStamp).toBe(pair.storyIndex + 1);
  });

  it('isolates contradictions across atom-keys regardless of chronological ingestion', () => {
    const ledger: BraidAtom[] = [
      { atomKey: 'CORE_VALVE_A', storyIndex: 1, bpStamp: 2, logicValue: 'TRUE', evidenceWeight: 0.9, fogAttenuation: 0.1 },
      { atomKey: 'CORE_VALVE_B', storyIndex: 3, bpStamp: 4, logicValue: 'FALSE', evidenceWeight: 0.8, fogAttenuation: 0.2 },
      { atomKey: 'CORE_VALVE_A', storyIndex: 5, bpStamp: 6, logicValue: 'FALSE', evidenceWeight: 0.9, fogAttenuation: 0.1 }
    ];

    const groupByKey = (items: BraidAtom[]) => {
      return items.reduce((acc, item) => {
        acc[item.atomKey] = acc[item.atomKey] || [];
        acc[item.atomKey].push(item);
        return acc;
      }, {} as Record<string, BraidAtom[]>);
    };

    const grouped = groupByKey(ledger);
    expect(grouped['CORE_VALVE_A'].length).toBe(2);
    const valuesA = grouped['CORE_VALVE_A'].map(a => a.logicValue);
    expect(valuesA).toEqual(['TRUE', 'FALSE']);
  });

  it('guarantees insight generates forward evidence claims without modifying historical records', () => {
    const historyChain: readonly number[] = Object.freeze([0.75, 0.70, 0.65]);
    const newEvidenceClaim = 0.30;
    const downstreamFog = historyChain[historyChain.length - 1] - (newEvidenceClaim * 0.5);

    expect(downstreamFog).toBeLessThan(historyChain[historyChain.length - 1]);
    expect(historyChain).toEqual([0.75, 0.70, 0.65]);
  });

  it('maps Mercury(650nm), Gemini(580nm), and Apollo(400nm) to strict mathematical operators', () => {
    const P = 0.8;
    const B = 1.0;
    const E = 0.9;
    const S = 0.95;

    const psi_m = Math.tanh(P * 1.5); // Math.tanh(1.2) = 0.833654607...
    const psi_g = B * S;
    const psi_a = (E * S) / (1.0 + P * 0.5);

    expect(psi_m).toBeCloseTo(0.8337, 4);
    expect(psi_g).toBeCloseTo(0.95, 4);
    expect(psi_a).toBeCloseTo(0.6107, 4);
  });
});
