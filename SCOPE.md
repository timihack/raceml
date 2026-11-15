# RaceML Scope and Boundaries

**Status:** Proposed specification; not implemented.

RaceML is a training-focused, CPU-first machine learning library. Users own data ingestion, cleaning, feature engineering, encoding choices, and dataset splitting. RaceML accepts already-prepared feature arrays/tables and labels.

## In scope

- Validate dimensions, dtypes, target compatibility and backend capabilities without altering the semantic meaning of features.
- Convert prepared input to backend-required representations, profiling and avoiding copies where possible.
- Train, predict, monitor CPU/memory use and report performance.
- Integrate established backends and, over time, independently implemented native RaceML algorithms.
- Offer optional model selection and tuning, plus incremental updates only for models that genuinely support them.

## Out of scope

- File loading (CSV, Parquet, Excel), cleaning, imputation pipelines, feature engineering, dataset splitting, and user-facing transformations.
- Silent encoding, imputation, feature selection or automatic data leakage prevention.
- Promising a hard RAM limit in the initial in-process execution mode.

Algorithm-native missing-value handling, binning or categorical handling are allowed when explicitly documented and supported by the selected model; these are training algorithm behaviors, not a general cleaning API.

## Public naming convention

The public estimator classes are `RaceMLClassifier` and `RaceMLRegressor`; optional automation classes are `RaceMLAutoClassifier` and `RaceMLAutoRegressor`. The import namespace is `raceml`. Do not introduce `Classifier`, `Regressor`, `AutoClassifier`, or `AutoRegressor` as competing canonical names.
