# Per-scenario constants & computations (+ `eventScoreDev` regression test)

Part of the parameter-sweep story. Pairs with `tasks/CONVENTIONS.md`. Independent
of `tasks/config-imports/` (that work is the contract-reuse story).

## Context

A scenario should be able to override `computations`/`constants` so a
parameter sweep over one contract (same field names, same `report`, different
constant weights) can be expressed without duplicating the whole config. Today
this silently fails: `build_scenarios` shallow-merges `{**config, **scenario}`
(so a scenario overriding one nested constant must restate the whole block),
and `generate_combos` runs `add_custom_columns` **once globally** with the
global `computations`/`constants`, so a scenario's constant override is
ignored at evaluation time.

Files involved:

- `src/at/read_write/read_config.py`
  - `build_scenarios` — currently `k: _standardize_config({**config, **scenario})`.
  - The `merger = Merger(...)` already defined at module scope (dicts merge,
    lists/scalars override) — reuse it for scenarios so merge semantics match
    file stacking.
- `src/at/tools/generate_combos.py`
  - `generate_scenario_combos` — currently does `config = {**config, **scenario_config}`; must match `build_scenarios`'s merge policy.
  - `generate_combos` — currently:
    ```python
    for scenario_name in config['scenarios'].keys():
        df = pd.concat([df, generate_scenario_combos(scenario_name, config)], ...)
    add_custom_columns(df, get_computation_fields(config), config)   # global, once
    ```
    Move the computation step into the per-scenario loop, using **that
    scenario's** merged config (which carries its own
    `computations`/`constants`). `report`/`fieldSets`/output stay global.
  - `get_computation_fields`, `get_computation_constants`,
    `get_expression_locals`, `add_custom_columns` are already parametrized on
    `config` — no signature changes needed, just call them with the scenario
    config.
- `tests/read_write/test_read_config.py` — `test_build_scenarios_merges_defaults_and_scenario_specific` covers current shallow behavior; update for deep-merge.
- `tests/tools/test_generate_combos.py` — add per-scenario computation/constant tests + the `eventScoreDev` regression test (see below).

## Open decisions

- **`report` stays global.** Settled — see `tasks/CONVENTIONS.md`. Do not make
  `report` per-scenario; needing per-scenario `report` is the signal to use
  config imports instead. Confirm the implementation does not accidentally
  route `report` through the per-scenario config.
- **`deepcopy` base for merge.** `Merger.merge` mutates the left argument in
  place; merging `config` directly would leak a scenario's overrides into the
  next iteration and into the global view. Merge onto `copy.deepcopy(config)`
  per scenario (in **both** `build_scenarios` and
  `generate_scenario_combos`). Verify `deepcopy` is imported.
- **Column-union edge case.** If scenarios define *different computed field
  names*, `pd.concat` produces NaN for scenarios lacking a column, and a
  global `report.selection` referencing a scenario-only column silently drops
  those rows. Document this (cheatsheet §11 / conventions) rather than
  engine-guarding it. Recommended author pattern: keep computation field names
  consistent across scenarios.
- **Per-scenario `computations` merge shape.** A scenario that overrides
  `computations` overrides the whole `computations` block under override
  semantics — but with deep-merge, nested `fields`/`constants` merge
  individually, so a scenario can override one constant without restating all
  fields. Confirm this matches author intent (it should: it is the point of
  the deep-merge change).

## Acceptance test

A single config exercising the full sweep:

```yml
interval: 1d
count: 5
latitude: 23.101
longitude: 77.461
constants:
  houseWeight: 1.0
  minScore: 0
computations:
  fields:
    eventScore: "h1 * constants.houseWeight + h5 + h9"
    eventScoreDev: >-
      (eventScore - eventScore.groupby(scenario).transform('mean'))
      / eventScore.groupby(scenario).transform('std')
report:
  selection: "eventScoreDev >= 1.0 and eventScore >= constants.minScore"
  order:
    eventScoreDev: descending
    eventScore: descending
  fieldSets:
    scenario: all
    panchang: all
    ashtakavarga: all
scenarios:
  balanced: {}
  houseHeavy:
    name: house-heavy
    constants:
      houseWeight: 2.5
```

Pass criteria:

1. `balanced` rows compute `eventScore` with `houseWeight == 1.0`;
   `houseHeavy` rows with `houseWeight == 2.5`. (Verify by inspecting the
   ratio of `eventScore` to `h1` across the two scenario groups, or by
   asserting computed values on a known-small fixture.)
2. `eventScoreDev` is a correct per-scenario z-score: within each scenario
   group, the mean of `eventScoreDev` is ~0 and the max row is +1σ (sample
   std, `ddof=1`).
3. `report.selection` (`eventScoreDev >= 1.0`) is applied **once globally**
   across the combined DataFrame, and `report.order`/`fieldSets` are global.
4. Existing presets/behaviors that do not use per-scenario
   `computations`/`constants` are unchanged (regression: run the existing
   `tests/read_write` and `tests/tools` suites).

Plus the `eventScoreDev` **regression test** (locks the eval-string pattern
so a future `df.eval` engine swap does not silently break it):

```python
def test_groupby_transform_string_produces_per_group_zscore():
    df = pd.DataFrame([
        {'scenario': 'a', 'eventScore': 1},
        {'scenario': 'a', 'eventScore': 2},
        {'scenario': 'a', 'eventScore': 3},
        {'scenario': 'b', 'eventScore': 10},
        {'scenario': 'b', 'eventScore': 20},
        {'scenario': 'b', 'eventScore': 30},
    ])
    add_custom_columns(df, {
        'eventScoreDev': "(eventScore - eventScore.groupby(scenario).transform('mean'))"
                         " / eventScore.groupby(scenario).transform('std')",
    }, {'computations': {'constants': {}, 'fields': {}}})
    # per-group z-score, ddof=1
    assert list(df['eventScoreDev']) == [-1.0, 0.0, 1.0, -1.0, 0.0, 1.0]
```

## Rejected alternatives

- **Per-scenario `report`.** Rejected — it forces either multiple output
  tables or a column-union model with NaN-filled selection/order/fieldSets
  interactions. Use config imports for per-contract reporting; scenarios stay
  parameter sweeps with shared `report`. See `tasks/CONVENTIONS.md`.
- **A `groupDev:` / `groupTransform:` computation mapping kind for
  `eventScoreDev`.** Rejected — verified against the repo's actual
  `add_custom_columns` path that `df.eval` supports
  `Series.groupby(...).transform('mean'|'std')` as a plain string expression,
  so the deviation column needs no engine change. Adding a mapping kind would
  be over-engineering. See `tasks/CONVENTIONS.md` for the chosen eval-string
  form and its `ddof=1` / constant-group-NaN caveats.
- **Shallow merge kept, scenarios restate whole blocks.** Rejected — it
  duplicates values and defeats the point of the feature. Deep-merge (reusing
  the existing file-stack `Merger`) gives scenarios the same merge semantics
  as file stacking.
- **Deep-merging `config` in place.** Rejected — `Merger.merge` mutates the
  left argument; per-scenario overrides would leak into the next iteration and
  the global view. Merge onto a `deepcopy` per scenario.
