# Notes

## Table of Contents

- [Initialization Notes](#initialization-notes)
- [Cycle Notes](#cycle-notes)

## Initialization Notes

- Deliberate-dev structure initialized from existing repository state.
- README ToDo list migrated into `backlog.md`.

## Cycle Notes

- Finalized Mercury quality BPHS cycle after implementation had already been committed.
- Corrected BPHS graha drishti metadata used by Mercury evaluation.
- Mercury conditional quality now considers conjunction and BPHS aspect influence with overlap deduplication.
- Finalized Moon quality cycle using a BPHS-oriented graded tithi score after direct execution-context entry by explicit user override.
- Moon conditional quality now derives from tithi ranges and a graded internal score while preserving the existing caller-facing quality labels.
- Finalized a bounded ShadBala Dig Bala audit cycle with explicit BPHS-oriented directional-reference handling and mapped tests.
- Finalized a broader ShadBala implementation and BPHS audit pass with first-pass implementations/revisions for Dig Bala, Ayana Bala, Drik Bala, Yuddha Bala, and Abda/Maasa reviewability.
- Added compact combo-generation time flags for Rahu Kalam, Yamaganda, and Gulika, plus dedicated planet-quality output columns for queryable preset logic.
- Added and iteratively calibrated a first-pass marketing preset with YAML-first weighted scoring, bounded dasha awareness, house-score scaling, and reduced-column TSV exports for review.
- During the broader ShadBala comparison pass, JA evidence suggested a narrower or conjunction-dominant Mercury classification rule for Paksha Bala than the current BPHS-oriented implementation uses.
- Remaining ShadBala alignment gaps were deferred to backlog for a future refinement cycle rather than addressed through speculative rule changes.
- Added first-pass Gowri Panchangam runtime support using sunrise/sunset-derived 8-part day/night segmentation, an algorithmic weekday-cycle model, and queryable combo-output fields.
- Kept provenance/verification concerns out of runtime artefacts and deferred them to backlog follow-up.
- Finalized the Gowri first-pass cycle with point-in-time-first lookup, numeric `gowriScore`, shared constants, and documented query/runtime conventions.
- Refreshed the marketing preset to derive its final score from a base score plus simple additive Gowri and special-planet Shadbala adjustments calibrated from observed review ranges.
- Updated the `launch` preset to use the same additive Gowri/Shadbala adjustment structure on top of its own base score, and added hourly review/verification TSV artefacts under `temp/`.
- Finalized root-level config constants support for presets and config-driven expressions.
- Added author-facing `constants.foo` access for `query` and string-valued `customColumns`, with evaluation-boundary rewriting to pandas-native external-variable access.
- Added constant-backed summary/list reference support for custom columns such as `min: constants.marketingMinHouses`.
- Refactored `presets/marketing.yml` to centralize repeated lists/filters under a root `constants` section.
- Further refined the preset pattern so weekday preferences can be expressed as reusable weight maps (for example `marketingWeekdayWeights`) and consumed through `vaara.map(constants.<weights>).fillna(0)`.
- Renamed the marketing dasha allow-list to `marketingCorePlanets` and aligned `presets/launch.yml` to the same constants-driven structure with `launchWeekdayWeights`, `launchCorePlanets`, and related shared lists.
- Documented config constants usage in `README.md` and `docs/guide.md`, including the weighted-weekday pattern.
- Simplified `qualityScore` in both presets so it only scores dynamically varying `Q` values (`Mercury`, `Moon`) and no longer includes constant or impossible branches for fixed-nature planets.
- Rebalanced launch filtering after that cleanup by removing the hard `moQ != 'malefic'` gate and recalibrating the score threshold, so launch still yields review candidates without relying on impossible/constant quality branches.
- Added `presets/staffOnboarding.yml` as a distinct institutional-joining preset using the same constants-driven YAML scoring pattern as marketing/launch, with 10th/11th/1st-led house weighting and Saturn-inclusive institutional support signals.
- Added `presets/studentOnboarding.yml` as a distinct course-entry preset using the same constants-driven YAML scoring pattern, with 4th/5th/9th-led learning weighting and education-specific weekday/nakshatra preferences.
- Added companion review export configs under `temp/` for the staff and student onboarding presets.
- Updated `tests/tools/test_generate_combos.py` to assert that both new presets follow the constants-driven preset pattern.
- Updated `tests/shadbala/test_shadbala_integration.py` to use the retained archived VC preset fixture path that matches the repository's current preset layout.
- Validated the cycle with targeted tests, full `./scripts/validate.sh`, and CLI smoke runs of the constant-backed marketing, launch, staff onboarding, and student onboarding presets.
- Finalized the configuration and input model cycle: introduced `count`+`interval` as the canonical sampling keys (legacy `frequency`/`periods` normalized at parse time), `startDate`/`startTime` aliases for base date/time inputs, `endDate`/`endTime` window inputs that derive `count` via both-inclusive ranges, compact DMS coordinate parsing, and fixed-duration `interval` validation.
- Unified config standardization into a single `_standardizeConfig` helper applied to both the global config and each scenario's merged config, eliminating the `endDatetime` internal variable and per-scenario special-case branching.
- Migrated `data/defaultConfig.yml`, `examples/`, and all `presets/` to the `count`+`interval` schema.
- Extended `tests/readwrite/test_read_config.py` with DMS, sampling, alias, and validation assertions; consolidated all `readConfig` assertions into the existing test module per the one-to-one module-to-test mapping.
