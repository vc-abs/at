# Design

## Table of Contents

- [High-Level Architecture](#high-level-architecture)
- [Execution Model](#execution-model)

## High-Level Architecture

- Python package under `src/at`.
- CLI entrypoint in `at.main`.
- Config-driven execution using YAML inputs and presets.
- Test modules organized by domain behavior under `tests/`.
- Panchang runtime now also includes an algorithmic Gowri Panchangam layer derived from sunrise/sunset-based segment timing plus a compact weekday-cycle rule.

## Gowri Panchangam First Pass

- Runtime lookup implementation: `src/at/panchang/gowri.py`
- Integration surfaces:
  - `Panchang.gowriSchedule`
  - `Panchang.gowriSegment`
  - `Panchang.gowri`
  - combo field set `gowriFlags`
  - expanded `panchang` field set with current Gowri fields

The first pass uses:
- local sunrise -> sunset divided into 8 equal day segments,
- local sunset -> next sunrise divided into 8 equal night segments,
- point-in-time lookup as the primary runtime path, with full schedule derivation available as a secondary surface,
- a rotating weekday cycle for the base Gowri names,
- `visham` placement derived from the effective weekday's Rahu segment,
- night Gowri treated as following the same order as the day Gowri of the weekday offset by four days,
- numeric scoring (`2`, `1`, `-1`) instead of positive/negative labels so `amirdham` can be modeled as stronger than other favorable segments.

## Execution Model

1. Load and merge config/presets.
2. Compute requested astrological values and derived scores/effects.
3. Emit output in configured format.
