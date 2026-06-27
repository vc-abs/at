# Project instructions for agents

- Treat IO contract changes as high-impact: deliberate on the shape, check the implementation/docs/tests that define it, and avoid implementing a contract refactor until the intended structure is clear.
- Until the project has a major version, do not spend effort preserving backward compatibility for contract changes unless explicitly asked.
- Any implementation or behavior change must include matching test updates when relevant.
- After implementation changes, run the relevant tests/validation for the touched area before reporting completion. Prefer targeted tests first; if unavailable, run the nearest broader suite or repo-standard validation.
- If a config key or section is not needed for a preset, it should not be present; keep preset YAML minimal and remove empty optional sections. Optional sections like `computations` should be omitted entirely when empty.
- In the final response, state what tests/validation were run and the result. If tests could not be run, say why and note the residual risk.
