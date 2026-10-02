import assert from "node:assert/strict";
import {
  BP,
  SIGMA,
  TAU,
  classify,
  contradictionFor,
  createProposition,
  evaluateClaims,
  fogFor,
  sigmaFor,
} from "./bp_adapter.mjs";

assert.equal(classify({ positive: true, negative: false }), BP.T);
assert.equal(classify({ positive: false, negative: true }), BP.F);
assert.equal(classify({ positive: true, negative: true }), BP.B);
assert.equal(classify({ positive: false, negative: false }), BP.N);

assert.equal(sigmaFor(BP.T), SIGMA.PROVEN);
assert.equal(sigmaFor(BP.F), SIGMA.DISPROVEN);
assert.equal(sigmaFor(BP.B), SIGMA.INCONSISTENT);
assert.equal(sigmaFor(BP.N), SIGMA.UNRESOLVED);

assert.equal(fogFor(BP.T), 0);
assert.equal(fogFor(BP.F), 0);
assert.equal(fogFor(BP.B), 2);
assert.equal(fogFor(BP.N), 1);

assert.equal(contradictionFor(BP.B), 1);
assert.equal(contradictionFor(BP.T), 0);

const positive = createProposition({
  atomKey: "gate:open",
  phi: "The gate is open.",
  positive: true,
  confidence: 0.9,
  tau: TAU.T3_TESTIMONIAL,
  turn: 4,
});

const negative = createProposition({
  atomKey: "gate:open",
  phi: "The gate is closed.",
  negative: true,
  confidence: 0.8,
  tau: TAU.T3_TESTIMONIAL,
  turn: 5,
});

assert.match(positive.phi, /^At Turn 4:/);
assert.match(negative.phi, /^At Turn 5:/);
assert.equal(positive.atomKey, negative.atomKey);

const evaluated = evaluateClaims([positive, negative]);
assert.equal(evaluated.length, 1);
assert.equal(evaluated[0].atomKey, "gate:open");
assert.equal(evaluated[0].bp, BP.B);
assert.equal(evaluated[0].sigma, SIGMA.INCONSISTENT);
assert.equal(evaluated[0].fog, 2);
assert.equal(evaluated[0].contradiction, 1);
assert.equal(evaluated[0].confidence, 0.85);

console.log("Ω-ONT-001 — MILESTONE 03");
console.log("STATUS: PASS");
console.log("BP: T / F / B / N");
console.log("ATOM GROUPING: atomKey");
console.log("CONTRADICTION: B → INCONSISTENT");
console.log("FOG: B → 2");
console.log("TIME-SCOPED PHI: preserved");
console.log("TESTS: PASS");
