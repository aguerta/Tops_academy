"""Verification Suite for C2C v3.3 Pipeline Prompts and Skill Alignment.

Validates:
1. Lean system prompts size limits (strictly <= 5,120 bytes, with author lean <= 4,750 bytes).
2. Elimination of rf" / fr" / {{{ in code blocks, presence of PrairieLearn @var@ tokens,
   stem_variants, shard_fixes/, and ArtifactMetadata prohibition.
3. Programmatic extraction and full end-to-end dry-run execution of Python template examples in prompt_shard_author.md
   (Full and Lean) through check_templates.check_single_template with 50 seeds, asserting errors == [].
4. Parity of compile_shard.py read prohibition with c2c_hook_guard.py and ROLE_SPECS v3.3.
5. Harmonized Pointer Mode in prompt_blind_judge.md (2-turn contract) and Inline Mode (1-turn resolution)
   without contradiction, plus ArtifactMetadata prohibition across all worker prompts.
6. SKILL.md v3.3 documentation compliance (Fast Bootstrap, director-id, Silent Reactive Barrier,
   weighted waves, shard_fixes, c2c_repair).
"""

from __future__ import annotations

import ast
import json
import re
import sys
from pathlib import Path
import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILL_DIR = REPO_ROOT / ".agents" / "skills" / "content-to-course"
PROMPTS_DIR = SKILL_DIR / "system_prompts"
LEAN_DIR = PROMPTS_DIR / "lean"

if str(SKILL_DIR) not in sys.path:
    sys.path.insert(0, str(SKILL_DIR))

from check_templates import check_single_template
from engine.assemble import assemble_question, format_template_string
from engine.invariants import check_instance_invariants
from engine.instantiate import instantiate_template


# ==============================================================================
# 1. LEAN PROMPTS SIZE LIMIT (<= 5,120 BYTES & AUTHOR LEAN <= 4,750 BYTES)
# ==============================================================================

def test_all_lean_prompts_under_5kb():
    """Verify all lean static system prompts are strictly <= 5,120 bytes."""
    assert LEAN_DIR.is_dir(), f"Missing lean directory: {LEAN_DIR}"
    lean_files = list(LEAN_DIR.glob("*.md"))
    assert len(lean_files) >= 3, f"Expected at least 3 lean prompts, found {len(lean_files)}"

    for lf in lean_files:
        size = lf.stat().st_size
        assert size <= 5120, (
            f"Lean prompt {lf.name} exceeded 5,120 bytes! Size: {size} bytes ({size - 5120} bytes over)"
        )


def test_lean_author_prompt_headroom_under_4750_bytes():
    """Verify lean/prompt_shard_author.md has comfortable headroom (strictly <= 4,750 bytes)."""
    pfile = LEAN_DIR / "prompt_shard_author.md"
    assert pfile.is_file(), f"Missing {pfile}"
    size = pfile.stat().st_size
    assert size <= 4750, (
        f"lean/prompt_shard_author.md exceeded tightened target of 4,750 bytes! Size: {size} bytes"
    )


# ==============================================================================
# 2. CODE BLOCKS: ZERO rf"/{{{ AND PRESENCE OF PRAIRIELEARN CONTRACT
# ==============================================================================

def _extract_code_blocks(markdown_text: str) -> list[str]:
    """Extract code blocks fenced with ```python or ``` from markdown."""
    pattern = re.compile(r"```(?:python)?\s*([\s\S]*?)```", re.IGNORECASE)
    return [m.group(1) for m in pattern.finditer(markdown_text)]


def test_no_rf_or_triple_braces_in_author_prompts():
    """Verify zero occurrences of rf\" or fr\" or {{{ in code blocks of prompt_shard_author.md."""
    for is_lean, pfile in [
        (False, PROMPTS_DIR / "prompt_shard_author.md"),
        (True, LEAN_DIR / "prompt_shard_author.md"),
    ]:
        assert pfile.is_file(), f"Missing prompt file: {pfile}"
        content = pfile.read_text(encoding="utf-8")
        code_blocks = _extract_code_blocks(content)
        assert len(code_blocks) > 0, f"No code blocks found in {pfile.name}"

        for b_idx, block in enumerate(code_blocks):
            # Check for banned rf" or fr" prefixes in string literals
            banned_rf_matches = re.findall(r"\b(?:rf|fr)[\'\"]", block, re.IGNORECASE)
            assert not banned_rf_matches, (
                f"Banned rf\"/fr\" literal found in {pfile.name} (code block {b_idx}): {banned_rf_matches}"
            )

            # Check for triple curly braces {{{ in code blocks
            assert "{{{" not in block, (
                f"Banned triple curly braces '{{{{{{' found in {pfile.name} (code block {b_idx})"
            )


def test_author_prompts_prairielearn_and_hardening_tokens():
    """Verify presence of @ PrairieLearn tokens, stem_variants, shard_fixes/, and ArtifactMetadata prohibition."""
    for is_lean, pfile in [
        (False, PROMPTS_DIR / "prompt_shard_author.md"),
        (True, LEAN_DIR / "prompt_shard_author.md"),
    ]:
        content = pfile.read_text(encoding="utf-8")
        # PrairieLearn tokens
        assert "@var@" in content or "@var:fmt@" in content or "@th@" in content
        # stem_variants
        assert "stem_variants" in content
        # modular fixes
        assert "shard_fixes/" in content or "shard_fixes" in content
        # ArtifactMetadata prohibition
        assert "ArtifactMetadata" in content
        assert "PROHIBIDO" in content or "NEVER" in content or "PROHIBITED" in content


# ==============================================================================
# 3. FULL DRY-RUN VALIDATION OF PROMPT EXAMPLES VIA check_single_template
# ==============================================================================

def test_execution_example_h01_full_author_prompt():
    """Extract and validate Example 1 (H-01 Carnot) through check_single_template (50 seeds, 0 errors)."""
    pf = PROMPTS_DIR / "prompt_shard_author.md"
    content = pf.read_text(encoding="utf-8")

    m_ex1 = re.search(r"### Ejemplo 1:[\s\S]*?```python\s*([\s\S]*?)```", content)
    assert m_ex1, "Failed to extract Example 1 code block from prompt_shard_author.md"
    code_ex1 = m_ex1.group(1).strip()

    ns = {}
    exec(code_ex1, ns)

    assert "gen_h01" in ns and "ver_h01" in ns and "TEMPLATES" in ns
    h01_tuple = ns["TEMPLATES"][0]
    stem_raw = h01_tuple[2]
    stems_list = [str(s) for s in stem_raw] if isinstance(stem_raw, (list, tuple)) else [str(stem_raw)]

    m_gen = re.search(r"def gen_h01\(rng\):[\s\S]*?(?=def ver_h01)", code_ex1)
    m_ver = re.search(r"def ver_h01\(res\):[\s\S]*?(?=TEMPLATES\s*=)", code_ex1)
    assert m_gen and m_ver

    gen_src = f"import random, math\n{m_gen.group(0).strip()}\ngenerate_params = gen_h01\ngenerate = gen_h01\n"
    ver_src = f"{m_ver.group(0).strip()}\nverify = ver_h01\ncross_check = ver_h01\n"

    tpl_dict = {
        "id": "T-H01",
        "template_id": "T-H01",
        "competency_id": "H-01",
        "interaction_type": "multiple_choice_7_options",
        "difficulty": "medium",
        "bloom": "Understand",
        "stem": stems_list[0],
        "stem_es": stems_list[0],
        "stem_variants": stems_list,
        "hints": list(h01_tuple[9]) if len(h01_tuple) >= 10 else ["Hint 1", "Hint 2", "Hint 3"],
        "solution": str(h01_tuple[5]),
        "distractor_ids": list(h01_tuple[7]),
        "generate_py": gen_src,
        "cross_check_py": ver_src,
    }

    # 1. Verification through engine.instantiate
    instantiated = instantiate_template(tpl_dict, "H-01", target_count=5, seed_offset=200)
    assert len(instantiated) == 5, f"Expected 5 instantiated questions, got {len(instantiated)}"

    for q in instantiated:
        is_valid, errs = check_instance_invariants(q, "multiple_choice_7_options")
        assert is_valid, f"Invariant validation failed on H-01: {errs}"
        assert len(q["options"]) == 7, "MC7 question must have exactly 7 options"
        assert "@" not in q["stem"], f"Unrendered @var@ in stem: {q['stem']}"
        for opt in q["options"]:
            assert "@" not in opt["content"], f"Unrendered @var@ in option: {opt['content']}"

    # 2. Strict verification through check_templates.check_single_template (50 dry-run seeds)
    declared_dids = set(h01_tuple[7])
    tpl_check_errors = check_single_template(
        template=tpl_dict,
        competency_id="H-01",
        declared_distractor_ids=declared_dids,
        num_dry_run_seeds=50,
    )
    assert tpl_check_errors == [], f"check_single_template failed on Full H-01: {tpl_check_errors}"


def test_execution_example_h02_full_author_prompt():
    """Extract and validate Example 2 (H-02 Raft) through check_single_template (50 seeds, 0 errors)."""
    pf = PROMPTS_DIR / "prompt_shard_author.md"
    content = pf.read_text(encoding="utf-8")

    m_gen = re.search(r"def gen_h02\(rng\):[\s\S]*?(?=def ver_h02)", content)
    m_ver = re.search(r"def ver_h02\(res\):[\s\S]*?(?=TEMPLATES\s*\+=)", content)
    m_tpl = re.search(r"TEMPLATES\s*\+=\s*\[([\s\S]*?)\]\n```", content)

    assert m_gen and m_ver and m_tpl, "Failed to extract H-02 code sections from prompt_shard_author.md"

    gen_raw = m_gen.group(0).strip()
    ver_raw = m_ver.group(0).strip()
    tpl_block = "TEMPLATES = [" + m_tpl.group(1).strip() + "]"

    ns = {}
    full_exec = f"import math, random\n{gen_raw}\n{ver_raw}\n{tpl_block}"
    exec(full_exec, ns)

    h02_tuple = ns["TEMPLATES"][0]
    stem_raw = h02_tuple[2]
    stems_list = [str(s) for s in stem_raw] if isinstance(stem_raw, (list, tuple)) else [str(stem_raw)]

    gen_src = f"import random, math\n{gen_raw}\ngenerate_params = gen_h02\ngenerate = gen_h02\n"
    ver_src = f"{ver_raw}\nverify = ver_h02\ncross_check = ver_h02\n"

    tpl_dict = {
        "id": "T-H02",
        "template_id": "T-H02",
        "competency_id": "H-02",
        "interaction_type": "multiple_choice_7_options",
        "difficulty": "medium",
        "bloom": "Understand",
        "stem": stems_list[0],
        "stem_es": stems_list[0],
        "stem_variants": stems_list,
        "hints": list(h02_tuple[9]) if len(h02_tuple) >= 10 else ["Hint 1", "Hint 2", "Hint 3"],
        "solution": str(h02_tuple[5]),
        "distractor_ids": list(h02_tuple[7]),
        "generate_py": gen_src,
        "cross_check_py": ver_src,
    }

    # 1. Verification through engine.instantiate
    instantiated = instantiate_template(tpl_dict, "H-02", target_count=5, seed_offset=500)
    assert len(instantiated) == 5, f"Expected 5 instantiated questions, got {len(instantiated)}"

    for q in instantiated:
        is_valid, errs = check_instance_invariants(q, "multiple_choice_7_options")
        assert is_valid, f"Invariant validation failed on H-02: {errs}"
        assert len(q["options"]) == 7, "MC7 question must have exactly 7 options"
        assert "@" not in q["stem"], f"Unrendered @var@ in stem: {q['stem']}"
        for opt in q["options"]:
            assert "@" not in opt["content"], f"Unrendered @var@ in option: {opt['content']}"

    # 2. Strict verification through check_templates.check_single_template (50 dry-run seeds)
    declared_dids = set(h02_tuple[7])
    tpl_check_errors = check_single_template(
        template=tpl_dict,
        competency_id="H-02",
        declared_distractor_ids=declared_dids,
        num_dry_run_seeds=50,
    )
    assert tpl_check_errors == [], f"check_single_template failed on Full H-02: {tpl_check_errors}"


def test_execution_example_lean_author_prompt():
    """Extract and validate H-01 template from Lean prompt_shard_author.md through check_single_template (50 seeds, 0 errors)."""
    pf = LEAN_DIR / "prompt_shard_author.md"
    content = pf.read_text(encoding="utf-8")

    m_code = re.search(r"```python\s*(import math[\s\S]*?)```", content)
    assert m_code, "Failed to extract python code block from lean prompt_shard_author.md"
    code_raw = m_code.group(1).strip()

    ns = {}
    exec(code_raw, ns)

    assert "gen_h01" in ns
    assert "ver_h01" in ns
    assert "TEMPLATES" in ns and len(ns["TEMPLATES"]) > 0

    h01_tuple = ns["TEMPLATES"][0]
    stem_raw = h01_tuple[2]
    stems_list = [str(s) for s in stem_raw] if isinstance(stem_raw, (list, tuple)) else [str(stem_raw)]

    m_gen = re.search(r"def gen_h01\(rng\):[\s\S]*?(?=def ver_h01)", code_raw)
    m_ver = re.search(r"def ver_h01\(res\):[\s\S]*?(?=TEMPLATES\s*=)", code_raw)
    assert m_gen and m_ver

    gen_src = f"import random, math\n{m_gen.group(0).strip()}\ngenerate_params = gen_h01\ngenerate = gen_h01\n"
    ver_src = f"{m_ver.group(0).strip()}\nverify = ver_h01\ncross_check = ver_h01\n"

    tpl_dict = {
        "id": "T-H01-LEAN",
        "template_id": "T-H01-LEAN",
        "competency_id": "H-01",
        "interaction_type": "multiple_choice_7_options",
        "difficulty": "medium",
        "bloom": "Understand",
        "stem": stems_list[0],
        "stem_es": stems_list[0],
        "stem_variants": stems_list,
        "hints": list(h01_tuple[9]),
        "solution": str(h01_tuple[5]),
        "distractor_ids": list(h01_tuple[7]),
        "generate_py": gen_src,
        "cross_check_py": ver_src,
    }

    # 1. Verification through engine.instantiate
    instantiated = instantiate_template(tpl_dict, "H-01", target_count=5, seed_offset=300)
    assert len(instantiated) == 5

    for q in instantiated:
        is_valid, errs = check_instance_invariants(q, "multiple_choice_7_options")
        assert is_valid, f"Lean H-01 invariant failure: {errs}"
        assert len(q["options"]) == 7
        assert "@" not in q["stem"]

    # 2. Strict verification through check_templates.check_single_template (50 dry-run seeds)
    declared_dids = set(h01_tuple[7])
    tpl_check_errors = check_single_template(
        template=tpl_dict,
        competency_id="H-01",
        declared_distractor_ids=declared_dids,
        num_dry_run_seeds=50,
    )
    assert tpl_check_errors == [], f"check_single_template failed on Lean H-01: {tpl_check_errors}"


# ==============================================================================
# 4. COMPILE_SHARD.PY READ PROHIBITION PARITY WITH HOOK GUARD
# ==============================================================================

def test_compile_shard_read_prohibition_parity():
    """Verify compile_shard.py is explicitly forbidden to read in prompt_shard_author.md (Full + Lean), matching c2c_hook_guard.py."""
    for is_lean, pfile in [
        (False, PROMPTS_DIR / "prompt_shard_author.md"),
        (True, LEAN_DIR / "prompt_shard_author.md"),
    ]:
        content = pfile.read_text(encoding="utf-8")

        # Must forbid reading compile_shard.py
        assert "compile_shard.py" in content
        assert "PROHIBIDO leer" in content or "FORBIDDEN to read" in content or "No scratch" in content

        # Verify compile_shard.py is NOT in READ section
        read_section_match = re.search(r"-\s*\*\*READ[^*]*\*\*:?(.*?)(?=-\s*\*\*WRITE|\Z)", content, re.DOTALL | re.IGNORECASE)
        assert read_section_match, f"Could not find READ section in {pfile.name}"
        read_section = read_section_match.group(1)
        assert "compile_shard.py" not in read_section, (
            f"compile_shard.py mistakenly declared in READ section of {pfile.name}!"
        )

        # Verification that full path is preserved for introspection policy tests
        if not is_lean:
            assert ".agents/skills/content-to-course/compile_shard.py" in content


# ==============================================================================
# 5. BLIND JUDGE: HARMONIZED POINTER 2-TURN & INLINE 1-TURN CONTRACTS
# ==============================================================================

def test_prompt_blind_judge_pointer_mode_and_zero_contradiction():
    """Verify prompt_blind_judge.md harmonizes Pointer Mode allowing assigned judge_XX.json while forbidding all other files."""
    for is_lean, pfile in [
        (False, PROMPTS_DIR / "prompt_blind_judge.md"),
        (True, LEAN_DIR / "prompt_blind_judge.md"),
    ]:
        content = pfile.read_text(encoding="utf-8")

        # Pointer item read authorized
        assert "judge_XX.json" in content
        assert "view_file" in content

        # Other internal files forbidden
        assert "cta.json" in content
        assert "templates" in content
        assert "shards" in content
        assert "judge_ground_truth.json" in content

        # Single-turn and completion signal
        assert "DONE:" in content
        assert "ArtifactMetadata" in content


def test_blind_judge_harmonized_pointer_two_turn_resolution():
    """Verify prompt_blind_judge.md (Full + Lean) delineates inline 1-turn vs pointer 2-turn resolution."""
    for is_lean, pfile in [
        (False, PROMPTS_DIR / "prompt_blind_judge.md"),
        (True, LEAN_DIR / "prompt_blind_judge.md"),
    ]:
        content = pfile.read_text(encoding="utf-8")

        # Inline mode: 1 turn
        assert "Zero-Warmup In-Prompt Payload" in content
        assert "RESOLUCIÓN EN 1 SOLO TURNO" in content

        # Pointer mode: 2 turns
        assert "Turno 1" in content or "Turn 1" in content
        assert "Turno 2" in content or "Turn 2" in content
        assert "send_message" in content


def test_artifact_metadata_prohibition_across_all_prompts():
    """Verify ArtifactMetadata is explicitly prohibited in all 6 worker prompt files."""
    prompts_to_check = [
        PROMPTS_DIR / "prompt_shard_author.md",
        LEAN_DIR / "prompt_shard_author.md",
        PROMPTS_DIR / "prompt_cta_architect.md",
        LEAN_DIR / "prompt_cta_architect.md",
        PROMPTS_DIR / "prompt_blind_judge.md",
        LEAN_DIR / "prompt_blind_judge.md",
    ]
    for pf in prompts_to_check:
        assert pf.is_file(), f"Missing prompt file: {pf}"
        content = pf.read_text(encoding="utf-8")
        assert "ArtifactMetadata" in content, f"Prompt {pf.name} missing explicit ArtifactMetadata prohibition!"


# ==============================================================================
# 6. SKILL.MD V3.3 RUNBOOK COMPLIANCE
# ==============================================================================

def test_skill_md_v33_architecture_and_director_diet():
    """Verify SKILL.md documents bootstrap SLA <= 90s, Silent Reactive Barrier, weighted waves, and diet rules."""
    skill_file = SKILL_DIR / "SKILL.md"
    assert skill_file.is_file(), f"Missing {skill_file}"
    content = skill_file.read_text(encoding="utf-8")

    # Fast Bootstrap
    assert "--stage bootstrap" in content
    assert "--director-id" in content

    # Silent Reactive Barrier Protocol
    assert "Silent Reactive Barrier" in content or "Barrera Reactiva Silenciosa" in content
    assert "k < N" in content or "k/N" in content

    # Weighted Waves & Sharding
    assert "--wave" in content
    assert "Hab-*" in content

    # Modular fixes & repair delegation
    assert "shard_fixes" in content
    assert "c2c_repair" in content

    # Lockfile release
    assert ".c2c_subagent_lock.json" in content
    assert "--stage unlock" in content

    # Zero legacy corpus.md
    assert "work/corpus.md" not in content
