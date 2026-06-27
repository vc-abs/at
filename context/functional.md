# Functional Context

## Table of Contents

- [Current Behavior Summary](#current-behavior-summary)
- [Observed Functional Areas](#observed-functional-areas)
- [Known Functional Gaps](#known-functional-gaps)

## Current Behavior Summary

The project provides a CLI-oriented auspicious-time (muhurta) analysis workflow driven by YAML configuration and optional presets.

Current implemented rule highlights:
- Mercury's conditional quality evaluates BPHS-aligned planetary influence using both conjunctions and graha drishti.
- Overlapping Mercury contributors are deduplicated, and balanced influence resolves to neutral.
- Moon quality uses a BPHS-oriented graded tithi score internally while preserving the existing benefic/malefic quality contract for callers.
- ShadBala directional strength exposes its directional-reference longitude explicitly and documents the BPHS-oriented linear Dig Bala interpretation used by the implementation.
- YAML `report.selection` expressions are passed to `pandas.DataFrame.query(...)`, so string filters support `.str.contains(...)` (for example, `nakshatra.str.contains('Rohini', na=False)`). Root config constants can now be referenced in `report.selection` and string-valued `computations` using author-facing `constants.foo` syntax, including mapping/weight dictionaries used through expressions such as `vaara.map(constants.marketingWeekdayWeights).fillna(0)`.
- Marketing-oriented presets can combine hard vetoes with YAML-first weighted scoring, including compact time-window flags, planet qualities, dasha-aware scoring, and Ashtakavarga-backed house weighting.
- The current marketing preset now derives a `baseMarketingScore`, then applies simple additive Gowri and special-planet Shadbala adjustments calibrated from observed score/strength ranges, while using shared root-level constants for repeated lists and filters.
- A separate launch preset now targets commencement/go-live use cases with stronger weighting on 1st/2nd/7th/10th/11th house support than the marketing preset, while using the same additive Gowri/Shadbala adjustment structure on top of its own `baseLaunchScore`.
- A new `staffOnboarding` preset now targets institutional joining/onboarding use cases with stronger weighting on 10th/11th/1st house fit, practical 2nd/6th support, and bounded Saturn-inclusive dasha/strength signals.
- A new `studentOnboarding` preset now targets course-entry and learning-commencement use cases with stronger weighting on 4th/5th/9th learning support, education-specific weekday/nakshatra preferences, and Jupiter/Mercury-led dasha/strength signals.
- The system generally evaluates many point-in-time records rather than operating range-first, and first-pass Gowri Panchangam follows that same model by deriving the current segment from sunrise/sunset-based 8-part day/night segmentation and an algorithmic weekday-cycle rule.
- Configuration inputs are standardized at the parsing layer: `latitude`/`longitude` accept compact DMS (`70E15`) or decimal degrees; `startDate`/`startTime` alias the base date/time inputs; `endDate`/`endTime` derive `count` via a both-inclusive range; `count`+`interval` are the canonical sampling keys (legacy `frequency`/`periods` normalized away); and `interval` must be a fixed-duration pandas alias.

## Observed Functional Areas

- CLI execution through `python3 main.py ...` and package script `at`.
- Preset and config composition support (as described in README usage examples).
- Domain calculation coverage implied by test groups:
  - core calculations,
  - dasha calculations,
  - panchang and muhurta-yoga logic,
  - read/write/output behavior,
  - combo generation tooling.
- Output field sets include `planetFlags` (`suF`, `moF`, ...), currently encoding technical state markers (retrograde `R`, combustion `C`) rather than planet quality labels.
- Output field sets include dedicated `planetQualities` columns (`suQ`, `moQ`, ...) for explicit quality-based filtering.
- Output field sets also include compact `timeFlags` via `timeF`, encoding bounded muhurta time-window markers such as Rahu Kalam (`RK`), Yamaganda (`YG`), and Gulika (`GK`) for query-time exclusion.
- Output field sets now also include Gowri fields for the current segment: `gowri`, `gowriScore`, `gowriM`, `gowriS`, `gowriT`, `gowriStart`, `gowriEnd`, plus compact `gowriF` for query-time filtering.
- The usual query mode for Gowri is point-oriented filtering/scoring on generated records, for example exact-name checks (`gowri == 'amirdham'`), numeric score filters (`gowriScore > 0`), and compact string checks on `gowriF`.
- Summary-style custom columns can now resolve constant-backed list references, for example `min: constants.marketingMinHouses`.
- `presets/marketing.yml` now uses YAML-first weighted scoring with compact outputs, explicit taboo-time vetoes, simple additive Gowri/Shadbala adjustments, reduced-column exports for reviewable TSV output, and shared root-level constants for repeated lists, filters, and weekday-weight mappings.
- All four richer presets (`marketing`, `launch`, `staffOnboarding`, `studentOnboarding`) now keep `qualityScore` limited to dynamically varying `Q` values (`Mercury`, `Moon`) rather than scoring fixed-nature planets through constant or impossible branches.
- `presets/launch.yml` now follows the same constants-driven structure for repeated lists, filters, weekday-weight mappings, and core-planet allow-lists while preserving its distinct launch scoring rubric; after the quality-score cleanup, it no longer hard-rejects `moQ == 'malefic'` and instead relies on the broader weighted rubric plus the recalibrated score threshold.
- `presets/staffOnboarding.yml` and `presets/studentOnboarding.yml` now follow the same constants-driven preset pattern as marketing/launch, including constant-backed list references, mapped weekday scoring, bounded Gowri/Shadbala add-ons, and reviewable score decomposition.

## Known Functional Gaps

Backlog includes many requested improvements in configuration model, muhurta/yoga breadth, explainability outputs, and performance optimization.
- Gowri/Choghadiya verification, provenance review, and any distinct Choghadiya exposure remain deferred beyond the first-pass implementation.
