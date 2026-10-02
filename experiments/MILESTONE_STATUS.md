# Ω-ONT-001 — Milestone Register

| Milestone | Component | Status |
|---|---|---|
| 01 | Deterministic Seed Lock | LOCKED |
| 02 | Replay Harness | IMPLEMENTED |
| 03 | BP T/F/B/N Adapter | IMPLEMENTED |
| 04 | Evidence / Pressure Adapter | VERIFIED |
| 05 | Ash Archive Provenance | VERIFIED |
| 06 | Merkle Verification | VERIFIED |
| 07 | State Export / Import | VERIFIED |
| 08 | Browser Acceptance | VERIFIED |
| 09 | Godot 4 Environmental Runtime | VERIFIED |
| 10 | Canonical Archive Commit | PENDING |

## Milestone 05 Provenance Invariant

```text
STORY(timestamp = t)
       ↓ immediately followed by
BP(timestamp = t + 1)
```

Adjacency is structurally locked and survives sorting, serialization, and deserialization.
