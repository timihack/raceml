# RaceML Native Engine Plan

**Status:** Research and design only. No native algorithms have been implemented.

## Purpose

RaceML will support two training paths under the same public estimator contracts: (1) integrated established backends and (2) independently developed RaceML algorithms. Native models must not be thin wrappers marketed as original algorithms.

## Design principles

- Start with working integrated adapters and reproducible baselines.
- Select a first native algorithm only after a written design and benchmark plan are approved.
- Implement a correct single-threaded reference version before SIMD, multicore scheduling, or Rust optimization.
- Preserve numerical correctness, deterministic tests where feasible, and explicit algorithm capabilities.
- Keep native dependencies optional; the Python API must not require a Rust toolchain for standard binary-wheel installation.
- Distinguish native algorithm training speed from orchestration improvements.

## Candidate research directions (not commitments)

Histogram-based decision trees, online linear models, and CPU-oriented numerical kernels. Evaluate each candidate for originality, implementation complexity, performance opportunity, and maintainability before selection.

## Native backend contract

Each implementation declares task type, supported input types, missing-value behavior, predict/probability support, incremental-update support, threading semantics, serialization format, and reproducibility limitations. Unsupported operations raise explicit errors.

## Verification gates

1. Mathematical specification and reference tests.
2. Accuracy and edge-case parity against trusted implementations.
3. Profiling, memory measurement and independent baseline comparisons.
4. CPU optimization with regression tests.
5. Release only after API, platform and serialization compatibility reviews.

Rust/PyO3 may be adopted for measured bottlenecks after explicit approval; Python-first remains the default.
