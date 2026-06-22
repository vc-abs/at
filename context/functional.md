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
- YAML `query` expressions are passed to `pandas.DataFrame.query(...)`, so string filters support `.str.contains(...)` (for example, `nakshatra.str.contains('Rohini', na=False)`).
- Marketing-oriented presets can combine hard vetoes with YAML-first weighted scoring, including compact time-window flags, planet qualities, dasha-aware scoring, and Ashtakavarga-backed house weighting.

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
- A first-pass `presets/marketing.yml` now uses YAML-first weighted scoring with compact outputs, explicit taboo-time vetoes, dasha-aware scoring, and reduced-column exports for reviewable TSV output.

## Known Functional Gaps

Backlog includes many requested improvements in configuration model, muhurta/yoga breadth, explainability outputs, and performance optimization.
- Backlog still includes preset-level `constants` support so repeated lists/weights can be centralized instead of duplicated inside YAML expression strings.
