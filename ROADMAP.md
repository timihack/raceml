# RaceML Development Roadmap

**Status:** Planned; dates are estimates, not commitments.

## Phase 0 — Specification and project setup

Approve PRD, architecture, design, benchmark protocol, license and support matrix. Create repository, packaging, CI, contribution guidelines and decision records.

**Exit:** Documents reviewed; CI executes a minimal test suite; package can be built and installed locally.

## Phase 1 — Working vertical slice

Build a simple public classifier/regressor interface, a LightGBM adapter, NumPy/pandas validation and basic wall-time/RSS reporting. Compare direct LightGBM to the wrapped workflow.

**Exit:** End-to-end fit/predict integration tests and initial reproducible baseline report.

## Phase 2 — Backend compatibility

Add scikit-learn and XGBoost adapters, registry, explicit capability reporting, metrics and persistence design.

**Exit:** Common contract tests pass for each supported backend.

## Phase 3 — Resource efficiency

Add CPU planning, thread-pool control, memory monitoring, conversion profiling and optimizations justified by measured bottlenecks.

**Exit:** Controlled resource tests and benchmark report including regressions.

## Phase 4 — Optional AutoML

Add a separately installable search module, bounded Optuna trials, validation safeguards and leaderboard/reporting.

**Exit:** Manual mode has no AutoML side effects; automated search obeys declared budgets to the extent enforceable.

## Phase 5 — Incremental learning

Implement capability-based update interfaces for compatible classifier and regressor, drift evaluation hooks and update benchmarks.

**Exit:** True online updates are tested; unsupported algorithms fail explicitly.

## Phase 6 — v0.1.0 readiness

Finalize docs, tests, CI matrix, package metadata, security review, license checks, benchmark results and release notes.

**Exit:** Installation and examples verified; no unsubstantiated speed claims.

## Later research

CatBoost integration, out-of-core improvements, native Rust kernels where proven useful, additional domains and optional GPU execution.

## Planning discipline

Each milestone requires an issue with scope, acceptance tests, benchmark impact and dependencies. Do not create implementation phases solely to match an arbitrary calendar.

## Revised sequencing

Phase 1 uses `RaceMLClassifier` and `RaceMLRegressor` with already-prepared inputs; no data-loading or cleaning module is planned. After integrated adapters and resource management are validated, open a separate native-engine research milestone covering algorithm selection, reference implementation, correctness tests, and measured optimization. Native engine development must not block the first integrated-backend release.
