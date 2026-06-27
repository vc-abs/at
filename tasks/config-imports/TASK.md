# Config imports + muhurta-base preset refactor

Part of the contract-reuse story. Independent of
`tasks/per-scenario-constants/` (that work is the parameter-sweep story).
References `tasks/CONVENTIONS.md` for the `eventScore` convention.

Two commits, in order (see `tasks/README.md` → *Committing*). If the engine
work in commit 1 proves unexpectedly large, use the escape hatch: stop after
commit 1 and defer the preset refactor to a follow-up session. Do not do the
refactor tired/late.

## Context

The four muhurta presets — `presets/marketing.yml`, `presets/launch.yml`,
`presets/staffOnboarding.yml`, `presets/studentOnboarding.yml` — are ~120
lines each and near-duplicate: identical `sources` list, identical
`computations.fields` *structure* (the same chain of `*HouseScore`,
`muhurtaYogaEffect`, `*Min`, `weekdayScore`, `nakshatraScore`, `tithiScore`,
`qualityScore`, `mdPhaseScore`/`adPhaseScore`/`padPhaseScore`/`dashaScore`,
`base*Score`, `gowri*Adj`, `*SpecialStrength`, `*ShadbalaAdj`, final
`*Score`), identical `computations.constants` *shape*, identical
`report.selection` *pattern* and `report.order`, near-identical
`report.fieldSets`. Only coefficients and the planet/house/tithi lists
differ. (Also note: `launch.yml` and `marketing.yml` define their fields
**twice** — once under `computations.fields:` and once as bare top-level keys
— a legacy flat-form duplication that `read_config`'s normalization papers
over; the refactor defines each field once.)

The reuse mechanism that exists today is command-line file stacking
(`main.py base.yml override.yml`). An in-file `imports:` directive makes the
same stacking self-documenting and self-contained: a preset declares what it
builds on, and a colleague can run it without knowing the base stack.

### Files involved (engine)

- `src/at/read_write/read_config.py`
  - `read_config(file_paths)` currently does:
    `config = merge_files([project_root + '/data/defaultConfig.yml'] + file_paths)`.
  - `merge_files` and the module-scope `merger` (`Merger` with dicts merge,
    lists/scalars override) already implement the merge policy to reuse.
  - Add: resolve an `imports:` key in each loaded YAML before merging the
    file's own body. Path resolution, merge order, and cycle handling per the
    Open decisions below. Strip `imports:` from the merged result.
    `defaultConfig.yml` is still prepended once by `read_config`, at the very
    bottom of the stack — imports do not bypass defaults.
- `tests/read_write/test_read_config.py` — add import-resolution tests.

### Files involved (preset refactor, commit 2)

- `presets/muhurta-base.yml` (new) — shared `sources`, shared
  `computations.fields` *structure* keyed on `eventScore` (per
  `tasks/CONVENTIONS.md`), shared `report.selection`/`order`/`fieldSets`
  referencing `eventScore`. Not standalone-runnable (see Open decisions).
- `presets/events/marketing.yml`, `launch.yml`, `staffOnboarding.yml`,
  `studentOnboarding.yml` (new) — each `imports: [../muhurta-base.yml]` and
  states only its `constants` + the two event-specific formulas
  (`eventHouseScore`, `baseEventScore`).
- The four old presets (`presets/{marketing,launch,staffOnboarding,studentOnboarding}.yml`)
  are replaced by the event files. Decide whether the old paths stay as thin
  shims that import the new event file, or are removed (see Open decisions).
- `docs/presets-cheatsheet.md` — new section on imports + the base as
  canonical example.

## Open decisions

### Engine (commit 1)

- **Path resolution.** Settled in discussion: `imports:` paths resolve
  **relative to the importing file's directory**, not CWD. (CWD-relative
  would reintroduce the "colleague can't run it" problem that imports are
  meant to solve.) Confirm the implementation resolves relative to the
  importing file's `os.path.dirname`.
- **Merge order.** Settled: imports are resolved depth-first, then merged
  left-to-right (earlier import = lower priority), then the importing file's
  own body is merged on top (highest priority). This matches current CLI
  stacking semantics exactly — the resolved result equals what
  `main.py <imports in order> <this file>` would produce. Confirm a
  multi-import file (`imports: [base.yml, tweaks.yml]`) merges as
  `merge_files([base.yml, tweaks.yml, this_file_body])` would.
- **Cycle detection.** Agreed to include. Use a visited-set keyed by resolved
  absolute path; on a repeat, raise a clear `ValueError` naming the cycle
  (`a.yml → b.yml → a.yml`). Cheap.
- **`imports:` key stripping.** Remove the `imports:` key from the merged
  result so downstream code (`_standardize_config`, `build_scenarios`) never
  sees it. Confirm no test asserts its presence.
- **Interaction with `scenarios`.** An imported file may define `scenarios`;
  the importer can override individual scenarios via deep-merge. Imports and
  per-scenario constants compose because both use the same `Merger`. Confirm
  with a test.

### Preset refactor (commit 2)

- **Is `muhurta-base.yml` standalone-runnable?** It is **not** — its
  `report.selection` references `eventScore` / `baseEventScore` /
  `eventHouseScore`, which the event files supply via `computations.fields`.
  Document it as an abstract base. Optional nicety: a `debug`-style guard so
  the base can smoke-run with placeholder formulas — defer unless trivial.
- **Old preset paths.** Decide: (a) remove `presets/marketing.yml` etc. and
  point users to `presets/events/marketing.yml`; (b) keep the old paths as
  one-line shims (`imports: [events/marketing.yml]`) for compatibility. Pre-1.0,
  AGENTS.md says no backward-compat effort is required, so (a) is acceptable
  and cleaner. Confirm preference and update any docs/CI/`temp/` review
  configs that reference the old paths (search `temp/` and `docs/` for the old
  filenames).
- **`eventScore` rename.** The four score columns (`marketingScore`,
  `launchScore`, etc.) become `eventScore`. This is intentional. Acceptance is
  column-set parity, not value parity. Update any `temp/` review configs or
  tests that reference the old score names. (`tests/tools/test_generate_combos.py`
  has preset-structure assertions mentioning `launchScore` — update them.)
- **Scope of refactor.** The four muhurta presets are the target. Smaller
  duplicates (`amkADL`/`amkDL` → a shared `amk-base`; `biz`/`bizUltra`;
  place presets like `inTNJambukeswarar`) are **out of scope** for this task —
  defer to follow-up unless trivially covered by the same import mechanism
  with no extra engine work.

## Acceptance test

### Engine (commit 1)

Tests in `tests/read_write/test_read_config.py`:

1. **Single import** — a file with `imports: [base.yml]` resolves the base and
   overlays its own body; the result equals `merge_files([base.yml, this.yml])`.
2. **Chained imports** — `c.yml imports b.yml imports a.yml` resolves
   depth-first; `c`'s body wins over `b` over `a`.
3. **Multi-import merge order** — `imports: [a.yml, b.yml]` merges `a` then
   `b` then this file; rightmost wins on conflict.
4. **Relative path resolution** — `imports: [../sibling.yml]` resolves
   relative to the importing file's directory, not CWD. (Use `tmp_path` with a
   subdirectory to verify.)
5. **Cycle rejection** — `a.yml imports b.yml imports a.yml` raises
   `ValueError` naming the cycle.
6. **`imports:` key stripped** — the merged result has no `imports` key.
7. **`defaultConfig` precedence unchanged** — `defaultConfig.yml` is still
   prepended once at the bottom; an import does not bypass or duplicate it.

### Preset refactor (commit 2)

1. Each of `presets/events/{marketing,launch,staffOnboarding,studentOnboarding}.yml`
   loads via `read_config` without error.
2. Each produces a `report` with the same `selection`/`order`/`fieldSets`
   **shape** as the original preset, with `eventScore` in place of the old
   per-event score name (column-set parity, not value parity).
3. The four event files share `muhurta-base.yml` and each is substantially
   smaller than the original (~15 lines vs ~120).
4. Existing preset-structure tests in `tests/tools/test_generate_combos.py`
   that reference the old score names are updated and pass.
5. `./scripts/validate.sh` passes.

## Rejected alternatives

- **Splitting engine and refactor into two task folders.** Rejected — the
  refactor is the engine's acceptance test; landing imports without a real
  consumer is dead code plus a synthetic test, and the refactor cannot be
  authored until the engine works. One folder, two commits (engine first,
  refactor second), with an escape hatch to defer the refactor if the engine
  runs long. See `tasks/README.md` → *Committing*.
- **A `@zscore(eventScore, scenario)` helper injected into
  `get_expression_locals`.** Rejected — would add named magic to the eval
  namespace (contract surface) for a verbosity win that the raw
  `groupby(...).transform(...)` string already covers. Revisit only if real
  presets show the repetition is a pain point. (This is noted here because the
  base's `eventScoreDev` would be the natural place to use such a helper; do
  not add it.)
- **Per-scenario `report` instead of imports.** Rejected — different problem.
  Imports handle contract variation (separate outputs, shared base);
  per-scenario constants handle value variation within one contract (one
  table). See `tasks/CONVENTIONS.md`.
