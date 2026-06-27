# Decisions

## Table of Contents

- [2026-06-22: Adopt deliberate-dev lifecycle artefacts](#2026-06-22-adopt-deliberate-dev-lifecycle-artefacts)
- [2026-06-22: Use BPHS graha drishti for Mercury conditional quality](#2026-06-22-use-bphs-graha-drishti-for-mercury-conditional-quality)
- [2026-06-22: Use BPHS-oriented tithi scoring for Moon conditional quality](#2026-06-22-use-bphs-oriented-tithi-scoring-for-moon-conditional-quality)
- [2026-06-22: Treat Dig Bala as a BPHS-oriented linear directional-strength falloff](#2026-06-22-treat-dig-bala-as-a-bphs-oriented-linear-directional-strength-falloff)
- [2026-06-22: Treat JA Mercury Paksha Bala divergence as comparison evidence only](#2026-06-22-treat-ja-mercury-paksha-bala-divergence-as-comparison-evidence-only)
- [2026-06-22: Prefer dedicated `*Q` columns for planet quality exposure](#2026-06-22-prefer-dedicated-q-columns-for-planet-quality-exposure)
- [2026-06-22: Model marketing/launch Gowri and Shadbala as additive score adjustments](#2026-06-22-model-marketinglaunch-gowri-and-shadbala-as-additive-score-adjustments)
- [2026-06-22: Use root config constants with author-facing `constants.foo` syntax](#2026-06-22-use-root-config-constants-with-author-facing-constantsfoo-syntax)
- [2026-06-22: Keep preset `qualityScore` limited to dynamically varying planet qualities](#2026-06-22-keep-preset-qualityscore-limited-to-dynamically-varying-planet-qualities)
- [2026-06-25: Adopt `count`+`interval` sampling model with parse-time normalization](#2026-06-25-adopt-countinterval-sampling-model-with-parse-time-normalization)
- [2026-06-25: Use compact DMS form for coordinate encoding](#2026-06-25-use-compact-dms-form-for-coordinate-encoding)

## 2026-06-22: Adopt deliberate-dev lifecycle artefacts

- **Decision**: Initialize and use `backlog`, `plan`, `context`, and `docs` artefacts in project root.
- **Rationale**: Improve execution clarity and preserve traceability from idea capture through implementation and finalization.
- **Consequences**: New work should flow via `backlog -> plan -> context -> implementation -> finalization`.

## 2026-06-22: Use BPHS graha drishti for Mercury conditional quality

- **Decision**: Treat BPHS as the canonical rule source for Mercury conditional quality and related graha drishti used in that evaluation.
- **Rationale**: Domain rules should follow an explicit textual authority rather than inheriting inconsistent software behavior from comparison tools.
- **Consequences**: Mercury quality now considers both conjunction and BPHS aspect influence, contributor overlap is deduplicated, and comparison tools such as JyotishApp remain reference points rather than authorities.

## 2026-06-22: Use BPHS-oriented tithi scoring for Moon conditional quality

- **Decision**: Implement Moon conditional quality from BPHS-oriented tithi ranges with an internal graded tithi score, while preserving the existing caller-facing benefic/malefic label contract.
- **Rationale**: This keeps Moon quality grounded in traditional tithi/paksha semantics without requiring wider API changes across dependent code.
- **Consequences**: Moon quality no longer uses the prior angular-distance proxy, benefic/malefic labels now derive from tithi-based logic, and future refinements can deepen the internal score model without changing current call sites.

## 2026-06-22: Treat Dig Bala as a BPHS-oriented linear directional-strength falloff

- **Decision**: Expose Dig Bala directional-reference longitude explicitly and retain a linear falloff interpretation from the directional-strength point to the opposite point.
- **Rationale**: This makes the current Dig Bala interpretation explicit, testable, and reviewable before broader ShadBala completion work proceeds.
- **Consequences**: Dig Bala behavior is now easier to validate in isolation, and remaining ShadBala work can build on a clearer documented baseline rather than an implicit formula.

## 2026-06-22: Treat JA Mercury Paksha Bala divergence as comparison evidence only

- **Decision**: Do not change Mercury's conditional-quality rule solely to match JA's Paksha Bala branch selection for the current manual comparison chart.
- **Rationale**: Current evidence suggests JA may be using a narrower or conjunction-dominant Mercury association rule than this project's BPHS-oriented implementation. Without confirming that the selected BPHS interpretation supports JA's narrower classification, JA output alone is insufficient authority for a rule change.
- **Consequences**: Mercury's current BPHS-oriented classification remains in place, JA divergence for the comparison case is documented as comparison evidence, and any future rule revision must be justified by the chosen canonical textual basis rather than parity pressure alone.

## 2026-06-22: Finalize current ShadBala pass with deferred refinement

- **Decision**: Finalize the current broad ShadBala implementation/audit pass and defer remaining JA comparison gaps to backlog rather than continue speculative in-cycle tuning.
- **Rationale**: The current pass materially improved implementation completeness, runtime stability, test coverage, and documentation, but residual JA differences remain in areas where canonical interpretation is not yet strong enough to justify further immediate rule changes.
- **Consequences**: The current ShadBala pass becomes the new documented baseline, future refinement work is explicitly backlog-driven, and further alignment changes require a new deliberate-dev cycle rather than silent extension of the current one.

## 2026-06-22: Prefer dedicated `*Q` columns for planet quality exposure

- **Decision**: If planet quality is exposed in combo outputs, use dedicated quality columns (for example `suQ`, `moQ`, `meQ`, ...) and do not encode quality into existing `planetFlags` columns.
- **Rationale**: Current flags represent technical state markers (retrograde/combustion) and may be computed independently; quality can be conditional and should remain explicit, semantically clear, and opt-in.
- **Consequences**: Future quality filtering will use `*Q` columns, existing `planetFlags` semantics remain stable, and compute/selection behavior can keep quality generation optional.

## 2026-06-22: Model marketing/launch Gowri and Shadbala as additive score adjustments

- **Decision**: Treat Gowri and the selected special planets' Shadbala strengths as simple additive score adjustments on top of each preset's base score, and use the same adjustment structure in both marketing and launch.
- **Rationale**: The presets need Gowri and strength awareness, but those signals should remain transparent, reviewable, and easy to calibrate from observed ranges. A direct additive multiplier model is simpler than the earlier bounded-percentage mapping while preserving clear separation between the base rubric and the adjustment signals.
- **Consequences**: `presets/marketing.yml` now derives `baseMarketingScore`, `presets/launch.yml` now derives `baseLaunchScore`, and both add simple Gowri/Shadbala adjustment terms on top of their distinct base rubrics. Hourly verification TSVs in `temp/` now support side-by-side review of the resulting candidate sets.

## 2026-06-22: Use root config constants with author-facing `constants.foo` syntax

- **Decision**: Add a root-level `constants` mapping to merged config and expose it to config-authored expressions through author-facing `constants.foo` syntax, with rewriting to pandas-native external-variable access only at evaluation boundaries.
- **Rationale**: Presets need reusable shared lists, thresholds, and maps to stay readable, but those values are config-scoped runtime data rather than row-scoped DataFrame columns. Author-facing `constants.foo` keeps YAML readable while avoiding fragile string interpolation or hidden temporary columns.
- **Consequences**: `config['constants']` is now always available, `report.selection` and string-valued `computations` can reference constants through `constants.foo`, summary/list-style computed columns can resolve references such as `constants.marketingMinHouses`, and presets can centralize repeated values without exporting those constants as output columns.

## 2026-06-22: Keep preset `qualityScore` limited to dynamically varying planet qualities

- **Decision**: Restrict `qualityScore` in the marketing and launch presets to dynamically varying quality labels only (`Mercury`, `Moon`) and do not score fixed-nature planets through `Q` branches.
- **Rationale**: In the current implementation, `Venus` and `Jupiter` are always benefic by `Q`, while `Sun` and `Mars` are always malefic; scoring them through preset `qualityScore` created constant or impossible branches that looked meaningful but did not discriminate real candidates.
- **Consequences**: Both presets now avoid impossible/always-on `qualityScore` cases, launch no longer depends on a hard `moQ != 'malefic'` gate to produce candidates, and preset thresholds/rubrics now reflect actual dynamic quality variation more faithfully.

## 2026-06-25: Adopt `count`+`interval` sampling model with parse-time normalization

- **Decision**: Replace `frequency`+`periods` with `count`+`interval` as the canonical sampling keys, normalized at the parsing layer so downstream code consumes only `count`+`interval`.
- **Rationale**: A single unified sampling model expressed as sample count and fixed cadence is clearer than the legacy frequency/periods pair. Normalizing at parse time avoids a parallel config model downstream.
- **Consequences**: Legacy `frequency`/`periods` are accepted and normalized away (not rejected). `interval` must be a fixed-duration pandas frequency alias; variable-calendar anchors (`M`, `Y`, etc.) are rejected as non-deterministic. `endDate`/`endTime` derive `count` via a both-inclusive range, overriding any coexisting `count` (the window is authoritative). All presets and defaults migrated to `count`+`interval`.

## 2026-06-25: Use compact DMS form for coordinate encoding

- **Decision**: Accept compact hemisphere-in-between DMS form (`70E15`, `15N5930`) and decimal degrees for `latitude`/`longitude`; reject structured-object and delimiter-string forms.
- **Rationale**: One canonical encoding plus the decimal shortcut minimizes parser surface while removing the need for users to pre-convert minutes/seconds to decimal degrees.
- **Consequences**: Compact form parses to decimal degrees at the config layer before any chart computation; hemisphere letters set sign (N/E positive, S/W negative).
