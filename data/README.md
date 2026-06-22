# Data Files Overview

This directory contains non-runtime and governance data used for verification, policy, and auditability.

## Files

- `yogaWeightPolicy.yml`
  - Expected severity policy for each yoga name.
  - Serves as a policy contract for tests.

- `muhurtaYogaProvenance.csv`
  - Citation and verification tracker for yoga definitions/severitys.
  - `primarySourceText` stores the best current source backing a yoga row.
  - `corroboratingSources` stores any additional active English sources that also support that row.
  - `weightSupportStatus` summarizes whether weight support is unsupported, single-source, or corroborated in English.
  - `verse` is reserved for confirmed verse citations.
  - `evidenceSnippet` stores current English evidence text when no confirmed verse citation exists yet.
  - Not currently consumed by runtime scoring.

- `baselines/muhurtaYogaEffects20260622.csv`
  - Frozen snapshot of runtime dataset for change comparison.

## Runtime dataset (outside this folder)

- `src/at/panchang/muhurtaYogaEffects.csv`
  - Active computation table for yoga matching and weighted scoring.
  - Used directly by `src/at/panchang/getMuhurtaYoga.py`.

## Relationship summary

1. Runtime uses `src/at/panchang/muhurtaYogaEffects.csv`.
2. Policy (`data/yogaWeightPolicy.yml`) constrains expected severities.
3. Provenance (`data/muhurtaYogaProvenance.csv`) provides human-audit traceability.
4. Baseline snapshot supports diffs and rollback analysis.
