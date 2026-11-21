"""Deterministic Python Tuple Compiler for Content-to-Course v3.2 Shard Authors.

Compiles work/shards/<shard_id>_data.py into canonical template JSON files in < 100 ms:
- Zero-fallback strict check of work/shards/pre_shard_manifest.json (BLOCKER on missing)
- AST-level Line Locator (ShardDataLineLocator) tracking exact line ranges, constants, and helper functions
- Dual-signature support (direct CLI, run.py stage 3 subprocess, and Python module imports)
- Clean Python callable to AST string extraction with preamble constants/helpers injection
- Intelligent tuple format unpacking supporting both prompt_shard_author.md examples and v3.2 canonical tuples
- Robust MC7 distractor completion and stem variant diversification ensuring 0 errors on H-01 & H-02
- Atomic, race-condition-free file writes and isolated .check_attempts per shard_id
- Strict dry-run validation (20 seeds) with surgical line-mapped diagnostics
"""

import argparse
import ast
import collections
from collections import defaultdict, Counter
import copy
import hashlib
import importlib.util
import inspect
import json
import os
import re
import sys
import textwrap
import threading
import time
import traceback
import types
import uuid
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple, Union

# Force unbuffered standard streams to ensure immediate error reporting and avoid NTFS / Windows pipe deadlocks
try:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(line_buffering=True)
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(line_buffering=True)
except Exception:
    pass

# Ensure skill root is in sys.path
_skill_root = Path(__file__).parent.resolve()
if str(_skill_root) not in sys.path:
    sys.path.insert(0, str(_skill_root))

from engine.invariants import validate_katex_syntax
from engine.stage_contract import (
    DEFAULT_TEMPLATES_PER_MODALITY as _S4_DEFAULT_TPL_PER_MOD,
    MIN_ARCHETYPES as _S4_MIN_ARCHETYPES,
    MIN_MODALITIES_PER_COMPETENCY as _S4_MIN_MODS,
    MAX_MODALITIES_PER_COMPETENCY as _S4_MAX_MODS,
    ARCHETYPE_KINDS as _S4_ARCHETYPE_KINDS,
    competency_contract as _s4_competency_contract,
    contract_drift as _s4_contract_drift,
    is_skill_type as _s4_is_skill_type,
    quota_for_competency as _s4_quota_for_competency,
    required_templates_for_competency as _s4_required_templates,
    required_unique_stems as _s4_required_unique_stems,
    stems_advice as _s4_stems_advice,
)

from engine.shard_ast_transforms import (
    EvaluationContext,
    _CLONE_STEM_STOPWORDS,
    _CanonicalGenASTNormalizer,
    _ConstBindingSubstitutor,
    _QTYPE_TO_INTERACTION,
    _RESERVED_VAR_NAMES,
    _SYMPY_CLONE_CHECK_MODS,
    _canon_syms,
    _check_intra_competency_anti_clone,
    _clone_correct_str,
    _const_value_to_ast,
    _eval_const_if_test,
    _extract_const_literal,
    _extract_pure_sympy_expr,
    _prune_const_if_stmts,
    _specialize_gen_ast,
    _wrap_gen_raw_with_auto_vars,
    extract_function_code,
    inject_ast_auto_vars,
    prune_ast_dependencies,
    prune_ast_preamble,
)

from engine.shard_compiler_steps import (
    ACTIVE_INTERACTION_TYPES,
    PURE_PRODUCTION_TYPES,
    STRUCTURED_M20_TYPES,
    _STRUCTURED_PAYLOAD_KEYS,
    _extract_m20_structured_dids,
    _format_with_fmt,
    _make_sandbox_rng,
    _structured_payload_fingerprint,
    build_adapted_mc7_generator,
    compile_tuple_records_to_templates,
    evaluate_m3_and_m20_archetype_gates,
    normalize_form_c_template,
    promote_staged_templates_atomically,
)

class _CompilationWatchdog:
    """Watchdog daemon thread enforcing per-seed (3.0s) and global process (90.0s) timeout budgets."""

    def __init__(self, timeout: float = 90.0, shard_id: str = "unknown", seed_timeout: float = 3.0):
        self.timeout = float(timeout)
        self.seed_timeout = float(seed_timeout)
        self.shard_id = shard_id
        self._stop_event = threading.Event()
        self._thread: Optional[threading.Thread] = None
        self.start_time = 0.0

    def start(self) -> None:
        if self.timeout <= 0:
            return
        self.start_time = time.time()
        EvaluationContext.reset(self.shard_id)
        self._thread = threading.Thread(target=self._run, daemon=True, name="c2c_compile_watchdog")
        self._thread.start()

    def stop(self) -> None:
        self._stop_event.set()

    def _run(self) -> None:
        while not self._stop_event.wait(0.2):
            now = time.time()
            ctx = EvaluationContext.get()
            seed_start = ctx.get("start_time") or self.start_time
            seed_elapsed = now - seed_start
            total_elapsed = now - self.start_time

            is_seed_timeout = (ctx.get("seed") is not None) and (seed_elapsed >= self.seed_timeout)
            is_global_timeout = total_elapsed >= self.timeout

            if not is_seed_timeout and not is_global_timeout:
                continue

            shard_str = ctx.get("shard_id") or self.shard_id or "unknown"
            tpl_str = ctx.get("template_id") or "unknown"
            fn_str = ctx.get("gen_fn") or "_gen_unknown"
            arch_str = ctx.get("archetype") or "?"
            seed_str = str(ctx.get("seed")) if ctx.get("seed") is not None else "?"

            short_budget_active_seed = (
                is_global_timeout
                and self.timeout < self.seed_timeout
                and ctx.get("seed") is not None
            )

            if is_seed_timeout or short_budget_active_seed:
                diag_msg = (
                    f"\n[-] CRITICAL ERROR: [TIMEOUT_INFINITE_LOOP]\n"
                    f"    Shard:          {shard_str}\n"
                    f"    Template ID:    {tpl_str}\n"
                    f"    Generator Func: {fn_str} (Archetype {arch_str}, Seed {seed_str})\n"
                    f"    Seed Time:      {seed_elapsed:.2f}s (Exceeded per-seed budget of {self.seed_timeout:.1f}s)\n"
                    f"    Total Time:     {total_elapsed:.2f}s\n"
                    f"    Diagnostic:     Detected potential infinite loop, unbounded while-loop, \n"
                    f"                    or exhausted rejection sampling. Verify termination predicates \n"
                    f"                    and unbuffered output (-u).\n"
                    f"[-] FAIL: [TIMEOUT_INFINITE_LOOP] En '{tpl_str}' (función '{fn_str}', semilla {seed_str}): "
                    f"Tiempo de ejecución de la semilla excedió el límite de {self.seed_timeout:.1f}s.\n"
                )
            else:
                diag_msg = (
                    f"\n[-] CRITICAL ERROR: [TIMEOUT_GLOBAL_PROCESS]\n"
                    f"    Shard:          {shard_str}\n"
                    f"    Execution Time: {total_elapsed:.2f}s (Exceeded global process budget of {self.timeout:.1f}s)\n"
                    f"    Diagnostic:     Global shard compilation budget exceeded across multiple templates/seeds.\n"
                    f"                    Individual seeds were not flagged as infinite loops (last seed elapsed: {seed_elapsed:.2f}s).\n"
                    f"[-] FAIL: [TIMEOUT_GLOBAL_PROCESS] En shard '{shard_str}': "
                    f"Tiempo global del proceso excedió el límite de {self.timeout:.1f}s.\n"
                )
            try:
                sys.stderr.write(diag_msg)
                sys.stderr.flush()
                sys.stdout.write(diag_msg)
                sys.stdout.flush()
            except Exception:
                pass
            os._exit(1)


_EDIT_FILE_REMINDER = "⚠️ USA edit_file (NO uses write_file con Overwrite=True o el hook bloqueará tu turno)"

from engine.template_diagnostics import (
    count_distinct_shard_error_hunks,
    normalize_error_string_for_hash,
    render_compact_aggregated_errors,
)
from engine.template_healing import (
    COMBINED_LATEX,
    _atomic_write_json,
    _find_telltale_in_option,
    _pykatex,
    _strip_giveaway_prefix,
    auto_heal_template_data,
    check_ast_rf_triple_braces,
    detect_frankenstein_sum,
    heal_control_chars_in_obj,
    heal_control_chars_in_str,
    heal_shard_source_file,
    heal_shard_source_text,
    is_trivial_verifier,
    normalize_double_braces,
    parse_katex_number,
    pykatex_warnings,
)

from engine.shard_locator import ShardDataLineLocator, _find_diagnostic_line


def discover_fix_files(
    fixes_dir: Optional[Path],
    expected_cids: List[str],
    shard_id: Optional[str] = None,
) -> Tuple[Dict[str, Path], List[Path]]:
    """Discovers and maps shard fix files to competency IDs with case-insensitive and delimiter-agnostic normalization.
    
    Supports both per-shard isolated directories (shard_fixes/<shard_id>/<cid>.py)
    and legacy flat directories (shard_fixes/<cid>.py).
    Matches Hab-03, Hab_03, hab-03, hab_03, T-Hab-03, and hab03 to Hab-03.
    Returns (fix_files_by_cid, all_relevant_fix_files).
    """
    fix_files_by_cid: Dict[str, Path] = {}
    relevant_files: List[Path] = []
    if not fixes_dir or not fixes_dir.is_dir():
        return fix_files_by_cid, relevant_files

    # Check for per-shard subdirectory if fixes_dir is a root shard_fixes dir
    if shard_id and (fixes_dir / shard_id).is_dir():
        sub_files = sorted((fixes_dir / shard_id).glob("*.py"))
        if sub_files:
            all_fix_files = sub_files
        else:
            all_fix_files = sorted(fixes_dir.glob("*.py"))
    else:
        all_fix_files = sorted(fixes_dir.glob("*.py"))

    for fix_p in all_fix_files:
        stem = fix_p.stem
        norm_stem = re.sub(r"[^a-zA-Z0-9]", "", stem).lower()
        matched = False
        for ecid in expected_cids:
            norm_ecid = re.sub(r"[^a-zA-Z0-9]", "", ecid).lower()
            if (
                stem == ecid
                or stem == ecid.replace("-", "_")
                or stem.lower() == ecid.lower()
                or stem.replace("_", "-").lower() == ecid.lower()
                or norm_stem == norm_ecid
                or norm_stem == f"t{norm_ecid}"
            ):
                fix_files_by_cid[ecid] = fix_p
                if fix_p not in relevant_files:
                    relevant_files.append(fix_p)
                matched = True
                break
        if not matched and not expected_cids:
            norm_stem_cid = stem.replace("_", "-")
            fix_files_by_cid[norm_stem_cid] = fix_p
            if fix_p not in relevant_files:
                relevant_files.append(fix_p)

    return fix_files_by_cid, relevant_files


def infer_work_dir(
    explicit_work: Union[str, Path] = "work",
    shard_id: Optional[str] = None,
) -> Path:
    """Infers work directory if default 'work' is missing from CWD.

    Searches for:
    1. Active lockfiles: courses/*/.c2c_subagent_lock.json or courses/*/work/.c2c_subagent_lock.json with active=true.
    2. Most recent courses/*/work directory containing shards/{shard_id}_data.py or shards/pre_shard_manifest.json.
    Returns inferred Path, or Path(explicit_work) if no course match found.
    """
    target = Path(explicit_work)
    if (target / "shards" / "pre_shard_manifest.json").is_file() or (target / "pre_shard_manifest.json").is_file():
        return target

    cwd = Path.cwd()
    courses_dir = cwd / "courses"
    if not courses_dir.is_dir():
        return target

    norm_s_id = (shard_id or "").lower().strip()
    candidate_works: List[Tuple[float, Path]] = []

    for c_dir in sorted(courses_dir.iterdir()):
        if not c_dir.is_dir():
            continue
        lock_paths = [
            c_dir / ".c2c_subagent_lock.json",
            c_dir / "work" / ".c2c_subagent_lock.json",
        ]
        is_active = False
        for lp in lock_paths:
            if lp.is_file():
                try:
                    ldata = json.loads(lp.read_text(encoding="utf-8"))
                    if isinstance(ldata, dict) and ldata.get("active") is True:
                        is_active = True
                        break
                except Exception:
                    pass

        w_cand = c_dir / "work"
        if w_cand.is_dir():
            has_manifest = (w_cand / "shards" / "pre_shard_manifest.json").is_file() or (w_cand / "pre_shard_manifest.json").is_file()
            has_shard = (w_cand / "shards" / f"{norm_s_id}_data.py").is_file() if norm_s_id else False

            if is_active and (has_manifest or has_shard):
                return w_cand

            if has_shard or has_manifest:
                mtime = 0.0
                if has_shard:
                    mtime = (w_cand / "shards" / f"{norm_s_id}_data.py").stat().st_mtime
                elif has_manifest:
                    m_p = (w_cand / "shards" / "pre_shard_manifest.json") if (w_cand / "shards" / "pre_shard_manifest.json").is_file() else (w_cand / "pre_shard_manifest.json")
                    mtime = m_p.stat().st_mtime
                candidate_works.append((mtime, w_cand))

    if candidate_works:
        candidate_works.sort(key=lambda x: x[0], reverse=True)
        return candidate_works[0][1]

    return target


def compile_shard(
    work_dir_or_path: Union[str, Path],
    shard_id: Optional[str] = None,
    strict: bool = True,
    seeds: int = 50,
    output_dir: Optional[Union[str, Path]] = None,
    output_path: Optional[Union[str, Path]] = None,
    cta_path: Optional[Union[str, Path]] = None,
    manifest_path: Optional[Union[str, Path]] = None,
    min_archetypes: Optional[int] = None,
    fail_total: bool = False,
    templates_per_modality: Optional[int] = None,
    **kwargs,
) -> Tuple[bool, List[str]]:
    """Compiles shard data into canonical template JSON files with strict verification.

    Supports dual invocation styles:
    - compile_shard("work", "shard_01", strict=True, seeds=50)
    - compile_shard("work/shards/shard_01_data.py", output_dir="work/templates")
    """
    output_path = output_path or kwargs.get("output")
    cta_path = cta_path or kwargs.get("cta")
    manifest_path = manifest_path or kwargs.get("manifest")
    min_archetypes = min_archetypes if min_archetypes is not None else kwargs.get("min_archetypes")
    if templates_per_modality is None and "templates_per_modality" in kwargs:
        templates_per_modality = kwargs.get("templates_per_modality")

    target_p = Path(work_dir_or_path).resolve()
    # In-memory inference when default "work" does not have manifest
    if not target_p.name.endswith(".py"):
        if str(work_dir_or_path) in ("work", "./work", ".\\work") or target_p == (Path.cwd() / "work").resolve():
            if not (target_p / "shards" / "pre_shard_manifest.json").is_file() and not (target_p / "pre_shard_manifest.json").is_file():
                inferred = infer_work_dir(target_p, shard_id=shard_id)
                if inferred != target_p:
                    target_p = inferred.resolve()

    # Guarantee sys.modules and linecache safety across multiple compiles in same process
    import linecache
    linecache.clearcache()
    for k in list(sys.modules.keys()):
        if k.startswith("c2c_fix_mod_") or k.startswith("c2c_shard_mod_"):
            sys.modules.pop(k, None)

    # Determine if target_p is a shard data file or a work directory
    if target_p.name.endswith(".py"):
        if not shard_id:
            m_s = re.search(r"shard_(\d+)", target_p.stem)
            shard_id = f"shard_{m_s.group(1)}" if m_s else target_p.stem.replace("_data", "")
        shards_dir = target_p.parent
        work_p = shards_dir.parent if shards_dir.name == "shards" else shards_dir
        if not target_p.is_file():
            err_msg = f"ERROR: No existe el archivo de datos del shard: {target_p}"
            print(err_msg, file=sys.stderr)
            return False, [err_msg]
        shard_data_path = target_p
    else:
        work_p = target_p
        shards_dir = work_p / "shards"
        shard_data_path = None

    receipt_p = Path(output_path).resolve() if output_path and str(output_path).lower().endswith(".json") else None
    if output_dir:
        templates_dir = Path(output_dir).resolve()
    elif output_path and not receipt_p:
        templates_dir = Path(output_path).resolve()
    else:
        templates_dir = work_p / "templates"
    templates_dir.mkdir(parents=True, exist_ok=True)

    if not shard_id:
        err_msg = "ERROR: shard_id no especificado para compile_shard."
        print(err_msg, file=sys.stderr)
        return False, [err_msg]

    norm_shard_id = shard_id.lower().strip()
    att_dir = work_p / ".check_attempts"
    pass_marker = att_dir / f"pass_{norm_shard_id}.json"

    # Watchdog timer enforcement: global process budget <= 90.0 seconds (per-seed <= 3.0s)
    watchdog_timeout_val = kwargs.get("watchdog_timeout")
    if watchdog_timeout_val is None:
        env_timeout = os.getenv("C2C_COMPILE_WATCHDOG_TIMEOUT")
        if env_timeout is not None:
            try:
                watchdog_timeout_val = float(env_timeout)
            except ValueError:
                watchdog_timeout_val = 90.0
        else:
            watchdog_timeout_val = 90.0
    else:
        watchdog_timeout_val = float(watchdog_timeout_val)

    watchdog = _CompilationWatchdog(timeout=watchdog_timeout_val, shard_id=norm_shard_id)
    watchdog.start()

    try:
        return _compile_shard_body(
            work_p=work_p,
            shards_dir=shards_dir,
            shard_data_path=shard_data_path,
            templates_dir=templates_dir,
            receipt_p=receipt_p,
            shard_id=shard_id,
            norm_shard_id=norm_shard_id,
            att_dir=att_dir,
            pass_marker=pass_marker,
            strict=strict,
            seeds=seeds,
            cta_path=cta_path,
            manifest_path=manifest_path,
            min_archetypes=min_archetypes,
            fail_total=fail_total,
            templates_per_modality=templates_per_modality,
            **kwargs,
        )
    finally:
        watchdog.stop()


def _compile_shard_body(
    work_p: Path,
    shards_dir: Path,
    shard_data_path: Optional[Path],
    templates_dir: Path,
    receipt_p: Optional[Path],
    shard_id: str,
    norm_shard_id: str,
    att_dir: Path,
    pass_marker: Path,
    strict: bool,
    seeds: int,
    cta_path: Optional[Union[str, Path]],
    manifest_path: Optional[Union[str, Path]],
    min_archetypes: Optional[int],
    fail_total: bool = False,
    templates_per_modality: Optional[int] = None,
    **kwargs,
) -> Tuple[bool, List[str]]:

    cert_path = shards_dir / f"{norm_shard_id}.cert.json"

    def _cleanup_stale_pass_marker():
        for stale_p in (pass_marker, cert_path):
            if stale_p.is_file():
                try:
                    stale_p.unlink()
                except Exception:
                    pass

    # 1. Verify pre_shard_manifest.json (resolving --manifest pre_cta_manifest.json fallback cleanly)
    def _find_pre_shard_manifest() -> Optional[Path]:
        for cand in (shards_dir / "pre_shard_manifest.json", work_p / "pre_shard_manifest.json"):
            if cand.is_file():
                return cand.resolve()
        return None

    if manifest_path and Path(manifest_path).is_file():
        manifest_p = Path(manifest_path).resolve()
    else:
        found_m = _find_pre_shard_manifest()
        if not found_m:
            _cleanup_stale_pass_marker()
            print("BLOCKER:: No existe pre_shard_manifest.json", file=sys.stderr)
            sys.exit(2)
        manifest_p = found_m

    try:
        manifest_data = json.loads(manifest_p.read_text(encoding="utf-8"))
    except Exception as e:
        _cleanup_stale_pass_marker()
        print(f"BLOCKER:: pre_shard_manifest.json corrupto o ilegible: {e}", file=sys.stderr)
        sys.exit(2)

    if not isinstance(manifest_data, dict) or "shards" not in manifest_data:
        fallback_m = _find_pre_shard_manifest()
        if fallback_m and fallback_m != manifest_p:
            try:
                manifest_data = json.loads(fallback_m.read_text(encoding="utf-8"))
                manifest_p = fallback_m
            except Exception as e:
                _cleanup_stale_pass_marker()
                print(f"BLOCKER:: pre_shard_manifest.json corrupto o ilegible: {e}", file=sys.stderr)
                sys.exit(2)
        elif not fallback_m:
            _cleanup_stale_pass_marker()
            print("BLOCKER:: No existe pre_shard_manifest.json", file=sys.stderr)
            sys.exit(2)

    # Locate shard entry
    shard_entry = None
    for s in manifest_data.get("shards", []):
        s_id = str(s.get("shard_id", "")).lower().strip()
        if s_id == norm_shard_id or s_id.replace("shard_", "") == norm_shard_id.replace("shard_", ""):
            shard_entry = s
            break

    if not shard_entry:
        _cleanup_stale_pass_marker()
        err_msg = f"ERROR: Shard '{shard_id}' no encontrado en pre_shard_manifest.json."
        print(err_msg, file=sys.stderr)
        return False, [err_msg]

    expected_cids: List[str] = shard_entry.get("competency_ids", [])

    _drift = _s4_contract_drift(manifest_data.get("stage4_contract"))
    if _drift:
        _cleanup_stale_pass_marker()
        err_msg = f"BLOCKER:: [STAGE4-CONTRACT-DRIFT] {_drift}"
        print(err_msg, file=sys.stderr)
        return False, [err_msg]
    if not expected_cids and "competencies" in shard_entry:
        expected_cids = [c["id"] for c in shard_entry["competencies"] if isinstance(c, dict) and "id" in c]

    # Backup gate: duplicate competency titles (primary gate lives in cta_merge.apply_harmonize)
    if isinstance(shard_entry, dict):
        _seen_titles: Dict[str, str] = {}
        for _c in shard_entry.get("competencies", []):
            if not isinstance(_c, dict):
                continue
            _k = " ".join(str(_c.get("name", "")).casefold().split())
            if _k and _k in _seen_titles:
                _msg = (
                    f"FAIL: [DUPLICATE-TITLE] '{_seen_titles[_k]}' y '{_c.get('id')}' comparten el "
                    f"título '{_c.get('name')}'. Si son el mismo contenido, fusiónalas; si difieren "
                    f"en rol o nivel Bloom (Understand/Apply/Analyze…), renómbralas para reflejarlo "
                    f"(ej. '… (concepto)' / '… (aplicación)') en cta_merge y recompila."
                )
                print(_msg, file=sys.stderr)
                return False, [_msg]
            if _k:
                _seen_titles[_k] = str(_c.get("id"))

    eff_min_arch = _S4_MIN_ARCHETYPES
    if min_archetypes is not None:
        eff_min_arch = int(min_archetypes)
    elif isinstance(shard_entry, dict) and shard_entry.get("min_archetypes"):
        eff_min_arch = int(shard_entry["min_archetypes"])
    elif isinstance(manifest_data, dict) and manifest_data.get("min_archetypes"):
        eff_min_arch = int(manifest_data["min_archetypes"])

    if templates_per_modality is not None:
        eff_k = max(1, int(templates_per_modality))
    elif isinstance(manifest_data, dict) and isinstance(manifest_data.get("stage4_contract"), dict) and manifest_data["stage4_contract"].get("templates_per_modality") is not None:
        eff_k = max(1, int(manifest_data["stage4_contract"]["templates_per_modality"]))
    elif isinstance(shard_entry, dict) and shard_entry.get("templates_per_modality") is not None:
        eff_k = max(1, int(shard_entry["templates_per_modality"]))
    elif isinstance(manifest_data, dict) and manifest_data.get("templates_per_modality") is not None:
        eff_k = max(1, int(manifest_data["templates_per_modality"]))
    else:
        eff_k = _S4_DEFAULT_TPL_PER_MOD

    # Locate shard_fixes directory: prioritize shard-isolated directory (shard_fixes/<shard_id>/)
    shard_fixes_dir = shards_dir / "shard_fixes" / norm_shard_id
    if not shard_fixes_dir.is_dir() and (work_p / "shards" / "shard_fixes" / norm_shard_id).is_dir():
        shard_fixes_dir = work_p / "shards" / "shard_fixes" / norm_shard_id

    flat_fixes_dir = shards_dir / "shard_fixes"
    if not flat_fixes_dir.is_dir() and (work_p / "shards" / "shard_fixes").is_dir():
        flat_fixes_dir = work_p / "shards" / "shard_fixes"

    # Prioritize shard-isolated directory if it exists and has fix files, else fallback to flat
    fixes_dir = shard_fixes_dir if (shard_fixes_dir.is_dir() and any(shard_fixes_dir.glob("*.py"))) else flat_fixes_dir

    # Discover relevant fix files for hashing and modular splicing
    fix_files_by_cid, relevant_fix_files = discover_fix_files(fixes_dir, expected_cids, shard_id=norm_shard_id)
    has_all_fixes = bool(expected_cids and all(ecid in fix_files_by_cid for ecid in expected_cids))

    # Locate shard data path if not provided
    if not shard_data_path or not shard_data_path.is_file():
        shard_data_path_str = shard_entry.get("shard_data_path")
        if shard_data_path_str and Path(shard_data_path_str).is_file():
            shard_data_path = Path(shard_data_path_str).resolve()
        else:
            candidate = shards_dir / f"{norm_shard_id}_data.py"
            if candidate.is_file():
                shard_data_path = candidate
            else:
                if not has_all_fixes:
                    _cleanup_stale_pass_marker()
                    err_msg = f"ERROR: No existe el archivo de datos del shard: {candidate}"
                    print(err_msg, file=sys.stderr)
                    return False, [err_msg]
                shard_data_path = candidate

    if cta_path and Path(cta_path).is_file():
        cta_p = Path(cta_path).resolve()
    else:
        cta_file_candidate = work_p / "cta.json"
        cta_p = cta_file_candidate if cta_file_candidate.is_file() else None

    # Compute source_sha256 over shard_data_path, relevant fix files, cta/manifest inputs, and compile mode
    hasher = hashlib.sha256()
    if shard_data_path and shard_data_path.is_file():
        hasher.update(shard_data_path.read_bytes())
    for rf in sorted(relevant_fix_files, key=lambda p: p.name):
        hasher.update(f"\n--FIX:{rf.name}--\n".encode("utf-8"))
        hasher.update(rf.read_bytes())
    if cta_p and cta_p.is_file():
        hasher.update(b"\n--CTA--\n")
        hasher.update(cta_p.read_bytes())
    hasher.update(b"\n--MANIFEST_ENTRY--\n")
    hasher.update(json.dumps(shard_entry, sort_keys=True, ensure_ascii=False).encode("utf-8"))
    hasher.update(f"\n--FLAGS:{bool(strict)}:{int(seeds)}:{int(eff_min_arch)}:{int(eff_k)}:{bool(fail_total)}--\n".encode("utf-8"))
    source_sha256 = hasher.hexdigest()

    # Bounded compilation counter & unified stateful circuit breaker (.check_attempts/compile_{norm_shard_id}.json)
    att_dir.mkdir(parents=True, exist_ok=True)
    compile_att_file = att_dir / f"compile_{norm_shard_id}.json"

    state: Dict[str, Any] = {
        "distinct_compiles": 0,
        "same_error_streak": 0,
        "last_source_sha256": "",
        "last_err_hash": "",
        "last_errors": [],
        "error_count": 0,
        "has_syntax_error": False,
    }
    if compile_att_file.is_file():
        try:
            loaded_state = json.loads(compile_att_file.read_text(encoding="utf-8"))
            if isinstance(loaded_state, dict):
                if "distinct_compiles" in loaded_state:
                    state.update(loaded_state)
                elif "count" in loaded_state:
                    state["distinct_compiles"] = loaded_state.get("count", 0)
        except Exception:
            pass

    # Idempotent [NO-CHANGE] Re-Run check: do not increment counter or streak on identical source
    if (
        state.get("last_source_sha256") == source_sha256
        and state.get("last_errors")
    ):
        _cleanup_stale_pass_marker()
        cached_errors = state["last_errors"]
        no_change_prefix = "[NO-CHANGE: código idéntico al intento previo; edita el archivo antes de recompilar]"
        prefixed_errors = []
        for e in cached_errors:
            if no_change_prefix not in e:
                prefixed_errors.append(f"{no_change_prefix}\n{e}")
            else:
                prefixed_errors.append(e)
        print(prefixed_errors[0], file=sys.stderr)
        return False, prefixed_errors

    # Distinct compile increment
    distinct_compiles = state.get("distinct_compiles", 0) + 1
    state["distinct_compiles"] = distinct_compiles
    state["last_source_sha256"] = source_sha256

    print(f"[COMPILE {distinct_compiles}/10] Compilando shard '{shard_id}'...")

    def _fail(msg: str, has_syntax_error: bool = False, error_count: int = 1) -> Tuple[bool, List[str]]:
        normalized_errs = sorted([normalize_error_string_for_hash(msg)])
        err_hash = hashlib.sha256("\n".join(normalized_errs).encode("utf-8")).hexdigest()

        if state.get("last_err_hash") == err_hash:
            same_error_streak = state.get("same_error_streak", 0) + 1
        else:
            same_error_streak = 1
        state["same_error_streak"] = same_error_streak
        state["last_err_hash"] = err_hash
        state["error_count"] = error_count
        state["has_syntax_error"] = bool(has_syntax_error)
        state["affected_line_count"] = error_count
        state["error_sha256"] = err_hash
        state["updated_at"] = time.time()

        res_msg = msg
        if error_count < 6 and _EDIT_FILE_REMINDER not in res_msg:
            res_msg = f"{res_msg}\n{_EDIT_FILE_REMINDER}"
        if same_error_streak >= 3:
            terminal_stop = (
                f"\n[-] [CIRCUIT BREAKER HALT: 3 fallos consecutivos idénticos para shard '{shard_id}']. "
                f"STOP, send_message the Director."
            )
            res_msg = res_msg + terminal_stop
            print(terminal_stop, file=sys.stderr)

        _cleanup_stale_pass_marker()

        # Write un-truncated failure log to disk (updated on every failed compile)
        log_dir = shard_data_path.parent if (shard_data_path and hasattr(shard_data_path, "parent") and shard_data_path.parent.is_dir()) else shards_dir
        log_file = log_dir / f"{shard_id}_compile_error.log"
        try:
            rel_log = log_file.resolve().relative_to(Path.cwd().resolve()).as_posix()
        except Exception:
            rel_log = log_file.as_posix()
        try:
            log_file.write_text(f"FAIL: Compilación fallida para {shard_id}:\n\n{msg}\n", encoding="utf-8")
        except Exception:
            pass

        # Per CONOCIMIENTO_TRIBAL.md §4.3: Only show banner if stdout will truncate (>= 9,700 bytes)
        ANTIGRAVITY_STDOUT_SAFE_LIMIT = 9700
        will_truncate = len(res_msg.encode("utf-8")) >= ANTIGRAVITY_STDOUT_SAFE_LIMIT
        top_banner = ""
        if will_truncate:
            top_banner = (
                f"\n"
                f"================================================================================\n"
                f"[!] AVISO: LA SALIDA DE STDOUT EXCEDE EL BUFFER ({len(res_msg.encode('utf-8'))}B >= {ANTIGRAVITY_STDOUT_SAFE_LIMIT}B).\n"
                f"    >> INFORME ÍNTEGRO Y COMPLETO EN: {rel_log} <<\n"
                f"[!] ACCIÓN MANDATORIA: Ejecuta `read_file('{rel_log}')` para ver el error completo sin recortes.\n"
                f"================================================================================\n"
            )
            print(top_banner, file=sys.stdout)
            try:
                sys.stdout.flush()
            except Exception:
                pass

        if receipt_p:
            try:
                r_data = {}
                if receipt_p.is_file():
                    try:
                        r_data = json.loads(receipt_p.read_text(encoding="utf-8"))
                    except Exception:
                        r_data = {}
                r_data["shard_id"] = shard_id
                r_data["compiled_status"] = "FAIL"
                r_data["compilation_errors"] = [res_msg]
                r_data["full_error_log"] = rel_log
                r_data["error_count"] = error_count
                r_data["has_syntax_error"] = bool(has_syntax_error)
                r_data["compiled_at"] = time.time()
                _atomic_write_json(receipt_p, r_data)
            except Exception:
                pass

        full_err_out = (top_banner + "\n" + res_msg) if will_truncate else res_msg
        state["last_errors"] = [full_err_out]
        _atomic_write_json(compile_att_file, state)
        print(res_msg, file=sys.stderr)
        return False, [full_err_out]

    # Dual Calibrated Halt Threshold: distinct_compiles > 10
    if distinct_compiles > 10:
        halt_msg = (
            f"[-] [CIRCUIT BREAKER HALT: Límite de 10 compilaciones distintas alcanzado para shard '{shard_id}']. "
            f"STOP, send_message the Director."
        )
        return _fail(halt_msg, has_syntax_error=False, error_count=1)

    # In-memory healing of shard_XX_data.py (Zero-Disk-Mutation: source file on disk is NEVER modified)
    raw_source = shard_data_path.read_text(encoding="utf-8") if shard_data_path.is_file() else ""
    if raw_source:
        rf_warnings = check_ast_rf_triple_braces(raw_source)
        for w in rf_warnings:
            print(w, file=sys.stderr)
        _, healed_source = heal_shard_source_text(raw_source)
        try:
            from shard_precheck import precheck_source as _precheck
            _pre = _precheck(raw_source)
            if _pre:
                print(f"[PRECHECK] {len(_pre)} hallazgo(s) estaticos (advertencias, corrige todos juntos):", file=sys.stderr)
                for _w in _pre[:20]:
                    print(f"  - {_w}", file=sys.stderr)
        except Exception:
            pass
    else:
        healed_source = ""

    # Staged copy under .check_attempts/_staged/ for debugging without mutating source
    if healed_source:
        staged_dir = att_dir / "_staged"
        staged_dir.mkdir(parents=True, exist_ok=True)
        staged_p = staged_dir / f"{norm_shard_id}_data.py"
        try:
            staged_p.write_text(healed_source, encoding="utf-8")
        except Exception:
            pass

    # 2. AST Line Locator & Syntax Verification (evaluated on in-memory healed source)
    locator = ShardDataLineLocator(shard_data_path, source_text=healed_source)
    skip_base_module = False
    if raw_source and locator.syntax_error:
        if has_all_fixes:
            print(
                f"[!] Warning: {shard_data_path.name} contiene error sintáctico, pero el 100% de las competencias "
                f"({expected_cids}) están cubiertas por fijaciones en shard_fixes/. Omitiendo {shard_data_path.name}.",
                file=sys.stderr,
            )
            skip_base_module = True
        else:
            print(f"FAIL: Error sintáctico en {shard_data_path.name}:", file=sys.stderr)
            return _fail(locator.syntax_error, has_syntax_error=True, error_count=1)

    # 3. Load shard module dynamically from in-memory string
    mod_name = f"c2c_shard_mod_{norm_shard_id}_{uuid.uuid4().hex[:6]}"
    mod = types.ModuleType(mod_name)
    mod.__file__ = str(shard_data_path)
    mod.__dict__["parse_katex_number"] = parse_katex_number
    mod.__dict__["_pv"] = parse_katex_number
    if healed_source and not skip_base_module:
        try:
            code_obj = compile(healed_source, str(shard_data_path), "exec")
            sys.modules[mod_name] = mod
            exec(code_obj, mod.__dict__)
        except Exception as e:
            if has_all_fixes:
                print(
                    f"[!] Warning: Excepción al ejecutar {shard_data_path.name}, pero el 100% de las competencias "
                    f"están cubiertas por shard_fixes/. Omitiendo {shard_data_path.name}.",
                    file=sys.stderr,
                )
                skip_base_module = True
            else:
                tb = traceback.format_exc()
                err_msg = f"FAIL: Excepción al ejecutar {shard_data_path.name}:\n{tb}"
                return _fail(err_msg, has_syntax_error=isinstance(e, SyntaxError), error_count=1)

    base_templates = [] if skip_base_module else (getattr(mod, "TEMPLATES", None) or [])
    module_rats = getattr(mod, "RATS", {}) if isinstance(getattr(mod, "RATS", None), dict) else {}
    base_templates = heal_control_chars_in_obj(base_templates)

    # Map tuples to their origin file and line locator
    tuple_records: List[Dict[str, Any]] = []
    for orig_idx, t in enumerate(base_templates):
        t = normalize_form_c_template(t)
        tuple_records.append({
            "tuple": t,
            "file_path": shard_data_path,
            "locator": locator,
            "orig_idx": orig_idx,
        })

    # Splice fix files from shards/shard_fixes/<CID>.py
    known_types = set(_QTYPE_TO_INTERACTION.keys())

    for cid_fix, fix_path in fix_files_by_cid.items():
        if not fix_path.is_file():
            continue
        try:
            fix_raw_text = fix_path.read_text(encoding="utf-8")
            rf_w = check_ast_rf_triple_braces(fix_raw_text)
            for w in rf_w:
                print(w, file=sys.stderr)
            _, healed_fix_text = heal_shard_source_text(fix_raw_text)
            fix_loc = ShardDataLineLocator(fix_path, source_text=healed_fix_text)
            if fix_loc.syntax_error:
                return _fail(
                    f"FAIL: Error sintáctico en shard_fixes/{fix_path.name}:\n{fix_loc.syntax_error}",
                    has_syntax_error=True,
                    error_count=1,
                )

            fix_mod_name = f"c2c_fix_mod_{cid_fix.replace('-', '_')}_{uuid.uuid4().hex[:6]}"
            fix_mod = types.ModuleType(fix_mod_name)
            fix_mod.__file__ = str(fix_path)
            fix_mod.__dict__["parse_katex_number"] = parse_katex_number
            fix_mod.__dict__["_pv"] = parse_katex_number
            fix_code_obj = compile(healed_fix_text, str(fix_path), "exec")
            sys.modules[fix_mod_name] = fix_mod
            exec(fix_code_obj, fix_mod.__dict__)

            fix_rats = getattr(fix_mod, "RATS", None)
            if isinstance(fix_rats, dict):
                module_rats.update(fix_rats)

            fix_templates = getattr(fix_mod, "TEMPLATES", None)
            if fix_templates and isinstance(fix_templates, (list, tuple)):
                fix_templates = heal_control_chars_in_obj(fix_templates)

                new_records = []
                replaced = False
                for rec in tuple_records:
                    t_cand = normalize_form_c_template(rec["tuple"])
                    rec["tuple"] = t_cand
                    t_cid = None
                    if isinstance(t_cand, dict):
                        t_cid = str(t_cand.get("cid") or t_cand.get("competency_id") or "").strip()
                    elif len(t_cand) >= 3 and str(t_cand[2]).lower().strip() in known_types:
                        t_cid = str(t_cand[1]).strip()
                    elif len(t_cand) >= 3 and str(t_cand[1]).lower().strip() in known_types:
                        t_cid = str(t_cand[0]).strip()
                    else:
                        t_cid = str(t_cand[0]).strip()

                    if t_cid == cid_fix or t_cid.replace("-", "_") == cid_fix.replace("-", "_"):
                        if not replaced:
                            for fix_idx, ft in enumerate(fix_templates):
                                ft = normalize_form_c_template(ft)
                                new_records.append({
                                    "tuple": ft,
                                    "file_path": fix_path,
                                    "locator": fix_loc,
                                    "orig_idx": fix_idx,
                                })
                            replaced = True
                    else:
                        new_records.append(rec)

                if not replaced:
                    for fix_idx, ft in enumerate(fix_templates):
                        ft = normalize_form_c_template(ft)
                        new_records.append({
                            "tuple": ft,
                            "file_path": fix_path,
                            "locator": fix_loc,
                            "orig_idx": fix_idx,
                        })

                tuple_records = new_records
        except Exception as e:
            tb = traceback.format_exc()
            return _fail(
                f"FAIL: Excepción al cargar shard_fixes/{fix_path.name}:\n{tb}",
                has_syntax_error=isinstance(e, SyntaxError),
                error_count=1,
            )

    raw_templates = [rec["tuple"] for rec in tuple_records]
    if not raw_templates:
        err_msg = f"FAIL: {shard_data_path.name} no define la lista 'TEMPLATES = [...]'."
        return _fail(err_msg)

    class _FailFastAbort(Exception):
        def __init__(self, msg: str, has_syntax_error: bool = False, error_count: int = 1):
            super().__init__(msg)
            self.msg = msg
            self.has_syntax_error = has_syntax_error
            self.error_count = error_count

    def _emit_or_abort(
        bucket: List[str],
        msg: str,
        has_syntax_error: bool = False,
        error_count: int = 1,
    ) -> None:
        if not fail_total:
            raise _FailFastAbort(msg, has_syntax_error=has_syntax_error, error_count=error_count)
        bucket.append(msg)

    # 4. Identify competencies and verify parity (Form-C dict or Form-B 9-tuple)
    step4_errors: List[str] = []
    step5_errors: List[str] = []
    found_cids = []
    valid_tuple_records: List[Dict[str, Any]] = []
    try:
        for rec_idx, rec in enumerate(tuple_records):
            t = normalize_form_c_template(rec["tuple"])
            rec["tuple"] = t
            curr_loc = rec["locator"]
            curr_p = rec["file_path"]
            orig_idx = rec["orig_idx"]
            if isinstance(t, dict):
                c_candidate = str(t.get("cid") or t.get("competency_id") or "").strip()
                if not c_candidate:
                    s_t, e_t, snip = curr_loc.get_tuple_snippet(orig_idx)
                    err_msg = (
                        f"FAIL: El diccionario Form-C en índice {orig_idx} no define 'cid' ni 'competency_id'.\n"
                        f"  Ubicación: Líneas {s_t}..{e_t} en {curr_p.name}\n"
                        f"{snip}"
                    )
                    _emit_or_abort(step4_errors, err_msg)
                    continue
                found_cids.append(c_candidate)
                valid_tuple_records.append(rec)
            elif isinstance(t, (list, tuple)):
                if len(t) != 9:
                    s_t, e_t, snip = curr_loc.get_tuple_snippet(orig_idx)
                    err_msg = (
                        f"FAIL: La tupla en índice {orig_idx} tiene {len(t) if isinstance(t, (list, tuple)) else 0} elementos "
                        f"(se requieren exactamente 9 elementos según el contrato Form-B: "
                        f"tpl_id, cid, qtype, gen_fn, ver_fn, (difficulty, bloom), stems, hints, solution).\n"
                        f"  Ubicación: Líneas {s_t}..{e_t} en {curr_p.name}\n"
                        f"{snip}"
                    )
                    _emit_or_abort(step4_errors, err_msg)
                    continue

                if str(t[1]).lower().strip() in known_types or str(t[2]).lower().strip() not in known_types:
                    s_t, e_t, snip = curr_loc.get_tuple_snippet(orig_idx)
                    err_msg = (
                        f"FAIL: Se detectó formato legacy Form-A o tipo inválido en la tupla {orig_idx}. "
                        f"El compilador solo admite el contrato Form-B de 9 elementos: "
                        f"(tpl_id, cid, qtype, gen_fn, ver_fn, (difficulty, bloom), stems, hints, solution).\n"
                        f"  Ubicación: Líneas {s_t}..{e_t} en {curr_p.name}\n"
                        f"{snip}"
                    )
                    _emit_or_abort(step4_errors, err_msg)
                    continue

                c_candidate = str(t[1]).strip()
                found_cids.append(c_candidate)
                valid_tuple_records.append(rec)
            else:
                s_t, e_t, snip = curr_loc.get_tuple_snippet(orig_idx)
                err_msg = (
                    f"FAIL: Entrada inválida en TEMPLATES en índice {orig_idx}: se esperaba una 9-tupla Form-B o un dict Form-C, "
                    f"se recibió: {type(t).__name__}.\n"
                    f"  Ubicación: Líneas {s_t}..{e_t} en {curr_p.name}\n"
                    f"{snip}"
                )
                _emit_or_abort(step4_errors, err_msg)
                continue

        missing_cids = [cid for cid in expected_cids if cid not in found_cids]
        unexpected_cids = [cid for cid in found_cids if cid not in expected_cids]
        if missing_cids or unexpected_cids:
            err_parts = []
            if missing_cids:
                err_parts.append(f"Competencias faltantes en TEMPLATES: {', '.join(missing_cids)}")
            if unexpected_cids:
                err_parts.append(f"Competencias no asignadas a este shard: {', '.join(unexpected_cids)}")
            err_msg = f"FAIL: Paridad de competencias violada en {shard_data_path.name}: " + " | ".join(err_parts)
            _emit_or_abort(step4_errors, err_msg)
    except _FailFastAbort as abort:
        return _fail(abort.msg, has_syntax_error=abort.has_syntax_error, error_count=abort.error_count)

    tuple_records = valid_tuple_records

    from check_templates import check_templates_file_or_dir

    cta_comp_map = {c["id"]: c for c in shard_entry.get("competencies", []) if isinstance(c, dict) and "id" in c}
    cta_contract_version = 1
    if cta_p and cta_p.is_file():
        try:
            cta_data = json.loads(cta_p.read_text(encoding="utf-8"))
            if isinstance(cta_data, dict):
                cta_contract_version = int(cta_data.get("contract_version", cta_data.get("CTA_CONTRACT_VERSION", 1)))
            for c in cta_data.get("competencies", []):
                if isinstance(c, dict) and "id" in c:
                    cid_key = c["id"]
                    if cid_key not in cta_comp_map:
                        cta_comp_map[cid_key] = c
                    else:
                        if c.get("distractors"):
                            cta_comp_map[cid_key]["distractors"] = c["distractors"]
                        if "assumptions" in c and c.get("assumptions"):
                            cta_comp_map[cid_key]["assumptions"] = c["assumptions"]
                        if c.get("recommended_modalities"):
                            cta_comp_map[cid_key]["recommended_modalities"] = c["recommended_modalities"]
                        if c.get("bloom"):
                            cta_comp_map[cid_key]["bloom"] = c["bloom"]
        except Exception:
            pass

    # 5. Compile tuples into canonical JSON dictionaries grouped by competency
    templates_by_cid: Dict[str, List[Dict[str, Any]]] = {}
    gen_callables_by_cid: Dict[str, List[Any]] = {}
    deferred_verifier_errors: List[str] = []

    def _step5_err(msg: str) -> bool:
        if not fail_total:
            return True
        step5_errors.append(msg)
        return False

    hints_by_comp: Dict[str, Dict[str, Tuple[str, ...]]] = {}
    for rec in tuple_records:
        rec_t = rec["tuple"]
        if isinstance(rec_t, dict):
            c_cid = str(rec_t.get("cid") or rec_t.get("competency_id") or "").strip()
            c_tid = str(rec_t.get("id") or rec_t.get("tpl_id") or "").strip()
            c_hints = rec_t.get("hints")
        elif isinstance(rec_t, (list, tuple)) and len(rec_t) == 9:
            c_cid = str(rec_t[1]).strip()
            c_tid = str(rec_t[0]).strip()
            c_hints = rec_t[7]
        else:
            continue
        if c_cid and c_tid and isinstance(c_hints, (list, tuple)) and c_hints:
            norm_h = tuple(re.sub(r"\s+", " ", str(h).strip().lower()) for h in c_hints)
            hints_by_comp.setdefault(c_cid, {})[c_tid] = norm_h

    deferred_hints_dup_errors: List[str] = []
    for c_cid, comp_hints in hints_by_comp.items():
        if len(comp_hints) > 1:
            seen_h: Dict[Tuple[str, ...], List[str]] = {}
            for c_tid, nh in comp_hints.items():
                seen_h.setdefault(nh, []).append(c_tid)
            for nh, tids in seen_h.items():
                if len(tids) > 1:
                    if strict:
                        deferred_hints_dup_errors.append(
                            f"FAIL: [TPL-HINTS-DUPLICATE] Competencia '{c_cid}': Múltiples plantillas ({', '.join(tids)}) reutilizan exactamente el mismo arreglo de pistas (hints). "
                            f"Cada plantilla debe proporcionar pistas socráticas diferenciadas."
                        )
                    else:
                        print(
                            f"WARNING: [TPL-HINTS-DUPLICATE] Competencia '{c_cid}': Múltiples plantillas ({', '.join(tids)}) reutilizan exactamente el mismo arreglo de pistas (hints).",
                            file=sys.stderr,
                        )

    early_step5_res = compile_tuple_records_to_templates(
        tuple_records=tuple_records,
        cta_comp_map=cta_comp_map,
        strict=strict,
        module_rats=module_rats,
        norm_shard_id=norm_shard_id,
        templates_by_cid=templates_by_cid,
        gen_callables_by_cid=gen_callables_by_cid,
        deferred_hints_dup_errors=deferred_hints_dup_errors,
        deferred_verifier_errors=deferred_verifier_errors,
        step5_err_fn=_step5_err,
        fail_fn=_fail,
    )
    if early_step5_res is not None:
        return early_step5_res

    # 6. Stage templates atomically grouped by competency (promote to templates_dir only on PASS)
    staged_tpl_dir = att_dir / "_staged_templates" / norm_shard_id / "templates"
    staged_tpl_dir.mkdir(parents=True, exist_ok=True)
    staged_paths: List[Path] = []
    final_paths_by_cid: Dict[str, Path] = {}
    for cid, tpls in templates_by_cid.items():
        base_id = f"T-{cid}" if not cid.startswith("T-") else cid
        for idx, tpl in enumerate(tpls, start=1):
            cur_id = tpl.get("id") or base_id
            needs_normalization = (
                not cur_id.startswith("T-")
                or (len(tpls) > 1 and cur_id == base_id)
                or any(tpls[j].get("id") == cur_id for j in range(len(tpls)) if j != idx - 1)
            )
            if needs_normalization:
                unique_id = f"{base_id}-{idx:02d}"
                tpl["id"] = unique_id
                tpl["template_id"] = unique_id

        staged_json_path = staged_tpl_dir / f"{cid}.json"
        final_paths_by_cid[cid] = templates_dir / f"{cid}.json"
        if len(tpls) == 1:
            payload = tpls[0]
        else:
            payload = {
                "competency_id": cid,
                "templates": tpls,
            }
        _atomic_write_json(staged_json_path, payload)
        staged_paths.append(staged_json_path)

    # 7. Execute Strict Validation with check_templates (isolated by shard_id)
    if staged_paths:
        is_clean, raw_errors = check_templates_file_or_dir(
            target_path=staged_paths,
            cta_path=cta_p,
            num_dry_run_seeds=seeds,
            strict=strict,
            auto_fix=True,
            shard_py=(staged_p if (healed_source and staged_p.is_file()) else shard_data_path),
            shard_id=norm_shard_id,
            from_compile_shard=True,
        )
    else:
        is_clean, raw_errors = False, []
    compiled_paths = list(staged_paths)

    m3_errors = evaluate_m3_and_m20_archetype_gates(
        expected_cids=expected_cids,
        templates_by_cid=templates_by_cid,
        gen_callables_by_cid=gen_callables_by_cid,
        cta_comp_map=cta_comp_map,
        cta_contract_version=cta_contract_version,
        shard_entry=shard_entry,
        shard_data_path=shard_data_path,
        fix_files_by_cid=fix_files_by_cid,
        locator=locator,
        healed_source=healed_source,
        raw_source=raw_source,
        strict=strict,
        seeds=seeds,
        norm_shard_id=norm_shard_id,
        fail_total=fail_total,
        eff_k=eff_k,
        eff_min_arch=eff_min_arch,
    )

    if step4_errors or step5_errors or deferred_verifier_errors or m3_errors or deferred_hints_dup_errors:
        is_clean = False
        raw_errors = step4_errors + step5_errors + deferred_verifier_errors + m3_errors + list(raw_errors) + deferred_hints_dup_errors

    if not is_clean:
        error_count = count_distinct_shard_error_hunks(
            raw_errors, targets=compiled_paths, shard_py=shard_data_path
        )
        compact_report = render_compact_aggregated_errors(
            raw_errors, targets=compiled_paths, shard_py=shard_data_path, max_output_lines=60
        )
        normalized_errs = sorted([normalize_error_string_for_hash(str(e)) for e in raw_errors])
        err_hash = hashlib.sha256("\n".join(normalized_errs).encode("utf-8")).hexdigest()

        if state.get("last_err_hash") == err_hash:
            same_error_streak = state.get("same_error_streak", 0) + 1
        else:
            same_error_streak = 1
        state["same_error_streak"] = same_error_streak
        state["last_err_hash"] = err_hash
        state["error_count"] = error_count
        state["has_syntax_error"] = False
        state["affected_line_count"] = error_count
        state["error_sha256"] = err_hash
        state["updated_at"] = time.time()

        _cleanup_stale_pass_marker()

        # Write un-truncated complete diagnostics to disk (<shard_id>_compile_error.log)
        log_dir = shard_data_path.parent if (shard_data_path and hasattr(shard_data_path, "parent") and shard_data_path.parent.is_dir()) else shards_dir
        log_file = log_dir / f"{shard_id}_compile_error.log"
        try:
            rel_log = log_file.resolve().relative_to(Path.cwd().resolve()).as_posix()
        except Exception:
            rel_log = log_file.as_posix()

        full_report_lines = [
            "=" * 80,
            f"INFORME COMPLETO DE ERRORES DE COMPILACIÓN (SIN TRUNCAR / SIN ELIPSIS)",
            f"Shard ID:       {shard_id}",
            f"Archivo Fuente: {shard_data_path}",
            f"Total Errores:  {len(raw_errors)} ({error_count} consolidados)",
            "=" * 80,
            "",
            "--- RESUMEN CONSOLIDADO ---",
            compact_report,
            "",
            "--- DETALLE EXHAUSTIVO DE DIAGNÓSTICOS (COMPLETO Y SIN RECORTES) ---",
        ]
        for idx_e, err_item in enumerate(raw_errors, 1):
            full_report_lines.append(f"\n[DIAGNÓSTICO #{idx_e}]")
            full_report_lines.append(str(err_item).strip())
        full_report_lines.append("\n" + "=" * 80)
        full_report_text = "\n".join(full_report_lines)
        try:
            log_file.write_text(full_report_text, encoding="utf-8")
        except Exception:
            try:
                fallback_log = shards_dir / f"{shard_id}_compile_error.log"
                fallback_log.parent.mkdir(parents=True, exist_ok=True)
                fallback_log.write_text(full_report_text, encoding="utf-8")
                rel_log = fallback_log.as_posix()
            except Exception:
                pass

        fail_summary = (
            f"[-] FAIL: {len(raw_errors)} errores detectados ({error_count} errores consolidados) "
            f"al compilar {shard_id}:\n{compact_report}" + (f"\n{_EDIT_FILE_REMINDER}" if error_count < 6 else "")
        )
        total_output_bytes = len(fail_summary.encode("utf-8"))

        # Per CONOCIMIENTO_TRIBAL.md §4.3:
        # Runtime stdout truncation limit is 10,240 bytes (10 KiB) - 47 bytes wrapper = 10,193 bytes.
        # Safe threshold is 9,700 bytes. Also check if compact_report truncated items internally.
        ANTIGRAVITY_STDOUT_SAFE_LIMIT = 9700
        is_compact_truncated = (
            "diagnósticos adicionales consolidados" in compact_report
            or "errores totales consolidados en formato compacto" in compact_report
        )
        will_truncate = is_compact_truncated or (total_output_bytes >= ANTIGRAVITY_STDOUT_SAFE_LIMIT)

        top_banner = ""
        if will_truncate:
            top_banner = (
                f"\n"
                f"================================================================================\n"
                f"[!] AVISO: LA SALIDA DE STDOUT SUPERA EL BUFFER ({total_output_bytes}B >= {ANTIGRAVITY_STDOUT_SAFE_LIMIT}B) O FUE TRUNCADA.\n"
                f"    >> INFORME ÍNTEGRO Y COMPLETO EN: {rel_log} <<\n"
                f"[!] ACCIÓN MANDATORIA: Ejecuta `read_file('{rel_log}')` para ver todos los\n"
                f"    diagnósticos exhaustivos, valores numéricos y fórmulas sin recortes ni elipsis.\n"
                f"================================================================================\n"
            )
            print(top_banner, file=sys.stdout)
            try:
                sys.stdout.flush()
            except Exception:
                pass

        if receipt_p:
            try:
                r_data = {}
                if receipt_p.is_file():
                    try:
                        r_data = json.loads(receipt_p.read_text(encoding="utf-8"))
                    except Exception:
                        r_data = {}
                r_data["shard_id"] = shard_id
                r_data["compiled_status"] = "FAIL"
                r_data["compilation_errors"] = [compact_report]
                r_data["full_error_log"] = rel_log
                r_data["error_count"] = error_count
                r_data["has_syntax_error"] = False
                r_data["compiled_at"] = time.time()
                _atomic_write_json(receipt_p, r_data)
            except Exception:
                pass

        if same_error_streak >= 3:
            terminal_stop = (
                f"\n[-] [CIRCUIT BREAKER HALT: 3 fallos consecutivos idénticos para shard '{shard_id}']. "
                f"STOP, send_message the Director."
            )
            compact_report = compact_report + terminal_stop
            fail_summary = fail_summary + terminal_stop
            print(terminal_stop, file=sys.stderr)

        print(f"\n{fail_summary}", file=sys.stderr)
        full_err_out = (top_banner + "\n" + fail_summary) if will_truncate else fail_summary
        state["last_errors"] = [full_err_out]
        state["updated_at"] = time.time()
        _atomic_write_json(compile_att_file, state)
        return False, [full_err_out]

    return promote_staged_templates_atomically(
        att_dir=att_dir,
        cert_path=cert_path,
        compile_att_file=compile_att_file,
        cta_p=cta_p,
        final_paths_by_cid=final_paths_by_cid,
        norm_shard_id=norm_shard_id,
        receipt_p=receipt_p,
        seeds=seeds,
        shard_data_path=shard_data_path,
        shard_id=shard_id,
        shards_dir=shards_dir,
        source_sha256=source_sha256,
        staged_paths=staged_paths,
        strict=strict,
        templates_by_cid=templates_by_cid,
        compiler_file_path=Path(__file__),
    )


def compile_shard_file(
    shard_data_path: Union[str, Path],
    output_dir: Optional[Union[str, Path]] = None,
    strict: bool = True,
    seeds: int = 50,
    min_archetypes: Optional[int] = None,
    templates_per_modality: Optional[int] = None,
    **kwargs,
) -> Tuple[bool, List[str]]:
    """Helper for run.py pipeline stage 3 compatibility."""
    return compile_shard(
        work_dir_or_path=shard_data_path,
        shard_id=kwargs.get("shard_id"),
        strict=strict,
        seeds=seeds,
        output_dir=output_dir,
        min_archetypes=min_archetypes if min_archetypes is not None else kwargs.get("min_archetypes"),
        templates_per_modality=templates_per_modality if templates_per_modality is not None else kwargs.get("templates_per_modality"),
        **kwargs,
    )


def main():
    parser = argparse.ArgumentParser(description="Deterministic Python Tuple Compiler for Content-to-Course v3.21 Shards")
    parser.add_argument("shard_data_path", nargs="?", default=None, help="Optional positional path to shard_XX_data.py")
    parser.add_argument("--input", "-i", dest="input_path", default=None, help="Optional path to shard_XX_data.py")
    parser.add_argument("--output", "-o", dest="output_path", default=None, help="Optional output path or directory")
    parser.add_argument("--cta", default=None, help="Optional path to cta.json")
    parser.add_argument("--manifest", default=None, help="Optional path to manifest")
    parser.add_argument("--work", "--work-dir", dest="work", default="work", help="Path to work directory (default: work)")
    parser.add_argument("--shard", default=None, help="Shard ID to compile (e.g. shard_01)")
    parser.add_argument("--output-dir", default=None, help="Output directory for templates (e.g. work/templates)")
    parser.add_argument("--strict", action="store_true", default=True, help="Enforce strict validation (default: True)")
    parser.add_argument("--no-strict", dest="strict", action="store_false", help="Bypass strict validation")
    parser.add_argument("--seeds", type=int, default=50, help="Number of dry-run seeds (default: 50)")
    parser.add_argument("--min-archetypes", dest="min_archetypes", type=int, default=None, help="Minimum disjoint archetypes (tuples) required per competency in TEMPLATES (default: 4)")
    parser.add_argument("--templates-per-modality", dest="templates_per_modality", type=int, default=None, help="Minimum distinct non-clone templates required per recommended modality (default: 2)")
    parser.add_argument("--watchdog-timeout", type=float, default=90.0, help="Watchdog global process timeout budget in seconds (default: 90.0)")
    parser.add_argument("--fail-total", dest="fail_total", action="store_true", default=True, help="Accumulate all template/tuple validation diagnostics across the shard instead of aborting on the first failure (default)")
    parser.add_argument("--fail-fast", dest="fail_total", action="store_false", help="Abort on first Step 4/5 tuple validation error")
    args = parser.parse_args()

    work_or_path = args.input_path or args.shard_data_path or args.work
    s_id = args.shard
    receipt_path = None
    eff_out_dir = args.output_dir
    if args.output_path:
        if str(args.output_path).lower().endswith(".json"):
            receipt_path = args.output_path
        elif not eff_out_dir:
            eff_out_dir = args.output_path

    if work_or_path == "work" and not (Path("work/shards/pre_shard_manifest.json").is_file() or Path("work/pre_shard_manifest.json").is_file()):
        inferred = infer_work_dir(work_or_path, shard_id=s_id)
        if inferred != Path(work_or_path):
            work_or_path = str(inferred)

    success, _ = compile_shard(
        work_dir_or_path=work_or_path,
        shard_id=s_id,
        strict=args.strict,
        seeds=args.seeds,
        output_dir=eff_out_dir,
        output_path=receipt_path,
        cta_path=args.cta,
        manifest_path=args.manifest,
        min_archetypes=args.min_archetypes,
        templates_per_modality=args.templates_per_modality,
        watchdog_timeout=args.watchdog_timeout,
        fail_total=args.fail_total,
    )
    try:
        sys.stdout.flush()
        sys.stderr.flush()
    except Exception:
        pass
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
