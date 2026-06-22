# Execution Context

## Table of Contents

- [Current Status](#current-status)
- [Most Recent Finalized Cycle](#most-recent-finalized-cycle)

## Current Status

- Active change set: none.
- Validation pending: no.
- Ready for finalization: no.

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
