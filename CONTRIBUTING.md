# Contributing to RaceML

RaceML is in pre-development. Contributions should begin with a scoped issue or agreed design change.

## Workflow

1. Read `README.md`, `PRD.md`, `ARCHITECTURE.md`, `DESIGN.md`, and `AGENTS.md`.
2. Discuss changes to public APIs, dependencies or architecture before implementing them.
3. Create a focused branch and include tests with the change.
4. Document any performance claim using `BENCHMARKS.md`.
5. Submit a PR describing the problem, changes, verification, limitations and compatibility impact.

## Standards

Use clear Python typing, small modules, reproducible experiments and explicit errors. Avoid speculative complexity, hidden automatic behavior and unmeasured optimization claims.

## Licensing

The project license has not yet been selected. Confirm the license and dependency compatibility before accepting external code or publishing distributions.

## Scope

Contributions must respect `SCOPE.md`: no general data-loading or cleaning features. Public estimator names use `RaceMLClassifier` and `RaceMLRegressor`. Native algorithm proposals require a design and benchmark plan; see `NATIVE_ENGINE.md`.
