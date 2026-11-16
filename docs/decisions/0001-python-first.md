# ADR 0001 — Python-first architecture with optional native optimization

**Status:** Accepted boundary; Phase 0A wording reconciliation under review

**Decision basis:** The mandatory Python-first policy in `AGENTS.md`, the existing architecture and native-engine plan, and approval of the Phase 0 correction plan. This status records that established boundary; it does not approve implementation, Rust adoption or later milestones.

## Context

RaceML integrates mature ML backends. A new Rust execution layer may introduce build complexity and data-transfer overhead without accelerating native model fit operations.

## Decision

Implement the first vertical slice in Python. Use established integrated backends for model training; RaceML input handling is limited to validation and backend-required conversion of user-prepared inputs. Wrapping a library that contains native code does not make it an independently developed native RaceML algorithm.

Independent native RaceML algorithms are a later research milestone and do not block v0.1.0. Select an algorithm only after its design and benchmark plan are approved, then implement a correct single-threaded reference before optimization. Introduce Rust/PyO3 only after profiling isolates a bottleneck, controlled benchmarks demonstrate an end-to-end benefit, and explicit approval is obtained. See [NATIVE_ENGINE.md](../../NATIVE_ENGINE.md).

## Consequences

Faster initial development and simpler packaging; some low-level optimizations remain deferred. Future native modules must preserve the public Python interface and provide tested fallbacks where appropriate.

Phase 0A adds no code, dependency or native build tooling. See [ADR 0002](0002-training-contracts.md) for the reconciled training contract proposal and remaining decisions.
