"""Independent Blind Judge Module for content-to-course v2.

Generates blind judge question batches (WITHOUT answer keys or solutions) for 2 instances
per template, evaluates judge responses against ground truth answer keys, and manages
correction cycles (maximum 3 cycles).

Zero domain logic: agnostically operates on templates conforming to template.schema.json.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import logging
import math
import re
import sys
import zlib
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union, Set

# Ensure skill directory is in sys.path
skill_dir = Path(__file__).parent.resolve()
if str(skill_dir) not in sys.path:
    sys.path.insert(0, str(skill_dir))

from engine.assemble import assemble_question
from engine.sandbox import execute_sandbox_instance

logger = logging.getLogger("judge")
MAX_CORRECTION_CYCLES = 3


def _load_templates(templates_path: Union[str, Path]) -> List[Dict[str, Any]]:
    """Loads all template objects from a JSON file or directory of JSON files, attaching SHA-256 hashes."""
    path = Path(templates_path)
    templates: List[Dict[str, Any]] = []

    if path.is_file():
        raw_bytes = path.read_bytes()
        file_sha = hashlib.sha256(raw_bytes).hexdigest()
        content = json.loads(raw_bytes.decode("utf-8"))
        if isinstance(content, dict):
            if "templates" in content:
                for t in content["templates"]:
                    if "competency_id" not in t and "competency_id" in content:
                        t["competency_id"] = content["competency_id"]
                    t_sha = hashlib.sha256(json.dumps(t, sort_keys=True).encode("utf-8")).hexdigest()
                    t["_sha256"] = t_sha
                    t["_file_sha256"] = file_sha
                    templates.append(t)
            else:
                t_sha = hashlib.sha256(json.dumps(content, sort_keys=True).encode("utf-8")).hexdigest()
                content["_sha256"] = t_sha
                content["_file_sha256"] = file_sha
                templates.append(content)
        elif isinstance(content, list):
            for t in content:
                t_sha = hashlib.sha256(json.dumps(t, sort_keys=True).encode("utf-8")).hexdigest()
                t["_sha256"] = t_sha
                t["_file_sha256"] = file_sha
                templates.append(t)
    elif path.is_dir():
        for file in sorted(path.glob("*.json")):
            try:
                raw_bytes = file.read_bytes()
                file_sha = hashlib.sha256(raw_bytes).hexdigest()
                data = json.loads(raw_bytes.decode("utf-8"))
                if isinstance(data, dict):
                    if "templates" in data:
                        for t in data["templates"]:
                            if "competency_id" not in t and "competency_id" in data:
                                t["competency_id"] = data["competency_id"]
                            t["_sha256"] = file_sha
                            t["_file_sha256"] = file_sha
                            templates.append(t)
                    else:
                        data["_sha256"] = file_sha
                        data["_file_sha256"] = file_sha
                        templates.append(data)
                elif isinstance(data, list):
                    for t in data:
                        t["_sha256"] = file_sha
                        t["_file_sha256"] = file_sha
                        templates.append(t)
            except Exception as e:
                logger.warning("Could not read template file %s: %s", file, e)

    return templates


def _normalize_option_letter(val: Any) -> str:
    """Normalize option identifier by removing 'opt_' or similar prefixes and converting to uppercase."""
    if val is None:
        return ""
    s = str(val).strip()
    # Strip prefixes like opt_, OPT_, option_, Option , etc.
    s = re.sub(r"^(?:opt(?:ion|ción)?_?|\s*)+", "", s, flags=re.IGNORECASE).strip()
    # If starting with a single letter (e.g. 'B', 'b', 'B.', 'B)', 'B: ...')
    m = re.match(r"^([A-Za-z])(?:\b|[.:\)\s]|$)", s)
    if m:
        return m.group(1).upper()
    return s.upper()


def _parse_float(val: Any) -> Optional[float]:
    """Parse numeric float from numeric or string value, handling commas, math formatting, and fractions."""
    if val is None:
        return None
    if isinstance(val, (int, float)):
        return float(val)
    s = str(val).strip().replace(" ", "").replace("$", "").replace("%", "")
    # Remove outer math formatting wrappers
    s = re.sub(r"^\$\$?(.*?)\$\$?$", r"\1", s)
    s = re.sub(r"^\\\[(.*?)\\\]$", r"\1", s)
    s = re.sub(r"^\\\((.*?)\\\)$", r"\1", s)
    s = s.strip("'\"` ")
    # Comma as decimal separator if single comma and no period
    if s.count(",") == 1 and "." not in s:
        s = s.replace(",", ".")
    try:
        return float(s)
    except (ValueError, TypeError):
        pass
    # Support simple fraction like "1/2" or "-3/4"
    if "/" in s:
        parts = s.split("/")
        if len(parts) == 2:
            try:
                num = float(parts[0])
                den = float(parts[1])
                if den != 0:
                    return num / den
            except (ValueError, TypeError):
                pass
    return None


def _is_numeric_equal(val1: Any, val2: Any, tol: float = 0.01) -> bool:
    """Checks whether two values are numerically equal within a given tolerance (default 0.01)."""
    f1 = _parse_float(val1)
    f2 = _parse_float(val2)
    if f1 is not None and f2 is not None:
        return abs(f1 - f2) <= tol or math.isclose(f1, f2, abs_tol=tol, rel_tol=1e-4)
    return False


def _normalize_str(s: Any) -> str:
    """Normalizes whitespace and removes math wrapper characters."""
    if s is None:
        return ""
    st = str(s).strip()
    # Strip LaTeX math wrappers $...$ or $$...$$ or \(...\) or \[...\]
    st = re.sub(r"^\$\$?(.*?)\$\$?$", r"\1", st)
    st = re.sub(r"^\\\[(.*?)\\\]$", r"\1", st)
    st = re.sub(r"^\\\((.*?)\\\)$", r"\1", st)
    st = st.strip("'\"` ").lower()
    return re.sub(r"\s+", "", st)


def generate_judge_batch(
    templates_path: Union[str, Path],
    work_dir: Union[str, Path],
    cta_path: Optional[Union[str, Path]] = None,
    seeds: Tuple[int, int] = (101, 202),
    items_per_competency: int = 2,
    ready_only: bool = False,
) -> Tuple[Path, Path]:
    """Generates work/judge_batch.json WITHOUT answer keys using stratified sampling by competency.
    
    Also generates work/judge_ground_truth.json (retained for comparison).

    Args:
        templates_path: Path to template JSON file or directory.
        work_dir: Working directory to write judge files.
        cta_path: Optional path to cta.json for distractor metadata.
        seeds: Two deterministic seeds for generating instances.
        items_per_competency: Stratified sample count per competency (defaults to 2).
                              If <= 0, generates 2 instances for every template.
        ready_only: If True, skips competencies that were already evaluated in earlier waves/batches.

    Returns:
        Tuple of (path_to_judge_batch_json, path_to_ground_truth_json).
    """
    work = Path(work_dir)
    work.mkdir(parents=True, exist_ok=True)

    templates = _load_templates(templates_path)
    if not templates:
        raise ValueError(f"No templates found in path: {templates_path}")

    # Load previously evaluated competencies if in ready_only mode
    evaluated_file = work / "verification" / "evaluated_competencies.json"
    evaluated_ids: Set[str] = set()
    saved_hashes: Dict[str, str] = {}
    if evaluated_file.is_file():
        try:
            ev_data = json.loads(evaluated_file.read_text(encoding="utf-8"))
            evaluated_ids = set(ev_data.get("evaluated_competency_ids", []))
            saved_hashes = ev_data.get("competency_hashes", {})
        except Exception:
            pass
    elif (work / "evaluated_competencies.json").is_file():
        try:
            ev_data = json.loads((work / "evaluated_competencies.json").read_text(encoding="utf-8"))
            evaluated_ids = set(ev_data.get("evaluated_competency_ids", []))
            saved_hashes = ev_data.get("competency_hashes", {})
        except Exception:
            pass

    if ready_only and (evaluated_ids or saved_hashes):
        unjudged_templates = []
        for t in templates:
            cid = str(t.get("competency_id", "comp-01"))
            t_sha = t.get("_sha256") or hashlib.sha256(json.dumps(t, sort_keys=True).encode("utf-8")).hexdigest()
            if cid in evaluated_ids:
                if cid in saved_hashes:
                    if saved_hashes[cid] == t_sha:
                        # Template unchanged: skip
                        continue
                    else:
                        # Template hash modified (repaired!): re-evaluate!
                        unjudged_templates.append(t)
                else:
                    # Legacy record without hash: skip
                    continue
            else:
                unjudged_templates.append(t)

        if unjudged_templates:
            templates = unjudged_templates
        else:
            logger.info("All templates in %s have already been evaluated and are unchanged (--ready-only).", templates_path)
            batch_path = work / "judge_batch.json"
            truth_path = work / "judge_ground_truth.json"
            if not batch_path.is_file():
                batch_path.write_text("[]", encoding="utf-8")
            if not truth_path.is_file():
                truth_path.write_text("{}", encoding="utf-8")
            return batch_path, truth_path

    # Load CTA distractors map if available
    cta_distractors_map: Dict[str, Dict[str, Any]] = {}
    if cta_path and Path(cta_path).is_file():
        try:
            cta_data = json.loads(Path(cta_path).read_text(encoding="utf-8"))
            for comp in cta_data.get("competencies", []):
                for d in comp.get("distractors", []):
                    if "id" in d:
                        cta_distractors_map[d["id"]] = d
        except Exception as e:
            logger.warning("Failed to load CTA distractors map from %s: %s", cta_path, e)

    judge_batch_items: List[Dict[str, Any]] = []
    ground_truth: Dict[str, Dict[str, Any]] = {}

    # Group templates by competency_id
    comp_templates: Dict[str, List[Dict[str, Any]]] = {}
    for t_idx, template in enumerate(templates):
        comp_id = template.get("competency_id", "comp-01")
        comp_templates.setdefault(comp_id, []).append(template)

    planned_items: List[Tuple[Dict[str, Any], int]] = []

    if items_per_competency > 0:
        # Stratified sampling: ~items_per_competency per competency
        for comp_id, t_list in comp_templates.items():
            # Group by interaction type for diverse stratified coverage
            by_type: Dict[str, List[Dict[str, Any]]] = {}
            for t in t_list:
                itype = t.get("interaction_type", "multiple_choice_7_options")
                by_type.setdefault(itype, []).append(t)

            type_queues = [list(q) for q in by_type.values()]
            selected_comp_items: List[Tuple[Dict[str, Any], int]] = []

            while len(selected_comp_items) < items_per_competency:
                added = False
                for q in type_queues:
                    if q and len(selected_comp_items) < items_per_competency:
                        t = q.pop(0)
                        seed = seeds[len(selected_comp_items) % len(seeds)]
                        selected_comp_items.append((t, seed))
                        added = True
                if not added:
                    # If all queues drained, cycle through t_list
                    for t in t_list:
                        if len(selected_comp_items) < items_per_competency:
                            seed = seeds[len(selected_comp_items) % len(seeds)]
                            selected_comp_items.append((t, seed))
                        else:
                            break
                    break

            planned_items.extend(selected_comp_items)
    else:
        # Unstratified: evaluate all templates across all seeds
        for template in templates:
            for seed in seeds:
                planned_items.append((template, seed))

    template_counts: Dict[str, int] = {}
    for template, seed in planned_items:
        template_id = template.get("id", "T-00")
        comp_id = template.get("competency_id", "comp-01")
        itype = template.get("interaction_type", "multiple_choice_7_options")

        inst_idx = template_counts.get(template_id, 0) + 1
        template_counts[template_id] = inst_idx
        item_id = f"{template_id}_judge_{inst_idx}"

        gen_res = execute_sandbox_instance(template["generate_py"], seed=seed)

        # Cryptographic per-item option shuffle seed (uniform A..G distribution)
        option_shuffle_seed = zlib.crc32(f"{template_id}:{inst_idx}:{seed}".encode("utf-8")) & 0xFFFFFFFF

        # Assemble full question
        assembled = assemble_question(
            template=template,
            gen_result=gen_res,
            competency_id=comp_id,
            question_index=inst_idx,
            cta_distractors_map=cta_distractors_map,
            seed=option_shuffle_seed,
        )

        # Strip all answer indicators for the blind judge
        judge_item: Dict[str, Any] = {
            "item_id": item_id,
            "template_id": template_id,
            "competency_id": comp_id,
            "interaction_type": itype,
            "stem": assembled["stem"],
        }

        gt_record: Dict[str, Any] = {
            "item_id": item_id,
            "template_id": template_id,
            "competency_id": comp_id,
            "interaction_type": itype,
        }

        if itype == "multiple_choice_7_options":
            options_blind = []
            correct_letter = None
            correct_content = None

            for opt in assembled.get("options", []):
                raw_id = opt.get("option_id") or opt.get("id", "")
                letter = _normalize_option_letter(raw_id)
                content = opt.get("content", "")
                options_blind.append({"id": letter, "content": content})
                if opt.get("is_correct") is True:
                    correct_letter = letter
                    correct_content = content

            judge_item["options"] = options_blind
            gt_record["correct_letter"] = correct_letter
            gt_record["correct_content"] = correct_content

        elif itype == "multiple_select":
            options_blind = []
            correct_letters = []
            correct_contents = []

            for opt in assembled.get("options", []):
                raw_id = opt.get("option_id") or opt.get("id", "")
                letter = _normalize_option_letter(raw_id)
                content = opt.get("content", "")
                options_blind.append({"id": letter, "content": content})
                if opt.get("is_correct") is True:
                    correct_letters.append(letter)
                    correct_contents.append(content)

            judge_item["options"] = options_blind
            gt_record["correct_letters"] = sorted(correct_letters)
            gt_record["correct_contents"] = sorted(correct_contents)

        elif itype == "fill_in_the_blank":
            ca = assembled.get("correct_answer", {})
            c_val = ca.get("value") or assembled.get("value")
            gt_record["correct_value"] = c_val
            gt_record["canonical_algebraic"] = ca.get("canonical_algebraic") or assembled.get("canonical_algebraic")
            gt_record["accepted_equivalents"] = ca.get("accepted_equivalents") or assembled.get("accepted_equivalents", [])
            tol = ca.get("tolerance") or assembled.get("tolerance", 0.01)
            try:
                tol = float(tol)
            except (ValueError, TypeError):
                tol = 0.01
            if tol < 0.01:
                tol = 0.01
            gt_record["tolerance"] = tol

            # Build enriched typed contract for blind judges
            parsed_num = _parse_float(c_val)
            expected_type = "float"
            decimal_places = 2
            format_example = "2.80 o 2.8"
            if parsed_num is not None:
                if parsed_num.is_integer():
                    expected_type = "integer"
                    decimal_places = 0
                    format_example = f"{int(parsed_num)}"
                else:
                    expected_type = "float"
                    decimal_places = 2
                    format_example = f"{parsed_num:.2f} o {round(parsed_num, 4)}"

            contract = {
                "expected_type": expected_type,
                "decimal_places": decimal_places,
                "tolerance": tol,
                "format_example": format_example,
            }
            judge_item["answer_contract"] = contract
            gt_record["answer_contract"] = contract

        if "graph" in assembled and assembled["graph"]:
            judge_item["graph"] = assembled["graph"]

        judge_batch_items.append(judge_item)
        ground_truth[item_id] = gt_record

    v_dir = work / "verification"
    v_dir.mkdir(parents=True, exist_ok=True)

    batch_path = work / "judge_batch.json"
    batch_json_str = json.dumps(judge_batch_items, indent=2, ensure_ascii=False)
    batch_path.write_text(batch_json_str, encoding="utf-8")
    (v_dir / "judge_batch.json").write_text(batch_json_str, encoding="utf-8")

    truth_path = work / "judge_ground_truth.json"
    truth_json_str = json.dumps(ground_truth, indent=2, ensure_ascii=False)
    truth_path.write_text(truth_json_str, encoding="utf-8")
    (v_dir / "judge_ground_truth.json").write_text(truth_json_str, encoding="utf-8")

    # Clean up stale split batches in verification and work so dispatch_judges slices the new batch fresh
    for stale_split in list(v_dir.glob("judge_batch_*.json")) + list(work.glob("judge_batch_*.json")):
        if stale_split.name not in ("judge_batch.json", "judge_redispatch_batch.json"):
            try:
                stale_split.unlink(missing_ok=True)
            except Exception:
                pass

    # Record evaluated competency IDs and their SHA-256 hashes for incremental streaming
    new_comp_ids = {t.get("competency_id", "comp-01") for t, _ in planned_items}
    total_evaluated_ids = sorted(evaluated_ids.union(new_comp_ids))
    total_hashes = dict(saved_hashes)
    for t in templates:
        cid = str(t.get("competency_id", "comp-01"))
        t_sha = t.get("_sha256") or hashlib.sha256(json.dumps(t, sort_keys=True).encode("utf-8")).hexdigest()
        total_hashes[cid] = t_sha

    ev_payload = {
        "last_updated": datetime.now(timezone.utc).isoformat(),
        "evaluated_competency_ids": total_evaluated_ids,
        "evaluated_count": len(total_evaluated_ids),
        "competency_hashes": total_hashes,
    }
    (v_dir / "evaluated_competencies.json").write_text(json.dumps(ev_payload, indent=2, ensure_ascii=False), encoding="utf-8")
    (work / "evaluated_competencies.json").write_text(json.dumps(ev_payload, indent=2, ensure_ascii=False), encoding="utf-8")

    logger.info("Generated judge batch with %d items at %s", len(judge_batch_items), batch_path)
    return batch_path, truth_path


def split_judge_batch(
    work_dir: Union[str, Path, List[Dict[str, Any]]],
    max_judges: int = 8,
    items_per_judge: int = 12,
    max_items_per_judge: Optional[int] = None,
) -> Any:
    """Splits work/judge_batch.json or raw items list into batches with at most items_per_judge items each (default <= 12).
    
    Args:
        work_dir: Working directory containing judge_batch.json, OR a direct list of item dicts.
        max_judges: Soft target for maximum number of judges.
        items_per_judge: Maximum item count per judge (default: 12).
        max_items_per_judge: Alias for items_per_judge.

    Returns:
        List of Paths if work_dir is a Path/str, or List of List[Dict] if work_dir is a list.
    """
    if max_items_per_judge is not None:
        items_per_judge = max_items_per_judge

    if isinstance(work_dir, list):
        items = work_dir
        if not items:
            return []
        limit = max(1, items_per_judge)
        return [items[i : i + limit] for i in range(0, len(items), limit)]

    work = Path(work_dir)
    batch_file = work / "verification" / "judge_batch.json"
    if not batch_file.is_file():
        batch_file = work / "judge_batch.json"
    if not batch_file.is_file():
        logger.warning("judge_batch.json not found in %s", work)
        return []

    try:
        items: List[Dict[str, Any]] = json.loads(batch_file.read_text(encoding="utf-8"))
    except Exception as e:
        logger.error("Failed to parse judge_batch.json: %s", e)
        return []

    if not items:
        return []

    total_items = len(items)
    # Strictly enforce items_per_judge <= 12 by sizing num_judges appropriately
    needed_judges = math.ceil(total_items / items_per_judge) if items_per_judge > 0 else 1
    num_judges = max(1, max(max_judges, needed_judges) if needed_judges > max_judges else needed_judges)
    num_judges = min(num_judges, total_items)
    num_judges = max(1, num_judges)

    # Stratified distribution by competency_id
    comp_groups: Dict[str, List[Dict[str, Any]]] = {}
    for item in items:
        cid = item.get("competency_id", "default")
        comp_groups.setdefault(cid, []).append(item)

    buckets: List[List[Dict[str, Any]]] = [[] for _ in range(num_judges)]
    curr_j = 0
    for cid, c_items in comp_groups.items():
        for itm in c_items:
            buckets[curr_j % num_judges].append(itm)
            curr_j += 1

    # Filter out empty buckets if any
    non_empty_buckets = [b for b in buckets if b]

    # Verification directory support
    verif_dir = work / "verification"
    verif_dir.mkdir(parents=True, exist_ok=True)

    generated_paths: List[Path] = []
    for idx, b_items in enumerate(non_empty_buckets):
        # Write to work/judge_batch_{idx+1:02d}.json
        out_p = work / f"judge_batch_{idx + 1:02d}.json"
        out_p.write_text(json.dumps(b_items, indent=2, ensure_ascii=False), encoding="utf-8")
        generated_paths.append(out_p)

        # Also write to work/verification/judge_batch_{idx+1:02d}.json
        verif_out_p = verif_dir / f"judge_batch_{idx + 1:02d}.json"
        verif_out_p.write_text(json.dumps(b_items, indent=2, ensure_ascii=False), encoding="utf-8")

    logger.info("Split %d items across %d judge batches (max %d items/judge) in %s", total_items, len(non_empty_buckets), items_per_judge, work)
    return generated_paths


def check_judge_completeness(work_dir: Union[str, Path]) -> Dict[str, Any]:
    """Detects truncated or missing judge responses across all batch files.
    
    Verifies that len(responses) == len(batch_items) for each judge batch.
    Returns completeness metrics, truncated batches, and exact missing item IDs.
    """
    work = Path(work_dir).resolve()
    verif_dir = work / "verification"
    judges_dir = work / "judges"

    # Locate batch files
    cand_batches = sorted(verif_dir.glob("judge_batch_*.json")) if verif_dir.is_dir() else []
    if not cand_batches:
        cand_batches = sorted(work.glob("judge_batch_*.json"))
    split_batches = [bf for bf in cand_batches if bf.name not in ("judge_batch.json", "judge_redispatch_batch.json")]
    if not split_batches:
        unsplit = verif_dir / "judge_batch.json"
        if not unsplit.is_file():
            unsplit = work / "judge_batch.json"
        if unsplit.is_file():
            split_batches = [unsplit]

    total_expected = 0
    total_received = 0
    all_missing_ids: List[str] = []
    batch_reports: List[Dict[str, Any]] = []

    for bf in split_batches:
        m = re.search(r"judge_batch_(\d+)", bf.name)
        j_id = m.group(1) if m else "01"

        try:
            b_data = json.loads(bf.read_text(encoding="utf-8"))
            raw_items = b_data.get("items", []) if isinstance(b_data, dict) else (b_data if isinstance(b_data, list) else [])
        except Exception:
            raw_items = []

        expected_ids: List[str] = []
        for itm in raw_items:
            if isinstance(itm, dict):
                iid = itm.get("item_id") or itm.get("question_id") or itm.get("id")
                if iid:
                    expected_ids.append(str(iid))

        # Look for corresponding response file
        resp_candidates = [
            verif_dir / f"judge_responses_{j_id}.json",
            work / f"judge_responses_{j_id}.json",
            judges_dir / f"judge_{j_id}.json",
            verif_dir / "judge_responses.json",
            work / "judge_responses.json",
        ]
        resp_file: Optional[Path] = None
        for rc in resp_candidates:
            if rc.is_file():
                resp_file = rc
                break

        resp_map: Dict[str, Any] = {}
        if resp_file:
            try:
                raw_resp = json.loads(resp_file.read_text(encoding="utf-8"))
                eval_list = None
                if isinstance(raw_resp, list):
                    eval_list = raw_resp
                elif isinstance(raw_resp, dict):
                    for cand_key in ("evaluations", "items", "results", "responses"):
                        if isinstance(raw_resp.get(cand_key), list):
                            eval_list = raw_resp[cand_key]
                            break
                if eval_list is not None:
                    for r in eval_list:
                        if isinstance(r, dict):
                            rid = r.get("item_id") or r.get("question_id") or r.get("id")
                            if rid:
                                resp_map[str(rid)] = r.get("answer") or r.get("response") or r.get("verdict") or True
                elif isinstance(raw_resp, dict):
                    dict_inner = raw_resp.get("responses", raw_resp) if isinstance(raw_resp.get("responses"), dict) else raw_resp
                    for k, v in dict_inner.items():
                        if isinstance(v, dict) and ("answer" in v or "response" in v or "verdict" in v):
                            resp_map[str(k)] = v.get("answer") or v.get("response") or v.get("verdict")
                        else:
                            resp_map[str(k)] = v
            except Exception as e:
                logger.warning("Could not read response file %s: %s", resp_file, e)

        # Check completeness for this batch
        received_ids = [iid for iid in expected_ids if iid in resp_map and resp_map[iid] is not None]
        missing_ids = [iid for iid in expected_ids if iid not in received_ids]

        total_expected += len(expected_ids)
        total_received += len(received_ids)
        all_missing_ids.extend(missing_ids)

        is_truncated = len(missing_ids) > 0
        batch_reports.append({
            "batch_file": bf.name,
            "judge_id": j_id,
            "expected_count": len(expected_ids),
            "received_count": len(received_ids),
            "missing_count": len(missing_ids),
            "missing_item_ids": missing_ids,
            "is_truncated": is_truncated,
            "status": "truncated" if is_truncated else "complete",
            "response_file": resp_file.as_posix() if resp_file else None,
        })

    is_complete = (len(all_missing_ids) == 0) and (total_expected > 0)
    truncated_batches_count = sum(1 for b in batch_reports if b["is_truncated"])

    return {
        "is_complete": is_complete,
        "total_batches": len(batch_reports),
        "completed_batches": len(batch_reports) - truncated_batches_count,
        "truncated_batches": truncated_batches_count,
        "total_expected_items": total_expected,
        "total_received_items": total_received,
        "total_missing_items": len(all_missing_ids),
        "missing_ids": all_missing_ids,
        "missing_item_ids": all_missing_ids,
        "batch_reports": batch_reports,
    }


def emit_judge_redispatch(
    work_dir: Union[str, Path],
    max_items_per_judge: int = 12,
) -> Dict[str, Any]:
    """Automatically detects incomplete evaluations and emits re-dispatch batch files for only missing IDs.
    
    Guarantees that re-dispatched items remain 100% blind (no ground truth or answer keys).
    """
    work = Path(work_dir).resolve()
    verif_dir = work / "verification"
    verif_dir.mkdir(parents=True, exist_ok=True)

    completeness = check_judge_completeness(work)
    if completeness["is_complete"] or completeness["total_missing_items"] == 0:
        logger.info("All judge evaluations are complete. No re-dispatch needed.")
        return {
            "redispatch_needed": False,
            "missing_count": 0,
            "batches": [],
            "item_files": [],
        }

    missing_set = set(completeness["missing_item_ids"])

    # Collect blind question definitions for missing IDs
    missing_items: List[Dict[str, Any]] = []
    seen_ids: Set[str] = set()

    cand_batches = sorted(verif_dir.glob("judge_batch_*.json")) + sorted(work.glob("judge_batch_*.json"))
    for bf in cand_batches:
        if bf.name.startswith("judge_redispatch_"):
            continue
        try:
            b_data = json.loads(bf.read_text(encoding="utf-8"))
            raw_items = b_data.get("items", []) if isinstance(b_data, dict) else (b_data if isinstance(b_data, list) else [])
            for itm in raw_items:
                if isinstance(itm, dict):
                    iid = str(itm.get("item_id") or itm.get("question_id") or itm.get("id"))
                    if iid in missing_set and iid not in seen_ids:
                        seen_ids.add(iid)
                        # Blind copy: ensure answer keys are absent
                        blind_item = {
                            "item_id": iid,
                            "question_id": itm.get("question_id") or iid,
                            "interaction_type": itm.get("interaction_type") or itm.get("question_type") or "multiple_choice",
                            "stem": itm.get("stem") or itm.get("stem_es") or "",
                            "stem_es": itm.get("stem_es") or itm.get("stem") or "",
                        }
                        if "options" in itm:
                            # Strip any is_correct flags
                            clean_opts = []
                            for opt in itm["options"]:
                                if isinstance(opt, dict):
                                    clean_opts.append({
                                        "id": opt.get("id") or opt.get("option_id", ""),
                                        "content": opt.get("content", ""),
                                    })
                            blind_item["options"] = clean_opts
                        if "answer_contract" in itm:
                            blind_item["answer_contract"] = itm["answer_contract"]
                        if "graph" in itm:
                            blind_item["graph"] = itm["graph"]
                        missing_items.append(blind_item)
        except Exception as e:
            logger.warning("Could not parse batch %s for re-dispatch: %s", bf, e)

    # Slice missing items into batches of <= max_items_per_judge (default 12)
    redispatch_batches: List[Path] = []
    num_batches = max(1, math.ceil(len(missing_items) / max_items_per_judge))
    batch_size = math.ceil(len(missing_items) / num_batches)

    for b_idx in range(num_batches):
        chunk = missing_items[b_idx * batch_size : (b_idx + 1) * batch_size]
        batch_path = verif_dir / f"judge_redispatch_batch_{b_idx + 1:02d}.json"
        batch_path.write_text(json.dumps(chunk, indent=2, ensure_ascii=False), encoding="utf-8")
        redispatch_batches.append(batch_path)

        # Also write to work/ root for compatibility
        work_batch_path = work / f"judge_redispatch_batch_{b_idx + 1:02d}.json"
        work_batch_path.write_text(json.dumps(chunk, indent=2, ensure_ascii=False), encoding="utf-8")

    # Consolidated re-dispatch file
    consolidated_p = verif_dir / "judge_redispatch_batch.json"
    consolidated_p.write_text(json.dumps(missing_items, indent=2, ensure_ascii=False), encoding="utf-8")

    # Save redispatch manifest in work/dispatch/
    dispatch_dir = work / "dispatch"
    dispatch_dir.mkdir(parents=True, exist_ok=True)
    manifest_p = dispatch_dir / "judge_redispatch_manifest.json"
    manifest_payload = {
        "redispatch_needed": True,
        "missing_count": len(missing_items),
        "missing_item_ids": [m["item_id"] for m in missing_items],
        "batch_count": len(redispatch_batches),
        "batches": [p.as_posix() for p in redispatch_batches],
        "consolidated_batch": consolidated_p.as_posix(),
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    manifest_p.write_text(json.dumps(manifest_payload, indent=2, ensure_ascii=False), encoding="utf-8")

    # Generate Subagents array for re-dispatch
    subagents = []
    for b_idx, b_path in enumerate(redispatch_batches, start=1):
        for j_num in (1, 2):
            subagents.append({
                "TypeName": "c2c_blind_judge",
                "Role": f"Blind Judge Re-dispatch Batch {b_idx:02d} - Judge {j_num}",
                "Model": "flash",
                "Prompt": (
                    f"You are Blind Judge {j_num} for Re-dispatch Batch {b_idx:02d}. "
                    f"Your work order is `{b_path.as_posix()}`. Read it first with `view_file`. "
                    f"Finalize strictly with: `DONE: verification/judge_responses_redispatch_{b_idx:02d}_{j_num}.json`."
                ),
            })

    logger.info("Emitted %d judge re-dispatch batches for %d missing items in %s", len(redispatch_batches), len(missing_items), work)
    return {
        "redispatch_needed": True,
        "missing_count": len(missing_items),
        "batches": [p.as_posix() for p in redispatch_batches],
        "consolidated_batch": consolidated_p.as_posix(),
        "Subagents": subagents,
    }


def compare_judge_responses(
    responses: Optional[Union[Dict[str, Any], List[Dict[str, Any]], str, Path]] = None,
    ground_truth: Optional[Dict[str, Dict[str, Any]]] = None,
    cycle: int = 1,
    work_dir: Optional[Union[str, Path]] = None,
) -> Dict[str, Any]:
    """Compares judge answers against ground truth answer keys and records discordances.
    
    Automatically discovers and merges all work/judge_responses_*.json when responses is None
    or a directory path.
    
    Args:
        responses: Judge responses dict `{item_id: answer}`, list, or path to file/directory.
        ground_truth: Ground truth mapping loaded from judge_ground_truth.json.
        cycle: Current correction cycle number (1 to 3).
        work_dir: Optional working directory for response discovery and ground truth loading.

    Returns:
        Evaluation report dictionary containing agreement rate and discordances.
    """
    raw_responses_list: List[Any] = []
    resolved_work_dir: Optional[Path] = None

    if work_dir is not None:
        resolved_work_dir = Path(work_dir)
    elif isinstance(responses, (str, Path)) and Path(responses).is_dir():
        resolved_work_dir = Path(responses)

    if responses is None or (isinstance(responses, (str, Path)) and Path(responses).is_dir()):
        if resolved_work_dir is None:
            raise ValueError("Either responses or work_dir must be provided")
        # Discover all judge_responses_*.json and judge_responses.json
        cand_files = sorted(resolved_work_dir.glob("judge_responses_*.json"))
        verif_dir = resolved_work_dir / "verification"
        if verif_dir.is_dir():
            for vf in sorted(verif_dir.glob("judge_responses_*.json")):
                if vf.name not in [cf.name for cf in cand_files]:
                    cand_files.append(vf)
        main_resp = resolved_work_dir / "judge_responses.json"
        if main_resp.is_file() and main_resp not in cand_files:
            cand_files.append(main_resp)
        verif_main = verif_dir / "judge_responses.json"
        if verif_main.is_file() and verif_main not in cand_files:
            cand_files.append(verif_main)
        for f in cand_files:
            try:
                raw_responses_list.append(json.loads(f.read_text(encoding="utf-8")))
            except Exception as e:
                logger.warning("Failed to load judge response file %s: %s", f, e)
    elif isinstance(responses, (str, Path)) and Path(responses).is_file():
        raw_responses_list.append(json.loads(Path(responses).read_text(encoding="utf-8")))
    elif isinstance(responses, (list, dict)):
        raw_responses_list.append(responses)
    elif responses is not None:
        raw_responses_list.append(responses)

    # Normalize and merge responses to dict {item_id: answer}
    resp_map: Dict[str, Any] = {}
    for raw in raw_responses_list:
        if isinstance(raw, list):
            for r in raw:
                iid = r.get("item_id")
                ans = r.get("answer") if "answer" in r else r.get("response")
                if iid:
                    resp_map[iid] = ans
        elif isinstance(raw, dict):
            dict_data = raw.get("responses", raw) if "responses" in raw and isinstance(raw["responses"], dict) else raw
            for k, v in dict_data.items():
                if isinstance(v, dict) and ("answer" in v or "response" in v):
                    resp_map[k] = v.get("answer", v.get("response"))
                else:
                    resp_map[k] = v

    if ground_truth is None:
        if resolved_work_dir:
            gt_p = resolved_work_dir / "judge_ground_truth.json"
            if gt_p.is_file():
                ground_truth = json.loads(gt_p.read_text(encoding="utf-8"))
        if ground_truth is None:
            raise ValueError("ground_truth mapping must be provided or judge_ground_truth.json present in work_dir")

    total = len(ground_truth)
    agreed = 0
    discordances: List[Dict[str, Any]] = []

    for item_id, gt in ground_truth.items():
        user_ans = resp_map.get(item_id)
        itype = gt.get("interaction_type", "multiple_choice_7_options")
        is_match = False
        reason = ""

        if user_ans is None:
            is_match = False
            reason = "Missing response from judge"
        elif itype == "multiple_choice_7_options":
            # Normalize option letters (removing opt_/OPT_ prefixes) and content text
            u_letter = _normalize_option_letter(user_ans)
            gt_letter = _normalize_option_letter(gt.get("correct_letter", ""))
            gt_content = gt.get("correct_content", "")

            if u_letter and gt_letter and u_letter == gt_letter:
                is_match = True
            elif _normalize_str(user_ans) == _normalize_str(gt_content):
                is_match = True
            else:
                is_match = False
                reason = f"Judge selected '{user_ans}' (letter '{u_letter}') but expected letter '{gt_letter}' ({gt_content})"

        elif itype == "fill_in_the_blank":
            gt_val = gt.get("correct_value")
            gt_canon = gt.get("canonical_algebraic")
            gt_equivs = gt.get("accepted_equivalents", [])
            raw_tol = gt.get("tolerance") or gt.get("answer_contract", {}).get("tolerance") or 0.01
            try:
                tol = float(raw_tol)
            except (ValueError, TypeError):
                tol = 0.01

            if _is_numeric_equal(user_ans, gt_val, tol=tol):
                is_match = True
            elif gt_canon and _is_numeric_equal(user_ans, gt_canon, tol=tol):
                is_match = True
            elif gt_canon and _normalize_str(user_ans) == _normalize_str(gt_canon):
                is_match = True
            elif _normalize_str(user_ans) == _normalize_str(gt_val):
                is_match = True
            elif any(_is_numeric_equal(user_ans, eq, tol=tol) for eq in gt_equivs):
                is_match = True
            elif any(_normalize_str(user_ans) == _normalize_str(eq) for eq in gt_equivs):
                is_match = True
            else:
                is_match = False
                reason = f"Judge provided '{user_ans}' but expected '{gt_val}' (or {gt_canon})"

        elif itype == "multiple_select":
            gt_letters = set(_normalize_option_letter(x) for x in gt.get("correct_letters", []))
            gt_contents = set(_normalize_str(c) for c in gt.get("correct_contents", []))

            # User ans might be list of letters or comma-separated string
            if isinstance(user_ans, list):
                raw_items = [str(x).strip() for x in user_ans]
            elif isinstance(user_ans, str):
                s = user_ans.strip()
                if s.startswith("[") and s.endswith("]"):
                    try:
                        parsed = json.loads(s)
                        if isinstance(parsed, list):
                            raw_items = [str(x).strip() for x in parsed]
                        else:
                            raw_items = [s]
                    except Exception:
                        raw_items = [x.strip() for x in re.split(r"[,;\s]+", s) if x.strip()]
                else:
                    raw_items = [x.strip() for x in re.split(r"[,;\s]+|\band\b|\by\b", s) if x.strip()]
            else:
                raw_items = []

            u_letters = set()
            u_contents = set()
            for item in raw_items:
                nl = _normalize_option_letter(item)
                if len(nl) == 1 and nl.isalpha():
                    u_letters.add(nl)
                u_contents.add(_normalize_str(item))

            if u_letters and u_letters == gt_letters:
                is_match = True
            elif u_contents and u_contents == gt_contents:
                is_match = True
            else:
                is_match = False
                reason = f"Judge selected {raw_items} (letters: {sorted(u_letters)}) but expected {sorted(gt_letters)}"

        if is_match:
            agreed += 1
        else:
            discordances.append({
                "item_id": item_id,
                "template_id": gt.get("template_id"),
                "competency_id": gt.get("competency_id"),
                "interaction_type": itype,
                "judge_response": user_ans,
                "expected": (
                    gt.get("correct_letter")
                    or gt.get("correct_value")
                    or gt.get("correct_letters")
                ),
                "reason": reason,
                "cycle": cycle,
            })

    agreement_rate = (agreed / total) if total > 0 else 1.0
    passed = agreement_rate >= 0.95 and len(discordances) <= (total * 0.05)

    affected_templates = sorted(list(set(d["template_id"] for d in discordances)))

    report_data = {
        "cycle": cycle,
        "total_items": total,
        "agreed_items": agreed,
        "agreement_rate": round(agreement_rate, 4),
        "passed": passed,
        "status": "passed" if passed else "disagreements",
        "disagreements": discordances,
        "discordances": discordances,
        "affected_template_ids": affected_templates,
        "can_retry": (cycle < MAX_CORRECTION_CYCLES and not passed),
        "max_cycles_reached": (cycle >= MAX_CORRECTION_CYCLES),
    }

    if resolved_work_dir:
        try:
            completeness = check_judge_completeness(resolved_work_dir)
            report_data["completeness"] = completeness
            if not completeness.get("is_complete", True) and completeness.get("total_missing_items", 0) > 0:
                report_data["truncated_warning"] = (
                    f"Incomplete evaluation detected: {completeness['total_missing_items']} missing/truncated items."
                )
        except Exception as e:
            logger.warning("Could not execute check_judge_completeness: %s", e)

        try:
            (resolved_work_dir / "judge_report.json").write_text(
                json.dumps(report_data, indent=2, ensure_ascii=False),
                encoding="utf-8",
            )
        except Exception as e:
            logger.warning("Failed to write canonical judge_report.json: %s", e)

    return report_data


def main() -> None:
    """CLI utility for judge batch generation and comparison."""
    parser = argparse.ArgumentParser(description="Blind Judge Verifier for Parametric Templates.")
    subparsers = parser.add_subparsers(dest="action", required=True)

    # prepare subcommand
    prep = subparsers.add_parser("prepare", help="Generate blind judge batch WITHOUT answer keys")
    prep.add_argument("--templates", required=True, help="Path to template file or directory")
    prep.add_argument("--work-dir", required=True, help="Working directory for judge artifacts")
    prep.add_argument("--cta", help="Optional path to cta.json for distractor mappings")
    prep.add_argument(
        "--items-per-competency",
        type=int,
        default=2,
        help="Stratified sample count per competency (default: 2, <=0 for unstratified)",
    )
    prep.add_argument(
        "--ready-only",
        action="store_true",
        default=False,
        help="Only evaluate templates whose competencies have not yet been evaluated",
    )

    # split subcommand
    split_p = subparsers.add_parser("split", help="Split judge_batch.json into stratified batches")
    split_p.add_argument("--work-dir", required=True, help="Working directory containing judge_batch.json")
    split_p.add_argument("--max-judges", type=int, default=8, help="Maximum number of judges (default: 8)")
    split_p.add_argument("--items-per-judge", type=int, default=12, help="Target items per judge (default: 12)")

    # check-completeness subcommand
    chk = subparsers.add_parser("check-completeness", help="Detect truncated or missing judge responses")
    chk.add_argument("--work-dir", required=True, help="Working directory containing judge batches and responses")

    # emit-redispatch subcommand
    redisp = subparsers.add_parser("emit-redispatch", help="Emit blind re-dispatch batches for missing items")
    redisp.add_argument("--work-dir", required=True, help="Working directory containing judge batches and responses")
    redisp.add_argument("--max-items-per-judge", type=int, default=12, help="Max items per judge batch (default: 12)")

    # compare subcommand
    comp = subparsers.add_parser("compare", help="Compare judge responses against ground truth")
    comp.add_argument("--responses", required=False, default=None, help="Path to judge responses JSON file or directory")
    comp.add_argument("--work-dir", required=True, help="Working directory containing judge_ground_truth.json")
    comp.add_argument("--cycle", type=int, default=1, help="Current correction cycle (1-3)")

    args = parser.parse_args()

    if args.action == "prepare":
        batch_p, truth_p = generate_judge_batch(
            templates_path=args.templates,
            work_dir=args.work_dir,
            cta_path=args.cta,
            items_per_competency=args.items_per_competency,
            ready_only=args.ready_only,
        )
        print(f"Generated judge batch: {batch_p}")
        print(f"Generated ground truth: {truth_p}")

    elif args.action == "split":
        split_batches = split_judge_batch(
            work_dir=args.work_dir,
            max_judges=args.max_judges,
            items_per_judge=args.items_per_judge,
        )
        print(f"Generated {len(split_batches)} split judge batches in {args.work_dir}:")
        for sb in split_batches:
            print(f"  * {sb}")

    elif args.action == "check-completeness":
        comp_res = check_judge_completeness(args.work_dir)
        print(json.dumps(comp_res, indent=2, ensure_ascii=False))
        if not comp_res["is_complete"]:
            sys.exit(2)

    elif args.action == "emit-redispatch":
        redisp_res = emit_judge_redispatch(args.work_dir, max_items_per_judge=args.max_items_per_judge)
        print(json.dumps(redisp_res, indent=2, ensure_ascii=False))

    elif args.action == "compare":
        truth_p = Path(args.work_dir) / "judge_ground_truth.json"
        if not truth_p.is_file():
            print(f"Error: {truth_p} not found.", file=sys.stderr)
            sys.exit(1)

        gt = json.loads(truth_p.read_text(encoding="utf-8"))
        resps = Path(args.responses) if args.responses else None

        report = compare_judge_responses(responses=resps, ground_truth=gt, cycle=args.cycle, work_dir=args.work_dir)
        report_p = Path(args.work_dir) / f"judge_report_cycle_{args.cycle}.json"
        report_p.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")

        print("==================================================")
        print(f"JUDGE EVALUATION CYCLE {args.cycle}/{MAX_CORRECTION_CYCLES}")
        print(f"Agreement Rate: {report['agreement_rate'] * 100:.1f}% ({report['agreed_items']}/{report['total_items']})")
        print(f"Status: {'PASSED' if report['passed'] else 'DISCORDANCES DETECTED'}")
        if report["discordances"]:
            print(f"Discordant Templates ({len(report['affected_template_ids'])}): {report['affected_template_ids']}")
            for d in report["discordances"][:5]:
                print(f"  - [{d['item_id']}] {d['reason']}")
        print(f"Report written to: {report_p}")
        print("==================================================")

        if not report["passed"]:
            if report["can_retry"]:
                print(f"Cycle {args.cycle} failed. Re-run after repairing affected templates (Cycle {args.cycle + 1}).")
                sys.exit(2)
            else:
                print("Max correction cycles reached with remaining discordances.")
                sys.exit(1)


if __name__ == "__main__":
    main()
