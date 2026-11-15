# ADR 0001 — Python-first architecture with optional native optimization

**Status:** Proposed

## Context

RaceML integrates mature ML backends. A new Rust execution layer may introduce build complexity and data-transfer overhead without accelerating native model fit operations.

## Decision

Implement the first vertical slice in Python. Use existing native-backed libraries for model training and data processing. Introduce Rust/PyO3 only after profiling isolates a bottleneck and controlled benchmarks demonstrate an end-to-end benefit.

## Consequences

Faster initial development and simpler packaging; some low-level optimizations remain deferred. Future native modules must preserve the public Python interface and provide tested fallbacks where appropriate.
