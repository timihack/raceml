# RaceML Security Policy

**Status:** Pre-development; no released version or established private vulnerability reporting channel.

## Security considerations

- Treat serialized models as untrusted inputs; pickle/joblib can execute code during deserialization.
- Do not load untrusted artifacts by default.
- Do not log credentials, tokens, private rows or raw datasets by default.
- Keep third-party dependencies current and review their licenses.
- Model and dataset metadata may be sensitive; minimize what is stored.
- Resource limits in an in-process Python runner are not security isolation.
- Do not execute arbitrary user-provided code as part of automated tuning without explicit trust boundaries.

## Reporting

Until a dedicated security contact or GitHub private vulnerability reporting is configured, do not publish sensitive exploit details in public issues. Project maintainers should configure a private reporting channel before the first release.

## Input and model boundaries

RaceML consumes prepared user inputs, not arbitrary user-specified data files. Validate input dimensions and sizes; avoid unsafe model deserialization and document trust boundaries for integrated and future native backends.
