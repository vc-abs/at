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
- Add/update tests with each behavior change.
- Reflect user-facing behavior changes in `docs/guide.md`.
