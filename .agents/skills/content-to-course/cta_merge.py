"""CTA Map-Reduce and Harmonization Engine for content-to-course v2.

Implements the Map-Reduce Phase of Cognitive Task Analysis (CTA):
1. merge_cta_parts: Deterministic merge of sectional CTA parts, canonical ID renumbering,
   prerequisite & distractor rewriting, duplicate candidate detection, draft & outline creation.
2. apply_harmonize: Safe, audited application of Harmonizer operations (add_prerequisites,
   rename, drop_duplicate_distractors, merge), strict backward-only DAG and order validation,
   full schema validation, deterministic Markdown rendering, and merge reporting.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import logging
import re
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple, Union

# Import validators from check_cta
try:
    from .check_cta import JsonLineLocator, check_cta_katex, check_prerequisites_dag, validate_cta_rules
except ImportError:
    from check_cta import JsonLineLocator, check_cta_katex, check_prerequisites_dag, validate_cta_rules


logger = logging.getLogger("cta_merge")

# Heuristic thresholds for duplicate candidate detection
JACCARD_DUPLICATE_THRESHOLD: float = 0.6
NAME_OVERLAP_THRESHOLD: float = 0.3


def tokenize_text(text: str) -> Set[str]:
    """Tokenize and normalize text into unique lowercase word tokens."""
    if not text:
        return set()
    # Normalize unicode and extract alphanumeric words
    tokens = re.findall(r"[a-zA-Z0-9_\u00C0-\u017F]+", text.lower())
    # Exclude single character punctuation slips
    return {t for t in tokens if len(t) > 1}


def jaccard_similarity(tokens_a: Set[str], tokens_b: Set[str]) -> float:
    """Compute Jaccard similarity index between two token sets."""
    if not tokens_a or not tokens_b:
        return 0.0
    intersection = len(tokens_a & tokens_b)
    union = len(tokens_a | tokens_b)
    return intersection / union if union > 0 else 0.0


def extract_evidence_keys(evidence_list: Optional[List[Dict[str, Any]]]) -> Set[Tuple[str, str]]:
    """Extract canonical (doc_stem, page_str) pairs from an evidence list."""
    keys: Set[Tuple[str, str]] = set()
    if not evidence_list:
        return keys
    for ev in evidence_list:
        doc = str(ev.get("doc") or ev.get("pdf") or "").strip().lower()
        if not doc:
            continue
        doc_stem = Path(doc).stem.lower()
        page = str(ev.get("page", "")).strip().lower()
        if page:
            keys.add((doc_stem, page))
    return keys


def auto_balance_math_delimiters(text: str) -> str:
    """Deterministically repairs triple dollars '$$$' and odd unescaped '$' delimiters
    ONLY when curly braces '{' and '}' are balanced AND \\left / \\right sizing environments are balanced
    (preserving intentional syntax error detection). Handles compound trailing punctuation and brackets.
    """
    if not isinstance(text, str) or not text:
        return text

    # 1. Collapse accidental triple dollars $$$ -> $$
    if "$$$" in text:
        text = re.sub(r"\${3,}", "$$", text)

    # 2. Check unescaped inline '$' count after masking '$$' display blocks
    masked = re.sub(r"(?<!\\)\$\$", "__DISPLAY_MATH__", text)
    unescaped_dollars = [m.start() for m in re.finditer(r"(?<!\\)\$", masked)]
    if len(unescaped_dollars) % 2 == 1:
        # Only auto-close if curly braces and \left / \right sizing delimiters are balanced
        open_braces = len(re.findall(r"(?<!\\)\{", text))
        close_braces = len(re.findall(r"(?<!\\)\}", text))
        left_count = len(re.findall(r"\\left(?![a-zA-Z])", text))
        right_count = len(re.findall(r"\\right(?![a-zA-Z])", text))
        if open_braces == close_braces and left_count == right_count:
            last_dollar = unescaped_dollars[-1]
            prefix = text[:last_dollar]

            unmatched_open_parens = 0
            for ch in prefix:
                if ch == "(":
                    unmatched_open_parens += 1
                elif ch == ")" and unmatched_open_parens > 0:
                    unmatched_open_parens -= 1

            unmatched_open_brackets = 0
            for ch in prefix:
                if ch == "[":
                    unmatched_open_brackets += 1
                elif ch == "]" and unmatched_open_brackets > 0:
                    unmatched_open_brackets -= 1

            stripped = text.rstrip()
            trailing_whitespace = text[len(stripped):]

            compound_suffixes = (").", "),", ");", "):", ")?", '?"', '!"')
            single_suffixes = (".", ",", ";", ":")

            if stripped.endswith(compound_suffixes):
                text = stripped[:-2].rstrip() + "$" + stripped[-2:] + trailing_whitespace
            elif stripped.endswith(single_suffixes):
                text = stripped[:-1].rstrip() + "$" + stripped[-1] + trailing_whitespace
            else:
                text = stripped + "$" + trailing_whitespace

    return text


def normalize_orphan_math(text: str) -> str:
    """Normalizes orphaned/unescaped LaTeX expressions like dot{w} -> $\\dot{w}$, bar{k} -> $\\bar{k}$ outside $...$."""
    if not isinstance(text, str) or not text:
        return text

    text = auto_balance_math_delimiters(text)

    # Split text into outside-math and inside-math segments using $ / $$ blocks
    parts = re.split(r"(\$\$.*?\$\$|\$.*?\$)", text, flags=re.DOTALL)
    for i in range(0, len(parts), 2):
        chunk = parts[i]
        if not chunk:
            continue
        # 1. \dot{w} -> $\dot{w}$, \bar{k} -> $\bar{k}$, etc. (with backslash)
        chunk = re.sub(
            r"\\(dot|ddot|bar|hat|tilde|vec)\{([^{}]+)\}",
            r"$\\\1{\2}$",
            chunk,
        )
        # 1b. dot{w} or bar{k} (without backslash) ONLY if argument is a concise math token (1-4 chars, no spaces)
        chunk = re.sub(
            r"(?<!\\)\b(dot|ddot|bar|hat|tilde|vec)\{([a-zA-Z0-9_+\-*^./]{1,4})\}",
            r"$\\\1{\2}$",
            chunk,
        )
        # 2. \frac{a}{b} -> $\frac{a}{b}$ (with backslash)
        chunk = re.sub(
            r"\\(frac|dfrac|tfrac|cfrac)\{([^{}]+)\}\{([^{}]+)\}",
            r"$\\\1{\2}{\3}$",
            chunk,
        )
        # 2b. frac{a}{b} (without backslash)
        chunk = re.sub(
            r"(?<!\\)\b(frac|dfrac|tfrac|cfrac)\{([a-zA-Z0-9_+\-*^./]+)\}\{([a-zA-Z0-9_+\-*^./]+)\}",
            r"$\\\1{\2}{\3}$",
            chunk,
        )
        # 3. \sqrt{x} -> $\sqrt{x}$ (with backslash)
        chunk = re.sub(
            r"\\sqrt\{([^{}]+)\}",
            r"$\\sqrt{\1}$",
            chunk,
        )
        # 3b. sqrt{x} (without backslash)
        chunk = re.sub(
            r"(?<!\\)\bsqrt\{([a-zA-Z0-9_+\-*^./]+)\}",
            r"$\\sqrt{\1}$",
            chunk,
        )
        # 4. Greek letters and common math operators with backslash: \alpha -> $\alpha$, \partial -> $\partial$, etc.
        chunk = re.sub(
            r"\\(alpha|beta|gamma|delta|epsilon|varepsilon|zeta|eta|theta|iota|kappa|lambda|mu|nu|xi|pi|rho|sigma|tau|upsilon|phi|chi|psi|omega|Gamma|Delta|Theta|Lambda|Xi|Pi|Sigma|Phi|Psi|Omega|partial|int|sum|prod|infty|times|cdot|approx|leq|geq|neq)\b",
            r"$\\\1$",
            chunk,
        )
        # 5. Raw subscript or superscript with braces: k_{t+1} -> $k_{t+1}$
        chunk = re.sub(
            r"(?<!\$)\b([a-zA-Z0-9\\]+[_^]\{[a-zA-Z0-9_+\-*./]+\})(?!\$)",
            r"$\1$",
            chunk,
        )
        parts[i] = chunk

    return auto_balance_math_delimiters("".join(parts))


def sanitize_competency_math(comp: Dict[str, Any]) -> None:
    """Recursively normalizes orphan math expressions in competency fields and distractors."""
    for field in ("name", "description_latex", "description"):
        val = comp.get(field)
        if isinstance(val, str):
            comp[field] = normalize_orphan_math(val)

    for d in comp.get("distractors", []):
        if isinstance(d, dict):
            for d_field in (
                "name",
                "manifestation",
                "remediation_hint",
                "wrong_belief",
                "correct_belief",
                "omitted_step",
                "trigger",
            ):
                d_val = d.get(d_field)
                if isinstance(d_val, str):
                    d[d_field] = normalize_orphan_math(d_val)


def find_duplicate_candidates(competencies: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Deterministic candidate detector for duplicate competencies.

    Identifies pairs of competencies of the same type that satisfy at least one objective signal:
    1. High lexical similarity (Jaccard of normalized name + description tokens >= 0.6)
    2. Shared evidence (identical doc & page) combined with partial name overlap.
    """
    candidates: List[Dict[str, Any]] = []
    n = len(competencies)

    for i in range(n):
        c1 = competencies[i]
        id1 = c1.get("id", "")
        type1 = c1.get("type", "").lower()
        name1 = c1.get("name", "")
        desc1 = c1.get("description_latex") or c1.get("description", "")
        text1_tokens = tokenize_text(f"{name1} {desc1}")
        name1_tokens = tokenize_text(name1)
        ev1_keys = extract_evidence_keys(c1.get("evidence", []))

        for j in range(i + 1, n):
            c2 = competencies[j]
            id2 = c2.get("id", "")
            type2 = c2.get("type", "").lower()

            # Must be of the same knowledge type
            if type1 != type2:
                continue

            name2 = c2.get("name", "")
            desc2 = c2.get("description_latex") or c2.get("description", "")
            text2_tokens = tokenize_text(f"{name2} {desc2}")
            name2_tokens = tokenize_text(name2)
            ev2_keys = extract_evidence_keys(c2.get("evidence", []))

            jaccard_lex = jaccard_similarity(text1_tokens, text2_tokens)
            jaccard_name = jaccard_similarity(name1_tokens, name2_tokens)
            shared_ev = ev1_keys & ev2_keys

            # Name overlap signal
            has_name_overlap = (
                jaccard_name >= NAME_OVERLAP_THRESHOLD
                or len(name1_tokens & name2_tokens) >= 1
                or (name1.lower() in name2.lower() if len(name1) > 4 else False)
                or (name2.lower() in name1.lower() if len(name2) > 4 else False)
            )

            signals: List[str] = []
            if jaccard_lex >= JACCARD_DUPLICATE_THRESHOLD:
                signals.append("lexical_similarity")
            if len(shared_ev) > 0 and has_name_overlap:
                signals.append("shared_evidence")

            if signals:
                candidates.append({
                    "pair": [id1, id2],
                    "type": type1,
                    "signals": signals,
                    "jaccard_similarity": round(jaccard_lex, 4),
                    "shared_evidence": [{"doc": d, "page": p} for d, p in shared_ev],
                    "name_overlap": sorted(list(name1_tokens & name2_tokens)),
                    "c1_name": name1,
                    "c2_name": name2,
                })

    return candidates


def merge_cta_parts(work_dir: Union[str, Path]) -> Dict[str, Any]:
    """Deterministically merges sectional CTA parts into a canonical CTA draft and final cta.json.

    1. Requires 'work/pre_cta_manifest.json' (raises blocker error if missing).
    2. Reads parts in work/cta_parts/ (part_*.json, cta_part_*.json).
    3. Orders competencies deterministically by (subpart_index, file_index, page, orig_idx)
       using the order of subparts and files defined in pre_cta_manifest.json.
    4. Deduplicates and sequentially renumbers canonical IDs: H-01.., C-01.., Hab-01...
    5. Maps and rewrites distractor IDs and prerequisites using id_map.
    6. Writes work/id_map.json, work/duplicate_candidates.json, work/cta_draft.json,
       work/cta_outline.json, work/cta_order.json, and canonical work/cta.json / work/cta.md.
    """
    work_path = Path(work_dir).resolve()
    manifest_file = work_path / "pre_cta_manifest.json"
    if not manifest_file.is_file():
        print("BLOCKER:: No existe pre_cta_manifest.json", file=sys.stderr)
        raise FileNotFoundError("BLOCKER:: No existe pre_cta_manifest.json")

    manifest_data = json.loads(manifest_file.read_text(encoding="utf-8"))
    files_list = manifest_data.get("files", [])
    subparts_list = manifest_data.get("subparts", [])

    # Index files: doc_name / doc_slug / doc_stem -> file_index
    doc_to_file_idx: Dict[str, int] = {}
    for f in files_list:
        f_idx = f.get("file_index", 0)
        d_name = str(f.get("doc", "")).strip().lower()
        d_slug = str(f.get("doc_slug", "")).strip().lower()
        if d_name:
            doc_to_file_idx[d_name] = f_idx
            doc_to_file_idx[Path(d_name).stem.lower()] = f_idx
        if d_slug:
            doc_to_file_idx[d_slug] = f_idx

    # Index subparts: subpart_id -> (subpart_index, file_index, doc, cta_out_path)
    subpart_meta: Dict[str, Dict[str, Any]] = {}
    for sp in subparts_list:
        sp_id = str(sp.get("subpart_id", "")).strip().lower()
        subpart_meta[sp_id] = sp
        subpart_meta[f"part_{sp.get('subpart_index', 0)+1:02d}"] = sp

    parts_dir = work_path / "cta_parts"
    if not parts_dir.exists() or not parts_dir.is_dir():
        raise FileNotFoundError(f"CTA parts directory not found at: {parts_dir.resolve()}")

    part_files: List[Path] = []
    seen_stems: Set[str] = set()
    for pattern in ("part_*.json", "cta_part_*.json", "*.json"):
        for p in sorted(parts_dir.glob(pattern)):
            if p.is_file() and p.stem not in seen_stems and not p.name.endswith("_data.py"):
                seen_stems.add(p.stem)
                part_files.append(p)

    if not part_files:
        raise FileNotFoundError(f"No sectional CTA parts found in {parts_dir.resolve()}")

    combined_competencies: List[Dict[str, Any]] = []
    course_id = manifest_data.get("course_id") or "course_generic"
    course_title = course_id.replace("_", " ").title()
    macro_competency = f"Mastery of {course_title}"

    for p_file in part_files:
        stem = p_file.stem.lower()
        sp_info = subpart_meta.get(stem)
        if not sp_info:
            nums = re.findall(r"\d+", stem)
            if nums:
                sp_info = subpart_meta.get(f"part_{int(nums[0]):02d}")

        sp_idx = sp_info.get("subpart_index", 0) if sp_info else 0
        def_file_idx = sp_info.get("file_index", 0) if sp_info else 0

        try:
            content = json.loads(p_file.read_text(encoding="utf-8"))
        except Exception as e:
            raise ValueError(f"Failed to parse JSON in {p_file}: {e}") from e

        if isinstance(content, list):
            comps = content
        elif isinstance(content, dict):
            comps = content.get("competencies", [])
            course_id = content.get("course_id", course_id)
            course_title = content.get("title", course_title)
            macro_competency = content.get("macro_competency", macro_competency)
        else:
            comps = []

        for orig_idx, c in enumerate(comps):
            ev_list = c.get("evidence", [])
            ev_doc = str(ev_list[0].get("doc", "")).strip().lower() if ev_list else ""
            f_idx = doc_to_file_idx.get(ev_doc, doc_to_file_idx.get(Path(ev_doc).stem.lower(), def_file_idx))

            p_val = ev_list[0].get("page", 0) if ev_list else c.get("unit_index", 0)
            try:
                page_int = int(p_val)
            except (ValueError, TypeError):
                m = re.search(r"\d+", str(p_val))
                page_int = int(m.group(0)) if m else 0

            c["_sort_key"] = (sp_idx, f_idx, page_int, orig_idx)
            combined_competencies.append(c)

    if not combined_competencies:
        raise ValueError(f"Zero competencies found across all parts in {parts_dir.resolve()}")

    # Deterministic sort by (subpart_index, file_index, page, orig_idx)
    combined_competencies.sort(key=lambda c: c["_sort_key"])
    for c in combined_competencies:
        c.pop("_sort_key", None)

    # Sanitize and normalize orphan LaTeX math in all competencies and distractors
    for comp in combined_competencies:
        sanitize_competency_math(comp)

    # Renumber canonical sequential IDs per category
    fact_count = 0
    concept_count = 0
    skill_count = 0

    comp_id_map: Dict[str, str] = {}
    dist_id_map: Dict[str, str] = {}

    for comp in combined_competencies:
        old_cid = comp.get("id", "")
        ctype = comp.get("type", "").lower()

        if ctype == "fact":
            fact_count += 1
            new_cid = f"H-{fact_count:02d}"
            prefix = f"H{fact_count:02d}"
        elif ctype == "concept":
            concept_count += 1
            new_cid = f"C-{concept_count:02d}"
            prefix = f"C{concept_count:02d}"
        elif ctype == "skill":
            skill_count += 1
            new_cid = f"Hab-{skill_count:02d}"
            prefix = f"Hab{skill_count:02d}"
        else:
            fact_count += 1
            new_cid = f"H-{fact_count:02d}"
            prefix = f"H{fact_count:02d}"

        if old_cid:
            comp_id_map[old_cid] = new_cid
        comp["id"] = new_cid

        distractors = comp.get("distractors", [])
        for d_idx, dist in enumerate(distractors, start=1):
            old_did = dist.get("id", "")
            new_did = f"D-{prefix}-{d_idx:02d}"
            if old_did:
                dist_id_map[old_did] = new_did
            dist["id"] = new_did

    # Rewrite prerequisites across all competencies
    for comp in combined_competencies:
        prereqs = comp.get("prerequisites", [])
        new_prereqs: List[str] = []
        for p in prereqs:
            mapped = comp_id_map.get(p, p)
            if mapped not in new_prereqs and mapped != comp["id"]:
                new_prereqs.append(mapped)
        comp["prerequisites"] = new_prereqs

    # Detect duplicate candidates
    duplicate_candidates = find_duplicate_candidates(combined_competencies)

    # Prepare outputs
    id_map_payload = {
        "competencies": comp_id_map,
        "distractors": dist_id_map,
    }

    draft_payload = {
        "course_id": course_id,
        "title": course_title,
        "macro_competency": macro_competency,
        "competencies": combined_competencies,
    }

    outline_payload = {
        "course_id": course_id,
        "title": course_title,
        "macro_competency": macro_competency,
        "competencies": [
            {
                "id": c["id"],
                "name": c.get("name", ""),
                "type": c.get("type", ""),
                "session": c.get("session", ""),
                "unit_index": c.get("unit_index", 0),
                "evidence": c.get("evidence", []),
                "prerequisites": c.get("prerequisites", []),
                "distractor_names": [d.get("name", "") for d in c.get("distractors", [])],
                "distractor_ids": [d.get("id", "") for d in c.get("distractors", [])],
            }
            for c in combined_competencies
        ],
    }

    order_list = [c["id"] for c in combined_competencies]
    order_hash = hashlib.sha256(json.dumps(order_list).encode("utf-8")).hexdigest()
    order_payload = {
        "order": order_list,
        "order_hash": order_hash,
    }

    (work_path / "id_map.json").write_text(
        json.dumps(id_map_payload, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    (work_path / "duplicate_candidates.json").write_text(
        json.dumps(duplicate_candidates, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    (work_path / "cta_draft.json").write_text(
        json.dumps(draft_payload, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    (work_path / "cta_outline.json").write_text(
        json.dumps(outline_payload, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    (work_path / "cta_order.json").write_text(
        json.dumps(order_payload, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    # Write canonical cta.json and cta.md
    final_cta_json = work_path / "cta.json"
    final_cta_json.write_text(
        json.dumps(draft_payload, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    final_cta_md = work_path / "cta.md"
    rendered_md = render_cta_md(draft_payload)
    final_cta_md.write_text(rendered_md, encoding="utf-8")

    logger.info(
        "Successfully merged %d parts into %d competencies. Detected %d duplicate candidates.",
        len(part_files),
        len(combined_competencies),
        len(duplicate_candidates),
    )

    ret = dict(draft_payload)
    ret["status"] = "success"
    ret["total_competencies"] = len(combined_competencies)
    ret["draft_path"] = str((work_path / "cta_draft.json").resolve())
    ret["outline_path"] = str((work_path / "cta_outline.json").resolve())
    ret["candidates_path"] = str((work_path / "duplicate_candidates.json").resolve())
    ret["duplicate_candidates"] = duplicate_candidates
    ret["parts"] = [p.name for p in part_files]
    return ret


def apply_harmonize(
    work_dir: Union[str, Path],
    no_merge: bool = False,
    manifest_path: Optional[Union[str, Path]] = None,
) -> Dict[str, Any]:
    """Applies Harmonizer directives to cta_draft.json and generates cta.json and cta.md.

    Supported operations in work/cta_harmonize.json:
    - add_prerequisites: Adds cross-session prerequisites. Must be backward-only and acyclic.
    - rename: Renames competencies respecting schema.
    - drop_duplicate_distractors: Drops duplicate distractors without violating quotas.
    - merge: Merges duplicate candidates (survivor is first in pedagogical order, unifies
      distractors & evidence, rewrites prerequisites). Rejects any pair not in candidates.

    Validates:
    - Pedagogical order has not been altered (compared against cta_order.json).
    - Full validate_cta_rules passes.
    - Deterministically renders work/cta.md.
    - Writes work/merge_report.json.
    """
    work_path = Path(work_dir)

    draft_file = work_path / "cta_draft.json"
    order_file = work_path / "cta_order.json"
    candidates_file = work_path / "duplicate_candidates.json"
    harmonize_file = work_path / "cta_harmonize.json"

    if not draft_file.exists():
        raise FileNotFoundError(f"Required artifact cta_draft.json not found in {work_path}")
    if not order_file.exists():
        raise FileNotFoundError(f"Required artifact cta_order.json not found in {work_path}")
    if not candidates_file.exists():
        raise FileNotFoundError(f"Required artifact duplicate_candidates.json not found in {work_path}")
    if not harmonize_file.exists():
        raise FileNotFoundError(f"Required artifact cta_harmonize.json not found in {work_path}")

    cta_draft = json.loads(draft_file.read_text(encoding="utf-8"))
    cta_order_data = json.loads(order_file.read_text(encoding="utf-8"))
    candidates_data = json.loads(candidates_file.read_text(encoding="utf-8"))
    harmonize_data = json.loads(harmonize_file.read_text(encoding="utf-8"))

    orig_order: List[str] = cta_order_data.get("order", [])
    competencies: List[Dict[str, Any]] = cta_draft.get("competencies", [])

    # Index allowed duplicate candidate pairs (normalized as sorted tuples)
    allowed_candidates_set: Set[Tuple[str, str]] = set()
    candidate_lookup: Dict[Tuple[str, str], Dict[str, Any]] = {}
    for cand in candidates_data:
        p = cand.get("pair", [])
        if len(p) == 2:
            key = tuple(sorted([p[0], p[1]]))
            allowed_candidates_set.add(key)
            candidate_lookup[key] = cand

    decisions_log: List[Dict[str, Any]] = []

    # 1. Process renames
    renames = harmonize_data.get("rename", [])
    for ren in renames:
        cid = ren.get("competency")
        new_name = ren.get("name")
        if not new_name or not isinstance(new_name, str) or not new_name.strip():
            raise ValueError(f"Rename failed: competency '{cid}' requires a non-empty string name.")
        target_comp = next((c for c in competencies if c["id"] == cid), None)
        if not target_comp:
            raise ValueError(f"Rename failed: competency '{cid}' not found in curriculum.")
        target_comp["name"] = new_name.strip()
        decisions_log.append({
            "operation": "rename",
            "competency": cid,
            "new_name": new_name.strip(),
        })

    # 2. Process drop_duplicate_distractors
    drops = harmonize_data.get("drop_duplicate_distractors", [])
    for drop_item in drops:
        cid = drop_item.get("competency")
        dids_to_drop = set(drop_item.get("distractor_ids", []))
        target_comp = next((c for c in competencies if c["id"] == cid), None)
        if not target_comp:
            raise ValueError(f"drop_duplicate_distractors failed: competency '{cid}' not found.")

        current_distractors = target_comp.get("distractors", [])
        existing_dids = {d.get("id") for d in current_distractors}
        missing_dids = dids_to_drop - existing_dids
        if missing_dids:
            raise ValueError(
                f"Cannot drop non-existent distractor IDs {missing_dids} in competency '{cid}'."
            )

        surviving_distractors = [d for d in current_distractors if d.get("id") not in dids_to_drop]

        # Quota enforcement: Fact/Concept >= 3, Skill >= 6 (with >= 2 omitted_step)
        ctype = target_comp.get("type", "").lower()
        if ctype in ("fact", "concept"):
            if len(surviving_distractors) < 3:
                raise ValueError(
                    f"Quota violation: Dropping distractors from {ctype} '{cid}' would leave "
                    f"{len(surviving_distractors)} (minimum 3 required)."
                )
        elif ctype == "skill":
            if len(surviving_distractors) < 6:
                raise ValueError(
                    f"Quota violation: Dropping distractors from Skill '{cid}' would leave "
                    f"{len(surviving_distractors)} (minimum 6 required)."
                )
            omitted_count = sum(1 for d in surviving_distractors if d.get("omitted_step"))
            if omitted_count < 2:
                raise ValueError(
                    f"Quota violation: Dropping distractors from Skill '{cid}' would leave "
                    f"{omitted_count} with omitted_step (minimum 2 required)."
                )

        target_comp["distractors"] = surviving_distractors
        decisions_log.append({
            "operation": "drop_duplicate_distractors",
            "competency": cid,
            "dropped_distractors": list(dids_to_drop),
            "remaining_count": len(surviving_distractors),
        })

    # 3. Process merges
    merges_directives = harmonize_data.get("merges", harmonize_data.get("merge", []))
    if no_merge:
        decisions_log.append({
            "operation": "merge",
            "status": "disabled_by_flag",
            "message": "Fusión desactivada por flag no_merge=True.",
        })
    else:
        for m_entry in merges_directives:
            pair = m_entry.get("pair", [])
            if len(pair) != 2:
                continue
            id_x, id_y = pair[0], pair[1]
            decision = m_entry.get("decision", "merge")
            reason = m_entry.get("reason", "")
            sorted_pair = tuple(sorted([id_x, id_y]))

            if sorted_pair not in allowed_candidates_set:
                raise ValueError(
                    f"REJECTED: Merge attempted on pair {pair} which was NOT identified as a candidate in duplicate_candidates.json."
                )

            if decision == "keep_separate":
                decisions_log.append({
                    "operation": "merge",
                    "pair": [id_x, id_y],
                    "decision": "keep_separate",
                    "reason": reason,
                })
                continue

            if decision == "merge":
                # Determine survivor: must be the one that appears EARLIER in pedagogical sequence
                idx_x = orig_order.index(id_x) if id_x in orig_order else 999999
                idx_y = orig_order.index(id_y) if id_y in orig_order else 999999
                if idx_x <= idx_y:
                    survivor_id, absorbed_id = id_x, id_y
                else:
                    survivor_id, absorbed_id = id_y, id_x

                comp_survivor = next((c for c in competencies if c["id"] == survivor_id), None)
                comp_absorbed = next((c for c in competencies if c["id"] == absorbed_id), None)

                if not comp_survivor or not comp_absorbed:
                    raise ValueError(
                        f"Merge failed: Competency {survivor_id} or {absorbed_id} not found."
                    )

                # Unify distractors (eliminate exact duplicates by name/belief signature)
                combined_distractors = list(comp_survivor.get("distractors", []))
                seen_signatures = {
                    (
                        str(d.get("name", "")).strip().lower(),
                        str(d.get("wrong_belief", "")).strip().lower(),
                        str(d.get("omitted_step", "")).strip().lower(),
                    )
                    for d in combined_distractors
                }
                seen_dids = {d.get("id") for d in combined_distractors}
                survivor_code = survivor_id.replace("-", "")

                for d in comp_absorbed.get("distractors", []):
                    sig = (
                        str(d.get("name", "")).strip().lower(),
                        str(d.get("wrong_belief", "")).strip().lower(),
                        str(d.get("omitted_step", "")).strip().lower(),
                    )
                    if sig not in seen_signatures:
                        d_copy = dict(d)
                        dist_idx = len(combined_distractors) + 1
                        new_did = f"D-{survivor_code}-{dist_idx:02d}"
                        while new_did in seen_dids:
                            dist_idx += 1
                            new_did = f"D-{survivor_code}-{dist_idx:02d}"
                        d_copy["id"] = new_did
                        seen_dids.add(new_did)
                        seen_signatures.add(sig)
                        combined_distractors.append(d_copy)

                comp_survivor["distractors"] = combined_distractors

                # Unify evidence citations
                survivor_evidence = list(comp_survivor.get("evidence", []))
                seen_ev_keys = extract_evidence_keys(survivor_evidence)
                for ev in comp_absorbed.get("evidence", []):
                    ev_doc_stem = Path(str(ev.get("doc") or ev.get("pdf") or "")).stem.lower()
                    ev_page = str(ev.get("page", "")).strip().lower()
                    if (ev_doc_stem, ev_page) not in seen_ev_keys:
                        seen_ev_keys.add((ev_doc_stem, ev_page))
                        survivor_evidence.append(ev)
                comp_survivor["evidence"] = survivor_evidence

                # Unify source examples if present
                if comp_absorbed.get("source_examples"):
                    merged_examples = list(dict.fromkeys(
                        comp_survivor.get("source_examples", []) + comp_absorbed.get("source_examples", [])
                    ))
                    comp_survivor["source_examples"] = merged_examples

                # Remove absorbed competency from curriculum
                competencies = [c for c in competencies if c["id"] != absorbed_id]

                # Rewrite prerequisites across all remaining competencies
                for c in competencies:
                    c_prereqs = c.get("prerequisites", [])
                    rewritten: List[str] = []
                    for pr in c_prereqs:
                        target = survivor_id if pr == absorbed_id else pr
                        if target != c["id"] and target not in rewritten:
                            rewritten.append(target)
                    c["prerequisites"] = rewritten

                decisions_log.append({
                    "operation": "merge",
                    "pair": [id_x, id_y],
                    "survivor": survivor_id,
                    "absorbed": absorbed_id,
                    "decision": "merge",
                    "reason": reason,
                })

    # 4. Process add_prerequisites
    add_prereqs = harmonize_data.get("add_prerequisites", [])
    # Index current competency positions in pedagogical order
    current_order_map = {c["id"]: idx for idx, c in enumerate(competencies)}

    for item in add_prereqs:
        cid = item.get("competency")
        reqs = item.get("requires", item.get("prerequisites", []))
        if isinstance(reqs, str):
            reqs = [reqs]

        if cid not in current_order_map:
            raise ValueError(f"add_prerequisites failed: Competency '{cid}' not found.")
        cid_pos = current_order_map[cid]
        comp = next(c for c in competencies if c["id"] == cid)
        comp_prereqs = list(comp.get("prerequisites", []))

        for req in reqs:
            if req not in current_order_map:
                raise ValueError(
                    f"add_prerequisites failed: Prerequisite '{req}' for '{cid}' not found."
                )
            req_pos = current_order_map[req]

            # Enforce backward-only constraint: req_pos < cid_pos
            if req_pos >= cid_pos:
                raise ValueError(
                    f"Backward-only violation: Competency '{cid}' (order pos {cid_pos}) "
                    f"cannot depend on '{req}' (order pos {req_pos}). Prerequisites must point only backward."
                )

            if req not in comp_prereqs:
                comp_prereqs.append(req)

        comp["prerequisites"] = comp_prereqs
        decisions_log.append({
            "operation": "add_prerequisites",
            "competency": cid,
            "requires": reqs,
        })

    # 5. Validate DAG acyclicity
    dag_errors = check_prerequisites_dag(competencies)
    if dag_errors:
        raise ValueError(f"Prerequisite DAG validation failed: {dag_errors}")

    # 6. Validate pedagogical order immutability
    current_ids = [c["id"] for c in competencies]
    expected_order = [cid for cid in orig_order if cid in current_ids]
    if current_ids != expected_order:
        raise ValueError(
            f"Pedagogical order violation: Competency ordering was modified. "
            f"Expected {expected_order}, got {current_ids}."
        )

    # 7. Validate full CTA schema and psychometric rules
    # Sanitize and normalize orphan LaTeX math in all competencies and distractors
    for comp in competencies:
        sanitize_competency_math(comp)

    cta_draft["competencies"] = competencies

    manifest_file = Path(manifest_path).resolve() if manifest_path else work_path / "pre_cta_manifest.json"
    if not manifest_file.is_file():
        print("BLOCKER:: No existe pre_cta_manifest.json", file=sys.stderr)
        raise FileNotFoundError("BLOCKER:: No existe pre_cta_manifest.json")
    manifest_data = json.loads(manifest_file.read_text(encoding="utf-8"))

    valid, rule_errors = validate_cta_rules(cta_draft, manifest_data)
    if not valid:
        raise ValueError(f"validate_cta_rules failed with errors: {rule_errors}")

    # 8. Write final cta.json
    final_cta_json = work_path / "cta.json"
    final_cta_json.write_text(
        json.dumps(cta_draft, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    # 9. Deterministically render and write cta.md
    final_cta_md = work_path / "cta.md"
    rendered_md = render_cta_md(cta_draft)
    final_cta_md.write_text(rendered_md, encoding="utf-8")

    # 10. Write merge_report.json
    merge_report = {
        "status": "success",
        "total_competencies": len(competencies),
        "decisions": decisions_log,
    }
    (work_path / "merge_report.json").write_text(
        json.dumps(merge_report, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    logger.info("Successfully harmonized curriculum: wrote %s and %s", final_cta_json, final_cta_md)
    return cta_draft


def render_cta_md(cta_data: Dict[str, Any]) -> str:
    """Deterministically renders a human-readable curriculum markdown document from cta.json."""
    title = cta_data.get("title", "Course Curriculum")
    course_id = cta_data.get("course_id", "course_generic")
    macro = cta_data.get("macro_competency", "")
    competencies = cta_data.get("competencies", [])

    facts = [c for c in competencies if c.get("type", "").lower() == "fact"]
    concepts = [c for c in competencies if c.get("type", "").lower() == "concept"]
    skills = [c for c in competencies if c.get("type", "").lower() == "skill"]
    total_distractors = sum(len(c.get("distractors", [])) for c in competencies)

    lines: List[str] = []
    lines.append(f"# Cognitive Task Analysis (CTA): {title}")
    lines.append("")
    lines.append(f"- **Course ID:** `{course_id}`")
    if macro:
        lines.append(f"- **Macro-Competency:** {macro}")
    lines.append(
        f"- **Structure:** {len(competencies)} total competencies "
        f"({len(facts)} Facts, {len(concepts)} Concepts, {len(skills)} Skills) with {total_distractors} fused distractors."
    )
    lines.append("")

    # Summary table
    lines.append("## Curriculum Overview")
    lines.append("")
    lines.append("| ID | Name | Type | Bloom | Session | Prerequisites | Distractors |")
    lines.append("|:---|:---|:---:|:---:|:---|:---|:---:|")

    for c in competencies:
        cid = c.get("id", "")
        name = c.get("name", "")
        ctype = c.get("type", "").title()
        bloom = c.get("bloom", "Apply")
        session = c.get("session", "-")
        prereqs = ", ".join(c.get("prerequisites", [])) or "-"
        d_count = len(c.get("distractors", []))
        lines.append(f"| `{cid}` | {name} | {ctype} | {bloom} | {session} | {prereqs} | {d_count} |")

    lines.append("")
    lines.append("---")
    lines.append("")

    # Granular details per competency
    lines.append("## Detailed Competency Specifications")
    lines.append("")

    for c in competencies:
        cid = c.get("id", "")
        name = c.get("name", "")
        ctype = c.get("type", "").title()
        bloom = c.get("bloom", "Apply")
        session = c.get("session", "-")
        desc = c.get("description_latex") or c.get("description", "")
        prereqs = ", ".join(c.get("prerequisites", [])) or "None"
        evidence = c.get("evidence", [])
        distractors = c.get("distractors", [])

        lines.append(f"### [{cid}] {name} ({ctype})")
        lines.append("")
        lines.append(f"- **Bloom Level:** {bloom}")
        lines.append(f"- **Session:** {session}")
        lines.append(f"- **Prerequisites:** {prereqs}")

        if evidence:
            ev_strs = []
            for ev in evidence:
                d = ev.get("doc") or ev.get("pdf") or ""
                p = ev.get("page")
                ev_strs.append(f"`{d}` (page {p})")
            lines.append(f"- **Evidence Citations:** {', '.join(ev_strs)}")

        lines.append("")
        lines.append("#### Description & Cognitive Model")
        lines.append(desc or "*No mathematical description provided.*")
        lines.append("")

        if distractors:
            lines.append(f"#### Fused Distractor Models ({len(distractors)})")
            lines.append("")
            lines.append("| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |")
            lines.append("|:---|:---|:---:|:---:|:---|:---|")
            for d in distractors:
                did = d.get("id", "")
                dname = d.get("name", "")
                etype = d.get("error_type", "other")
                sev = d.get("severity", "medium")
                trap_desc = d.get("wrong_belief") or d.get("omitted_step") or "-"
                hint = d.get("remediation_hint", "-")
                lines.append(
                    f"| `{did}` | {dname} | {etype} | {sev} | {trap_desc} | {hint} |"
                )
            lines.append("")

        lines.append("---")
        lines.append("")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="CTA Map-Reduce and Harmonization Manager")
    subparsers = parser.add_subparsers(dest="command", required=True)

    merge_parser = subparsers.add_parser("merge", help="Merge sectional CTA parts into cta_draft.json")
    merge_parser.add_argument("--work", "--work-dir", dest="work_dir", default="work", help="Path to working directory containing pre_cta_manifest.json")

    apply_parser = subparsers.add_parser("apply", help="Apply cta_harmonize.json to cta_draft.json")
    apply_parser.add_argument("--work", "--work-dir", dest="work_dir", default="work", help="Path to working directory")
    apply_parser.add_argument("--no-merge", action="store_true", help="Disable duplicate merging")
    apply_parser.add_argument("--manifest", help="Optional path to pre_cta_manifest.json for evidence checks")

    args = parser.parse_args()

    if args.command == "merge":
        try:
            merge_cta_parts(args.work_dir)
            print(f"SUCCESS: Sectional parts merged in {args.work_dir}")
            sys.exit(0)
        except FileNotFoundError as e:
            if "BLOCKER::" in str(e):
                sys.exit(2)
            print(f"FAIL: merge_cta_parts failed: {e}", file=sys.stderr)
            sys.exit(1)
        except Exception as e:
            print(f"FAIL: merge_cta_parts failed: {e}", file=sys.stderr)
            sys.exit(1)

    elif args.command == "apply":
        try:
            apply_harmonize(args.work_dir, no_merge=args.no_merge, manifest_path=args.manifest)
            print(f"SUCCESS: Harmonization applied in {args.work_dir}")
            sys.exit(0)
        except FileNotFoundError as e:
            if "BLOCKER::" in str(e):
                sys.exit(2)
            print(f"FAIL: apply_harmonize failed: {e}", file=sys.stderr)
            sys.exit(1)
        except Exception as e:
            print(f"FAIL: apply_harmonize failed: {e}", file=sys.stderr)
            sys.exit(1)


if __name__ == "__main__":
    main()
