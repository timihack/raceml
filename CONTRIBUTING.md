# Contributing to RaceML

Thank you for your interest in contributing to RaceML.

RaceML is an open-source, resource-aware machine learning project licensed under Apache License 2.0. The project is currently in pre-development.

We welcome bug reports, documentation improvements, tests, benchmark proposals, and code contributions.

## Before contributing

Read the following documents:

- `README.md`
- `PRD.md`
- `ARCHITECTURE.md`
- `DESIGN.md`
- `SCOPE.md`
- `NATIVE_ENGINE.md`
- `AGENTS.md`
- `CODE_OF_CONDUCT.md`

For performance or native algorithm changes, also read `BENCHMARKS.md`. Read `TESTING.md` for verification and `ROADMAP.md` for milestone scope. The [Phase 0 report](docs/PHASE_0_REPORT.md) lists unresolved decisions and review gates.

Discuss major API changes, dependencies, and architecture proposals through a GitHub issue before implementing them.

Phase 0A reconciles specifications only. Phase 0B setup changes and implementation must wait for Phase 0A review and approval. Preserve the v0.1.0 AutoML and incremental-learning requirements; optional AutoML means users opt in, not that its delivery is deferred.

## Contribution workflow

External contributors should use the **Fork → Branch → Pull Request** workflow.

Maintainers with repository access may use a feature branch in the upstream repository and open a pull request against `main`. Keep unrelated work on separate branches. Automated agents must follow `AGENTS.md` authorization requirements for pushes, merges and publication; fork synchronization examples below do not authorize an agent to push to `main`.

### 1. Fork the repository

Visit https://github.com/timihack/raceml and click **Fork**.

This creates a copy of RaceML under your GitHub account.

### 2. Clone your fork

```bash
git clone git@github.com:YOUR_USERNAME/raceml.git
cd raceml
```

Add the official repository as an upstream remote:

```bash
git remote add upstream https://github.com/timihack/raceml.git
git remote -v
```

### 3. Set up the development environment

Install `uv` if it is not already installed.

```bash
uv python install 3.12
uv sync
```

Run the existing tests:

```bash
uv run pytest
```

### 4. Synchronize your fork

Before starting a contribution:

```bash
git fetch upstream
git switch main
git merge --ff-only upstream/main
git push origin main
```

If your fork's `main` has diverged, resolve that separately rather than forcing an update without reviewing the differences.

### 5. Create a feature branch

Create a branch from the updated `main`:

```bash
git switch -c feat/your-feature-name
```

Suggested prefixes:

- `feat/` — New functionality
- `fix/` — Bug fixes
- `docs/` — Documentation
- `test/` — Tests
- `perf/` — Performance improvements
- `refactor/` — Internal code changes without intended behaviour changes

Keep each branch focused on one issue or related change.

### 6. Make your changes

Follow the existing project architecture and coding conventions.

RaceML does not provide a general-purpose data-loading, cleaning, or feature-engineering subsystem.

Public estimator classes use the names `RaceMLClassifier` and `RaceMLRegressor`.

Native algorithm contributions must include a technical explanation, correctness tests, and an appropriate benchmark plan.

Do not make performance claims without measurements.

### 7. Run checks

Before submitting a pull request:

```bash
uv run ruff check .
uv run ruff format --check src/ tests/
uv run mypy src/raceml
uv run pytest
```

Include tests for changes to executable code.

### 8. Commit and push

```bash
git add .
git commit -m "feat: describe your contribution"
git push -u origin feat/your-feature-name
```

### 9. Open a pull request

Open:

https://github.com/timihack/raceml/compare

Select:

- Base repository: `timihack/raceml`
- Base branch: `main`
- Head repository: `YOUR_USERNAME/raceml`
- Compare branch: `feat/your-feature-name`

Complete the pull-request template.

Explain the problem, the changes made, how you tested them, and any compatibility or performance implications.

Link the relevant issue when applicable.

### 10. Review and merge

Maintainers will review the pull request.

Contributors may be asked to revise code, add tests, or update documentation.

Pull requests must pass required CI checks and satisfy repository rules before merging.

Maintainers decide whether and when to merge contributions.

Contributors should not push directly to the upstream `main` branch.

## Coding standards

Use clear Python type annotations, focused modules, explicit errors, and reproducible tests.

Avoid unnecessary dependencies and changes outside the approved scope.

Keep model training behaviour predictable. Optional automation must not unexpectedly override user-selected algorithms or parameters.

## Performance contributions

Performance improvements must follow `BENCHMARKS.md`.

Include the benchmark environment, dataset characteristics, baseline, measured results, and reproducible commands.

Report training time and memory consumption separately. Do not describe an optimization as faster or more memory-efficient without supporting results.

## Security

Do not publish security vulnerabilities in public issues.

Follow `SECURITY.md` for private reporting instructions.

## Licensing

RaceML is licensed under the **Apache License, Version 2.0**.

By submitting a contribution, you agree that your contribution is licensed under Apache 2.0 as part of RaceML.

Contributors must have the right to submit their code and must preserve required copyright, licence, and attribution notices.

Third-party code must have a compatible licence and must not be copied into RaceML without appropriate review.

## Code of Conduct

All contributors must follow `CODE_OF_CONDUCT.md`.

Community conduct concerns can be reported privately to:

**timihack.it@gmail.com**

## Questions

For development questions, open a GitHub issue or use an available repository discussion channel.

For security concerns, use the private reporting procedure described in `SECURITY.md`.
