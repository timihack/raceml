# ADR 0002 — Reconcile training contracts and delivery prerequisites

**Status:** Proposed for Phase 0A review; no implementation authorized by this ADR

**Date:** 2026-11-16

## Context

The existing specifications establish training-only scope and two backend families, but leave conflicting or incomplete details: a validation strategy could imply internal splitting; adapter metadata is missing from the illustrative protocol; fit return behavior is ambiguous; the first adapter precedes registry/capability work; module paths disagree; persistence implementation and Polars/Arrow conversion lack explicit delivery tasks.

The user approved specification reconciliation and the milestone order, while requiring Phase 0A review and approval before Phase 0B or implementation. This ADR distinguishes preserved decisions from proposed contract clarifications. It does not select unresolved technical details or reduce v0.1.0 scope.

## Preserved decisions

- Public estimators are `RaceMLClassifier` and `RaceMLRegressor`; optional automation is `RaceMLAutoClassifier` and `RaceMLAutoRegressor` in namespace `raceml`.
- Users supply prepared features, labels and validation splits. RaceML validates inputs and performs backend-required conversion only. No loading, cleaning, imputation, feature engineering or splitting API.
- Manual training is default; optional AutoML must not be imported or invoked by manual mode. AutoML delivery remains required for v0.1.0.
- Integrated adapters arrive first. Independent native RaceML algorithms are later research under [ADR 0001](0001-python-first.md) and [NATIVE_ENGINE.md](../../NATIVE_ENGINE.md), not renamed wrappers.
- Online updates, probability prediction and persistence are capability-dependent. Unsupported online updates must fail explicitly without a substitute algorithm or full retraining. At least one online classifier and regressor remain required for v0.1.0.
- Initial in-process memory limits are observed budgets, not hard caps. No performance hypothesis is an achieved result.

## Proposed reconciliation

1. Remove internal validation-strategy language. Both manual evaluation and AutoML consume explicit user-prepared validation inputs. Split metadata is recorded when supplied; the library does not generate it.
2. Public estimator `fit` returns `self`; `resource_report()` exposes a separate report. In the illustrative internal protocol, adapter `fit` mutates state and returns `None`. Add required adapter metadata alongside fit, predict, parameter inspection and capability discovery. Keep optional operations out of the universal base protocol.
3. Include `UnsupportedUpdateError` in the error taxonomy as a proposed specialization of `UnsupportedCapabilityError`. Final error inheritance and pre-fit behavior are decisions before Phase 1 coding.
4. Establish the minimal registry, capabilities, configuration and errors before the LightGBM adapter in Phase 1. Phase 2 extends those foundations with scikit-learn and conditional XGBoost, metrics, Polars/Arrow conversion and actual persistence implementation.
5. Use the planned module map in [DESIGN.md](../../DESIGN.md#11-proposed-internal-modules): `input/` for validation/conversion, `engine/` for the existing training-execution responsibility, `models/` for public estimators and `models/backends/` for integrated adapters. Other documented responsibilities remain unchanged; no new architecture layer or empty-file scaffolding is requested. Native algorithm files are deferred to their approved research milestone.
6. Separate Phase 0A documentation review from Phase 0B setup changes. Record the ignore-rule, dependency and CI gaps now; fix them only after the review gate. Keep all original v0.1.0 requirements and their conditional/deferred qualifications.

## Remaining decisions

This proposal does not settle the complete estimator signatures, defaults, fitted attributes, refit semantics, algorithm identifiers, backend parameter namespace, capability types, input matrix, persistence formats/trust policy, dependency groups, verified support matrix, budget semantics or benchmark configurations. The [Phase 0 decision register](../PHASE_0_REPORT.md#remaining-technical-decisions) records when each must be resolved. Rejecting conflicting thread settings is a recommendation for review, not an implemented rule.

## Consequences and alternatives

Returning `self` keeps the fit example estimator-oriented; a model/report tuple would require revising the examples and return contract. A separate report method already exists in the proposed API. Using `input/` makes the scope visible and matches the existing scaffold; retaining `data/` would require equally explicit restrictions and reconciliation with that scaffold.

Moving foundational contracts before their first consumer removes a delivery dependency error without adding a framework. Explicit Phase 2 conversion and persistence tasks close roadmap gaps without deferring product requirements. Detailed choices remain gated rather than being inferred from examples.

## Verification and approval

Phase 0A verification is documentation consistency, link/anchor and example syntax checks, whitespace checks and existing repository checks. No estimator behavior, package build, integration or performance result is established by this ADR. Review and approve the Phase 0A change before starting setup or implementation; then finalize technical details before their dependent milestone tasks.
