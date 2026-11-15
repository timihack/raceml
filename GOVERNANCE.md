# RaceML Governance

## Project ownership and scope

RaceML is an open-source project licensed under Apache-2.0. Its purpose is high-performance machine learning training through integrated backends and independently developed native algorithms. Dataset cleaning, general-purpose loading, and feature engineering are outside the core scope.

## Roles

**Contributors** submit issues, documentation, tests, benchmarks, and code. **Reviewers** provide technical feedback. **Maintainers** triage issues, review and merge pull requests, manage releases, and enforce project policies. The **project lead** coordinates the roadmap and resolves decisions when consensus is not reached. Initial maintainers and the project lead are to be identified in the repository; no appointments are implied by this document.

## Decision-making

1. Small changes are discussed in their issue or pull request.
2. Changes to public APIs, dependencies, architecture, performance methodology, or licensing require an issue or architecture decision record (ADR) before implementation.
3. Maintainers seek consensus, documenting trade-offs and objections.
4. If consensus cannot be reached, the project lead makes a documented decision, subject to the project's licence and contributor rights.
5. Changes that materially alter the project's direction require public discussion before merging.

## Contributions and reviews

- Open an issue before large features or breaking API changes.
- Pull requests require passing relevant tests and at least one maintainer review when a reviewer is available.
- Authors should not self-approve changes where independent review is possible.
- Benchmarks must include hardware, datasets, versions, seeds, comparison conditions, and raw measurements.
- Claims of faster training or lower memory use must be supported by reproducible evidence.
- Dependencies must be checked for compatible licences and maintenance status.

## Maintainer access

Maintainers earn access through sustained contributions, sound review judgment, and adherence to project policies. New maintainers are nominated by an existing maintainer and approved by the project lead after discussion. Access is least-privilege and may be revoked for inactivity, security risk, or misconduct after review.

## Releases

Maintainers manage versioning, release notes, compatibility checks, and publishing. Breaking changes require migration notes. No release should be published without tests and an approved release checklist. Package publication credentials should use trusted publishing or short-lived credentials where supported.

## Security and conduct

Security vulnerabilities should follow `SECURITY.md`; conduct concerns follow `CODE_OF_CONDUCT.md`. Sensitive reports should not be handled through public issues.

## Amendments

Governance changes require a public proposal and a documented maintainer decision. This document is effective when adopted in the repository.
