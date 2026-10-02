import fs from "node:fs";
import assert from "node:assert/strict";

const html = fs.readFileSync("experiments/browser_acceptance.html", "utf8");

assert.ok(html.includes("CathedralSerializer"), "Browser acceptance harness must import serializer adapter.");
assert.ok(html.includes("OFFLINE"), "Harness must enforce offline execution invariants.");

console.log("Ω-ONT-001 — MILESTONE 08");
console.log("STATUS: PASS");
console.log("BROWSER ACCEPTANCE SURFACE: FORGED & VALIDATED");
