# RaceML Detailed Design

**Status:** Phase 0 reconciliation merged; detailed Phase 1 contract proposal under review. Code samples are illustrative and not implemented.

## 1. Proposed user-facing API

```python
from raceml import RaceMLClassifier

model = RaceMLClassifier(
    algorithm="lightgbm",
    cpu_cores=4,
    memory_limit="4GB",  # monitored budget initially
    n_estimators=500,
)
model.fit(X_train, y_train)
predictions = model.predict(X_test)
report = model.resource_report()
```

Regression follows the same pattern with `RaceMLRegressor`. Constructor kwargs must be validated against backend capabilities; unsupported parameters must fail explicitly.

Public `fit` returns the fitted estimator (`self`); `resource_report()` returns a separate report. The concrete [Phase 1 contract proposal](docs/PHASE_1_CONTRACTS.md) specifies defaults, requested-parameter inspection, fit option routing, fitted state, initial input/schema rules and errors for review before coding. [ADR 0004](docs/decisions/0004-phase-1-estimator-contracts.md) records the choices and alternatives; its proposals are not implemented APIs.

## 2. Optional automation

```python
from raceml.automl import RaceMLAutoClassifier

search = RaceMLAutoClassifier(time_limit=300, cpu_cores=4, metric="roc_auc")
search.fit(X_train, y_train, validation_data=(X_valid, y_valid))
```

`RaceMLAutoRegressor` follows the same pattern. AutoML must not run unless explicitly requested. It must avoid using held-out test data for selection. Training and validation arrays are prepared and split by the user; RaceML never creates an internal split or preprocessing pipeline. Time and trial budgets are required by the PRD; the example does not finalize the trial-budget parameter, defaults, search space or cancellation semantics. Those decisions belong before Phase 4 implementation. Optional installation and use do not remove AutoML from v0.1.0 scope.

## 3. Core contracts

```python
from typing import Protocol, Any


class ModelAdapter(Protocol):
    def fit(self, X: Any, y: Any, **kwargs: Any) -> None: ...
    def predict(self, X: Any) -> Any: ...
    def get_params(self) -> dict[str, Any]: ...
    def capabilities(self) -> dict[str, bool]: ...
    def metadata(self) -> dict[str, Any]: ...
```

This is an illustrative minimum protocol, not final typing. Adapter `fit` mutates adapter state and returns `None` in this proposal; public estimator `fit` returns `self`. Final signatures, capability records, parameter round-trip rules and fitted-state errors must be reviewed before Phase 1 implementation. `predict_proba`, online update and persistence belong to capability-specific contracts. `partial_fit` must not appear as universally supported in the base protocol; expose it via an optional capability or a separate protocol. Registry metadata records task, input constraints, backend version and serialization support.

Each adapter declares constructor and fit options separately for its verified backend/version path. A backend's variadic `**kwargs` is not blanket permission to accept unknown names. The [routing proposal](docs/PHASE_1_CONTRACTS.md#4-validation-data-and-native-fit-arguments) maps explicit user-prepared validation data, rejects competing aliases/sources, and preserves backend-native logging/callback semantics. Unsupported options are never ignored or moved silently between constructor and fit.

## 4. Configuration

- Task: classification or regression.
- Algorithm: explicit registered backend identifier.
- Seed: optional reproducibility setting.
- `cpu_cores`: positive integer within supported constraints.
- `memory_limit`: human-readable budget; monitoring only in initial version.
- Backend parameters: namespaced or validated against backend constructor.
- Validation: explicit user-prepared validation data, with no internal splitting and no held-out test data used for selection.

The Phase 1 proposal retains flat backend constructor keywords and native fit keywords, requires `algorithm`, proposes `cpu_cores=1`, `random_state=None` and `memory_limit=None`, and rejects duplicate thread/main-seed aliases. These concrete choices await review. Initial Phase 1 selection is proposed as `lightgbm` only; the initial scikit-learn estimator list and identifiers remain Phase 2 decisions. See [constructor and fit options](docs/PHASE_1_CONTRACTS.md#3-constructor-options-and-fit-options).

## 5. Input validation and conversion

`DataAdapter` checks shape, target length, column schema, dtype compatibility and missing-value handling. It reports whether a conversion occurred. Never silently drop or reorder features. Record feature names and order for prediction-time validation.

The existing illustrative `DataAdapter` name denotes an internal input adapter only. It provides no loading, cleaning, imputation, encoding, feature engineering or splitting API. Algorithm-native handling may be passed through only when supported and documented. Sparse layouts, target types, categorical/missing-value compatibility and named-versus-positional input checks require explicit compatibility decisions before their implementations.

The [initial numeric input/schema proposal](docs/PHASE_1_CONTRACTS.md#5-phase-1-input-and-schema-proposal) defines a concrete dense NumPy/pandas subset and its failure behavior. Broader dtype/container paths still require declared compatibility; no arbitrary dtype or zero-copy support is implied.

## 6. Model subsystem

`Registry` resolves backend by task and declared capabilities. `RaceMLClassifier` and `RaceMLRegressor` delegate to adapters. The fitted estimator retains the selected adapter, configuration and training metadata under attributes to be specified before implementation. Probability prediction is supported only for applicable models. Minimal registry and capability contracts precede the first adapter in Phase 1; integrated backends and future independent native implementations share those contracts.

## 7. Resource subsystem

`ResourcePlan` holds requested thread count, memory budget and optional time budget. `ResourceReport` records observed wall time, CPU and peak RSS, measurement method and limitations. Resource planning must not silently override user algorithm settings.

An in-process monitored memory budget is not a hard cap. Memory units, observation boundaries, RSS sampling, thread-conflict rules and overrun behavior remain open. No strict time or memory enforcement is implied for an already-running backend fit.

## 8. Incremental subsystem

Three separate capabilities: `online_update`, `warm_start`, `full_retrain`. An `update(X, y)` call is permitted only for an adapter declaring `online_update`. Otherwise raise `UnsupportedUpdateError` with alternatives. No silent retraining.

## 9. Error taxonomy

- `BackendUnavailableError`
- `UnsupportedCapabilityError`
- `UnsupportedUpdateError` (proposed specialization of `UnsupportedCapabilityError` for an update without `online_update` support)
- `InvalidConfigurationError`
- `DataSchemaError`
- `NotFittedError` (Phase 1 proposal for operations requiring a successful fit)
- `ResourceBudgetExceededError` (only when an enforceable mechanism exists)
- `UnsafeModelLoadError`

The Phase 1 proposal adds `NotFittedError` and a [built-in-based inheritance tree](docs/PHASE_1_CONTRACTS.md#6-fitted-state-outputs-and-failures), without a mandatory scikit-learn dependency. Review before implementation. The enforceable-budget error is reserved for a future enforcement mechanism and must not imply one exists initially; persistence types remain a Phase 2 gate.

## 10. Persistence

Persist backend type/version, model artifact, feature schema, task and reproducibility metadata. Serialization format is backend-dependent and must be documented. Untrusted pickle-based loading is not enabled by default.

Format selection, trusted-load policy, manifest validation and compatibility rules remain decisions before Phase 2 persistence implementation. Save/load is a v0.1.0 requirement, not merely a design exercise. No format is declared safe by this proposal.

## 11. Proposed internal modules

```text
src/raceml/
  __init__.py
  core/{config,registry,protocols,errors}.py
  engine/executor.py
  input/{adapters,validation}.py
  models/{classifier,regressor}.py
  models/backends/{sklearn,lightgbm,xgboost}.py
  resources/{planner,monitor,report}.py
  evaluation/{metrics,validation}.py
  incremental/{protocols,updater}.py
  automl/{search,tuning}.py
  persistence/{manifest,storage}.py
  benchmarks/{runner,report}.py
  native/  # independent algorithms only in a later research milestone
```

This module map was reconciled in [ADR 0002](docs/decisions/0002-training-contracts.md) and merged in Phase 0A. It aligns input responsibilities with the existing `input/` package and places integrated adapters under `models/backends/`; `engine/` represents the training execution already described in the architecture. `evaluation/validation.py` concerns supplied validation data and metrics, never splitting. The map creates no new architecture layer and is not a requirement to create empty files in advance. Phase 0B anchored artifact ignore rules so they no longer hide `models/` source directories. Existing empty local placeholders remain untracked; this proposal adds no source files.

## 12. Design acceptance

Each public operation must have defined inputs, outputs, error behavior, capability checks and tests. Backend parity means consistent semantics where feasible, not identical underlying algorithms.

The [Phase 0 decision register](docs/PHASE_0_REPORT.md#remaining-technical-decisions) identifies unresolved details and the milestone before which each must be settled. An illustrative snippet does not close those decisions or demonstrate implementation.

## Canonical API and data ownership

`RaceMLClassifier` and `RaceMLRegressor` are the canonical public estimator names. Optional automation classes are `RaceMLAutoClassifier` and `RaceMLAutoRegressor`. Prepared `X` and `y` are passed directly to `fit`; RaceML never loads, cleans, imputes, or splits the dataset. Internal validation and conversions required by a selected backend are allowed and should be measurable.

```python
from raceml import RaceMLClassifier, RaceMLRegressor

classifier = RaceMLClassifier(algorithm="lightgbm", cpu_cores=4)
classifier.fit(X_train, y_train)
predictions = classifier.predict(X_test)

regressor = RaceMLRegressor(algorithm="xgboost", cpu_cores=4)
regressor.fit(X_train_reg, y_train_reg)
```

A future native algorithm can be selected through the same `algorithm` parameter, but no native identifier is finalized. This supersedes any older examples with generic `Classifier` or `Regressor` names.
