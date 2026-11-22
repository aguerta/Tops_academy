"""Diagnostic formatting and error aggregation for template validation."""

import json
import re
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

from engine.sandbox import call_with_timeout
from engine.shard_locator import ShardDataLineLocator

AGENT_WARNING_NOTE = (
    "NOTA PARA EL AGENTE: NO abras ni inspecciones el código de check_templates.py ni rules.py. "
    "Corrige directamente el texto en tu script generador."
)


class DiagnosticError(str):
    """Enriched diagnostic error string with structured metadata for canonical aggregation."""
    rule_tag: str
    competency: str
    template: str
    item_id: Union[str, List[str]]
    field_name: str
    snippet: str
    cause: str
    actions: List[str]
    lines: List[int]
    file_path: Optional[str]

    def __new__(
        cls,
        content: str,
        rule_tag: str = "",
        competency: str = "",
        template: str = "",
        item_id: Union[str, List[str]] = "",
        field_name: str = "",
        snippet: str = "",
        cause: str = "",
        actions: Optional[List[str]] = None,
        lines: Optional[List[int]] = None,
        file_path: Optional[str] = None,
    ):
        obj = super().__new__(cls, content)
        obj.rule_tag = rule_tag
        obj.competency = competency
        obj.template = template
        obj.item_id = item_id
        obj.field_name = field_name
        obj.snippet = snippet
        obj.cause = cause
        obj.actions = actions or []
        obj.lines = list(lines) if lines else []
        obj.file_path = file_path
        return obj


def format_diagnostic_error(
    rule_tag: str,
    competency: str,
    template: str,
    item_id: Union[str, List[str]],
    field_name: str,
    snippet: str,
    cause: str,
    actions: List[str],
    lines: Optional[List[int]] = None,
    file_path: Optional[str] = None,
) -> DiagnosticError:
    """Format validation error with enriched surgical and prescriptive diagnostics."""
    if isinstance(item_id, list):
        if not item_id:
            items_str = "N/A"
        elif len(item_id) > 5 and all(str(x).startswith("seed=") for x in item_id):
            seed_ints = sorted(int(str(x).split("=")[1]) for x in item_id if "=" in str(x))
            items_str = f"semillas {seed_ints[0]}..{seed_ints[-1]} ({len(item_id)} semillas)"
        elif len(item_id) > 6:
            items_str = f"{item_id[0]}, {item_id[1]}, ... {item_id[-1]} ({len(item_id)} reactivos)"
        elif len(item_id) > 1:
            items_str = ", ".join(str(x) for x in item_id)
        elif len(item_id) == 1:
            items_str = str(item_id[0])
        else:
            items_str = str(item_id)

        if len(item_id) > 1 or "semillas" in items_str or "reactivos" in items_str:
            reactivo_label = "Reactivos"
        else:
            reactivo_label = "Reactivo"
    else:
        items_str = str(item_id)
        reactivo_label = "Reactivo"

    if lines:
        unique_lines = sorted(set(lines))
        if len(unique_lines) == 1:
            lines_str = f", Línea: {unique_lines[0]}"
        else:
            lines_str = f", Líneas: {', '.join(str(l) for l in unique_lines)} ({len(lines)} ocurrencias)"
    else:
        lines_str = ""

    actions_formatted = "\n".join(f"      {idx + 1}. {act}" for idx, act in enumerate(actions))
    primary_action = actions[0] if actions else "Corrige el archivo generador."
    raw_str = (
        f"[-] [{rule_tag}]\n"
        f"    UBICACIÓN: Competencia: '{competency}', Plantilla: '{template}', {reactivo_label}: '{items_str}'{lines_str}, Campo: '{field_name}'\n"
        f"    FRAGMENTO INFRACTOR: {snippet}\n"
        f"    CAUSA: {cause}\n"
        f"    ACTION REQUIRED: {primary_action}\n"
        f"    ACCIONES CORRECTIVAS:\n"
        f"{actions_formatted}\n"
        f"    {AGENT_WARNING_NOTE}"
    )
    return DiagnosticError(
        raw_str,
        rule_tag=rule_tag,
        competency=competency,
        template=template,
        item_id=item_id,
        field_name=field_name,
        snippet=snippet,
        cause=cause,
        actions=actions,
        lines=lines or [],
        file_path=file_path,
    )


def find_lines_in_file(fpath: Path, pattern: str) -> List[int]:
    """Scan file lines for a pattern or snippet to dynamically identify offending lines."""
    if not fpath.is_file() or not pattern:
        return []
    try:
        lines = fpath.read_text(encoding="utf-8", errors="replace").splitlines()
        clean_pat = pattern.strip()
        if len(clean_pat) > 50:
            clean_pat = clean_pat[:50].strip()
        found = []
        for idx, line in enumerate(lines, start=1):
            if clean_pat in line:
                found.append(idx)
        return found
    except Exception:
        return []


def find_template_field_line(fpath: Path, tpl_id: str, field_name: Optional[str] = None) -> List[int]:
    """Scan file lines to locate template ID block and optionally field_name within that block."""
    if not fpath.is_file() or not tpl_id:
        return []
    try:
        lines = fpath.read_text(encoding="utf-8", errors="replace").splitlines()
        tpl_idx = -1
        # Find template id line
        for idx, l in enumerate(lines, start=1):
            if f'"{tpl_id}"' in l or f"'{tpl_id}'" in l:
                tpl_idx = idx
                break
        if tpl_idx == -1:
            return []
        if not field_name:
            return [tpl_idx]
        # Search forward for field_name until next template id or end of object
        field_target = f'"{field_name}"'
        field_target_alt = f"'{field_name}'"
        for idx in range(tpl_idx, min(tpl_idx + 150, len(lines) + 1)):
            line_str = lines[idx - 1]
            if field_target in line_str or field_target_alt in line_str:
                return [idx]
            # Stop if we hit the next template
            if idx > tpl_idx and ('"id":' in line_str or "'id':" in line_str):
                break
        return [tpl_idx]
    except Exception:
        return []


def extract_diagnostic_metadata(err: Union[str, DiagnosticError]) -> Dict[str, Any]:
    """Extract canonical diagnostic metadata from DiagnosticError or traditional formatted string."""
    if isinstance(err, DiagnosticError) and getattr(err, "rule_tag", None):
        return {
            "rule_tag": err.rule_tag,
            "competency": err.competency,
            "template": err.template,
            "field_name": err.field_name,
            "snippet": err.snippet,
            "cause": err.cause,
            "action": err.actions[0] if err.actions else "Corregir archivo",
            "lines": list(err.lines),
            "file_path": err.file_path,
        }

    err_str = str(err)
    if "[M3-ARCHETYPES]" in err_str:
        rule_tag = "M3-ARCHETYPES"
        m_cid = (
            re.search(r"competencia\s+'([^']+)'", err_str, re.IGNORECASE)
            or re.search(r"tuplas\s+de\s+'([^']+)'", err_str, re.IGNORECASE)
            or re.search(r"^([A-Za-z0-9_-]+)\.json", err_str)
        )
        comp = m_cid.group(1).strip() if m_cid else ""
        tpl = f"T-{comp}" if comp else ""
        field_name = "TEMPLATES"
        m_cause_m3 = re.search(r"\[M3-ARCHETYPES\]\s*(.+?)(?:\s*Nota:|\Z)", err_str)
        cause = m_cause_m3.group(1).strip() if m_cause_m3 else err_str.splitlines()[0]
        if "clones idénticos" in err_str:
            action = (
                f"Cada uno de los arquetipos de '{comp}' debe tener su propio enunciado y wrapper/generador disjunto (gen_1..4)."
                if comp else "Diversificar enunciados y generadores de cada arquetipo."
            )
        else:
            action = (
                f"Agregar tuplas faltantes para '{comp}' en TEMPLATES usando helper parametrizado def _gen_{comp.lower().replace('-', '_')}(rng, arch) + 4 wrappers gen_1..4."
                if comp else "Agregar tuplas de arquetipos faltantes en TEMPLATES usando helper parametrizado."
            )
        snippet = f"TEMPLATES[{comp}]" if comp else "TEMPLATES"
        return {
            "rule_tag": rule_tag,
            "competency": comp,
            "template": tpl,
            "field_name": field_name,
            "snippet": snippet,
            "cause": cause,
            "action": action,
            "lines": [],
            "file_path": None,
        }

    if "[STEM-DIVERSITY-GATE]" in err_str or "[DIAG-MAGIC-MULT]" in err_str or "[PSYCHOMETRIC-OPTIONS" in err_str or "[VERIFIER-TAUTOLOGY-DETECTED]" in err_str:
        if "[STEM-DIVERSITY-GATE]" in err_str:
            rule_tag = "STEM-DIVERSITY-GATE"
        elif "[DIAG-MAGIC-MULT]" in err_str:
            rule_tag = "DIAG-MAGIC-MULT"
        elif "[VERIFIER-TAUTOLOGY-DETECTED]" in err_str:
            rule_tag = "VERIFIER-TAUTOLOGY-DETECTED"
        elif "parenthetical_telltale_linter" in err_str:
            rule_tag = "PSYCHOMETRIC-OPTIONS / parenthetical_telltale_linter"
        else:
            rule_tag = "PSYCHOMETRIC-OPTIONS"
        m_cid = (
            re.search(r"competency\s+'([^']+)'", err_str, re.IGNORECASE)
            or re.search(r"^([A-Za-z0-9_-]+)\.json", err_str)
        )
        comp = m_cid.group(1).strip() if m_cid else ""
        m_tpl = re.search(r"[Ee]n\s+'([^']+)'", err_str)
        tpl = m_tpl.group(1).strip() if m_tpl else (f"T-{comp}" if comp else "")
        m_body = re.search(r"\[(?:STEM-DIVERSITY-GATE|DIAG-MAGIC-MULT|PSYCHOMETRIC-OPTIONS|VERIFIER-TAUTOLOGY-DETECTED)(?:[ /A-Za-z0-9_-]*)\]\s*(.+)", err_str)
        body_txt = m_body.group(1).strip() if m_body else err_str
        lines: List[int] = []
        m_line_direct = re.search(r"L[íi]neas?\s*(\d+)", err_str)
        if m_line_direct:
            lines = [int(m_line_direct.group(1))]

        if rule_tag == "VERIFIER-TAUTOLOGY-DETECTED":
            m_fn = re.search(r"ver_fn\s*'([^']+)'", err_str)
            fn_name = m_fn.group(1).strip() if m_fn else "ver_fn"
            m_dist = re.search(r"distractor falso\s*'([^']*)'", err_str)
            dist_val = m_dist.group(1).strip() if m_dist else ""
            line_str = f" (Línea {lines[0]})" if lines else ""
            dist_str = f" '{dist_val}'" if dist_val else " incorrecto"
            cause = f"[{rule_tag}] Verificador ver_fn '{fn_name}' en '{tpl}'{line_str} no refuta distractor{dist_str}."
            action = "Modificar ver_fn para refutar este distractor falso (verificar propiedades analíticas reales, sin tautología)."
        elif "Provide >=" in body_txt:
            parts = body_txt.split("Provide >=", 1)
            cause = f"[{rule_tag}] {parts[0].strip()}"
            action = f"Provide >= {parts[1].strip()}"
        elif "PROHIBIDO ajustar multiplicadores" in body_txt or "Reemplaza los multiplicadores" in body_txt:
            parts = re.split(r"(?:PROHIBIDO ajustar multiplicadores.*?|Reemplaza los multiplicadores.*)", body_txt)
            cause = f"[{rule_tag}] {parts[0].strip()}"
            action = "PROHIBIDO ajustar multiplicadores decimales; reemplace la expresión por la fórmula algebraica del error conceptual."
        elif "Elimina coletillas parentéticas" in body_txt:
            parts = body_txt.split("Elimina coletillas parentéticas", 1)
            cause = f"[{rule_tag}] {parts[0].strip()}"
            action = f"Elimina coletillas parentéticas {parts[1].strip()}"
        else:
            cause = f"[{rule_tag}] {body_txt}"
            action = "Corregir en las líneas indicadas de shard_XX_data.py."
        return {
            "rule_tag": rule_tag,
            "competency": comp,
            "template": tpl,
            "field_name": "TEMPLATES",
            "snippet": tpl or comp,
            "cause": cause,
            "action": action,
            "lines": lines,
            "file_path": None,
        }

    m_rule = re.search(r"^\[-\]\s*\[([^\]]+)\]", err_str, re.MULTILINE)
    m_loc = re.search(r"UBICACI[ÓO]N:\s*Competencia:\s*'([^']*)',\s*Plantilla:\s*'([^']*)'.*?Campo:\s*'([^']*)'", err_str)
    m_lines = re.search(r"L[íi]neas?:\s*([0-9,\s]+)", err_str)
    m_cause = re.search(r"CAUSA:\s*(.+)", err_str)
    m_act = re.search(r"ACTION REQUIRED:\s*(.+)", err_str)
    m_snip = re.search(r"FRAGMENTO INFRACTOR:\s*(.+)", err_str)

    rule_tag = m_rule.group(1).strip() if m_rule else "GENERAL: VALIDATION_ERROR"
    comp = m_loc.group(1).strip() if m_loc else ""
    tpl = m_loc.group(2).strip() if m_loc else ""
    field_name = m_loc.group(3).strip() if m_loc else ""
    cause = m_cause.group(1).strip() if m_cause else err_str.splitlines()[0]
    action = m_act.group(1).strip() if m_act else "Corregir el archivo infractor."
    snippet = m_snip.group(1).strip() if m_snip else ""

    lines: List[int] = []
    if m_lines:
        for num in re.findall(r"\d+", m_lines.group(1)):
            lines.append(int(num))

    return {
        "rule_tag": rule_tag,
        "competency": comp,
        "template": tpl,
        "field_name": field_name,
        "snippet": snippet,
        "cause": cause,
        "action": action,
        "lines": lines,
        "file_path": None,
    }




def normalize_error_string_for_hash(text: str) -> str:
    """Normalize volatile elements in error messages (hex addresses, module uuids, temp paths, timestamps, CRLF) for deterministic hashing."""
    if not isinstance(text, str):
        text = str(text)
    # Normalize CRLF and backslashes
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = text.replace("\\", "/")
    # Strip memory addresses
    text = re.sub(r"at 0x[0-9a-fA-F]+", "at 0xHEX", text)
    # Strip ephemeral module names generated with random UUIDs
    text = re.sub(r"c2c_(?:shard|fix)_mod_[a-zA-Z0-9_-]+_[0-9a-fA-F]{6,8}", "c2c_mod", text)
    # Strip timestamps (ISO, RFC, or common date formats)
    text = re.sub(r"\b\d{4}-\d{2}-\d{2}[T\s]\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})?\b", "<TIMESTAMP>", text)
    # Strip temp paths and staging paths
    text = re.sub(r"(?:[A-Za-z]:)?/[^\s:]*?/(?:\.?tmp|temp|\.check_attempts/_staged)[^\s:]*", "<TEMP_PATH>", text, flags=re.IGNORECASE)
    # Strip ephemeral tmp file names
    text = re.sub(r"\.[a-zA-Z0-9_-]+\.tmp\.\d+_[0-9a-fA-F]+", "<TMP_FILE>", text)
    return text.strip()




def _format_dry_failure(
    competency_id: str = "UNKNOWN",
    tpl_id: str = "UNKNOWN",
    generate_py: str = "",
    failing_seed: int = 100,
    cross_check_py: Optional[str] = None,
    shard_py: Optional[Union[str, Path]] = None,
    exc: Optional[Exception] = None,
    params: Optional[Dict[str, Any]] = None,
    print_output: bool = True,
    raw_error: Optional[str] = None,
) -> str:
    """Format and print TPL-DRY failure diagnostics with line-mapped traceback frames.

    Reports:
    - First failing seed
    - Generator parameters for that seed
    - type(exc).__name__: str(exc)
    - Last 3 traceback frames mapped to shard_XX_data.py source lines
    """
    import inspect
    import traceback
    from engine.sandbox import build_sandbox_globals, _LazyNPRNG

    extracted_params: Dict[str, Any] = dict(params) if params else {}

    # If exc or params not provided, execute generate(rng) for failing_seed to capture live state
    if (exc is None or not extracted_params) and generate_py:
        try:
            env = build_sandbox_globals()
            import random
            random.seed(failing_seed)
            rng = random.Random(failing_seed)
            rng.np = _LazyNPRNG(failing_seed)
            compiled = compile(generate_py, "<generate_py>", "exec")
            exec(compiled, env)
            gen_fn = env.get("generate")
            if gen_fn:
                try:
                    res = call_with_timeout(gen_fn, args=(rng,), timeout=0.4, seed=failing_seed)
                    if isinstance(res, dict) and "vars" in res and isinstance(res["vars"], dict):
                        if not extracted_params:
                            extracted_params = {k: v for k, v in res["vars"].items()}
                    if cross_check_py:
                        cc_env = build_sandbox_globals()
                        cc_compiled = compile(cross_check_py, "<cross_check_py>", "exec")
                        exec(cc_compiled, cc_env)
                        ver_fn = cc_env.get("verify")
                        if ver_fn:
                            cc_res = call_with_timeout(ver_fn, args=(res,), timeout=0.4, seed=failing_seed)
                            if cc_res is False:
                                raise AssertionError("cross_check verification returned False")
                except Exception as run_e:
                    if exc is None:
                        exc = run_e
                    if not extracted_params:
                        tb = run_e.__traceback__
                        while tb:
                            f = tb.tb_frame
                            if f.f_code.co_name == "generate":
                                for k, v in f.f_locals.items():
                                    if k not in ("rng", "__builtins__") and not callable(v) and not inspect.ismodule(v):
                                        extracted_params[k] = v
                                break
                            tb = tb.tb_next
        except Exception as comp_e:
            if exc is None:
                exc = comp_e

    # Format exception name and message
    if exc is not None:
        exc_str = f"{type(exc).__name__}: {exc}"
    elif raw_error:
        exc_str = str(raw_error)
    else:
        exc_str = "Exception: Unknown error during dry-run execution"

    # Extract traceback frames
    tb_frames = []
    if exc is not None and exc.__traceback__ is not None:
        tb_frames = traceback.extract_tb(exc.__traceback__)

    # Strip internal frames (compile_shard.py, check_templates.py, engine/)
    clean_frames = []
    for fr in tb_frames:
        fn = str(fr.filename).replace("\\", "/").lower()
        if any(skip in fn for skip in ("check_templates.py", "compile_shard.py", "engine/sandbox.py", "engine/assemble.py")):
            continue
        if fr.name in ("_format_dry_failure", "execute_sandbox_batch", "check_single_template"):
            continue
        clean_frames.append(fr)
    if not clean_frames and tb_frames:
        clean_frames = [tb_frames[-1]]
    if not clean_frames:
        clean_frames = [traceback.FrameSummary("<sandbox>", 1, "generate", line="")]

    last_frames = clean_frames[-3:] if len(clean_frames) >= 3 else clean_frames

    # Map frames to shard_XX_data.py or modular shard_fixes/<CID>.py source lines
    shard_obj = Path(shard_py).resolve() if shard_py and Path(shard_py).is_file() else None
    fix_obj = None
    if shard_py:
        sp = Path(shard_py).resolve()
        shards_dir = sp.parent if sp.parent.name == "shards" else sp.parent / "shards"
        fixes_dir = shards_dir / "shard_fixes"
        if fixes_dir.is_dir():
            # Check shard-specific subdirectory first, then flat fallback
            shard_id_hint = sp.stem.replace("_data", "")
            cand_dirs = [fixes_dir / shard_id_hint, fixes_dir]
            for c_dir in cand_dirs:
                if c_dir.is_dir():
                    for f in c_dir.glob("*.py"):
                        if f.stem in (competency_id, competency_id.replace("-", "_")):
                            fix_obj = f
                            break
                if fix_obj:
                    break
    if fix_obj:
        shard_obj = fix_obj

    locator = None
    if shard_obj and ShardDataLineLocator:
        try:
            locator = ShardDataLineLocator(shard_obj)
        except Exception:
            locator = None

    frame_lines = []
    for fr in last_frames:
        fr_lineno = fr.lineno or 1
        fr_name = fr.name
        fr_line = fr.line or ""

        rel_fix_str = str(fix_obj.relative_to(shards_dir)).replace("\\", "/") if (fix_obj and 'shards_dir' in locals()) else (f"shard_fixes/{shard_obj.name}" if fix_obj else (shard_obj.name if shard_obj else fr.filename))
        mapped_file = rel_fix_str if fix_obj else (shard_obj.name if shard_obj else fr.filename)
        mapped_lineno = fr_lineno
        mapped_code = fr_line

        if locator:
            if fr_name in locator.functions:
                fn_start, _ = locator.functions[fr_name]
                mapped_lineno = fn_start + fr_lineno - 1
            else:
                t_info = locator.get_tuple_info(competency_id) or locator.get_tuple_info(tpl_id)
                if t_info:
                    gen_fn_name = t_info.get("gen_fn_name")
                    if gen_fn_name and gen_fn_name in locator.functions:
                        fn_start, _ = locator.functions[gen_fn_name]
                        mapped_lineno = fn_start + fr_lineno - 1
                    else:
                        gen_elt = t_info.get("elements", {}).get("generator_code", {})
                        gen_start = gen_elt.get("start_line", t_info.get("start_line", 1))
                        mapped_lineno = gen_start + fr_lineno - 1
            if 1 <= mapped_lineno <= len(locator.lines):
                mapped_code = locator.lines[mapped_lineno - 1].strip()

        frame_lines.append(
            f"      File \"{mapped_file}\", line {mapped_lineno}, in {fr_name}\n        {mapped_code}"
        )

    shard_label = str(fix_obj.relative_to(shards_dir)).replace("\\", "/") if (fix_obj and 'shards_dir' in locals()) else (f"shard_fixes/{shard_obj.name}" if fix_obj else (shard_obj.name if shard_obj else "shard_XX_data.py"))
    report_lines = [
        f"[-] [TPL-DRY: FALLO EN EJECUCIÓN DRY-RUN]",
        f"    Competencia: {competency_id} | Plantilla: {tpl_id}",
        f"    Primer seed fallido: {failing_seed}",
        f"    Parámetros: {extracted_params}",
        f"    Excepción: {exc_str}",
        f"    Traceback (últimos {len(frame_lines)} frames mapeados a {shard_label}):",
    ]
    report_lines.extend(frame_lines)

    formatted_msg = "\n".join(report_lines)
    if print_output:
        print(formatted_msg, file=sys.stderr)
    return formatted_msg


def build_compact_diagnostic_groups(
    errors: List[Union[str, DiagnosticError]],
    targets: Optional[List[Path]] = None,
    shard_py: Optional[Union[str, Path]] = None,
) -> Tuple[Dict[str, Dict[Tuple[str, str], Dict[Tuple[str, str], List[int]]]], int]:
    """Group diagnostic errors canonicalized by rule_tag, file_path/shard_ref, and cause/action.

    Returns:
        (grouped_dict, total_items_count)
    """
    if not errors:
        return {}, 0

    # Build or lookup ShardDataLineLocator
    locators_by_path: Dict[str, Any] = {}
    default_locator = None
    if shard_py and Path(shard_py).is_file() and ShardDataLineLocator:
        default_locator = ShardDataLineLocator(shard_py)
        locators_by_path[str(Path(shard_py).resolve())] = default_locator

    cid_to_shard_path: Dict[str, Path] = {}
    manifest_candidates = [
        Path("work/shards/pre_shard_manifest.json"),
        Path("shards/pre_shard_manifest.json"),
        Path("work/pre_shard_manifest.json"),
    ]
    if targets and targets[0].parent:
        manifest_candidates.insert(0, targets[0].parent.parent / "shards" / "pre_shard_manifest.json")
        manifest_candidates.insert(1, targets[0].parent / "pre_shard_manifest.json")

    for mc in manifest_candidates:
        if mc.is_file():
            try:
                m_data = json.loads(mc.read_text(encoding="utf-8"))
                for s in m_data.get("shards", []):
                    sp = s.get("shard_data_path")
                    if sp and Path(sp).is_file():
                        sp_obj = Path(sp).resolve()
                        for cid_item in s.get("competency_ids", []):
                            cid_to_shard_path[str(cid_item)] = sp_obj
                        for c_item in s.get("competencies", []):
                            if isinstance(c_item, dict) and "id" in c_item:
                                cid_to_shard_path[str(c_item["id"])] = sp_obj
                break
            except Exception:
                pass

    records = []
    for err in errors:
        rec = extract_diagnostic_metadata(err)
        fpath = rec["file_path"]
        if not fpath and rec["competency"]:
            cid = rec["competency"]
            # Prioritize matching target path first
            matched_target: Optional[Path] = None
            if targets:
                for t in targets:
                    t_path = Path(t)
                    if t_path.is_file() and (t_path.stem == cid or cid in t_path.stem):
                        matched_target = t_path
                        break
                    elif t_path.is_dir() and (t_path / f"{cid}.json").is_file():
                        matched_target = t_path / f"{cid}.json"
                        break
                    elif t_path.stem == cid:
                        matched_target = t_path
                        break
            if matched_target:
                try:
                    fpath = matched_target.resolve().relative_to(Path.cwd().resolve()).as_posix()
                except Exception:
                    fpath = matched_target.as_posix()
            else:
                cand1 = Path("work/templates") / f"{cid}.json"
                cand2 = Path("templates") / f"{cid}.json"
                if cand1.is_file():
                    fpath = str(cand1.as_posix())
                elif cand2.is_file():
                    fpath = str(cand2.as_posix())
                elif targets and targets[0].parent:
                    cand_t = targets[0].parent / f"{cid}.json"
                    try:
                        fpath = cand_t.resolve().relative_to(Path.cwd().resolve()).as_posix()
                    except Exception:
                        fpath = cand_t.as_posix()
                elif targets:
                    try:
                        fpath = Path(targets[0]).resolve().relative_to(Path.cwd().resolve()).as_posix()
                    except Exception:
                        fpath = str(targets[0].as_posix())
                else:
                    fpath = f"work/templates/{cid}.json"
        elif not fpath and targets:
            try:
                fpath = Path(targets[0]).resolve().relative_to(Path.cwd().resolve()).as_posix()
            except Exception:
                fpath = str(targets[0].as_posix())
        else:
            fpath = fpath or "work/templates"

        if fpath:
            try:
                p_fpath = Path(fpath)
                if p_fpath.is_absolute() and p_fpath.is_relative_to(Path.cwd()):
                    fpath = p_fpath.relative_to(Path.cwd()).as_posix()
            except Exception:
                pass

        rec["file_path"] = fpath

        # Locate lines dynamically if not present
        if not rec["lines"] and rec["file_path"]:
            p = Path(rec["file_path"])
            if p.is_file():
                search_term = rec["snippet"] or rec["template"]
                if search_term and len(search_term) >= 3:
                    rec["lines"] = find_lines_in_file(p, search_term)
                if not rec["lines"] and rec.get("template"):
                    rec["lines"] = find_template_field_line(p, rec["template"], rec.get("field_name"))

        # Map to shard_XX_data.py line range
        cid_val = rec["competency"]
        shard_ref = ""
        target_locator = default_locator
        if not target_locator and cid_val and cid_val in cid_to_shard_path and ShardDataLineLocator:
            sp_obj = cid_to_shard_path[cid_val]
            sp_key = str(sp_obj)
            if sp_key not in locators_by_path:
                locators_by_path[sp_key] = ShardDataLineLocator(sp_obj)
            target_locator = locators_by_path[sp_key]

        if target_locator:
            lookup_key = cid_val or rec.get("template") or ""
            t_info = target_locator.get_tuple_info(lookup_key) if lookup_key else None
            if not t_info and rec.get("template"):
                t_cand = rec["template"].replace("T-", "")
                t_info = target_locator.get_tuple_info(t_cand)
            if not t_info and len(target_locator.tuples) == 1:
                t_info = target_locator.tuples[0]
            if t_info:
                s_l = t_info["start_line"]
                e_l = t_info["end_line"]
                shard_ref = f" [Tupla en {target_locator.file_path.name}: Líneas {s_l}..{e_l} (StartLine: {s_l}, EndLine: {e_l})]"

        rec["shard_ref"] = shard_ref
        records.append(rec)

    # Group by rule_tag -> (file_path, shard_ref) -> (cause, action) -> lines
    grouped: Dict[str, Dict[Tuple[str, str], Dict[Tuple[str, str], List[int]]]] = defaultdict(
        lambda: defaultdict(lambda: defaultdict(list))
    )

    for r in records:
        rtag = r["rule_tag"]
        fp = r["file_path"]
        s_ref = r.get("shard_ref", "")
        # Zero artificial limits: causes and actions are preserved 100% in full
        scause = r["cause"]
        sact = r["action"]

        grouped[rtag][(fp, s_ref)][(scause, sact)].extend(r["lines"])

    total_items = sum(len(err_map) for file_map in grouped.values() for err_map in file_map.values())
    return grouped, total_items


def count_distinct_shard_error_hunks(
    raw_errors: List[Union[str, DiagnosticError]],
    targets: Optional[List[Path]] = None,
    shard_py: Optional[Union[str, Path]] = None,
) -> int:
    """Count the number of deduplicated/consolidated diagnostic hunks.

    Guarantees >= 1 when raw_errors is not empty, representing distinct logical issues
    rather than per-seed duplicates.
    """
    if not raw_errors:
        return 0
    _, total_items = build_compact_diagnostic_groups(raw_errors, targets=targets, shard_py=shard_py)
    return max(1, total_items)


def render_compact_aggregated_errors(
    errors: List[Union[str, DiagnosticError]],
    targets: Optional[List[Path]] = None,
    max_output_lines: int = 60,
    shard_py: Optional[Union[str, Path]] = None,
) -> str:
    """Render canonical LLM-optimized single-line aggregated error output grouped by rule (< 30 lines)."""
    if not errors:
        return ""

    has_cb = any("CIRCUIT BREAKER" in str(e) for e in errors)
    header = (
        f"FAIL: CIRCUIT BREAKER TRIPPED ({len(errors)} errores en templates):"
        if has_cb
        else f"FAIL: {len(errors)} validaciones fallidas en templates:"
    )

    grouped, total_items = build_compact_diagnostic_groups(errors, targets=targets, shard_py=shard_py)
    hunk_count = max(1, total_items)

    if hunk_count < 6:
        directive_line = f"[UMBRAL < 6 ({hunk_count}/5 errores)]: Usa edit_file quirúrgico o write_file(Overwrite=True) si el archivo tiene < 300 líneas para corregir todo en 1 turno atómico."
    else:
        directive_line = f"[UMBRAL >= 6 ({hunk_count} errores)]: Usa write_file modular en shard_fixes/<CID>.py (1-2 comps) o write_file(Overwrite=True) completo."

    out_lines = [header, ""]
    truncated = False
    total_rendered_items = 0

    # Reserve room for truncation message (1 line) and directive_line (1 line)
    line_limit = max(2, max_output_lines - 3)

    for rtag, file_map in grouped.items():
        if len(out_lines) >= line_limit:
            truncated = True
            break
        m_rid = re.match(r"^([A-Za-z0-9_-]+)", rtag)
        short_rid = m_rid.group(1) if m_rid else rtag
        out_lines.append(f"[-] [{rtag}]")

        for (fp, s_ref), err_map in file_map.items():
            if len(out_lines) >= line_limit:
                truncated = True
                break
            for (cause, act), l_list in err_map.items():
                if len(out_lines) >= line_limit:
                    truncated = True
                    break
                uniq_lines = sorted(set(l_list))
                if uniq_lines:
                    if len(uniq_lines) > 5:
                        lines_str = f":L{uniq_lines[0]}-{uniq_lines[-1]} ({len(uniq_lines)} líneas)"
                    else:
                        lines_str = f":L{','.join(str(x) for x in uniq_lines)}"
                else:
                    lines_str = ""

                # Canonical single-line output containing: RULE, FILE, LINES, SHARD_TUPLE_REF, CAUSE, ACTION
                out_lines.append(f"  • [{short_rid}] {fp}{lines_str}{s_ref} -> Causa: {cause} | Acción: {act}")
                total_rendered_items += 1
        out_lines.append("")

    if truncated or total_rendered_items < total_items:
        remaining = total_items - total_rendered_items
        if remaining > 0:
            out_lines.append(f"  ... y {remaining} diagnósticos adicionales consolidados.")

    out_lines.append(directive_line)

    res_str = "\n".join(out_lines).strip()
    res_lines = res_str.splitlines()
    if len(res_lines) > max_output_lines:
        if max_output_lines >= 3:
            res_lines = res_lines[:max_output_lines - 2] + [
                f"  ... ({len(errors)} errores totales consolidados en formato compacto < 30 líneas).",
                directive_line,
            ]
        elif max_output_lines == 2:
            res_lines = [res_lines[0], directive_line]
        else:
            res_lines = [directive_line]
        res_str = "\n".join(res_lines)
    return res_str


def get_canonical_invariant_key(inv_err: str) -> str:
    """Derive canonical grouping key for invariant errors to aggregate dynamic values across seeds."""
    clean = inv_err.strip()
    if "Distractor identical to correct answer" in clean:
        return "Distractor identical to correct answer"
    if "Duplicate option content detected" in clean:
        return "Duplicate option content detected"
    if "Length anti-giveaway violation" in clean:
        if "too short" in clean:
            return "Length anti-giveaway: correct option too short"
        return "Length anti-giveaway: correct option too long"
    if "MS length anti-giveaway violation" in clean:
        if "too short" in clean:
            return "MS length anti-giveaway: correct options too short"
        return "MS length anti-giveaway: correct options too long"
    if "open_symbolic variable collision" in clean:
        return "open_symbolic variable collision: symbolic variable numerically bound in vars"
    if "Phantom numeric leak in open_symbolic" in clean:
        return "Phantom numeric leak in open_symbolic diagnostic_distractors.error_rationale"
    if "leaked verbatim in stem text" in clean:
        return "Correct answer leaked verbatim in stem text"
    if "leaked verbatim in first hint" in clean:
        return "Correct answer leaked verbatim in first hint"
    if "Synthetic boilerplate distractor" in clean:
        return "Synthetic boilerplate distractor pattern detected"
    if "Scaffolding answer leak" in clean:
        return "Scaffolding answer leak detected in hint"
    if "Metainformación delatora en distractor visible" in clean:
        return "Metainformación delatora en distractor visible"
    if "Metainformación delatora parentética" in clean:
        return "Metainformación delatora parentética en opción visible"
    if "Distractor con prefijo sintético de clonación" in clean:
        return "Distractor con prefijo sintético de clonación"
    if "Envenenamiento anti-socrático" in clean:
        return "Envenenamiento anti-socrático en pista"
    if "Fuga prematura de clave correcta" in clean:
        return "Fuga prematura de clave correcta en pista"
    if "palabra clave stub" in clean or "ID de competencia stub" in clean:
        return "Pista stub en lugar de andamiaje socrático"
    if "Relleno artificial de longitud" in clean:
        return "Relleno artificial de longitud en opción"
    if "Corrupción matemática de cuantificador universal" in clean:
        return "Corrupción matemática de cuantificador universal"
    if "[TPL-KATEX-SYMPY-LEAK]" in clean:
        return "[TPL-KATEX-SYMPY-LEAK] Raw SymPy syntax leaked inside KaTeX math"
    if "[TPL-TAUTOLOGICAL-IDENTITY]" in clean:
        return "[TPL-TAUTOLOGICAL-IDENTITY] Redundant self-identity in solution/hints"
    m_var = re.search(r"Unsubstituted template variable '\{([^}]+)\}' detected in (.+)", clean)
    if m_var:
        return f"Unsubstituted variable '{{{m_var.group(1)}}}' in {m_var.group(2).rstrip('.')}"
    m_math = re.search(r"(Unbalanced curly braces in LaTeX math expression in [^:]+)", clean)
    if m_math:
        return m_math.group(1)
    norm = re.sub(r"'[^']*'", "'...'", clean)
    norm = re.sub(r"\b\d+\b", "N", norm)
    return norm


def format_invariant_error_diagnostic(
    cid: str,
    tpl_id: str,
    q_id: Union[str, List[str]],
    inv_err: str,
    q_obj: Optional[Dict[str, Any]] = None,
) -> str:
    """Formats an error from check_instance_invariants into the enriched diagnostic structure."""
    inv_clean = inv_err.strip()

    # Case A-pre: Parenthetical telltale clue in visible options
    if "parenthetical_telltale_linter" in inv_clean or "Metainformación delatora parentética" in inv_clean:
        m_tt = re.search(r"'(.*?)'", inv_clean)
        snippet = m_tt.group(1) if m_tt else inv_clean
        cause = f"Metainformación delatora parentética en opción visible: '{snippet}'."
        actions = [
            "Elimina coletillas parentéticas del texto visible de la opción.",
            "Traslada explicaciones conceptuales a 'error_rationale' o 'sol'.",
            "Asegura que el estudiante deduzca la respuesta por razonamiento matemático.",
        ]
        return format_diagnostic_error("PSYCHOMETRIC-OPTIONS", cid, tpl_id, q_id, "options", snippet, cause, actions)

    # Case A-pre2: Telltale cues / Distractor confession in visible options
    if "distractor_integrity_linter" in inv_clean or "Metainformación delatora en distractor visible" in inv_clean:
        m_tt = re.search(r"'(.*?)'", inv_clean)
        snippet = m_tt.group(1) if m_tt else inv_clean
        cause = f"Metainformación delatora en distractor visible: '{snippet}'."
        actions = [
            "Elimina palabras y frases delatoras ('erróneamente', 'incorrectamente', 'falsamente', etc.) del texto visible del distractor.",
            "Formula la opción de forma neutral y afirmativa presentando el procedimiento matemático erróneo sin calificarlo.",
            "Traslada la justificación diagnóstica de la concepción errónea a 'error_rationale'.",
        ]
        return format_diagnostic_error("PSYCHOMETRIC-OPTIONS / DISTRACTOR-INTEGRITY", cid, tpl_id, q_id, "options", snippet, cause, actions)

    # Case A-pre3: Cloned distractor prefix / value
    if "cloned_distractor_value_linter" in inv_clean or "prefijo sintético de clonación" in inv_clean or "clonado con valor idéntico" in inv_clean:
        m_cl = re.search(r"'(.*?)'", inv_clean)
        snippet = m_cl.group(1) if m_cl else inv_clean
        cause = f"Distractor sintético o clonado: '{snippet}'."
        actions = [
            "Elimina prefijos sintéticos como 'Opción alterna N:' o 'Variante N:'.",
            "Formula cada distractor a partir de una concepción errónea o error de cálculo verosímil y auténtico.",
        ]
        return format_diagnostic_error("PSYCHOMETRIC-OPTIONS / CLONED-DISTRACTOR", cid, tpl_id, q_id, "options", snippet, cause, actions)

    # Case A-pre4: Anti-Socratic hint poisoning / Answer leak in hints
    if "socratic_scaffolding_integrity_linter" in inv_clean or "Envenenamiento anti-socrático" in inv_clean or "Fuga prematura de clave" in inv_clean or "Pista" in inv_clean and "stub" in inv_clean:
        m_sc = re.search(r"'(.*?)'", inv_clean)
        snippet = m_sc.group(1) if m_sc else inv_clean
        cause = f"Fallo de andamiaje socrático en pistas: {inv_clean}"
        actions = [
            "No incluyas distractores ni errores conceptuales bajo frases como 'asegurando considerar adecuadamente'.",
            "Evita revelar la solución exacta en las primeras pistas (Pista 1 o 2).",
            "Formula pistas socráticas progresivas que guíen el razonamiento del estudiante.",
        ]
        return format_diagnostic_error("SCAFFOLDING-INTEGRITY", cid, tpl_id, q_id, "hints", snippet, cause, actions)

    # Case A-pre5: Artificial length padding
    if "Relleno artificial de longitud" in inv_clean:
        m_pad = re.search(r"'(.*?)'", inv_clean)
        snippet = m_pad.group(1) if m_pad else inv_clean
        cause = f"Relleno artificial de longitud en opción visible: '{snippet}'."
        actions = [
            "Elimina coletillas burocráticas o cláusulas de relleno en opciones.",
            "Asegura que la longitud de las opciones sea natural y coherente con el contenido matemático.",
        ]
        return format_diagnostic_error("ANTI-GAMING-PADDING", cid, tpl_id, q_id, "options", snippet, cause, actions)

    # Case A-pre6: Vacuous universal quantifier
    if "Corrupción matemática de cuantificador universal" in inv_clean:
        cause = f"Corrupción matemática de cuantificador universal: {inv_clean}."
        actions = [
            "No sustituyas 'epsilon' por una constante fija mientras mantienes 'para todo epsilon > 0'.",
            "Verifica la coherencia lógica de las proposiciones universales cuantificadas.",
        ]
        return format_diagnostic_error("MATHEMATICAL-INTEGRITY", cid, tpl_id, q_id, "options", "forall eps", cause, actions)

    # Case A0: Unescaped LaTeX math command
    if "Unescaped LaTeX math command" in inv_clean:
        m_cmd = re.search(r"Unescaped LaTeX math command '([^']+)' detected in (.+?)\.", inv_clean)
        snippet = m_cmd.group(1) if m_cmd else "cmd{var}"
        field_name = m_cmd.group(2).rstrip(".") if m_cmd else "text"
        cause = f"Comando matemático LaTeX '{snippet}' sin barra invertida '\\' o sin delimitadores '$...$' detectado en '{field_name}'."
        actions = [
            f"Reemplazar por notación KaTeX válida delimitada por '$' (ej. '$\\{snippet}$').",
            "PROHIBIDO declarar variables matemáticas en el diccionario 'vars' retornado por generate_py.",
            "Asegurar que todas las expresiones matemáticas estén estrictamente delimitadas por '$...$'.",
        ]
        return format_diagnostic_error("R-20: SINTAXIS / LLAVES", cid, tpl_id, q_id, field_name, snippet, cause, actions)

    # Case A: Unsubstituted template variable '{var}'
    m_var = re.search(r"Unsubstituted template variable '\{([^}]+)\}' detected in (.+)", inv_clean)
    if m_var:
        var_name = m_var.group(1)
        field_name = m_var.group(2).rstrip(".")
        snippet = f"{{{var_name}}}"
        is_distractor_context = "option" in field_name.lower() or "rationale" in field_name.lower()
        if is_distractor_context:
            cause = (
                f"Subcadena '{{{var_name}}}' detectada dentro del texto del distractor/opción en '{field_name}'. "
                f"NO corresponde a un parámetro dinámico de generate_py, sino a sintaxis matemática o texto de distractor."
            )
            actions = [
                f"Si '{{{var_name}}}' es parte de notación matemática, delimítela en '$...$' (ej. '$\\dot{{{var_name}}}$' o '$\\bar{{{var_name}}}$') en el template.",
                f"PROHIBIDO declarar '{var_name}' en el diccionario 'vars' retornado por generate_py (provoca aberraciones sintácticas en cascada).",
                f"Quitar las llaves '{{}}' si es texto plano literal no paramétrico.",
            ]
        else:
            cause = f"Llaves '{{{var_name}}}' no declaradas en el diccionario 'vars' generado en generate_py o no sustituidas en el campo '{field_name}'."
            actions = [
                f"Usar '${var_name}$' si se trata de notación matemática en LaTeX.",
                "Quitar las llaves '{}' si es texto plano literal no paramétrico.",
                f"Declarar '{var_name}' en el diccionario 'vars' retornado por generate_py (SOLO si es un parámetro dinámico del stem o hints, NUNCA para distractores).",
            ]
        return format_diagnostic_error("R-20: SINTAXIS / LLAVES", cid, tpl_id, q_id, field_name, snippet, cause, actions)

    # Case B: Triple dollar delimiter '$$$'
    if "$$$" in inv_clean:
        m_ctx = re.search(r"detected in (.+)", inv_clean)
        field_name = m_ctx.group(1).rstrip(".") if m_ctx else "stem / hint / text"
        snippet = "$$$"
        cause = f"Delimitador matemático triple '$$$' inválido detectado en '{field_name}'."
        actions = [
            "Reemplazar '$$$' por '$$' si se trata de un bloque matemático en display mode.",
            "Reemplazar '$$$' por '$' si es matemática inline.",
            "Asegurar que los delimitadores de apertura y cierre coincidan sin signos de dólar redundantes.",
        ]
        return format_diagnostic_error("R-20: SINTAXIS / LLAVES", cid, tpl_id, q_id, field_name, snippet, cause, actions)

    # Case C: Unbalanced display math delimiter '$$'
    if "Unbalanced display math delimiter '$$'" in inv_clean:
        m_ctx = re.search(r"in (.+)", inv_clean)
        field_name = m_ctx.group(1).rstrip(".") if m_ctx else "stem / hint / text"
        snippet = "$$"
        cause = f"Delimitadores '$$' de display math no balanceados en '{field_name}' (número impar de '$$')."
        actions = [
            "Asegurarse de que cada '$$' de apertura tenga un '$$' de cierre.",
            "No mezclar '$$' con '$' en la misma expresión matemática.",
            "Escapar cualquier símbolo de dólar literal como '\\$'.",
        ]
        return format_diagnostic_error("R-20: SINTAXIS / LLAVES", cid, tpl_id, q_id, field_name, snippet, cause, actions)

    # Case D: Unbalanced inline math delimiter '$'
    if "Unbalanced inline math delimiter '$'" in inv_clean:
        m_ctx = re.search(r"in (.+)", inv_clean)
        field_name = m_ctx.group(1).rstrip(".") if m_ctx else "stem / hint / text"
        snippet = "$"
        cause = f"Delimitadores '$' de matemática inline no balanceados en '{field_name}' (número impar de '$')."
        actions = [
            "Verificar que cada '$' de apertura cuente con su correspondiente '$' de cierre.",
            "Escapar cualquier símbolo de dólar literal o de moneda como '\\$'.",
            "Evitar saltos de línea o texto no matemático dentro del bloque '$...$'.",
        ]
        return format_diagnostic_error("R-20: SINTAXIS / LLAVES", cid, tpl_id, q_id, field_name, snippet, cause, actions)

    # Case E: Residual double curly braces '{{' or '}}'
    if "Residual double curly braces" in inv_clean:
        m_ctx = re.search(r"detected in (.+)", inv_clean)
        field_name = m_ctx.group(1).rstrip(".") if m_ctx else "stem / hint / text"
        snippet = "{{ o }}"
        cause = f"Llaves dobles residuales '{{' o '}}' provenientes de formato o f-string de Python en '{field_name}'."
        actions = [
            "Usar llaves simples '{...}' para grupos en LaTeX en lugar de llaves dobles '{{...}}'.",
            "Revisar el escape de llaves en f-strings dentro de generate_py.",
            "Utilizar raw strings r'...' para expresiones KaTeX.",
        ]
        return format_diagnostic_error("R-20: SINTAXIS / LLAVES", cid, tpl_id, q_id, field_name, snippet, cause, actions)

    # Case F: Unbalanced curly braces in LaTeX math expression
    if "Unbalanced curly braces in LaTeX math expression" in inv_clean or ("LaTeX math expression in" in inv_clean and "unbalanced braces" in inv_clean) or "unbalanced braces" in inv_clean.lower():
        m_field = re.search(r"in\s+([^:]+?)(?::|\s+has\s+unbalanced)", inv_clean, re.IGNORECASE)
        raw_field = m_field.group(1).strip() if m_field else "math expression"

        # Check if option error_rationale or content
        m_opt = re.search(r"option\s+(\d+)\s*(error_rationale|content)?", raw_field, re.IGNORECASE)
        field_name = raw_field
        if m_opt:
            opt_num = int(m_opt.group(1))
            opt_idx = opt_num - 1 if opt_num >= 1 else opt_num
            opt_type = m_opt.group(2).lower() if m_opt.group(2) else ("error_rationale" if "rationale" in raw_field.lower() else "content")
            field_name = f"options[{opt_idx}].{opt_type}"
            did_found = None
            if q_obj and isinstance(q_obj, dict):
                opts = q_obj.get("options", [])
                if 0 <= opt_idx < len(opts):
                    did_found = opts[opt_idx].get("distractor_id") or opts[opt_idx].get("id")
            if not did_found:
                m_did = re.search(r"\b(D-[A-Za-z0-9_-]+)\b", inv_clean)
                if m_did:
                    did_found = m_did.group(1)
            if did_found:
                field_name = f"{field_name} (distractor {did_found})"
        elif "stem" in raw_field.lower():
            field_name = "stem"
        elif "solution" in raw_field.lower() or "explanation" in raw_field.lower():
            field_name = "solution"

        # Extract snippet
        m_snip = re.search(r"['\"]([^'\"]*)['\"]", inv_clean)
        if not m_snip:
            m_snip = re.search(r":\s*(\$?[^$]+\$?.*)", inv_clean)
        snippet = m_snip.group(1).strip() if m_snip else "{ o }"

        # Analyze balance and patterns
        open_c = snippet.count("{")
        close_c = snippet.count("}")
        pattern_notes = []
        if "_}{" in snippet or "^}{" in snippet:
            pattern_notes.append("patrón invertido '_}{' o '^}{'")
        if open_c != close_c:
            pattern_notes.append(f"open={open_c} vs close={close_c}")

        pattern_str = f" ({', '.join(pattern_notes)})" if pattern_notes else ""
        cause = f"Llaves '{{' y '}}' desbalanceadas{pattern_str} dentro de la fórmula LaTeX en '{field_name}': '{snippet}'."

        action_detail = (
            f"Faltan {open_c - close_c} llave(s) de cierre '}}'." if open_c > close_c else
            f"Sobran {close_c - open_c} llave(s) de cierre '}}'." if close_c > open_c else
            "Revisar el orden de apertura y cierre de llaves '{' y '}'."
        )
        actions = [
            f"Balancear las llaves en '{field_name}' ({action_detail}).",
            "Verificar que subíndices y superíndices sigan la sintaxis KaTeX '_{sub}' o '^{sup}' y no '_}{' o '^}{'.",
            "Si se usaron llaves literales escapadas '\\{', asegurar que la barra invertida esté presente.",
            "Revisar macros de LaTeX con múltiples argumentos como \\frac{a}{b} donde falte una llave de cierre.",
        ]
        return format_diagnostic_error("R-20: SINTAXIS / LLAVES", cid, tpl_id, q_id, field_name, snippet, cause, actions)

    # Case F2: Unclosed nested LaTeX macro or accent
    if "Unclosed nested macro brace detected" in inv_clean or "nested macro" in inv_clean:
        m_ctx = re.search(r"in ([^:]+):", inv_clean)
        field_name = m_ctx.group(1).strip() if m_ctx else "math expression"
        return format_diagnostic_error(
            "R-20: SINTAXIS / LLAVES", cid, tpl_id, q_id, field_name, inv_clean,
            f"Acento o macro anidado de LaTeX sin cerrar correctamente en '{field_name}'.",
            [
                "Asegurar que macros anidados como \\hat{\\boldsymbol{\\beta}} tengan ambas llaves de cierre '}}'.",
                "Revisar expresiones matemáticas con acentos combinados con estilos vectoriales o matriciales.",
                "Balancear todas las llaves en la fórmula.",
            ],
        )

    # Case F3: Macro arity / unclosed argument
    if "requires 2 arguments" in inv_clean or "unclosed first argument" in inv_clean or "unclosed second argument" in inv_clean or "missing argument brackets" in inv_clean:
        m_ctx = re.search(r"in ([^.]+)", inv_clean)
        field_name = m_ctx.group(1).strip() if m_ctx else "math expression"
        return format_diagnostic_error(
            "R-20: SINTAXIS / LLAVES", cid, tpl_id, q_id, field_name, inv_clean,
            f"Macro de LaTeX (como \\frac, \\binom, \\overset) con aridad incorrecta o argumento incompleto en '{field_name}'.",
            [
                "Comprobar que \\frac posea tanto numerador como denominador: \\frac{num}{den}.",
                "Cerrar adecuadamente cada bloque de llaves '{...}'.",
                "Evitar macros con argumentos incompletos antes del cierre del delimitador '$'.",
            ],
        )

    # Case F4: Unclosed or mismatched LaTeX environment
    if "LaTeX environment" in inv_clean:
        m_ctx = re.search(r"in ([^.]+)", inv_clean)
        field_name = m_ctx.group(1).strip() if m_ctx else "math expression"
        return format_diagnostic_error(
            "R-20: SINTAXIS / LLAVES", cid, tpl_id, q_id, field_name, inv_clean,
            f"Entorno LaTeX sin cerrar o con cierre discordante en '{field_name}'.",
            [
                "Asegurar que cada \\begin{env} tenga su correspondiente \\end{env}.",
                "Verificar entornos matriciales o de casos como pmatrix, bmatrix, cases, aligned.",
                "Comprobar que no haya errores tipográficos en el nombre del entorno.",
            ],
        )

    # Case F5: Unclosed or unmatched scalable delimiter
    if "scalable delimiter" in inv_clean:
        m_ctx = re.search(r"in ([^.]+)", inv_clean)
        field_name = m_ctx.group(1).strip() if m_ctx else "math expression"
        return format_diagnostic_error(
            "R-20: SINTAXIS / LLAVES", cid, tpl_id, q_id, field_name, inv_clean,
            f"Delimitador escalable \\left o \\right sin emparejar en '{field_name}'.",
            [
                "Emparejar cada \\left( con \\right), \\left[ con \\right], \\left\\{ con \\right\\}.",
                "Si se requiere un delimitador invisible, usar \\left. o \\right..",
                "Verificar la simetría de paréntesis y corchetes en las fórmulas matemáticas.",
            ],
        )

    # Case G: Distractor identical to correct answer (TPL-D4)
    if "Distractor identical to correct answer" in inv_clean:
        m_d = re.search(r"Distractor identical to correct answer:\s*'(.*)'", inv_clean)
        snippet = m_d.group(1) if m_d else inv_clean
        cause = f"TPL-D4 violation in '{tpl_id}': distractor matches correct answer '{snippet}' (invariant violation). Un distractor generado en generate_py es idéntico a la respuesta correcta."
        actions = [
            "Verificar en generate_py que los distractores nunca tomen el valor de la clave correcta.",
            "Añadir una guarda en generate_py que desplace o regenere el distractor si colisiona con 'correct'.",
            "Comprobar casos particulares donde parámetros aleatorios anulen la diferencia.",
        ]
        return format_diagnostic_error("TPL-D4: TPL-D4 violation: DISTRACTOR IDÉNTICO A RESPUESTA CORRECTA", cid, tpl_id, q_id, "options", snippet, cause, actions)

    # Case H: Length anti-giveaway violation (R-15 / R-15-MS)
    if "Length anti-giveaway violation" in inv_clean:
        cause = f"La longitud de la respuesta correcta difiere significativamente del rango de los distractores (fuera de 0.80x - 1.20x): {inv_clean}"
        actions = [
            f"Detalles observados: {inv_clean}",
            "Calibrar la longitud de la respuesta correcta o de los distractores para que tengan una extensión homogénea.",
            "Homogeneizar el nivel de detalle y formato matemático entre todas las opciones.",
            "Asegurar que 0.80 * min(len(D)) <= len(correct) <= 1.20 * max(len(D)).",
        ]
        return format_diagnostic_error("R-15: EQUILIBRIO DE LONGITUD", cid, tpl_id, q_id, "options", inv_clean, cause, actions)

    if "MS length anti-giveaway violation" in inv_clean:
        cause = f"La longitud promedio de las opciones verdaderas difiere de las falsas en multiple_select (fuera de 0.85x - 1.15x): {inv_clean}"
        actions = [
            f"Detalles observados: {inv_clean}",
            "Equilibrar la extensión y nivel de detalle entre las afirmaciones verdaderas y falsas del ítem multiple_select.",
            "Asegurar que 0.85 <= avg(len(true)) / avg(len(false)) <= 1.15.",
        ]
        return format_diagnostic_error("R-15-MS: EQUILIBRIO DE LONGITUD MS", cid, tpl_id, q_id, "options", inv_clean, cause, actions)

    if "open_symbolic variable collision" in inv_clean or "Phantom numeric leak in open_symbolic" in inv_clean:
        cause = f"Fuga de valores numéricos fantasma en ítem open_symbolic: {inv_clean}"
        actions = [
            "Las variables declaradas en symbolic_config.variables (ej. 's', 'n') son simbólicas libres y NUNCA deben incluirse con valores numéricos en 'vars'.",
            "No reutilices RATS con placeholders numéricos (@s@, @n@) en plantillas open_symbolic; escribe los símbolos literales (ej. $s$, $n$) en el error_rationale.",
            "Verifica que ningún decimal ausente del enunciado aparezca en diagnostic_distractors[*].error_rationale.",
        ]
        return format_diagnostic_error("OPEN-SYM-DISJOINT: FUGA NUMÉRICA EN SIMBÓLICO", cid, tpl_id, q_id, "diagnostic_distractors", inv_clean, cause, actions)

    # Case I: Answer leak (R-19)
    if "leaked verbatim in" in inv_clean:
        cause = "El valor o texto de la respuesta correcta aparece textualmente en el stem o en la primera pista, revelando la clave."
        actions = [
            "Remover la mención textual de la respuesta del enunciado de la pregunta o de la primera pista.",
            "Reformular la primera pista para que oriente sobre el método conceptual sin dar el resultado numérico/algebraico.",
            "Verificar que la consigna plantee el problema requiriendo el cálculo en lugar de enunciar la solución.",
        ]
        return format_diagnostic_error("R-19: FUGA DE RESPUESTA", cid, tpl_id, q_id, "stem / hints[0]", inv_clean, cause, actions)

    # Case J: Missing error_rationale
    if "must possess a non-empty 'error_rationale'" in inv_clean:
        is_ms = "MS option" in inv_clean
        rule_tag = "R-22: RATIONALE EN MULTIPLE_SELECT" if is_ms else "R-17: RATIONALE FALTANTE EN DISTRACTOR"
        m_opt = re.search(r"option\s+(\d+)", inv_clean, re.IGNORECASE)
        opt_idx = m_opt.group(1) if m_opt else "X"
        field_name = f"options[{opt_idx}].error_rationale"
        cause = f"La opción distractora {opt_idx} con is_correct=False carece de un 'error_rationale' explicativo."
        actions = [
            "Agregar una explicación diagnóstica en 'error_rationale' para cada opción con is_correct=False.",
            "Describir la falacia conceptual o error procedimental que lleva a seleccionar dicha opción.",
            "Asegurar que el texto de rationale no sea una cadena vacía ni un placeholder genérico.",
        ]
        return format_diagnostic_error(rule_tag, cid, tpl_id, q_id, field_name, "(vacío o ausente)", cause, actions)

    # Case K: Duplicate options
    if "Duplicate option content detected" in inv_clean:
        m_opt = re.search(r"detected(?:\s+in\s+MS)?:\s*'(.*)'", inv_clean)
        snippet = m_opt.group(1) if m_opt else inv_clean
        cause = f"Dos o más opciones tienen contenido idéntico ('{snippet}')."
        actions = [
            "Garantizar que todos los distractores generados en generate_py sean disjuntos y únicos.",
            "Agregar una comprobación en generate_py que descarte o regenere opciones repetidas.",
            "Variar las fórmulas de perturbación para producir valores distintos.",
        ]
        return format_diagnostic_error("TPL-D4: OPCIONES DUPLICADAS", cid, tpl_id, q_id, "options", snippet, cause, actions)

    # Case L: Synthetic boilerplate distractor pattern
    if "Synthetic boilerplate distractor" in inv_clean:
        m_s = re.search(r"pattern detected:\s*(.*)", inv_clean)
        snippet = m_s.group(1) if m_s else inv_clean
        cause = "Opciones distractoras generadas mediante plantilla sintética repetitiva o inversión simétrica trivial ('converge' vs 'diverge')."
        actions = [
            "Reemplazar distractores boilerplate por modelos de error y confusiones conceptuales reales.",
            "Diversificar la redacción y argumentos analíticos de cada opción distractora.",
            "Evitar variaciones triviales donde solo se cambie un término opuesto o un parámetro numérico.",
        ]
        return format_diagnostic_error("R-18: DISTRACTORES BOILERPLATE SINTÉTICOS", cid, tpl_id, q_id, "options", snippet, cause, actions)

    # Case M: Scaffolding answer leak in hints
    if "Scaffolding answer leak" in inv_clean:
        m_s = re.search(r"hint\s+\d+:\s*(.*)", inv_clean)
        snippet = m_s.group(1) if m_s else inv_clean
        cause = "La pista (scaffolding) proporciona una regla mecánica de descarte que delata directamente la respuesta correcta."
        actions = [
            "Reescribir la pista para proporcionar guía pedagógica sin dar instrucciones explícitas de descarte mecánico.",
            "Fomentar la deducción del estudiante a partir de ecuaciones y principios teóricos.",
            "Eliminar frases como 'Descarte las respuestas...' o 'Elimine opciones...' del texto de hints.",
        ]
        return format_diagnostic_error("R-19: FUGA DE RESPUESTA EN ANDAMIAJE", cid, tpl_id, q_id, "hints", snippet, cause, actions)

    # Case A-pre7: Raw SymPy syntax leaked in KaTeX ([TPL-KATEX-SYMPY-LEAK])
    if "[TPL-KATEX-SYMPY-LEAK]" in inv_clean:
        cause = f"Sintaxis cruda de Python/SymPy ('**', '*' o 'sqrt(') filtrada dentro de KaTeX: {inv_clean}"
        actions = [
            "Formatea potencias y expresiones simbólicas en LaTeX con '^{...}' o sympy.latex(...) dentro de vars['ans'] y texto KaTeX.",
            "Reserva el operador '**' de Python exclusivamente para los campos simbólicos de evaluación ('correct', 'accepted_equivalents').",
        ]
        return format_diagnostic_error("TPL-KATEX-SYMPY-LEAK: SINTAXIS SYMPY EN KATEX", cid, tpl_id, q_id, "text", inv_clean, cause, actions)

    # Case A-pre8: Tautological self-identity ($X = X$) ([TPL-TAUTOLOGICAL-IDENTITY])
    if "[TPL-TAUTOLOGICAL-IDENTITY]" in inv_clean:
        cause = f"Identidad tautológica redundante ($X = X$) detectada en solución o pista: {inv_clean}"
        actions = [
            "Evita repetir la misma expresión simbólica o numérica idéntica a ambos lados de '=' en 'sol' o 'hints'.",
            "Muestra el paso algebraico intermedio o la sustitución efectiva en lugar de una igualdad trivial.",
        ]
        return format_diagnostic_error("TPL-TAUTOLOGICAL-IDENTITY: IDENTIDAD TAUTOLÓGICA", cid, tpl_id, q_id, "solution / hints", inv_clean, cause, actions)

    # Fallback Invariant
    return format_diagnostic_error(
        rule_tag="INVARIANT: invariant violation",
        competency=cid,
        template=tpl_id,
        item_id=q_id,
        field_name="instance",
        snippet=inv_clean,
        cause=f"Template '{tpl_id}' invariant violation ({q_id}): {inv_clean}",
        actions=[
            "Revisar la salida de generate_py para cumplir con los requerimientos estructurales del reactivo.",
            "Asegurar que todos los campos requeridos estén presentes y sean del tipo esperado.",
            "Verificar que el reactivo cumpla con la especificación de interaction_type.",
        ],
    )


def format_parity_error(
    cid: str,
    err: Any,
    questions_by_id: Dict[str, Dict[str, Any]],
    item_ids: Optional[Union[str, List[str]]] = None,
) -> str:
    """Formats a ValidationError from production parity check with prescriptive diagnosis."""
    rule_id = getattr(err, "rule_id", "PARITY")
    msg = getattr(err, "message", str(err))
    if item_ids is not None:
        item_id = item_ids
        rep_id = item_ids[0] if isinstance(item_ids, list) and item_ids else (item_ids if isinstance(item_ids, str) else "UNKNOWN")
    else:
        item_id = getattr(err, "item_id", None) or "UNKNOWN"
        rep_id = item_id

    q = questions_by_id.get(rep_id, {})
    tpl_id = q.get("template_id") or "UNKNOWN"

    # Rule R-20
    if rule_id == "R-20":
        m_field = re.search(r"in\s+([a-zA-Z0-9_.\[\]]+):", msg)
        field_name = m_field.group(1) if m_field else "stem / options / text"

        if "Unreplaced template variable" in msg:
            m_s = re.search(r"Unreplaced template variable\(s\) found:\s*(.*)", msg)
            snippet = m_s.group(1) if m_s else "{var}"
            is_distractor_context = "option" in field_name.lower() or "rationale" in field_name.lower()
            clean_var = snippet.replace('{','').replace('}','')
            if is_distractor_context:
                cause = (
                    f"Subcadena '{snippet}' detectada dentro del texto del distractor/opción en '{field_name}'. "
                    f"NO corresponde a un parámetro dinámico de generate_py."
                )
                actions = [
                    f"Si '{snippet}' es notación matemática, delimítela en '$...$' (ej. '$\\dot{{{clean_var}}}$' o '$\\bar{{{clean_var}}}$') en el template.",
                    f"PROHIBIDO declarar '{clean_var}' en el diccionario 'vars' retornado por generate_py (provoca aberraciones sintácticas en cascada).",
                    "Quitar las llaves '{}' si es texto plano literal no paramétrico.",
                ]
            else:
                cause = f"Llaves '{snippet}' no declaradas en el diccionario 'vars' retornado por generate_py o no reemplazadas en '{field_name}'."
                actions = [
                    f"Usar '${clean_var}$' si se trata de notación matemática en LaTeX.",
                    "Quitar las llaves '{}' si es texto plano literal no paramétrico.",
                    f"Agregar la clave sin llaves al diccionario 'vars' retornado por generate_py (SOLO si es parámetro dinámico del stem/hints, NUNCA para distractores).",
                ]
            return format_diagnostic_error("R-20: SINTAXIS / LLAVES", cid, tpl_id, item_id, field_name, snippet, cause, actions)

        if "Unbalanced display math delimiters '$$'" in msg:
            return format_diagnostic_error(
                "R-20: SINTAXIS / LLAVES", cid, tpl_id, item_id, field_name, "$$",
                f"Delimitadores '$$' de display math no balanceados en '{field_name}' (número impar de '$$').",
                [
                    "Asegurarse de que cada '$$' de apertura tenga un '$$' de cierre.",
                    "No mezclar '$$' con '$' en la misma expresión.",
                    "Escapar cualquier símbolo de dólar literal como '\\$'.",
                ]
            )

        if "Unbalanced inline math delimiters '$'" in msg:
            return format_diagnostic_error(
                "R-20: SINTAXIS / LLAVES", cid, tpl_id, item_id, field_name, "$",
                f"Delimitadores '$' de matemática en línea no balanceados en '{field_name}' (número impar de '$').",
                [
                    "Verificar que cada '$' de apertura cuente con su correspondiente '$' de cierre.",
                    "Escapar cualquier símbolo de dólar literal como '\\$'.",
                    "Comprobar que no haya saltos de línea dentro del bloque '$...$'.",
                ]
            )

        if "Forbidden triple math delimiter '$$$'" in msg:
            return format_diagnostic_error(
                "R-20: SINTAXIS / LLAVES", cid, tpl_id, item_id, field_name, "$$$",
                f"Delimitador matemático triple '$$$' inválido detectado en '{field_name}'.",
                [
                    "Reemplazar '$$$' por '$$' si es bloque matemático en display mode.",
                    "Reemplazar '$$$' por '$' si es matemática inline.",
                    "Asegurar que los delimitadores de apertura y cierre coincidan.",
                ]
            )

        if "Residual double braces" in msg:
            return format_diagnostic_error(
                "R-20: SINTAXIS / LLAVES", cid, tpl_id, item_id, field_name, "{{ o }}",
                f"Llaves dobles residuales '{{' o '}}' provenientes de f-strings en Python dentro de '{field_name}'.",
                [
                    "Usar llaves simples '{...}' para grupos en LaTeX en lugar de llaves dobles '{{...}}'.",
                    "Revisar el escape de llaves en f-strings dentro de generate_py.",
                    "Utilizar raw strings r'...' para expresiones KaTeX.",
                ]
            )

        if "Unbalanced curly braces in LaTeX math block" in msg:
            m_s = re.search(r"LaTeX math block:\s*'(.*)'", msg)
            snippet = m_s.group(1) if m_s else "{ o }"
            return format_diagnostic_error(
                "R-20: SINTAXIS / LLAVES", cid, tpl_id, item_id, field_name, snippet,
                f"Llaves curvas '{{' y '}}' desbalanceadas dentro de la fórmula LaTeX en '{field_name}': '{snippet}'.",
                [
                    "Contar y balancear las llaves '{' y '}' en la expresión LaTeX.",
                    "Asegurar que llaves literales estén escapadas como '\\{'.",
                    "Revisar macros de LaTeX como \\frac{a}{b} donde falte una llave de cierre.",
                ]
            )

        if "Leaked raw code variable identifier" in msg:
            m_s = re.search(r"identifier\(s\) found:\s*(.*)", msg)
            snippet = m_s.group(1) if m_s else "identificador de código"
            return format_diagnostic_error(
                "R-20: SINTAXIS / LLAVES", cid, tpl_id, item_id, field_name, snippet,
                f"Identificador interno de código filtrado al texto del reactivo ({snippet}).",
                [
                    "Eliminar o formatear las variables internas de código antes de insertarlas en el texto.",
                    "Reemplazar identificadores crudos (_val, _num, _str) por su valor formateado o símbolo matemático.",
                    "Verificar que el texto dirigido al estudiante sea completamente natural y pedagógico.",
                ]
            )

        return format_diagnostic_error(
            "R-20: SINTAXIS / LLAVES", cid, tpl_id, item_id, field_name, msg,
            f"Error de sintaxis KaTeX o delimitadores en '{field_name}'.",
            [
                "Revisar la sintaxis de KaTeX y los delimitadores '$' y '$$'.",
                "Asegurar que todas las llaves '{' y '}' estén balanceadas.",
                "Verificar que no queden placeholders sin sustituir.",
            ]
        )

    # Rule R-18
    if rule_id == "R-18":
        if "boilerplate" in msg.lower() or "antonym" in msg.lower() or "synthetic" in msg.lower():
            m_q = re.search(r"Question '([^']+)'", msg)
            field_name = "options"
            snippet = msg
            cause = f"Patrón sintético / boilerplate o pares antónimos detectados en opciones de '{m_q.group(1) if m_q else item_id}': {msg}"
            actions = [
                "Variar la formulación y estructura de cada distractor basándose en errores conceptuales reales del estudiante en lugar de invertir palabras clave o usar plantillas repetitivas.",
                "Evitar pares simétricos mecánicos (ej. 'estable' vs 'inestable') sin explicación física/matemática diferenciada.",
                "Asegurar que cada opción distractora corresponda a un misconception específico de cta.json.",
            ]
            return format_diagnostic_error("R-18: BOILERPLATE / PATRÓN SINTÉTICO", cid, tpl_id, item_id, field_name, snippet, cause, actions)
        m_field = re.search(r"Option '([^']+)'", msg)
        opt_id = m_field.group(1) if m_field else "option"
        field_name = f"options[{opt_id}].content"
        m_s = re.search(r"visible content:\s*'(.*)'", msg)
        snippet = m_s.group(1) if m_s else msg
        cause = "Uso de términos metalingüísticos o autocríticos ('confundiendo', 'asumiendo erróneamente', etc.) en el texto visible de la opción que revelan al estudiante que es un distractor."
        actions = [
            "Reescribir el contenido de la opción como una afirmación objetiva o resultado alternativo plausible sin juzgar su veracidad en el texto visible.",
            "Mover la justificación del error ('confundiendo...', 'asumiendo erróneamente...') exclusivamente al campo 'error_rationale'.",
            "Asegurar que todas las opciones mantengan una apariencia neutra y verosímil sin dar pistas psicométricas.",
        ]
        return format_diagnostic_error("R-18: META-INFORMACIÓN / GIVEAWAY", cid, tpl_id, item_id, field_name, snippet, cause, actions)

    # Rule R-19
    if rule_id == "R-19":
        field_name = "stem"
        m_s = re.search(r"answer '([^']+)' leaked", msg)
        snippet = m_s.group(1) if m_s else msg
        cause = "El valor o clave de la respuesta correcta aparece textualmente dentro del stem del reactivo (fuga de respuesta), o hay sustitución que corrompió un operador (ej. \\dot<número>)."
        actions = [
            "Remover el valor o expresión de respuesta del enunciado (stem) reemplazándolo por una consigna neutra o línea de completación.",
            "Asegurar que las variables de LaTeX no sustituyan números directamente dentro de macros sin llaves.",
            "Verificar que la consigna plantee el problema requiriendo el cálculo en lugar de mostrar la solución.",
        ]
        return format_diagnostic_error("R-19: FUGA DE RESPUESTA / SINTAXIS", cid, tpl_id, item_id, field_name, snippet, cause, actions)

    # Rule R-22
    if rule_id == "R-22":
        m_field = re.search(r"Option '([^']+)'", msg)
        opt_id = m_field.group(1) if m_field else "option"
        field_name = f"options[{opt_id}].error_rationale"
        cause = "Opción incorrecta (is_correct=False) en ítem de selección múltiple (multiple_select) carece de 'error_rationale' diagnóstico formativo."
        actions = [
            "Agregar una explicación diagnóstica en 'error_rationale' para cada opción con is_correct=False.",
            "Explicar la falacia conceptual o el cálculo incorrecto que conduce a seleccionar dicha opción.",
            "Asegurarse de que el texto de rationale no esté vacío ni sea un placeholder genérico.",
        ]
        return format_diagnostic_error("R-22: RATIONALE EN MULTIPLE_SELECT", cid, tpl_id, item_id, field_name, "(vacío o ausente)", cause, actions)

    # Rule R-17
    if rule_id == "R-17":
        m_field = re.search(r"Option '([^']+)'", msg)
        opt_id = m_field.group(1) if m_field else "option"
        field_name = f"options[{opt_id}].error_rationale"
        m_s = re.search(r"error_rationale':\s*'(.*)'", msg)
        snippet = m_s.group(1) if m_s else "(vacío o placeholder)"
        cause = "El campo 'error_rationale' contiene un placeholder genérico prohibido (ej. 'placeholder', 'distractor', 'error') o está vacío."
        actions = [
            "Redactar una explicación pedagógica formativa sobre el error que comete el estudiante al elegir la opción.",
            "Eliminar palabras prohibidas como 'placeholder', 'distractor', 'error', 'n/a' o 'ninguno'.",
            "Describir la confusión conceptual o error algebraico/aritmético subyacente.",
        ]
        return format_diagnostic_error("R-17: RATIONALE GENÉRICO / PLACEHOLDER", cid, tpl_id, item_id, field_name, snippet, cause, actions)

    # Rule R-15: Option Length Parity (Per-Item)
    if rule_id == "R-15":
        correct_opt = next((opt for opt in q.get("options", []) if opt.get("is_correct")), None)
        distractor_opts = [opt for opt in q.get("options", []) if not opt.get("is_correct")]
        L_c = len(str(correct_opt.get("content", "")).strip()) if correct_opt else 0
        dist_lens = [len(str(d.get("content", "")).strip()) for d in distractor_opts]
        max_d = max(dist_lens) if dist_lens else 1
        min_d = min(dist_lens) if dist_lens else 1
        details_str = f"len(correct)={L_c} vs [min(D)={min_d}, max(D)={max_d}]. Longitudes distractores: {dist_lens}"
        cause = f"Disparidad de longitud en opciones: {details_str}."
        actions = [
            "Calibrar la longitud de la respuesta correcta o de los distractores para que tengan una extensión homogénea.",
            "Homogeneizar el nivel de detalle y formato matemático entre todas las opciones.",
            "Asegurar que 0.80 * min(len(D)) <= len(correct) <= 1.20 * max(len(D)).",
        ]
        return format_diagnostic_error("R-15: EQUILIBRIO DE LONGITUD", cid, tpl_id, item_id, "options", details_str, cause, actions)

    # Rule R-16: Option Length Distribution (Course-Level)
    if rule_id == "R-16":
        cause = f"Sesgo de longitud a nivel de competencia: {msg}."
        actions = [
            "Calibrar las plantillas de modo que la respuesta correcta no sea sistemáticamente la opción más larga ni la más corta.",
            "Asegurar que algunos distractores sean más largos y otros más cortos que la respuesta correcta en cada plantilla.",
            "Mantener la tasa de respuestas más largas/cortas por debajo del umbral del 25%.",
        ]
        return format_diagnostic_error("R-16: SESGO DE LONGITUD DE CLAVE", cid, tpl_id, "ALL", "options", msg, cause, actions)

    # Rule S-01
    if rule_id == "S-01":
        return format_diagnostic_error(
            "S-01: SOLUCIÓN PASO A PASO OBLIGATORIA", cid, tpl_id, item_id, "solution / detailed_solution",
            "(vacío o ausente)",
            "El reactivo carece de una solución explicativa paso a paso requerida en modo strict.",
            [
                "Agregar el campo 'detailed_solution' o 'solution' en la plantilla con la resolución paso a paso.",
                "Describir el procedimiento matemático o conceptual completo para llegar a la respuesta correcta.",
                "Asegurar que la solución esté redactada con KaTeX válido.",
            ]
        )

    # Rule S-02
    if rule_id == "S-02":
        return format_diagnostic_error(
            "S-02: MISCONCEPTION WARNING OBLIGATORIO", cid, tpl_id, item_id, "misconception_warning",
            "(vacío o ausente)",
            "El reactivo carece de una advertencia de error común ('misconception_warning') requerida en modo strict.",
            [
                "Agregar el campo 'misconception_warning' o 'common_misconception_warning' en la plantilla.",
                "O asociar distractor_ids que tengan 'remediation_hint' definido en cta.json.",
                "Explicar brevemente el error más común que deben evitar los estudiantes.",
            ]
        )

    # Rule S-03
    if rule_id == "S-03":
        return format_diagnostic_error(
            "S-03: DIFICULTAD EXPLÍCITA", cid, tpl_id, item_id, "difficulty",
            "(inválido o ausente)",
            "El reactivo no especifica un nivel de dificultad válido ('easy', 'medium', 'hard') en modo strict.",
            [
                "Declarar 'difficulty': 'easy', 'medium' o 'hard' en la plantilla.",
                "Alinear la dificultad con el nivel de Bloom y la complejidad del problema.",
                "No dejar el campo vacío ni con valores no reconocidos.",
            ]
        )

    # Generic Fallback
    action_fallback = "Revisa la regla y ajusta el generador o las variantes."
    return format_diagnostic_error(
        f"{rule_id}: CONTRATO DE VALIDACIÓN", cid, tpl_id, item_id, "question",
        msg,
        f"Violación de la regla {rule_id}: {msg}",
        [
            action_fallback,
            "Verificar la estructura y tipos de datos de los reactivos producidos.",
            "Corregir directamente en el script generador o archivo de plantillas.",
        ]
    )

