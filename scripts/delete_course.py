#!/usr/bin/env python3
"""Convenience CLI forwarder for the delete-course skill.
Delegates directly to .agents/skills/delete-course/scripts/delete_course.py
"""
import sys
from pathlib import Path

SKILL_SCRIPT = Path(__file__).resolve().parent.parent / ".agents" / "skills" / "delete-course" / "scripts" / "delete_course.py"

if not SKILL_SCRIPT.is_file():
    print(f"Error: Engine script not found at {SKILL_SCRIPT}", file=sys.stderr)
    sys.exit(1)

# Execute engine
import importlib.util
spec = importlib.util.spec_from_file_location("delete_course_engine", SKILL_SCRIPT)
mod = importlib.util.module_from_spec(spec)
sys.modules["delete_course_engine"] = mod
spec.loader.exec_module(mod)

if __name__ == "__main__":
    mod.main()
