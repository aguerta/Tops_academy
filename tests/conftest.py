"""Shared session-scoped fixtures for Top's Academy test suite (Milestone 7 Via B).

Caches parsed JSON objects and raw text of real published courses in courses/*.json
per worker session to eliminate redundant disk I/O and JSON deserialization across
admission, lexical, and KaTeX sanitization tests.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
COURSES_DIR = REPO_ROOT / "courses"

_RAW_COURSES_CACHE: dict[str, str] | None = None
_PARSED_COURSES_CACHE: dict[str, dict[str, Any]] | None = None


def get_cached_raw_courses() -> dict[str, str]:
    """Return mapping of filename -> raw UTF-8 text for all courses/*.json (cached per process)."""
    global _RAW_COURSES_CACHE
    if _RAW_COURSES_CACHE is None:
        _RAW_COURSES_CACHE = {}
        if COURSES_DIR.is_dir():
            for path in sorted(COURSES_DIR.glob("*.json")):
                if path.name.startswith("unit_test_dummy"):
                    continue
                try:
                    _RAW_COURSES_CACHE[path.name] = path.read_text(encoding="utf-8")
                except FileNotFoundError:
                    continue
    return _RAW_COURSES_CACHE


def get_cached_parsed_courses() -> dict[str, dict[str, Any]]:
    """Return mapping of filename -> parsed JSON dict for all courses/*.json (cached per process)."""
    global _PARSED_COURSES_CACHE
    if _PARSED_COURSES_CACHE is None:
        raw_map = get_cached_raw_courses()
        _PARSED_COURSES_CACHE = {name: json.loads(raw) for name, raw in raw_map.items()}
    return _PARSED_COURSES_CACHE


@pytest.fixture(scope="session")
def real_courses_raw() -> dict[str, str]:
    """Session-scoped fixture returning {filename: raw_json_str} for all published courses."""
    return get_cached_raw_courses()


@pytest.fixture(scope="session")
def real_courses_parsed() -> dict[str, dict[str, Any]]:
    """Session-scoped fixture returning {filename: parsed_dict} for all published courses."""
    return get_cached_parsed_courses()
