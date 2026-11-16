# RaceML Phase 1 Estimator Contract Proposal

**Status:** Accepted in [PR #4](https://github.com/timihack/raceml/pull/4). Initial core foundations are implemented for separate review; public estimators and the full Phase 1 vertical slice remain incomplete. See the [core implementation report](PHASE_1_CORE_REPORT.md).

**Date:** 2026-11-16

## 1. Scope and review decisions

This proposal resolves Phase 1 portions of D02 (estimator/adapter contracts) and D03 (initial input/schema compatibility), plus configuration portions of D05. It preserves [SCOPE.md](../SCOPE.md), [NATIVE_ENGINE.md](../NATIVE_ENGINE.md), optional AutoML, the NumPy-only core and all v0.1.0 requirements. No source, tests, dependencies, CI or backend integrations are changed here.

Public additions accepted beyond the earlier illustrative examples are `random_state`, `sample_weight`, a public `get_params()`, documented fitted attributes and `NotFittedError`. They make reproducibility, training weights, configuration round trips and pre-fit failures explicit. They add no architecture layer or dependency. The existing illustrative constructor keywords, `validation_data`, fit keyword forwarding, prediction, report and capability-dependent operations are made precise below. These choices were reviewed in PR #4; acceptance is not evidence of implemented public APIs.

Phase 1 delivers only the `lightgbm` registry entry for classification/regression. No algorithm is selected by default. Later scikit-learn identifiers/estimators need Phase 2 review; XGBoost remains conditional for v0.1.0, CatBoost remains later work, and no native RaceML identifier is selected. A backend dependency being installed does not register an implemented adapter automatically.

Phase 1 admits CPU execution only. A backend option requesting an unsupported GPU or distributed execution path fails explicitly rather than being silently changed to CPU execution.

## 2. Proposed public interface

The namespace remains `raceml`. The same constructor and fit signature apply to `RaceMLRegressor`; probability prediction is classifier-only. The following is a signature proposal, not executable library code:

```python
from typing import Any, Self


class RaceMLClassifier:
    def __init__(
        self,
        *,
        algorithm: str,
        cpu_cores: int = 1,
        memory_limit: str | None = None,
        random_state: int | None = None,
        **backend_params: Any,
    ) -> None: ...

    def fit(
        self,
        X: Any,
        y: Any,
        *,
        validation_data: tuple[Any, Any] | None = None,
        sample_weight: Any = None,
        **fit_params: Any,
    ) -> Self: ...

    def predict(self, X: Any) -> Any: ...
    def predict_proba(self, X: Any) -> Any: ...
    def get_params(self) -> dict[str, Any]: ...
    def resource_report(self) -> dict[str, Any]: ...
```

`Any` in this sketch avoids importing optional table/backends at import time; accepted inputs and return shapes are constrained below. Implementation types must express those contracts with NumPy types and optional imports under type checking. This is not a promise of scikit-learn inheritance, cloning, `set_params`, metadata routing or pipeline compatibility.

Construction checks RaceML configuration and the registered task/algorithm without importing a concrete backend or tuner. Backend parameter/version checks occur lazily at fit, before backend training begins. `get_params()` works before fit and returns a fresh flat mapping of RaceML settings plus caller-supplied backend constructor parameters; it includes no fit data, fitted model or report. It does not instantiate the backend to expand its defaults. Reconstructing the same estimator class with that mapping preserves the requested configuration; nested user objects are not deep-copied or serialized.

## 3. Constructor options and fit options

Constructor keywords after RaceML settings belong to the selected backend constructor. Keywords passed to `fit` belong to its fit operation. Neither set is silently moved to the other, ignored or interpreted as an AutoML search space. No alternate `val_data` alias is proposed.

The adapter declares separate accepted constructor and fit parameters for each verified backend version. Explicit backend signatures are checked alongside a reviewed catalog for native parameters accepted through backend `**kwargs`. A variadic signature alone does not authorize arbitrary names: unknown or unreviewed options fail with `InvalidConfigurationError` before backend training, with a supported-version explanation. A recognized operation that RaceML deliberately does not support raises `UnsupportedCapabilityError` instead. RaceML validates its own settings, option routing and documented constraints; it does not promise to duplicate every backend value validator. Remaining backend constraints may raise during backend execution, without retry or substitution.

- `cpu_cores`: a positive integer, excluding booleans; default 1. For LightGBM it maps to `n_jobs`. Explicit backend thread aliases are rejected, even if numerically equal, with guidance to use `cpu_cores`; there is no silent precedence or clamping. Initial mapping does not promise control over every BLAS/OpenMP pool.
- `random_state`: `None` or an integer in `[0, 2**32 - 1]`, excluding booleans. LightGBM receives that canonical setting. Aliases of the backend's main seed are rejected with guidance to use it; independent component-seed settings may remain explicit reviewed backend parameters. `None` uses backend seed behavior; RaceML does not generate a hidden seed or promise deterministic output.
- `memory_limit`: `None` or a positive human-readable byte budget. Proposed units are decimal `B`, `KB`, `MB`, `GB` and binary `KiB`, `MiB`, `GiB`, with positive decimal quantities resolving to a whole number of bytes. Reject unknown units, nonpositive values and ambiguous inputs. It is monitored, never an initial hard cap; exceeding it is reported without pretending enforcement exists.
- Backend algorithm parameters keep documented defaults unless the user supplies an accepted value or RaceML applies one of its declared resource/seed mappings. Record requested and effective settings separately.

Callbacks and custom evaluation functions are explicit trusted user code, forwarded only when supported at that operation. They are not invoked during validation, cloned, tuned or silently injected by RaceML. Users provide fresh stateful callbacks for repeated fits as required by their backend. Reports store fit option names, not callbacks, their representations, arrays or arbitrary Python objects. Objective options that invalidate the standard prediction/probability contract must fail explicitly; custom-objective support needs its own verified output contract before admission.

## 4. Validation data and native fit arguments

`validation_data=(X_valid, y_valid)` represents one user-prepared validation pair. RaceML never creates a split, aligns rows by index, encodes features or uses test labels for model selection. Supplied validation rows receive the same feature/target validation as training rows. RaceML cannot determine whether a caller has mislabeled their held-out test set as validation.

Only one source of validation data is permitted in a fit call: the canonical argument, a native paired-set argument, or a native feature/target pair. Reject canonical/native combinations, mixed native forms, missing pairs and duplicate aliases even if values appear identical. Native arguments may represent multiple explicit validation pairs when the selected version supports them; check every pair and preserve order. Auxiliary evaluation names/weights/scores must match those pairs under the adapter's declared shape contract, or fail before training.

Native validation values of `None` do not select an additional source; empty supplied sets are invalid, and a feature/target pair with only one non-`None` side is incomplete. This does not permit unknown parameter names merely because their values are `None`.

The adapter maps the canonical pair to the selected supported backend API; it does not invent a universal backend `fit` signature. These inspected upstream references illustrate why versioned routing is necessary:

| Reference checked on 2026-11-16 | Validation argument and logging location | RaceML consequence |
|---|---|---|
| [LightGBM classifier 4.7.0](https://lightgbm.readthedocs.io/en/stable/pythonapi/lightgbm.LGBMClassifier.html#lightgbm.LGBMClassifier.fit) and [regressor 4.7.0](https://lightgbm.readthedocs.io/en/stable/pythonapi/lightgbm.LGBMRegressor.html#lightgbm.LGBMRegressor.fit) | `eval_X`/`eval_y`; `eval_set` is deprecated. Fit accepts callbacks, not `verbose`. | Canonical validation uses the new pair for 4.7. A reviewed native `eval_set` path may retain the backend deprecation warning; never suppress or reinterpret it silently. `fit(verbose=...)` fails with guidance to supported logging controls. |
| [LightGBM logging callback](https://lightgbm.readthedocs.io/en/stable/pythonapi/lightgbm.log_evaluation.html) | Explicit evaluation-logging callback. | User may pass it through supported fit callbacks; RaceML does not create it automatically. |
| [XGBoost stable API 3.4.2](https://xgboost.readthedocs.io/en/stable/python/python_api.html#xgboost.XGBClassifier.fit) | Fit has `eval_set` and `verbose`; current constructor options include callbacks and early-stopping configuration. | A later adapter must distinguish constructor and fit options; do not copy LightGBM routing. |
| [CatBoost classifier fit](https://catboost.ai/docs/en/concepts/python-reference_catboostclassifier_fit) | Fit has `eval_set` and `verbose`, including forms involving files. | Reference only; CatBoost is deferred. RaceML's training-only boundary would still reject data-file inputs. |

These are documentation observations, not a verified backend matrix. XGBoost's inspected stable docs are 3.4.2 while the lockfile currently has 3.4.1. Each actual adapter/version requires tests against its installed signature and behavior before support is claimed. Older LightGBM versions require their own reviewed routing; a broad install requirement is not evidence of compatibility.

For Phase 1, constructor tuning and safe fit controls such as evaluation metrics, weights and callbacks are admitted only with the declared version/shape checks. A non-`None` `init_model` requests continuation, not an online update; reject it explicitly until warm-start/trusted-model handling is approved and tested. File-based training/validation inputs, file-loading shortcuts and unreviewed model-loading routes are never accepted through keyword forwarding. Native feature-name overrides must not contradict RaceML's recorded schema. Backend-native categorical/missing-value behavior is allowed only on an explicitly declared compatible input path.

Illustrative use after implementation and approval:

```python
from raceml import RaceMLClassifier

model = RaceMLClassifier(
    algorithm="lightgbm",
    cpu_cores=4,
    random_state=42,
    n_estimators=500,
)
model.fit(
    X_train,
    y_train,
    validation_data=(X_valid, y_valid),
    sample_weight=train_weights,
    eval_metric="binary_logloss",
    callbacks=user_callbacks,
)
```

## 5. Phase 1 input and schema proposal

The initial declared subset is dense, real numeric/bool NumPy feature arrays and numeric/bool pandas DataFrames, with one-dimensional NumPy or pandas Series targets. NumPy feature arrays must be two-dimensional; all training/validation datasets are nonempty with at least one feature and matching target lengths. Prediction inputs are also nonempty and two-dimensional. Reject complex/object/string features, duplicate/non-string DataFrame column names, missing/infinite targets, infinite numeric features, multi-output/multilabel targets and unsupported nullable extension dtypes explicitly. This subset does not promise every dtype supported by a backend. Broader categorical, sparse and extension-dtype paths require explicit compatibility decisions and tests before being admitted; Polars/Arrow remain required Phase 2 work.

Classification supports binary and multiclass homogeneous boolean/integer/integral-float/string labels with at least two training classes; numeric labels must be finite. Regression targets are finite real numeric values. No implicit target reshaping, numeric-string coercion, row filtering or imputation. Validation classification labels must belong to training classes. Feature NaNs are permitted only when the selected adapter declares backend-native missing-value support; RaceML preserves them rather than imputing. `sample_weight`, when supplied, is one-dimensional real numeric data with matching row count, finite nonnegative values and at least one positive weight.

Rows are positional, including pandas inputs: RaceML does not join/reindex data. Named feature inputs require exact feature names and order at validation/prediction; unnamed inputs require the fitted feature count and positional order. Reject named/unnamed feature mixing rather than inventing name mappings. Numeric widths may differ when the declared backend path supports both, but incompatible dtype-kind changes fail. RaceML does not sort columns, silently drop extras or mutate caller-owned arrays/tables. Report necessary conversions/copies without a zero-copy promise.

For unnamed arrays, a same-width column permutation cannot be detected from shape alone; users own ordering. Category-vocabulary semantics, pandas categorical support and sparse layout tests remain explicit extension gates; this initial numeric subset does not move NumPy/pandas delivery out of Phase 1 or Polars/Arrow out of v0.1.0.

## 6. Fitted state, outputs and failures

Every successful `fit` returns `self` and represents a fresh training run using the requested configuration, never a hidden online update or search. Validate configuration, capabilities and inputs before changing existing fitted state. Once backend training starts, clear previous fitted state and release the old adapter reference; a backend failure leaves the estimator unfitted. This avoids promising rollback or retaining two complete models for transactional retraining. There is no guarantee that native allocations are immediately returned to the OS. Calls on the same estimator are not promised thread-safe.

After success expose `n_features_in_`, `classes_` for classifiers, `feature_names_in_` only for named input, and a `metadata_` snapshot. Do not invent feature names for unnamed RaceML inputs or expose training data through those attributes. Class order is stable and matches the probability columns; predictions preserve input row order and original class labels.

| Operation | Result | Required failure behavior |
|---|---|---|
| `fit(...)` | Same estimator instance | RaceML configuration, option routing/schema and unavailable backend checks precede training; backend execution constraints may fail during training and leave unfitted state as described above. |
| `predict(X)` | NumPy array of shape `(n_rows,)`: labels for classification, numeric predictions for regression | `NotFittedError` before fit; `DataSchemaError` for mismatched features. No raw scores, leaves or contributions silently substituted. |
| Classifier `predict_proba(X)` | Floating NumPy array `(n_rows, n_classes)` matching `classes_`, including two columns for binary classification | `NotFittedError` before fit; `UnsupportedCapabilityError` when probability semantics are unsupported; schema failures explicit. |
| `get_params()` | Fresh requested-configuration mapping, before or after fit | No backend/tuner import; no fit-only options or data included. |
| `resource_report()` | Fresh mapping snapshot with measurement method/limitations, requested/effective resources and observed timings/RSS | `NotFittedError` without a successful fit. Unknown/unmeasurable values are labeled, never fabricated. Exact measurement protocol is a separate gate below. |

Prediction kwargs that would change these output semantics are outside this initial signature. Supporting another operation later requires its own explicit contract, not overloading `predict` to return unrelated shapes.

Proposed error inheritance uses Python built-ins without a required scikit-learn import: `InvalidConfigurationError` and `DataSchemaError` derive from `ValueError`; `BackendUnavailableError` from `ImportError`; `NotFittedError` from `RuntimeError`; `UnsupportedCapabilityError` from `NotImplementedError`; `UnsupportedUpdateError` from `UnsupportedCapabilityError`. Unknown/unimplemented algorithms are invalid configuration; missing dependencies for implemented algorithms give installation guidance. Backend execution failures are not silently converted into another algorithm or hidden retraining. Error messages and routine metadata must not include private rows, credentials or callback representations.

`update`, warm starts and save/load remain capability-specific later milestones. LightGBM's initial entry declares no online update or admitted warm start. Any exposed unsupported update raises `UnsupportedUpdateError`, with no call to fit. Regressors do not expose a working probability operation. Persistence error/format contracts are finalized in Phase 2, not invented here.

## 7. Internal adapter and metadata responsibilities

The minimal base protocol remains fit, predict, requested-parameter inspection, metadata and capability discovery. Internal adapter fit returns `None`; the public estimator returns `self`. Input validation produces a schema and backend-required representation; core execution routes validated fit options. No concrete backend is called directly from the public API, and no optional tuner is imported by the manual path.

The registry records algorithm identifier, integrated/native category, task, supported backend/version path, accepted input formats and dtype constraints, probability/update/warm-start/persistence support, and separate constructor/fit parameter rules. Capability discovery describes actual implemented operations; installation, a matching method name or `**kwargs` is not sufficient evidence. Do not add registration APIs or generic plugin loading to implement this fixed initial entry.

For the existing illustrative `capabilities() -> dict[str, bool]` protocol, propose required keys `predict_proba`, `online_update`, `warm_start`, `full_retrain` and `persistence`. The initial LightGBM classifier declares only `predict_proba` and `full_retrain` true; its regressor declares only `full_retrain` true. `full_retrain` describes ordinary fresh fit, never an update fallback or another public method. Registry fields carry the non-boolean schema/version/task details. A missing package raises `BackendUnavailableError`; an installed but unverified version path raises `UnsupportedCapabilityError` with declared compatibility guidance, not a false missing-package claim.

Training metadata records task, algorithm and backend category/version, RaceML/Python/package versions, schema, requested/effective configuration and seed/thread mappings, fit option names, timing phases and measurement limitations. Store only approved non-sensitive configuration fields; omit arbitrary objects and private data, documenting omissions. Record split identifiers/seeds only when supplied by the user. Do not retain validation/training arrays in reports or serialize callbacks as metadata.

## 8. Implementation and evidence gates

Approval of this proposal permits the contracts it defines to guide separately scoped implementation; it does not establish measured support. Implement in dependency order: configuration/errors and fake-adapter contracts → registry/capabilities → numeric NumPy/pandas validation → installed LightGBM mapping/fit/predict → resource reports → matched direct-backend baseline. Announce exact source/test files before each coding task and use feature branches/PRs.

Remaining decisions must be resolved before their dependent tasks:

| Gate | Remaining decision |
|---|---|
| Before the LightGBM adapter is claimed supported | Verified installed backend/version matrix and accepted constructor/native-fit catalogs, including continuation/custom-objective restrictions and native validation variants. Documentation examples are not runtime evidence. |
| Before resource reporting and the first comparison | D05 RSS method/sampling, phase boundaries and overrun observations; D07 fingerprint policy/cost/privacy and report field details; D06 exact workloads/seeds, quality tolerances, repetitions and raw-result destination. No research target is guaranteed. |
| Before Phase 2 additions | Specific scikit-learn identifiers/estimators; broader input compatibility; conditional XGBoost contracts; safe persistence formats. Review options that internally create holdouts against the user-owned splitting boundary rather than forwarding them blindly. |
| Before Phases 4/5 or native research | AutoML search/budget/cancellation contracts, online initialization/class semantics, and separately approved native algorithm design remain later gates. |

The proposed acceptance cases are listed in [TESTING.md](../TESTING.md#phase-1-contract-acceptance-proposal). No backend integration or benchmark is run by this documentation change.

## 9. Proposal verification record

This section is the historical verification snapshot for the documentation-only contract PR, before PR #4 was merged. Current implementation scope and evidence are recorded separately in the core report linked above.

Changed files are `DESIGN.md`, `ARCHITECTURE.md`, `TESTING.md`, `ROADMAP.md`, this specification and [ADR 0004](decisions/0004-phase-1-estimator-contracts.md). The two pre-existing empty local model placeholders remain untracked and untouched. No source, tests, dependencies, setup, original PRD requirements or mandatory scope/native boundaries changed. Work remains unstaged, uncommitted and unpushed for the user.

Local checks used the existing Python 3.12.3 environment. The following commands ran with `PYTHONDONTWRITEBYTECODE=1` for Python checks and without tool caches:

| Check | Outcome |
|---|---|
| `.venv/bin/python -B /tmp/raceml_phase1_docs_check.py` | Passed: 22 Markdown files, 71 local links/anchors, seven Python snippets and balanced fences. Ad hoc standard-library audit, not new repository tooling. |
| `.venv/bin/ruff check --no-cache .` | Passed. |
| `.venv/bin/ruff format --check --no-cache src/ tests/` | Passed: 12 local Python files, including the two existing placeholders. |
| `.venv/bin/python -B -m mypy --no-incremental --cache-dir=/dev/null src/raceml` | Passed: ten local source files, including the two existing placeholders. |
| `.venv/bin/python -B -m pytest -p no:cacheprovider` | Passed: eight tests, four opt-in artifact checks skipped without `RACEML_DIST_DIR`. |
| `git diff --check` and change-scope audit | Passed: six documentation changes only; existing placeholders untouched and no staged changes. |

Manual review compared this proposal with the original requirements, scope/native boundaries, milestone order and the linked primary backend references. No backend package was installed or executed to verify these proposed mappings. Artifact builds/installations were not rerun for this documentation-only change; no benchmark or hosted CI result is claimed. Syntax-valid snippets are not executable feature evidence.

Next after review: announce exact source/test files for the initial configuration, errors and fake-adapter contract implementation. Real backend/version catalogs, reports and measurements retain the evidence gates above; the full Phase 1 vertical slice is not complete.
