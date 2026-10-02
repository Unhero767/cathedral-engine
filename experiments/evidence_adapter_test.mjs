import assert from "node:assert/strict";
import { EpistemicField } from "./evidence_adapter.mjs";

const field = new EpistemicField();

// Step 1: Inject Contradiction
field.applyObservation({ contradictionInput: 0.6, evidenceInput: 0.0 });
assert.equal(field.contradiction, 0.6);
assert.ok(field.pressure > 0, "Pressure must be greater than zero after contradiction.");

const pressureAfterContradiction = field.pressure;

// Step 2: Inject Evidence (Dampens pressure without erasing contradiction history)
field.applyObservation({ contradictionInput: 0.0, evidenceInput: 0.4 });
assert.equal(field.contradiction, 0.6, "Historical contradiction must remain preserved.");
assert.equal(field.evidence, 0.4);
assert.ok(field.pressure < pressureAfterContradiction, "Evidence must successfully reduce active pressure.");

console.log("Ω-ONT-001 — MILESTONE 04");
console.log("STATUS: PASS");
console.log("CONTRADICTION PRESERVED: 0.6");
console.log("EVIDENCE DAMPENING: ACTIVE");
console.log(`FINAL STABILITY: ${field.stability}`);
