---
name: claude-codex-sync
description: Synchronize Claude Code and Codex configuration for the current user and the current repository. Use when the user wants to import Claude settings into Codex, import Codex settings into Claude, or keep both sides' skills and instruction files aligned.
---

Use this skill to run the bundled cross-platform sync tool.

Rules:
- Default to `--scope all` when the user says "current environment", "everything", or asks for both user-level and repo-level sync.
- Prefer `diff` first unless the user explicitly says to apply immediately.
- Use explicit directions instead of guessing:
  - Claude -> Codex: `claude-codex-sync sync --from claude --to codex --scope all`
  - Codex -> Claude: `claude-codex-sync sync --from codex --to claude --scope all`
- On apply, add `--apply`.
- If the command reports unsupported items, summarize them instead of hiding them.

Status and diagnostics:
- `claude-codex-sync status --scope all`
- `claude-codex-sync doctor --scope all`

If the global `claude-codex-sync` wrapper is unavailable, resolve this skill's bundled script and run it directly:
- `python3 scripts/claude-codex-sync.py sync --from claude --to codex --scope all`
- `python3 scripts/claude-codex-sync.py sync --from codex --to claude --scope all`
