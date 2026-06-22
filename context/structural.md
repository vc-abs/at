# Structural Context

## Table of Contents

- [Repository Layout](#repository-layout)
- [Implementation Surface](#implementation-surface)
- [Validation Surface](#validation-surface)

## Repository Layout

- `src/at/` contains the package implementation.
- `tests/` contains test modules grouped by domain (`core`, `dasha`, `panchang`, `readwrite`, `tools`).
- Root-level scripts include setup and validation helpers.

## Implementation Surface

- Package entrypoint script: `at = at.main:cli` (from `pyproject.toml`).
- Main implementation files currently visible:
  - `src/at/main.py`
  - `src/at/__init__.py`

## Validation Surface

- Test suite present under `tests/` with multiple domain-focused modules.
- `tests/core/test_planet_quality.py` now covers BPHS aspect metadata, Mercury influence evaluation paths, and Moon tithi-based quality behavior.
- Coverage + lint workflow referenced in README via `./scripts/validate.sh`.
