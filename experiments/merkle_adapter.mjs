/**
 * Ω-ONT-001 — Milestone 06
 * Merkle Verification & Parent-Hash Chaining Adapter
 *
 * Binds every archival entry to its predecessor via cryptographic hashing,
 * forming an immutable Merkle DAG ledger.
 */

import { createHash } from "node:crypto";

export class MerkleArchiveLedger {
  constructor() {
    this.chain = [];
    this.genesisHash = "0".repeat(64);
  }

  hashBlock(blockData, parentHash) {
    return createHash("sha256")
      .update(parentHash + JSON.stringify(blockData))
      .digest("hex");
  }

  appendEntry(payload) {
    const parentHash = this.chain.length === 0 
      ? this.genesisHash 
      : this.chain[this.chain.length - 1].hash;

    const block = {
      index: this.chain.length,
      timestamp: Date.now(),
      payload,
      parentHash,
    };

    const hash = this.hashBlock(block, parentHash);
    const sealedBlock = { ...block, hash };
    this.chain.push(sealedBlock);
    return sealedBlock;
  }

  verifyIntegrity() {
    for (let i = 0; i < this.chain.length; i++) {
      const block = this.chain[i];
      const expectedParent = i === 0 ? this.genesisHash : this.chain[i - 1].hash;

      if (block.parentHash !== expectedParent) {
        return { valid: false, brokenIndex: i, reason: "Parent hash mismatch" };
      }

      const { hash, ...blockWithoutHash } = block;
      const recomputedHash = this.hashBlock(blockWithoutHash, block.parentHash);

      if (recomputedHash !== hash) {
        return { valid: false, brokenIndex: i, reason: "Payload tampering detected" };
      }
    }
    return { valid: true };
  }

  tamperPayload(index, maliciousPayload) {
    if (this.chain[index]) {
      this.chain[index].payload = maliciousPayload;
    }
  }
}
