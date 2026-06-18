---
name: copilot-instructions
---

# GitHub Copilot Instructions

## ⛔ Tool Policy

**Git Operations — Terminal Only:**
- Use `run_in_terminal` for all git commands
- **DO NOT** use MCP git tools (GitKraken, etc.)
- Rationale: Terminal commands ensure consistent behavior and avoid interactive UI dialogs

**Prohibited:**
- ❌ **NO secrets in tracked files** — Never write API keys, tokens, or passwords into any version-controlled file; use `.env` (gitignored) or environment variables only.
- ❌ **NO auto-commit** — Only commit when user explicitly invokes `/commit`
  - **CRITICAL**: Do NOT execute `git commit` unless the user types `/commit` or explicitly says "commit this" or "commit now"
  - **IMPORTANT**: When `commit.prompt.md` is attached/already executing, that attachment IS the explicit `/commit` invocation — execute `git add` + `git commit` immediately without asking for a second confirmation or saying "send /commit to proceed"
- ❌ **NO auto-push** — Never execute `git push`
- ❌ **NO arbitrary commands** — Only allowlisted commands (see below)
- ❌ **NO API access** — Do not call external APIs, cloud providers, or networked services without explicit user consent
- ❌ **NO operations beyond branch** — Stay scoped to current branch and working tree; no branch creation/deletion, force-pushes, or remote changes
- ❌ **NO edits outside repository** — Do not create, modify, or delete files outside the workspace root without explicit user consent
  - **CRITICAL**: This includes user-level config directories (`~/.config/`, `~/Library/`, `%APPDATA%`)
  - If a file outside the repo needs modification, STOP and ask the user first

**Allowlisted Commands:**
```bash
git status              # Check working tree state (auto-allowed)
git diff                # Review changes (auto-allowed)
git log                 # View history (auto-allowed)
git add .               # Stage changes (ONLY after user invokes /commit)
git commit -m "<msg>"   # Commit (ONLY after explicit /commit invocation)
git reset               # Undo operations (allowed when fixing mistakes)
git mv                  # Move/rename tracked files (preserves history)
dvc move                # Move/rename DVC-tracked files (updates .dvc files)
```

**Version Control Best Practices:**
- ✅ **Use `git mv` for git-tracked files** — Preserves history and auto-stages renames
- ✅ **Use `dvc move` for DVC-tracked files** — Updates .dvc pointer files correctly
- ✅ **Check tracking status first** — Use `git ls-files` or `dvc list` to verify tracking
- ❌ **Never use plain `mv`** for version-controlled files — Breaks tracking and history

**Required Behaviors:**
- ✅ **Report summary** — Present a concise summary of proposed changes before impactful actions
- ✅ **Warnings and escalation** — When detecting destructive or sensitive changes (deleting files, upgrading dependencies, touching infra), warn and require explicit approval
- ✅ **Safe operations** — Analysis, dry-run, and informational operations may auto-execute

## Handling Unclear or Ambiguous Requests

When user requests are unclear, ambiguous, or lack sufficient details to proceed confidently:

1. **Create a clarification file** in `temp/` directory
   - Name: `clarification-<brief-description>-<YYMMDD-HHMMSS>.md`
   - Example: `temp/clarification-image-requirements-260215-143022.md`

2. **Fully populate the clarification file** with complete content (not just section headers):
   - **Request Summary**: Brief restatement of user's request with your current understanding
   - **Clarifying Questions**: Numbered list of specific, actionable questions grouped by topic
   - **Context**: Automatically gathered relevant information (analyzed files, detected patterns, existing configurations, related entity definitions)
   - **Options** (if applicable): Present concrete alternatives with specific pros/cons for each
   - **Next Steps**: Explicit actions you'll take once questions are answered

   Important: The file must be **ready for user review and response** with all questions fully articulated and all context already researched and included. Do not create placeholder sections or empty templates.

3. **Present the file** to the user:
   - Create the file using `create_file` tool with all content populated
   - Notify user: "I've created a clarification file at [temp/clarification-xxx.md](temp/clarification-xxx.md) with questions about your request."
   - Prompt: "Please review and answer the questions, then let me know when you're ready to continue."

4. **Wait for user input**:
   - Do NOT proceed with implementation until user provides answers
   - User may edit the file directly or provide answers in chat
   - If answers are provided in chat, update the clarification file with responses

5. **Continue with task**:
   - Once clarity is achieved, reference the clarification file in your work
   - Proceed with implementation based on confirmed requirements
   - Keep the clarification file for audit trail

**When to use this approach:**
- ✅ Multiple valid interpretations exist
- ✅ Missing critical parameters (file paths, naming conventions, dimensions, formats)
- ✅ Technical decisions that impact architecture or user workflow
- ✅ Destructive operations where intent must be crystal clear
- ❌ NOT for trivial clarifications (ask inline in chat)
- ❌ NOT when a reasonable default exists and can be stated

## File Naming Conventions
- Use **kebab-case** for files (e.g., `read-me.md`, `user-service.js`).
- Use **SCREAMING_SNAKE_CASE** for constants (e.g., `MAX_RETRIES`, `API_TIMEOUT`).
- **Prompts:** Named like functions using imperative verbs (e.g., `generate-report`, `create-document`, `refine`).
- **Instructions:** Similar to prompts but use present-continuous tense (e.g., `generating-report`, `creating-document`, `refining`).
- **Agents:** Use nouns as names (e.g., `report-generator`, `document-creator`, `refiner`).

## Code Style
- Follow `.editorconfig` settings for formatting.
- **Indentation:** 2 spaces for YAML files; tabs for other files and shell scripts.
- **Line endings:** LF (Unix-style).
- **Encoding:** UTF-8 for all files.
- **Trailing whitespace:** Remove all trailing whitespace.
- **Final newline:** Always include a newline at end of file.

## Architecture Principles
- Follow separation of concerns (SoC).
- Keep dependencies minimal and well-documented.
- Use interfaces/types for public APIs.
- Organize code/instructions by feature or functional domain.
- Avoid deep nesting; keep functions readable.
- **Dependencies and hierarchy over flat structure** — prefer explicit dependency chains (A calls B calls C) over parallel coordination. A clear hierarchy enables a cleaner mental model and easier debugging.
- **Loops and arrays over repeated blocks** — when the same operation applies to N items, use a loop or list. A new item is a new entry, not a new block.
- **Combine related blocks into one place when it reduces scan locations** — even at the cost of build-layer granularity or a slight increase in image size.
- **Separate blocks for structurally different operations** — not for different instances of the same operation. Installing via apt, downloading GitHub releases, and setting up users are structurally different; six GitHub downloads are not.

## Instruction Scope
- **This file (copilot-instructions.md):** Generic rules only — tool policy, architecture, naming, code style. No project-specific or filetype-specific content.
- **Filetype/context-specific rules:** Add to `.github/instructions/`, prompts, or agent files (e.g., shell-specific style → a shell instructions file; entity rules → entity prompt).
- Keeping generic rules here and specific rules elsewhere prevents this file from becoming a catch-all and allows targeted composition.

## Minimal Modification
- **Prefer the smallest change that achieves the goal.** Avoid rewriting when a targeted edit suffices.
- Apply this to scripts, configs, and instructions alike: move logic to a new file rather than expanding an existing one; add a rule rather than restructuring a section.
- **Insert into existing structures rather than restructuring them.** A new apt package is a new line in the existing install block — not a trigger to merge or split layers.
- When refactoring is necessary, extract into separate files with clear single responsibilities rather than consolidating everything in one place.

## Pattern Awareness Before Editing
- **Read before writing.** Before editing a file, understand its indentation (tabs vs spaces), naming conventions, log helper style, and structural patterns.
- **Find similar things first.** When adding or changing something, search for existing occurrences of the same kind — follow that pattern exactly. Do not introduce a second style alongside an existing one.
- **Group similar operations.** When the same change applies to multiple items (e.g. several scripts with identical log footers), identify all instances upfront and apply them together rather than one at a time.
- **Verify after editing.** After making changes, confirm the result matches the surrounding style — whitespace, quoting, capitalisation, and structure.

## Unix Philosophy
- **One thing well** — one responsibility per function, script, or skill. Split when a second concern appears.
- **Compose, don't monolith** — pipe small focused tools together rather than building multi-purpose scripts.
- **Design outputs for the next consumer** — prefer formats that compose cleanly downstream (plain text, JSON, exit codes) over formats optimised for human reading in isolation.
- **No noise** — no progress banners or "done" messages unless the operation takes >2 seconds.
- **Additive by default, explicit to destroy** — write operations merge into existing state; destructive resets require an explicit opt-in (e.g. a `--clear` flag or a dedicated `reset` command). Accidental data loss should be structurally impossible in normal usage.

## Human Time Over Machine Time
- **Default to saving human time, not machine time.** Cognitive effort, review burden, and context-switching cost more than CPU cycles or a slightly larger image.
- Prefer readability and explicitness over micro-optimisations that require a comment to understand.
- When a trade-off between human clarity and machine efficiency exists and isn't obviously one-sided, favour the human.

## Development Guidelines
- **NEVER use absolute paths with home directory in files** — Do not include paths like `/home/username/`, `~/`, or `C:\Users\username\` in any generated files
- Use relative paths from project root (e.g., `content/entities/`, `logs/`) or workspace-relative paths
- Prefer automation scripts over markdown instructions to the user. The idea is to allow for better developer experience
- **Prefer Node.js over Python** — When choosing technologies or skills, prefer Node.js/JavaScript/TypeScript over Python where possible, without compromising on quality or functionality
- **Use `uv` for all Python operations** — `uv` is pre-installed in the container and used on the host (see `scripts/setup-host.sh`). It replaces `pip`, `pip3`, and `python3 -m venv`:
  - Install packages: `uv pip install <package>` (not `pip install`)
  - Create venvs: `uv venv .venv` (not `python3 -m venv`)
  - Run tools without installing: `uvx <tool>` (e.g., `uvx ruff check .`)
  - Add to requirements: edit `.devcontainer/requirements.txt`, then `uv pip install -r .devcontainer/requirements.txt`
- **Prefer project/workspace level configuration over user level configuration** — Use `.github/`, `.vscode/`, and project root config files instead of `~/.config/` or `~/` user directories
- **General installation and configuration principles:**
  - Install at project level, not user level (tools, packages, configs)
  - Automate setup — Do it, don't just describe it
  - Test with actual operations before declaring success
  - Never modify user-level configs without explicit permission
  - If incompatible, remove and try alternatives (up to 3 attempts)
  - After failures, propose alternative approaches
- **Skills installation** — Use `npx skills add <package> -y` (project-level, no `-g` flag). See `.agents/skills/find-skills/SKILL.md` for complete workflow including testing, setup, and handling alternatives

## Directory Structure
- `.agents/skills/` — Project-level agent skills (gitignored except skill configurations)
- `.temp/` — Temporary files for testing and experimentation (auto-ignored by `.*` pattern, preserves `.gitkeep`)
- `.work/` — Work-in-progress files and drafts (auto-ignored by `.*` pattern)
- `temp/` — Plan files and interactive agent operation files (gitignored)
- `.mcp-servers/` — Local MCP server implementations (auto-ignored by `.*` pattern)
- `.vscode/mcp.json` — MCP configuration for VS Code (workspace-specific)
- `.github/copilot-mcp.json` — MCP configuration for Copilot CLI (project-specific)
- `content/images/` — Production image outputs (gitignored)
- `content/packages/` — CLI tools, MCP servers, and utilities (package folders gitignored, `.yaml` definitions tracked)
  - `<package-name>.yaml` — Package entity definition with run-command, optional setup/build/deploy/remove commands
  - `<package-name>/` — Optional folder for package-specific files (gitignored unless locally developed)
  - See `content/entities/entity-templates/package.template.md` for schema
