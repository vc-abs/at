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
- Combo-generation implementation now also exposes:
  - compact `timeFlags`/`timeF` output from `src/at/tools/generateCombos.py`,
  - dedicated `planetQualities`/`*Q` output from `src/at/tools/generateCombos.py`,
  - marketing preset configuration in `presets/marketing.yml` with weighted scoring built on existing output fields.

## Validation Surface

- Test suite present under `tests/` with multiple domain-focused modules.
- `tests/core/test_planet_quality.py` now covers BPHS aspect metadata, Mercury influence evaluation paths, and Moon tithi-based quality behavior.
- `tests/tools/test_generate_combos.py` now covers compact time-flag output, planet-quality output, and field-set selection behavior for combo generation.
- `tests/shadbala/test_shadbala.py` now covers Dig Bala reference-longitude and linear falloff behavior.
- Coverage + lint workflow referenced in README via `./scripts/validate.sh`.
