# RaceML Phase 0 Report

**Status:** Phase 0A specification reconciliation prepared for review. Phase 0A approval, Phase 0B setup and implementation remain pending.

**Date:** 2026-11-16

## Authorization and scope

The initial audit was read-only. The user subsequently approved the correction plan and milestone order and authorized Phase 0A documentation reconciliation on a dedicated feature branch with a pull request. That approval does not authorize Phase 0B, feature implementation, release publication, merging or repository settings changes. Phase 0A must be reviewed and approved before later work starts.

All original v0.1.0 requirements remain in the [PRD](../PRD.md), including AutoML and online updates for at least one classifier and regressor. AutoML is optional for users, not omitted from the release. XGBoost retains its conditional inclusion; independent native algorithms remain later research. No new dependency, runtime API, native component or architecture layer is implemented by this change.

## Repository baseline

- Repository: `timihack/raceml`; license: Apache-2.0 with `LICENSE` and `NOTICE` present.
- Initial audit checkout: `docs/fork-contribution-workflow` at `4d3608c`, with a clean working tree and only `origin` configured.
- Phase 0A base: fetched `origin/main` at `ecf713d`, which already includes contribution-workflow PR #1. Dedicated branch: `docs/phase-0a-specification-reconciliation`. No unrelated branch changes are included.
- The scaffold contains eight tracked, empty Python package modules and one import test. Two additional empty local placeholders under `src/raceml/models/` are ignored by the artifact rules and are not tracked. No estimator, backend adapter, resource monitor, tuner, persistence system or independent native algorithm is implemented.
- `pyproject.toml` declares Python >=3.12, core NumPy/scikit-learn dependencies and optional LightGBM, XGBoost, CatBoost and Optuna groups. Installed packages and lockfile entries do not demonstrate backend implementation or compatibility.
- CI configures Ubuntu/Python 3.12 and default development dependencies. It runs lint, format, mypy and pytest, without artifact builds, clean installation or backend integration jobs. Hosted CI results have not been established by the local audit.

## Established decisions

1. Apache-2.0 licensing and import namespace `raceml`.
2. Canonical `RaceMLClassifier` / `RaceMLRegressor`; optional `RaceMLAutoClassifier` / `RaceMLAutoRegressor`.
3. Training-only prepared inputs. No loading, cleaning, imputation, feature engineering or splitting APIs; no silent feature dropping/reordering. Backend-native handling is allowed only when explicitly supported and documented.
4. Python-first, integrated adapters initially, independent native algorithms later. Native algorithm selection and Rust adoption need their own approved evidence and design gates.
5. Manual training by default; no tuner import or search in manual mode. Optional AutoML remains a v0.1.0 deliverable.
6. True online updates only when declared; no silent substitution or retraining. Classifier and regressor online support remain v0.1.0 deliverables.
7. Initial memory limits are observed budgets. The 20% time and 30% peak-memory reductions are research hypotheses, not release guarantees or measured achievements.

The source hierarchy now states that [SCOPE.md](../SCOPE.md) and [NATIVE_ENGINE.md](../NATIVE_ENGINE.md), together with mandatory agent decisions, constrain the detailed specifications. Reconciliation does not alter those boundaries.

## Findings and disposition

| ID | Finding | Phase 0A correction or remaining action |
|---|---|---|
| F01 | DESIGN permitted a validation strategy that could imply internal splitting. | Restrict validation and AutoML to explicit user-prepared splits; record user-supplied split metadata only. |
| F02 | Registry and capabilities followed the first adapter in the roadmap. | Move minimal contracts, errors, capabilities and registry before the first Phase 1 adapter. |
| F03 | Polars/Arrow and actual save/load implementation had no explicit delivery task. | Assign both to Phase 2, preserving v0.1.0 requirements and integration evidence. |
| F04 | Fit return behavior, adapter metadata and update errors were incomplete. | Add a review proposal for public `fit -> self`, separate reports, adapter metadata and update-error specialization in DESIGN and ADR 0002. Detailed signatures/types remain open. |
| F05 | Module paths disagreed across DESIGN and the scaffold. | Propose `input/`, existing training `engine/` responsibility, and integrated adapters under `models/backends/`. No source files are added or moved. |
| F06 | Unanchored `data/` and `models/` artifact rules hide matching package source. | Record the observed ignored placeholders. Rule corrections are Phase 0B work; `.gitignore` is unchanged here. |
| F07 | Dependency declarations do not resolve optional-backend policy or table-input installation. | Record core-versus-optional scikit-learn and explicit pandas/Polars/Arrow dependency decisions before Phase 0B. No dependency or lockfile changes. |
| F08 | CI lacks artifact build/install and backend/input coverage; broad Python metadata is not a verified matrix. | Document current evidence and Phase 0B setup checks; add feature jobs in their milestones. CI is unchanged here. |
| F09 | License/naming remained listed as open; ADR 0001 still marked the established Python-first boundary proposed. | Record settled license/names and the accepted Python-first boundary; distinguish wording and contract proposals still under review. |
| F10 | README headline suggested established performance and placed incremental estimators under later work. | Describe speed/memory as aims and retain AutoML/online updates in planned v0.1.0 delivery. |
| F11 | Benchmark workloads, tolerances, RSS method and raw-result retention were undecided; "native fit" was ambiguous. | Separate backend fit timing from independent native algorithm work; record measurement and retention decisions before the first benchmark. No benchmark or result is invented. |
| F12 | Maintainer roles and private vulnerability reporting are not established in policy documents. | Record as pre-release decisions. No maintainer appointment, contact assumption or settings change is made. |

All corrections preserve the [architecture](../ARCHITECTURE.md). [ADR 0001](decisions/0001-python-first.md) records the existing Python-first/native boundary; [ADR 0002](decisions/0002-training-contracts.md) proposes the contract and module-map clarifications for review. Neither is implementation evidence.

## Remaining technical decisions

Recommendations below are proposals, not additional approved requirements. Decide each item before its dependent work; do not silently choose a policy from an example.

| ID | Decision | Recommendation or limits | Gate |
|---|---|---|---|
| D01 | Verified Python/OS/backend support and dependency groups | Begin verification with the existing Ubuntu/Python 3.12 configuration. Decide whether scikit-learn remains core or becomes optional, how table-input packages are declared, and which backend versions are tested. Do not claim all Python >=3.12 combinations are supported. | Before Phase 0B dependency/CI edits; expand with feature evidence |
| D02 | Complete estimator and adapter contracts | Review the `fit -> self`/adapter `fit -> None` proposal, report access and error specialization; finalize signatures, fitted-state/refit behavior, capability types, parameter round trips, seed defaults, algorithm identifiers and initial scikit-learn estimator list. | Before Phase 1 coding; additional estimator details before Phase 2 |
| D03 | Input and schema compatibility | Define accepted target shapes/types, sparse layouts, categorical/missing-value handling, named/positional mixing and prediction/update schema checks per supported backend. Preserve feature semantics and ordering. | Before each Phase 1/2 input path and Phase 5 updates |
| D04 | Persistence and trust | Select backend-specific artifacts, manifest/compatibility checks and trusted-loading policy, especially for scikit-learn. No untrusted pickle/joblib loading by default. | Before Phase 2 persistence implementation |
| D05 | Resource-budget semantics | Define memory units, measurement scope/sampling and overrun reporting, CPU-thread mapping/pool behavior and conflicting-setting handling. Recommendation: reject conflicting thread settings instead of silent precedence. Hard enforcement is not initially promised. | Basic rules before Phase 1; expanded controls before Phase 3 |
| D06 | Benchmark configuration and raw evidence | Predeclare workloads/generators, datasets/licenses/checksums, shapes/dtypes, splits/seeds, matched parameters, quality tolerances, repetitions, timing boundaries, RSS method and result storage/retention. Synthetic fixtures are a candidate, not a selected workload. | Before the first Phase 1 comparison; extend for later experiments |
| D07 | Metadata and fingerprints | Define data fingerprint scope, cost and privacy behavior, stable report fields and user-provided split metadata. Do not store private rows or imply internal splitting. | Before Phase 1 reports and benchmark implementation |
| D08 | AutoML search and budgets | Decide candidates/space, metric defaults, trial/time settings, cancellation and possible overrun during a running fit. Require user-prepared validation; do not claim hard termination without a mechanism. | Before Phase 4 implementation |
| D09 | Online estimators and update semantics | Select at least one genuine online classifier and regressor; define initialization/classes, schema/state checks and held-out evaluation. Warm start is not online update. | Before Phase 5 implementation |
| D10 | Native algorithm selection and optimization | No algorithm or native identifier selected. Require a written design and benchmark plan, reference correctness, independent baselines, then measured optimization; Rust needs explicit approval. | Separate later research milestone |
| D11 | Release ownership, reporting and timing | Identify maintainers/project lead, establish a private security reporting route, and choose a release date only when ready. Repository settings and publication require explicit authorization. | Before Phase 6 release approval |

## Milestones and acceptance

The [roadmap](../ROADMAP.md) preserves the approved sequence:

1. **0A:** Reconcile specifications, report and ADRs; obtain review and approval.
2. **0B:** After that approval, correct setup gaps and verify build/install, dependency policy and CI foundations.
3. **1:** Minimal contracts/registry → prepared NumPy/pandas validation → LightGBM classifier/regressor → basic CPU/reporting → matched baseline.
4. **2:** scikit-learn and conditional XGBoost, metrics, Polars/Arrow conversion, persistence implementation and shared contracts.
5. **3:** Resource controls, profiling and optimizations with equivalent before/after evidence.
6. **4:** Optional bounded AutoML, explicit validation, cancellation tests and separate search comparisons.
7. **5:** True online classifier/regressor updates, capability/schema checks, quality and update-versus-retrain evidence.
8. **6:** Full v0.1.0 acceptance, supported-environment evidence, examples, licensing/security and release review.
9. **Later research:** Independent native algorithms after integrated baselines/resource validation; never a blocker for the first integrated release.

The [requirement traceability table](../ROADMAP.md#v010-requirement-traceability) maps every original v0.1.0 must-have and FR-01–FR-10 to delivery and verification. No requirement is deferred by this reconciliation. Implement each scoped task through a feature branch and pull request; announce exact files and focused checks before coding.

## Phase 0A changes

Updated `AGENTS.md`, `PRD.md`, `ARCHITECTURE.md`, `DESIGN.md`, `ROADMAP.md`, `BENCHMARKS.md`, `TESTING.md`, `README.md`, `CONTRIBUTING.md` and ADR 0001. Added this report and ADR 0002. `SCOPE.md`, `NATIVE_ENGINE.md`, licensing, governance/security policy, source, tests, `.gitignore`, packaging, lockfile and CI remain unchanged.

## Verification

Checks ran in the existing Python 3.12.3 environment without synchronizing dependencies. Cache/bytecode writes were disabled for the checks below.

| Command or check | Outcome |
|---|---|
| `PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -B /tmp/raceml_phase0a_docs_check.py` | Passed: 18 repository Markdown files, 50 local links/anchors, balanced fences and five syntax-valid Python snippets. This was an ad hoc standard-library audit in `/tmp`, not new repository tooling. |
| Same documentation audit: scope and requirement preservation | Passed: exactly 12 documentation changes; original PRD scope, FR-01–FR-10, non-functional requirements and performance hypotheses unchanged; every FR traced in ROADMAP. Scope/native documents, source, tests and setup files unchanged. |
| `.venv/bin/ruff check --no-cache .` | Passed. |
| `.venv/bin/ruff format --check --no-cache src/ tests/` | Passed: nine files already formatted. |
| `PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -B -m mypy --no-incremental --cache-dir=/dev/null src/raceml` | Passed: ten local source files checked, including the two ignored placeholders. |
| `PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -B -m pytest -p no:cacheprovider` | Passed: one scaffold import test. |
| `git diff --check` | Passed after removing trailing whitespace from the edited PRD header. |

Manual review checked training-only scope, canonical naming, dual-engine separation, optional/manual behavior, milestone dependencies and the distinction between established decisions, proposals and unresolved details. Link checks were local; external URLs and rendered Mermaid diagrams were not validated. Syntax-valid examples are not executable feature evidence.

Package builds, clean artifact installation, backend integrations and benchmarks were not run in Phase 0A. Hosted CI status belongs to the pull request and is not inferred from local checks. There are no performance measurements and no claim of improvement. Phase 0B and implementation remain gated on Phase 0A review and approval.
