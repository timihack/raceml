# RaceML Product Requirements Document

**Status:** Draft for approval  
**Target release:** v0.1.0  
**Project:** Resource-Aware Compute Engine for Machine Learning

## 1. Product statement

RaceML is a general-purpose, open-source Python ML library, initially focused on tabular classification and regression. It aims to improve end-to-end model development on CPU-constrained machines by managing training execution, CPU and memory resources, and optional automated search across integrated and native model engines.

## 2. Problems

1. Duplicate data conversions and temporary arrays can increase peak memory.
2. Nested parallelism and uncontrolled model trials can waste CPU resources.
3. ML engines expose inconsistent configuration, prediction and evaluation interfaces.
4. Manual experimentation takes time; optional automation must not be imposed on users.
5. Incremental updates differ across algorithms and must be represented accurately.

These are hypotheses about particular workflows, not claims that every existing library exhibits these problems.

## 3. Intended users

Data scientists, ML engineers, researchers, students, independent developers, and competition participants. Competition use requires users to check the specific event's rules; RaceML does not guarantee compliance.

## 4. Five product areas

### P1 — Faster end-to-end training

Reduce training input conversion, redundant backend allocations and orchestration overhead. Control nested thread pools and cache reusable artifacts when safe. Do not claim to accelerate native training algorithms without evidence.

### P2 — Memory efficiency

Support compact input representations, avoid unnecessary copies, monitor whole-process peak resident memory and use chunked workflows when supported by the backend. Hard memory caps are out of scope for the initial in-process runner.

### P3 — CPU-first optimization

Allow explicit thread limits, avoid oversubscription, measure CPU utilization and document backend-specific limitations.

### P4 — Optional AutoML

Offer opt-in model selection and hyperparameter tuning through an optional dependency group. Manual mode must not trigger any automated search. Time and trial budgets must be explicit.

### P5 — Incremental learning

Expose update operations only for compatible estimators. Distinguish true online updates from warm starts and full retraining. Track update quality on held-out data.

## 5. v0.1.0 scope

### Must have

- Python package with typed public APIs and optional backend dependencies.
- Classification and regression through LightGBM and scikit-learn; XGBoost integration in the same release if adapter contract and tests pass.
- NumPy and pandas inputs; Polars and Arrow inputs via measured conversion paths.
- Explicit algorithm selection and backend parameters; manual mode is default.
- CPU thread configuration with documented limits.
- Training and prediction, validation metrics, model metadata and save/load with safe-loading guidance.
- Benchmark harness measuring end-to-end wall time, prediction latency, peak RSS, predictive quality and reproducibility metadata.
- Incremental updates for at least one supported classifier and regressor.
- Optional AutoML module with bounded search and no import requirement for manual users.
- CI tests on supported environments.

### Deferred

- Custom boosting algorithm, universal GPU engine, distributed training, full streaming support for every estimator, guaranteed hard memory caps, automatic drift-triggered production retraining, full support for images/text/audio.

## 6. Functional requirements

| ID | Requirement | Acceptance evidence |
|---|---|---|
| FR-01 | Fit and predict with supported classifiers/regressors | Integration tests per backend |
| FR-02 | Explicitly select algorithm and parameters | Configuration round-trip tests |
| FR-03 | Accept supported in-memory inputs | Input matrix tests |
| FR-04 | Configure CPU threads | Adapter tests and runtime report |
| FR-05 | Record memory and timing | Reproducible report schema |
| FR-06 | Evaluate predictions | Metric tests against reference results |
| FR-07 | Disable all AutoML in manual mode | Tests that no tuner is imported or invoked |
| FR-08 | Opt-in AutoML with budgets | Budget and cancellation tests |
| FR-09 | Incrementally update compatible models | Capability and regression tests |
| FR-10 | Persist model and metadata | Save/load prediction parity tests |

## 7. Non-functional requirements

- Reproducible experiments with seeds, data fingerprints, package versions and hardware metadata.
- Clear exceptions for unsupported operations; no silent fallback to retraining.
- Optional dependencies loaded only when needed.
- No untrusted pickle/joblib deserialization by default.
- No network access or telemetry by default.
- Document supported OS/Python/backend combinations after CI verification.
- Code coverage is a diagnostic, not a substitute for meaningful tests.

## 8. Performance hypotheses

- **H1:** At least 20% lower end-to-end wall time on a defined subset of workflows compared with equivalent standalone baselines.
- **H2:** At least 30% lower peak process-tree RSS on a defined subset of workflows.
- **H3:** No material deterioration in held-out predictive quality within predeclared tolerance.

Do not treat these as universal release guarantees. Pre-register workloads, baselines and tolerances in BENCHMARKS.md.

## 9. Release acceptance

All must-have requirements either pass tests or are explicitly deferred with version change and rationale. Benchmarks must publish both wins and losses. No invented measurements. API and install examples must be tested before public documentation describes them as functional.

## 10. Open decisions

Exact Python version support, license, backend version matrix, persistence format, API naming, benchmark datasets, resource-budget enforcement strategy and release date require approval or testing.

## Scope revision — training only and dual engines

Users prepare their own features and targets; RaceML does not load files, clean data, impute, engineer features, or split datasets. The initial API is `RaceMLClassifier` / `RaceMLRegressor`. The long-term product includes integrated model backends **and** independently developed native RaceML algorithms. Native algorithms are research work and are not required for v0.1.0. See [SCOPE.md](SCOPE.md) and [NATIVE_ENGINE.md](NATIVE_ENGINE.md). Any earlier mention of user-facing data preparation is superseded by this section.
