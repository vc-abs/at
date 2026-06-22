# Guide

## Table of Contents

- [What This Tool Does](#what-this-tool-does)
- [Basic Usage](#basic-usage)
- [Query Language Notes](#query-language-notes)
- [Gowri Panchangam Notes](#gowri-panchangam-notes)
- [Preset Notes](#preset-notes)

## What This Tool Does

`at` helps identify auspicious times for selected activities using Vedic astrology inputs and configurable presets.

## Basic Usage

- Setup environment: `sh ./setup.sh`
- Run with config: `python3 main.py ./examples/config.yml`
- Run validation: `./scripts/validate.sh`

## Query Language Notes

- The YAML `query` value is evaluated using `pandas.DataFrame.query(...)`.
- String contains checks are supported through vectorized string accessors, e.g.:
  - `nakshatra.str.contains('Rohini', na=False)`
  - `nakshatra.str.contains('rohini', case=False, na=False)`
  - `timeF.str.contains('RK', na=False) == False`
  - `gowriScore > 0`
  - `gowri == 'amirdham'`
- Compact flag columns can be queried the same way; for example `timeF` may contain pipe-separated markers such as `RK`, `YG`, and `GK`.
- Gowri compact flags use `gowriF`, which contains pipe-separated markers built from the current Gowri name, polarity, and time-of-day bucket.
- Use `na=False` for robust behavior when a string column may contain nulls.

## Gowri Panchangam Notes

- The first pass exposes current Gowri fields through the `panchang` field set and a dedicated `gowriFlags` field set.
- Available current-segment fields include:
  - `gowri` — current Gowri segment name
  - `gowriScore` — numeric quality score for the current segment
  - `gowriM` — simple meaning label (`best`, `good`, `gain`, `wealth`, `evil`, `bad`)
  - `gowriS` — segment number within the current day/night block
  - `gowriT` — `day` or `night`
  - `gowriStart` / `gowriEnd` — current segment bounds
  - `gowriF` — compact pipe-separated flag string for querying
- `amirdham` is scored as `2`; other favorable labels are `1`; unfavorable labels are `-1`.
- The first pass uses an algorithmic weekday-cycle model rather than a persisted runtime Gowri table.

## Preset Notes

- `presets/marketing.yml` provides a first-pass marketing/campaign-launch preset.
- It combines:
  - hard vetoes for compact time-window flags (`timeF`),
  - weighted YAML scoring for houses, tithi, nakshatra, dasha phases, and quality signals,
  - reduced-column TSV export support via stacked override configs.
- Current marketing preset scope intentionally excludes owner/business-chart-specific natal alignment logic.
