/**
 * Ω-ONT-001 — Milestone 05
 * Ash Archive Provenance & Ledger Adjacency Adapter
 *
 * Enforces the structural invariant:
 * STORY(t) → BP(t + 1)
 */

export class AshArchiveLedger {
  constructor() {
    this.entries = [];
  }

  recordCycle({ turn = 0, storyData = {}, bpState = {} } = {}) {
    const storyEntry = {
      sequence: this.entries.length,
      tier: "STORY",
      timestamp: turn,
      payload: storyData,
    };

    const bpEntry = {
      sequence: this.entries.length + 1,
      tier: "BP",
      timestamp: turn + 1,
      payload: bpState,
    };

    this.entries.push(storyEntry, bpEntry);
  }

  verifyAdjacency() {
    for (let i = 0; i < this.entries.length; i += 2) {
      const story = this.entries[i];
      const bp = this.entries[i + 1];

      if (!story || !bp) return false;
      if (story.tier !== "STORY" || bp.tier !== "BP") return false;
      if (bp.timestamp !== story.timestamp + 1) return false;
    }
    return true;
  }

  exportSerialized() {
    return JSON.stringify(this.entries);
  }

  importSerialized(jsonString) {
    const raw = JSON.parse(jsonString);
    this.entries = raw.sort((a, b) => a.sequence - b.sequence);
  }
}
