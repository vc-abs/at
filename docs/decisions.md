# Decisions

## Table of Contents

- [2026-06-22: Adopt deliberate-dev lifecycle artefacts](#2026-06-22-adopt-deliberate-dev-lifecycle-artefacts)
- [2026-06-22: Use BPHS graha drishti for Mercury conditional quality](#2026-06-22-use-bphs-graha-drishti-for-mercury-conditional-quality)
- [2026-06-22: Use BPHS-oriented tithi scoring for Moon conditional quality](#2026-06-22-use-bphs-oriented-tithi-scoring-for-moon-conditional-quality)
- [2026-06-22: Treat Dig Bala as a BPHS-oriented linear directional-strength falloff](#2026-06-22-treat-dig-bala-as-a-bphs-oriented-linear-directional-strength-falloff)
- [2026-06-22: Treat JA Mercury Paksha Bala divergence as comparison evidence only](#2026-06-22-treat-ja-mercury-paksha-bala-divergence-as-comparison-evidence-only)
- [2026-06-22: Prefer dedicated `*Q` columns for planet quality exposure](#2026-06-22-prefer-dedicated-q-columns-for-planet-quality-exposure)
- [2026-06-22: Model marketing/launch Gowri and Shadbala as additive score adjustments](#2026-06-22-model-marketinglaunch-gowri-and-shadbala-as-additive-score-adjustments)

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
