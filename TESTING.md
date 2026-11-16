# RaceML Testing Strategy

**Status:** Reconciled verification plan for Phase 0A review. Only the scaffold import test currently exists.

## Test levels

1. Unit tests: configuration, validation, registry, capability checks and report formatting.
2. Contract tests: every backend must satisfy the same supported estimator behaviors.
3. Integration tests: real fit/predict, save/load, data conversion and resource reporting.
4. Negative tests: missing optional dependencies, unsupported online update, invalid inputs, schema drift, invalid parameters and unsafe loading.
5. Reproducibility tests: fixed seeds and consistent outputs within declared tolerances.
6. Performance tests: benchmark scripts run separately from ordinary CI; alert on regressions but account for machine variability.

## CI proposal

Run formatting/linting, type checks, package build and tests on a verified Python/OS matrix. Keep expensive model benchmarks in scheduled or manually triggered jobs.

Current CI configures Ubuntu/Python 3.12, default development dependencies, lint, format, mypy and pytest. It does not build wheel/sdist artifacts, test clean artifact installation or run backend integrations. Package metadata declares Python >=3.12; the verified support matrix remains a decision. Phase 0A records these gaps without changing CI or packaging.

Phase 0B, after approval, verifies builds and isolated wheel/sdist installation and aligns the initial support/dependency policy. Feature milestones add backend/input and optional-dependency jobs as their code arrives. Manual-mode checks must run where the tuner is absent and verify it is neither imported nor invoked. A successful check on empty modules is not evidence that planned estimators work.

## Documentation and Phase 0A checks

For specification-only changes, check local Markdown links and anchors, balanced fenced examples, cross-document scope/naming/milestone consistency, and `git diff --check`. Parse illustrative Python snippets for syntax without treating them as executable examples. Run existing lint, format, type and scaffold tests where the environment permits, recording exact commands and outcomes. Do not add implementation tests, dependencies or setup changes in Phase 0A. Build/install, backend integration and benchmark evidence remain later gates.

## Milestone verification

| Milestone | Focused evidence |
|---|---|
| 0A | Documentation checks and existing scaffold checks; review approval |
| 0B | Build, isolated artifact installation, dependency/support and CI setup checks |
| 1 | Configuration/registry/input unit tests; real LightGBM fit/predict; negative configuration, missing backend, unsupported capability and schema tests; report/reproducibility/manual-mode checks; matched baseline |
| 2 | Shared backend contracts; Polars/Arrow conversions; reference metrics; save/load parity; invalid manifest/schema and unsafe-loading failures |
| 3 | Controlled resource observations, thread behavior and equivalent before/after performance measurements |
| 4 | Optional AutoML imports, user-prepared validation, budgets, cancellation and manual-mode isolation |
| 5 | Classifier/regressor online updates, class/schema checks, unsupported updates without retraining and held-out quality |
| 6 | Complete v0.1.0 requirement evidence, verified support matrix, optional installs and executable examples |

## Release gate

No failing required tests; examples executable; dependency groups installable; backend support matrix documented; known benchmark regressions disclosed.

## Suggested tools

The scaffold already configures pytest, Ruff, mypy and pytest-cov; coverage is diagnostic. Isolated benchmark runners remain to be implemented. Pin test datasets and versions.

## Revised acceptance checks

Test canonical imports `RaceMLClassifier` and `RaceMLRegressor`, prepared-input handling, and backend conversion without silent cleaning. Do not create tests for user-facing file loaders or imputation pipelines. Integrated and native backends must pass the same estimator contract tests when native algorithms are introduced.
