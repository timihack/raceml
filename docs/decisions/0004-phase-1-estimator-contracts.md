# ADR 0004 — Phase 1 estimator and backend fit contracts

**Status:** Accepted in [PR #4](https://github.com/timihack/raceml/pull/4). Initial core foundations implemented for separate review; no public estimator implementation.

**Date:** 2026-11-16

## Context

Phase 0A and Phase 0B are merged in PRs #2 and #3. The user confirmed readiness for the next task after creating `docs/phase-1-estimator-contracts`. The prior reconciliation established the architecture and milestone sequence, but left detailed constructor/fit routing, defaults, fitted state, schema behavior and error contracts open. The user specifically asked about backend fit options such as validation data and verbosity.

The Phase 0 register groups initial and later estimator details under D02. This proposal scopes the first implementation contract to LightGBM, leaving the exact scikit-learn list/identifiers gated before their Phase 2 adapters, as the approved roadmap sequences them. It does not approve an unspecified scikit-learn integration or drop a required backend.

## Proposed decision

Adopt the [Phase 1 contract specification](../PHASE_1_CONTRACTS.md) after review, while preserving training-only scope and the existing component boundaries:

- Require an explicit algorithm; initially implement only the `lightgbm` classifier/regressor registry entry, with lazy backend imports and no manual-mode tuner imports.
- Preserve flat validated backend constructor keywords. Fit accepts explicit `validation_data`, `sample_weight` and validated native `**fit_params`; never route an option to a different operation silently.
- Map canonical validation data through the selected adapter/version and reject duplicate or competing validation sources. A backend's broader file/container API does not expand RaceML's prepared-input boundary.
- Propose `cpu_cores=1`, `memory_limit=None` and `random_state=None`, with explicit thread/seed alias conflict errors. Memory remains an observed budget.
- Preserve public `fit -> self`, internal adapter `fit -> None`, a separate report and configuration inspection. Specify numeric NumPy/pandas input/schema rules, fresh-fit lifecycle, output shapes, fitted attributes and a dependency-free typed error hierarchy including `NotFittedError`.
- Keep capability discovery honest and conditional: no implied LightGBM online update, no persistence or native algorithm implementation in this task, no automatic backend substitution or search.

The new inspection/default/error details are review proposals that make existing acceptance requirements testable, not assertions of implemented APIs. No dependency or architecture layer is added. Public names remain `RaceMLClassifier` / `RaceMLRegressor`; optional AutoML and classifier/regressor online learning remain required for v0.1.0 in their existing milestones.

## Evidence motivating separate fit routing

The contract specification links the inspected primary backend references. LightGBM 4.7.0 introduces a validation argument change and does not accept fit-time `verbose`; the inspected XGBoost and CatBoost references accept fit-time verbosity. Therefore neither unchecked passthrough nor a universal set of fit keywords is sufficient. The references are not installed-version tests, and the inspected XGBoost stable version differs from the current lockfile.

## Alternatives and trade-offs

- A nested `backend_fit_params` mapping would separate namespaces but add another wrapper convention. Direct fit keywords preserve native call style while reviewed routing enforces the operation boundary.
- Treating a backend `**kwargs` as permission for arbitrary names would allow typos or unsupported options to be ignored. Explicit signatures plus versioned catalogs provide errors before training.
- A global `verbose` or early-stopping abstraction would hide backend differences. Native options remain explicit; a new cross-backend abstraction would need a separate proposal.
- Transactional refit could retain the previous model while training a replacement, increasing peak memory. The proposed lifecycle preserves old state through preflight only, then releases it before fresh backend training; a training failure leaves the estimator unfitted.
- The initial numeric input subset is deliberately explicit. Further categorical/sparse/extension paths require declared compatibility, without deferring mandatory container support to another release.

## Approval, verification and remaining decisions

Review this ADR and the concrete signatures/defaults/initial input subset before estimator implementation. This branch changes documentation only and runs documentation/existing repository checks. Resource measurement/fingerprint/benchmark choices remain gates before reports and comparisons; installed backend catalogs require tests before a support claim. Phase 2+ estimator selection, persistence, AutoML budgets, online updates and native algorithm research retain their existing approval and verification gates.
