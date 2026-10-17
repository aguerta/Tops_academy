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

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILL_DIR = REPO_ROOT / ".agents" / "skills" / "content-to-course"
PROMPTS_DIR = SKILL_DIR / "system_prompts"

if str(SKILL_DIR) not in sys.path:
    sys.path.insert(0, str(SKILL_DIR))

from dispatch import generate_define_subagent_specs


# ==============================================================================
# 1. SHARD AUTHOR PROMPT: 1 TUPLE PER COMPETENCY & NO CONTRADICTIONS
# ==============================================================================

def test_no_contradiction_in_prompt_shard_author():
    """Verify prompt_shard_author.md specifies exactly 1 tuple per competency covering 6 distractors."""
    pf = PROMPTS_DIR / "prompt_shard_author.md"
    assert pf.is_file(), f"Missing {pf}"
    content = pf.read_text(encoding="utf-8")

    # Scope-Lock & Inversion
    assert "## 0. SCOPE-LOCK" in content
    assert "Load Inversion" in content
    assert "BLOCKER:: No existe pre_shard_manifest.json" in content

    # 1 tuple per competency covering 6 distractors D-XX-01..06
    assert "1 tupla paramétrica por competencia" in content.lower() or "1 tupla por competencia" in content.lower()
    assert "D-XX-01..06" in content
    assert "TEMPLATES = [" in content

    # Documents both 9-element and 10-element tuples
    assert "9 Elementos" in content or "9 elementos" in content
    assert "10 Elementos" in content or "10 elementos" in content
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
        assert "\\rho" in content
        assert "\\frac" in content
        assert "\\alpha" in content
        assert "\\beta" in content

        # Short variables table ($r$, $k$, \bar{k}, \dot{k})
        assert "$r$" in content
        assert "$k$" in content
        assert "\\bar" in content
        assert "\\dot" in content

        # Hybrid write protocol
        assert "Append=True" in content
        assert "replace_file_content" in content

        # CLI ban on python -c
        assert "python -c" in content
        assert "PROHIBIDO" in content

    # Shard Author specific rules
    assert "R-16" in author_content
    assert "0.80" in author_content
    assert "1.20" in author_content
    assert "R-18" in author_content
    assert "R-20" in author_content

    # CTA Architect specific distractor naming rule
    assert "R-18" in cta_content
    assert "omitted_step" in cta_content


# ==============================================================================
# 3. EXAMPLE 2 (H-02 RAFT) CLEANLINESS & STRICT LENGTH PARITY
# ==============================================================================

def test_example_2_raft_cleanliness_and_length_parity():
    """Verify Example 2 (H-02 Raft) options are free of forbidden giveaways and strictly satisfy length parity."""
    content = (PROMPTS_DIR / "prompt_shard_author.md").read_text(encoding="utf-8")

    # Locate Example 2 code block
    m = re.search(r"def gen_h02\(rng\):.*?(?=def ver_h02)", content, re.DOTALL)
    assert m is not None, "Could not extract gen_h02 block from prompt_shard_author.md"
    gen_code = m.group(0)

    # Cleanliness: zero forbidden prefix giveaways inside the code block
    forbidden_prefixes = [
        "Inversión de roles:",
        "Omisión de límites:",
        "Asumiendo erróneamente:",
        "Confusión de conceptos:",
        "Falsa generalización:",
    ]
    for fp in forbidden_prefixes:
        assert fp not in gen_code, f"Forbidden giveaway prefix '{fp}' found in gen_h02 code block!"

    # Cleanliness: zero forbidden giveaway adverbs in option strings
    forbidden_adverbs = ["correctamente", "adecuadamente", "exactamente", "rigurosamente", "únicamente"]
    for adv in forbidden_adverbs:
        assert adv not in gen_code, f"Forbidden giveaway adverb '{adv}' found in gen_h02 code block!"

    # Rigorous Mathematical Parity across all possible cluster sizes
    nodes_test_cases = [5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31, 33, 35, 37, 39, 41, 43, 45, 47, 49, 51]
    for nodes in nodes_test_cases:
        f_max = (nodes - 1) // 2
        quorum = (nodes // 2) + 1
        f_sub = max(1, f_max - 2)

        correct_str = f"Quórum mayoritario de $Q = {quorum}$ nodos tolerando hasta $f = {f_max}$ caídas simultáneas"
        distractors = [
            f"Quórum minoritario de $Q = {f_max}$ nodos tolerando hasta $f = {quorum}$ caídas simultáneas",
            f"Consenso estricto de $Q = {nodes - 1}$ nodos tolerando a lo sumo $f = 1$ fallo de red",
            f"Quórum mayoritario de $Q = {quorum}$ nodos sobreestimando la tolerancia a $f = {nodes - 1}$ nodos",
            f"Quórum sobredimensionado de $Q = {quorum + 2}$ nodos reduciendo la tolerancia a $f = {f_sub}$ caídas",
            f"Quórum par de mitad exacta $Q = {nodes // 2}$ nodos expuesto a particiones de split-brain",
            f"Unanimidad absoluta de $Q = {nodes}$ nodos perdiendo toda tolerancia ante fallos con $f = 0$",
        ]

        c_len = len(correct_str)
        d_lens = [len(d) for d in distractors]
        min_d = min(d_lens)
        max_d = max(d_lens)
        avg_d = sum(d_lens) / len(d_lens)

        # Invariant length bounds: 0.80 * min(D) <= len(correct) <= 1.20 * max(D)
        assert 0.80 * min_d <= c_len <= 1.20 * max_d, (
            f"Failed invariant length bounds for nodes={nodes}: c_len={c_len}, min_d={min_d}, max_d={max_d}"
        )
        # Psychometric average parity: 0.80 * avg(D) <= len(correct) <= 1.20 * avg(D)
        assert 0.80 * avg_d <= c_len <= 1.20 * avg_d, (
            f"Failed psychometric parity for nodes={nodes}: c_len={c_len}, avg_d={avg_d:.2f}"
        )


# ==============================================================================
# 4. EXAMPLE 1 (H-01 CARNOT) CLEANLINESS & LENGTH PARITY
# ==============================================================================

def test_example_1_carnot_cleanliness_and_length_parity():
    """Verify Example 1 (H-01 Carnot) options are clean and satisfy length parity."""
    content = (PROMPTS_DIR / "prompt_shard_author.md").read_text(encoding="utf-8")

    m = re.search(r"def gen_h01\(rng\):.*?(?=def ver_h01)", content, re.DOTALL)
    assert m is not None, "Could not extract gen_h01 block from prompt_shard_author.md"
    gen_code = m.group(0)

    forbidden_prefixes = [
        "Inversión de roles:",
        "Omisión de límites:",
        "Asumiendo erróneamente:",
        "Confusión de conceptos:",
        "Falsa generalización:",
    ]
    for fp in forbidden_prefixes:
        assert fp not in gen_code, f"Forbidden giveaway prefix '{fp}' found in gen_h01 code block!"

    import random
    rng = random.Random(12345)
    for _ in range(50):
        tc = rng.randint(250, 350)
        delta = rng.randint(150, 450)
        th = tc + delta
        ans_val = round(1.0 - (tc / th), 3)

        d2 = round(tc / th, 3)
        if d2 == ans_val:
            d2 = round(d2 + 0.05, 3)

        correct = f"$\\eta = {ans_val}$"
        distractors = [
            f"$\\eta = {round(abs(1.0 - (th / tc)), 3) + 0.1}$",
            f"$\\eta = {d2}$",
            f"$\\eta = {round(1.0 - ((tc - 40) / (th - 40)), 3)}$",
            f"$\\eta = {round(1.0 - (tc / (1.5 * th)), 3)}$",
            f"$\\eta = {round((th - tc) / (th + tc), 3)}$",
            f"$\\eta = {round((th - tc) / (2 * th), 3)}$",
        ]

        c_len = len(correct)
        d_lens = [len(d) for d in distractors]
        min_d = min(d_lens)
        max_d = max(d_lens)
        avg_d = sum(d_lens) / len(d_lens)

        assert 0.80 * min_d <= c_len <= 1.20 * max_d
        assert 0.80 * avg_d <= c_len <= 1.20 * avg_d


# ==============================================================================
# 5. CTA ARCHITECT: GRANULARITY TABLE, DYNAMIC EVIDENCE & TRIAD
# ==============================================================================

def test_cta_granularity_table_and_dynamic_evidence():
    """Verify prompt_cta_architect.md defines fine/standard/coarse modes, dynamic evidence, and the Knowledge Triad."""
    content = (PROMPTS_DIR / "prompt_cta_architect.md").read_text(encoding="utf-8")

    # Granularity Table
    assert "Modos de Granularidad Curricular" in content
    assert "`fine`" in content
    assert "`standard`" in content
    assert "`coarse`" in content
    assert "6 – 10" in content
    assert "3 – 5" in content
    assert "1 – 2" in content

    # Dynamic Evidence Callout
    assert "[!IMPORTANT]" in content
    assert "REGLAS DE TRAZABILIDAD DINÁMICA DE EVIDENCIA" in content
    assert "1-indexed" in content
    assert "Slide" in content
    assert "section_heading" in content

    # Knowledge Triad
    assert "The Knowledge Triad Decomposition" in content
    assert "Facts [H]" in content
    assert "Concepts [C]" in content
    assert "Skills [Hab]" in content
    assert "omitted_step" in content


# ==============================================================================
# 6. ANTI-CHEAT & INTROSPECTION POLICIES
# ==============================================================================

def test_anti_cheat_and_introspection_policy():
    """Verify authorized compile_shard.py tuple inspection and strict ban on check_templates and engine/*."""
    author_content = (PROMPTS_DIR / "prompt_shard_author.md").read_text(encoding="utf-8")
    cta_content = (PROMPTS_DIR / "prompt_cta_architect.md").read_text(encoding="utf-8")

    # Shard Author: compile_shard.py read allowed for unpacking structure
    assert ".agents/skills/content-to-course/compile_shard.py" in author_content
    # Shard Author: check_templates, src/validator, engine forbidden
    assert "check_templates.py" in author_content
    assert "src/validator/*" in author_content
    assert "engine/*" in author_content
    assert "scratch/**" in author_content

    # CTA Architect: engine/* and SKILL.md forbidden
    assert "engine/*" in cta_content
    assert "SKILL.md" in cta_content


# ==============================================================================
# 7. BLIND JUDGE: ZERO-WARMUP, SINGLE TURN & FLEXIBLE OUTPUT PATH
# ==============================================================================

def test_prompt_blind_judge_contracts():
    """Verify prompt_blind_judge.md specifies single-turn resolution, zero disk reads, and echoes assigned output path."""
    content = (PROMPTS_DIR / "prompt_blind_judge.md").read_text(encoding="utf-8")

    # Zero-warmup & single turn
    assert "Zero-Warmup In-Prompt Payload" in content
    assert "RESOLUCIÓN EN 1 SOLO TURNO" in content
    assert "view_file" in content
    assert "search_web" in content

    # Flexible output paths accepted
    assert "<work_dir>/judges/judge_XX.json" in content
    assert "<work_dir>/verification/judge_responses_XX.json" in content

    # Completion contract echoes assigned output path
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
        assert size < 46080, f"Type spec {tname} exceeded 46,080 bytes: {size}"

        data = json.loads(tfile.read_text(encoding="utf-8"))
        sp = data.get("system_prompt", "")
        assert len(sp) > 500
        assert "[TRUNCADO]" not in sp
        assert not sp.startswith("...")
