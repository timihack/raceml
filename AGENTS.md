# Instructions for Coding Agents Working on RaceML

This file governs automated contributions to the RaceML repository.

## Project identity

RaceML = Resource-Aware Compute Engine for Machine Learning. Open-source, general-purpose ML library, initially tabular and CPU-first. Manual training is default; AutoML is opt-in. Status at document creation: pre-development.

## Source of truth

`SCOPE.md` and `NATIVE_ENGINE.md`, together with the mandatory decisions below, constrain all specifications. Older passages cannot expand these boundaries. Within those boundaries:

1. `PRD.md` defines scope and acceptance criteria.
2. `ARCHITECTURE.md` defines component boundaries.
3. `DESIGN.md` defines intended APIs and contracts.
4. `BENCHMARKS.md` defines performance methodology.
5. `ROADMAP.md` defines implementation sequence.
6. `TESTING.md` defines verification.

If documents conflict, stop and describe the conflict instead of guessing. Propose a minimal documentation change and request approval before changing a high-level decision.

The [Phase 0 report](docs/PHASE_0_REPORT.md) records reconciliation findings, unresolved decisions and milestone gates. A proposed ADR or illustrative API is not evidence of implementation or approval. Phase 0A must be reviewed and approved before Phase 0B setup changes or feature implementation begin.

## Before any coding task

- Read the relevant documents and existing code.
- State the exact files expected to change and the test plan.
- Keep work within the requested milestone.
- Do not add a new dependency, native component, public API or architecture layer without explaining the reason.
- Ask when requirements are ambiguous or an irreversible decision is needed.

## Implementation rules

- Python-first; do not introduce Rust until profiling and approval justify it.
- Prefer small, typed, testable modules over speculative abstractions.
- Keep model backends behind explicit adapter interfaces.
- Never silently replace the requested algorithm or retrain when online updates are unsupported.
- Keep AutoML separate and optional; never start it in manual mode.
- Treat memory limits as observed budgets unless hard enforcement exists.
- Avoid unnecessary data copies; measure before claiming zero-copy behavior.
- Preserve feature ordering, schema and reproducibility metadata.
- Avoid unrelated refactors and unnecessary comments.
- Never add telemetry or network access by default.

## Performance claims

20% faster end-to-end training and 30% lower peak RAM are research targets, **not** established results. Do not put them in release notes as achievements without reproducible measurements. Benchmark direct backends fairly, report losses as well as wins and preserve raw data.

## Testing and completion

- Write unit and integration tests for changed behavior.
- Run focused tests first, then relevant broader checks.
- Include negative tests for invalid configuration, missing backend, unsupported capability and schema mismatch.
- For performance work, include before/after measurements with equivalent conditions.
- Report commands executed, outcomes and unrun checks. Never claim a test passed if it was not run.
- Do not publish packages, push branches, merge PRs, alter secrets or modify deployment without explicit approval.

## Security

Do not load untrusted pickle/joblib artifacts. Never expose credentials or private dataset records in logs. Review third-party dependency licenses before redistribution.

## Task completion format

Summarize: files changed; behavior added; tests run and results; benchmark evidence if relevant; known limitations; next suggested task. Do not claim completion of work that remains unfinished.

## Mandatory scope and naming decisions

- Canonical public estimators: `RaceMLClassifier`, `RaceMLRegressor`; optional automation: `RaceMLAutoClassifier`, `RaceMLAutoRegressor`.
- **Do not implement data loading, cleaning, imputation, feature engineering, or splitting APIs.** User supplies prepared `X` and `y`. Only input validation and backend-required conversion belong in RaceML.
- Maintain two backend categories: established integrated adapters now, independently developed native RaceML algorithms later. Do not describe wrappers as native algorithms.
- Read `SCOPE.md` and `NATIVE_ENGINE.md` before planning changes. If an older passage conflicts with these rules, follow these rules and flag the inconsistency.
