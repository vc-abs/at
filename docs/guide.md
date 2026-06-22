# Guide

## Table of Contents

- [What This Tool Does](#what-this-tool-does)
- [Basic Usage](#basic-usage)
- [Query Language Notes](#query-language-notes)
- [Config Constants](#config-constants)
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

## Config Constants

- Configs may define a root-level `constants` mapping for reusable preset/config values.
- In expression strings such as `query` and string-valued `customColumns`, use author-facing `constants.foo` syntax.
- Example patterns:
  - allow/filter lists: `nakshatra.isin(constants.launchNakshatras)`
  - mapping/weight dictionaries: `vaara.map(constants.marketingWeekdayWeights).fillna(0)`
  - numeric lookups: `h2 * constants.houseWeights.h2 + h3 * constants.houseWeights.h3`
- In summary/list-style custom columns, constant-backed lists can also be referenced directly:
  - `min: constants.marketingMinHouses`
- A useful pattern is to centralize weekday preferences as a weight map and then query on the derived score, for example `weekdayScore > 0`, instead of duplicating both a weekday allow-list and a separate weekday score formula.
- Constants stay available on merged runtime config as `config['constants']`.
- Constants are config-scoped runtime data, not output columns; they only appear in output if a config explicitly derives a custom column from them.

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

- `presets/marketing.yml` provides a marketing/campaign-timing preset.
- It combines:
  - hard vetoes for compact time-window flags (`timeF`),
  - weighted YAML base scoring for houses, tithi, nakshatra, dasha phases, and quality signals,
  - dynamic quality scoring based only on planets whose `Q` can vary in the current implementation (`Mercury`, `Moon`),
  - a simple additive Gowri adjustment derived from `gowriScore`,
  - a simple additive special-planet Shadbala adjustment derived from the average of Mercury, Venus, Moon, Jupiter, and Sun strengths,
  - reduced-column TSV export support via stacked override configs.
- `presets/launch.yml` provides a separate launch/go-live preset for product launch, company start, offer go-live, and similar commencement-oriented use cases.
- The launch preset intentionally emphasizes commencement/transactability houses more than the marketing preset, but now uses the same simple additive Gowri/Shadbala adjustment pattern on top of its own base score.
- Both presets now avoid impossible or always-on quality branches for fixed-nature planets; fixed benefic/malefic tendencies are captured through the broader rubric rather than through constant `qualityScore` terms.
- Current preset scope intentionally excludes owner/business-chart-specific natal alignment logic.
