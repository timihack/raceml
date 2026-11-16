# RaceML Development Roadmap

**Status:** Milestone order approved; reconciled tasks and acceptance criteria under Phase 0A review. Implementation has not begun. No release date is committed.

## Phase 0 — Specification and project setup

Phase 0 is split into specification review and project setup. Apache-2.0 licensing, canonical estimator names, training-only scope and dual-engine boundaries are established decisions, not new selection tasks.

### Phase 0A — Specification reconciliation

Audit documentation and the scaffold; reconcile scope, API proposals and sequencing; record findings, remaining technical decisions and relevant ADRs. Preserve all v0.1.0 requirements, including optional AutoML and incremental learning. Prepare a dedicated documentation branch and pull request.

**Exit:** Reconciled documents, [Phase 0 report](docs/PHASE_0_REPORT.md) and ADRs reviewed and approved. Running existing checks does not complete the remaining setup gates. Phase 0B and feature implementation must not begin before that approval.

### Phase 0B — Project setup verification

**Depends on:** Phase 0A review and approval, and a decision on the initial support/dependency policy.

Correct artifact ignore rules that hide package source, align approved dependency groups and lockfile, and verify packaging and CI. Add wheel/sdist build and isolated artifact installation checks. Verify the initial support baseline rather than inferring it from version metadata. No estimator implementation belongs in Phase 0B.

**Exit:** Lint, format, type and minimal tests pass; package builds and installs locally from artifacts; CI setup evidence and initial support limitations are documented.

## Phase 1 — Working vertical slice

**Depends on:** Phase 0B and finalized Phase 1 contracts.

Establish minimal configuration, errors, adapter protocol, registry and capabilities before the first adapter. Build `RaceMLClassifier` / `RaceMLRegressor`, prepared NumPy/pandas validation, a LightGBM adapter, basic CPU-thread mapping and wall-time/RSS reporting. Add a benchmark runner and matched direct-LightGBM comparison with predeclared workloads and quality tolerances.

**Exit:** Real fit/predict integration tests; invalid configuration, missing backend, unsupported capability and schema-mismatch tests; reproducibility and manual-mode isolation checks; initial reproducible baseline report with raw measurements and limitations. No speedup is required to report the baseline honestly.

## Phase 2 — Backend compatibility

**Depends on:** Phase 1 contracts and working baseline; input compatibility and persistence decisions before their implementations.

Add the approved scikit-learn estimators, metrics, measured Polars/Arrow conversion paths and backend-specific persistence implementation. Add XGBoost conditionally, as stated in the PRD, when its adapter contract and tests pass. Extend the existing registry and capabilities rather than creating them after the first adapter.

**Exit:** Shared backend contract tests; input conversion/schema tests; metric reference tests; save/load prediction parity and unsafe-loading failures; direct-backend comparisons where applicable. Document supported backend/input combinations. Save/load and Polars/Arrow support remain v0.1.0 requirements.

## Phase 3 — Resource efficiency

**Depends on:** Phase 2 compatibility and baseline evidence.

Expand CPU planning, thread-pool control, memory monitoring and conversion profiling. Optimize only measured bottlenecks; retain observed-budget semantics without claiming hard memory enforcement.

**Exit:** Controlled resource tests and benchmark report including regressions.

## Phase 4 — Optional AutoML

**Depends on:** Phase 3, plus approved search space, budget and cancellation semantics.

Add a separately installable search module, bounded Optuna trials, explicit user-prepared validation data and leaderboard/reporting. No internal splitting or feature preparation. Manual mode must neither import nor invoke the tuner. AutoML remains required for v0.1.0 and optional for users.

**Exit:** Manual-mode isolation, budget, cancellation and validation tests; automated search obeys declared budgets to the extent enforceable, with overrun limitations documented; separate AutoML benchmark evidence.

## Phase 5 — Incremental learning

**Depends on:** Phase 4 in the approved milestone sequence; the update contract builds on earlier backend capabilities.

Implement true online updates for at least one supported classifier and regressor, schema/class checks, held-out quality evaluation and update benchmarks. Drift evaluation hooks do not authorize automatic production retraining or a general data-preparation subsystem.

**Exit:** True online update correctness and regression tests; unsupported algorithms fail explicitly without retraining; update-versus-full-retraining timings and held-out quality are reported under equivalent conditions.

## Phase 6 — v0.1.0 readiness

**Depends on:** Phases 1–5 and all v0.1.0 acceptance evidence.

Finalize docs, tests, verified support/CI matrix, package metadata, security review, license checks, benchmark results and release notes. Resolve maintainer ownership and private vulnerability reporting before release.

**Exit:** Every v0.1.0 must-have has acceptance evidence; installation, optional groups and examples are verified; regressions and limitations are disclosed; no unsubstantiated speed claims. Any scope deferral needs separate approval, version change and rationale under the PRD. Publishing, merging and repository settings remain separately authorized actions.

## Later research

After integrated adapters and resource management are validated, open a separate native-engine research milestone: approved algorithm design and benchmark plan → correct single-threaded reference → accuracy/edge-case comparisons → profiling → measured optimization. Independently developed native RaceML algorithms must use the common estimator contracts and must not be described as wrappers. Rust requires profiling evidence and explicit approval. This research does not block the first integrated-backend release.

Other later work may include CatBoost integration, out-of-core improvements, additional domains and optional GPU execution; these are not v0.1.0 commitments.

## v0.1.0 requirement traceability

| PRD requirement | Delivery milestone | Acceptance evidence |
|---|---|---|
| Typed package, optional dependencies, supported-environment CI | 0B foundations; 1–5 feature checks; 6 final matrix | Builds, isolated installs, types, optional-group and CI results |
| FR-01 fit/predict; FR-02 explicit selection/configuration | 1 LightGBM; 2 scikit-learn and conditional XGBoost | Integration and configuration round-trip tests |
| FR-03 prepared in-memory inputs | 1 NumPy/pandas; 2 Polars/Arrow | Input compatibility, conversion and schema tests |
| FR-04 CPU threads; FR-05 timing/memory | 1 basic mapping/report; 3 resource controls | Adapter/runtime checks and documented measurements |
| FR-06 evaluation; metadata | 1 training metadata; 2 metrics | Metadata and reference metric tests |
| Benchmark harness, latency, RSS, quality, reproducibility | 1 initial harness; 2–5 extensions; 6 final reports | Matched baselines, raw measurements and disclosed limitations |
| FR-07 manual mode has no AutoML | 1 initial isolation; 4 full isolation | Tuner absent/not imported and never invoked in manual mode |
| FR-08 optional AutoML with budgets | 4 | Budget, cancellation and validation tests |
| FR-09 classifier and regressor online updates | 5 | Supported/unsupported update and quality tests |
| FR-10 model and metadata persistence | 2 | Save/load parity, schema/manifest and unsafe-load tests |

## Planning discipline

Each milestone requires an issue with scope, acceptance tests, benchmark impact and dependencies. Do not create implementation phases solely to match an arbitrary calendar.

Use a focused feature branch and pull request per related change, with exact planned files and checks announced before coding. The [decision register](docs/PHASE_0_REPORT.md#remaining-technical-decisions) identifies unresolved technical prerequisites; a roadmap task does not approve an undecided API, dependency or algorithm.
