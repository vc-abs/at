# Tasks

`tasks/` holds **in-flight implementation work** only. It is not a permanent
planning surface — the backlog (`backlog.md`) and plan (`plan.md`) stay the
sources of truth for *what* is planned. Each subfolder here carries the extra
context a fresh session needs to implement one cohesive change: open decisions,
the acceptance test, and the alternatives already rejected.

## Lifecycle (Option A — ephemeral)

1. A task folder is created here when a change is scoped and ready to implement.
2. A session implements it, landing one or more commits (see *Committing*
   below). The matching test updates land in the same commit per `AGENTS.md`.
3. On completion, any **durable outcomes** are folded into the permanent doc
   surfaces:
   - author-facing conventions → `docs/presets-cheatsheet.md` (and `docs/guide.md` where relevant);
   - implementation-surface notes → `context/structural.md`;
   - agent-facing rules → `AGENTS.md`.
4. The task folder is then **deleted** (see *Deleting a task folder* below).

Nothing in `tasks/` is meant to survive. If a note is worth keeping, it belongs
in the permanent docs above, not here.

## TASK.md sections

Each `<task>/TASK.md` uses these four sections, in this order:

- **Context** — what the change is and why, with file pointers. Enough for a
  fresh session to orient without re-deriving the goal.
- **Open decisions** — what is settled vs. what the implementing session may
  need to choose. Treat the *current code* as ground truth when acting on
  these (a task file is a snapshot and can drift once edits begin).
- **Acceptance test** — the concrete check that says "done". Must be runnable
  without re-deriving the goal.
- **Rejected alternatives** — decisions already closed, with the reason, so a
  fresh session does not reopen them. This section is the one most often
  skipped and most valuable to keep.

## Committing

Follow the repo's existing conventions — see `.gitmessage` and
`.github/prompts/commit.md`:

- Single-line subject only, unless a body is explicitly requested.
- Format: `<type>(<scope>): <subject>` with types
  `feat, fix, docs, style, refactor, perf, test, chore`.
- Subject: imperative mood, lowercase, no period, max 72 chars.
- Derive the message strictly from the diff.

Per `AGENTS.md`, any implementation or behavior change includes matching test
updates in the same commit. Prefer targeted tests first; if unavailable, run
the nearest broader suite or `./scripts/validate.sh` (ruff + pytest with
coverage).

Suggested granularity for the current tasks:

- `tasks/per-scenario-constants/` → one commit:
  `feat(config): deep-merge scenarios and apply computations per scenario`
  (engine + tests + docs in one atomic change).
- `tasks/config-imports/` → two commits, in order:
  1. `feat(config): support preset imports with cycle detection`
     (engine + resolver tests, no preset changes yet).
  2. `refactor(presets): collapse muhurta presets onto a shared base`
     (the `muhurta-base.yml` + four event files + docs; depends on commit 1).

Validate before committing each:

```bash
./scripts/validate.sh          # ruff + pytest --cov
# or, targeted:
.venv/bin/python -m pytest tests/read_write tests/tools -q
.venv/bin/python -m ruff check src --config ruff.toml
```

Do not commit the `tasks/` folder as part of the implementation commits
themselves — see below.

## Deleting a task folder

Once a task is fully implemented and its durable outcomes have been moved to
the permanent docs, remove its folder so `tasks/` only ever holds in-flight
work:

```bash
git rm -r tasks/<task>/
```

Deletion is its own commit, separate from the implementation commits:

- `chore(tasks): remove completed <task> scaffolding`

This keeps implementation history (the feature commits) clean of scaffolding
removal noise, and makes the task's lifecycle explicit in the log.

Order of operations for finishing a task:

1. Land the implementation commit(s) for the task.
2. Move durable outcomes into `docs/` / `context/` / `AGENTS.md` as a docs
   commit if the edits are non-trivial, or fold them into the final
   implementation commit if small.
3. `git rm -r tasks/<task>/` and commit with `chore(tasks): …`.
4. Confirm `tasks/` now contains only folders for still-open tasks (or is
   empty).

When the **last** open task is removed, also delete any now-stale shared files
that lived only to support in-flight tasks (e.g. `tasks/CONVENTIONS.md` once no
remaining task references it). An empty `tasks/` directory is fine; do not keep
it populated with stale scaffolding.

## On extracting a skill

This hand-authored format is the seed for a future `task-splitting` skill. Do
not skill-ify until at least two task folders have gone through the full
lifecycle (create → implement → fold outcomes → delete), so the skill is
abstracted from observed shape rather than from one example. See the discussion
history in the originating session for the rationale.
