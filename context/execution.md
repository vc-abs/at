# Execution Context

This document stores active implementation-cycle state for the current execution context.

## Table of Contents

- [Active Cycle](#active-cycle)
- [Validation](#validation)
- [Completion State](#completion-state)

## Active Cycle

- Current cycle item: **none**.
- Active change set: **none**.
- Cycle status: **idle (no active implementation cycle)**.

## Validation

Latest finalized-cycle validation evidence:

- `./scripts/validate.sh` ✅
  - result: `104 passed`
- `./.venv/bin/python main.py ./presets/marketing.yml ./presets/.quick.yml ./presets/.vc.yml | head -n 5` ✅
  - result: constant-backed marketing preset produced a filtered candidate row
- `./.venv/bin/python main.py ./presets/launch.yml ./presets/.quick.yml ./presets/.vc.yml | head -n 5` ✅
  - result: launch preset produced filtered review candidates after the quality-score cleanup

## Completion State

- Most recent finalized cycle: **Preset-level constants support and preset quality-score cleanup**.
- Finalization state: **complete**.
- Plan synchronization state: **clean** (`plan.md` has no active plan items).

Finalization summary:

- root config now always exposes `constants`
- `generateCombos` supports author-facing `constants.foo` syntax in `query` and string `customColumns`
- summary/list-style custom columns can resolve constant-backed references such as `constants.marketingMinHouses`
- marketing and launch presets now use shared constants for repeated lists, filters, and weekday-weight mappings
- both presets limit `qualityScore` to dynamically varying `Q` values (`Mercury`, `Moon`)
- launch no longer hard-rejects `moQ == 'malefic'`; it now relies on the broader weighted rubric with a recalibrated threshold
- guide, notes, decisions, and functional context were synchronized with the delivered behavior
