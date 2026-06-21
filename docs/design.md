# Design

## Table of Contents

- [High-Level Architecture](#high-level-architecture)
- [Execution Model](#execution-model)

## High-Level Architecture

- Python package under `src/at`.
- CLI entrypoint in `at.main`.
- Config-driven execution using YAML inputs and presets.
- Test modules organized by domain behavior under `tests/`.

## Execution Model

1. Load and merge config/presets.
2. Compute requested astrological values and derived scores/effects.
3. Emit output in configured format.
