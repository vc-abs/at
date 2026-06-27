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
- Configuration parsing now standardizes all accepted inputs in `src/at/readWrite/readConfig.py` via a single `_standardizeConfig` helper applied to both the global config and each scenario's merged config:
  - compact DMS and decimal-degree coordinate parsing for `latitude`/`longitude`,
  - `startDate`/`startTime` aliases consumed into base `year`/`month`/`day`/`hour`/`minute`/`second`,
  - `endDate`/`endTime` window inputs that derive per-scenario `count` via both-inclusive `pd.date_range`,
  - legacy `frequency`/`periods` normalized to `interval`/`count`,
  - fixed-duration `interval` validation rejecting variable-calendar anchors,
  - downstream `generateScenarioCombos` in `src/at/tools/generateCombos.py` consumes only `count`+`interval`.
- Panchang implementation now also includes:
  - Gowri schedule runtime in `src/at/panchang/gowri.py`,
  - shared Gowri constants in `src/at/core/constants.py`,
  - `Panchang` accessors for Gowri schedule/current segment/current flags.
- Combo-generation implementation now also exposes:
  - compact `timeFlags`/`timeF` output from `src/at/tools/generateCombos.py`,
  - dedicated `planetQualities`/`*Q` output from `src/at/tools/generateCombos.py`,
  - dedicated ShadBala strength fields (`suS`, `moS`, `maS`, `meS`, `juS`, `veS`, `saS`, `totalS`, `avgIP`) selectable from `src/at/tools/generateCombos.py`,
  - dedicated Gowri fields/flags (`gowri`, `gowriScore`, `gowriM`, `gowriS`, `gowriT`, `gowriStart`, `gowriEnd`, `gowriF`) from `src/at/tools/generateCombos.py`,
  - root-level config `constants` support in `src/at/readWrite/getDefaultConfig.py` and merged runtime config loading,
  - combo-generation constant helpers in `src/at/tools/generateCombos.py` for:
    - wrapping constants in a shared attribute-access namespace,
    - rewriting author-facing `constants.foo` expressions to pandas-native external-variable access at evaluation time,
    - resolving constant-backed summary/list references before DataFrame summary operations,
  - marketing preset configuration in `presets/events/marketing.yml` (importing `presets/muhurta-base.yml`) with a `baseEventScore` plus simple additive Gowri/Shadbala adjustments built on existing output fields,
  - separate launch preset configuration in `presets/events/launch.yml` (importing the base) with the same additive Gowri/Shadbala adjustment pattern and companion launch review configs under `temp/`,
  - separate staff onboarding preset configuration in `presets/events/staffOnboarding.yml` (importing the base) with institutional-fit weighting and companion review export config under `temp/`,
  - separate student onboarding preset configuration in `presets/events/studentOnboarding.yml` (importing the base) with learning-support weighting and companion review export config under `temp/`,
  - a shared abstract muhurta base in `presets/muhurta-base.yml` that owns the common `sources`, the shared score-chain structure (coefficient-driven via `constants.event*`), the shared muhurta tithi lists (`preferredTithis`/`tithisToAvoid`/`waningRiktaTithis`/`waningPoornaTithis`), and the shared `report` keyed on `eventScore`; not standalone-runnable,
  - preset `imports:` directive resolution in `src/at/read_write/read_config.py` (`_load_with_imports`): paths resolve relative to the importing file's directory, imports merge depth-first left-to-right with the importing file's body on top (matching CLI stacking), cycle detection via a visited-path chain, and the `imports:` key stripped from the merged result; `defaultConfig.yml` is still prepended once at the bottom,
  - per-scenario constants & computations in `src/at/read_write/read_config.py` and `src/at/tools/generate_combos.py`: scenarios deep-merge onto a `copy.deepcopy(config)` per scenario via the same module-scope `Merger` used for file stacking (`merge_scenario_config`), so dicts merge and lists/scalars override; `_normalize_computations` is applied per merged scenario (and to the base config) so a scenario's top-level `constants` deep-merge with global `constants` before being folded into `computations.constants`; `build_scenarios` runs on the pre-normalization config so scenario-level `constants` compose with global `constants`; `generate_scenario_combos` returns `(df, merged_config)` and `generate_combos` runs `add_custom_columns` **per scenario** with that scenario's merged config, so per-scenario constant/computation overrides take effect at evaluation time; `report` (selection / order / fieldSets) stays global and is applied once to the combined DataFrame; the column-union edge case (scenarios with different computed field names → NaN on concat) is documented in `docs/presets-cheatsheet.md` §11 rather than engine-guarded,
  - hourly review/verification artefacts under `temp/`, including `review-week-hourly.yml`, `marketing-review-week-export.yml`, `launch-review-week-export.yml`, `staff-onboarding-review-week-export.yml`, `student-onboarding-review-week-export.yml`, and their generated TSV outputs.

## Validation Surface

- Test suite present under `tests/` with multiple domain-focused modules.
- `tests/core/test_planet_quality.py` now covers BPHS aspect metadata, Mercury influence evaluation paths, and Moon tithi-based quality behavior.
- `tests/panchang/test_gowri.py` covers first-pass Gowri schedule lookup and day/night segment selection behavior.
- `tests/tools/test_generate_combos.py` now covers compact time-flag output, planet-quality output, Gowri output fields, field-set selection behavior, source-group pruning, and constant-backed selection/computation behavior for combo generation, including base/event preset-structure checks for `muhurta-base` and the `launch`, `staffOnboarding`, and `studentOnboarding` event files, plus the `eventScoreDev` groupby-transform regression test and per-scenario constant/computation acceptance tests against `tests/fixtures/per_scenario_constants.yml`.
- `tests/shad_bala/test_shadbala.py` now covers Dig Bala reference-longitude and linear falloff behavior.
- `tests/shad_bala/test_shadbala_integration.py` loads the `referenceEvent` scenario from `tests/fixtures/shadbala_scenario.yml` (stacked with `presets/debug.yml` and `presets/allFieldSets.yml`) so validation runs against a committed, version-controlled fixture.
- `tests/read_write/test_read_config.py` covers scenario deep-merging (including per-scenario `constants` folded into `computations.constants` and non-leaking overrides via `merge_scenario_config`), file merge behavior, default-config loading, DMS compact/decimal coordinate parsing, `startDate`/`startTime` alias equivalence, `endDate`/`endTime` count derivation (both-inclusive), legacy `frequency`/`periods` normalization, fixed-duration `interval` validation, partial-end-pair fail-fast behavior, and preset `imports:` resolution (single/chained/multi-import merge order, relative-path resolution, cycle rejection, key stripping, default-config precedence, and composition with `scenarios`).
- Coverage + lint workflow referenced in README via `./scripts/validate.sh`.
