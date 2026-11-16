# RaceML Testing Strategy

**Status:** Phase 0A reconciled and merged; Phase 0B setup checks prepared for review. No estimators are implemented.

## Test levels

1. Unit tests: configuration, validation, registry, capability checks and report formatting.
2. Contract tests: every backend must satisfy the same supported estimator behaviors.
3. Integration tests: real fit/predict, save/load, data conversion and resource reporting.
4. Negative tests: missing optional dependencies, unsupported online update, invalid inputs, schema drift, invalid parameters and unsafe loading.
5. Reproducibility tests: fixed seeds and consistent outputs within declared tolerances.
6. Performance tests: benchmark scripts run separately from ordinary CI; alert on regressions but account for machine variability.

## CI proposal

Run formatting/linting, type checks, package build and tests on a verified Python/OS matrix. Keep expensive model benchmarks in scheduled or manually triggered jobs.

The Phase 0A baseline CI configured Ubuntu/Python 3.12, default development dependencies, lint, format, mypy and pytest, without artifact builds or isolated installs. Phase 0B retains that platform baseline and adds locked synchronization, wheel/sdist builds and artifact installation checks. Hosted results must be verified on the pull request; adding a job is not evidence it passed.

[ADR 0003](docs/decisions/0003-package-and-support-policy.md) records the approved policy: NumPy-only core, optional backend/table packages, Ubuntu/Python 3.12 for initial setup verification, and no verified claim for other Python/OS combinations. Package metadata still declares Python >=3.12; lower dependency bounds are not a tested minimum-version matrix. Feature milestones add backend/input and optional-dependency jobs as their code arrives. Manual-mode checks must run where the tuner is absent and verify it is neither imported nor invoked. A successful check on empty modules is not evidence that planned estimators work.

## Packaging checks

`tests/integration/test_packaging.py` checks root artifact ignore boundaries during normal tests. Its four artifact checks skip unless `RACEML_DIST_DIR` identifies a directory containing exactly one wheel and one source archive:

```bash
uv build --no-sources
RACEML_DIST_DIR=dist uv run --locked pytest tests/integration/test_packaging.py
```

Each artifact's metadata must match the declared version, Python requirement, NumPy-only core and optional groups, with both `LICENSE` and `NOTICE` preserved. Each is then installed with its base dependencies into a fresh environment; a separate `python -I` process verifies the import comes from that installation and optional libraries/tuners are absent and not imported. No `--no-deps` installation shortcut is used. Missing/ambiguous artifact sets fail when checks are enabled. These tests perform development/CI package-index access; ordinary imports and normal tests do not initiate downloads.

Use a fresh output directory to avoid stale archives. Record environment, commands, results, resolved versions and unrun combinations in the [Phase 0B report](docs/PHASE_0B_REPORT.md). No backend fit/predict, input conversion, full extras compatibility or performance support is established by these setup checks.

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
