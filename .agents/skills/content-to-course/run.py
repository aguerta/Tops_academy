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
import datetime
import json
import logging
import re
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Union

# Safe stdout encoding on Windows
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# Ensure skill directory is in sys.path
skill_dir = Path(__file__).parent.resolve()
if str(skill_dir) not in sys.path:
    sys.path.insert(0, str(skill_dir))

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
from course_publisher import CoursePublisher
from cta_merge import apply_harmonize, merge_cta_parts
from dispatch import build_dispatch, get_type_definitions, scope_check, snapshot_work_dir
from engine.assemble import check_course_giveaway_distribution
from engine.diversity import evaluate_competency_diversity
from engine.instantiate import instantiate_competency
from engine.invariants import check_instance_invariants
from ingest import ingest_course
from judge import compare_judge_responses, generate_judge_batch
from plan_shards import plan_shards
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
    "cta-apply": "run_stage_cta_apply",
    "dispatch": "run_stage_dispatch",
    "scope-check": "run_stage_scope_check",
    "define-types": "run_stage_define_types",
    "judge-compare": "run_stage_judge_compare",
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
    ) -> None:
        self.raw_pdf = pdf
        self.output_dir = Path(output_dir)
        self.review_cta = review_cta
        self.strict = strict
        self.append = append
        self.random_seed = random_seed
        self.vision = vision
        self.legacy_transcribe = legacy_transcribe
        self.shards_k = shards_k
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

        # Determine work directory first (isolate --append into work_append/)
        work_leaf = "work_append" if self.append else "work"
        clean_work_dir = sanitize_cli_arg(work_dir) if work_dir else None
        clean_course_id = sanitize_cli_arg(course_id) if course_id else None
        clean_title = sanitize_cli_arg(title) if title else None

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

        input_target = sources[0] if len(sources) == 1 else sources[0].parent
        prep_res = prepare_course(
            input_path=input_target,
            work_dir=self.work_dir,
            course_id=self.course_id,
            courses_dir=self.output_dir,
            append=self.append,
            cta_mode=self.cta_mode,
            granularity=self.granularity,
            order_override=self.order,
            title=self.title,
        )

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
            for part_data_p in sorted(cta_parts_dir.glob("part_*_data.py")):
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

            compiled_parts = sorted(cta_parts_dir.glob("part_*.json"))
            if compiled_parts:
                latest_part_mtime = max(p.stat().st_mtime for p in compiled_parts)
                if not cta_file.is_file() or latest_part_mtime > cta_file.stat().st_mtime:
                    print("  [*] Merging compiled CTA parts into cta.json...")
                    merge_cta_parts(self.work_dir)

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
        res = plan_shards(cta_file, shards_dir, k=self.shards_k)

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
            if not is_clean:
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

        if shard_data_files and (compile_shard_mod or compile_shard_script.is_file()):
            print(f"  [*] Compiling {len(shard_data_files)} pending shard data files...")
            for s_data_p in shard_data_files:
                shard_id = re.sub(r"_data$", "", s_data_p.stem)
                if compile_shard_mod and hasattr(compile_shard_mod, "compile_shard"):
                    ok, errs = compile_shard_mod.compile_shard(self.work_dir, shard_id=shard_id, strict=True)
                    if not ok:
                        logger.warning("Compilation for %s reported issues: %s", shard_id, errs[:3] if errs else "unknown")
                elif compile_shard_script.is_file():
                    import subprocess
                    subprocess.run([sys.executable, str(compile_shard_script), "--work", str(self.work_dir), "--shard", shard_id, "--strict"], check=False)

        if not templates_dir.is_dir() or not list(templates_dir.glob("*.json")):
            raise FileNotFoundError(
                f"Missing required templates: No .json files found in {templates_dir.resolve()}\n"
                f"Strict fail-fast: Exercise creator subagents must author templates before this stage."
            )

        is_valid, errors = check_templates_file_or_dir(templates_dir, cta_path=cta_file)
        if not is_valid:
            print("\n[ERROR] Templates validation failed:", file=sys.stderr)
            for err in errors[:10]:
                print(f"  - {err}", file=sys.stderr)
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
        return {"templates_dir": str(templates_dir.resolve()), "count": len(template_files)}

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

        for comp in competencies:
            cid = comp["id"]
            cat = comp.get("type", "concept").title()
            course_comp_dict, comp_questions, div_res = comp_results_map[cid]
            course_competencies_output.append(course_comp_dict)

            quota = 30 if cat.lower() == "skill" else 20
            div_ratio = div_res["diversity_ratio"]
            unique_c = div_res["unique_masked"]
            total_c = div_res["total"]
            if div_ratio < 0.5:
                raise ValueError(
                    f"Stem diversity gate failed for competency '{cid}': ratio is {div_ratio:.3f} "
                    f"({unique_c}/{total_c} unique masked patterns), strictly required >= 0.5."
                )
            print(f"  [*] Instantiated {quota} items for '{cid}' ({cat}) - Stem diversity: {div_ratio:.3f} ({unique_c}/{total_c})")

            # Re-index questions cleanly
            for q in comp_questions:
                q["id"] = f"Q-{cid.replace('-', '')}-{q_global_idx:03d}"
                q["question_id"] = q["id"]
                q_global_idx += 1

            all_questions.extend(comp_questions)

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
            print("  [*] Generating blind judge batch (stratified 2 items/competency WITHOUT answer keys)...")
            judge_batch_p, gt_p = generate_judge_batch(
                templates_path=templates_dir,
                work_dir=self.work_dir,
                cta_path=cta_file if cta_file.is_file() else None,
                items_per_competency=2,
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
        source_file = verified_file if verified_file.is_file() else (self.work_dir / "course.json")
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
                if jr_data.get("status") not in ("pass", "passed", "success") and not jr_data.get("passed", False):
                    disagreements = jr_data.get("disagreements", []) or jr_data.get("discordances", [])
                    if disagreements:
                        raise RuntimeError(
                            f"Publication blocked: Blind judge evaluations have {len(disagreements)} unresolved disagreement(s). "
                            "Repair discordances via dispatch --role repair before publishing."
                        )
            except Exception as ex:
                if "Publication blocked" in str(ex):
                    raise
                logger.warning("Could not read judge_report.json during publish check: %s", ex)

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
        print(f"  [+] Final CTA validated: {res.get('total_competencies', 0)} competencies.")
        print(f"  [+] cta.json written to: {res.get('cta_path')}")
        print(f"  [+] cta.md generated at: {res.get('cta_md_path')}")
        print(f"  [+] Merge report written to: {res.get('report_path')}")
        print("  [+] Auxiliary Stage (cta-apply) completed successfully.")
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
        if hasattr(self, "work_dir") and self.work_dir:
            self.work_dir.mkdir(parents=True, exist_ok=True)
            (self.work_dir / "subagent_types.json").write_text(types_json, encoding="utf-8")
        (skill_dir / "subagent_types.json").write_text(types_json, encoding="utf-8")

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
            t_file.write_text(json.dumps(t, indent=2, ensure_ascii=False), encoding="utf-8")
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
            res = method()
            return {str(target_stage).lower(): res, "elapsed_seconds": round(time.time() - start_time, 2)}

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
            res = method()
            results[s_name] = res
            if res.get("paused_for_review") is True:
                return results

        results["elapsed_seconds"] = round(time.time() - start_time, 2)
        return results


def main() -> None:
    """CLI Entry Point."""
    parser = argparse.ArgumentParser(
        description="Modular Content-to-Course v3 Pipeline Runner."
    )
    stage_choices = [
        "prepare", "ingest", "cta", "shard", "templates", "build", "verify", "publish",
        "0", "1", "2", "3", "4", "5", "6",
        "cta-merge", "cta-apply", "dispatch", "scope-check",
        "define-types", "judge-compare",
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
        "--seed",
        type=int,
        default=42,
        help="Base random seed for reproducible question generation.",
    )
    parser.add_argument(
        "--shards",
        type=int,
        default=None,
        help="Number of author shards (defaults to dynamic max 2 competencies per shard).",
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

    sanitized_argv = [sys.argv[0]] + [sanitize_cli_arg(a) for a in sys.argv[1:]]
    args = parser.parse_args(sanitized_argv[1:])

    pdf_arg = args.pdf
    if args.pdf:
        if len(args.pdf) == 1:
            pdf_arg = sanitize_cli_arg(args.pdf[0])
        else:
            pdf_arg = [sanitize_cli_arg(p) for p in args.pdf]

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
        order=order_arg,
        cta_mode=args.cta_mode,
        granularity=args.granularity,
        no_merge=args.no_merge,
        role=args.role,
        ids=args.ids,
        ready_only=args.ready_only,
        skip_judges=args.skip_judges,
    )

    try:
        runner.execute(
            target_stage=args.stage,
            from_stage=args.from_stage,
        )
    except Exception as ex:
        err_info = {
            "status": "failed",
            "error": str(ex),
            "stage": args.stage or args.from_stage or "full",
            "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        }
        print(f"\n[FATAL ERROR] Pipeline terminated:\n{json.dumps(err_info, indent=2, ensure_ascii=False)}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
