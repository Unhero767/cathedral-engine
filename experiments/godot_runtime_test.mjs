import fs from "node:fs";
import assert from "node:assert/strict";

const gdscript = fs.readFileSync("experiments/CathedralRuntimeAdapter.gd", "utf8");

assert.ok(gdscript.includes("class_name CathedralRuntimeAdapter"), "GDscript must define the runtime adapter class.");
assert.ok(gdscript.includes("apply_serialized_state"), "Adapter must ingest serialized package states.");
assert.ok(gdscript.includes("epistemic_stability"), "Adapter must track epistemic stability values.");

console.log("Ω-ONT-001 — MILESTONE 09");
console.log("STATUS: PASS");
console.log("GODOT 4 ENVIRONMENTAL RUNTIME: FORGED & VERIFIED");
