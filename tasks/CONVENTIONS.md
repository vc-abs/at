# Conventions (in-flight)

**This file is transient.** It exists only to give the active tasks a single
shared reference for conventions that span more than one task folder. When the
tasks that establish these conventions are complete, fold their durable
content into `docs/presets-cheatsheet.md` (author-facing) and
`context/structural.md` (implementation-facing), then delete this file. See
`tasks/README.md`.

## Primary score column: `eventScore`

The canonical primary muhurta-score column name is **`eventScore`**.

- Event-type presets compute `eventScore` instead of per-event names
  (`marketingScore`, `launchScore`, `staffOnboardingScore`,
  `studentOnboardingScore`).
- The `scenario` column already disambiguates *which* event a row belongs to,
  so a shared column name does not lose information.
- A shared name lets a shared base preset define one `report.selection` /
  `report.order` keyed on `eventScore`, and lets multiple output files be
  concatenated and compared across event types.

Optional breakdown columns keep descriptive names (`eventHouseScore`,
`weekdayScore`, `tithiScore`, `qualityScore`, `dashaScore`,
`gowriEventAdj`, `eventShadbalaAdj`) — these are components, not the headline.

## Within-scenario deviation: `eventScoreDev`

For parameter sweeps (same `eventScore` column, different constant weights per
scenario), the companion column **`eventScoreDev`** is a within-scenario
z-score computed as an eval string:

```yml
computations:
  fields:
    eventScore: "h1 * constants.houseWeight + h5 + h9"
    eventScoreDev: >-
      (eventScore - eventScore.groupby(scenario).transform('mean'))
      / eventScore.groupby(scenario).transform('std')
```

Notes (to document in `docs/presets-cheatsheet.md` on completion):

- `transform('std')` uses sample std (`ddof=1`). `ddof=0` is **not**
  expressible via the eval-string form; accept and document.
- A constant `eventScore` within a scenario → `std` is 0 → `eventScoreDev` is
  NaN → those rows silently fail `eventScoreDev >= 1.0`. Expected; document.
- The deviation is computed in `add_custom_columns`, which runs *before*
  `report.selection`, so the mean/std are taken over the **full scan window**,
  not the filtered survivors. This is the intended semantics.
- `scenario` is already a real column on every row (added in `get_time_combos`
  and surfaced by the `scenario` field-set), so the groupby needs no plumbing.

`eventScoreDev` is **most useful** paired with per-scenario constants (where
weight rescaling makes absolute `minEventScore` thresholds break), but it
works on the combined DataFrame regardless of how scores were computed.

## `report` stays global

`report` (selection / order / fieldSets) is **global** and applied once to the
combined DataFrame across all scenarios. It is **not** per-scenario.

Rationale (rejected alternative — do not reopen): making `report`
per-scenario would require either multiple output tables or a column-union
model with NaN-filled selection/order/fieldSets interactions. The moment a
scenario needs its own `report`, it is no longer a parameter sweep over one
contract — it is a separate config, and **config imports** (see
`tasks/config-imports/`) are the correct mechanism, producing one output per
config. Scenarios stay parameter sweeps with shared reporting.

## Scenario merge policy

Scenarios **override** global behavior for the keys they touch (semantic
level), expressed via **deep-merge** for dict-valued blocks (mechanical level)
so authors do not have to restate unchanged nested keys.

- Dicts (`computations`, `computations.constants`, `computations.fields`,
  `report`, nested `constants`) deep-merge.
- Lists (`sources`) and scalars override (restate the whole list/value).
- This is the same merge policy already used for stacked config files
  (`Merger` in `read_config.py`), so scenarios get merge semantics identical
  to file stacking.
- Implementation must deep-merge onto a **copy** of the global config per
  scenario, so a scenario's overrides do not leak across iterations or into
  the global view.

## Per-scenario `sources` is a footgun without per-scenario computations

Today `sources` is already read from the merged per-scenario config inside
`generate_scenario_combos`, so a scenario *can* prune `sources`. But
everything downstream (`computations`, `report.selection`, `report.order`,
`report.fieldSets`) is global and assumes a uniform schema. Pruning a source
that a global computation/selection/fieldSet references causes either silent
NaN drops (if some scenarios keep it) or a hard `KeyError` /
`UndefinedVariableError` (if all scenarios prune it).

Per-scenario `computations` (see `tasks/per-scenario-constants/`) widens the
safe window: a scenario that prunes `sources` can also override
`computations` to only reference the columns it still produces. Safe
per-scenario `sources` therefore composes with, and benefits from, the
per-scenario computations work.
