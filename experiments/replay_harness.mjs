#!/usr/bin/env node

/**
 * Ω-ONT-001 — Milestone 02: Deterministic Replay Harness
 *
 * Canonical pipeline:
 *
 *   "Ω-001-32"
 *        ↓
 *      xmur3
 *        ↓
 *    Mulberry32
 *        ↓
 * deterministic experiment stream
 *
 * No network.
 * No external model.
 * No Math.random().
 * No system-time entropy.
 */

import { createHash } from "node:crypto";
import assert from "node:assert/strict";

const CANONICAL_SEED = "Ω-001-32";

function xmur3(str) {
  let h = 1779033703 ^ str.length;

  for (let i = 0; i < str.length; i++) {
    h = Math.imul(h ^ str.charCodeAt(i), 3432918353);
    h = (h << 13) | (h >>> 19);
  }

  return function seed() {
    h = Math.imul(h ^ (h >>> 16), 2246822507);
    h = Math.imul(h ^ (h >>> 13), 3266489909);
    return (h ^= h >>> 16) >>> 0;
  };
}

function mulberry32(seed) {
  let a = seed >>> 0;

  return function random() {
    a |= 0;
    a = (a + 0x6d2b79f5) | 0;

    let t = Math.imul(a ^ (a >>> 15), 1 | a);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;

    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

function createRng(seedString) {
  return mulberry32(xmur3(seedString)());
}

function clamp(value, min = 0, max = 1) {
  return Math.max(min, Math.min(max, value));
}

function runExperiment({
  seed = CANONICAL_SEED,
  interactions = [],
  particleCount = 32,
} = {}) {
  const rng = createRng(seed);

  const particles = Array.from({ length: particleCount }, (_, id) => ({
    id,
    x: rng(),
    y: rng(),
    z: rng(),
    phase: rng() * Math.PI * 2,
    truth: rng(),
    falsity: rng(),
  }));

  const state = {
    experiment: "Ω-ONT-001",
    seed,
    turn: 0,
    dimension: 12,
    mode: "FIELD",
    contradiction: 0,
    entropy: 0,
    curvature: 0,
    pressure: 0,
    evidence: 0,
    stability: 1,
    observer: 0.5,
    depth: 1,
    phase: "STABLE",
    interactionIndex: 0,
  };

  for (const interaction of interactions) {
    state.interactionIndex++;

    switch (interaction.type) {
      case "observe": {
        state.observer = clamp(interaction.value);
        break;
      }
      case "depth": {
        state.depth = clamp(interaction.value, 0.45, 1.8);
        break;
      }
      case "perturb": {
        const intensity = clamp(interaction.value);
        for (const particle of particles) {
          particle.truth = clamp(particle.truth + (rng() * 0.12 - 0.06) * intensity);
          particle.falsity = clamp(particle.falsity + (rng() * 0.12 - 0.06) * intensity);
        }
        state.pressure = clamp(state.pressure + intensity * 0.1);
        break;
      }
      default:
        throw new Error(`Unknown interaction: ${interaction.type}`);
    }
  }

  const contradiction = particles.filter((p) => p.truth > 0.5 && p.falsity > 0.5).length / particles.length;
  const meanTruth = particles.reduce((sum, p) => sum + p.truth, 0) / particles.length;
  const meanFalsity = particles.reduce((sum, p) => sum + p.falsity, 0) / particles.length;

  state.contradiction = Number(contradiction.toFixed(12));
  state.entropy = Number((-(meanTruth * Math.log2(Math.max(meanTruth, Number.EPSILON)) + (1 - meanTruth) * Math.log2(Math.max(1 - meanTruth, Number.EPSILON)))).toFixed(12));
  state.evidence = Number(clamp((meanTruth + (1 - meanFalsity)) / 2).toFixed(12));
  state.stability = Number(clamp(1 - state.pressure - state.contradiction * 0.5).toFixed(12));
  state.phase = state.contradiction > 0.25 ? "CONTRADICTION" : state.pressure > 0.25 ? "PRESSURED" : "STABLE";

  return { state, particles };
}

function digest(value) {
  return createHash("sha256").update(JSON.stringify(value)).digest("hex");
}

function assertReplay(trace) {
  const first = runExperiment(trace);
  const second = runExperiment(trace);
  const firstDigest = digest(first);
  const secondDigest = digest(second);

  assert.equal(firstDigest, secondDigest, "Replay mismatch: identical input produced different output.");
  return { digest: firstDigest, state: first.state };
}

const TRACE = {
  seed: CANONICAL_SEED,
  interactions: [
    { type: "observe", value: 0.75 },
    { type: "depth", value: 1.25 },
    { type: "perturb", value: 0.4 },
    { type: "observe", value: 0.5 },
  ],
};

const result = assertReplay(TRACE);

console.log("Ω-ONT-001 — MILESTONE 02");
console.log("STATUS: PASS");
console.log(`SEED: ${CANONICAL_SEED}`);
console.log("RNG: xmur3 → Mulberry32");
console.log(`REPLAY DIGEST: ${result.digest}`);
console.log("REPLAY: identical");
console.log("NETWORK: none");
console.log("EXTERNAL MODEL: none");
console.log("Math.random(): forbidden");
console.log(JSON.stringify(result.state, null, 2));
