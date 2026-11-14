"""Contract tests for Milestone 9 platform hierarchy, Content Core drawer, and M1/M6/M14 preservation."""
from __future__ import annotations

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
PLATFORM_SRC = REPO_ROOT / "platform" / "src"

TYPES_TS = PLATFORM_SRC / "types.ts"
HIERARCHY_ADAPTER_TS = PLATFORM_SRC / "utils" / "hierarchyAdapter.ts"
CONTENT_CORE_DRAWER_TSX = PLATFORM_SRC / "components" / "ContentCoreDrawer.tsx"
MASTERY_GRID_TSX = PLATFORM_SRC / "components" / "MasteryGrid.tsx"
COURSE_OVERVIEW_TSX = PLATFORM_SRC / "components" / "CourseOverview.tsx"
SIDEBAR_TSX = PLATFORM_SRC / "components" / "Sidebar.tsx"


def _strip_ts_comments(source: str) -> str:
    """Remove single-line and block comments so contract checks do not match dead comments."""
    no_block = re.sub(r"/\*[\s\S]*?\*/", "", source)
    return re.sub(r"//.*", "", no_block)


def _extract_interface_body(source: str, interface_name: str) -> str:
    pattern = re.compile(rf"export\s+interface\s+{re.escape(interface_name)}\s*\{{")
    match = pattern.search(source)
    assert match is not None, f"Missing exported interface '{interface_name}' in types.ts"
    start = match.end()
    depth = 1
    idx = start
    while idx < len(source) and depth > 0:
        ch = source[idx]
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
        idx += 1
    assert depth == 0, f"Unbalanced braces for interface '{interface_name}'"
    return source[start : idx - 1]


def test_types_ts_defines_m9_hierarchy_interfaces() -> None:
    raw = _strip_ts_comments(TYPES_TS.read_text(encoding="utf-8"))

    for iface in (
        "ExplicitAssumption",
        "ContentGlossaryTerm",
        "ContentCore",
        "SubtopicUnit",
        "ContentModule",
    ):
        _extract_interface_body(raw, iface)

    core_body = _extract_interface_body(raw, "ContentCore")
    for field in (
        "intuitive_analogy",
        "governing_theorems_and_assumptions",
        "worked_example",
        "common_exam_pitfalls",
    ):
        assert re.search(rf"\b{field}\b", core_body), (
            f"ContentCore missing required field '{field}'"
        )

    module_body = _extract_interface_body(raw, "ContentModule")
    for field in ("core", "source_file", "content_challenge_pool"):
        assert re.search(rf"\b{field}\b", module_body), (
            f"ContentModule missing required field '{field}'"
        )


def test_hierarchy_adapter_exports_resolve_course_modules() -> None:
    raw = _strip_ts_comments(HIERARCHY_ADAPTER_TS.read_text(encoding="utf-8"))
    assert re.search(r"export\s+function\s+resolveCourseModules\s*\(", raw), (
        "hierarchyAdapter.ts must export resolveCourseModules"
    )


def test_m9_components_preserve_testids_and_expose_m9_badges() -> None:
    drawer_src = _strip_ts_comments(CONTENT_CORE_DRAWER_TSX.read_text(encoding="utf-8"))
    grid_src = _strip_ts_comments(MASTERY_GRID_TSX.read_text(encoding="utf-8"))
    overview_src = _strip_ts_comments(COURSE_OVERVIEW_TSX.read_text(encoding="utf-8"))
    sidebar_src = _strip_ts_comments(SIDEBAR_TSX.read_text(encoding="utf-8"))

    # ContentCoreDrawer contract
    for testid in (
        'data-testid="content-core-drawer"',
        'data-testid="content-core-close"',
        'data-testid="tab-khanmigo-blocks"',
        'data-testid="tab-module-glossary"',
    ):
        assert testid in drawer_src, f"ContentCoreDrawer.tsx missing {testid}"

    # CourseOverview preserves M1/M6/M14 testids and exposes open-content-core-
    for testid in (
        'data-testid="sticky-completion-bar"',
        'data-testid="up-next-banner"',
        'data-testid="completion-tracker-summary"',
        'data-testid="course-progress-bar-overview"',
        'data-testid="course-challenge-card"',
    ):
        assert testid in overview_src, f"CourseOverview.tsx missing preserved {testid}"
    assert "open-content-core-" in overview_src, (
        "CourseOverview.tsx must expose open-content-core- trigger"
    )
    assert "module-header-" in overview_src, (
        "CourseOverview.tsx must expose module-header- testid"
    )

    # MasteryGrid preserves M1/M6/M14 testids and exposes PRE-XX / evidence / assumptions badges
    for marker in (
        "competency-block-${unit.id}",
        "unit-status-${unit.id}",
        "competency-${unit.id}",
        "quiz-marker-${unit.id}",
        "unit-test-marker-${unit.id}",
        "prereq-badge-${unit.id}",
        "evidence-badge-${unit.id}",
        "assumptions-toggle-${unit.id}",
    ):
        assert marker in grid_src, f"MasteryGrid.tsx missing {marker}"
    assert "PRE-" in grid_src, "MasteryGrid.tsx must detect PRE- prerequisites"

    # Sidebar preserves M1/M6/M14 testids and exposes PRE-XX / evidence badges
    for marker in (
        'data-testid="sidebar"',
        'data-testid="sidebar-toggle"',
        "sidebar-unit-status-${unit.id}",
        "sidebar-prereq-badge-${unit.id}",
    ):
        assert marker in sidebar_src, f"Sidebar.tsx missing {marker}"
    assert "PRE-" in sidebar_src, "Sidebar.tsx must detect PRE- prerequisites"
    assert "firstEvidence" in sidebar_src or "evidence" in sidebar_src, (
        "Sidebar.tsx must render evidence indicator"
    )


def test_m9_components_do_not_force_whitespace_normal_on_katex() -> None:
    for path in (
        CONTENT_CORE_DRAWER_TSX,
        MASTERY_GRID_TSX,
        COURSE_OVERVIEW_TSX,
        SIDEBAR_TSX,
    ):
        src = _strip_ts_comments(path.read_text(encoding="utf-8"))
        assert not re.search(r"white-space\s*:\s*normal", src, re.IGNORECASE), (
            f"{path.name} must not force white-space: normal (breaks KaTeX rendering)"
        )
        assert not re.search(r"\.katex[^\n]*whitespace-normal", src), (
            f"{path.name} must not apply whitespace-normal to .katex"
        )
