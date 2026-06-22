# Execution Context

## Table of Contents

- [Current Status](#current-status)
- [Most Recent Finalized Cycle](#most-recent-finalized-cycle)

## Current Status

- Active change set: none.
- Validation pending: no.
- Ready for finalization: no.

## Most Recent Finalized Cycle
- Topic: Gowri Panchangam first pass with algorithmic weekday-cycle lookup and queryable output fields.
- Outcome: completed and finalized as a bounded delivery, including point-in-time-first Gowri runtime support, numeric scoring, shared constants, tests, and synchronized docs/context.
- Validation evidence:
  - `./.venv/bin/pytest -q` passed (`94 passed`)
  - `./scripts/validate.sh` passed
- Delivered changes:
  - added runtime Gowri point-in-time and schedule lookup in `src/at/panchang/gowri.py`,
  - exposed current Gowri fields in `Panchang`, the `panchang` field set, and the `gowriFlags` field set,
  - switched from polarity labels to numeric `gowriScore` and corrected the label to `amirdham`,
  - centralized reusable Gowri constants in `src/at/core/constants.py`,
  - aligned new source naming with the repository's current camelCase convention while keeping snake_case filenames,
  - documented the repo-wide point-in-time execution model and query patterns for Gowri,
  - deferred provenance/verification and any separate Choghadiya exposure to backlog follow-up.

## Most Recent Finalized Cycle

- Topic: marketing preset first pass with compact time flags and weighted YAML scoring.
- Outcome: completed and finalized as a bounded delivery, including new combo-output surfaces plus a reviewable marketing preset and TSV exports.
- Validation evidence:
  - `./.venv/bin/pytest -q` passed (`79 passed`)
  - `./.venv/bin/python main.py ./presets/marketing.yml ./examples/presetExtensions.yml` exited successfully
  - `./.venv/bin/python main.py ./presets/marketing.yml ./temp/marketing-week-export.yml` exited successfully and wrote `temp/marketing-week.tsv`
  - `./.venv/bin/python main.py ./presets/marketing.yml ./temp/marketing-quarter-export.yml` exited successfully and wrote `temp/marketing-quarter.tsv`
- Delivered changes:
  - added compact `timeFlags`/`timeF` output for Rahu Kalam, Yamaganda, and Gulika exclusion,
  - added dedicated `planetQualities`/`*Q` output columns,
  - added `presets/marketing.yml` with YAML-first weighted scoring for houses, tithi, nakshatra, quality, and bounded dasha phases,
  - calibrated Ashtakavarga-backed house scoring to contribute roughly around one-third of matched-score mix while keeping quarter-window candidate volume near the prior baseline,
  - added reduced-column TSV export flows for week and quarter review windows,
  - deferred owner/business-chart-specific natal alignment and preset-level `constants` support to backlog.
