import assert from "node:assert/strict";
import { CathedralSerializer } from "./serializer_adapter.mjs";

const mockState = {
  experiment: "Ω-ONT-001",
  seed: "Ω-001-32",
  turn: 10,
  contradiction: 0.125,
  stability: 0.8975,
  belnapDunn: { T: 0.5, F: 0.2, B: 0.1, N: 0.2, harmonicScars: 1 }
};

const mockLedger = [
  { index: 0, tier: "STORY", payload: { event: "Genesis altar." }, parentHash: "0".repeat(64), hash: "1111..." },
  { index: 1, tier: "BP", payload: { evaluation: "T" }, parentHash: "1111...", hash: "2222..." }
];

const mockTrace = {
  seed: "Ω-001-32",
  interactions: [{ type: "observe", value: 0.75 }]
};

const exportStr = CathedralSerializer.exportPackage({
  state: mockState,
  ledger: mockLedger,
  trace: mockTrace
});

assert.ok(exportStr, "Serializer must generate an export string.");

const imported = CathedralSerializer.importPackage(exportStr);
assert.ok(imported.valid, "Imported package must pass checksum verification.");
assert.deepEqual(imported.state, mockState, "Exported and imported states must match precisely.");
assert.deepEqual(imported.ledger, mockLedger, "Ledger chains must remain lossless.");
assert.deepEqual(imported.trace, mockTrace, "Interaction trace must be preserved.");

const tamperedObj = JSON.parse(exportStr);
tamperedObj.payload.state.stability = 0.1;
const tamperedStr = JSON.stringify(tamperedObj);

assert.throws(() => {
  CathedralSerializer.importPackage(tamperedStr);
}, /Checksum verification failed/, "Tampered package imports must trigger a checksum rejection.");

console.log("Ω-ONT-001 — MILESTONE 07");
console.log("STATUS: PASS");
console.log("STATE EXPORT/IMPORT SERIALIZER: VERIFIED");
console.log("SHA-256 PACKAGE INTEGRITY & TAMPER DEFENSE: ACTIVE");
