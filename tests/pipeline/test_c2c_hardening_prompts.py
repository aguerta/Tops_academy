"""Regression tests for Stream 2B forensic hardening of lean system prompts and SKILL.md."""

from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SKILL_DIR = REPO_ROOT / ".agents" / "skills" / "content-to-course"
LEAN_DIR = SKILL_DIR / "system_prompts" / "lean"
SKILL_MD = SKILL_DIR / "SKILL.md"


def test_lean_prompt_shard_author_hardening():
    """Verify explicit compile_shard.py path, epistemic completeness, pre-compile check, and batching/DONE rules."""
    content = (LEAN_DIR / "prompt_shard_author.md").read_text(encoding="utf-8")

    # 1A: Explicit relative path in <instructions>
    assert ".agents/skills/content-to-course/compile_shard.py" in content

    # 1B: Epistemic self-contained rule in <contracts>
    assert "EPISTEMIC-SELF-CONTAINED" in content
    assert "stem_variants" in content

    # 1C: Compact Pre-Compile Check in <contracts>
    assert "PRE-COMPILE CHECK" in content
    assert 'r"..."' in content
    assert "@var@" in content
    assert "[R-15]" in content and "[R-16]" in content

    # 1D: Atomic edit_file batching and background compile DONE prohibition in <error_recovery>
    assert "edit_file" in content
    assert "en un solo turno paralelo" in content
    assert "Prohibido emitir `DONE:` mientras un `run_command` de compilación siga ejecutándose en segundo plano" in content


def test_lean_prompt_repair_hardening():
    """Verify Epistemic Sweep and Windows PowerShell Unix-command ban in prompt_repair.md."""
    raw = (LEAN_DIR / "prompt_repair.md").read_bytes()
    assert b"\r\n" not in raw, "prompt_repair.md must maintain pure LF line endings"
    content = raw.decode("utf-8")

    # 2A: Epistemic Sweep (M20 parameterized archetypes)
    assert "Epistemic Sweep" in content
    assert "<<S4_MIN_ARCH>>" in content or "4/4" in content

    # 2B: Ban Unix commands on Windows PowerShell
    for cmd in ("`rg`", "`grep`", "`awk`", "`sed`"):
        assert cmd in content
    assert "line_range" in content


def test_lean_prompt_cta_architect_doc_name_rule():
    """Verify element 5: doc must use original manifest PDF name, never internal slice name."""
    raw = (LEAN_DIR / "prompt_cta_architect.md").read_bytes()
    assert b"\r\n" not in raw, "prompt_cta_architect.md must maintain pure LF line endings"
    content = raw.decode("utf-8")

    assert "5: doc" in content
    assert "*_part_XX.pdf" in content
    assert "PDF fuente original" in content


def test_skill_md_workflow_absolute_path_and_repair_rejudge():
    """Verify SKILL.md uses <workflow_script_path> from bootstrap and repair_and_rejudge / no concurrent rejudge-compare."""
    content = SKILL_MD.read_text(encoding="utf-8")

    # 4A: No relative ScriptPath for c2c_wave_workflow.py
    assert 'ScriptPath=".agents/skills/content-to-course/workflows/c2c_wave_workflow.py"' not in content
    assert "<workflow_script_path absoluto devuelto por --stage bootstrap>" in content

    # 4B: mode="repair_and_rejudge" and rejudge-compare guard
    assert 'mode="repair_and_rejudge"' in content or "repair_and_rejudge" in content
    assert "rejudge-compare" in content
    assert "mientras una tarea `run_workflow` siga activa en segundo plano" in content
