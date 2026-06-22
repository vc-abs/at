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
- Maintain a one-to-one mapping between implementation modules and test modules.
- Add new assertions for a module in that module's existing test file; do not create `*_more` or catch-all follow-up test files for the same source module.
- When introducing a new implementation module, add its dedicated test module in the corresponding `tests/` area using the matching module-oriented name.
- Add/update tests with each behavior change.
- Reflect user-facing behavior changes in `docs/guide.md`.
