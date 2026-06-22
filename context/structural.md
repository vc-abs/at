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
- Panchang implementation now also includes:
  - Gowri schedule runtime in `src/at/panchang/gowri.py`,
  - shared Gowri constants in `src/at/core/constants.py`,
  - `Panchang` accessors for Gowri schedule/current segment/current flags.
- Combo-generation implementation now also exposes:
  - compact `timeFlags`/`timeF` output from `src/at/tools/generateCombos.py`,
  - dedicated `planetQualities`/`*Q` output from `src/at/tools/generateCombos.py`,
  - dedicated ShadBala strength fields (`suS`, `moS`, `maS`, `meS`, `juS`, `veS`, `saS`, `totalS`, `avgIP`) selectable from `src/at/tools/generateCombos.py`,
  - dedicated Gowri fields/flags (`gowri`, `gowriScore`, `gowriM`, `gowriS`, `gowriT`, `gowriStart`, `gowriEnd`, `gowriF`) from `src/at/tools/generateCombos.py`,
  - marketing preset configuration in `presets/marketing.yml` with a `baseMarketingScore` plus simple additive Gowri/Shadbala adjustments built on existing output fields,
  - separate launch preset configuration in `presets/launch.yml` with its own `baseLaunchScore`, the same additive Gowri/Shadbala adjustment pattern, and companion launch review configs under `temp/`,
  - hourly review/verification artefacts under `temp/`, including `review-week-hourly.yml`, `marketing-review-week-export.yml`, `launch-review-week-export.yml`, and their generated TSV outputs.

## Validation Surface

- Test suite present under `tests/` with multiple domain-focused modules.
- `tests/core/test_planet_quality.py` now covers BPHS aspect metadata, Mercury influence evaluation paths, and Moon tithi-based quality behavior.
- `tests/panchang/test_gowri.py` covers first-pass Gowri schedule lookup and day/night segment selection behavior.
- `tests/tools/test_generate_combos.py` now covers compact time-flag output, planet-quality output, Gowri output fields, and field-set selection behavior for combo generation.
- `tests/shadbala/test_shadbala.py` now covers Dig Bala reference-longitude and linear falloff behavior.
- Coverage + lint workflow referenced in README via `./scripts/validate.sh`.
