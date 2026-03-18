#!/usr/bin/env python3

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = REPO_ROOT / "skills"
ROOT_README = REPO_ROOT / "README.md"
REQUIRED_FILES = ("README.md", "SKILL.md", "install.sh")
OPTIONAL_FILES = ("install.ps1",)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate that skills in Skill Foundry follow the repository layout rules.",
    )
    parser.add_argument(
        "skills",
        nargs="*",
        help="Optional skill names to validate. Defaults to every directory under skills/.",
    )
    return parser.parse_args()


def list_skill_dirs(selected: list[str]) -> list[Path]:
    if selected:
        skill_dirs = [SKILLS_DIR / name for name in selected]
    else:
        skill_dirs = sorted(path for path in SKILLS_DIR.iterdir() if path.is_dir())
    return skill_dirs


def validate_skill_dir(skill_dir: Path) -> list[str]:
    errors: list[str] = []
    skill_name = skill_dir.name

    if not skill_dir.exists():
        return [f"{skill_name}: skill directory does not exist"]

    for filename in REQUIRED_FILES:
        path = skill_dir / filename
        if not path.is_file():
            errors.append(f"{skill_name}: missing required file {path.relative_to(REPO_ROOT)}")

    install_sh = skill_dir / "install.sh"
    if install_sh.exists() and not os.access(install_sh, os.X_OK):
        errors.append(f"{skill_name}: install.sh is not executable")

    for filename in OPTIONAL_FILES:
        path = skill_dir / filename
        if path.exists() and not path.is_file():
            errors.append(f"{skill_name}: optional path must be a file: {path.relative_to(REPO_ROOT)}")

    if ROOT_README.exists():
        readme_text = ROOT_README.read_text(encoding="utf-8")
        if f"`{skill_name}`" not in readme_text or f"skills/{skill_name}" not in readme_text:
            errors.append(f"{skill_name}: root README.md does not document this skill")
    else:
        errors.append("README.md is missing at repository root")

    return errors


def main() -> int:
    args = parse_args()

    if not SKILLS_DIR.is_dir():
        print(f"Error: skills directory does not exist: {SKILLS_DIR}", file=sys.stderr)
        return 1

    skill_dirs = list_skill_dirs(args.skills)
    if not skill_dirs:
        print("Error: no skill directories found", file=sys.stderr)
        return 1

    all_errors: list[str] = []
    for skill_dir in skill_dirs:
        all_errors.extend(validate_skill_dir(skill_dir))

    if all_errors:
        print("Skill layout validation failed:", file=sys.stderr)
        for error in all_errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    validated = ", ".join(path.name for path in skill_dirs)
    print(f"Skill layout validation passed: {validated}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
