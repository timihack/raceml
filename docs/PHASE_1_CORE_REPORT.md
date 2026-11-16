# Phase 1 — Initial Core Implementation

**Status:** Initial core implementation and local checks complete; ready for user commit, push and PR review. Public estimators and real backend adapters remain unimplemented.

**Date:** 2026-11-16

## Authorization and scope

The [Phase 1 contracts](PHASE_1_CONTRACTS.md) were accepted by merged [PR #4](https://github.com/timihack/raceml/pull/4), merge commit `c838f28`. The user confirmed completion, and the next dependency-ordered task implements internal configuration, typed errors, the base adapter protocol and a minimal registry. Work is on `feat/phase-1-core-contracts`; the user retains commits, pushes and PR merging.

This is the first bounded implementation task, not completion of the Phase 1 vertical slice. The package root still exports no public estimators. There are no production registry entries, no LightGBM adapter, no input conversion/validation, no fit-option catalog/routing engine, no resource monitor, no AutoML, no online updates and no persistence or native algorithms. Tests use fake adapters only; installing a backend does not advertise a working integration.

## Files and behavior

- `src/raceml/core/config.py`: frozen internal requested configuration, basic task/identifier/core/seed validation, exact decimal/binary byte-budget parsing and fresh flat requested-parameter mappings. The budget is an observation setting, not an allocation or enforcement mechanism.
- `src/raceml/core/errors.py`: the accepted built-in-based Phase 1 exception types. No enforceable-budget or persistence error mechanism is invented.
- `src/raceml/core/protocols.py`: the minimal typed adapter interface and its five boolean capability fields; optional probability/update methods are not required on the base protocol.
- `src/raceml/core/registry.py`: immutable internal descriptor lookup by algorithm/task and lazy adapter factories. It rejects duplicate entries, unknown algorithms and task mismatches. Only a missing declared dependency is wrapped with installation guidance; unrelated/internal import failures and unsupported-version errors retain their original identity. No fallback, automatic fit, production registrations, public registration API or plugin loading.
- `tests/unit/test_config.py`, `tests/unit/test_registry.py`: configuration/budget boundaries, snapshot/round-trip behavior, safe representations, task/algorithm resolution, lazy factories and failure behavior.
- `tests/integration/test_core_contracts.py`: typed fake-adapter composition and a fresh-process import guard blocking optional backends, input packages and AutoML. The fake only records calls; it does not train or predict a model.
- `tests/integration/test_packaging.py`: extend the installed-artifact probe to verify the new core modules are packaged and usable without optional dependencies.
- `.github/workflows/ci.yml`, `CONTRIBUTING.md`: include the typed fake-adapter test in the existing mypy check and document the same command, so protocol conformance is verified in CI.
- `DESIGN.md`, `ARCHITECTURE.md`, `ROADMAP.md`, `TESTING.md`, the contract specification and ADR 0004: update implementation/acceptance status and link the evidence boundary. This report records the current task separately from the historical contract-proposal checks.

No dependency, lockfile, build configuration, mandatory scope/native plan or PRD requirement changes. CI adds only the typed contract test to its existing type-check command; no publishing or deployment is introduced. The two pre-existing empty local files under `src/raceml/models/` remain untouched and untracked and are excluded from the proposed commit paths.

## Design boundaries

`EstimatorConfig` validates its own settings; algorithm availability is a separate registry lookup. Backend parameter mappings are shallow structural snapshots: later mutations of the caller's outer dictionary do not change the requested configuration, while nested user objects keep identity as the accepted contract requires. Backend objects are excluded from automatic configuration representations. Backend names/ranges, thread/main-seed aliases, constructor-versus-fit validation and version compatibility are deferred to their real adapter paths, not guessed in generic configuration code.

The internal registry accepts source-defined descriptor sequences for wiring/tests, copies them into an immutable lookup and offers no register/unregister or dynamic import API. Its default is empty until a real adapter passes its implementation gate. Descriptor metadata currently covers identity/task/category, factory and optional dependency guidance. Input/version/parameter catalogs remain the next adapter work, and the boolean protocol is not evidence that any real backend capability is implemented.

Missing backend guidance is intentionally narrow: the factory must report `ModuleNotFoundError.name` matching the declared dependency module. A transitive dependency or missing internal module is not falsely labeled as the selected backend being absent. Future concrete adapters must declare and handle their actual dependency/version requirements explicitly.

## Verification

Checks used the existing Python 3.12.3 environment. Python commands below used `PYTHONDONTWRITEBYTECODE=1`; pytest disabled its cache, Ruff disabled caches, and mypy used no incremental cache. No dependencies were synchronized or added for this task.

| Command or check | Result |
|---|---|
| `.venv/bin/python -B -m pytest -p no:cacheprovider tests/unit/test_config.py tests/unit/test_registry.py tests/integration/test_core_contracts.py` | Passed: 73 focused tests, including invalid configuration/budgets, lazy lookup, unavailable backend guidance and fresh-process import isolation. |
| `.venv/bin/python -B -m pytest -p no:cacheprovider` | Passed: 81 tests; four opt-in artifact checks skipped without `RACEML_DIST_DIR`. The focused tests were included after lint/type fixes. |
| `.venv/bin/ruff check --no-cache .` and `.venv/bin/ruff format --check --no-cache src/ tests/` | Passed: 19 local Python files formatted, including two preserved empty model placeholders. |
| `.venv/bin/python -B -m mypy --no-incremental --cache-dir=/dev/null src/raceml tests/integration/test_core_contracts.py` | Passed: 15 local source/test files, including the two placeholders and typed fake adapter. |
| `uv lock --check --offline --cache-dir /tmp/raceml-phase0b-uv-cache` | Passed; lockfile unchanged. |
| `uv build /tmp/raceml-phase1-core-source-n29bc9af --offline --no-sources --cache-dir /tmp/raceml-phase0b-uv-cache --out-dir /tmp/raceml-phase1-core-dist` | Passed: clean-snapshot sdist and wheel built offline. |
| `RACEML_DIST_DIR=/tmp/raceml-phase1-core-dist UV_CACHE_DIR=/tmp/raceml-phase0b-uv-cache UV_OFFLINE=1 .venv/bin/python -B -m pytest -p no:cacheprovider tests/integration/test_packaging.py` | Passed: all 11 checks, including both metadata/notices tests and separate wheel/sdist installs. The installed core modules work without optional libraries/tuners. |
| Clean wheel contents | Passed: all 12 intended package modules present; the two pre-existing untracked model placeholders absent. |
| `.venv/bin/python -B /tmp/raceml_phase1_docs_check.py` | Passed: 23 Markdown files, 76 local links/anchors, seven Python snippets and balanced fences. Ad hoc standard-library audit, not new repository tooling. |
| `git diff --check` and change-scope review | Passed; no staged changes, commits or pushes performed by the agent. |

The clean snapshot copied current tracked-file contents plus the four new core modules, three new test files and this report, without Git metadata, a virtual environment or untracked model placeholders. Final documentation/CI recipe edits do not change built runtime code. The fresh-install checks use cached packages offline; no backend is downloaded or trained. Fake-adapter tests verify composition and isolation, not real model quality, fit-option validation or prediction behavior.

No hosted CI result, additional Python/OS matrix, data-schema implementation, real backend/version compatibility or performance result is inferred. Input-schema negative tests belong to the next validation task, not the fake adapter. The proposed registry is only the initial lookup/factory foundation; its real catalog remains unimplemented.

## Remaining work

After this task's review, implement numeric NumPy/pandas schema validation and the real LightGBM adapter path with its verified version/dependency/constructor/fit catalogs, followed by public estimators, resource reporting and the matched baseline in dependency order. D05 RSS methodology, D07 fingerprint/report details and D06 benchmark configurations remain gates before their dependent tasks. Full AutoML, incremental support and independent native research keep their approved milestones.

No performance improvement is claimed, and no model training benchmark is appropriate to this core-only task. Hosted CI and additional environment support require separate evidence after the user's push.
