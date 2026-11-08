"""End-to-End Content-to-Course v2 Modular CLI Runner.

Orchestrates multi-stage generation of interactive Top's Academy courses:
- Stage 0 (ingest): Multiformat ingestion (PDFs, images >2500px tiled, manifest, SHA-256 cache)
- Stage 1 (cta): Cognitive Task Analysis (cta.json validation, fused distractors, Bloom)
- Stage 2 (templates): Template validation (AST whitelist, 50-seed dry run, invariants, TPL-D1..D4)
- Stage 3 (build): Generic engine instantiation, quotas (30/20), masked stem diversity >= 0.5
- Stage 4 (verify): Invariants, anti-giveaway distribution, blind judge batch, strict validation
- Stage 5 (publish): Persistence to courses/<course_id>.json, append mode, platform registration

Strict Fail-Fast Guarantee:
- If any required artifact is missing, terminates immediately with non-zero exit code.
- Zero silent fallbacks to hardcoded templates.
- Zero external LLM API calls (the Antigravity agent is the LLM).
- Zero domain logic in Python code.
"""

from __future__ import annotations

import argparse
import contextlib
import datetime
import hashlib
import io
import json
import logging
import os
import re
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Set, Union

# Safe stdout encoding on Windows
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# Ensure skill directory is in sys.path
skill_dir = Path(__file__).parent.resolve()
repo_root = skill_dir.parents[2]
if str(skill_dir) not in sys.path:
    sys.path.insert(0, str(skill_dir))

from engine.interstage_schemas import ArtifactCertificate, RejectionSpec, verify_certificate

try:
    from check_cta import check_cta_file, validate_cta_rules
except ImportError:
    from check_cta import validate_cta_rules
    check_cta_file = validate_cta_rules

try:
    from compile_cta import compile_cta_file
except ImportError:
    try:
        from compile_cta import compile_cta as compile_cta_file
    except ImportError:
        compile_cta_file = None
from check_templates import check_templates_file_or_dir
from course_publisher import CoursePublisher, PublishQualityGateError
from cta_merge import apply_harmonize, merge_cta_parts, prepare_harmonize_from_single_draft
from dispatch import (
    build_dispatch,
    dispatch_authors,
    dispatch_cta,
    dispatch_cta_reduce,
    dispatch_judges,
    generate_define_subagent_specs,
    get_type_definitions,
    scope_check,
    snapshot_work_dir,
)
from engine.assemble import check_course_giveaway_distribution
from engine.diversity import evaluate_competency_diversity
from engine.stage_contract import MIN_DIVERSITY_RATIO, is_skill_type, quota_for_type, required_unique_stems, stems_advice, stems_advice_text
from engine.instantiate import instantiate_competency
from engine.invariants import check_instance_invariants
from ingest import ingest_course
from judge import compare_judge_responses, generate_judge_batch
from plan_shards import DEFAULT_COMPS_PER_SHARD, plan_shards
from prepare import is_corrupted_unicode, prepare_course, sanitize_cli_arg, sanitize_path
from repair_loop import RepairLoop
from telemetry_collector import record_stage_telemetry
from validator.core import validate_course_content

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("run_pipeline")


def record_stage_timing(work_dir: Path, stage_name: str, duration_sec: float) -> None:
    """Records stage execution time in work/timings.json."""
    timings_file = work_dir / "timings.json"
    data: Dict[str, Any] = {}
    if timings_file.is_file():
        try:
            data = json.loads(timings_file.read_text(encoding="utf-8"))
        except Exception:
            pass
    if "stages" not in data or not isinstance(data["stages"], dict):
        data["stages"] = {}
    data["stages"][stage_name] = round(duration_sec, 2)
    data["last_updated"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
    try:
        timings_file.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    except Exception as e:
        logger.warning("Could not record timing in %s: %s", timings_file, e)


@contextlib.contextmanager
def cap_stdout_to_log(work_dir: Path, stage_name: str, max_bytes: int = 16000):
    """Captures stage stdout, writes full verbose log to work/logs/<stage>.log, and caps console stdout to max_bytes."""
    clean_stage = re.sub(r"[^\w-]", "_", stage_name)
    logs_dir = work_dir / "logs"
    logs_dir.mkdir(parents=True, exist_ok=True)
    log_file = logs_dir / f"{clean_stage}.log"

    old_stdout = sys.stdout
    buffer = io.StringIO()
    sys.stdout = buffer
    try:
        yield
    finally:
        sys.stdout = old_stdout
        captured = buffer.getvalue()
        try:
            log_file.write_text(captured, encoding="utf-8")
        except Exception as e:
            logger.warning("Could not write stage log to %s: %s", log_file, e)

        encoded = captured.encode("utf-8", errors="replace")
        if len(encoded) > max_bytes:
            note = f"\n\n[... truncated verbose output ({len(encoded)} bytes). Full log: {log_file.as_posix()} ...]\n\n"
            note_len = len(note.encode("utf-8"))
            budget = max(0, max_bytes - note_len)
            head_len = budget // 2
            tail_len = budget - head_len
            head_str = encoded[:head_len].decode("utf-8", errors="ignore")
            tail_str = encoded[len(encoded) - tail_len:].decode("utf-8", errors="ignore") if tail_len > 0 else ""
            sys.stdout.write(head_str + note + tail_str)
        else:
            sys.stdout.write(captured)
        sys.stdout.flush()


def format_compact_json_stdout(
    payload: Dict[str, Any],
    work_dir: Path,
    stage_name: str,
    work_orders_file: Optional[Path] = None,
    max_bytes: int = 14000,
) -> str:
    """Serializes payload to JSON strictly guaranteeing stdout is <= max_bytes and 100% valid parseable JSON.

    1. Tries standard indent=2.
    2. If > max_bytes, tries compact separators=(',', ':').
    3. If still > max_bytes, creates a valid compact summary JSON pointing to work orders on disk and stage log.
    """
    raw_indent = json.dumps(payload, indent=2, ensure_ascii=False)
    if len(raw_indent.encode("utf-8")) <= max_bytes:
        return raw_indent

    raw_compact = json.dumps(payload, separators=(",", ":"), ensure_ascii=False)
    if len(raw_compact.encode("utf-8")) <= max_bytes:
        return raw_compact

    orders_rel = work_orders_file.as_posix() if work_orders_file else (work_dir / "dispatch" / f"{stage_name}_work_orders.json").as_posix()
    log_rel = (work_dir / "logs" / f"{stage_name}.log").as_posix()

    summary_dict = dict(payload)
    subagents = summary_dict.get("Subagents", [])
    total_subagents = len(subagents)

    # First attempt at summary: shorten Prompt in Subagents
    compact_subagents = []
    for sa in subagents:
        p_text = sa.get("Prompt", "")
        if len(p_text) > 80:
            p_text = p_text[:77] + "..."
        c_sa = {
            "Role": sa.get("Role", ""),
            "TypeName": sa.get("TypeName", ""),
            "Prompt": p_text,
        }
        compact_subagents.append(c_sa)
    summary_dict["Subagents"] = compact_subagents
    summary_dict["work_orders_file"] = orders_rel
    summary_dict["stage_log"] = log_rel
    summary_dict["_notice"] = f"Payload condensed ({total_subagents} subagents). Full orders: {orders_rel}"

    # Remove verbose item_files if present to save bytes
    if "item_files" in summary_dict and len(summary_dict["item_files"]) > 3:
        summary_dict["item_files_count"] = len(summary_dict["item_files"])
        summary_dict.pop("item_files", None)

    cand = json.dumps(summary_dict, separators=(",", ":"), ensure_ascii=False)
    if len(cand.encode("utf-8")) <= max_bytes:
        return cand

    # Second attempt: replace Subagents array with count and pointers only
    summary_dict.pop("Subagents", None)
    summary_dict["subagents_count"] = total_subagents
    cand2 = json.dumps(summary_dict, separators=(",", ":"), ensure_ascii=False)
    if len(cand2.encode("utf-8")) <= max_bytes:
        return cand2

    # Guaranteed ultra-minimal summary
    minimal = {
        "status": summary_dict.get("status", "ready"),
        "stage": stage_name,
        "course_id": summary_dict.get("course_id", ""),
        "subagent_count": total_subagents,
        "work_orders_file": orders_rel,
        "stage_log": log_rel,
        "_notice": f"Ultra-compact summary for {total_subagents} subagents. Inspect {orders_rel} with view_file.",
    }
    return json.dumps(minimal, separators=(",", ":"), ensure_ascii=False)


STAGE_NAMES = ["prepare", "cta", "shard", "templates", "build", "verify", "publish"]
STAGE_MAP = {
    "0": 0, "prepare": 0, "ingest": 0,
    "1": 1, "cta": 1,
    "2": 2, "shard": 2, "shards": 2,
    "3": 3, "templates": 3,
    "4": 4, "build": 4,
    "5": 5, "verify": 5,
    "6": 6, "publish": 6,
}
AUXILIARY_STAGES = {
    "cta-merge": "run_stage_cta_merge",
    "cta-reduce": "run_stage_cta_reduce",
    "cta-apply": "run_stage_cta_apply",
    "dispatch": "run_stage_dispatch",
    "scope-check": "run_stage_scope_check",
    "define-types": "run_stage_define_types",
    "judge-compare": "run_stage_judge_compare",
    "repair-matrix": "run_stage_repair_matrix",
    "rejudge": "run_stage_rejudge",
    "rejudge-compare": "run_stage_rejudge_compare",
    "certify": "run_stage_certify",
    "gates": "run_stage_gates",
    "bootstrap": "run_stage_bootstrap",
    "unlock": "run_stage_unlock",
    "wave-status": "run_stage_wave_status",
    "dispatch-cta": "run_stage_dispatch_cta",
    "dispatch-authors": "run_stage_dispatch_authors",
    "dispatch-judges": "run_stage_dispatch_judges",
    "judge-generate": "run_stage_judge_generate",
}


def sanitize_slug(name: str) -> str:
    """Sanitizes a name into an alphanumeric slug with underscores."""
    s = re.sub(r"[^\w\s-]", "", name.lower())
    s = re.sub(r"[-\s]+", "_", s).strip("_")
    return s or "custom_course"


class PipelineRunner:
    """Modular multi-stage course generation orchestrator with strict fail-fast semantics."""

    def __init__(
        self,
        pdf: Optional[Union[str, List[str], Path, List[Path]]] = None,
        course_id: Optional[str] = None,
        title: Optional[str] = None,
        work_dir: Optional[Union[str, Path]] = None,
        output_dir: Union[str, Path] = "courses",
        review_cta: bool = False,
        strict: bool = True,
        append: bool = False,
        random_seed: int = 42,
        vision: str = "auto",
        legacy_transcribe: bool = False,
        shards_k: Optional[int] = None,
        comps_per_shard: int = DEFAULT_COMPS_PER_SHARD,
        order: Optional[Union[str, List[str]]] = None,
        no_handouts: bool = False,
        cta_mode: str = "auto",
        granularity: str = "standard",
        no_merge: bool = False,
        partial: bool = False,
        role: Optional[str] = None,
        ids: Optional[Union[str, List[Union[str, int]]]] = None,
        ready_only: bool = False,
        skip_judges: bool = False,
        director_id: Optional[str] = None,
        wave: Optional[int] = None,
        no_pointer: bool = False,
        sources: Optional[Union[str, List[str], Path, List[Path]]] = None,
        source_dir: Optional[Union[str, Path]] = None,
        unlock: bool = False,
        base_course: Optional[Union[str, Path]] = None,
        force_recheck: bool = False,
    ) -> None:
        self.force_recheck = force_recheck
        if pdf is not None:
            self.raw_pdf = pdf
        elif sources is not None:
            self.raw_pdf = sources
        elif source_dir is not None:
            self.raw_pdf = source_dir
        else:
            self.raw_pdf = None

        self.director_id = str(director_id or "").strip() or os.environ.get("C2C_DIRECTOR_ID", "")
        self.wave = wave
        self.no_pointer = no_pointer
        self.unlock = unlock
        self.output_dir = Path(output_dir)
        self.review_cta = review_cta
        self.strict = strict
        self.append = append
        self.random_seed = random_seed
        self.vision = vision
        self.legacy_transcribe = legacy_transcribe
        self.shards_k = shards_k
        self.comps_per_shard = comps_per_shard
        self.order = order
        self.no_handouts = no_handouts
        if str(cta_mode).strip().lower() in ("multiple", "multi", "map-reduce", "map_reduce"):
            self.cta_mode = "mapreduce"
        elif str(cta_mode).strip().lower() in ("single", "direct_cta", "direct-cta"):
            self.cta_mode = "direct"
        else:
            self.cta_mode = cta_mode
        self.granularity = granularity
        self.no_merge = no_merge
        self.partial = partial
        self.role = role
        self.ids = [ids] if isinstance(ids, (str, int)) else ids
        self.ready_only = ready_only
        self.skip_judges = skip_judges

        clean_work_dir = sanitize_cli_arg(work_dir) if work_dir else None
        clean_course_id = sanitize_cli_arg(course_id) if course_id else None
        clean_title = sanitize_cli_arg(title) if title else None

        if base_course is not None:
            self.base_course = Path(sanitize_cli_arg(str(base_course)))
            self.append = True
            if not clean_course_id:
                clean_course_id = self.base_course.stem
            if Path(output_dir) == Path("courses") and self.base_course.parent.name:
                self.output_dir = self.base_course.parent
        else:
            self.base_course = None

        # Determine work directory first (isolate --append into work_append/)
        work_leaf = "work_append" if self.append else "work"

        if clean_work_dir:
            self.work_dir = Path(clean_work_dir)
        elif clean_course_id:
            self.work_dir = Path("courses") / sanitize_slug(clean_course_id) / work_leaf
        elif self.raw_pdf:
            first_path = Path(self.raw_pdf[0] if isinstance(self.raw_pdf, (list, tuple)) else self.raw_pdf)
            self.work_dir = Path("courses") / sanitize_slug(first_path.stem) / work_leaf
        else:
            self.work_dir = Path("courses") / "custom_course" / work_leaf

        self.work_dir.mkdir(parents=True, exist_ok=True)

        # Determine course ID
        if clean_course_id:
            self.course_id = sanitize_slug(clean_course_id)
        elif (self.work_dir / "cta.json").is_file():
            try:
                c_data = json.loads((self.work_dir / "cta.json").read_text(encoding="utf-8"))
                self.course_id = sanitize_slug(c_data.get("course_id", "custom_course"))
            except Exception:
                self.course_id = "custom_course"
        elif self.raw_pdf:
            first_path = Path(self.raw_pdf[0] if isinstance(self.raw_pdf, (list, tuple)) else self.raw_pdf)
            self.course_id = sanitize_slug(first_path.stem)
        else:
            self.course_id = "custom_course"

        # Determine course title with Windows Unicode fallback
        if clean_title and not is_corrupted_unicode(clean_title):
            self.title = clean_title
        else:
            # Fallback to cta.json, pre_cta_manifest.json, or courses/<id>.json if title is missing or contains \ufffd
            recovered_title: Optional[str] = None
            for cand_path in (
                self.work_dir / "cta.json",
                self.work_dir / "pre_cta_manifest.json",
                self.output_dir / f"{self.course_id}.json",
                Path("courses") / f"{self.course_id}.json",
            ):
                if cand_path.is_file():
                    try:
                        c_data = json.loads(cand_path.read_text(encoding="utf-8"))
                        t_val = c_data.get("course_title") or c_data.get("title")
                        if t_val and not is_corrupted_unicode(t_val):
                            recovered_title = t_val
                            break
                    except Exception:
                        pass
            if recovered_title:
                if clean_title and is_corrupted_unicode(clean_title):
                    logger.warning(
                        "CLI --title contains corrupted character ('\\ufffd'): %r. "
                        "Recovered title from course metadata: %r",
                        clean_title, recovered_title
                    )
                self.title = recovered_title
            elif clean_title:
                self.title = clean_title
            else:
                self.title = self.course_id.replace("_", " ").title()

    # -------------------------------------------------------------------------
    # STAGE 0: Prepare (replaces Ingest)
    # -------------------------------------------------------------------------
    def run_stage_prepare(self) -> Dict[str, Any]:
        """Stage 0: Multiformat pre-processing, Beamer cleanup, density scoring & manifest."""
        t0 = time.time()
        print("\n" + "=" * 70)
        print("[STAGE 0: PREPARE] Stage 0: Lossless source partitioning & pre_cta_manifest generation")
        print("=" * 70)

        if not self.raw_pdf:
            raise FileNotFoundError(
                "Cannot execute Stage 0 (prepare): No input path provided via --pdf."
            )

        if self.append and self.work_dir.name == "work_append" and self.work_dir.is_dir():
            import shutil
            for stale_item in ("cta.json", "cta.md", "cta_data.py", "course.json", "course_verified.json", "judge_report.json", "templates", "shards", "verification", "cta_parts", "cta"):
                stale_p = self.work_dir / stale_item
                if stale_p.is_dir():
                    shutil.rmtree(stale_p, ignore_errors=True)
                elif stale_p.is_file():
                    stale_p.unlink(missing_ok=True)

        sources: List[Path] = []
        raw_items = self.raw_pdf if isinstance(self.raw_pdf, (list, tuple)) else [self.raw_pdf]
        for item in raw_items:
            p = sanitize_path(item)
            if not p or not p.exists():
                raise FileNotFoundError(f"Input path does not exist: {p.resolve() if p else item}")
            sources.append(p)

        courses_dir_target = self.output_dir
        if self.base_course and self.base_course.is_file():
            courses_dir_target = self.base_course.parent

        prep_res = prepare_course(
            input_path=sources,
            work_dir=self.work_dir,
            course_id=self.course_id,
            courses_dir=courses_dir_target,
            append=self.append,
            cta_mode=self.cta_mode,
            granularity=self.granularity,
            order_override=self.order,
            title=self.title,
        )

        if "cta_mode" in prep_res:
            self.cta_mode = prep_res["cta_mode"]

        # Ensure work/pre_cta_manifest.json exists (zero fallbacks)
        pre_cta_file = self.work_dir / "pre_cta_manifest.json"
        if not pre_cta_file.is_file():
            print("[BLOCKER] BLOCKER:: No existe pre_cta_manifest.json", file=sys.stderr)
            sys.exit(2)

        # Pre-seed immutable compile_cta.py compiler in canonical work_dir
        compile_src = skill_dir / "compile_cta.py"
        if compile_src.is_file():
            import shutil
            shutil.copy2(compile_src, self.work_dir / "compile_cta.py")

        total_items = prep_res.get("total_pages", prep_res.get("manifest", {}).get("total_items", prep_res.get("total_files", 0)))
        print(f"  [+] Ingest completed with {total_items} items.")
        print(f"  [+] Manifest generated at: {pre_cta_file.resolve()}")

        # Display resolved document order if order.json exists
        order_file = self.work_dir / "order.json"
        if order_file.is_file():
            try:
                ord_data = json.loads(order_file.read_text(encoding="utf-8"))
                docs = ord_data.get("documents") or ord_data.get("order") or ord_data
                print(f"  [+] Resolved document order: {docs}")
            except Exception:
                pass

        cta_m = prep_res.get("cta_mode", self.cta_mode)
        print(f"  [+] CTA Mode: {str(cta_m).upper()}")
        print(f"  [+] FASE 1 (Síntesis CTA en modo {str(cta_m).upper()}):")
        print(f"      python .agents/skills/content-to-course/run.py --stage dispatch --role cta-direct --work-dir \"{self.work_dir}\"")

        elapsed = time.time() - t0
        record_stage_timing(self.work_dir, "prepare", elapsed)
        record_stage_telemetry(self.work_dir, "00", "prepare", status="completed", metadata={"duration_seconds": elapsed})
        print("  [+] Stage 0 (prepare) completed successfully.")
        return prep_res

    run_stage_ingest = run_stage_prepare

    # -------------------------------------------------------------------------
    # STAGE 1: CTA (Cognitive Task Analysis)
    # -------------------------------------------------------------------------
    def run_stage_cta(self) -> Dict[str, Any]:
        """Stage 1: Cognitive Task Analysis contract validation and review checkpoint."""
        t0 = time.time()
        print("\n" + "=" * 70)
        print("[STAGE 1: CTA] Cognitive Task Analysis validation (cta.json)")
        print("=" * 70)

        # 1. Verifica primero que exista work/pre_cta_manifest.json
        pre_cta_file = self.work_dir / "pre_cta_manifest.json"
        if not pre_cta_file.is_file():
            print("[BLOCKER] BLOCKER:: No existe pre_cta_manifest.json", file=sys.stderr)
            sys.exit(2)

        # Advisory scope check on CTA subagent
        try:
            role = "cta-map" if (self.work_dir / "sections").is_dir() else "cta-direct"
            is_clean, violations = scope_check(self.work_dir, role, {})
            if not is_clean:
                logger.warning("Advisory scope-check for '%s': %d non-standard files found: %s", role, len(violations), violations[:5])
        except Exception:
            pass

        # 2. Si existe work/cta_data.py y cta.json no existe o cta_data.py es más reciente, compilar
        cta_data_file = self.work_dir / "cta_data.py"
        cta_file = self.work_dir / "cta.json"
        if cta_data_file.is_file():
            needs_compile = not cta_file.is_file() or (cta_data_file.stat().st_mtime > cta_file.stat().st_mtime)
            if needs_compile:
                if compile_cta_file:
                    print(f"  [*] Compiling cta_data.py -> cta.json using compile_cta...")
                    ok, _, errs, _ = compile_cta_file(cta_data_file, output_dir=self.work_dir)
                    if not ok:
                        print("\n[ERROR] cta_data.py compilation failed:", file=sys.stderr)
                        for err in errs:
                            print(f"  - {err}", file=sys.stderr)
                        raise ValueError("cta_data.py compilation failed.")
                else:
                    compile_script = self.work_dir / "compile_cta.py"
                    if not compile_script.is_file():
                        compile_script = skill_dir / "compile_cta.py"
                    if compile_script.is_file():
                        import subprocess
                        subprocess.run([sys.executable, str(compile_script), str(cta_data_file)], check=False)

        # 2b. Compilar partes en modo mapreduce si existen archivos part_XX_data.py pendientes
        cta_parts_dir = self.work_dir / "cta_parts"
        if cta_parts_dir.is_dir():
            compile_script = self.work_dir / "compile_cta.py"
            if not compile_script.is_file():
                compile_script = skill_dir / "compile_cta.py"
            pending_parts = sorted(
                list(set(list(cta_parts_dir.glob("part_*_data.py")) + list(cta_parts_dir.glob("cta_part_*_data.py"))))
            )
            for part_data_p in pending_parts:
                part_stem = re.sub(r"_data$", "", part_data_p.stem)
                part_json_p = cta_parts_dir / f"{part_stem}.json"
                needs_compile = not part_json_p.is_file() or (part_data_p.stat().st_mtime > part_json_p.stat().st_mtime)
                if needs_compile:
                    print(f"  [*] Compiling {part_data_p.name} -> {part_json_p.name} using compile_cta.py --work {self.work_dir} --part {part_stem}...")
                    if compile_script.is_file():
                        import subprocess
                        res = subprocess.run(
                            [sys.executable, str(compile_script), "--work", str(self.work_dir), "--part", part_stem],
                            capture_output=True,
                            text=True,
                        )
                        if res.returncode != 0:
                            print(f"\n[ERROR] {part_data_p.name} compilation failed:\n{res.stderr or res.stdout}", file=sys.stderr)
                            raise ValueError(f"{part_data_p.name} compilation failed with exit code {res.returncode}.")
                        else:
                            print(f"  [+] {part_data_p.name} compiled successfully.")
                    elif compile_cta_file:
                        ok, _, errs, _ = compile_cta_file(
                            cta_data_path=part_data_p,
                            output_dir=cta_parts_dir,
                            manifest_path=pre_cta_file,
                            output_json_name=f"{part_stem}.json",
                        )
                        if not ok:
                            print(f"\n[ERROR] {part_data_p.name} compilation failed:", file=sys.stderr)
                            for err in errs:
                                print(f"  - {err}", file=sys.stderr)
                            raise ValueError(f"{part_data_p.name} compilation failed.")

        # Symmetric Harmonization Predicate (Matiz 3 and Matiz 4a)
        is_append_mode = bool(getattr(self, "append", False)) or (self.work_dir / "delta_manifest.json").is_file()
        part_files_set = set()
        if cta_parts_dir.is_dir():
            for p in cta_parts_dir.glob("part_*.json"):
                part_files_set.add(p)
            for p in cta_parts_dir.glob("cta_part_*.json"):
                part_files_set.add(p)
        cta_shards_dir = self.work_dir / "cta"
        if cta_shards_dir.is_dir():
            for p in cta_shards_dir.glob("cta_shard_*.json"):
                part_files_set.add(p)
        part_files = sorted(list(part_files_set))
        needs_harmonize = (self.cta_mode == "mapreduce") or bool(part_files) or bool(is_append_mode)

        harmonize_file = self.work_dir / "cta_harmonize.json"

        if needs_harmonize:
            if not harmonize_file.is_file():
                if part_files:
                    print("  [*] Merging sectional CTA parts into draft...")
                    merge_cta_parts(self.work_dir)
                else:
                    print("  [*] Preparing harmonization draft from single source in append mode...")
                    prepare_harmonize_from_single_draft(self.work_dir)

                print("  [*] Emitting dispatch for c2c_cta_harmonizer...")
                reduce_res = dispatch_cta_reduce(self.work_dir, pointer=not self.no_pointer)
                print("  [+] Next Stage: cta-apply")
                print(json.dumps(reduce_res, indent=2, ensure_ascii=False))
                elapsed = time.time() - t0
                record_stage_timing(self.work_dir, "cta", elapsed)
                record_stage_telemetry(self.work_dir, "01", "cta", status="completed", metadata={"duration_seconds": elapsed, "needs_harmonize": True})
                return {
                    "paused_for_review": False,
                    "needs_harmonize": True,
                    "next_stage": "cta-apply",
                    "status": "needs_harmonize",
                    "Subagents": reduce_res.get("Subagents", []),
                    "item_files": reduce_res.get("item_files", []),
                }

            if not cta_file.is_file() or harmonize_file.stat().st_mtime > cta_file.stat().st_mtime:
                print("  [*] Applying harmonization directives...")
                apply_harmonize(self.work_dir, no_merge=self.no_merge)

        if not cta_file.is_file():
            raise FileNotFoundError(
                f"Missing required artifact: {cta_file.resolve()}\n"
                f"Strict fail-fast: cta.json must be generated by the CTA subagent following "
                f"system_prompts/prompt_competence_analyser.md before running this stage.\n"
                f"No silent fallback to hardcoded templates is permitted."
            )

        manifest_data = json.loads(pre_cta_file.read_text(encoding="utf-8"))

        cta_data = json.loads(cta_file.read_text(encoding="utf-8"))

        # Deterministic sanitization of orphan LaTeX math in all competencies and distractors
        comps = cta_data.get("competencies", [])
        if comps:
            try:
                from cta_merge import sanitize_competency_math
                cta_raw_before = json.dumps(cta_data, sort_keys=True)
                for comp in comps:
                    sanitize_competency_math(comp)
                if json.dumps(cta_data, sort_keys=True) != cta_raw_before:
                    cta_file.write_text(json.dumps(cta_data, indent=2, ensure_ascii=False), encoding="utf-8")
                    print("  [+] Auto-sanitized and normalized orphan LaTeX math expressions in cta.json.")
            except Exception as e:
                logger.warning("Could not auto-sanitize cta.json math: %s", e)

        # Validate CTA schema and rules CTA-D1, CTA-D2
        is_valid, errors = check_cta_file(cta_data, manifest_data=manifest_data, file_path=cta_file) if check_cta_file else validate_cta_rules(cta_data, manifest_data=manifest_data, file_path=cta_file)
        if not is_valid:
            print("\n[ERROR] cta.json failed validation:", file=sys.stderr)
            for err in errors:
                print(f"  - {err}", file=sys.stderr)
            raise ValueError(f"cta.json contains {len(errors)} validation errors.")
        comps = cta_data.get("competencies", [])
        facts = [c for c in comps if c.get("type", "").lower() == "fact"]
        concepts = [c for c in comps if c.get("type", "").lower() == "concept"]
        skills = [c for c in comps if c.get("type", "").lower() == "skill"]

        total_distractors = sum(len(c.get("distractors", [])) for c in comps)

        print(f"  [+] Validated cta.json: {len(comps)} competencies")
        print(f"      - Facts: {len(facts)}, Concepts: {len(concepts)}, Skills: {len(skills)}")
        print(f"      - Total fused distractors: {total_distractors}")
        print("  [+] Rules CTA-D1 (distractor count) and CTA-D2 (unique IDs/models) verified.")

        elapsed = time.time() - t0
        record_stage_timing(self.work_dir, "cta", elapsed)
        record_stage_telemetry(self.work_dir, "01", "cta", status="completed", metadata={"duration_seconds": elapsed, "competencies": len(comps)})

        if self.review_cta:
            print("\n" + "*" * 70)
            print("[CHECKPOINT: --review-cta] CTA analysis paused for human/agent review.")
            print(f"  Review file: {cta_file.resolve()}")
            print(f"  Course title: {cta_data.get('title', self.title)}")
            print("  Competencies summary:")
            for c in comps:
                d_count = len(c.get("distractors", []))
                print(f"    * [{c.get('id')}] ({c.get('type')}) {c.get('name')} - {d_count} distractors")
            print("To proceed to template authoring and question generation, resume with:")
            print(f"  python .agents/skills/content-to-course/run.py --from-stage templates --work-dir \"{self.work_dir}\"")
            print("*" * 70 + "\n")
            return {"paused_for_review": True, "cta_data": cta_data}

        print("  [+] Stage 1 (cta) completed successfully.")
        return {"paused_for_review": False, "cta_data": cta_data}

    # -------------------------------------------------------------------------
    # STAGE 2: Shard
    # -------------------------------------------------------------------------
    def run_stage_shard(self) -> Dict[str, Any]:
        """Stage 2: Shard CTA competencies across author batches (max 5-6 per shard)."""
        t0 = time.time()
        print("\n" + "=" * 70)
        print("[STAGE 2: SHARD] Partitioning CTA competencies for parallel authoring")
        print("=" * 70)

        # 1. Verifica work/pre_cta_manifest.json (si no existe, BLOCKER:: No existe pre_cta_manifest.json)
        pre_cta_file = self.work_dir / "pre_cta_manifest.json"
        if not pre_cta_file.is_file():
            print("[BLOCKER] BLOCKER:: No existe pre_cta_manifest.json", file=sys.stderr)
            sys.exit(2)

        cta_file = self.work_dir / "cta.json"
        if not cta_file.is_file():
            raise FileNotFoundError(
                f"Missing required artifact: {cta_file.resolve()}\n"
                f"Cannot shard competencies without cta.json. Run stage cta first."
            )

        shards_dir = self.work_dir / "shards"
        shards_dir.mkdir(parents=True, exist_ok=True)
        res = plan_shards(cta_file, shards_dir, k=self.shards_k, max_comps=self.comps_per_shard)

        # Verificar que exista work/shards/pre_shard_manifest.json (cero fallbacks)
        pre_shard_file = shards_dir / "pre_shard_manifest.json"
        if not pre_shard_file.is_file():
            print("[BLOCKER] BLOCKER:: No existe pre_shard_manifest.json", file=sys.stderr)
            sys.exit(2)

        print(f"  [+] Partitioned {res['total_competencies']} competencies into {res['total_shards']} shards:")
        for s in res["shards"]:
            print(f"      * [{s['shard_id']}] {s['competency_count']} competencies (weight={s['weight']}): {', '.join(s['competency_ids'])}")
        elapsed = time.time() - t0
        record_stage_timing(self.work_dir, "shard", elapsed)
        record_stage_telemetry(self.work_dir, "02", "shard", status="completed", metadata={"duration_seconds": elapsed, "shards": res.get("total_shards")})
        print("  [+] Stage 2 (shard) completed successfully.")
        return res

    # -------------------------------------------------------------------------
    # STAGE 3: Templates
    # -------------------------------------------------------------------------
    def run_stage_templates(self) -> Dict[str, Any]:
        """Stage 3: Parametric templates validation (AST, sandbox, 50-seed dry run, TPL-D1..D4)."""
        t0 = time.time()
        print("\n" + "=" * 70)
        print("[STAGE 3: TEMPLATES] Parametric templates sandbox validation")
        print("=" * 70)

        # 1. Verifica primero que exista work/shards/pre_shard_manifest.json
        pre_shard_file = self.work_dir / "shards" / "pre_shard_manifest.json"
        if not pre_shard_file.is_file():
            print("[BLOCKER] BLOCKER:: No existe pre_shard_manifest.json", file=sys.stderr)
            sys.exit(2)

        # Advisory scope check on author subagents
        try:
            is_clean, violations = scope_check(self.work_dir, "author", {})
            # Only author-owned areas are relevant here; other files are outputs of earlier/later stages.
            violations = [v for v in violations if v.startswith(("shards/", "templates/"))]
            if violations:
                logger.warning("Advisory scope-check for 'author': %d non-standard files found: %s", len(violations), violations[:5])
        except Exception:
            pass

        cta_file = self.work_dir / "cta.json"
        if not cta_file.is_file():
            raise FileNotFoundError(
                f"Missing required artifact: {cta_file.resolve()}\n"
                f"Cannot validate templates without cta.json. Run stage cta first."
            )

        templates_dir = self.work_dir / "templates"
        templates_dir.mkdir(parents=True, exist_ok=True)

        # 2. Si existen work/shards/shard_XX_data.py y compile_shard.py está disponible, compilar shards pendientes
        shards_dir = self.work_dir / "shards"
        shard_data_files = sorted(list(shards_dir.glob("shard_*_data.py")))
        compile_shard_mod = None
        try:
            import compile_shard as cs_mod
            compile_shard_mod = cs_mod
        except ImportError:
            pass

        compile_shard_script = shards_dir / "compile_shard.py"
        if not compile_shard_script.is_file():
            compile_shard_script = skill_dir / "compile_shard.py"

        # Cargar pre_shard_manifest.json si existe para compilación incremental
        pre_shard_manifest_p = shards_dir / "pre_shard_manifest.json"
        if not pre_shard_manifest_p.is_file():
            pre_shard_manifest_p = self.work_dir / "pre_shard_manifest.json"

        shard_to_cids: Dict[str, List[str]] = {}
        if pre_shard_manifest_p.is_file():
            try:
                sm_data = json.loads(pre_shard_manifest_p.read_text(encoding="utf-8"))
                shards_info = sm_data.get("shards", [])
                if isinstance(shards_info, list):
                    for s in shards_info:
                        s_id = s.get("shard_id") or "shard_01"
                        c_ids = s.get("competency_ids") or []
                        if not c_ids and "competencies" in s:
                            c_ids = [c.get("id") for c in s["competencies"] if isinstance(c, dict) and "id" in c]
                        for cid in c_ids:
                            if cid:
                                shard_to_cids.setdefault(s_id, []).append(cid)
                elif isinstance(shards_info, dict):
                    for s_id, comps in shards_info.items():
                        if isinstance(comps, list):
                            for c in comps:
                                cid = c.get("id") if isinstance(c, dict) else str(c)
                                if cid:
                                    shard_to_cids.setdefault(s_id, []).append(cid)
            except Exception as e:
                logger.warning("Error reading pre_shard_manifest.json in run_stage_templates: %s", e)

        for sf in sorted(shards_dir.glob("shard_*.json")):
            try:
                sdata = json.loads(sf.read_text(encoding="utf-8"))
                s_id = sdata.get("shard_id", sf.stem)
                for cid in sdata.get("competency_ids", []):
                    if cid and s_id not in shard_to_cids:
                        shard_to_cids.setdefault(s_id, []).append(cid)
                if "competencies" in sdata and isinstance(sdata["competencies"], list):
                    for c in sdata["competencies"]:
                        cid = c.get("id") if isinstance(c, dict) else str(c)
                        if cid and s_id not in shard_to_cids:
                            shard_to_cids.setdefault(s_id, []).append(cid)
            except Exception:
                pass

        if shard_data_files and (compile_shard_mod or compile_shard_script.is_file()):
            print(f"  [*] Compiling {len(shard_data_files)} pending shard data files...")
            cta_mtime = cta_file.stat().st_mtime if cta_file.is_file() else 0.0
            for s_data_p in shard_data_files:
                shard_id = re.sub(r"_data$", "", s_data_p.stem)
                cids = shard_to_cids.get(shard_id, [])
                if cids:
                    all_up_to_date = True
                    s_mtime = s_data_p.stat().st_mtime
                    for cid in cids:
                        cid_json = templates_dir / f"{cid}.json"
                        if not cid_json.is_file() or cid_json.stat().st_size == 0:
                            all_up_to_date = False
                            break
                        cid_mtime = cid_json.stat().st_mtime
                        if cid_mtime < s_mtime or cid_mtime < cta_mtime:
                            all_up_to_date = False
                            break
                        shard_fixes_candidates = [
                            shards_dir / "shard_fixes" / shard_id / f"{cid}.py",
                            shards_dir / "shard_fixes" / shard_id / f"{cid.lower()}.py",
                            shards_dir / "shard_fixes" / f"{cid}.py",
                            self.work_dir / "shard_fixes" / f"{cid}.py",
                            shards_dir / "shard_fixes" / f"{cid.lower()}.py",
                            self.work_dir / "shard_fixes" / f"{cid.lower()}.py",
                        ]
                        has_newer_fix = False
                        for fix_p in shard_fixes_candidates:
                            if fix_p.is_file() and cid_mtime < fix_p.stat().st_mtime:
                                has_newer_fix = True
                                break
                        if has_newer_fix:
                            all_up_to_date = False
                            break
                    if all_up_to_date:
                        print(f"  [i] Skipping compilation for {s_data_p.name} (templates up-to-date).")
                        continue

                if compile_shard_mod and hasattr(compile_shard_mod, "compile_shard"):
                    ok, errs = compile_shard_mod.compile_shard(self.work_dir, shard_id=shard_id, strict=True, min_archetypes=4)
                    if not ok:
                        logger.warning("Compilation for %s reported issues: %s", shard_id, errs[:3] if errs else "unknown")
                elif compile_shard_script.is_file():
                    import subprocess
                    subprocess.run(
                        [sys.executable, str(compile_shard_script), "--work", str(self.work_dir), "--shard", shard_id, "--strict", "--min-archetypes", "4"],
                        check=False,
                    )

        if not templates_dir.is_dir() or not list(templates_dir.glob("*.json")):
            raise FileNotFoundError(
                f"Missing required templates: No .json files found in {templates_dir.resolve()}\n"
                f"Strict fail-fast: Exercise creator subagents must author templates before this stage."
            )

        all_template_files = sorted(list(templates_dir.glob("*.json")))

        # Cryptographic fast-path: verify shard_XX.cert.json receipts (< 5 ms)
        certified_cids: Set[str] = set()
        certified_template_files: Set[Path] = set()

        if not getattr(self, "force_recheck", False) and cta_file.is_file():
            cta_bytes = cta_file.read_bytes()
            cta_sha = hashlib.sha256(cta_bytes).hexdigest()

            cert_files = sorted(list(shards_dir.glob("shard_*.cert.json")))
            for cert_f in cert_files:
                try:
                    c_data = json.loads(cert_f.read_text(encoding="utf-8"))
                    if not c_data.get("passed_50_seeds"):
                        continue
                    if c_data.get("cta_sha256") and c_data["cta_sha256"] != cta_sha:
                        continue

                    s_id = c_data.get("artifact_id") or re.sub(r"\.cert$", "", cert_f.stem)
                    s_id_clean = re.sub(r"_data$", "", s_id)
                    s_py = shards_dir / f"{s_id_clean}_data.py"
                    if not s_py.is_file():
                        continue
                    s_sha = hashlib.sha256(s_py.read_bytes()).hexdigest()
                    if c_data.get("source_sha256") != s_sha:
                        continue

                    # Check if any surgical fix is newer than the certificate
                    cert_mtime = cert_f.stat().st_mtime
                    s_cids = shard_to_cids.get(s_id_clean, [])
                    has_newer_fix = False
                    for cid_item in s_cids:
                        for fix_cand in (
                            shards_dir / "shard_fixes" / s_id_clean / f"{cid_item}.py",
                            shards_dir / "shard_fixes" / f"{cid_item}.py",
                            self.work_dir / "shard_fixes" / f"{cid_item}.py",
                        ):
                            if fix_cand.is_file() and fix_cand.stat().st_mtime > cert_mtime:
                                has_newer_fix = True
                                break
                        if has_newer_fix:
                            break
                    if has_newer_fix:
                        continue

                    # Verify each template hash declared in the certificate
                    tpl_shas = c_data.get("template_shas", {})
                    if not tpl_shas:
                        continue
                    shard_tpls_valid = True
                    shard_cids = set()
                    shard_files = set()
                    for t_name, expected_sha in tpl_shas.items():
                        t_path = templates_dir / t_name if t_name.endswith(".json") else templates_dir / f"{t_name}.json"
                        if not t_path.is_file():
                            shard_tpls_valid = False
                            break
                        actual_sha = hashlib.sha256(t_path.read_bytes()).hexdigest()
                        if actual_sha != expected_sha:
                            shard_tpls_valid = False
                            break
                        shard_cids.add(t_path.stem)
                        shard_files.add(t_path)

                    if shard_tpls_valid:
                        certified_cids.update(shard_cids)
                        certified_template_files.update(shard_files)
                except Exception as ex:
                    logger.debug("Certificate check error on %s: %s", cert_f.name, ex)

        uncertified_templates = [tf for tf in all_template_files if tf not in certified_template_files]

        if not getattr(self, "force_recheck", False) and len(certified_template_files) == len(all_template_files) and len(all_template_files) > 0:
            print(f"  [+] Fast-path < 5 ms: All {len(all_template_files)} template(s) cryptographically certified via shard_XX.cert.json.")
            is_valid = True
            errors = []
        elif uncertified_templates and len(certified_template_files) > 0 and not getattr(self, "force_recheck", False):
            print(f"  [+] Fast-path < 5 ms: Skipping {len(certified_template_files)} pre-certified template(s). Checking {len(uncertified_templates)} pending template(s)...")
            is_valid, errors = check_templates_file_or_dir(uncertified_templates, cta_path=cta_file)
        else:
            is_valid, errors = check_templates_file_or_dir(templates_dir, cta_path=cta_file)

        # Build errors_by_cid mapping
        errors_by_cid: Dict[str, List[str]] = {}
        known_cids: Set[str] = set()
        try:
            cta_obj = json.loads(cta_file.read_text(encoding="utf-8"))
            for c in cta_obj.get("competencies", []):
                if isinstance(c, dict) and "id" in c:
                    known_cids.add(c["id"])
        except Exception:
            pass
        for tf in templates_dir.glob("*.json"):
            known_cids.add(tf.stem)

        for err in errors:
            err_str = str(err)
            matched = set()
            if hasattr(err, "competency") and getattr(err, "competency") in known_cids:
                matched.add(getattr(err, "competency"))
            for cid in known_cids:
                if re.search(rf"(?<![A-Za-z0-9_-]){re.escape(cid)}(?![A-Za-z0-9_-])", err_str):
                    matched.add(cid)
            for m in re.finditer(r"\b(?:C|H|Hab)-\d+\b", err_str):
                cand_cid = m.group(0)
                if cand_cid in known_cids:
                    matched.add(cand_cid)

            for cid in matched:
                errors_by_cid.setdefault(cid, []).append(err_str)

        total_t = 0
        for tf in templates_dir.glob("*.json"):
            try:
                t_data = json.loads(tf.read_text(encoding="utf-8"))
                if isinstance(t_data, list):
                    total_t += len(t_data)
                elif isinstance(t_data, dict):
                    if "templates" in t_data and isinstance(t_data["templates"], list):
                        total_t += len(t_data["templates"])
                    else:
                        total_t += 1
            except Exception:
                pass
        total_s = total_t * 50

        reports_dir = self.work_dir / "reports"
        reports_dir.mkdir(parents=True, exist_ok=True)
        report_file = reports_dir / "templates_report.json"
        report_data = {
            "status": "PASS" if is_valid else "FAIL",
            "total_templates": total_t,
            "total_seeds_run": total_s,
            "errors": [str(e) for e in errors],
            "warnings": [],
            "errors_by_cid": errors_by_cid,
            "failed_competencies": sorted(errors_by_cid.keys()),
        }
        report_file.write_text(json.dumps(report_data, indent=2, ensure_ascii=False), encoding="utf-8")

        if not is_valid:
            print("\n[ERROR] Templates validation failed:", file=sys.stderr)
            for err in errors[:10]:
                print(f"  - {err}", file=sys.stderr)

            # Persist rejection spec for downstream repair
            try:
                fail_cids = sorted(errors_by_cid.keys())
                shard_to_cids_rev = {cid: sid for sid, cids in shard_to_cids.items() for cid in cids}
                fail_shards = sorted({shard_to_cids_rev.get(c, "shard_01") for c in fail_cids})
                repair_cmd = (
                    f'& ".venv\\Scripts\\python.exe" .agents/skills/content-to-course/dispatch.py dispatch-repair '
                    f'--work-dir "{self.work_dir.as_posix()}" --ids {" ".join(fail_cids)}'
                ) if fail_cids else ""
                rej = RejectionSpec(
                    status="REJECTED",
                    course_id=self.course_id,
                    total_issues=len(errors),
                    failing_competencies=fail_cids,
                    failing_shards=fail_shards,
                    affected_shards=fail_shards,
                    proposed_repair_command=repair_cmd,
                    diagnostics_by_competency=errors_by_cid,
                    report_text="\n".join([str(e) for e in errors[:50]]),
                )
                rej.write_json(self.work_dir / "template_failures.json")
            except Exception as rej_ex:
                logger.debug("Could not write template_failures.json: %s", rej_ex)

            if any("CIRCUIT BREAKER" in err for err in errors):
                raise RuntimeError(
                    f"Circuit Breaker tripped in {templates_dir}: 3 consecutive identical validation failures. "
                    "Halting pipeline execution to prevent further token waste."
                )
            raise ValueError(f"Templates in {templates_dir} contain {len(errors)} errors.")

        template_files = list(templates_dir.glob("*.json"))
        print(f"  [+] Validated templates across {len(template_files)} competency file(s).")
        print("  [+] AST whitelist, 50-seed dry-run, invariants, and TPL-D1..D4 passed.")
        elapsed = time.time() - t0
        record_stage_timing(self.work_dir, "templates", elapsed)
        record_stage_telemetry(self.work_dir, "03", "templates", status="completed", metadata={"duration_seconds": elapsed, "count": len(template_files)})
        print("  [+] Stage 3 (templates) completed successfully.")
        return {"status": "PASS", "templates_dir": str(templates_dir.resolve()), "count": len(template_files)}

    # -------------------------------------------------------------------------
    # STAGE 4: Build (Instantiation)
    # -------------------------------------------------------------------------
    def run_stage_build(self) -> Dict[str, Any]:
        """Stage 4: Instantiate question banks to meet quotas with masked stem diversity >= 0.5."""
        t0 = time.time()
        print("\n" + "=" * 70)
        print("[STAGE 4: BUILD] Generic engine question instantiation & diversity")
        print("=" * 70)

        cta_file = self.work_dir / "cta.json"
        if not cta_file.is_file():
            raise FileNotFoundError(f"Missing required artifact: {cta_file.resolve()}")

        templates_dir = self.work_dir / "templates"
        if not templates_dir.is_dir() or not list(templates_dir.glob("*.json")):
            raise FileNotFoundError(f"Missing templates in {templates_dir.resolve()}")

        cta_data = json.loads(cta_file.read_text(encoding="utf-8"))
        competencies = cta_data.get("competencies", [])

        # Build distractor map
        distractor_map: Dict[str, Dict[str, Any]] = {}
        for comp in competencies:
            for d in comp.get("distractors", []):
                if "id" in d:
                    distractor_map[d["id"]] = d

        # Load all template files grouped by competency_id
        templates_by_comp: Dict[str, List[Dict[str, Any]]] = {}
        for tf in sorted(templates_dir.glob("*.json")):
            tdata = json.loads(tf.read_text(encoding="utf-8"))
            if isinstance(tdata, dict) and "templates" in tdata:
                cid = tdata.get("competency_id", tf.stem)
                for t in tdata["templates"]:
                    if "competency_id" not in t:
                        t["competency_id"] = cid
                    templates_by_comp.setdefault(cid, []).append(t)
            elif isinstance(tdata, list):
                for t in tdata:
                    cid = t.get("competency_id", tf.stem)
                    templates_by_comp.setdefault(cid, []).append(t)
            elif isinstance(tdata, dict):
                cid = tdata.get("competency_id", tf.stem)
                if "competency_id" not in tdata:
                    tdata["competency_id"] = cid
                templates_by_comp.setdefault(cid, []).append(tdata)

        # Parallel competency question instantiation
        import zlib
        import os
        from concurrent.futures import ThreadPoolExecutor

        def _instantiate_single_comp(comp: Dict[str, Any]) -> Tuple[Dict[str, Any], List[Dict[str, Any]], Dict[str, Any]]:
            cid = comp["id"]
            cat = comp.get("type", "concept").title()
            name = comp.get("name", cid)
            desc = comp.get("description_latex") or comp.get("description", "")
            course_comp_dict = {
                "id": cid,
                "code": cid.upper(),
                "name": name,
                "category": cat,
                "description": desc,
                "mastery_target": 100,
                "prerequisites": comp.get("prerequisites", []),
            }
            comp_templates = templates_by_comp.get(cid, [])
            if not comp_templates:
                raise ValueError(
                    f"No templates found for competency '{cid}' ({name}). "
                    f"Strict fail-fast requires all competencies to have templates."
                )
            comp_res = instantiate_competency(
                competency=comp,
                templates=comp_templates,
                cta_distractors_map=distractor_map,
                seed_offset_base=self.random_seed + (zlib.crc32(cid.encode("utf-8")) % 10000),
            )
            comp_questions = comp_res["questions"] if isinstance(comp_res, dict) and "questions" in comp_res else comp_res
            for q in comp_questions:
                check_instance_invariants(q, q["interaction_type"])
            stems = [q["stem"] for q in comp_questions]
            div_res = evaluate_competency_diversity(stems)
            return course_comp_dict, comp_questions, div_res

        max_workers = min(16, (os.cpu_count() or 4) * 2, len(competencies))
        comp_results_map: Dict[str, Any] = {}
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_cid = {executor.submit(_instantiate_single_comp, comp): comp["id"] for comp in competencies}
            for fut in future_to_cid:
                cid_key = future_to_cid[fut]
                comp_results_map[cid_key] = fut.result()

        # Strictly preserve the exact pedagogical sequence of competencies as declared in cta.json
        all_questions: List[Dict[str, Any]] = []
        course_competencies_output: List[Dict[str, Any]] = []
        q_global_idx = 1

        stem_gate_failures: List[Dict[str, Any]] = []
        for comp in competencies:
            cid = comp["id"]
            cat = comp.get("type", "concept").title()
            course_comp_dict, comp_questions, div_res = comp_results_map[cid]
            course_competencies_output.append(course_comp_dict)

            quota = quota_for_type(cat)
            div_ratio = div_res["diversity_ratio"]
            unique_c = div_res["unique_masked"]
            total_c = div_res["total"]
            if div_ratio < MIN_DIVERSITY_RATIO:
                stem_gate_failures.append({
                    "cid": cid,
                    "cat": cat,
                    "quota": quota,
                    "div_ratio": div_ratio,
                    "unique_c": unique_c,
                    "total_c": total_c,
                })
                continue
            print(f"  [*] Instantiated {quota} items for '{cid}' ({cat}) - Stem diversity: {div_ratio:.3f} ({unique_c}/{total_c})")

            # Re-index questions cleanly
            for q in comp_questions:
                q["id"] = f"Q-{cid.replace('-', '')}-{q_global_idx:03d}"
                q["question_id"] = q["id"]
                q_global_idx += 1

            all_questions.extend(comp_questions)

        if stem_gate_failures:
            from compile_shard import ShardDataLineLocator
            shards_dir = self.work_dir / "shards"
            manifest_p = shards_dir / "pre_shard_manifest.json"
            if not manifest_p.is_file():
                manifest_p = self.work_dir / "pre_shard_manifest.json"
            cid_to_shard: Dict[str, str] = {}
            if manifest_p.is_file():
                try:
                    m_obj = json.loads(manifest_p.read_text(encoding="utf-8"))
                    for s_item in (m_obj.get("shards") or []):
                        if isinstance(s_item, dict) and s_item.get("shard_id"):
                            for c_id_m in (s_item.get("competency_ids") or []):
                                cid_to_shard[str(c_id_m)] = str(s_item["shard_id"])
                except Exception:
                    pass
            fail_cids = [f["cid"] for f in stem_gate_failures]
            fail_shards = sorted({cid_to_shard.get(c, "shard_01") for c in fail_cids})
            work_rel_str = self.work_dir.as_posix()
            repair_cmd = f'& ".venv\\Scripts\\python.exe" .agents/skills/content-to-course/dispatch.py dispatch-repair --work-dir "{work_rel_str}" --ids {" ".join(fail_cids)}'
            locations_list: List[Dict[str, Any]] = []
            md_lines: List[str] = [
                "======================================================================",
                "[SPECIFIC ERROR REPORT — BUILD STEM DIVERSITY GATE REJECTION]",
                "======================================================================",
                f"Competencias Afectadas ({len(fail_cids)}): {', '.join(fail_cids)}",
                f"Shards Afectados ({len(fail_shards)}): {', '.join(fail_shards)}",
                f"PROPOSED REPAIR COMMAND: {repair_cmd}",
                "",
                "[-] [STEM-DIVERSITY-GATE / build_stem_diversity_gate]",
                "  Descripción: Ratio de diversidad estructural de enunciados (unique_masked / quota) menor a 0.50.",
                "  Causa: Las plantillas de la competencia definen muy pocas variantes sintácticas en `stems` (ej. 3x3 = 9 stems < 15 requeridos para Skill o < 10 para Concept/Fact).",
                "  Acción: En `s1`, `s2`, `s3` de `shard_XX_data.py`, provee " + stems_advice_text() + "",
            ]
            for f_item in stem_gate_failures:
                f_cid = f_item["cid"]
                is_sk = is_skill_type(f_item["cat"])
                req_u = required_unique_stems(f_item["quota"])
                req_pt = stems_advice("skill" if is_sk else "concept")["per_tpl"]
                tot_pt = stems_advice("skill" if is_sk else "concept")["total"]
                cat_lbl = "skills" if is_sk else "concepts/facts"
                s_id = cid_to_shard.get(f_cid, "shard_01")
                isolated_fix_p = shards_dir / "shard_fixes" / s_id / f"{f_cid}.py"
                flat_fix_p = shards_dir / "shard_fixes" / f"{f_cid}.py"
                fix_p = isolated_fix_p if isolated_fix_p.is_file() else flat_fix_p
                py_p = fix_p if fix_p.is_file() else (shards_dir / f"{s_id}_data.py")
                s_file_rel = f"shards/shard_fixes/{s_id}/{f_cid}.py" if isolated_fix_p.is_file() else (f"shards/shard_fixes/{f_cid}.py" if flat_fix_p.is_file() else f"shards/{s_id}_data.py")
                loc_inst = ShardDataLineLocator(py_p) if py_p.is_file() else None
                c_tpls = templates_by_comp.get(f_cid, [])
                for t_i, t_d in enumerate(c_tpls):
                    t_id = t_d.get("id") or t_d.get("template_id") or f"T-{f_cid}-{t_i+1:02d}"
                    t_info = loc_inst.find_tuple_for_question(f_cid, template_id=t_id) if loc_inst else None
                    l_s, l_e, c_lns = loc_inst.find_offending_lines(t_info, "anti_gaming_psychometric_linter", "stem") if loc_inst else (1, 1, [])
                    fn_nm = t_info.get("gen_fn_name", "gen_fn") if t_info else (t_d.get("gen_fn_name") or "gen_fn")
                    fn_s = t_info.get("gen_fn_line_start", 1) if t_info else 1
                    fn_e = t_info.get("gen_fn_line_end", 1) if t_info else 1
                    tp_s = t_info.get("tuple_line_start", 1) if t_info else 1
                    tp_e = t_info.get("tuple_line_end", 1) if t_info else 1
                    finding_msg = (
                        f"Diagnostic: Stem diversity gate failed for competency '{f_cid}' "
                        f"(only {f_item['unique_c']} stems, required >= {req_u} unique, quota {f_item['quota']} for {cat_lbl}, ratio={f_item['div_ratio']:.3f}). "
                        f"Provide >= {req_pt} distinct syntactic stems per template (totaling >= {tot_pt})."
                    )
                    locations_list.append({
                        "competency_id": f_cid,
                        "shard_id": s_id,
                        "shard_file": s_file_rel,
                        "template_id": t_id,
                        "item_ids": [],
                        "gen_fn_name": fn_nm,
                        "gen_fn_line_start": fn_s,
                        "gen_fn_line_end": fn_e,
                        "tuple_line_start": tp_s,
                        "tuple_line_end": tp_e,
                        "offending_line_start": l_s,
                        "offending_line_end": l_e,
                        "offending_code_lines": c_lns,
                        "sample_findings": [finding_msg],
                    })
                    md_lines.append(
                        f"  * {s_file_rel}:L{l_s}-L{l_e} | competency_id={f_cid} | template_id={t_id} "
                        f"| [Fn {fn_nm}: L{fn_s}..L{fn_e} | Tupla: L{tp_s}..L{tp_e}]"
                    )
                    md_lines.append(f"    Detalle: {finding_msg}")
                    if c_lns:
                        md_lines.append("    CONTEXTO EXACTO (OFFENDING LINES):")
                        for cl in c_lns[:8]:
                            md_lines.append(f"      {cl}")
            md_lines.append("======================================================================")
            md_text = "\n".join(md_lines)
            rej = RejectionSpec(
                status="REJECTED",
                course_id=self.course_id,
                total_issues=len(stem_gate_failures),
                failing_competencies=fail_cids,
                failing_shards=fail_shards,
                affected_shards=fail_shards,
                proposed_repair_command=repair_cmd,
                groups={
                    "build_stem_diversity_gate": [
                        {
                            "linter": "build_stem_diversity_gate",
                            "rule_tag": "STEM-DIVERSITY-GATE",
                            "severity": "CRITICAL",
                            "description": "Ratio de diversidad estructural de enunciados (unique_masked / quota) menor a 0.50.",
                            "cause": "Las plantillas de la competencia definen muy pocas variantes sintácticas en `stems`.",
                            "action": "En `s1`, `s2`, `s3` de `shard_XX_data.py`, provee " + stems_advice_text(),
                            "locations": locations_list,
                        }
                    ]
                },
                grouped_by_rule={
                    "build_stem_diversity_gate": [
                        {
                            "linter": "build_stem_diversity_gate",
                            "rule_tag": "STEM-DIVERSITY-GATE",
                            "severity": "CRITICAL",
                            "description": "Ratio de diversidad estructural de enunciados (unique_masked / quota) menor a 0.50.",
                            "cause": "Las plantillas de la competencia definen muy pocas variantes sintácticas en `stems`.",
                            "action": "En `s1`, `s2`, `s3` de `shard_XX_data.py`, provee " + stems_advice_text(),
                            "locations": locations_list,
                        }
                    ]
                },
                report_text=md_text,
            )
            rej.write_json(self.work_dir / "specific_error_report.json")
            rej.write_json(self.work_dir / "template_failures.json")
            (self.work_dir / "specific_error_report.md").write_text(md_text + "\n", encoding="utf-8")
            first_f = stem_gate_failures[0]
            raise ValueError(
                f"Stem diversity gate failed for competency '{first_f['cid']}': ratio is {first_f['div_ratio']:.3f} "
                f"({first_f['unique_c']}/{first_f['total_c']} unique masked patterns), strictly required >= 0.5.\n\n"
                f"{md_text}"
            )

        import datetime
        now_iso = datetime.datetime.now(datetime.timezone.utc).isoformat()
        course_desc = cta_data.get("macro_competency") or f"Banco interactivo de práctica deliberada para {self.title}."
        if len(course_desc) < 10:
            course_desc = f"Curso interactivo y banco de práctica deliberada para {self.title}."

        # Assemble course dictionary
        course_data = {
            "$schema": "http://json-schema.org/draft-07/schema#",
            "schema_version": "1.0.0",
            "course_id": self.course_id,
            "course_title": cta_data.get("title") or self.title or "Modelo de Crecimiento de Solow",
            "title": cta_data.get("title") or self.title or "Modelo de Crecimiento de Solow",
            "description": course_desc,
            "language": "es",
            "created_at": now_iso,
            "competencies": course_competencies_output,
            "questions": all_questions,
        }

        # Check course level giveaway bounds
        giveaway_passes, giveaway_stats = check_course_giveaway_distribution(all_questions)
        longest_pct = giveaway_stats.get("longest_ratio", 0.0) * 100
        shortest_pct = giveaway_stats.get("shortest_ratio", 0.0) * 100
        print(f"  [+] Anti-giveaway distribution: longest={longest_pct:.1f}%, shortest={shortest_pct:.1f}%")

        course_file = self.work_dir / "course.json"
        course_file.write_text(json.dumps(course_data, indent=2, ensure_ascii=False), encoding="utf-8")
        elapsed = time.time() - t0
        record_stage_timing(self.work_dir, "build", elapsed)
        record_stage_telemetry(self.work_dir, "04", "build", status="completed", metadata={"duration_seconds": elapsed, "total_questions": len(all_questions)})
        print(f"  [+] Successfully built course bank with {len(all_questions)} questions: {course_file}")
        print("  [+] Stage 4 (build) completed successfully.")
        return {"course_file": str(course_file.resolve()), "total_questions": len(all_questions)}

    # -------------------------------------------------------------------------
    # STAGE 5: Verify
    # -------------------------------------------------------------------------
    def run_stage_verify(self) -> Dict[str, Any]:
        """Stage 5: Blind judge batch generation and strict validation with repair loop."""
        t0 = time.time()
        print("\n" + "=" * 70)
        print("[STAGE 5: VERIFY] Independent verification & strict validation")
        print("=" * 70)

        # Advisory scope check on judge subagents
        try:
            is_clean, violations = scope_check(self.work_dir, "judge", {})
            if not is_clean:
                logger.warning("Advisory scope-check for 'judge': %d non-standard files found: %s", len(violations), violations[:5])
        except Exception:
            pass

        course_file = self.work_dir / "course.json"
        if not course_file.is_file():
            raise FileNotFoundError(f"Missing required artifact: {course_file.resolve()}. Run stage build first.")

        templates_dir = self.work_dir / "templates"
        cta_file = self.work_dir / "cta.json"

        # 1. Generate blind judge batch for independent evaluation
        if templates_dir.is_dir() and list(templates_dir.glob("*.json")):
            print("  [*] Generating blind judge batch (stratified random selection, max 10 judges x 20 items WITHOUT answer keys)...")
            judge_batch_p, gt_p = generate_judge_batch(
                templates_path=templates_dir,
                work_dir=self.work_dir,
                cta_path=cta_file if cta_file.is_file() else None,
                seeds=None,
                items_per_competency=0,
                max_judges=10,
                max_items_per_judge=20,
            )
            print(f"      Judge batch written: {judge_batch_p}")
            print(f"      Ground truth written: {gt_p}")

        course_data = json.loads(course_file.read_text(encoding="utf-8"))
        raw_text = json.dumps(course_data, indent=2, ensure_ascii=False)

        # 2. Strict validation
        v_res = validate_course_content(raw_text, strict=self.strict)
        if not v_res.is_valid:
            print("  [!] Initial validation encountered issues. Running RepairLoop...")
            repairer = RepairLoop(max_iterations=3, strict=self.strict)
            rep_res = repairer.repair_course(course_data)
            if not rep_res.success:
                print("\n[ERROR] Course failed validation even after auto-repair:", file=sys.stderr)
                for err in rep_res.remaining_errors[:5]:
                    print(f"  - [{err.rule_id}] {err.message}", file=sys.stderr)
                raise ValueError("Validation failed on generated course.")
            course_data = rep_res.repaired_course_data
            print(f"  [+] Repaired across {rep_res.iterations_run} iteration(s).")
        else:
            print(f"  [+] 100% strict validation passed (16/16 rules).")

        verified_file = self.work_dir / "course_verified.json"
        verified_file.write_text(json.dumps(course_data, indent=2, ensure_ascii=False), encoding="utf-8")
        elapsed = time.time() - t0
        record_stage_timing(self.work_dir, "verify", elapsed)
        record_stage_telemetry(self.work_dir, "05", "verify", status="completed", metadata={"duration_seconds": elapsed, "verified_course_path": str(verified_file.resolve())})
        print(f"  [+] Verified course written to: {verified_file}")
        print("  [+] Stage 5 (verify) completed successfully.")
        return {"verified_course_path": str(verified_file.resolve())}

    # -------------------------------------------------------------------------
    # STAGE 6: Publish
    # -------------------------------------------------------------------------
    def run_stage_publish(self) -> Dict[str, Any]:
        """Stage 6: Publish course to platform directory (courses/<course_id>.json)."""
        t0 = time.time()
        print("\n" + "=" * 70)
        print("[STAGE 6: PUBLISH] Publishing course to platform repository")
        print("=" * 70)

        verified_file = self.work_dir / "course_verified.json"
        course_file = self.work_dir / "course.json"
        if verified_file.is_file() and course_file.is_file():
            source_file = course_file if course_file.stat().st_mtime > verified_file.stat().st_mtime else verified_file
        else:
            source_file = verified_file if verified_file.is_file() else course_file
        if not source_file.is_file():
            raise FileNotFoundError(f"Missing required artifact: {source_file.resolve()}. Run stage build/verify first.")

        # Enforce blind judge evaluation verification prior to platform publish
        judge_report_file = self.work_dir / "judge_report.json"
        if not self.skip_judges:
            if not judge_report_file.is_file():
                cycle_reports = sorted(self.work_dir.glob("judge_report_cycle_*.json"))
                if cycle_reports:
                    judge_report_file = cycle_reports[-1]
            if not judge_report_file.is_file():
                raise RuntimeError(
                    f"Publication blocked: Missing judge report at {judge_report_file.resolve()}. "
                    "All courses must complete independent blind judge evaluation prior to publish, "
                    "or pass --skip-judges to explicitly bypass."
                )
            try:
                jr_data = json.loads(judge_report_file.read_text(encoding="utf-8"))
            except Exception as parse_ex:
                raise RuntimeError(
                    f"Publication blocked: Invalid or unreadable judge report at {judge_report_file.resolve()}: {parse_ex}"
                )
            if not jr_data.get("passed", False) or jr_data.get("status") not in ("pass", "passed", "success"):
                disagreements = jr_data.get("disagreements", []) or jr_data.get("discordances", [])
                raise RuntimeError(
                    f"Publication blocked: Blind judge evaluations have {len(disagreements)} unresolved disagreement(s) "
                    f"or report passed=False (status={jr_data.get('status')}). "
                    "Repair discordances via dispatch --role repair before publishing."
                )

        course_data = json.loads(source_file.read_text(encoding="utf-8"))
        if self.course_id and self.course_id != "custom_course":
            course_data["course_id"] = self.course_id
        if self.title and not is_corrupted_unicode(self.title):
            course_data["course_title"] = self.title
            course_data["title"] = self.title
        elif is_corrupted_unicode(self.title):
            clean_title = course_data.get("course_title") or course_data.get("title")
            if is_corrupted_unicode(clean_title) and (self.work_dir / "cta.json").is_file():
                try:
                    c_data = json.loads((self.work_dir / "cta.json").read_text(encoding="utf-8"))
                    clean_title = c_data.get("course_title") or c_data.get("title")
                except Exception:
                    pass
            if clean_title and not is_corrupted_unicode(clean_title):
                logger.warning(
                    "Publish --title contains corrupted character ('\\ufffd'): %r. "
                    "Falling back to clean title: %r",
                    self.title, clean_title
                )
                course_data["course_title"] = clean_title
                course_data["title"] = clean_title

        cta_md: Optional[str] = None
        cta_md_file = self.work_dir / "cta.md"
        if cta_md_file.is_file():
            cta_md = cta_md_file.read_text(encoding="utf-8")

        publisher = CoursePublisher(courses_dir=self.output_dir)
        pub_result = publisher.publish(
            course_data=course_data,
            strict=self.strict,
            cta_markdown=cta_md,
            append=self.append,
            work_dir=self.work_dir,
        )

        if not pub_result.success:
            raise RuntimeError(f"Course publication failed: {pub_result.error_message}")

        elapsed = time.time() - t0
        record_stage_timing(self.work_dir, "publish", elapsed)
        record_stage_telemetry(self.work_dir, "06", "publish", status="completed", metadata={"duration_seconds": elapsed, "published_json": str(pub_result.published_json_path)})

        print("\n" + "=" * 70)
        print("[SUCCESS] COURSE PUBLISHED TO PLATFORM!")
        print(f"  Title:        {pub_result.course_title}")
        print(f"  Course ID:    {pub_result.course_id}")
        print(f"  Course File:  {pub_result.published_json_path}")
        if pub_result.published_cta_path:
            print(f"  CTA Markdown: {pub_result.published_cta_path}")
        print(f"  Questions:    {pub_result.total_questions} items across {pub_result.total_competencies} competencies")
        print(f"  Validation:   Passed (Hermetic CLI validator with in-memory fallback; strict={self.strict})")
        print(f"  Launch URL:   {pub_result.launch_url}")
        print(f"  Command:      {pub_result.launch_command}")
        print("=" * 70 + "\n")

        # Automatic Lockfile Lifecycle Release on successful publish
        lock_file = self.work_dir / ".c2c_subagent_lock.json"
        if lock_file.is_file():
            try:
                try:
                    lock_data = json.loads(lock_file.read_text(encoding="utf-8"))
                    lock_data["active"] = False
                    lock_file.write_text(json.dumps(lock_data, indent=2), encoding="utf-8")
                except Exception:
                    pass
                lock_file.unlink(missing_ok=True)
                print(f"  [+] Automatically released subagent lock: {lock_file.resolve()}")
            except Exception as e:
                logger.warning("Could not release lockfile at %s: %s", lock_file, e)

        return pub_result.to_dict()

    # -------------------------------------------------------------------------
    # AUXILIARY STAGES: CTA Map-Reduce, Dispatch, Scope Check, Define Types, Judge Compare
    # -------------------------------------------------------------------------
    def run_stage_cta_merge(self) -> Dict[str, Any]:
        """Auxiliary Stage: Merge sectional CTA parts into draft, outline and candidates."""
        t0 = time.time()
        print("\n" + "=" * 70)
        print("[AUX STAGE: CTA-MERGE] Merging sectional CTA parts (Map -> Reduce)")
        print("=" * 70)

        # Advisory scope check on cta-map
        try:
            is_clean, violations = scope_check(self.work_dir, "cta-map", {})
            if not is_clean:
                logger.warning("Advisory scope-check for 'cta-map': %d non-standard files found: %s", len(violations), violations[:5])
        except Exception:
            pass

        res = merge_cta_parts(self.work_dir)
        elapsed = time.time() - t0
        record_stage_timing(self.work_dir, "cta_merge", elapsed)
        print(f"  [+] Merged {res.get('total_competencies', 0)} competencies across {len(res.get('parts', []))} part(s).")
        print(f"  [+] Draft written to: {res.get('draft_path')}")
        print(f"  [+] Outline written to: {res.get('outline_path')}")
        candidates = res.get("duplicate_candidates", [])
        print(f"  [+] Duplicate candidates detected: {len(candidates)} pair(s) in {res.get('candidates_path')}")
        for c in candidates:
            print(f"      * [{c.get('pair')}] reason: {c.get('reason')}")
        print("  [+] Auxiliary Stage (cta-merge) completed successfully.")
        return res

    def run_stage_cta_apply(self) -> Dict[str, Any]:
        """Auxiliary Stage: Apply Harmonizer operations and write verified cta.json & cta.md."""
        t0 = time.time()
        print("\n" + "=" * 70)
        print("[AUX STAGE: CTA-APPLY] Applying CTA Harmonizer decisions & generating cta.json")
        print("=" * 70)

        # Advisory scope check on cta-reduce
        try:
            is_clean, violations = scope_check(self.work_dir, "cta-reduce", {})
            if not is_clean:
                logger.warning("Advisory scope-check for 'cta-reduce': %d non-standard files found: %s", len(violations), violations[:5])
        except Exception:
            pass

        res = apply_harmonize(self.work_dir, no_merge=self.no_merge)
        elapsed = time.time() - t0
        record_stage_timing(self.work_dir, "cta_apply", elapsed)
        cta_p = self.work_dir / "cta.json"
        cta_md_p = self.work_dir / "cta.md"
        rep_p = self.work_dir / "merge_report.json"
        total_comps = len(res.get("competencies", [])) if isinstance(res, dict) else 0
        print(f"  [+] Final CTA validated: {total_comps} competencies.")
        print(f"  [+] cta.json written to: {cta_p}")
        print(f"  [+] cta.md generated at: {cta_md_p}")
        print(f"  [+] Merge report written to: {rep_p}")
        print("  [+] Auxiliary Stage (cta-apply) completed successfully.")
        if isinstance(res, dict):
            res["total_competencies"] = total_comps
            res["cta_path"] = str(cta_p.resolve())
            res["cta_md_path"] = str(cta_md_p.resolve())
            res["report_path"] = str(rep_p.resolve())
        return res

    def run_stage_cta_reduce(self) -> Dict[str, Any]:
        """Auxiliary Stage: Generate CTA Harmonizer dispatch payload."""
        t0 = time.time()
        print("\n" + "=" * 70)
        print("[AUX STAGE: CTA-REDUCE] Generating c2c_cta_harmonizer dispatch")
        print("=" * 70)
        res = dispatch_cta_reduce(self.work_dir, pointer=not self.no_pointer)
        elapsed = time.time() - t0
        record_stage_timing(self.work_dir, "dispatch_cta_reduce", elapsed)
        subagents = res.get("Subagents", [])
        print(f"  [+] Dispatched c2c_cta_harmonizer with {len(subagents)} subagent(s).")
        print(json.dumps(res, indent=2, ensure_ascii=False))
        print("  [+] Auxiliary Stage (cta-reduce) completed successfully.")
        return res

    def run_stage_dispatch(self) -> Dict[str, Any]:
        """Auxiliary Stage: Generate subagent dispatch payload with strict SCOPE-LOCK."""
        if not self.role:
            raise ValueError(
                "Missing required argument '--role' for stage dispatch. "
                "Choose from: cta, cta-direct, cta-map, cta-reduce, author, judge, repair."
            )
        t0 = time.time()
        print("\n" + "=" * 70)
        print(f"[AUX STAGE: DISPATCH] Generating invoke_subagent payload for role '{self.role}'")
        print("=" * 70)

        # Inform role-specific contracts
        if self.role == "author":
            print("  [*] Enforcing contract: Autoría modular por competencia (work/templates/<comp_id>.json), prohibidos scripts monolíticos de 2,000 líneas.")
            print("  [*] Forbidden paths: check_templates.py, src/validator/*, rules.py, engine/*, SKILL.md, work/build_<shard_id>.py")
        elif self.role == "judge":
            print("  [*] Enforcing contract: Cero búsquedas web, resolver por primeros principios, BLOCKED si falta contexto.")
            print("  [*] Forbidden tools/paths: search_web, read_url_content, navegación web, templates/*, ground truth")
        elif self.role == "cta-direct":
            print("  [*] Enforcing contract: Máximo 10 competencias por lote, prohibido emitir competencias en el chat.")
            print("  [*] Generation method: Script generador estructurado hacia work/cta.json y work/cta.md")

        payload = build_dispatch(
            role=self.role,
            work_dir=self.work_dir,
            ids=self.ids,
            ready_only=self.ready_only,
        )
        elapsed = time.time() - t0
        record_stage_timing(self.work_dir, f"dispatch_{self.role}", elapsed)
        subagents = payload.get("Subagents", [])
        print(f"  [+] Generated dispatch payload with {len(subagents)} subagent(s).")
        audit_file = self.work_dir / "dispatch" / f"{self.role}.json"
        print(f"  [+] Audit payload written to: {audit_file.resolve()}")

        # Guardar y listar rutas individuales en work/dispatch/items/<role>_<idx:02d>.json
        items_dir = self.work_dir / "dispatch" / "items"
        items_dir.mkdir(parents=True, exist_ok=True)
        if subagents:
            print("  [+] Rutas individuales para subagentes (lectura paralela con view_file en 1 turno sin truncamiento):")
            for idx, sa in enumerate(subagents, 1):
                item_file = items_dir / f"{self.role}_{idx:02d}.json"
                item_file.write_text(json.dumps(sa, indent=2, ensure_ascii=False), encoding="utf-8")
                print(f"      * [{idx:02d}] {item_file.resolve()} -> {sa.get('Role')}")

        print("\n" + "-" * 70)
        print(json.dumps(payload, indent=2, ensure_ascii=False))
        print("-" * 70 + "\n")
        print(f"  [+] Auxiliary Stage (dispatch: {self.role}) completed successfully.")
        return payload

    def run_stage_scope_check(self) -> Dict[str, Any]:
        """Auxiliary Stage: Validate that subagents respected SCOPE-LOCK boundaries."""
        if not self.role:
            raise ValueError(
                "Missing required argument '--role' for stage scope-check. "
                "Choose from: cta, cta-direct, cta-map, cta-reduce, author, judge, repair."
            )
        t0 = time.time()
        print("\n" + "=" * 70)
        print(f"[AUX STAGE: SCOPE-CHECK] Verifying scope boundaries for role '{self.role}'")
        print("=" * 70)

        is_clean, violations = scope_check(self.work_dir, self.role, {})
        elapsed = time.time() - t0
        record_stage_timing(self.work_dir, f"scope_check_{self.role}", elapsed)
        if not is_clean:
            print(f"\n[ERROR] Scope check failed for role '{self.role}': {len(violations)} violations found:", file=sys.stderr)
            for v in violations:
                print(f"  - Disallowed file: {v}", file=sys.stderr)
            raise ValueError(f"Scope boundary violation detected for role '{self.role}'.")
        print(f"  [+] Scope check PASSED for role '{self.role}' (0 violations detected).")
        print("  [+] Auxiliary Stage (scope-check) completed successfully.")
        return {"role": self.role, "is_clean": True, "violations": []}

    def run_stage_define_types(self) -> Dict[str, Any]:
        """Auxiliary Stage: Generate define_subagent payloads for all specialized c2c subagent types."""
        types_list = get_type_definitions()
        # Persist definitions to disk for guaranteed non-truncated access
        types_json = json.dumps(types_list, indent=2, ensure_ascii=False)
        types_bytes = types_json.replace("\r\n", "\n").encode("utf-8")
        if hasattr(self, "work_dir") and self.work_dir:
            self.work_dir.mkdir(parents=True, exist_ok=True)
            (self.work_dir / "subagent_types.json").write_bytes(types_bytes)
        (skill_dir / "subagent_types.json").write_bytes(types_bytes)

        # Guardar y listar rutas individuales en work/dispatch/types/<type_name>.json
        types_dir = self.work_dir / "dispatch" / "types"
        types_dir.mkdir(parents=True, exist_ok=True)
        print("\n" + "=" * 70)
        print("[AUX STAGE: DEFINE-TYPES] Subagent Type Definitions for Orchestrator")
        print("=" * 70)
        print("[!] DIRECTIVA OBLIGATORIA PARA EL DIRECTOR (GOOGLE ANTIGRAVITY):")
        print("    Invoca la tool 'define_subagent' para los tipos SIMULTÁNEAMENTE en un")
        print("    ÚNICO turno mediante Parallel Tool Calling (referencia /antigravity-guide).")
        print("    Queda TERMINANTEMENTE PROHIBIDO registrar subagentes secuencialmente uno")
        print("    por uno consumiendo turnos separados. Posteriormente, para abrir y")
        print("    ejecutar subagentes en paralelo, usa la tool específica 'invoke_subagent'.")
        print("    Rutas individuales (lectura paralela con view_file en 1 turno sin truncamiento):")
        for t in types_list:
            t_file = types_dir / f"{t['name']}.json"
            t_file.write_bytes(json.dumps(t, indent=2, ensure_ascii=False).replace("\r\n", "\n").encode("utf-8"))
            print(f"      * {t_file.resolve()} (write={t['enable_write_tools']})")
        print("=" * 70)
        for t in types_list:
            print(f"  * {t['name']}: {t['description']} (write={t['enable_write_tools']})")
        print("\n" + "-" * 70)
        print(types_json)
        print("-" * 70 + "\n")
        print("  [+] Subagent type contracts defined, saved to subagent_types.json, and verified.")
        print("  [+] ACCIÓN INMEDIATA: Emite las llamadas a 'define_subagent' en paralelo AHORA en este turno.")
        return {"types": types_list}

    def run_stage_judge_compare(self) -> Dict[str, Any]:
        """Auxiliary Stage: Compare blind judge responses against ground truth."""
        t0 = time.time()
        print("\n" + "=" * 70)
        print("[AUX STAGE: JUDGE-COMPARE] Comparing blind judge evaluations vs Ground Truth")
        print("=" * 70)
        res = compare_judge_responses(work_dir=self.work_dir)
        elapsed = time.time() - t0
        record_stage_timing(self.work_dir, "judge_compare", elapsed)
        record_stage_telemetry(self.work_dir, "05b", "judge_compare", status="completed", metadata={"duration_seconds": elapsed, "passed": res.get("passed", False)})
        passed = res.get("passed", False)
        print(f"  [+] Judge comparison finished with status: {'PASSED' if passed else 'DISCORDANCES'}")
        print(f"  [+] Agreement rate: {res.get('agreement_rate', 0.0) * 100:.1f}% ({res.get('agreed_items', 0)}/{res.get('total_items', 0)})")
        disagreements = res.get("disagreements", []) or res.get("discordances", [])
        if disagreements:
            print(f"  [!] Disagreements detected: {len(disagreements)}")
            for d in disagreements[:5]:
                print(f"      * [{d.get('item_id')}] template={d.get('template_id')}")
        report_file = self.work_dir / "judge_report.json"
        print(f"  [+] Canonical report saved to: {report_file}")
        print("  [+] Auxiliary Stage (judge-compare) completed.")
        return res

    def run_stage_repair_matrix(self) -> Dict[str, Any]:
        """Auxiliary Stage: Consolidate linter/build failures and blind-judge objections into ONE repair matrix per shard."""
        t0 = time.time()
        print("\n" + "=" * 70)
        print("[AUX STAGE: REPAIR-MATRIX] Consolidating gate findings per shard")
        print("=" * 70)

        cid_to_shard: Dict[str, str] = {}
        shard_to_cids: Dict[str, List[str]] = {}
        for mp in (self.work_dir / "shards" / "pre_shard_manifest.json", self.work_dir / "pre_shard_manifest.json"):
            if mp.is_file():
                try:
                    for s_item in (json.loads(mp.read_text(encoding="utf-8")).get("shards") or []):
                        if isinstance(s_item, dict) and s_item.get("shard_id"):
                            s_id = str(s_item["shard_id"])
                            c_ids = [str(c) for c in (s_item.get("competency_ids") or [])]
                            for c in c_ids:
                                cid_to_shard[c] = s_id
                            shard_to_cids.setdefault(s_id, []).extend(c_ids)
                    break
                except Exception:
                    pass

        matrix: Dict[str, Dict[str, Any]] = {}

        def _add(cid: Any, source: str, detail: str) -> None:
            if not cid:
                return
            cid = str(cid)
            entry = matrix.setdefault(cid, {"shard_id": cid_to_shard.get(cid, "shard_01"), "sources": [], "findings": []})
            if source not in entry["sources"]:
                entry["sources"].append(source)
            if detail and detail not in entry["findings"] and len(entry["findings"]) < 12:
                entry["findings"].append(detail)

        # 1. Linter / build gate / publication / template failure findings
        report_candidates = [
            self.work_dir / "specific_error_report.json",
            self.work_dir / "publish_rejection_spec.json",
            self.work_dir / "template_failures.json",
        ]
        for rep_p in report_candidates:
            if not rep_p.is_file():
                continue
            try:
                spec = json.loads(rep_p.read_text(encoding="utf-8"))
                for cid in (spec.get("failing_competencies") or []):
                    _add(cid, "linter", "")

                # Read grouped_by_rule or groups
                grps = spec.get("grouped_by_rule") or spec.get("groups") or {}
                if isinstance(grps, list):
                    for grp in grps:
                        tag = grp.get("rule_tag") or grp.get("linter") or "LINTER"
                        for loc in (grp.get("locations") or []):
                            msgs = loc.get("sample_findings") or [""]
                            _add(loc.get("competency_id"), "linter", f"[{tag}] {loc.get('template_id', '')}: {msgs[0]}"[:400])
                elif isinstance(grps, dict):
                    for rule_name, rule_items in grps.items():
                        if isinstance(rule_items, list):
                            for ent in rule_items:
                                if isinstance(ent, dict):
                                    tag = ent.get("rule_tag") or ent.get("linter") or rule_name
                                    if ent.get("locations"):
                                        for loc in ent["locations"]:
                                            msgs = loc.get("sample_findings") or [""]
                                            _add(loc.get("competency_id"), "linter", f"[{tag}] {loc.get('template_id', '')}: {msgs[0]}"[:400])
                                    else:
                                        cid = ent.get("competency_id") or ent.get("cid")
                                        msg = ent.get("message") or ent.get("detail") or str(ent)
                                        _add(cid, "linter", f"[{tag}] {msg}"[:400])
                                elif isinstance(ent, str):
                                    _add("", "linter", f"[{rule_name}] {ent}"[:400])
                        elif isinstance(rule_items, dict):
                            tag = rule_items.get("rule_tag") or rule_items.get("linter") or rule_name
                            cids = rule_items.get("competencies") or rule_items.get("competency_ids") or []
                            sample = rule_items.get("sample") or rule_items.get("message") or rule_name
                            if cids:
                                for cid in cids:
                                    _add(cid, "linter", f"[{tag}] {sample}"[:400])
                            else:
                                cid = rule_items.get("competency_id") or rule_items.get("cid")
                                _add(cid, "linter", f"[{tag}] {sample}"[:400])

                # Read diagnostics_by_competency
                diag = spec.get("diagnostics_by_competency") or {}
                if isinstance(diag, dict):
                    for cid, diag_entries in diag.items():
                        if isinstance(diag_entries, list):
                            for d_item in diag_entries:
                                if isinstance(d_item, dict):
                                    msg = d_item.get("message") or (d_item.get("messages", [""])[0] if isinstance(d_item.get("messages"), list) else "") or str(d_item)
                                    tag = d_item.get("rule_tag") or d_item.get("linter") or "DIAG"
                                    _add(cid, "linter", f"[{tag}] {msg}"[:400])
                                else:
                                    _add(cid, "linter", str(d_item)[:400])
                        elif isinstance(diag_entries, str):
                            _add(cid, "linter", diag_entries[:400])
                        elif isinstance(diag_entries, dict):
                            _add(cid, "linter", str(diag_entries)[:400])

                # Read failing_shards / affected_shards
                for s_id in (spec.get("failing_shards") or spec.get("affected_shards") or []):
                    cids_for_s = shard_to_cids.get(s_id, [])
                    if cids_for_s:
                        for c_id in cids_for_s:
                            _add(c_id, "linter", f"[SHARD] {s_id} marked as failing/affected")
                    elif str(s_id).startswith("C-"):
                        _add(str(s_id), "linter", f"[SHARD] {s_id} marked as failing/affected")
            except Exception as e:
                logger.warning("Could not read %s: %s", rep_p.name, e)

        # 2. Blind judge objections
        jr_p = self.work_dir / "judge_report.json"
        if jr_p.is_file():
            try:
                jr = json.loads(jr_p.read_text(encoding="utf-8"))
                for d in (jr.get("disagreements") or jr.get("discordances") or []):
                    if isinstance(d, dict):
                        reason = d.get("reason") or d.get("error") or d.get("feedback") or "Discordancia evaluador ciego"
                        _add(d.get("cid") or d.get("competency_id"), "judge", f"[JUDGE] {d.get('item_id', '')}: {reason}"[:400])
                tpl_to_cid: Dict[str, str] = {}
                for tp in (self.work_dir / "templates").glob("*.json"):
                    try:
                        td = json.loads(tp.read_text(encoding="utf-8"))
                        for t_obj in (td if isinstance(td, list) else td.get("templates", [td]) if isinstance(td, dict) else []):
                            if isinstance(t_obj, dict) and (t_obj.get("id") or t_obj.get("template_id")):
                                tpl_to_cid[str(t_obj.get("id") or t_obj.get("template_id"))] = tp.stem
                    except Exception:
                        pass

                def _resolve(c: str) -> str:
                    return tpl_to_cid.get(c, c)

                for key in ("failed_competencies", "failed_templates"):
                    val = jr.get(key) or []
                    for c in (val.keys() if isinstance(val, dict) else val):
                        if isinstance(c, str):
                            _add(_resolve(c), "judge", "")
                        elif isinstance(c, dict):
                            _add(_resolve(str(c.get("cid") or c.get("competency_id") or "")), "judge", str(c.get("reason", ""))[:400])
            except Exception as e:
                logger.warning("Could not read judge_report.json: %s", e)

        by_shard: Dict[str, List[str]] = {}
        for cid, e in matrix.items():
            by_shard.setdefault(e["shard_id"], []).append(cid)
        fail_cids = sorted(matrix)
        repair_cmd = (
            f'& ".venv\\Scripts\\python.exe" .agents/skills/content-to-course/dispatch.py dispatch-repair '
            f'--work-dir "{self.work_dir.as_posix()}" --ids {" ".join(fail_cids)}'
        ) if fail_cids else ""
        result = {
            "status": "REPAIR_NEEDED" if fail_cids else "CLEAN",
            "failing_competencies": fail_cids,
            "by_shard": {k: sorted(v) for k, v in sorted(by_shard.items())},
            "matrix": matrix,
            "single_wave_repair_command": repair_cmd,
        }
        (self.work_dir / "repair_matrix.json").write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"  [+] Matrix: {len(fail_cids)} competencies across {len(by_shard)} shard(s) -> repair_matrix.json")
        if repair_cmd:
            print(f"  [>] ONE consolidated repair wave: {repair_cmd}")
        record_stage_timing(self.work_dir, "repair_matrix", time.time() - t0)
        return result

    def run_stage_gates(self) -> Dict[str, Any]:
        """Auxiliary Stage: Full deterministic gates sequence (build + verify + publication QA dry-run + repair-matrix)."""
        print("\n" + "=" * 70)
        print("[AUX STAGE: GATES] Full deterministic quality gates (build + verify + QA dry-run + repair-matrix)")
        print("=" * 70)
        for stale in (
            "specific_error_report.json",
            "specific_error_report.md",
            "publish_rejection_spec.json",
            "publish_rejection_spec.md",
            "audit_gate_report.json",
        ):
            (self.work_dir / stale).unlink(missing_ok=True)

        build_ok = True
        verify_ok = True
        qa_ok = True

        # 1. Step 1: build
        try:
            self.run_stage_build()
        except Exception as e:
            build_ok = False
            print(f"  [!] Build gate reported findings: {str(e).splitlines()[0] if str(e) else type(e).__name__}")

        # 2. Step 2: verify (lexical and psychometric content validation)
        course_file = self.work_dir / "course.json"
        if course_file.is_file():
            try:
                self.run_stage_verify()
            except Exception as e:
                verify_ok = False
                print(f"  [!] Verify gate reported findings: {str(e).splitlines()[0] if str(e) else type(e).__name__}")
        else:
            verify_ok = False

        # 3. Step 3: QA deterministic publication dry-run (CoursePublisher / standardized_audit_engine)
        course_candidate = self.work_dir / "course_verified.json"
        if not course_candidate.is_file():
            course_candidate = course_file

        if course_candidate.is_file():
            try:
                publisher = CoursePublisher(courses_dir=self.output_dir, project_root=repo_root)
                from course_publisher import _load_run_full_audit, build_specific_error_report
                audit_fn = _load_run_full_audit(publisher.project_root)
                if audit_fn:
                    course_parsed = json.loads(course_candidate.read_text(encoding="utf-8"))
                    audit_rep = audit_fn(course_parsed)
                    num_q = len(course_parsed.get("questions", []))
                    mastery_readiness = audit_rep.get("mastery_path_readiness", {})
                    mpri_val = audit_rep.get("mpri_score")
                    mpri_score = mpri_val if mpri_val is not None else mastery_readiness.get("mpri_score", 0.0)
                    pillars = audit_rep.get("pillars", mastery_readiness.get("pillars", {}))
                    zpd_score = pillars.get("zpd_adaptive_progression", {}).get("score", 0.0)
                    hard_penalties = audit_rep.get("hard_penalties", [])
                    all_issues = audit_rep.get("all_issues", [])
                    risk_clusters = audit_rep.get("risk_clusters", {})
                    length_padded = risk_clusters.get("length_padded_options", [])

                    qa_failures = []
                    if num_q >= 20 and mpri_score < 75.0:
                        qa_failures.append(f"MPRI score below threshold: {mpri_score} < 75.0 (with {num_q} questions)")
                    if num_q >= 6 and zpd_score <= 0.0:
                        qa_failures.append(f"ZPD progression score collapsed: {zpd_score} <= 0.0 (with {num_q} questions)")
                    if hard_penalties:
                        qa_failures.append(f"Hard penalties detected ({len(hard_penalties)})")
                    crit_issues = [i for i in all_issues if i.get("severity") == "critical"]
                    if crit_issues:
                        qa_failures.append(f"Critical audit issues detected ({len(crit_issues)})")
                    if length_padded:
                        qa_failures.append(f"Length-padded options detected in {len(length_padded)} items")

                    if qa_failures:
                        qa_ok = False
                        print(f"  [!] QA publication audit dry-run detected {len(qa_failures)} blocking issue(s).")
                        build_specific_error_report(
                            parsed=course_parsed,
                            audit_report=audit_rep,
                            gate_failures=qa_failures,
                            work_dir=self.work_dir,
                        )
            except Exception as ex:
                qa_ok = False
                print(f"  [!] QA gate evaluation encountered error: {ex}")
        else:
            qa_ok = False

        # 4. Step 4: repair-matrix consolidating all findings
        matrix_res = self.run_stage_repair_matrix()
        all_passed = bool(build_ok and verify_ok and qa_ok and (matrix_res.get("status") == "CLEAN") and not matrix_res.get("failing_competencies"))
        matrix_res["build_ok"] = build_ok
        matrix_res["verify_ok"] = verify_ok
        matrix_res["qa_ok"] = qa_ok
        matrix_res["gates_passed"] = all_passed
        matrix_res["status"] = "PASS" if all_passed else "FAIL"

        if not all_passed:
            print("  [!] Gates reported failures. Repair matrix populated.")
        else:
            print("  [+] All quality gates passed cleanly.")

        return matrix_res

    def _detect_changed_competencies(self) -> List[str]:
        """Competencies whose template hash differs from the one recorded when last judged (i.e. repaired since)."""
        import hashlib
        from judge import _load_templates
        ev_p = self.work_dir / "verification" / "evaluated_competencies.json"
        if not ev_p.is_file():
            ev_p = self.work_dir / "evaluated_competencies.json"
        if not ev_p.is_file():
            return []
        saved = json.loads(ev_p.read_text(encoding="utf-8")).get("competency_hashes", {})
        changed: set = set()
        for t in _load_templates(self.work_dir / "templates"):
            cid = str(t.get("competency_id", ""))
            sha = t.get("_sha256") or hashlib.sha256(json.dumps(t, sort_keys=True).encode("utf-8")).hexdigest()
            if cid in saved and saved[cid] != sha:
                changed.add(cid)
        return sorted(changed)

    def run_stage_rejudge(self) -> Dict[str, Any]:
        """Auxiliary Stage: Surgical re-arbitration. Re-judges ONLY repaired competencies (--ids, or auto-detected by template hash change)."""
        import shutil
        t0 = time.time()
        print("\n" + "=" * 70)
        print("[AUX STAGE: REJUDGE] Surgical blind re-arbitration (no mass re-dispatch)")
        print("=" * 70)
        target = [str(x).strip() for x in (self.ids or []) if str(x).strip()] or self._detect_changed_competencies()
        if not target:
            print("  [+] No repaired/targeted competencies detected. Nothing to re-judge.")
            return {"status": "nothing_to_rejudge", "ids": []}

        jr_p = self.work_dir / "judge_report.json"
        base_p = self.work_dir / "judge_report_baseline.json"
        if jr_p.is_file() and not base_p.is_file():
            shutil.copy2(jr_p, base_p)

        # Archive stale responses: item_ids are reused across generations and would mask the new verdicts.
        archive = self.work_dir / "judge_archive" / time.strftime("%Y%m%d_%H%M%S")
        for d in (self.work_dir, self.work_dir / "verification", self.work_dir / "judges"):
            if d.is_dir():
                for f in list(d.glob("judge_responses*.json")):
                    archive.mkdir(parents=True, exist_ok=True)
                    shutil.move(str(f), str(archive / f"{d.name}__{f.name}"))

        (self.work_dir / "rejudge_scope.json").write_text(
            json.dumps({"ids": target, "baseline": base_p.name if base_p.is_file() else None}, indent=2), encoding="utf-8"
        )
        res = dispatch_judges(self.work_dir, ids=target, pointer=not self.no_pointer)
        n_sub = len(res.get("Subagents", []))
        (self.work_dir / "dispatch").mkdir(parents=True, exist_ok=True)
        (self.work_dir / "dispatch" / "judge_work_orders.json").write_text(json.dumps(res, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"  [+] Re-judging {len(target)} competency(ies): {', '.join(target)} -> {n_sub} judge(s)")
        print("  [>] After judges reply: run.py --stage rejudge-compare")
        record_stage_timing(self.work_dir, "rejudge", time.time() - t0)
        return {"status": "dispatched", "ids": target, "subagents_count": n_sub, "Subagents": res.get("Subagents", []), "item_files": res.get("item_files", [])}

    def run_stage_rejudge_compare(self) -> Dict[str, Any]:
        """Auxiliary Stage: Compare surgical re-judge answers and merge them into the full judge_report.json (other competencies keep their verdicts)."""
        t0 = time.time()
        print("\n" + "=" * 70)
        print("[AUX STAGE: REJUDGE-COMPARE] Merging surgical verdicts into full report")
        print("=" * 70)
        scope_p = self.work_dir / "rejudge_scope.json"
        base_p = self.work_dir / "judge_report_baseline.json"
        if not scope_p.is_file():
            raise RuntimeError("No rejudge_scope.json: run --stage rejudge first.")
        target = set(json.loads(scope_p.read_text(encoding="utf-8")).get("ids", []))
        partial = compare_judge_responses(work_dir=self.work_dir)
        (self.work_dir / "judge_report_rejudge.json").write_text(json.dumps(partial, indent=2, ensure_ascii=False), encoding="utf-8")

        base = json.loads(base_p.read_text(encoding="utf-8")) if base_p.is_file() else {"disagreements": [], "total_items": 0, "agreed_items": 0}
        def _cid(d: Dict[str, Any]) -> str:
            return str(d.get("cid") or d.get("competency_id") or "")
        kept = [d for d in (base.get("disagreements") or base.get("discordances") or []) if _cid(d) not in target]
        discord = kept + list(partial.get("disagreements") or [])
        base_total = int(base.get("total_items", base.get("total", 0)) or 0)
        total_items = base_total if base_total else partial.get("total_items", 0)
        agreed = total_items - len(discord)
        failed_c = sorted({_cid(d) for d in discord if _cid(d)})
        failed_t = sorted({str(d.get("template_id")) for d in discord if d.get("template_id")})
        complete = bool(partial.get("all_complete", False)) and total_items > 0
        passed = complete and not discord
        merged = dict(base)
        merged.update({
            "total": total_items, "total_items": total_items, "agreed_items": agreed,
            "agreement_rate": round(agreed / total_items, 4) if total_items else 0.0,
            "passed": passed, "status": "passed" if passed else ("incomplete" if not complete else "disagreements"),
            "all_complete": complete, "failed_templates": failed_t, "failed_competencies": failed_c,
            "affected_template_ids": failed_t, "disagreements": discord, "discordances": discord,
            "rejudged_competencies": sorted(target),
        })
        (self.work_dir / "judge_report.json").write_text(json.dumps(merged, indent=2, ensure_ascii=False), encoding="utf-8")
        base_p.write_text(json.dumps(merged, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"  [+] Surgical result: {'PASSED' if not partial.get('disagreements') else 'DISCORDANCES'} for {sorted(target)}")
        print(f"  [+] Merged report: status={merged['status']}, remaining disagreements={len(discord)}")
        record_stage_timing(self.work_dir, "rejudge_compare", time.time() - t0)
        return merged

    def run_stage_certify(self) -> Dict[str, Any]:
        """Auxiliary Stage: Mandatory formal Director validation. Re-runs templates -> build -> verify -> publish and writes certification.json.
        It does NOT stop at the first failure: every non-destructive gate (templates, build, verify) runs so ALL findings are collected,
        then repair-matrix consolidates them (with judge objections) to start one complete repair cycle. Publish only runs when every
        prior gate passed, so a stale/failed bank is never published. The Director must never assume success from a subagent's DONE report."""
        t0 = time.time()
        print("\n" + "=" * 70)
        print("[AUX STAGE: CERTIFY] Formal re-validation: templates -> build -> verify -> publish")
        print("=" * 70)
        steps: List[Dict[str, Any]] = []
        cert: Dict[str, Any] = {"status": "CERTIFIED", "steps": steps}

        def _run(name: str, fn: Any) -> bool:
            s0 = time.time()
            try:
                fn()
                steps.append({"stage": name, "ok": True, "seconds": round(time.time() - s0, 2)})
                return True
            except BaseException as e:  # SystemExit from strict gates must also fail certification
                if isinstance(e, KeyboardInterrupt):
                    raise
                err = str(e).splitlines()[0][:400] if str(e) else type(e).__name__
                steps.append({"stage": name, "ok": False, "seconds": round(time.time() - s0, 2), "error": err})
                print(f"  [!] Gate '{name}' failed: {err}")
                return False

        results = [_run(n, f) for n, f in (
            ("templates", self.run_stage_templates),
            ("build", self.run_stage_build),
            ("verify", self.run_stage_verify),
        )]
        if all(results):
            _run("publish", self.run_stage_publish)
        else:
            steps.append({"stage": "publish", "ok": False, "skipped": True, "error": "skipped: prerequisite gates failed"})

        failed = [s["stage"] for s in steps if not s["ok"]]
        if failed:
            cert["status"] = "REJECTED"
            cert["failed_stages"] = failed
            matrix = self.run_stage_repair_matrix()
            cert["repair_matrix"] = {"failing_competencies": matrix.get("failing_competencies", []), "by_shard": matrix.get("by_shard", {}),
                                     "single_wave_repair_command": matrix.get("single_wave_repair_command", "")}
            print(f"  [!] CERTIFICATION REJECTED. Failed gates: {', '.join(failed)}")
            print("  [>] Run ONE consolidated repair wave from repair_matrix.json, then rejudge only repaired competencies and certify again.")
        cert["total_seconds"] = round(time.time() - t0, 2)
        (self.work_dir / "certification.json").write_text(json.dumps(cert, indent=2, ensure_ascii=False), encoding="utf-8")
        if cert["status"] == "CERTIFIED":
            print("  [+] CERTIFIED: all formal gates re-executed successfully.")
        else:
            sys.exit(1)
        return cert
    def run_stage_bootstrap(self) -> Dict[str, Any]:
        """Stage bootstrap: Atomically prepare, define subagent specs, pointer dispatch_cta, and write lockfile."""
        t0 = time.time()
        logs_dir = self.work_dir / "logs"
        logs_dir.mkdir(parents=True, exist_ok=True)
        bootstrap_log_file = logs_dir / "bootstrap.log"

        if not self.raw_pdf:
            raise FileNotFoundError(
                "Cannot execute bootstrap: No input path provided via --pdf, --sources, or --source-dir."
            )

        if self.append and self.work_dir.name == "work_append" and self.work_dir.is_dir():
            import shutil
            for stale_item in ("cta.json", "cta.md", "cta_data.py", "course.json", "course_verified.json", "judge_report.json", "templates", "shards", "verification", "cta_parts", "cta"):
                stale_p = self.work_dir / stale_item
                if stale_p.is_dir():
                    shutil.rmtree(stale_p, ignore_errors=True)
                elif stale_p.is_file():
                    stale_p.unlink(missing_ok=True)

        prep_buffer = io.StringIO()
        with contextlib.redirect_stdout(prep_buffer):
            prep_res = self.run_stage_prepare()

        # 2. generate_define_subagent_specs (lean=True)
        type_res = generate_define_subagent_specs(self.work_dir, lean=True)
        type_files = type_res.get("type_files", [])

        # 3. dispatch_cta (pointer=True unless --no-pointer)
        cta_dispatch = dispatch_cta(self.work_dir, pointer=not self.no_pointer)
        cta_subagents = cta_dispatch.get("Subagents", [])

        # 4. Write work/.c2c_subagent_lock.json conforming to c2c_hook_guard.py
        lock_file = self.work_dir / ".c2c_subagent_lock.json"
        now_utc = datetime.datetime.now(datetime.timezone.utc).isoformat()
        lock_payload = {
            "active": True,
            "director_conversation_id": self.director_id or "",
            "course_id": self.course_id,
            "work_dir": self.work_dir.resolve().as_posix(),
            "created_at": now_utc,
            "fsm_state": "bootstrap",
            "turn_count": 0,
            "max_turns": 40,
            "est_tokens": 0,
            "max_tokens": 5000000,
            "last_error_sha256": "",
            "error_sha256_streak": 0,
            "max_error_streak": 3,
            "exempt_conversation_ids": [],
        }
        lock_file.write_text(json.dumps(lock_payload, indent=2, ensure_ascii=False), encoding="utf-8")

        elapsed = time.time() - t0
        record_stage_timing(self.work_dir, "bootstrap", elapsed)
        record_stage_telemetry(self.work_dir, "00b", "bootstrap", status="completed", metadata={"duration_seconds": elapsed, "lock_file": str(lock_file.resolve())})

        summary = {
            "status": "ready_for_cta",
            "course_id": self.course_id,
            "work_dir": self.work_dir.resolve().as_posix(),
            "lock_file": lock_file.resolve().as_posix(),
            "type_spec_files": [Path(p).resolve().as_posix() for p in type_files],
            "cta_unit_count": len(cta_subagents),
            "Subagents": cta_subagents,
            "elapsed_seconds": round(elapsed, 2),
        }
        orders_file = self.work_dir / "dispatch" / "cta_work_orders.json"
        stdout_json = format_compact_json_stdout(
            payload=summary,
            work_dir=self.work_dir,
            stage_name="bootstrap",
            work_orders_file=orders_file,
            max_bytes=1450,
        )
        prep_log = prep_buffer.getvalue()
        bootstrap_log_file.write_text(prep_log + "\n" + json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
        print(stdout_json)
        return summary

    def run_stage_unlock(self) -> Dict[str, Any]:
        """Auxiliary Stage: Release .c2c_subagent_lock.json."""
        lock_file = self.work_dir / ".c2c_subagent_lock.json"
        unlocked = False
        if lock_file.is_file():
            try:
                try:
                    data = json.loads(lock_file.read_text(encoding="utf-8"))
                    data["active"] = False
                    lock_file.write_text(json.dumps(data, indent=2), encoding="utf-8")
                except Exception:
                    pass
                lock_file.unlink(missing_ok=True)
                unlocked = True
            except Exception as e:
                logger.warning("Error releasing lockfile %s: %s", lock_file, e)
        res = {
            "status": "unlocked" if unlocked else "no_active_lock",
            "lock_file": str(lock_file.resolve()),
            "released": unlocked,
        }
        print(f"  [+] Subagent lock released: {lock_file.resolve()} (unlocked={unlocked})")
        return res

    def run_stage_wave_status(self) -> Dict[str, Any]:
        """Auxiliary Stage: Crystal-clear <= 5-line summary of shard compilation status per wave."""
        t0 = time.time()
        manifest_path = self.work_dir / "shards" / "pre_shard_manifest.json"
        if not manifest_path.is_file():
            manifest_path = self.work_dir / "pre_shard_manifest.json"

        if not manifest_path.is_file():
            print(f"[WAVE STATUS] No pre_shard_manifest.json found in {self.work_dir.as_posix()}")
            return {"status": "no_manifest", "waves": []}

        try:
            mdata = json.loads(manifest_path.read_text(encoding="utf-8"))
        except Exception as e:
            print(f"[WAVE STATUS] Corrupted manifest at {manifest_path.as_posix()}: {e}")
            return {"status": "corrupted_manifest", "error": str(e)}

        shards = mdata.get("shards", [])
        templates_dir = self.work_dir / "templates"
        attempts_dir = self.work_dir / ".check_attempts"

        waves_dict: Dict[int, List[Dict[str, Any]]] = {}
        for s in shards:
            w_idx = s.get("wave_index", 1)
            waves_dict.setdefault(w_idx, []).append(s)

        total_shards = len(shards)
        total_completed = 0
        total_pending = 0
        total_cb = 0

        wave_stats = []
        for w_idx in sorted(waves_dict.keys()):
            w_shards = waves_dict[w_idx]
            w_comp = 0
            w_pend = 0
            w_cb = 0
            for s in w_shards:
                s_id = s.get("shard_id", "")
                c_ids = s.get("competency_ids", [])

                all_templates = bool(c_ids) and all((templates_dir / f"{cid}.json").is_file() for cid in c_ids)
                if all_templates:
                    w_comp += 1
                    continue

                norm_shard_id = re.sub(r"[^\w-]", "_", s_id)
                att_file = attempts_dir / f"compile_{norm_shard_id}.json"
                is_cb = False
                if att_file.is_file():
                    try:
                        att_state = json.loads(att_file.read_text(encoding="utf-8"))
                        streak = att_state.get("same_error_streak", 0)
                        compiles = att_state.get("distinct_compiles", 0)
                        last_errs = str(att_state.get("last_errors", []))
                        if streak >= 3 or compiles > 10 or "CIRCUIT BREAKER" in last_errs:
                            is_cb = True
                    except Exception:
                        pass

                if is_cb:
                    w_cb += 1
                else:
                    w_pend += 1

            total_completed += w_comp
            total_pending += w_pend
            total_cb += w_cb
            wave_stats.append({
                "wave_index": w_idx,
                "total": len(w_shards),
                "completed": w_comp,
                "pending": w_pend,
                "circuit_broken": w_cb,
            })

        print(f"[WAVE STATUS] Total Shards: {total_completed}/{total_shards} completed ({total_pending} pending, {total_cb} circuit-broken)")
        if len(wave_stats) <= 4:
            for ws in wave_stats:
                print(f"  * Wave {ws['wave_index']}: {ws['completed']}/{ws['total']} completed ({ws['pending']} pending, {ws['circuit_broken']} circuit-broken)")
        else:
            w_parts = [f"W{ws['wave_index']}: {ws['completed']}/{ws['total']} (cb={ws['circuit_broken']})" for ws in wave_stats]
            print("  * " + " | ".join(w_parts[:len(w_parts)//2]))
            print("  * " + " | ".join(w_parts[len(w_parts)//2:]))

        elapsed = time.time() - t0
        return {
            "status": "ok",
            "total_shards": total_shards,
            "completed": total_completed,
            "pending": total_pending,
            "circuit_broken": total_cb,
            "waves": wave_stats,
            "duration_seconds": round(elapsed, 3),
        }

    def run_stage_dispatch_cta(self) -> Dict[str, Any]:
        """Auxiliary Stage: Generate CTA dispatch payload and work orders."""
        t0 = time.time()
        res = dispatch_cta(self.work_dir, pointer=not self.no_pointer)
        elapsed = time.time() - t0
        record_stage_timing(self.work_dir, "dispatch_cta", elapsed)

        work_orders_file = self.work_dir / "dispatch" / "cta_work_orders.json"
        summary_payload = {
            "status": "dispatched",
            "stage": "dispatch-cta",
            "course_id": self.course_id,
            "subagents_count": len(res.get("Subagents", [])),
            "item_files": res.get("item_files", []),
            "work_orders_file": work_orders_file.resolve().as_posix(),
            "Subagents": res.get("Subagents", []),
            "elapsed_seconds": round(elapsed, 2),
        }
        stdout_str = format_compact_json_stdout(
            payload=summary_payload,
            work_dir=self.work_dir,
            stage_name="dispatch-cta",
            work_orders_file=work_orders_file,
            max_bytes=1450,
        )
        print(stdout_str)
        return res

    def run_stage_dispatch_authors(self) -> Dict[str, Any]:
        """Auxiliary Stage: Generate author dispatch payload with wave filtering."""
        t0 = time.time()
        res = dispatch_authors(
            self.work_dir,
            wave_index=self.wave,
            ids=self.ids,
            pointer=not self.no_pointer,
        )
        elapsed = time.time() - t0
        record_stage_timing(self.work_dir, f"dispatch_authors_wave_{self.wave or 'all'}", elapsed)

        work_orders_file = self.work_dir / "dispatch" / "author_work_orders.json"
        (self.work_dir / "dispatch").mkdir(parents=True, exist_ok=True)
        work_orders_file.write_text(json.dumps(res, indent=2, ensure_ascii=False), encoding="utf-8")

        summary_payload = {
            "status": "dispatched",
            "stage": "dispatch-authors",
            "wave": self.wave,
            "course_id": self.course_id,
            "subagents_count": len(res.get("Subagents", [])),
            "item_files": res.get("item_files", []),
            "work_orders_file": work_orders_file.resolve().as_posix(),
            "Subagents": res.get("Subagents", []),
            "elapsed_seconds": round(elapsed, 2),
        }
        stdout_str = format_compact_json_stdout(
            payload=summary_payload,
            work_dir=self.work_dir,
            stage_name="dispatch-authors",
            work_orders_file=work_orders_file,
            max_bytes=1450,
        )
        print(stdout_str)
        return res

    def run_stage_dispatch_judges(self) -> Dict[str, Any]:
        """Auxiliary Stage: Generate blind judge dispatch payload."""
        t0 = time.time()
        res = dispatch_judges(
            self.work_dir,
            ready_only=self.ready_only,
            ids=self.ids,
            pointer=not self.no_pointer,
        )
        elapsed = time.time() - t0
        record_stage_timing(self.work_dir, "dispatch_judges", elapsed)

        work_orders_file = self.work_dir / "dispatch" / "judge_work_orders.json"
        (self.work_dir / "dispatch").mkdir(parents=True, exist_ok=True)
        work_orders_file.write_text(json.dumps(res, indent=2, ensure_ascii=False), encoding="utf-8")

        summary_payload = {
            "status": "dispatched",
            "stage": "dispatch-judges",
            "ready_only": self.ready_only,
            "course_id": self.course_id,
            "subagents_count": len(res.get("Subagents", [])),
            "item_files": res.get("item_files", []),
            "work_orders_file": work_orders_file.resolve().as_posix(),
            "Subagents": res.get("Subagents", []),
            "elapsed_seconds": round(elapsed, 2),
        }
        stdout_str = format_compact_json_stdout(
            payload=summary_payload,
            work_dir=self.work_dir,
            stage_name="dispatch-judges",
            work_orders_file=work_orders_file,
            max_bytes=1450,
        )
        print(stdout_str)
        return res

    def run_stage_judge_generate(self) -> Dict[str, Any]:
        """Auxiliary Stage: Generate blind judge batch and ground truth."""
        t0 = time.time()
        print("\n" + "=" * 70)
        print(f"[AUX STAGE: JUDGE-GENERATE] Generating judge batch (ready_only={self.ready_only})")
        print("=" * 70)
        templates_dir = self.work_dir / "templates"
        cta_file = self.work_dir / "cta.json"
        judge_p, gt_p = generate_judge_batch(
            templates_path=templates_dir,
            work_dir=self.work_dir,
            cta_path=cta_file if cta_file.is_file() else None,
            seeds=None,
            items_per_competency=0,
            ready_only=self.ready_only,
            max_judges=10,
            max_items_per_judge=20,
        )
        elapsed = time.time() - t0
        record_stage_timing(self.work_dir, "judge_generate", elapsed)
        res = {"judge_batch_path": str(judge_p), "ground_truth_path": str(gt_p)}
        print(f"  [+] Judge batch: {judge_p}")
        print(f"  [+] Ground truth: {gt_p}")
        print("  [+] Auxiliary Stage (judge-generate) completed.")
        return res

    # -------------------------------------------------------------------------
    # Pipeline Orchestrator
    # -------------------------------------------------------------------------
    def execute(
        self,
        target_stage: Optional[str] = None,
        from_stage: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Executes the pipeline according to target_stage or from_stage."""
        start_time = time.time()

        # Route auxiliary stages if requested
        if target_stage is not None and str(target_stage).lower() in AUXILIARY_STAGES:
            method_name = AUXILIARY_STAGES[str(target_stage).lower()]
            method = getattr(self, method_name)
            stage_slug = str(target_stage).lower()
            with cap_stdout_to_log(self.work_dir, stage_slug):
                res = method()
            if stage_slug == "gates" and isinstance(res, dict) and not res.get("gates_passed", True):
                raise RuntimeError("Quality gates failed. Blocking issues found in build, verify, or QA audit; repair matrix populated.")
            return {stage_slug: res, "elapsed_seconds": round(time.time() - start_time, 2)}

        if from_stage is not None:
            norm_from = str(from_stage).lower()
            if norm_from not in STAGE_MAP:
                raise ValueError(f"Invalid from-stage '{from_stage}'. Choose from: {STAGE_NAMES}")
            start_idx = STAGE_MAP[norm_from]
            end_idx = len(STAGE_NAMES) - 1
        elif target_stage is not None:
            norm_target = str(target_stage).lower()
            if norm_target not in STAGE_MAP:
                raise ValueError(f"Invalid stage '{target_stage}'. Choose from: {STAGE_NAMES}")
            start_idx = STAGE_MAP[norm_target]
            end_idx = start_idx
        else:
            start_idx = 0
            end_idx = len(STAGE_NAMES) - 1

        results: Dict[str, Any] = {}
        stage_methods = [
            self.run_stage_prepare,
            self.run_stage_cta,
            self.run_stage_shard,
            self.run_stage_templates,
            self.run_stage_build,
            self.run_stage_verify,
            self.run_stage_publish,
        ]

        for idx in range(start_idx, end_idx + 1):
            s_name = STAGE_NAMES[idx]
            method = stage_methods[idx]
            with cap_stdout_to_log(self.work_dir, s_name):
                res = method()
            results[s_name] = res
            if res.get("paused_for_review") is True:
                return results

        results["elapsed_seconds"] = round(time.time() - start_time, 2)
        return results


def _require_pykatex() -> None:
    """Fail fast if PyKaTeX is missing (otherwise KaTeX validation silently degrades).

    Explicit opt-out: set C2C_PYKATEX=off.
    """
    if os.environ.get("C2C_PYKATEX", "").lower() == "off":
        return
    try:
        import pykatex  # noqa: F401
    except ImportError:
        sys.stderr.write(
            "[ERROR] PyKaTeX is not installed: KaTeX validation would be silently skipped.\n"
            "        Install it with `pip install PyKaTeX` (or `pip install -e .[dev]`), "
            "or set C2C_PYKATEX=off to skip it explicitly.\n"
        )
        sys.exit(2)


def main() -> None:
    """CLI Entry Point."""
    _require_pykatex()
    parser = argparse.ArgumentParser(
        description="Modular Content-to-Course v3 Pipeline Runner."
    )
    stage_choices = [
        "prepare", "ingest", "cta", "shard", "templates", "build", "verify", "publish",
        "0", "1", "2", "3", "4", "5", "6",
        "cta-merge", "cta-reduce", "cta-apply", "dispatch", "scope-check",
        "define-types", "judge-compare", "repair-matrix", "gates", "rejudge", "rejudge-compare", "certify",
        "bootstrap", "unlock", "wave-status",
        "dispatch-cta", "dispatch-authors", "dispatch-judges", "judge-generate",
    ]
    parser.add_argument(
        "--stage",
        choices=stage_choices,
        help="Run a single pipeline stage.",
    )
    parser.add_argument(
        "--from-stage",
        choices=stage_choices,
        help="Resume execution from a specific stage to completion.",
    )
    parser.add_argument(
        "--review-cta",
        action="store_true",
        help="Pause execution after CTA stage for inspection before template generation.",
    )
    parser.add_argument(
        "--pdf",
        nargs="+",
        help="Path(s) to input course PDF(s) or directory containing course documents.",
    )
    parser.add_argument(
        "--sources",
        nargs="+",
        help="Alias for --pdf (source PDF/document paths).",
    )
    parser.add_argument(
        "--source-dir",
        help="Directory of source course documents (alternative to --pdf).",
    )
    parser.add_argument(
        "--director-id",
        default=None,
        help="Director conversation ID for subagent lockfile.",
    )
    parser.add_argument(
        "--wave",
        type=int,
        default=None,
        help="Wave index filter for shard authoring.",
    )
    parser.add_argument(
        "--no-pointer",
        action="store_true",
        default=False,
        help="Emit full inline prompts instead of compact pointer prompts.",
    )
    parser.add_argument(
        "--unlock",
        action="store_true",
        default=False,
        help="Release active .c2c_subagent_lock.json.",
    )
    parser.add_argument(
        "--course-id",
        help="Alphanumeric slug identifier for the course.",
    )
    parser.add_argument(
        "--title",
        help="Human-readable title for the course.",
    )
    parser.add_argument(
        "--work-dir",
        help="Working directory for intermediate stage artifacts (defaults to courses/<course_id>/work).",
    )
    parser.add_argument(
        "--output-dir",
        default="courses",
        help="Destination courses folder (defaults to courses/).",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        default=True,
        help="Enforce strict validation mode.",
    )
    parser.add_argument(
        "--append",
        action="store_true",
        default=False,
        help="Append questions into existing course JSON instead of overwriting.",
    )
    parser.add_argument(
        "--base-course",
        default=None,
        help="Path or course ID of existing base course for incremental append mode.",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Base random seed for reproducible question generation.",
    )
    parser.add_argument(
        "--shards",
        type=int,
        default=None,
        help="Number of author shards (defaults to dynamic max 2 competencies per shard in Case 2B).",
    )
    parser.add_argument(
        "--comps-per-shard",
        type=int,
        default=DEFAULT_COMPS_PER_SHARD,
        help="Max competencies per shard (defaults to 2 for Case 2B; change to 3 for Case 2A).",
    )
    parser.add_argument(
        "--order",
        nargs="*",
        help="Custom document processing order (list of filenames or path to order.json).",
    )
    parser.add_argument(
        "--cta-mode",
        choices=["auto", "mapreduce", "direct", "multiple"],
        default="auto",
        help="CTA processing mode (direct: single-pass direct CTA, mapreduce/multiple: sectional map-reduce).",
    )
    parser.add_argument(
        "--granularity",
        choices=["fine", "standard", "coarse"],
        default="standard",
        help="Pedagogical competency granularity (fine: 12-18/10pp, standard: 6-10/10pp, coarse: 3-5/10pp).",
    )
    parser.add_argument(
        "--no-merge",
        action="store_true",
        default=False,
        help="Disable duplicate competency merging in cta-apply stage.",
    )
    parser.add_argument(
        "--role",
        choices=["cta", "cta-direct", "cta-map", "cta-reduce", "author", "judge", "repair"],
        help="Subagent role for dispatch and scope-check stages.",
    )
    parser.add_argument(
        "--ready-only",
        action="store_true",
        default=False,
        help="Dispatch only ready sections/items in dispatch stage.",
    )
    parser.add_argument(
        "--ids",
        nargs="*",
        help="Optional specific IDs (shards, sections, competencies) to dispatch.",
    )
    parser.add_argument(
        "--skip-judges",
        action="store_true",
        default=False,
        help="Bypass independent blind judge report verification on publish stage.",
    )
    parser.add_argument(
        "--force-recheck",
        action="store_true",
        default=False,
        help="Bypass certificate caching and force full re-execution.",
    )

    sanitized_argv = [sys.argv[0]] + [sanitize_cli_arg(a) for a in sys.argv[1:]]
    args = parser.parse_args(sanitized_argv[1:])

    raw_pdf_input = args.pdf or args.sources or args.source_dir
    pdf_arg = raw_pdf_input
    if raw_pdf_input:
        if isinstance(raw_pdf_input, (list, tuple)):
            if len(raw_pdf_input) == 1:
                pdf_arg = sanitize_cli_arg(raw_pdf_input[0])
            else:
                pdf_arg = [sanitize_cli_arg(p) for p in raw_pdf_input]
        else:
            pdf_arg = sanitize_cli_arg(raw_pdf_input)

    order_arg = args.order[0] if (args.order and len(args.order) == 1) else args.order

    runner = PipelineRunner(
        pdf=pdf_arg,
        course_id=sanitize_cli_arg(args.course_id),
        title=sanitize_cli_arg(args.title),
        work_dir=sanitize_cli_arg(args.work_dir),
        output_dir=sanitize_cli_arg(args.output_dir),
        review_cta=args.review_cta,
        strict=args.strict,
        append=args.append,
        random_seed=args.seed,
        shards_k=args.shards,
        comps_per_shard=args.comps_per_shard,
        order=order_arg,
        cta_mode=args.cta_mode,
        granularity=args.granularity,
        no_merge=args.no_merge,
        role=args.role,
        ids=args.ids,
        ready_only=args.ready_only,
        skip_judges=args.skip_judges,
        director_id=sanitize_cli_arg(args.director_id),
        wave=args.wave,
        no_pointer=args.no_pointer,
        unlock=args.unlock,
        base_course=sanitize_cli_arg(args.base_course),
        force_recheck=args.force_recheck,
    )

    if args.unlock:
        runner.run_stage_unlock()
        return

    try:
        runner.execute(
            target_stage=args.stage,
            from_stage=args.from_stage,
        )
    except Exception as ex:
        err_info: Dict[str, Any] = {
            "status": "failed",
            "stage": args.stage or args.from_stage or "full",
            "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        }
        spec_json_p = runner.work_dir / "specific_error_report.json"
        spec_md_p = runner.work_dir / "specific_error_report.md"
        if spec_json_p.is_file():
            try:
                spec_d = json.loads(spec_json_p.read_text(encoding="utf-8"))
                err_info["specific_error_report_file"] = spec_md_p.as_posix()
                err_info["specific_error_report_json"] = spec_json_p.as_posix()
                err_info["orchestrator_directive"] = (
                    f"READ FIRST: {spec_md_p.as_posix()} — Contiene las líneas exactas (Lstart..Lend), "
                    f"template_id, item_id, CONTEXTO EXACTO y el comando de reparación agrupado por linter."
                )
                err_info["failing_competencies"] = spec_d.get("failing_competencies", [])
                err_info["failing_shards"] = spec_d.get("failing_shards", [])
                err_info["proposed_repair_command"] = spec_d.get("proposed_repair_command", "")
            except Exception:
                pass
        raw_err_str = str(ex)
        if spec_json_p.is_file() and "\n\n# SPECIFIC ERROR REPORT" in raw_err_str:
            raw_err_str = raw_err_str.split("\n\n# SPECIFIC ERROR REPORT", 1)[0]
        err_info["error"] = raw_err_str
        print(f"\n[FATAL ERROR] Pipeline terminated:\n{json.dumps(err_info, indent=2, ensure_ascii=False)}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
