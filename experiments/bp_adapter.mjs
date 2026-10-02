/**
 * Ω-ONT-001 — Milestone 03
 * BP / Belnap-Dunn T/F/B/N Adapter
 */

export const BP = Object.freeze({
  T: "T",
  F: "F",
  B: "B",
  N: "N",
});

export const SIGMA = Object.freeze({
  PROVEN: "PROVEN",
  DISPROVEN: "DISPROVEN",
  INCONSISTENT: "INCONSISTENT",
  UNRESOLVED: "UNRESOLVED",
});

export const TAU = Object.freeze({
  T5_EMPIRICAL: "T5_EMPIRICAL",
  T4_STRUCTURAL: "T4_STRUCTURAL",
  T3_TESTIMONIAL: "T3_TESTIMONIAL",
  T2_INFERRED: "T2_INFERRED",
  T1_HYPOTHETICAL: "T1_HYPOTHETICAL",
});

export function classify({ positive = false, negative = false } = {}) {
  if (positive && negative) return BP.B;
  if (positive) return BP.T;
  if (negative) return BP.F;
  return BP.N;
}

export function sigmaFor(bp) {
  switch (bp) {
    case BP.T: return SIGMA.PROVEN;
    case BP.F: return SIGMA.DISPROVEN;
    case BP.B: return SIGMA.INCONSISTENT;
    case BP.N:
    default: return SIGMA.UNRESOLVED;
  }
}

export function fogFor(bp) {
  switch (bp) {
    case BP.B: return 2;
    case BP.N: return 1;
    case BP.T:
    case BP.F:
    default: return 0;
  }
}

export function contradictionFor(bp) {
  return bp === BP.B ? 1 : 0;
}

export function createProposition({
  atomKey,
  phi,
  positive = false,
  negative = false,
  confidence = 0,
  tau = TAU.T3_TESTIMONIAL,
  turn = 0,
} = {}) {
  if (!atomKey) throw new TypeError("atomKey is required");
  const bp = classify({ positive, negative });
  return Object.freeze({
    atomKey,
    phi: `At Turn ${turn}: ${phi ?? ""}`.trim(),
    bp,
    sigma: sigmaFor(bp),
    tau,
    confidence: Math.max(0, Math.min(1, confidence)),
    fog: fogFor(bp),
    contradiction: contradictionFor(bp),
    turn,
    positive,
    negative,
  });
}

export function evaluateAtom(claims = []) {
  const positive = claims.some((c) => c.positive || c.bp === BP.T || c.bp === BP.B || c.polarity === "positive");
  const negative = claims.some((c) => c.negative || c.bp === BP.F || c.bp === BP.B || c.polarity === "negative");
  const bp = classify({ positive, negative });
  const rawConfidence = claims.length === 0 ? 0 : claims.reduce((sum, claim) => sum + Math.max(0, Math.min(1, claim.confidence ?? 0)), 0) / claims.length;
  const confidence = Number(rawConfidence.toFixed(4));
  return Object.freeze({
    bp,
    sigma: sigmaFor(bp),
    fog: fogFor(bp),
    contradiction: contradictionFor(bp),
    confidence,
  });
}

export function groupByAtomKey(claims = []) {
  const groups = new Map();
  for (const claim of claims) {
    if (!groups.has(claim.atomKey)) groups.set(claim.atomKey, []);
    groups.get(claim.atomKey).push(claim);
  }
  return groups;
}

export function evaluateClaims(claims = []) {
  const groups = groupByAtomKey(claims);
  return [...groups.entries()].map(([atomKey, atomClaims]) => ({
    atomKey,
    claims: atomClaims,
    ...evaluateAtom(atomClaims),
  }));
}
