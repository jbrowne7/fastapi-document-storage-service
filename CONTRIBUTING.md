# Contributing

## Branching
- Branches: `main` (production, protected), `dev` (integration, protected)
- Work from `dev` using short‑lived branches:
  - `feature/<short-name>` for features
  - `fix/<short-name>` for bug fixes
- Flow:
  - feature/fix → PR into `dev`
- Rebase `dev` often; keep PRs small.

## Commits
- Format: `<type>(optional scope): <summary>`
- Types: `feat`, `fix`
- Examples:
  - `feature(auth): add JWT login endpoint`
  - `fix(documents): handle empty PDF pages`

## Pull Requests
- Target `dev` for feature/fix PRs; target `main` only for release/hotfix PRs.
- Prefer “Squash and merge”. PR title becomes the commit on the base branch (use Conventional Commit style).
- Link issues in the description using `Fixes #123` or `Closes #123`.
- Keep PRs focused (≤ ~300 lines). Add tests and docs updates.
- Pass checks: lint/type/tests before requesting review.

## Issues
- Use templates:
  - Bug: expected vs actual, logs
  - Feature: problem, proposal
- Labels: `type:bug`, `type:feature`, `area:api|auth|ingestion|vector|qa`

## Releases
- Semantic Versioning: `MAJOR.MINOR.PATCH`
- Tag releases (e.g., `v0.1.0`) and generate notes from merged PRs.

## Code style
- Python 3.11+, FastAPI, Pydantic v2
- Tests: pytest
