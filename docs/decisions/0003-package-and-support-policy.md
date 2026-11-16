# ADR 0003 — Core dependencies, optional extras and initial setup verification

**Status:** Accepted dependency/support policy; Phase 0B changes pending review

**Date:** 2026-11-16

## Context and authorization

Phase 0A was merged in PR #2. The user authorized the next milestone and explicitly approved D01: NumPy as the only core dependency, scikit-learn moved to a `sklearn` extra, optional `pandas`, `polars` and `arrow` extras, and Ubuntu/Python 3.12 as the initial verification baseline. Other combinations remain unverified. The user retains responsibility for commits and pushes.

The package currently declares Python >=3.12; this is an installation constraint, not a tested support matrix. No backend or input conversion is implemented yet. Packaging an extra does not establish that its adapter works.

## Decision

- Retain `numpy>=1.26` as the only core runtime dependency. Move the existing `scikit-learn>=1.5` requirement to `raceml[sklearn]`.
- Add `raceml[pandas]` (`pandas>=2.2`), `raceml[polars]` (`polars>=1.0`) and `raceml[arrow]` (`pyarrow>=16.0`) for explicit installation of planned input dependencies. These bounds are dependency declarations, not verified minimum-version support claims.
- Preserve existing backend and `automl` extras; include all declared optional dependencies in `all`. AutoML remains optional for users and required for v0.1.0 delivery. Existing CatBoost packaging does not move its adapter into v0.1.0 scope.
- Keep Python >=3.12 metadata and the existing Ubuntu/Python 3.12 CI baseline. Add lock consistency, source/wheel builds, artifact metadata/license checks and isolated installation/import checks. Add no estimator or conversion code in Phase 0B.
- Explicitly include `LICENSE` and `NOTICE` in distributions through `license-files`; require Hatchling >=1.27 for its default core metadata 2.4 behavior. See [Hatch metadata](https://hatch.pypa.io/latest/config/metadata/#license) and [Hatchling history](https://hatch.pypa.io/latest/history/hatchling/#1270-2024-11-26).
- Anchor root dataset/artifact ignore rules so they cannot hide `src/raceml/models/` or other package source. Preserve existing local source placeholders rather than deleting or committing them automatically.

## Verification boundaries

Normal tests exercise ignore rules without network access. Opt-in packaging tests consume artifacts from `RACEML_DIST_DIR`, inspect wheel/sdist metadata and notices, and install each artifact with its base dependencies into a separate clean environment. A Python process in isolated mode verifies the import comes from that environment, NumPy is available, and optional libraries/tuners are absent and not imported. Both clean installs are development/CI operations; importing RaceML does not initiate network access.

The artifact checks run automatically in CI after `uv build --no-sources`, following [uv's package-building guidance](https://docs.astral.sh/uv/guides/package/). Lock validation uses `uv sync --locked`, which is documented in [uv's GitHub Actions guidance](https://docs.astral.sh/uv/guides/integration/github/). Builds, clean installation and local tests establish scaffold packaging only, not model/backend compatibility. Hosted CI evidence must come from the review PR.

## Dependency license review

No third-party code or binary is vendored into RaceML. New optional declarations refer to separately installed packages. Reviewed upstream project licenses: [pandas BSD-3-Clause](https://pandas.pydata.org/docs/getting_started/overview.html#license), [Polars MIT](https://github.com/pola-rs/polars/blob/main/LICENSE), and [Apache Arrow Apache-2.0 with third-party notices](https://github.com/apache/arrow/blob/main/LICENSE.txt). Existing installed scikit-learn metadata identifies BSD-3-Clause; moving that requirement does not introduce a new package. A full resolved dependency/artifact license review remains a release gate; this review does not authorize bundling their binaries or removing their notices.

## Consequences and remaining decisions

Base installation becomes smaller and allows missing-backend/manual-mode isolation tests. Users wanting scikit-learn must explicitly install `raceml[sklearn]`; no released RaceML API is being migrated. Table extras install dependencies without promising working conversion paths before their milestones.

Only the initial packaging baseline is selected. Exact backend/input compatibility, minimum-version tests, additional Python/OS support, complete fit-option forwarding and estimator contracts, persistence, budgets and benchmarks remain the technical gates recorded in the Phase 0 report. No performance improvement is claimed.
