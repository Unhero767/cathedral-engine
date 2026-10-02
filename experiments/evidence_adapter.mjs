/**
 * Ω-ONT-001 — Milestone 04
 * Evidence & Pressure Damping Adapter
 *
 * Governs the dynamic feedback loop:
 * contradiction → pressure → investigation → evidence → stability
 * 
 * Historical contradiction is preserved; active pressure is dampened by evidence.
 */

export class EpistemicField {
  constructor({ contradiction = 0, pressure = 0, evidence = 0, stability = 1.0 } = {}) {
    this.contradiction = contradiction;
    this.pressure = pressure;
    this.evidence = evidence;
    this.stability = stability;
    this.history = [];
  }

  applyObservation({ contradictionInput = 0, evidenceInput = 0 } = {}) {
    // Record immutable historical trace step using push()
    this.history.push({
      contradictionPrior: this.contradiction,
      evidencePrior: this.evidence,
      incomingContradiction: contradictionInput,
      incomingEvidence: evidenceInput
    });

    // Cumulative contradiction (history is preserved)
    this.contradiction = Number((this.contradiction + contradictionInput).toFixed(4));
    
    // Evidence accumulates
    this.evidence = Number((this.evidence + evidenceInput).toFixed(4));
    
    // Pressure formula: Contradiction drives pressure up, Evidence dampens it down
    const rawPressure = (this.contradiction * 2.0) - (this.evidence * 1.5);
    this.pressure = Number(Math.max(0.0, rawPressure).toFixed(4));
    
    // Stability is inversely bounded by active pressure
    this.stability = Number(Math.max(0.0, 1.0 - (this.pressure * 0.5)).toFixed(4));
  }
}
