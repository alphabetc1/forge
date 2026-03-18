#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import os
import sys
from pathlib import Path


CURRENT_PLATFORM_ENV = "CLAUDE_CODEX_SYNC_CURRENT_PLATFORM"
ROOT = Path(__file__).resolve().parents[1]


def detect_platform(skill_root: Path) -> str | None:
    parts = set(skill_root.parts)
    if ".claude" in parts:
        return "claude"
    if ".agents" in parts or ".codex" in parts:
        return "codex"
    return None


platform = detect_platform(ROOT)
if platform:
    os.environ.setdefault(CURRENT_PLATFORM_ENV, platform)

CLI_PATH = ROOT / "claude-codex-sync" / "cli.py"
SPEC = importlib.util.spec_from_file_location("claude_codex_sync_cli", CLI_PATH)
if SPEC is None or SPEC.loader is None:  # pragma: no cover
    raise ImportError(f"Unable to load CLI module from {CLI_PATH}")

MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)
main = MODULE.main


if __name__ == "__main__":
    raise SystemExit(main())
