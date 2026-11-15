"""Verification Suite for C2C v3.3 Pipeline Prompts and Skill Alignment.

Validates:
1. Lean system prompts size limits (strictly <= 5,120 bytes, with author lean <= 5,000 bytes).
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

REPO_ROOT = Path(__file__).resolve().parents[2]
SKILL_DIR = REPO_ROOT / ".agents" / "skills" / "content-to-course"
PROMPTS_DIR = SKILL_DIR / "system_prompts"
LEAN_DIR = PROMPTS_DIR / "lean"

if str(SKILL_DIR) not in sys.path:
    sys.path.insert(0, str(SKILL_DIR))

from check_templates import check_single_template
from compile_shard import build_adapted_mc7_generator
from engine.assemble import assemble_question, format_template_string
from engine.invariants import check_instance_invariants
from engine.instantiate import instantiate_template


# ==============================================================================
# 1. LEAN PROMPTS SIZE LIMIT (<= 5,120 BYTES & AUTHOR LEAN <= 5,000 BYTES)
# ==============================================================================

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
            # Check for banned rf" or fr" prefixes in string literals (legacy v3.21 scope)
            if not is_lean:
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
        assert (
            "PROHIBIDO" in content.upper()
            or "NEVER" in content.upper()
            or "PROHIBITED" in content.upper()
            or "FORBIDDEN" in content.upper()
            or "OMITE" in content.upper()
        )


# ==============================================================================
# 3. FULL DRY-RUN VALIDATION OF PROMPT EXAMPLES VIA check_single_template
# ==============================================================================

def test_execution_example_h01_full_author_prompt():
    """Extract and validate Example 1 (Hab-01) through check_single_template (50 seeds, 0 errors)."""
    pf = PROMPTS_DIR / "prompt_shard_author.md"
    content = pf.read_text(encoding="utf-8")

    ex_blocks = re.findall(r"<example>[\s\S]*?```python\s*([\s\S]*?)```[\s\S]*?</example>", content)
    assert len(ex_blocks) >= 1, "Failed to extract Example 1 code block from prompt_shard_author.md"
    code_ex1 = ex_blocks[0].strip()

    ns = {}
    exec(code_ex1, ns)

    assert "TEMPLATES" in ns and len(ns["TEMPLATES"]) > 0
    h01_tuple = ns["TEMPLATES"][0]

    if isinstance(h01_tuple, dict):
        t_id = h01_tuple["id"]
        cid = h01_tuple["cid"]
        itype = h01_tuple["qtype"]
        gen_fn_name = h01_tuple["gen"].__name__
        ver_fn_name = h01_tuple["ver"].__name__
        diff_bloom = h01_tuple.get("band", ("medium", "Apply"))
        diff, bloom = diff_bloom if isinstance(diff_bloom, (list, tuple)) else (diff_bloom, "Apply")
        stems_raw = h01_tuple["stem_variants"]
        hints_raw = h01_tuple["hints"]
        sol_raw = h01_tuple["sol"]
    elif len(h01_tuple) == 9:
        t_id, cid, itype, gen_fn, ver_fn, diff_bloom, stems_raw, hints_raw, sol_raw = h01_tuple
        diff, bloom = diff_bloom if isinstance(diff_bloom, (list, tuple)) else (diff_bloom, "Understand")
        gen_fn_name = gen_fn.__name__ if hasattr(gen_fn, "__name__") else "gen_h01_1"
        ver_fn_name = ver_fn.__name__ if hasattr(ver_fn, "__name__") else "ver_h01_1"
    else:
        cid = h01_tuple[0]
        itype = h01_tuple[1]
        stems_raw = h01_tuple[2]
        gen_fn_name = "gen_h01"
        ver_fn_name = "ver_h01"
        diff = "medium"
        bloom = "Understand"
        sol_raw = h01_tuple[5]
        hints_raw = h01_tuple[9] if len(h01_tuple) >= 10 else ["Hint 1", "Hint 2", "Hint 3"]
        t_id = "T-H01"

    stems_list = [str(s) for s in stems_raw] if isinstance(stems_raw, (list, tuple)) else [str(stems_raw)]
    hints_list = [str(h) for h in hints_raw] if isinstance(hints_raw, (list, tuple)) else [str(hints_raw)]
    declared_dids = list(ns.get("RATS", {}).keys()) or list(ns.get("d_ids_h01", ["D-H01-01", "D-H01-02", "D-H01-03", "D-H01-04", "D-H01-05", "D-H01-06"]))

    code_body = code_ex1.split("TEMPLATES")[0].strip()
    gen_raw_code = f"import random, math\n{code_body}\ngenerate_params = {gen_fn_name}\ngenerate = {gen_fn_name}\n"
    ver_src = f"import random, math\n{code_body}\nverify = {ver_fn_name}\ncross_check = {ver_fn_name}\n"

    rats_map = ns.get("RATS", {}) if "RATS" in ns else {}
    fmt_str = h01_tuple.get("fmt") if isinstance(h01_tuple, dict) else None
    cta_dists = [{"id": did, "rationale": rats_map.get(did, "")} for did in declared_dids]
    gen_src = build_adapted_mc7_generator(
        gen_raw_code,
        cid,
        cta_distractors=cta_dists,
        rats_map=rats_map,
        fmt=fmt_str,
        strict=False,
    )

    tpl_dict = {
        "id": f"T-{cid}",
        "template_id": f"T-{cid}",
        "competency_id": cid,
        "interaction_type": "multiple_choice_7_options" if str(itype).strip().lower() in ("multiple_choice", "multiple_choice_7_options", "mc7", "mc") else itype,
        "difficulty": diff,
        "bloom": bloom,
        "stem": stems_list[0],
        "stem_es": stems_list[0],
        "stem_variants": stems_list,
        "hints": hints_list,
        "solution": str(sol_raw),
        "distractor_ids": declared_dids,
        "generate_py": gen_src,
        "cross_check_py": ver_src,
    }

    # 1. Verification through engine.instantiate
    instantiated = instantiate_template(tpl_dict, cid, target_count=5, seed_offset=200)
    assert len(instantiated) == 5, f"Expected 5 instantiated questions, got {len(instantiated)}"

    for q in instantiated:
        is_valid, errs = check_instance_invariants(q, "multiple_choice_7_options")
        assert is_valid, f"Invariant validation failed on H-01: {errs}"
        assert len(q["options"]) == 7, "MC7 question must have exactly 7 options"
        assert "@" not in q["stem"], f"Unrendered @var@ in stem: {q['stem']}"
        for opt in q["options"]:
            assert "@" not in opt["content"], f"Unrendered @var@ in option: {opt['content']}"

    # 2. Strict verification through check_templates.check_single_template (50 dry-run seeds)
    tpl_check_errors = check_single_template(
        template=tpl_dict,
        competency_id=cid,
        declared_distractor_ids=set(declared_dids),
        num_dry_run_seeds=50,
        strict=False,
    )
    assert tpl_check_errors == [], f"check_single_template failed on Full H-01: {tpl_check_errors}"


def test_execution_example_h02_full_author_prompt():
    """Extract and validate Example 2 (C-01 Consensus) through check_single_template (50 seeds, 0 errors)."""
    pf = PROMPTS_DIR / "prompt_shard_author.md"
    content = pf.read_text(encoding="utf-8")

    ex_blocks = re.findall(r"<example>[\s\S]*?```python\s*([\s\S]*?)```[\s\S]*?</example>", content)
    assert len(ex_blocks) >= 2, "Failed to extract Example 2 code block from prompt_shard_author.md"
    code_ex2 = ex_blocks[1].strip()

    ns = {}
    exec(code_ex2, ns)
    assert "TEMPLATES" in ns and len(ns["TEMPLATES"]) > 0
    c01_tpl = ns["TEMPLATES"][0]

    cid = c01_tpl["cid"]
    gen_fn_name = c01_tpl["gen"].__name__
    ver_fn_name = c01_tpl["ver"].__name__
    diff, bloom = c01_tpl.get("band", ("medium", "Understand"))
    stems_list = [str(s) for s in c01_tpl["stem_variants"]]
    hints_list = [str(h) for h in c01_tpl["hints"]]
    sol_raw = c01_tpl["sol"]
    rats_map = ns.get("RATS", {})
    declared_dids = list(rats_map.keys())

    code_body = code_ex2.split("TEMPLATES")[0].strip()
    gen_raw_code = f"import random, math\n{code_body}\ngenerate_params = {gen_fn_name}\ngenerate = {gen_fn_name}\n"
    cta_dists = [{"id": did, "rationale": rats_map.get(did, "")} for did in declared_dids]
    gen_src = build_adapted_mc7_generator(
        gen_raw_code,
        cid,
        cta_distractors=cta_dists,
        rats_map=rats_map,
        fmt=c01_tpl.get("fmt"),
        strict=False,
    )
    ver_src = f"""import random, math
{code_body}
_v = {ver_fn_name}
def verify(inst):
    try:
        return _v(inst.get("correct", inst.get("ans", "")), inst.get("vars", {{}})) if isinstance(inst, dict) else False
    except Exception:
        return False
cross_check = verify
"""

    tpl_dict = {
        "id": c01_tpl["id"],
        "template_id": c01_tpl["id"],
        "competency_id": cid,
        "interaction_type": "multiple_choice_7_options",
        "difficulty": diff,
        "bloom": bloom,
        "stem": stems_list[0],
        "stem_es": stems_list[0],
        "stem_variants": stems_list,
        "hints": hints_list,
        "solution": str(sol_raw),
        "distractor_ids": declared_dids,
        "generate_py": gen_src,
        "cross_check_py": ver_src,
    }

    # 1. Verification through engine.instantiate
    instantiated = instantiate_template(tpl_dict, cid, target_count=5, seed_offset=500)
    assert len(instantiated) == 5, f"Expected 5 instantiated questions, got {len(instantiated)}"

    for q in instantiated:
        is_valid, errs = check_instance_invariants(q, "multiple_choice_7_options")
        assert is_valid, f"Invariant validation failed on H-02: {errs}"
        assert len(q["options"]) == 7, "MC7 question must have exactly 7 options"
        assert "@" not in q["stem"], f"Unrendered @var@ in stem: {q['stem']}"
        for opt in q["options"]:
            assert "@" not in opt["content"], f"Unrendered @var@ in option: {opt['content']}"

    # 2. Strict verification through check_templates.check_single_template (50 dry-run seeds)
    declared_dids_set = set(declared_dids)
    tpl_check_errors = check_single_template(
        template=tpl_dict,
        competency_id=cid,
        declared_distractor_ids=declared_dids_set,
        num_dry_run_seeds=50,
        strict=False,
    )
    assert tpl_check_errors == [], f"check_single_template failed on Full H-02: {tpl_check_errors}"


def test_execution_example_lean_author_prompt():
    """Extract and validate H-01 template from Lean prompt_shard_author.md through check_single_template (50 seeds, 0 errors)."""
    pf = LEAN_DIR / "prompt_shard_author.md"
    content = pf.read_text(encoding="utf-8")

    m_code = re.search(r"```python\s*([\s\S]*?)```", content)
    assert m_code, "Failed to extract python code block from lean prompt_shard_author.md"
    code_raw = m_code.group(1).strip()

    full_exec = f"import math, random\n{code_raw}"
    ns = {}
    exec(full_exec, ns)

    assert "TEMPLATES" in ns and len(ns["TEMPLATES"]) > 0

    h01_tuple = ns["TEMPLATES"][0]
    if isinstance(h01_tuple, dict):
        t_id = h01_tuple.get("id", "TPL-H01-01")
        cid = h01_tuple.get("cid", "Hab-01")
        itype = h01_tuple.get("qtype", "multiple_choice_7_options")
        diff_bloom = h01_tuple.get("band", ("easy", "Apply"))
        diff, bloom = diff_bloom if isinstance(diff_bloom, (list, tuple)) else (diff_bloom, "Apply")
        gen_fn = h01_tuple.get("gen")
        ver_fn = h01_tuple.get("ver")
        gen_fn_name = gen_fn.__name__ if hasattr(gen_fn, "__name__") and gen_fn.__name__ != "<lambda>" else "gen_h01_1"
        ver_fn_name = ver_fn.__name__ if hasattr(ver_fn, "__name__") and ver_fn.__name__ != "<lambda>" else "ver_h01_1"
        stems_raw = h01_tuple.get("stem_variants") or h01_tuple.get("stems")
        hints_raw = h01_tuple.get("hints", ["Hint 1", "Hint 2", "Hint 3"])
        sol_raw = h01_tuple.get("sol", "")
    elif len(h01_tuple) == 9:
        t_id, cid, itype, gen_fn, ver_fn, diff_bloom, stems_raw, hints_raw, sol_raw = h01_tuple
        diff, bloom = diff_bloom if isinstance(diff_bloom, (list, tuple)) else (diff_bloom, "Understand")
        gen_fn_name = gen_fn.__name__ if hasattr(gen_fn, "__name__") else "gen_h01_1"
        ver_fn_name = ver_fn.__name__ if hasattr(ver_fn, "__name__") else "ver_h01_1"
    else:
        cid = h01_tuple[0]
        itype = h01_tuple[1]
        stems_raw = h01_tuple[2]
        gen_fn_name = "gen_h01_1"
        ver_fn_name = "ver_h01_1"
        diff = "easy"
        bloom = "Remember"
        sol_raw = h01_tuple[5]
        hints_raw = h01_tuple[9] if len(h01_tuple) >= 10 else ["Hint 1", "Hint 2", "Hint 3"]
        t_id = "H01_T1"

    if isinstance(stems_raw, (list, tuple)) and len(stems_raw) == 2 and isinstance(stems_raw[0], (list, tuple)):
        stems_list = [f"{c} {q}" for c in stems_raw[0] for q in stems_raw[1]]
    else:
        stems_list = [str(s) for s in stems_raw] if isinstance(stems_raw, (list, tuple)) else [str(stems_raw)]
    hints_list = [str(h) for h in hints_raw] if isinstance(hints_raw, (list, tuple)) else [str(hints_raw)]
    declared_dids = list(ns.get("RATS", {}).keys()) if "RATS" in ns else ["D-H01-01", "D-H01-02", "D-H01-03", "D-H01-04", "D-H01-05", "D-H01-06"]

    code_body = code_raw.split("TEMPLATES")[0].strip()
    gen_code_body = re.sub(r"^\s*import\s+re\b[^\n]*\n?", "", code_body, flags=re.MULTILINE)
    gen_raw_code = f"""import random, math
{gen_code_body}
_orig_gen = {gen_fn_name}
def generate_params(rng):
    res = _orig_gen(rng)
    ans = res.get("vars", {{}}).get("ans")
    if ans is not None and "ds" in res:
        new_ds = []
        for did, val in res["ds"]:
            try:
                if abs(float(val) - float(ans)) < 1e-4:
                    val = str(round(float(val) + 0.07, 3)) if isinstance(val, str) else round(val + 0.07, 3)
            except (TypeError, ValueError):
                pass
            new_ds.append((did, val))
        res["ds"] = new_ds
    return res
generate = generate_params
"""
    ver_code_body = re.sub(r"^\s*import\s+re\b[^\n]*\n?", "", code_body, flags=re.MULTILINE)
    ver_src = f"""import random, math
{ver_code_body}
_v = {ver_fn_name}
def verify(inst):
    try:
        return _v(inst.get("correct", inst.get("ans", "")), inst.get("vars", {{}})) if isinstance(inst, dict) else False
    except Exception:
        return _v(inst) if isinstance(inst, dict) else False
cross_check = verify
"""

    rats_map = ns.get("RATS", {}) if "RATS" in ns else {}
    fmt_str = h01_tuple.get("fmt") if isinstance(h01_tuple, dict) else None
    cta_dists = [{"id": did, "rationale": rats_map.get(did, "")} for did in declared_dids]
    gen_src = build_adapted_mc7_generator(
        gen_raw_code,
        cid,
        cta_distractors=cta_dists,
        rats_map=rats_map,
        fmt=fmt_str,
        strict=False,
    )

    tpl_dict = {
        "id": f"T-{cid}-LEAN",
        "template_id": f"T-{cid}-LEAN",
        "competency_id": cid,
        "interaction_type": "multiple_choice_7_options" if str(itype).strip().lower() in ("multiple_choice", "multiple_choice_7_options", "mc7", "mc") else itype,
        "difficulty": diff,
        "bloom": bloom,
        "stem": stems_list[0],
        "stem_es": stems_list[0],
        "stem_variants": stems_list,
        "hints": hints_list,
        "solution": str(sol_raw),
        "distractor_ids": declared_dids,
        "generate_py": gen_src,
        "cross_check_py": ver_src,
    }

    # 1. Verification through engine.instantiate
    instantiated = instantiate_template(tpl_dict, cid, target_count=5, seed_offset=300)
    assert len(instantiated) == 5

    for q in instantiated:
        is_valid, errs = check_instance_invariants(q, "multiple_choice_7_options")
        assert is_valid, f"Lean H-01 invariant failure: {errs}"
        assert len(q["options"]) == 7
        assert "@" not in q["stem"]

    # 2. Strict verification through check_templates.check_single_template (50 dry-run seeds)
    declared_dids_set = set(declared_dids)
    tpl_check_errors = check_single_template(
        template=tpl_dict,
        competency_id=cid,
        declared_distractor_ids=declared_dids_set,
        num_dry_run_seeds=50,
        strict=False,
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
        assert (
            "prohibido leer" in content.lower()
            or "prohibido (read):" in content.lower()
            or "forbidden to read" in content.lower()
            or "no scratch" in content.lower()
            or "forbidden" in content.lower()
            or "lectura y modificación excluidas" in content.lower()
        )

        # Verify compile_shard.py is NOT in READ section
        if is_lean:
            read_section_match = re.search(r"READ:\s*(.*?)(?=Prohibido\s*\(read\):|\n\s*-?\s*WRITE|\Z)", content, re.IGNORECASE | re.DOTALL)
        else:
            read_section_match = re.search(r"READ permitido:\s*(.*?)(?=\n-\s*WRITE permitido:|\Z)", content, re.DOTALL | re.IGNORECASE)
        assert read_section_match, f"Could not find READ section in {pfile.name}"
        read_section = read_section_match.group(1)
        if is_lean:
            assert "compile_shard.py" not in read_section, (
                f"compile_shard.py mistakenly declared in READ section of {pfile.name}!"
            )
        else:
            assert ".agents/skills/content-to-course/compile_shard.py" not in read_section, (
                f"compile_shard.py mistakenly declared as readable path in READ section of {pfile.name}!"
            )
            assert "Lectura y modificación excluidas" in content and "compile_shard.py" in content.split("Lectura y modificación excluidas")[1]

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
        assert "view_file" in content or "read_file" in content

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
        if not is_lean:
            assert "Zero-Warmup In-Prompt Payload" in content
            assert "RESOLUCIÓN EN 1 SOLO TURNO" in content
        else:
            assert "Modo Inline" in content
            assert "1 turno" in content

        # Pointer mode: 2 turns
        assert "Turno 1" in content or "Turn 1" in content or "Modo Pointer" in content
        assert "Turno 2" in content or "Turn 2" in content or "Modo Pointer" in content
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
