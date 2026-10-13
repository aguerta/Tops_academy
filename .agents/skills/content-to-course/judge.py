"""Independent Blind Judge Module for content-to-course v2.

Generates blind judge question batches (WITHOUT answer keys or solutions) for 2 instances
per template, evaluates judge responses against ground truth answer keys, and manages
correction cycles (maximum 3 cycles).

Zero domain logic: agnostically operates on templates conforming to template.schema.json.
"""

from __future__ import annotations

import argparse
import json
import logging
import math
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

# Ensure skill directory is in sys.path
skill_dir = Path(__file__).parent.resolve()
if str(skill_dir) not in sys.path:
    sys.path.insert(0, str(skill_dir))

from engine.assemble import assemble_question
from engine.sandbox import execute_sandbox_instance

logger = logging.getLogger("judge")
MAX_CORRECTION_CYCLES = 3


def _load_templates(templates_path: Union[str, Path]) -> List[Dict[str, Any]]:
    """Loads all template objects from a JSON file or directory of JSON files."""
    path = Path(templates_path)
    templates: List[Dict[str, Any]] = []

    if path.is_file():
        content = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(content, dict):
            if "templates" in content:
                for t in content["templates"]:
                    if "competency_id" not in t and "competency_id" in content:
                        t["competency_id"] = content["competency_id"]
                    templates.append(t)
            else:
                templates.append(content)
        elif isinstance(content, list):
            templates.extend(content)
    elif path.is_dir():
        for file in sorted(path.glob("*.json")):
            try:
                data = json.loads(file.read_text(encoding="utf-8"))
                if isinstance(data, dict):
                    if "templates" in data:
                        for t in data["templates"]:
                            if "competency_id" not in t and "competency_id" in data:
                                t["competency_id"] = data["competency_id"]
                            templates.append(t)
                    else:
                        templates.append(data)
                elif isinstance(data, list):
                    templates.extend(data)
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

    Returns:
        Tuple of (path_to_judge_batch_json, path_to_ground_truth_json).
    """
    work = Path(work_dir)
    work.mkdir(parents=True, exist_ok=True)

    templates = _load_templates(templates_path)
    if not templates:
        raise ValueError(f"No templates found in path: {templates_path}")

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

        # Assemble full question
        assembled = assemble_question(
            template=template,
            gen_result=gen_res,
            competency_id=comp_id,
            question_index=inst_idx,
            cta_distractors_map=cta_distractors_map,
            seed=seed,
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

    batch_path = work / "judge_batch.json"
    batch_path.write_text(json.dumps(judge_batch_items, indent=2, ensure_ascii=False), encoding="utf-8")

    truth_path = work / "judge_ground_truth.json"
    truth_path.write_text(json.dumps(ground_truth, indent=2, ensure_ascii=False), encoding="utf-8")

    logger.info("Generated judge batch with %d items at %s", len(judge_batch_items), batch_path)
    return batch_path, truth_path


def split_judge_batch(
    work_dir: Union[str, Path],
    max_judges: int = 4,
    items_per_judge: int = 40,
) -> List[Path]:
    """Splits work/judge_batch.json into stratified batches work/judge_batch_{idx:02d}.json.
    
    Args:
        work_dir: Working directory containing judge_batch.json.
        max_judges: Maximum number of split batches / judges.
        items_per_judge: Target item count per judge.

    Returns:
        List of Paths to generated judge_batch_{idx:02d}.json files.
    """
    work = Path(work_dir)
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
    num_judges = min(max_judges, max(1, math.ceil(total_items / items_per_judge))) if items_per_judge > 0 else max_judges
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

    generated_paths: List[Path] = []
    for idx, b_items in enumerate(buckets):
        out_p = work / f"judge_batch_{idx + 1:02d}.json"
        out_p.write_text(json.dumps(b_items, indent=2, ensure_ascii=False), encoding="utf-8")
        generated_paths.append(out_p)

    logger.info("Split %d items across %d judge batches in %s", total_items, num_judges, work)
    return generated_paths


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
        main_resp = resolved_work_dir / "judge_responses.json"
        if main_resp.is_file() and main_resp not in cand_files:
            cand_files.append(main_resp)
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

    # split subcommand
    split_p = subparsers.add_parser("split", help="Split judge_batch.json into stratified batches")
    split_p.add_argument("--work-dir", required=True, help="Working directory containing judge_batch.json")
    split_p.add_argument("--max-judges", type=int, default=4, help="Maximum number of judges (default: 4)")
    split_p.add_argument("--items-per-judge", type=int, default=40, help="Target items per judge (default: 40)")

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
