import assert from "node:assert/strict";
import { AshArchiveLedger } from "./ash_archive_adapter.mjs";

const ledger = new AshArchiveLedger();

ledger.recordCycle({
  turn: 10,
  storyData: { event: "The chamber resonates with gold joy." },
  bpState: { evaluation: "T", harmonicScars: 0 }
});

ledger.recordCycle({
  turn: 12,
  storyData: { event: "Contradiction pressure spikes in the outer choir." },
  bpState: { evaluation: "B", harmonicScars: 2 }
});

assert.ok(ledger.verifyAdjacency(), "Ash Archive adjacency invariant must hold.");

const serialized = ledger.exportSerialized();
const shuffled = JSON.parse(serialized).sort(() => Math.random() - 0.5);

const recoveredLedger = new AshArchiveLedger();
recoveredLedger.importSerialized(JSON.stringify(shuffled));

assert.ok(recoveredLedger.verifyAdjacency(), "Adjacency must survive sorting and deserialization.");

console.log("Ω-ONT-001 — MILESTONE 05");
console.log("STATUS: PASS");
console.log("STORY(t) → BP(t + 1) INVARIANT: VERIFIED");
console.log("PROVENANCE ADJACENCY: RESILIENT TO DESERIALIZATION & SORTING");
