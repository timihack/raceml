# RaceML Benchmark Protocol

**Status:** Proposed methodology. No results have been measured.

## 1. Research questions

- Does RaceML reduce end-to-end wall time for matched model workflows?
- Does it reduce peak process-tree resident memory?
- What overhead does RaceML add to direct-backend training?
- Does resource-aware AutoML reach target predictive quality with fewer CPU-hours?
- Do incremental updates outperform full retraining on suitable workloads without unacceptable quality loss?

## 2. Baselines

Direct scikit-learn, LightGBM and XGBoost workflows using identically prepared inputs, data splits, backend versions, hyperparameters, thread counts and random seeds. AutoML comparisons against defined Optuna and AutoGluon workflows in a separate experiment class.

## 3. Dataset matrix

Choose openly licensed, version-pinned datasets representing: small numeric classification; medium mixed categorical classification; regression; sparse high-dimensional features; missing-value-heavy data; larger-than-memory input when a backend genuinely supports out-of-core processing. Record URLs, licenses, checksums, shapes and preprocessing steps before experiments. Do not claim datasets were tested until they are downloaded and run.

## 4. Hardware and environment

Record CPU model, physical/logical cores, RAM, OS/kernel, Python, package versions, power mode, CPU affinity, BLAS/OpenMP settings, storage type and thermal conditions. Keep conditions comparable. Run with a fixed CPU limit and memory budget where supported.

## 5. Metrics

- End-to-end wall-clock duration: from prepared input handoff through fitted model, with phases also reported.
- Native fit duration separately.
- Peak process-tree RSS; specify sampling interval and measurement limitations.
- Prediction latency and throughput after warm-up.
- Classification: accuracy, F1, ROC-AUC where valid; regression: RMSE and MAE.
- CPU-hours and search time to reach a predefined validation score for AutoML.
- Update duration and held-out performance after each incremental batch.

## 6. Fairness controls

Use identical splits and test sets; prevent leakage; keep equivalent model hyperparameters and preprocessing; avoid nested oversubscription; isolate runs; randomize execution order; use warm-up runs where appropriate. Do not compare a tuned model to an untuned baseline as if algorithm speed alone caused the difference.

## 7. Repetition and statistics

At least five measured repetitions for initial comparisons when practical; report median, dispersion, raw run data and uncertainty. Do not conceal regressions. Predeclare exclusions and explain any failed runs.

## 8. Proposed targets, not claims

- 20% lower end-to-end training time on a predeclared subset of workloads.
- 30% lower peak memory on a predeclared subset.
- Comparable held-out quality within task-specific tolerances declared before testing.

Define exactly which workloads qualify before announcing success. Report aggregate and per-workload outcomes.

## 9. Report schema

Each run: dataset ID/checksum, split ID, baseline or RaceML, algorithm, parameters, seed, environment, threads, timing phases, peak RSS, quality metrics, status, errors and measurement method. Save machine-readable JSON/CSV plus a human-readable summary.

## 10. Benchmark governance

Do not invent benchmark numbers or label targets as achieved. Commit scripts and configurations. Any published speedup must state its denominator, dataset, hardware and measurement scope.

## Training-only benchmark boundary

Benchmark timers start at the handoff of **already-prepared** `X` and `y`, not at CSV/Parquet loading or user cleaning. Record input conversion time separately from model fit time. Compare identical prepared inputs, algorithm settings, thread limits and seeds. Report integrated-backend overhead separately from native RaceML algorithm performance. The 20% training-time and 30% peak-memory reductions are hypotheses, not results.
