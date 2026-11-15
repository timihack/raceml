# RaceML Testing Strategy

**Status:** Planned.

## Test levels

1. Unit tests: configuration, validation, registry, capability checks and report formatting.
2. Contract tests: every backend must satisfy the same supported estimator behaviors.
3. Integration tests: real fit/predict, save/load, data conversion and resource reporting.
4. Negative tests: missing optional dependencies, unsupported online update, invalid inputs, schema drift, invalid parameters and unsafe loading.
5. Reproducibility tests: fixed seeds and consistent outputs within declared tolerances.
6. Performance tests: benchmark scripts run separately from ordinary CI; alert on regressions but account for machine variability.

## CI proposal

Run formatting/linting, type checks, package build and tests on a verified Python/OS matrix. Keep expensive model benchmarks in scheduled or manually triggered jobs.

## Release gate

No failing required tests; examples executable; dependency groups installable; backend support matrix documented; known benchmark regressions disclosed.

## Suggested tools

pytest, Ruff, a Python type checker selected during setup, coverage reporting, and isolated benchmark runners. Pin test datasets and versions.

## Revised acceptance checks

Test canonical imports `RaceMLClassifier` and `RaceMLRegressor`, prepared-input handling, and backend conversion without silent cleaning. Do not create tests for user-facing file loaders or imputation pipelines. Integrated and native backends must pass the same estimator contract tests when native algorithms are introduced.
