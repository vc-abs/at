# Decisions

## Table of Contents

- [2026-06-22: Adopt deliberate-dev lifecycle artefacts](#2026-06-22-adopt-deliberate-dev-lifecycle-artefacts)
- [2026-06-22: Use BPHS graha drishti for Mercury conditional quality](#2026-06-22-use-bphs-graha-drishti-for-mercury-conditional-quality)

## 2026-06-22: Adopt deliberate-dev lifecycle artefacts

- **Decision**: Initialize and use `backlog`, `plan`, `context`, and `docs` artefacts in project root.
- **Rationale**: Improve execution clarity and preserve traceability from idea capture through implementation and finalization.
- **Consequences**: New work should flow via `backlog -> plan -> context -> implementation -> finalization`.

## 2026-06-22: Use BPHS graha drishti for Mercury conditional quality

- **Decision**: Treat BPHS as the canonical rule source for Mercury conditional quality and related graha drishti used in that evaluation.
- **Rationale**: Domain rules should follow an explicit textual authority rather than inheriting inconsistent software behavior from comparison tools.
- **Consequences**: Mercury quality now considers both conjunction and BPHS aspect influence, contributor overlap is deduplicated, and comparison tools such as JyotishApp remain reference points rather than authorities.
