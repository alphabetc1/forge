# Skill Foundry Repo Rules

This repository is a skill monorepo.

When you add or update a skill in this repository, you must follow these rules:

## Required layout

1. Create the skill under `skills/<name>/`.
2. Add at least:
   - `README.md`
   - `SKILL.md`
   - `install.sh`
3. If the skill should support native PowerShell installation, also add `install.ps1`.
4. Keep scripts, assets, examples, references, docs, and any other skill-specific files inside that skill's own directory.
5. Do not place skill-specific files at the repository root.

## Discovery rules

1. The root installers auto-discover installable skills from `skills/*/install.sh` and `skills/*/install.ps1`.
2. Do not add manual registration code to the root installers just to make a new skill discoverable.
3. Ensure `skills/<name>/install.sh` is executable, otherwise the root Bash installer will not list or install the skill.

## Documentation rules

1. Update the root `README.md` when a new skill is added.
2. Add the new skill to the root skills table.
3. Add a detailed section for the new skill if it is intended to be user-facing.

## Behavior rules for agents

1. If a requested skill does not fit this repository layout, stop and explain the conflict instead of inventing a new structure.
2. Prefer small, repo-consistent changes over creating parallel conventions.
3. Before finishing, run:

```bash
python scripts/validate_skill_layout.py
```

Or validate a single skill:

```bash
python scripts/validate_skill_layout.py <name>
```
