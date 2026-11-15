# RaceML

**Resource-Aware Compute Engine for Machine Learning**

**Faster training. Less memory. One interface.**

RaceML is a proposed open-source, CPU-first machine learning library offering a common Python interface for model training, evaluation, resource-aware execution, optional automated model selection, and incremental updates for supported estimators.

> **Status:** Pre-development. The project has no released implementation. Targets of 20% less end-to-end training time and 30% less peak memory on selected workloads are research targets, not measured results.

Planned import:

```python
import raceml
```

## Principles

- General-purpose ML library, initially focused on tabular classification and regression.
- Python-first. Introduce Rust only after profiling demonstrates a need.
- Integrate established model engines rather than reimplementing them initially.
- Manual configuration by default; AutoML is an optional, separately installable feature.
- Report performance using fair, reproducible experiments.
- Never imply that a wrapper makes the underlying model algorithm faster.

## Planned integrations

Initial: scikit-learn, LightGBM, XGBoost. Later: CatBoost, additional online estimators, optional native kernels and GPU capabilities.

## Documentation

- [PRD](PRD.md): product requirements and acceptance criteria
- [Architecture](ARCHITECTURE.md): subsystems and boundaries
- [Design](DESIGN.md): APIs and component contracts
- [Benchmarks](BENCHMARKS.md): measurement protocol
- [Roadmap](ROADMAP.md): delivery stages
- [Agents](AGENTS.md): instructions for coding agents
- [Testing](TESTING.md): quality gates
- [Contributing](CONTRIBUTING.md): development workflow
- [Security](SECURITY.md): security expectations
- [Decisions](docs/decisions/0001-python-first.md): architecture decision record

## Development status

No production code or validated performance results exist yet. Examples in design documents are proposals and must not be described as working features.

## Training-only scope and dual-engine direction

RaceML accepts user-prepared data. Users retain control over loading, cleaning, feature engineering and splitting; RaceML handles model training and execution. The roadmap includes both established integrated model backends and independently developed native algorithms.

Planned public API:

```python
from raceml import RaceMLClassifier, RaceMLRegressor

model = RaceMLClassifier(algorithm="lightgbm", cpu_cores=4)
model.fit(X_train, y_train)
predictions = model.predict(X_test)
```

See [Scope](SCOPE.md) and [Native Engine](NATIVE_ENGINE.md).
