# Decisions

## Table of Contents

- [2026-06-22: Adopt deliberate-dev lifecycle artefacts](#2026-06-22-adopt-deliberate-dev-lifecycle-artefacts)
- [2026-06-22: Use BPHS graha drishti for Mercury conditional quality](#2026-06-22-use-bphs-graha-drishti-for-mercury-conditional-quality)
- [2026-06-22: Use BPHS-oriented tithi scoring for Moon conditional quality](#2026-06-22-use-bphs-oriented-tithi-scoring-for-moon-conditional-quality)

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
