# RaceML Detailed Design

**Status:** Draft interface specification; code samples are illustrative and not implemented.

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

## 2. Optional automation

```python
from raceml.automl import RaceMLAutoClassifier

search = RaceMLAutoClassifier(time_limit=300, cpu_cores=4, metric="roc_auc")
search.fit(X_train, y_train, validation_data=(X_valid, y_valid))
```

AutoML must not run unless explicitly requested. It must avoid using held-out test data for selection.

## 3. Core contracts

```python
from typing import Protocol, Any


class ModelAdapter(Protocol):
    def fit(self, X: Any, y: Any, **kwargs: Any) -> None: ...
    def predict(self, X: Any) -> Any: ...
    def get_params(self) -> dict[str, Any]: ...
    def capabilities(self) -> dict[str, bool]: ...
```

Actual typing and return contracts will be finalized during implementation. `partial_fit` must not appear as universally supported in the base protocol; expose it via an optional capability or a separate protocol.

## 4. Configuration

- Task: classification or regression.
- Algorithm: explicit registered backend identifier.
- Seed: optional reproducibility setting.
- `cpu_cores`: positive integer within supported constraints.
- `memory_limit`: human-readable budget; monitoring only in initial version.
- Backend parameters: namespaced or validated against backend constructor.
- Validation: user-provided split or explicit strategy, with no test leakage.

## 5. Data subsystem

`DataAdapter` checks shape, target length, column schema, dtype compatibility and missing-value handling. It reports whether a conversion occurred. Never silently drop or reorder features. Record feature names and order for prediction-time validation.

## 6. Model subsystem

`Registry` resolves backend by task and declared capabilities. `RaceMLClassifier` and `RaceMLRegressor` delegate to adapters. Fit results include model reference, configuration and training metadata. Probability prediction is supported only for applicable models.

## 7. Resource subsystem

`ResourcePlan` holds requested thread count, memory budget and optional time budget. `ResourceReport` records observed wall time, CPU and peak RSS, measurement method and limitations. Resource planning must not silently override user algorithm settings.

## 8. Incremental subsystem

Three separate capabilities: `online_update`, `warm_start`, `full_retrain`. An `update(X, y)` call is permitted only for an adapter declaring `online_update`. Otherwise raise `UnsupportedUpdateError` with alternatives. No silent retraining.

## 9. Error taxonomy

- `BackendUnavailableError`
- `UnsupportedCapabilityError`
- `InvalidConfigurationError`
- `DataSchemaError`
- `ResourceBudgetExceededError` (only when an enforceable mechanism exists)
- `UnsafeModelLoadError`

## 10. Persistence

Persist backend type/version, model artifact, feature schema, task and reproducibility metadata. Serialization format is backend-dependent and must be documented. Untrusted pickle-based loading is not enabled by default.

## 11. Proposed internal modules

```text
src/raceml/
  __init__.py
  core/{config,registry,protocols,errors}.py
  data/{adapters,validation}.py
  models/{classifier,regressor}.py
  backends/{sklearn,lightgbm,xgboost}.py
  resources/{planner,monitor,report}.py
  evaluation/{metrics,validation}.py
  incremental/{protocols,updater}.py
  automl/{search,tuning}.py
  persistence/{manifest,storage}.py
  benchmarks/{runner,report}.py
```

This is a design proposal, not a requirement to create empty files in advance.

## 12. Design acceptance

Each public operation must have defined inputs, outputs, error behavior, capability checks and tests. Backend parity means consistent semantics where feasible, not identical underlying algorithms.

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
