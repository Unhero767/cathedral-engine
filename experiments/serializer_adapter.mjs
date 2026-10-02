/**
 * Ω-ONT-001 — Milestone 07
 * State Export / Import Serializer Adapter
 *
 * Packages full simulation state, Merkle chains, and interaction histories
 * into cryptographically verified, portable transport blocks.
 */

import { createHash } from "node:crypto";

export class CathedralSerializer {
  static exportPackage({ state = {}, ledger = [], trace = {} } = {}) {
    const rawPayload = {
      version: "Ω-ONT-001-M07",
      timestamp: Date.now(),
      state,
      ledger,
      trace,
    };

    const payloadString = JSON.stringify(rawPayload, null, 2);
    const checksum = createHash("sha256").update(payloadString).digest("hex");

    return JSON.stringify({
      checksum,
      payload: rawPayload,
    }, null, 2);
  }

  static importPackage(packagedJsonString) {
    let container;
    try {
      container = JSON.parse(packagedJsonString);
    } catch (e) {
      throw new Error("Invalid JSON transport package.");
    }

    const { checksum, payload } = container;
    if (!checksum || !payload) {
      throw new Error("Malformed package structure: missing checksum or payload.");
    }

    const payloadString = JSON.stringify(payload, null, 2);
    const verifiedChecksum = createHash("sha256").update(payloadString).digest("hex");

    if (verifiedChecksum !== checksum) {
      throw new Error("Checksum verification failed: package payload has been altered.");
    }

    return {
      valid: true,
      state: payload.state,
      ledger: payload.ledger,
      trace: payload.trace,
    };
  }
}
