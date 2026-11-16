# RaceML Phase 0B — Project Setup Verification

**Status:** Local setup checks passed; prepared for user commit, push and PR review. Hosted CI remains unverified. No estimator implementation.

**Date:** 2026-11-16

## Scope and authorization

Phase 0A was merged in PR #2 at `66e57c0`. The user authorized the next milestone and approved dependency/support decision D01 in [ADR 0003](decisions/0003-package-and-support-policy.md). Work is on `chore/phase-0b-project-setup`. Changes remain uncommitted and unpushed for the user to review and publish.

This phase fixes root artifact ignore rules, declares optional dependencies, updates the lockfile, includes licensing in distributions, and adds build/install checks. It does not add estimators, backend adapters, data preparation, resource control, AutoML, incremental updates or native algorithms. All original v0.1.0 requirements remain intact. The [Phase 0A report](PHASE_0_REPORT.md) remains the historical audit snapshot; its open D01 policy is resolved by ADR 0003, while later technical gates remain.

## Files changed

- `.gitignore`: anchor root data/dataset/artifact/model/benchmark output directories so source is visible.
- `pyproject.toml`: NumPy-only core, `sklearn`/`pandas`/`polars`/`arrow` extras, expanded `all`, explicit `LICENSE`/`NOTICE`, and Hatchling >=1.27 for metadata 2.4 behavior.
- `uv.lock`: resolve the approved dependency groups without intentionally upgrading unrelated packages.
- `.github/workflows/ci.yml`: validate the lock during synchronization and runs; build sdist/wheel; run artifact and isolated-install tests.
- `tests/integration/test_packaging.py`: ignore-boundary regression tests, metadata/notices checks and clean artifact installation/import checks.
- `CONTRIBUTING.md`, `TESTING.md`: setup policy, commands, opt-in packaging checks and evidence limits.
- `docs/decisions/0003-package-and-support-policy.md` and this report: authorization, policy and verification record.

The ignore fix also makes two pre-existing empty local files under `src/raceml/models/` visible as untracked. They were not authored or modified in Phase 0B and are excluded from the suggested commit paths. Review them separately; do not delete or add them automatically. The local wheel includes ten source modules, while a clean snapshot of the intended commit includes only the eight tracked package modules. Both built successfully; the full isolated-install run used the clean snapshot's artifacts, so these placeholders cannot mask a missing tracked package file.

## Support and dependency evidence

The approved initial setup target is Ubuntu/Python 3.12. `requires-python = ">=3.12"` remains an installation constraint, not a claim that all newer versions/platforms were tested. Hosted CI results remain pending the user's push and pull request. Runtime extras declare dependencies, not functioning backends or input conversions.

NumPy remains core. scikit-learn moves to `sklearn`; pandas, Polars and PyArrow are explicit extras. Existing LightGBM, XGBoost, CatBoost and Optuna extras remain, with no advancement of deferred CatBoost scope. License review for the new optional declarations and packaging sources is recorded in ADR 0003. A full release dependency/binary review is still required.

## Verification results

Local checks used Ubuntu 26.04.1 LTS on x86_64, Python 3.12.3 and uv 0.7.9. Builds used Hatchling 1.33.0. Network-restricted dependency resolution initially failed with a DNS error; it succeeded after sandbox escalation. The task cache was `/tmp/raceml-phase0b-uv-cache`. Existing lockfile package versions were preserved; only Polars 2.1.0, polars-runtime-32 2.1.0 and PyArrow 26.0.1 were added. The locked development environment retained NumPy 2.5.4; both fresh artifact installs independently resolved NumPy 2.5.5 from the index under the declared `>=1.26` constraint. These were installability checks, not matched performance experiments.

| Check and command | Result |
|---|---|
| `uv lock --cache-dir /tmp/raceml-phase0b-uv-cache --python /usr/bin/python3.12` | Passed after network approval: 53 packages resolved; no existing version changes. |
| `uv sync --locked --cache-dir /tmp/raceml-phase0b-uv-cache --python /usr/bin/python3.12` | Passed: base development environment installed; optional scikit-learn and its unused dependencies removed from the project environment. |
| `uv lock --check --offline --cache-dir /tmp/raceml-phase0b-uv-cache` | Passed. |
| `pytest tests/integration/test_packaging.py -k artifact_ignore_boundaries` | Passed: seven ignore-boundary checks. |
| `uv build --offline --no-sources --cache-dir /tmp/raceml-phase0b-uv-cache --out-dir /tmp/raceml-phase0b-local-dist` | Passed: source archive and wheel built from the local checkout. |
| `RACEML_DIST_DIR=/tmp/raceml-phase0b-local-dist pytest tests/integration/test_packaging.py -k distribution_metadata` | Passed: both artifacts preserve metadata, extras, LICENSE and NOTICE. |
| `uv build /tmp/raceml-phase0b-source-2mnitqop --offline --no-sources --cache-dir /tmp/raceml-phase0b-uv-cache --out-dir /tmp/raceml-phase0b-clean-dist` | Passed from a clean source snapshot excluding the pre-existing untracked placeholders. |
| `RACEML_DIST_DIR=/tmp/raceml-phase0b-clean-dist UV_CACHE_DIR=/tmp/raceml-phase0b-uv-cache pytest tests/integration/test_packaging.py` | Passed: 11 tests, including both metadata checks and both clean installs with base dependencies; optional packages/tuners absent and unimported. |
| `.venv/bin/ruff check --no-cache .` | Passed. |
| `.venv/bin/ruff format --check --no-cache src/ tests/` | Passed: 12 local Python files, including the two preserved placeholders. |
| `python -B -m mypy --no-incremental --cache-dir=/dev/null src/raceml` | Passed: ten local source files, including the two preserved placeholders. |
| `python -B -m pytest -p no:cacheprovider` | Passed: eight tests; four artifact checks skipped as intended without `RACEML_DIST_DIR`. |
| `python -B /tmp/raceml_phase0b_docs_check.py` | Passed: 20 Markdown files, 55 local links/anchors, five Python snippets and balanced fences. Ad hoc standard-library audit, not repository tooling. |
| `git diff --check` | Passed. |

The pytest and mypy commands above used `.venv/bin/python -B` with `PYTHONDONTWRITEBYTECODE=1`; pytest disabled its cache with `-p no:cacheprovider`. The clean snapshot copied current tracked file contents plus the three intended new files (this report, ADR 0003 and the packaging test) into a fresh temporary directory. It contained eight package modules and no Git metadata or virtual environment. Documentation-only final report edits do not change the built package or test code.

No hosted job result, full extras installation, backend/input compatibility, minimum-version matrix or performance result is inferred from these passes. External links and rendered Mermaid diagrams were not validated.

## Remaining work and limitations

Local setup evidence is complete; commit, push, hosted CI and review remain with the user. Additional Python/OS matrices, backend/input compatibility, minimum dependency-version tests, full extras installation, estimator fit-option forwarding, persistence, budgets and benchmarks remain later gates. No performance benchmark is appropriate to this setup-only change, and no improvement is claimed. The next suggested task after review is Phase 1 contract finalization, including backend-specific constructor-versus-fit options, before the first estimator implementation.
