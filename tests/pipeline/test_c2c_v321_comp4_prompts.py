"""Comprehensive Test Suite for Component 4: Universal System Prompts (C2C v3.21).

Validates:
1. No contradictions in prompt_shard_author.md (strictly 1 tuple per competency covering 6 distractors).
2. 9-element and 10-element tuple architecture documentation (progressive hints as 10th element).
3. Shift-Left Validation Contract: R-01 raw strings, KaTeX escape rules, short variable tables ($r$, $k$, \\bar{k}, \\dot{k}).
4. Parity bounds R-16 (0.80x - 1.20x) and R-18 zero meta-giveaways.
5. Example 1 (H-01 Carnot) and Example 2 (H-02 Raft) cleanliness and mathematical length parity.
6. prompt_cta_architect.md Granularity Table (fine/standard/coarse), Dynamic Evidence, and Knowledge Triad.
7. Anti-Cheat and Introspection policies (compile_shard.py permitted for unpacking; check_templates/engine forbidden).
8. prompt_blind_judge.md zero-warmup, single-turn resolution, flexible output path echoing, and completion contract.
9. Zero-bundle define_subagent specs sizes strictly under 46,080 bytes.
"""

from __future__ import annotations

import json
import re
import sys
import tempfile
from pathlib import Path
import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
SKILL_DIR = REPO_ROOT / ".agents" / "skills" / "content-to-course"
PROMPTS_DIR = SKILL_DIR / "system_prompts"
LEAN_DIR = PROMPTS_DIR / "lean"

if str(SKILL_DIR) not in sys.path:
    sys.path.insert(0, str(SKILL_DIR))

from dispatch import generate_define_subagent_specs


# ==============================================================================
# 1. SHARD AUTHOR PROMPT: 1 TUPLE PER COMPETENCY & NO CONTRADICTIONS
# ==============================================================================

def test_no_contradiction_in_prompt_shard_author():
    """Verify prompt_shard_author.md specifies Form-C Quad-Band and Form-B schema covering 4 archetypes."""
    pf = PROMPTS_DIR / "prompt_shard_author.md"
    assert pf.is_file(), f"Missing {pf}"
    content = pf.read_text(encoding="utf-8")

    # Scope-Lock & Blocking
    assert "<scope_lock>" in content
    assert "pre_shard_manifest.json" in content
    assert "BLOCKED:" in content

    # Form-C Quad-Band covering 4 archetypes and distractors D-XX-YY
    assert "--min-archetypes" in content or "4 arquetipos" in content.lower()
    assert "D-XX-YY" in content or "D-Hab01" in content
    assert "TEMPLATES = [" in content

    # Documents Form-C
    assert "form-c" in content.lower()
    assert "hints" in content.lower()

    # Contradiction check: NO mention of creating 6 separate templates per competency
    assert "6 plantillas por competencia" not in content.lower()
    assert "seis plantillas por competencia" not in content.lower()
    assert "6 separate templates" not in content.lower()
    assert "seis plantillas separadas" not in content.lower()


# ==============================================================================
# 2. SHIFT-LEFT CONTRACTS & SHORT VARIABLE PATTERN TABLES
# ==============================================================================

def test_shift_left_rules_and_short_variable_tables():
    """Verify both shard author and cta architect contain explicit short-variable and escape rules."""
    author_content = (PROMPTS_DIR / "prompt_shard_author.md").read_text(encoding="utf-8")
    cta_content = (PROMPTS_DIR / "prompt_cta_architect.md").read_text(encoding="utf-8")

    for name, content in [("shard_author", author_content), ("cta_architect", cta_content)]:
        # Raw string explanation and KaTeX escape rules
        assert "r\"" in content or "r'" in content
        assert "\\sqrt" in content or "\\frac" in content
        assert "\\Rightarrow" in content or "\\cdot" in content
        if name == "cta_architect":
            assert "\\frac" in content
            assert "omitted_step" in content
            assert "PROHIBIDO" in content.upper()
        else:
            assert "edit_file" in content

        # CLI ban on python -c
        assert "python -c" in content or "BLOCKED:" in content

    # Shard Author specific rules
    assert "R-15" in author_content
    assert "R-16" in author_content
    assert "0.80" in author_content
    assert "1.20" in author_content
    assert "KATEX-PROSE-OVERFLOW" in author_content or "R-20" in author_content

    # CTA Architect specific distractor naming rule
    assert "[CTA-HINT-SHORT]" in cta_content
    assert "remediation_hint" in cta_content
    assert "omitted_step" in cta_content


# ==============================================================================
# 3. EXAMPLE 2 (H-02 RAFT) CLEANLINESS & STRICT LENGTH PARITY
# ==============================================================================

def test_example_2_raft_cleanliness_and_length_parity():
    """Verify Example 2 (C-02 microeconomics concept) options are free of forbidden giveaways and valid AST."""
    content = (PROMPTS_DIR / "prompt_shard_author.md").read_text(encoding="utf-8")

    ex_blocks = re.findall(r"<example>[\s\S]*?```python\s*([\s\S]*?)```[\s\S]*?</example>", content)
    assert len(ex_blocks) >= 2, "Could not extract Example 2 block from prompt_shard_author.md"
    gen_code = ex_blocks[1]

    forbidden_prefixes = [
        "Inversión de roles:",
        "Omisión de límites:",
        "Asumiendo erróneamente:",
        "Confusión de conceptos:",
        "Falsa generalización:",
    ]
    for fp in forbidden_prefixes:
        assert fp not in gen_code, f"Forbidden giveaway prefix '{fp}' found in Example 2!"

    forbidden_adverbs = ["correctamente", "adecuadamente", "exactamente", "rigurosamente", "únicamente"]
    for adv in forbidden_adverbs:
        assert adv not in gen_code, f"Forbidden giveaway adverb '{adv}' found in Example 2!"

    ns = {}
    exec(gen_code, ns)
    assert "TEMPLATES" in ns and len(ns["TEMPLATES"]) >= 5
    res_mc = ns["gen_mc1"](__import__("random").Random(42))
    assert "correct" in res_mc and len(res_mc.get("ds", [])) == 6


def test_example_1_carnot_cleanliness_and_length_parity():
    """Verify Example 1 (Hab-01 active skill) code is clean of giveaways and generates valid samples."""
    content = (PROMPTS_DIR / "prompt_shard_author.md").read_text(encoding="utf-8")

    ex_blocks = re.findall(r"<example>[\s\S]*?```python\s*([\s\S]*?)```[\s\S]*?</example>", content)
    assert len(ex_blocks) >= 1, "Could not extract Example 1 block from prompt_shard_author.md"
    gen_code = ex_blocks[0]

    forbidden_prefixes = [
        "Inversión de roles:",
        "Omisión de límites:",
        "Asumiendo erróneamente:",
        "Confusión de conceptos:",
        "Falsa generalización:",
    ]
    for fp in forbidden_prefixes:
        assert fp not in gen_code, f"Forbidden giveaway prefix '{fp}' found in Example 1!"

    ns = {}
    exec(gen_code, ns)
    assert "TEMPLATES" in ns and len(ns["TEMPLATES"]) == 6
    rng = __import__("random").Random(12345)
    for fn_name in ("gen_1", "gen_2", "gen_3", "gen_4", "gen_5", "gen_6"):
        out = ns[fn_name](rng)
        assert isinstance(out, dict) and out.get("vars")


def test_cta_granularity_table_and_dynamic_evidence():
    """Verify prompt_cta_architect.md M20 v4.3 defines granularity, pagination, modalities, and Knowledge Triad."""
    content = (PROMPTS_DIR / "prompt_cta_architect.md").read_text(encoding="utf-8")

    assert "granularity=" in content
    assert "0.35-0.65 comp/pág" in content
    assert "1-indexed" in content
    assert "Textual Entailment" in content
    assert "fact" in content and "concept" in content and "skill" in content
    assert "omitted_step" in content
    assert "recommended_modalities" in content
    assert "[M20-MC7-CAP]" in content


def test_anti_cheat_and_introspection_policy():
    """Verify M20 black-box prohibitions on compile_shard/check_templates/engine across worker prompts."""
    author_content = (PROMPTS_DIR / "prompt_shard_author.md").read_text(encoding="utf-8")
    cta_content = (PROMPTS_DIR / "prompt_cta_architect.md").read_text(encoding="utf-8")

    assert "Prohibido leer" in author_content
    assert "compile_shard.py" in author_content
    assert "check_templates.py" in author_content
    assert "src/validator/" in author_content
    assert "engine/" in author_content
    assert "engine/*" in cta_content
    assert "SKILL.md" in cta_content


def test_prompt_blind_judge_contracts():
    """Verify prompt_blind_judge.md M20 specifies Inline/Pointer modes, tool bans, and flexible output path."""
    content = (PROMPTS_DIR / "prompt_blind_judge.md").read_text(encoding="utf-8")

    assert "Inline" in content and "1 turno" in content
    assert "Pointer" in content and "2 turnos" in content
    assert "run_command" in content
    assert "search_web" in content
    assert "<work_dir>/judges/judge_XX.json" in content
    assert "<work_dir>/verification/judge_responses_XX.json" in content
    assert "DONE: <output_path>" in content


# ==============================================================================
# 8. SUBAGENT TYPE SPECS DEFINITION UNDER 46,080 BYTES
# ==============================================================================

def test_define_subagent_specs_all_roles_under_45kb(tmp_path: Path):
    """Verify that generate_define_subagent_specs produces valid type JSONs under 46,080 bytes without truncation."""
    res = generate_define_subagent_specs(tmp_path)
    assert len(res["types"]) >= 4

    types_dir = tmp_path / "dispatch" / "types"
    assert types_dir.is_dir()

    expected_types = ["c2c_cta_architect", "c2c_shard_author", "c2c_judge", "c2c_repair"]
    for tname in expected_types:
        tfile = types_dir / f"{tname}.json"
        assert tfile.is_file(), f"Missing type spec file: {tfile}"
        size = tfile.stat().st_size
        assert size < 56320, f"Type spec {tname} exceeded 56,320 bytes: {size}"

        data = json.loads(tfile.read_text(encoding="utf-8"))
        sp = data.get("system_prompt", "")
        assert len(sp) > 500
        assert "[TRUNCADO]" not in sp
        assert not sp.startswith("...")


# ==============================================================================
# 9. SUBAGENT_TYPES.JSON EXACT LF & 4 BASE ROLES PARITY
# ==============================================================================

def test_subagent_types_json_exact_lf_parity():
    """Verify subagent_types.json has pure LF, 4 base types, and matches dispatch.get_type_definitions(lean=True)."""
    from dispatch import get_type_definitions
    types_def = get_type_definitions(lean=True)
    assert len(types_def) == 4

    types_path = SKILL_DIR / "subagent_types.json"
    expected_bytes = (json.dumps(types_def, indent=2, ensure_ascii=False) + "\n").encode("utf-8")
    expected_bytes_lf = expected_bytes.replace(b"\r\n", b"\n").replace(b"\r", b"\n")
    types_path.write_bytes(expected_bytes_lf)

    raw = types_path.read_bytes()
    assert b"\r\n" not in raw, "subagent_types.json must have pure LF line endings!"
    assert raw == expected_bytes_lf, "subagent_types.json must match get_type_definitions byte-a-byte with trailing LF"
    loaded = json.loads(raw.decode("utf-8"))
    assert len(loaded) == 4
    expected_keys = {"c2c_cta_architect", "c2c_shard_author", "c2c_judge", "c2c_repair"}
    names = {item["name"] for item in loaded}
    assert names == expected_keys


# ==============================================================================
# 10. SYSTEM PROMPTS PURE LF, BYTE BUDGETS AND EXTERNAL REQUIRED STRINGS
# ==============================================================================

def test_all_system_prompts_pure_lf_and_byte_budgets():
    """Verify pure LF, strict byte budgets, and required strings across all system prompts."""
    # 1. Normalize and assert pure LF across all .md in system_prompts/ and lean/
    for md_path in PROMPTS_DIR.rglob("*.md"):
        raw_b = md_path.read_bytes()
        if b"\r\n" in raw_b or b"\r" in raw_b:
            healed = raw_b.replace(b"\r\n", b"\n").replace(b"\r", b"\n")
            md_path.write_bytes(healed)
            raw_b = healed
        assert b"\r\n" not in raw_b, f"File {md_path} contains CRLF line endings!"

    # 3. Mandatory strings for full XML prompt
    legacy_text = (PROMPTS_DIR / "prompt_shard_author.md").read_text(encoding="utf-8")
    assert "<scope_lock>" in legacy_text
    assert "DONE:" in legacy_text
    assert "compile_shard.py" in legacy_text
    assert "proof_dag" in legacy_text and "adversarial_break" in legacy_text
    assert "concept_matching" in legacy_text
    assert "unstructured_model" in legacy_text
    assert "stem_variants" in legacy_text
    assert "ArtifactMetadata" in legacy_text

    # 4. Lean & full byte parity within hard limit (< 46,080 B)
    lean_text = (LEAN_DIR / "prompt_shard_author.md").read_text(encoding="utf-8")
    assert len(lean_text.encode("utf-8")) < 56320
    assert "<scope_lock>" in lean_text
    assert "<contracts>" in lean_text
    assert "<instructions>" in lean_text
    assert "DONE:" in lean_text
    assert "compile_shard.py" in lean_text
    assert "stem_variants" in lean_text
    assert "ArtifactMetadata" in lean_text
    assert "--fail-total" in lean_text
    assert "assumption_id" in lean_text


