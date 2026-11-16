# RaceML Detailed Design

**Status:** Reconciled interface proposal for Phase 0A review; code samples are illustrative and not implemented. Established scope and naming are preserved; contract clarifications below require review before implementation.

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

The proposed public `fit(X, y, ...)` returns the fitted estimator (`self`). Training configuration and metadata remain associated with that estimator; `resource_report()` returns a separate report. This resolves the earlier ambiguity about returning a model/report tuple without adding another public method. Exact fitted attributes, refit behavior, signatures and return types must be finalized before Phase 1 coding.

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

## 4. Configuration

- Task: classification or regression.
- Algorithm: explicit registered backend identifier.
- Seed: optional reproducibility setting.
- `cpu_cores`: positive integer within supported constraints.
- `memory_limit`: human-readable budget; monitoring only in initial version.
- Backend parameters: namespaced or validated against backend constructor.
- Validation: explicit user-prepared validation data, with no internal splitting and no held-out test data used for selection.

The parameter namespace, seed defaults, algorithm identifiers and the initial scikit-learn estimator list remain decisions. The Phase 0A recommendation is to reject conflicting RaceML/backend thread settings rather than silently select precedence; its exact validation rules must be approved before implementation.

## 5. Input validation and conversion

`DataAdapter` checks shape, target length, column schema, dtype compatibility and missing-value handling. It reports whether a conversion occurred. Never silently drop or reorder features. Record feature names and order for prediction-time validation.

The existing illustrative `DataAdapter` name denotes an internal input adapter only. It provides no loading, cleaning, imputation, encoding, feature engineering or splitting API. Algorithm-native handling may be passed through only when supported and documented. Sparse layouts, target types, categorical/missing-value compatibility and named-versus-positional input checks require explicit compatibility decisions before their implementations.

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
- `ResourceBudgetExceededError` (only when an enforceable mechanism exists)
- `UnsafeModelLoadError`

The complete inheritance tree and pre-fit failure type remain to be finalized before their operations are implemented. The enforceable-budget error is reserved for a future enforcement mechanism and must not imply one exists initially.

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

This reconciled module map is proposed for review in [ADR 0002](docs/decisions/0002-training-contracts.md). It aligns input responsibilities with the existing `input/` package and places integrated adapters under `models/backends/`; `engine/` represents the training execution already described in the architecture. `evaluation/validation.py` concerns supplied validation data and metrics, never splitting. The map creates no new architecture layer and is not a requirement to create empty files in advance. The repository's unanchored artifact ignore rules currently hide `models/` source directories; correcting those rules belongs to Phase 0B after approval.

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
