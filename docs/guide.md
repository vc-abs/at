# Guide

## Table of Contents

- [What This Tool Does](#what-this-tool-does)
- [Basic Usage](#basic-usage)
- [Query Language Notes](#query-language-notes)
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
- Compact flag columns can be queried the same way; for example `timeF` may contain pipe-separated markers such as `RK`, `YG`, and `GK`.
- Use `na=False` for robust behavior when a string column may contain nulls.

## Preset Notes

- `presets/marketing.yml` provides a first-pass marketing/campaign-launch preset.
- It combines:
  - hard vetoes for compact time-window flags (`timeF`),
  - weighted YAML scoring for houses, tithi, nakshatra, dasha phases, and quality signals,
  - reduced-column TSV export support via stacked override configs.
- Current marketing preset scope intentionally excludes owner/business-chart-specific natal alignment logic.
