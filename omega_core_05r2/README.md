# Ω5-R2 // Multi-Ingress Reconciliation Experiment

## Purpose

Ω5-R2 tests concurrent event ingress directly into multiple replication nodes.
Unlike Ω5-R1, clients are not forced through a single fixed leader.

## Architecture

Client A → Node A
Client B → Node B
Client C → Node C

Concurrent ingress → event preservation → branch reconciliation → converged event state

## Scope

- multi-ingress event admission
- duplicate detection
- contradictory evidence preservation
- concurrent branch formation
- deterministic reconciliation
- event-ID convergence
- content-hash integrity
- replay equivalence

## Explicit non-claims

Ω5-R2 does NOT establish:

- Raft
- Paxos
- consensus
- Byzantine fault tolerance
- leader election
- multi-region durability
- production SLA
- distributed linearizability

## Core invariant

same id_e + same content_hash = same logical event

Opposing evidence remains distinct and may subsequently produce FOUR.B at the semantic layer.

## Ordering boundary

Event time tau_e is not equivalent to arrival order or commit order.

## Status

Experimental. Do not use Ω5-R2 benchmark results as evidence of consensus or production distributed-database behavior.
