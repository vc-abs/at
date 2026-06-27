# Presets Cheatsheet

## What a preset is

A preset is a YAML config file passed to `main.py`.

You can run one file:

```bash
python3 main.py ./presets/panchang.yml
```

Or stack multiple files:

```bash
python3 main.py ./presets/events/marketing.yml ./examples/presetExtensions.yml
```

Files are merged left to right.
The file on the right has higher priority.

The runtime also loads defaults from [`data/defaultConfig.yml`](../data/defaultConfig.yml) first.

---

## 1) Simplest useful run

Use an existing preset:

```bash
python3 main.py ./presets/panchang.yml
```

That preset is small:

```yml
day: 14
hour: 12
minute: 0
second: 0
frequency: 1d
periods: 365
fieldSets:
  scenario: all
  panchang: all
scenarios:
  panchang:
    name: "panchang"
    month: 4
```

What it does:
- scans one row per day
- keeps only `scenario` and `panchang` output fields
- defines a named scenario
- relies on defaults for ayanamsa, timezone offset, and location

---

## 2) Small custom preset

Start with a tiny file and only choose what to output.

```yml
# ./temp/my-panchang.yml
fieldSets:
  scenario: all
  panchang: all
```

Run it:

```bash
python3 main.py ./temp/my-panchang.yml
```

This relies on defaults from `data/defaultConfig.yml`, including:
- `ayanamsa`
- `utcHour` / `utcMinute`
- `latitude` / `longitude`
- `frequency`
- `periods`

---

## 3) Set the scan window and place

Add your own date/time seed, timezone offset, place, and scan size.

```yml
# ./temp/my-window.yml
year: 2025
month: 1
day: 4
hour: 6
minute: 0
second: 0
utcHour: 5
utcMinute: 30
latitude: 13.0827
longitude: 80.2707
frequency: 30min
periods: 96

fieldSets:
  scenario: all
  panchang: all
```

Run it:

```bash
python3 main.py ./temp/my-window.yml
```

Notes:
- `frequency` uses pandas-style date range frequencies such as `15min`, `30min`, `1h`, `1d`.
- `periods` is the number of rows to generate.
- the starting timestamp comes from `year/month/day/hour/minute/second` plus `utcHour/utcMinute`

---

## 4) Stack presets and overrides

A very common pattern is:
1. start from a richer preset
2. add a small override file on the right

Example:

```bash
python3 main.py ./presets/events/launch.yml ./examples/presetExtensions.yml
```

### Merge rules

When multiple YAML files are passed:

- dicts are deep-merged
- scalars are overridden
- lists are overridden, not appended
- the rightmost file wins

### Example

Base file:

```yml
fieldSets:
  scenario: all
  panchang: all
customColumns:
  score: "h1 + h5 + h9"
```

Override file:

```yml
fieldSets:
  panchang:
    - tithi
    - nakshatra
exportTo: ./temp/out.tsv
```

Merged effect:
- `fieldSets.scenario` stays
- `fieldSets.panchang` becomes the explicit list from the override
- `customColumns.score` stays
- `exportTo` is added

### Important gotcha

Lists do **not** merge item by item.
If you override a list, restate the whole list you want.

### Imports: self-documenting stacking

Instead of stacking files on the command line, a preset can declare what it
builds on with an `imports:` directive. This makes the stack
self-documenting and self-contained — a colleague can run a single file
without knowing the base stack.

```yml
# ./presets/events/launch.yml
imports: [../muhurta-base.yml]
computations:
  constants:
    eventWeekdayWeights: { wednesday: 28, friday: 24, thursday: 22, sunday: 20 }
    # ...event-specific coefficients and lists...
  fields:
    eventHouseScore: >-
      (h1 * 1.2 + h2 * 1.4 + h7 * 1.4 + h10 * 1.5 + h11 * 1.6) * 0.38
    baseEventScore: >-
      eventHouseScore + muhurtaYogaEffect * 12 + weekdayScore + dashaScore
    eventScore: >-
      baseEventScore + gowriEventAdj + eventShadbalaAdj
```

Resolution rules:

- `imports:` paths resolve **relative to the importing file's directory**, not
  CWD, so the preset is portable.
- Imports are resolved depth-first, then merged left-to-right (earlier import =
  lower priority), then the importing file's own body is merged on top (highest
  priority). The result equals what
  `main.py <imports in order> <this file>` would produce.
- The same merge rules apply: dicts deep-merge, lists and scalars override.
- The `imports:` key is stripped from the merged result; downstream code never
  sees it.
- Import cycles raise a `ValueError` naming the cycle.
- `data/defaultConfig.yml` is still prepended once at the very bottom of the
  stack; imports do not bypass or duplicate the defaults.

The canonical example is `presets/muhurta-base.yml`, an abstract base that owns
the shared `sources`, the shared score-chain structure (coefficient-driven via
`constants.event*`), and the shared `report` keyed on `eventScore`. It is **not
standalone-runnable** — its `report.selection` and score chain reference
`eventHouseScore` / `baseEventScore` / `eventScore`, which an importing event
preset must supply. The four event presets
(`presets/events/{marketing,launch,staffOnboarding,studentOnboarding}.yml`)
import it and each declare only their coefficients plus those three formulas.

Imports also compose with `scenarios`: an imported file may define `scenarios`,
and the importer can override individual scenarios via deep-merge, because both
use the same merge policy.

#### Primary score column: `eventScore`

The canonical primary muhurta-score column name is **`eventScore`**. Event-type
presets compute `eventScore` instead of per-event names
(`marketingScore`, `launchScore`, …). The `scenario` column already
disambiguates *which* event a row belongs to, so a shared column name loses
no information — and it lets a shared base preset define one `report.selection`
/ `report.order` keyed on `eventScore`, and lets multiple output files be
concatenated and compared across event types. Optional breakdown columns keep
descriptive names (`eventHouseScore`, `weekdayScore`, `tithiScore`,
`qualityScore`, `dashaScore`, `gowriEventAdj`, `eventShadbalaAdj`) — these are
components, not the headline.

---

## 5) Choose output columns with `fieldSets`

`fieldSets` control which columns appear in the final output.

Each field set accepts:
- `all`
- `none`
- an explicit list of columns

### Available field sets

- `scenario`
- `panchang`
- `muhurtaYogaEffects`
- `objectHouses`
- `planetaryDegrees`
- `ashtakavarga`
- `mahaDasha`
- `antarDashas`
- `planetFlags`
- `planetQualities`
- `timeFlags`
- `gowriFlags`
- `shadBalaStrength`
- `karakas`

### Example: all columns from a few sets

```yml
fieldSets:
  scenario: all
  panchang: all
  muhurtaYogaEffects: all
  timeFlags: all
```

### Example: only selected columns

```yml
fieldSets:
  scenario: all
  panchang:
    - tithi
    - nakshatra
    - vaara
  muhurtaYogaEffects:
    - positive
    - negative
  timeFlags:
    - timeF
```

### Example: suppress a set

```yml
fieldSets:
  scenario: all
  panchang: all
  shadBalaStrength: none
```

Tip: start narrow. `all` on many field sets can make output very wide.

---

## 6) Filter rows with `report.selection`

`report.selection` is evaluated with `pandas.DataFrame.query(...)`.

Simple example:

```yml
report:
  selection: "positive + negative > 0"
  fieldSets:
    scenario: all
    panchang: all
    muhurtaYogaEffects: all
```

String example:

```yml
report:
  selection: >-
    nakshatra.str.contains('rohini', case=False, na=False) and
    timeF.str.contains('RK', na=False) == False
```

Useful patterns already used in the repo:
- `nakshatra.str.contains('Rohini', na=False)`
- `timeF.str.contains('RK|YG|GK', na=False) == False`
- `gowriScore > 0`
- `gowri == 'amirdham'`

### Query gotchas

- Use pandas query syntax, not arbitrary Python.
- Reference column names that exist in the generated DataFrame.
- Quote string literals.
- Use `na=False` for safer string filtering on nullable columns.

---

## 7) Add computed columns with `computations`

Use `computations` to derive scores, summaries, booleans, and helper columns.

### Simple expression columns

```yml
computations:
  dharma: "h1 + h5 + h9"
  muhurtaYogaEffect: "positive + negative"
```

### Summary columns across multiple columns

```yml
computations:
  minH:
    min:
      - h2
      - h6
      - h9
      - h10
      - h11
```

### Filter using the computed columns

```yml
report:
  selection: "dharma > 75 and muhurtaYogaEffect > 0"
  order:
    dharma: descending
    muhurtaYogaEffect: descending
```

### Evaluation notes

- string-valued `computations` are evaluated with `df.eval(...)`
- summary columns such as `min`, `max`, etc. operate across listed columns
- computed columns are available to later steps like `report.selection`, `report.order`, and output selection

### Gotcha

Define dependencies in a safe order.
If one custom column uses another, put the dependency first.

---

## 8) Reuse values with `constants`

Use root-level `constants` for reusable lists, thresholds, and maps.

```yml
constants:
  tabooTimeFlagsRegex: 'RK|YG|GK'
  goodWeekdayWeights:
    wednesday: 30
    friday: 24
    thursday: 22
  minHouses:
    - h3
    - h5
    - h7
    - h10
    - h11
  minScore: 300

report:
  selection: >-
    timeF.str.contains(constants.tabooTimeFlagsRegex, na=False) == False and
    weekdayScore > 0 and
    score >= constants.minScore

computations:
  weekdayScore: >-
    vaara.map(constants.goodWeekdayWeights).fillna(0)
  minH:
    min: constants.minHouses
  score: >-
    h3 + h5 + h7 + h10 + h11 + weekdayScore
```

You can reference constants from:
- `query`
- string-valued `customColumns`
- summary/list-style custom columns such as `min: constants.minHouses`

This is the main pattern used by the richer event presets like:
- `presets/events/marketing.yml`
- `presets/events/launch.yml`
- `presets/events/staffOnboarding.yml`
- `presets/events/studentOnboarding.yml`

These four share `presets/muhurta-base.yml` via `imports:` (see *Imports* below).

---

## 9) Sort results with `order`

Use `order` to sort the filtered DataFrame before output. `report.selection` is applied first, then `order` sorts the surviving rows; the sort is stable, so tied rows keep their original relative order.

```yml
order:
  eventScore: descending
  baseEventScore: descending
  muhurtaYogaEffect: descending
```

Another example:

```yml
order:
  dharma: descending
  muhurtaYogaEffect: descending
```

---

## 10) Export instead of printing to stdout

By default, output is printed to stdout using `exportSeparator`.

To write to a file:

```yml
exportTo: ./temp/results.tsv
exportSeparator: "\t"
```

CSV example:

```yml
exportTo: ./temp/results.csv
exportSeparator: ","
```

Run:

```bash
python3 main.py ./temp/my-export.yml
```

---

## 11) Use multiple scenarios in one run

You can define `scenarios` so one config produces multiple named scans.

```yml
year: 2025
month: 4
day: 14
hour: 6
minute: 0
second: 0
latitude: 23.101
longitude: 77.461
frequency: 1d
periods: 10

fieldSets:
  scenario: all
  panchang: all

scenarios:
  default: {}
  evening:
    hour: 18
    name: evening-scan
  nextMonth:
    month: 5
    name: next-month-scan
```

Scenario values inherit the top-level defaults unless overridden.

### Merge policy (scenarios stack like files)

A scenario is **deep-merged** onto a fresh copy of the global config, using
the same policy as stacked config files (see §4):

- **dicts merge** (`computations`, `computations.constants`,
  `computations.fields`, nested `constants`);
- **lists and scalars override** (restate the whole list/value).

So a scenario can override a single constant without restating the rest of
the block, and the override stays scoped to that scenario — it does not leak
into sibling scenarios or the global view.

### Per-scenario `constants` and `computations`

A scenario may override `constants` (or `computations.constants` /
`computations.fields`) to express a **parameter sweep** over one contract:
the same field names and the same `report`, but different constant weights.
Computations are evaluated **per scenario** using that scenario's merged
config, so a scenario's constant override actually changes computed values.

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

`balanced` rows compute `eventScore` with `houseWeight == 1.0`; `houseHeavy`
rows with `houseWeight == 2.5` — without restating `minScore`, the `fields`,
or the `report`.

### `eventScoreDev` — within-scenario z-score

`eventScoreDev` is a within-scenario z-score written as a plain eval string
using `Series.groupby(scenario).transform(...)`:

```yml
computations:
  fields:
    eventScoreDev: >-
      (eventScore - eventScore.groupby(scenario).transform('mean'))
      / eventScore.groupby(scenario).transform('std')
```

Notes:

- `transform('std')` uses **sample std (`ddof=1`)**. Population std
  (`ddof=0`) is not expressible via the eval-string form.
- A constant `eventScore` within a scenario → `std` is 0 → `eventScoreDev`
  is NaN → those rows silently fail `eventScoreDev >= 1.0`. Expected.
- The deviation is computed in `add_custom_columns`, which runs **before**
  `report.selection`, so the mean/std are taken over the full scan window,
  not the filtered survivors.
- `scenario` is already a real column on every row, so the groupby needs no
  plumbing.

`eventScoreDev` is most useful paired with per-scenario constants (weight
rescaling makes absolute `minEventScore`-style thresholds break), but it
works on the combined DataFrame regardless of how scores were computed.

### `report` stays global

`report` (selection / order / fieldSets) is **global** and applied once to
the combined DataFrame across all scenarios. It is not per-scenario. The
moment a scenario needs its own `report`, it is no longer a parameter sweep
over one contract — split it into a separate config (see §4 *Imports*).

### Edge case: scenarios with different computed field names

If scenarios define *different* computed field names, `pd.concat` produces
NaN for scenarios lacking a column, and a global `report.selection` /
`report.fieldSets` referencing a scenario-only column will silently drop or
blank those rows. The engine does not guard against this. Recommended
author pattern: keep computation field names consistent across scenarios.

### Footgun: per-scenario `sources` without per-scenario `computations`

`sources` is already read from the merged per-scenario config inside
`generate_scenario_combos`, so a scenario *can* prune `sources`. But everything
downstream of it (`computations`, `report.selection`, `report.order`,
`report.fieldSets`) assumes a uniform schema. Pruning a source that a global
computation/selection/fieldSet references causes either silent NaN drops (if
some scenarios keep it) or a hard `KeyError` / `UndefinedVariableError` (if all
scenarios prune it).

Per-scenario `computations` (above) widens the safe window: a scenario that
prunes `sources` can also override `computations` to only reference the columns
it still produces. Safe per-scenario `sources` therefore composes with, and
benefits from, per-scenario computations.

---

## 12) Progressive build-up example

Here is the same idea grown step by step.

### Step A: just show panchang

```yml
fieldSets:
  scenario: all
  panchang: all
```

### Step B: add a date window

```yml
year: 2025
month: 1
day: 4
hour: 6
minute: 0
second: 0
frequency: 1h
periods: 48

fieldSets:
  scenario: all
  panchang: all
```

### Step C: add supporting data needed for filtering

```yml
fieldSets:
  scenario: all
  panchang: all
  muhurtaYogaEffects: all
  timeFlags: all
  ashtakavarga: all
```

### Step D: add helper columns

```yml
computations:
  muhurtaYogaEffect: "positive + negative"
  dharma: "h1 + h5 + h9"
```

### Step E: add filtering and sorting

```yml
report:
  selection: "dharma > 75 and muhurtaYogaEffect > 0"
  order:
    dharma: descending
    muhurtaYogaEffect: descending
```

### Step F: extract only the columns you care about

```yml
report:
  fieldSets:
    scenario: all
    panchang:
      - tithi
      - nakshatra
      - vaara
    muhurtaYogaEffects:
      - positive
      - negative
```

---

## 13) Complete examples

## Complete example A: simple custom scoring preset

```yml
# ./temp/dharma-scan.yml
year: 2025
month: 1
day: 4
hour: 6
minute: 0
second: 0
utcHour: 5
utcMinute: 30
latitude: 23.101
longitude: 77.461
frequency: 1h
periods: 72

report:
  selection: "dharma > 75 and muhurtaYogaEffect > 0"

computations:
  dharma: "h1 + h5 + h9"
  muhurtaYogaEffect: "positive + negative"
  maxOfDharma:
    max:
      - h1
      - h5
      - h9

report:
  order:
    dharma: descending
    muhurtaYogaEffect: descending
  fieldSets:
    scenario: all
    panchang: all
    muhurtaYogaEffects: all
    ashtakavarga: all
```

Run it:

```bash
python3 main.py ./temp/dharma-scan.yml
```

## Complete example B: constants-driven marketing-style preset

```yml
# ./temp/simple-marketing.yml
year: 2025
month: 2
day: 10
hour: 6
minute: 0
second: 0
utcHour: 5
utcMinute: 30
latitude: 23.101
longitude: 77.461
frequency: 30min
periods: 96

constants:
  tabooTimeFlagsRegex: 'RK|YG|GK'
  weekdayWeights:
    wednesday: 30
    friday: 24
    thursday: 22
  focusHouses:
    - h3
    - h5
    - h7
    - h10
    - h11
  minScore: 140

report:
  selection: >-
    timeF.str.contains(constants.tabooTimeFlagsRegex, na=False) == False and
    muhurtaYogaEffect >= 0 and
    minFocusHouse >= 24 and
    weekdayScore > 0 and
    score >= constants.minScore

computations:
  muhurtaYogaEffect: >-
    positive + negative
  weekdayScore: >-
    vaara.map(constants.weekdayWeights).fillna(0)
  minFocusHouse:
    min: constants.focusHouses
  score: >-
    (h3 * 1.5 + h5 * 1.0 + h7 * 1.2 + h10 * 1.6 + h11 * 1.7) * 0.42 +
    muhurtaYogaEffect * 12 + weekdayScore

report:
  order:
    score: descending
    muhurtaYogaEffect: descending
  fieldSets:
    scenario: all
    panchang:
      - tithi
      - nakshatra
      - vaara
      - gowri
      - gowriScore
    muhurtaYogaEffects:
      - positive
      - negative
    timeFlags:
    - timeF
  ashtakavarga: all
```

Run it:

```bash
python3 main.py ./temp/simple-marketing.yml
```

## Complete example C: stack a built-in preset with a small export override

Override file:

```yml
# ./temp/launch-export.yml
exportTo: ./temp/launch-results.tsv
exportSeparator: "\t"
fieldSets:
  scenario: all
  panchang:
    - tithi
    - nakshatra
    - vaara
    - eventScore
  muhurtaYogaEffects:
    - positive
    - negative
  timeFlags:
    - timeF
```

Run it:

```bash
python3 main.py ./presets/events/launch.yml ./temp/launch-export.yml
```

This is often the cleanest workflow:
- keep the scoring logic in a reusable preset
- keep the run-specific output/export choices in a small override file

---

## 14) Built-in presets worth studying

If you want real repo examples, start here:

- `presets/panchang.yml` — minimal reporting preset
- `presets/biz.yml` — simple score + filter pattern
- `presets/muhurta-base.yml` — abstract shared muhurta base (imports target; not standalone-runnable)
- `presets/events/marketing.yml` — marketing/campaign scoring (imports the base)
- `presets/events/launch.yml` — launch/go-live scoring (imports the base)
- `presets/events/staffOnboarding.yml` — institutional joining scoring (imports the base)
- `presets/events/studentOnboarding.yml` — education/course-entry scoring (imports the base)
- `presets/allFieldSets.yml` — useful for seeing every output group

---

## 15) Gotchas

### Rightmost file wins

```bash
python3 main.py base.yml override.yml
```

`override.yml` has higher priority.

### Lists replace, they do not append

If a later file sets a list, it replaces the earlier list.

### `report.selection` uses pandas query syntax

That means:
- string expressions need quotes
- `.str.contains(...)` is supported
- `na=False` is usually safer for string filters

### `computations` expressions must reference available columns

If you compute from `h1`, `h5`, `h9`, make sure the underlying data exists in the generated DataFrame.

### `report.fieldSets` affect final output, not whether columns can be computed earlier

You can compute and filter on columns, then still choose a smaller final output.

### Prefer `report.fieldSets` over `skipColumns`

Some older examples mention `skipColumns`, but the current runtime path is driven by `report.fieldSets`.
Prefer `report.fieldSets` for shaping output.
