import assert from "node:assert/strict";
import { MerkleArchiveLedger } from "./merkle_adapter.mjs";

const ledger = new MerkleArchiveLedger();

ledger.appendEntry({ tier: "STORY", content: "The first altar is cast in gold." });
ledger.appendEntry({ tier: "BP", content: "State evaluated as Proven (T)." });
ledger.appendEntry({ tier: "STORY", content: "A shadow fractures the northern wall." });
ledger.appendEntry({ tier: "BP", content: "State evaluated as Inconsistent (B / Harmonic Scar)." });

const initialCheck = ledger.verifyIntegrity();
assert.ok(initialCheck.valid, "Pristine Merkle ledger must pass integrity validation.");

ledger.tamperPayload(1, { tier: "BP", content: "Tampered state history." });

const compromisedCheck = ledger.verifyIntegrity();
assert.equal(compromisedCheck.valid, false, "Tampering must be caught by hash chain verification.");
assert.equal(compromisedCheck.brokenIndex, 1, "Compromised index must be precisely identified.");

console.log("Ω-ONT-001 — MILESTONE 06");
console.log("STATUS: PASS");
console.log("MERKLE DAG CHAINING: VERIFIED");
console.log("TAMPER DETECTION: ACTIVE & PRECISION-BOUND");
