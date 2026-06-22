# Development Approach

## Table of Contents

- [Default Workflow](#default-workflow)
- [Quality Gates](#quality-gates)
- [Implementation Guidelines](#implementation-guidelines)

## Default Workflow

1. Promote one focused backlog item to `plan`.
2. Select an approach in `plan` and promote it to `context`.
3. Implement incrementally with small, testable commits.
4. Validate through lint + tests before finalization.

## Quality Gates

- Run project validation command when available: `./scripts/validate.sh`.
- Maintain/improve test coverage for touched code.
- Preserve CLI and config compatibility unless explicitly changed in plan/context.

## Implementation Guidelines

- Prefer deterministic calculations and explicit units/types.
- Keep domain constants and rules traceable and documented.
- Prefer YAML/config-first solutions over runtime/code expansion when the requested behavior can be expressed clearly and maintainably in the existing preset/query/custom-column surface.
- When YAML expressions become long or compound, prefer multi-line YAML string forms for readability where supported, including escaped continuation where needed to preserve query semantics.
- Prefer dictionary/data-driven dispatch over long `if`/`elif` chains or switch-style branching when selecting behavior by key/category, unless branching is genuinely clearer for a small bounded case.
- Maintain a one-to-one mapping between implementation modules and test modules.
- Use snake_case for Python filenames, including test modules (for example `test_muhurta_yoga_rules.py`).
- Add new assertions for a module in that module's existing test file; do not create `*_more` or catch-all follow-up test files for the same source module.
- When introducing a new implementation module, add its dedicated test module in the corresponding `tests/` area using the matching module-oriented snake_case name.
- Add/update tests with each behavior change.
- Prefer short lead-in sentences followed by bullet lists when recording multiple functional rules or behavior highlights in `context/functional.md`.
- Reflect user-facing behavior changes in `docs/guide.md`.
- For large binary reference artifacts (for example PDFs), prefer keeping only immediately used artifacts in-repo; otherwise store source links in backlog/docs for on-demand retrieval.
- If large PDFs must be retained locally, track them with DVC pointers (`*.dvc`) and do not commit raw binaries to Git history.
- Repository pre-commit policy denies direct `.pdf` staging.
