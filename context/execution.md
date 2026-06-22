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

- `./.venv/bin/python main.py ./presets/staffOnboarding.yml ./presets/archive/.quick.yml ./presets/.private/vc.yml | head -n 5` ✅
  - result: staff onboarding preset produced candidate rows on the retained VC chart
- `./.venv/bin/python main.py ./presets/studentOnboarding.yml ./presets/archive/.quick.yml ./presets/.private/vc.yml | head -n 5` ✅
  - result: student onboarding preset produced candidate rows on the retained VC chart
- `./.venv/bin/python main.py ./temp/staff-onboarding-review-week-export.yml ./presets/staffOnboarding.yml ./presets/.private/vc.yml` ✅
  - result: staff onboarding weekly review TSV generated successfully
- `./.venv/bin/python main.py ./temp/student-onboarding-review-week-export.yml ./presets/studentOnboarding.yml ./presets/.private/vc.yml` ✅
  - result: student onboarding weekly review TSV generated successfully
- `./.venv/bin/python main.py ./temp/staff-onboarding-review-month-export.yml ./presets/staffOnboarding.yml` ✅
  - result: staff onboarding monthly review TSV generated successfully in `temp/`
- `./.venv/bin/python main.py ./temp/student-onboarding-review-month-export.yml ./presets/studentOnboarding.yml` ✅
  - result: student onboarding monthly review TSV generated successfully in `temp/`
- `./.venv/bin/python -m pytest tests/tools/test_generate_combos.py -q` ✅
  - result: preset-structure and combo-generation checks passed
- `./.venv/bin/python -m pytest tests/shadbala/test_shadbala_integration.py -q` ✅
  - result: archived VC fixture integration checks passed
- `./scripts/validate.sh` ✅
  - result: `106 passed`

## Completion State

- Most recent finalized cycle: **Staff and student onboarding presets**.
- Finalization state: **complete**.
- Plan synchronization state: **clean** (`plan.md` has no active plan items).

Finalization summary:

- added `presets/staffOnboarding.yml`
- added `presets/studentOnboarding.yml`
- kept `presets/education.yml` unchanged as the minimal legacy education preset
- added weekly and monthly review export configs/TSVs under `temp/` for both onboarding presets
- added preset-structure assertions for both onboarding presets in `tests/tools/test_generate_combos.py`
- updated `tests/shadbala/test_shadbala_integration.py` to use `presets/archive/.vc.yml`, matching the retained repository fixture layout
- synchronized `docs/guide.md`, `docs/notes.md`, `context/functional.md`, and `context/structural.md` with the delivered onboarding preset behavior
