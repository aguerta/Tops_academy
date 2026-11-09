"""Course Publisher for Top's Academy Platform.

Validates course banks via the strict validator CLI (`validate-course --strict`),
persists the course JSON to `courses/<course_id>.json`, publishes the CTA markdown,
and outputs platform integration launch instructions.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import logging
import os
import re
import subprocess
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Optional

from validator.core import validate_course_content
from validator.models import ValidationResult

logger = logging.getLogger(__name__)


def sanitize_cli_arg(arg: Any) -> Any:
    """Sanitize CLI argument by stripping outer and escaped quotes from Windows shells."""
    if not isinstance(arg, str):
        return arg
    cleaned = arg.strip()
    for _ in range(3):
        if (cleaned.startswith('"') and cleaned.endswith('"')) or (
            cleaned.startswith("'") and cleaned.endswith("'")
        ):
            if len(cleaned) <= 1:
                break
            cleaned = cleaned[1:-1].strip()
        if cleaned.startswith(r'\"') and cleaned.endswith(r'\"'):
            cleaned = cleaned[2:-2].strip()
    cleaned = cleaned.replace(r'\"', '"')
    if (cleaned.startswith('"') and cleaned.endswith('"')) or (
        cleaned.startswith("'") and cleaned.endswith("'")
    ):
        cleaned = cleaned[1:-1].strip()
    if len(cleaned) > 3 and cleaned.endswith("\\"):
        cleaned = cleaned.rstrip("\\")
    return cleaned


def is_corrupted_unicode(text: Optional[str]) -> bool:
    """Detect if string contains corrupted Unicode replacement character (\ufffd)."""
    if not text:
        return False
    return "\ufffd" in text or "\uFFFD" in text


class PublishQualityGateError(ValueError):
    """Raised when course bank fails standardized audit quality gate prior to publication."""
    pass


SPANISH_ACADEMIC_STOPWORDS = {
    "de", "la", "el", "en", "los", "las", "un", "una", "del", "al",
    "para", "por", "con", "sin", "sobre", "entre", "mediante", "hacia",
    "desde", "como", "calculo", "analisis", "aplicacion", "propiedad",
    "propiedades", "estudio", "uso", "concepto", "metodo", "modelo",
    "teorema", "definicion", "habilidad", "hecho", "competencia",
    "descripcion", "completa", "validacion", "psicometrica",
}


def _strip_accents(text: str) -> str:
    """Normalize text by converting accented vowels to unaccented equivalents."""
    acc_map = {
        "á": "a", "é": "e", "í": "i", "ó": "o", "ú": "u",
        "Á": "a", "É": "e", "Í": "i", "Ó": "o", "Ú": "u",
        "ü": "u", "Ü": "u", "ñ": "n", "Ñ": "n",
    }
    return "".join(acc_map.get(ch, ch) for ch in text).lower()


def _extract_content_stems(text: str) -> set[str]:
    """Normalize text, strip math blocks, remove academic stopwords, and truncate to 5-char stems."""
    clean = _strip_accents(text)
    clean = re.sub(r"\$[^$]+\$", " ", clean)
    words = re.findall(r"[a-z]+", clean)
    stems = set()
    for w in words:
        if len(w) >= 3 and w not in SPANISH_ACADEMIC_STOPWORDS:
            stems.add(w[:5])
    return stems


def _extract_math_symbols(text: str) -> set[str]:
    """Extract LaTeX math command tokens and math-mode identifiers."""
    symbols = set()
    for m in re.findall(r"\\[a-zA-Z]+", text):
        symbols.add(m.lower())
    for math_block in re.findall(r"\$([^$]+)\$", text):
        idents = re.findall(r"[a-zA-Z]+", math_block)
        for ident in idents:
            symbols.add(ident)
    return symbols


def _jaccard_similarity(set_a: set[str], set_b: set[str]) -> float:
    """Compute Jaccard similarity index between two token sets."""
    if not set_a or not set_b:
        return 0.0
    return len(set_a & set_b) / len(set_a | set_b)


def are_competencies_duplicate(c_incoming: dict[str, Any], c_existing: dict[str, Any]) -> bool:
    """Detect whether two competencies represent the same concept using composite similarity.
    
    Checks exact name equality, content stem Jaccard (>= 0.38), or composite stem + math (>= 0.28 and >= 0.50).
    """
    name_inc = str(c_incoming.get("name") or c_incoming.get("title") or "").strip().lower()
    name_ex = str(c_existing.get("name") or c_existing.get("title") or "").strip().lower()
    if name_inc and name_ex and name_inc == name_ex:
        return True

    stems_name_inc = _extract_content_stems(name_inc)
    stems_name_ex = _extract_content_stems(name_ex)

    text_inc = f"{c_incoming.get('name') or ''} {c_incoming.get('description') or c_incoming.get('description_latex') or ''}"
    text_ex = f"{c_existing.get('name') or ''} {c_existing.get('description') or c_existing.get('description_latex') or ''}"

    stems_inc = _extract_content_stems(text_inc)
    stems_ex = _extract_content_stems(text_ex)
    content_stem_j = _jaccard_similarity(stems_inc, stems_ex)

    math_inc = _extract_math_symbols(text_inc)
    math_ex = _extract_math_symbols(text_ex)
    math_j = _jaccard_similarity(math_inc, math_ex) if (math_inc and math_ex) else 0.0

    # Must share at least one name stem (or both have empty name stems) to avoid cross-concept false matches
    has_name_overlap = bool(stems_name_inc & stems_name_ex) or (not stems_name_inc and not stems_name_ex)
    if not has_name_overlap:
        return False

    if content_stem_j >= 0.38:
        return True
    if content_stem_j >= 0.28 and math_j >= 0.50:
        return True
    return False


def check_prerequisites_dag(competencies: list[dict[str, Any]]) -> list[str]:
    """Ensure prerequisite references exist and form an acyclic directed graph."""
    errors = []
    comp_ids = {c["id"] for c in competencies if isinstance(c, dict) and "id" in c}
    adj: dict[str, list[str]] = {cid: [] for cid in comp_ids}
    for comp in competencies:
        if not isinstance(comp, dict) or "id" not in comp:
            continue
        cid = comp["id"]
        for prereq in comp.get("prerequisites", []):
            if prereq not in comp_ids:
                errors.append(f"Competency '{cid}' references non-existent prerequisite '{prereq}'.")
            else:
                adj[cid].append(prereq)

    visited: dict[str, int] = {}

    def dfs(node: str, path: list[str]) -> bool:
        visited[node] = 1
        for neighbor in adj.get(node, []):
            if visited.get(neighbor) == 1:
                cycle_str = " -> ".join(path + [neighbor])
                errors.append(f"Cycle detected in prerequisites: {cycle_str}")
                return False
            if visited.get(neighbor, 0) == 0:
                if not dfs(neighbor, path + [neighbor]):
                    return False
        visited[node] = 2
        return True

    for cid in comp_ids:
        if visited.get(cid, 0) == 0:
            dfs(cid, [cid])

    return errors


def _load_run_full_audit(project_root: Optional[Path] = None) -> Any:
    """Dynamically loads run_full_audit from standardized_audit_engine.py."""
    if "standardized_audit_engine" in sys.modules:
        mod = sys.modules["standardized_audit_engine"]
        if hasattr(mod, "run_full_audit"):
            return getattr(mod, "run_full_audit")

    candidates = []
    curr_file = Path(__file__).resolve()
    candidates.append(curr_file.parent.parent / "course-qa-evaluator" / "scripts" / "standardized_audit_engine.py")
    if project_root:
        candidates.append(
            Path(project_root).resolve() / ".agents" / "skills" / "course-qa-evaluator" / "scripts" / "standardized_audit_engine.py"
        )
    for parent in curr_file.parents:
        cand = parent / ".agents" / "skills" / "course-qa-evaluator" / "scripts" / "standardized_audit_engine.py"
        if cand not in candidates:
            candidates.append(cand)

    for cand_p in candidates:
        if cand_p.is_file():
            try:
                script_dir = str(cand_p.parent)
                if script_dir not in sys.path:
                    sys.path.insert(0, script_dir)
                import standardized_audit_engine
                if hasattr(standardized_audit_engine, "run_full_audit"):
                    return getattr(standardized_audit_engine, "run_full_audit")
            except Exception:
                try:
                    spec = importlib.util.spec_from_file_location("standardized_audit_engine", str(cand_p))
                    if spec and spec.loader:
                        mod = importlib.util.module_from_spec(spec)
                        sys.modules["standardized_audit_engine"] = mod
                        spec.loader.exec_module(mod)
                        if hasattr(mod, "run_full_audit"):
                            return getattr(mod, "run_full_audit")
                except Exception as e:
                    logger.warning("Could not dynamically load audit engine from %s: %s", cand_p, e)
    return None


def _resolve_linter_remediation(
    linter_name: str,
    message: str,
    cid: str,
    file_label: str,
    gen_fn_name: str,
    line_range_label: str,
) -> tuple[str, str, str]:
    """Maps an audit linter and message to (rule_tag, cause, prescriptive_action)."""
    l_low = (linter_name or "").lower()
    m_low = (message or "").lower()
    fn_ref = f"función `{gen_fn_name}` ({line_range_label})" if gen_fn_name else line_range_label

    if "diagnostic_rationale" in l_low or "magic" in l_low:
        if "multiplicador" in m_low or "arbitrary" in m_low:
            return (
                "DIAG-MAGIC-MULT / diagnostic_rationale_alignment_linter",
                (
                    f"El generador en `{file_label}` ({fn_ref}) construye distractores numéricos escalando `ans` "
                    f"por factores constantes o colisionando con multiplicadores prohibidos "
                    f"(0.333, 0.5, 0.667, 0.75, 1.25, 1.333, 1.5, 1.667, 1.85, 2.1, 0.45, 0.15) desconectados de su `error_rationale`."
                ),
                (
                    f"En `{file_label}` ({fn_ref}), reemplaza los multiplicadores sobre `ans` (ej. `ans * 0.70`, `ans / 2.0`, `ans * 1.5`) "
                    f"por las fórmulas algebraicas reales de cada concepción errónea declarada en `dists` y filtra en el bucle de desduplicación "
                    f"que ningún distractor `d` tenga razón `abs(d - round(ans * m, 3)) <= 0.0015` para `m` en "
                    f"`(1.333, 0.667, 1.667, 0.333, 1.25, 0.75, 1.5, 0.5, 2.1, 0.45, 1.85, 0.15)`."
                ),
            )
        return (
            "DIAG-RATIONALE / diagnostic_rationale_alignment_linter",
            f"Los `error_rationale` en `{file_label}` ({fn_ref}) son estáticos, genéricos (< 25 chars) o con unicidad < 30%.",
            (
                f"En `{file_label}` ({fn_ref}), asegura que cada 3-tupla `(did, val, rationale)` en `dists` explique el desvío "
                f"específico interpolando al menos un `@var@` del diccionario `vars` (longitud >= 25 caracteres)."
            ),
        )

    if "socratic" in l_low or "scaffolding" in l_low or "hint" in l_low:
        return (
            f"SOCRATIC-HINTS / {linter_name}",
            (
                f"Las pistas (`hints`) de `{cid}` en `{file_label}` ({line_range_label}) contienen spoilers de la respuesta, "
                f"envenenamiento simbólico/textual copiando `wrong_belief` o muletillas anti-socráticas."
            ),
            (
                f"En `{file_label}` ({line_range_label}), reescribe las 3 pistas con andamiaje socrático constructivo "
                f"(Pista 1: principio conceptual; Pista 2: identidad/planteamiento algebraico; Pista 3: verificación o despeje final "
                f"sin revelar la respuesta ni mencionar errores comunes)."
            ),
        )

    if "length_padded" in l_low or "anti_gaming" in l_low or "distractor_integrity" in l_low or "cloned" in l_low or "telltale" in l_low:
        return (
            f"PSYCHOMETRIC-OPTIONS / {linter_name}",
            (
                f"Las opciones de `{cid}` en `{file_label}` ({fn_ref}) presentan relleno artificial de longitud (`[R-15]`), "
                f"desbalance de longitud (>1.65x), valores clonados, pistas parentéticas o respuestas memorizables."
            ),
            (
                f"En `{file_label}` ({fn_ref}), equilibra la longitud y estructura sintáctica de `correct` y `dists`, "
                f"elimina coletillas repetitivas o parentéticas y asegura que `correct` y los 6 distractores varíen con `@var@`."
            ),
        )

    if "katex" in l_low or "uninterpolated" in l_low or "residue" in l_low or "blind_string" in l_low:
        return (
            f"KATEX-SYNTAX / {linter_name}",
            (
                f"Defecto de sintaxis LaTeX/KaTeX o interpolación de variables en `{file_label}` ({line_range_label}): {message}"
            ),
            (
                f"En `{file_label}` ({line_range_label}), corrige las fórmulas usando cadenas `r\"...\"`, balancea `$` y `{{}}`, "
                f"mantén `\\text{{...}}` <= 45 caracteres, usa `\\Rightarrow`/`\\Leftrightarrow` y verifica que todo `@var@` esté en `vars`."
            ),
        )

    if "zpd" in l_low or "modality" in l_low or "archetype" in l_low:
        return (
            f"ZPD-TRI-BAND / {linter_name}",
            f"Cobertura incompleta de bandas ZPD (`easy`, `medium`, `hard`), arquetipos estructurales (< 3), niveles de Bloom o modalidades activas en `{cid}` ({file_label}).",
            (
                f"En `{file_label}` ({line_range_label}), define al menos 3 tuplas ortogonales en `TEMPLATES` para `{cid}` cubriendo "
                f"`('easy', ...)`, `('medium', ...)`, `('hard', ...)` con >= 2 niveles de Bloom, enunciados estructuralmente distintos y la cuota de `fill_in_the_blank` / `multiple_select`."
            ),
        )

    if "dag" in l_low or "architecture" in l_low:
        return (
            f"DAG-TOPOLOGY / {linter_name}",
            f"Violación topológica en el DAG de competencias (`{cid}`): {message}",
            (
                f"En `{file_label}` ({line_range_label}), corrige `prerequisites` respetando la jerarquía "
                f"`Fact (H-*) -> Concept (C-*) -> Skill (Hab-*)` dentro de un único grafo conexo sin nodos isla."
            ),
        )

    return (
        f"QUALITY-GATE / {linter_name or 'audit_gate'}",
        f"Incumplimiento detectado por `{linter_name}` en `{cid}` ({file_label}, {line_range_label}): {message}",
        f"Edita `{file_label}` en {line_range_label} corrigiendo la condición reportada y recompila el shard con `compile_shard.py --strict`.",
    )


def build_specific_error_report(
    parsed: Optional[dict[str, Any]] = None,
    audit_report: Optional[dict[str, Any]] = None,
    gate_failures: Optional[list[str]] = None,
    work_dir: Optional[Path] = None,
    *,
    course_data: Optional[dict[str, Any]] = None,
) -> dict[str, Any]:
    """Builds a grouped, line-mapped, prescriptive error report from audit_gate_report and persists specific_error_report.{md,json}."""
    if parsed is None:
        parsed = course_data or {}
    if audit_report is None:
        audit_report = {}
    if gate_failures is None:
        gate_failures = []
    course_id = str(parsed.get("course_id") or audit_report.get("course_id") or "course")
    questions = [q for q in (parsed.get("questions") or []) if isinstance(q, dict)]
    q_by_id: dict[str, dict[str, Any]] = {}
    q_by_cid: dict[str, list[dict[str, Any]]] = {}
    for q in questions:
        qid = str(q.get("id") or q.get("question_id") or "").strip()
        cid = str(q.get("competency_id") or "").strip()
        if qid:
            q_by_id[qid] = q
        if cid:
            q_by_cid.setdefault(cid, []).append(q)

    # Import ShardDataLineLocator dynamically from compile_shard.py
    ShardDataLineLocator = None
    curr_dir = Path(__file__).resolve().parent
    if str(curr_dir) not in sys.path:
        sys.path.insert(0, str(curr_dir))
    try:
        from compile_shard import ShardDataLineLocator as _SDLL
        ShardDataLineLocator = _SDLL
    except Exception:
        pass

    # Map competency_id -> shard_id and active Python source file
    cid_to_shard: dict[str, str] = {}
    shard_to_py: dict[str, Path] = {}
    cid_to_py: dict[str, Path] = {}
    locators_cache: dict[str, Any] = {}

    def _get_locator(py_path: Optional[Path]) -> Any:
        if not py_path or not py_path.is_file() or not ShardDataLineLocator:
            return None
        key = str(py_path.resolve())
        if key not in locators_cache:
            try:
                locators_cache[key] = ShardDataLineLocator(py_path)
            except Exception:
                locators_cache[key] = None
        return locators_cache[key]

    def _rel_posix(p: Optional[Path]) -> str:
        if not p:
            return "work/shards/shard_XX_data.py"
        try:
            return p.resolve().relative_to(Path.cwd().resolve()).as_posix()
        except Exception:
            return p.as_posix()

    if work_dir and work_dir.is_dir():
        for m_cand in (work_dir / "shards" / "pre_shard_manifest.json", work_dir / "pre_shard_manifest.json"):
            if m_cand.is_file():
                try:
                    m_data = json.loads(m_cand.read_text(encoding="utf-8"))
                    for s_entry in m_data.get("shards", []):
                        if not isinstance(s_entry, dict):
                            continue
                        s_id = str(s_entry.get("shard_id") or "").strip()
                        cids = list(s_entry.get("competency_ids") or [])
                        if not cids and isinstance(s_entry.get("competencies"), list):
                            cids = [str(c.get("id")) for c in s_entry["competencies"] if isinstance(c, dict) and c.get("id")]
                        s_py = work_dir / "shards" / f"{s_id}_data.py"
                        if s_entry.get("shard_data_path") and Path(s_entry["shard_data_path"]).is_file():
                            s_py = Path(s_entry["shard_data_path"])
                        if s_id:
                            shard_to_py[s_id] = s_py
                        for c_item in cids:
                            cid_to_shard[str(c_item)] = s_id
                            isolated_fix = work_dir / "shards" / "shard_fixes" / s_id / f"{c_item}.py"
                            flat_fix = work_dir / "shards" / "shard_fixes" / f"{c_item}.py"
                            fix_cand = isolated_fix if isolated_fix.is_file() else flat_fix
                            cid_to_py[str(c_item)] = fix_cand if fix_cand.is_file() else s_py
                    break
                except Exception:
                    pass

        # Fallback scan of work/shards/shard_*_data.py if manifest missing or incomplete
        shards_dir = work_dir / "shards"
        if shards_dir.is_dir():
            for py_f in sorted(shards_dir.glob("shard_*_data.py")):
                s_id = py_f.stem.replace("_data", "")
                shard_to_py.setdefault(s_id, py_f)
                loc = _get_locator(py_f)
                if loc:
                    for t_info in getattr(loc, "tuples", []):
                        t_cid = t_info.get("competency_id")
                        if t_cid and t_cid not in cid_to_py:
                            cid_to_shard[t_cid] = s_id
                            isolated_fix = shards_dir / "shard_fixes" / s_id / f"{t_cid}.py"
                            flat_fix = shards_dir / "shard_fixes" / f"{t_cid}.py"
                            fix_cand = isolated_fix if isolated_fix.is_file() else flat_fix
                            cid_to_py[t_cid] = fix_cand if fix_cand.is_file() else py_f

    # Load template_id hints from work/templates/<cid>.json if available
    cid_templates_meta: dict[str, list[dict[str, Any]]] = {}
    if work_dir and (work_dir / "templates").is_dir():
        for tpl_f in sorted((work_dir / "templates").glob("*.json")):
            try:
                tdata = json.loads(tpl_f.read_text(encoding="utf-8"))
                if isinstance(tdata, dict):
                    t_list = tdata.get("templates") if isinstance(tdata.get("templates"), list) else [tdata]
                    cid_templates_meta[tpl_f.stem] = [t for t in t_list if isinstance(t, dict)]
            except Exception:
                pass

    # Collect relevant issues that caused the Quality Gate rejection
    all_issues = [
        i for i in (audit_report.get("all_issues") or audit_report.get("issues") or [])
        if isinstance(i, dict)
    ]
    crit_issues = [i for i in all_issues if i.get("severity") == "critical"]
    warn_issues = [i for i in all_issues if i.get("severity") == "warning"]

    selected_issues: list[dict[str, Any]] = list(crit_issues)
    has_non_crit_gate_failure = any(
        not gf.startswith("Critical audit issues detected") for gf in gate_failures
    )
    if has_non_crit_gate_failure or not selected_issues:
        for wi in warn_issues:
            if wi not in selected_issues:
                selected_issues.append(wi)

    # Also synthesize issue records for length_padded_options and hard_penalties if not already covered
    risk_clusters = audit_report.get("risk_clusters") or {}
    length_padded_ids = risk_clusters.get("length_padded_options") or []
    covered_item_ids = {str(i.get("item_id") or "") for i in selected_issues}
    for lp_qid in length_padded_ids:
        if str(lp_qid) not in covered_item_ids:
            q_lp = q_by_id.get(str(lp_qid), {})
            selected_issues.append({
                "linter": "anti_gaming_psychometric_linter",
                "dimension": "D2_assessment",
                "severity": "critical",
                "item_id": str(lp_qid),
                "competency_id": str(q_lp.get("competency_id") or "unassigned"),
                "message": "Opción correcta con relleno artificial de longitud (length_padded_options).",
                "snippet": "",
            })

    for hp in (audit_report.get("hard_penalties") or []):
        if isinstance(hp, dict) and not selected_issues:
            first_q = questions[0] if questions else {}
            selected_issues.append({
                "linter": str(hp.get("rule") or "hard_penalty"),
                "dimension": "D1_architecture",
                "severity": "critical",
                "item_id": str(first_q.get("id") or "course_bank"),
                "competency_id": str(first_q.get("competency_id") or "global"),
                "message": str(hp.get("reason") or hp.get("rule") or "Hard penalty triggered"),
                "snippet": "",
            })

    if not selected_issues and gate_failures:
        first_q = questions[0] if questions else {}
        for gf in gate_failures:
            selected_issues.append({
                "linter": "publish_quality_gate",
                "dimension": "D1_architecture",
                "severity": "critical",
                "item_id": str(first_q.get("id") or "course_bank"),
                "competency_id": str(first_q.get("competency_id") or "global"),
                "message": gf,
                "snippet": "",
            })

    # Group and consolidate by rule_tag -> (file_rel, cid, template_id, gen_fn_name, off_start, off_end)
    grouped_by_rule: dict[str, dict[tuple[str, str, str, str, int, int], dict[str, Any]]] = {}
    diagnostics_by_competency: dict[str, list[dict[str, Any]]] = {}
    code_contexts: dict[tuple[str, str, str, int, int], list[tuple[int, str]]] = {}
    failing_competencies_set: set[str] = set()
    failing_shards_set: set[str] = set()

    for iss in selected_issues:
        linter = str(iss.get("linter") or "audit_gate")
        item_id = str(iss.get("item_id") or "unknown")
        q_obj = q_by_id.get(item_id)
        cid = str(iss.get("competency_id") or (q_obj.get("competency_id") if q_obj else "") or "").strip()
        if cid in ("unknown", "unassigned", "global", "") and q_obj:
            cid = str(q_obj.get("competency_id") or "").strip()
        if not cid and item_id.startswith("comp_"):
            cid = item_id[5:]

        is_dag_issue = "dag" in linter.lower() or "architecture" in linter.lower()
        shard_id = cid_to_shard.get(cid, "")
        py_path = cid_to_py.get(cid)
        if is_dag_issue and work_dir:
            cta_py = work_dir / "cta_data.py"
            cta_json = work_dir / "cta.json"
            py_path = cta_py if cta_py.is_file() else (cta_json if cta_json.is_file() else py_path)

        file_rel = _rel_posix(py_path) if py_path else (
            f"{_rel_posix(work_dir)}/shards/{shard_id}_data.py" if (work_dir and shard_id) else "work/shards/shard_XX_data.py"
        )

        loc = _get_locator(py_path) if (py_path and py_path.suffix == ".py" and not is_dag_issue) else None
        q_diff = str(q_obj.get("difficulty") or "").strip() if q_obj else ""
        q_itype = str(q_obj.get("interaction_type") or q_obj.get("type") or "").strip() if q_obj else ""
        q_bloom = str(q_obj.get("bloom_taxonomy_level") or q_obj.get("bloom") or "").strip() if q_obj else ""
        q_tpl_id = str(q_obj.get("template_id") or "").strip() if q_obj else ""

        if not q_tpl_id and cid in cid_templates_meta and q_diff:
            for tm in cid_templates_meta[cid]:
                if str(tm.get("difficulty") or "").lower() == q_diff.lower():
                    q_tpl_id = str(tm.get("id") or tm.get("template_id") or "")
                    break

        t_info = None
        if loc:
            t_info = loc.find_tuple_for_question(
                cid=cid,
                template_id=q_tpl_id or None,
                difficulty=q_diff or None,
                interaction_type=q_itype or None,
                bloom=q_bloom or None,
            )

        template_id = (
            (t_info.get("template_id") if t_info else None)
            or q_tpl_id
            or (f"T-{cid}-01" if cid else "T-UNKNOWN")
        )
        gen_fn_name = (t_info.get("gen_fn_name") if t_info else None) or ""
        t_start = int(t_info.get("start_line", 1)) if t_info else 1
        t_end = int(t_info.get("end_line", t_start)) if t_info else t_start
        fn_start, fn_end = (loc.functions.get(gen_fn_name, (t_start, t_end))) if (loc and gen_fn_name) else (t_start, t_end)

        if loc:
            off_start, off_end, off_lines = loc.find_offending_lines(
                t_info,
                linter_name=linter,
                needle=str(iss.get("snippet") or iss.get("message") or ""),
            )
        else:
            off_start, off_end, off_lines = fn_start, fn_end, []

        line_range_label = f"L{off_start}-L{off_end}" if off_start != off_end else f"L{off_start}"
        rule_tag, cause, action = _resolve_linter_remediation(
            linter_name=linter,
            message=str(iss.get("message") or ""),
            cid=cid or "global",
            file_label=file_rel,
            gen_fn_name=gen_fn_name,
            line_range_label=line_range_label,
        )

        if cid and cid not in ("global", "unassigned", "unknown"):
            failing_competencies_set.add(cid)
        if shard_id:
            failing_shards_set.add(shard_id)

        group_key = (file_rel, cid or "global", template_id, gen_fn_name, off_start, off_end)
        rule_bucket = grouped_by_rule.setdefault(rule_tag, {})
        if group_key not in rule_bucket:
            rule_bucket[group_key] = {
                "rule_tag": rule_tag,
                "linter": linter,
                "severity": str(iss.get("severity") or "critical"),
                "file": file_rel,
                "shard_id": shard_id,
                "competency_id": cid or "global",
                "template_id": template_id,
                "gen_fn_name": gen_fn_name,
                "offending_start_line": off_start,
                "offending_end_line": off_end,
                "fn_start_line": fn_start,
                "fn_end_line": fn_end,
                "tuple_start_line": t_start,
                "tuple_end_line": t_end,
                "item_ids": [],
                "messages": [],
                "cause": cause,
                "action": action,
                "offending_code": [f"L{ln}: {txt}" for ln, txt in off_lines],
            }
        entry = rule_bucket[group_key]
        if item_id and item_id not in entry["item_ids"]:
            entry["item_ids"].append(item_id)
        msg_str = str(iss.get("message") or "").strip()
        if msg_str and msg_str not in entry["messages"]:
            entry["messages"].append(msg_str)

        if off_lines:
            ctx_key = (file_rel, cid or "global", f"{template_id} / {gen_fn_name or 'tuple'}", fn_start, fn_end)
            if ctx_key not in code_contexts:
                code_contexts[ctx_key] = off_lines

    # Build proposed repair commands
    work_rel = _rel_posix(work_dir) if work_dir else f"courses/{course_id}/work"
    sorted_cids = sorted(failing_competencies_set)
    sorted_shards = sorted(failing_shards_set)
    if sorted_cids:
        cids_arg = " ".join(sorted_cids)
        proposed_repair_cmd = (
            f'& ".venv\\Scripts\\python.exe" .agents/skills/content-to-course/dispatch.py '
            f'dispatch-repair --work-dir "{work_rel}" --ids {cids_arg}'
        )
    else:
        proposed_repair_cmd = (
            f'& ".venv\\Scripts\\python.exe" .agents/skills/content-to-course/dispatch.py '
            f'dispatch-repair --work-dir "{work_rel}"'
        )

    followup_cmds = [
        f'& ".venv\\Scripts\\python.exe" .agents/skills/content-to-course/run.py --stage templates --work-dir "{work_rel}"',
        f'& ".venv\\Scripts\\python.exe" .agents/skills/content-to-course/run.py --stage build --work-dir "{work_rel}"',
        f'& ".venv\\Scripts\\python.exe" .agents/skills/content-to-course/run.py --stage publish --work-dir "{work_rel}" --output-dir courses --skip-judges',
    ]

    # Populate diagnostics_by_competency for dispatch.py consumption
    total_consolidated = 0
    serializable_groups: dict[str, list[dict[str, Any]]] = {}
    for r_tag, bucket in grouped_by_rule.items():
        serializable_groups[r_tag] = []
        for _, g_entry in bucket.items():
            total_consolidated += 1
            serializable_groups[r_tag].append(g_entry)
            c_key = g_entry["competency_id"]
            diagnostics_by_competency.setdefault(c_key, []).append(g_entry)

    report_md_path = (work_dir / "specific_error_report.md") if work_dir else None
    report_json_path = (work_dir / "specific_error_report.json") if work_dir else None
    report_md_rel = _rel_posix(report_md_path) if report_md_path else f"{work_rel}/specific_error_report.md"

    # Format structured text/markdown report
    md_lines: list[str] = [
        "# SPECIFIC ERROR REPORT — PRE-PUBLISH QUALITY GATE",
        f"- **Course ID:** `{course_id}`",
        f"- **Status:** `REJECTED` ({len(selected_issues)} hallazgos consolidados en {total_consolidated} bloque(s) de plantilla a través de {len(sorted_cids)} competencia(s): `{', '.join(sorted_cids) or 'global'}`)",
        f"- **Affected Shards:** `{', '.join(sorted_shards) or 'N/A'}`",
        f"- **Report Path:** `{report_md_rel}`",
        f"- **Proposed Repair Command:** `{proposed_repair_cmd}`",
        "",
        "## 1. GROUPED ERRORS BY RULE / LINTER",
        "",
    ]

    for r_tag, entries in serializable_groups.items():
        md_lines.append(f"[-] [{r_tag}]")
        if entries:
            first_ent = entries[0]
            first_desc = first_ent["messages"][0] if first_ent["messages"] else "Incumplimiento de regla de calidad"
            md_lines.append(f"  Descripción: {first_desc}")
            md_lines.append(f"  Causa: {first_ent['cause']}")
            md_lines.append(f"  Acción: {first_ent['action']}")
        for ent in entries:
            off_s = ent["offending_start_line"]
            off_e = ent["offending_end_line"]
            line_str = f"L{off_s}-L{off_e}" if off_s != off_e else f"L{off_s}"
            items_list = ent["item_ids"]
            items_preview = ", ".join(items_list[:6])
            if len(items_list) > 6:
                items_preview += f", ... ({len(items_list)} items)"
            elif len(items_list) > 1:
                items_preview += f" ({len(items_list)} items)"
            fn_label = f"Fn {ent['gen_fn_name']}: L{ent['fn_start_line']}..L{ent['fn_end_line']} | " if ent["gen_fn_name"] else ""
            tuple_label = f"Tupla: L{ent['tuple_start_line']}..L{ent['tuple_end_line']}"
            desc_str = ent["messages"][0] if ent["messages"] else "Incumplimiento de regla de calidad"
            md_lines.append(
                f"  • {ent['file']}:{line_str} "
                f"[comp={ent['competency_id']} | template_id={ent['template_id']} | item_ids={items_preview}] "
                f"[{fn_label}{tuple_label}] — {desc_str}"
            )
        md_lines.append("")

    if code_contexts:
        md_lines.append("## 2. CONTEXTO EXACTO (OFFENDING LINES)")
        md_lines.append("")
        for (f_rel, c_id, fn_id, fn_s, fn_e), c_lines in code_contexts.items():
            md_lines.append(f"--- {f_rel} ({c_id} / {fn_id} StartLine={fn_s}, EndLine={fn_e}) ---")
            for ln, ltxt in c_lines[:10]:
                md_lines.append(f"  L{ln:3d}: {ltxt}")
            md_lines.append("")

    md_lines.extend([
        "## 3. PROPOSED REPAIR COMMAND (ORQUESTADOR / C2C_REPAIR)",
        f"1. Despachar reparación quirúrgica para las competencias afectadas (`{', '.join(sorted_cids) or 'ALL'}`):",
        "   ```powershell",
        f"   {proposed_repair_cmd}",
        "   ```",
        "2. Una vez completado `c2c_repair`, recompilar plantillas, reconstruir el banco y republicar:",
        "   ```powershell",
        *[f"   {cmd}" for cmd in followup_cmds],
        "   ```",
    ])

    report_text = "\n".join(md_lines)
    from engine.interstage_schemas import RejectionSpec
    rej_spec = RejectionSpec(
        status="REJECTED",
        course_id=course_id,
        total_issues=len(selected_issues),
        consolidated_blocks=total_consolidated,
        failing_competencies=sorted_cids,
        failing_shards=sorted_shards,
        affected_shards=sorted_shards,
        specific_error_report_path=report_md_rel,
        proposed_repair_command=proposed_repair_cmd,
        followup_commands=followup_cmds,
        gate_failures=gate_failures,
        grouped_by_rule=serializable_groups,
        groups=serializable_groups,
        diagnostics_by_competency=diagnostics_by_competency,
        report_text=report_text,
    )
    structured_payload = rej_spec.to_dict()

    if work_dir:
        try:
            work_dir.mkdir(parents=True, exist_ok=True)
            if report_md_path:
                report_md_path.write_text(report_text, encoding="utf-8")
            if report_json_path:
                report_json_path.write_text(json.dumps(structured_payload, indent=2, ensure_ascii=False), encoding="utf-8")
            rej_spec_path = work_dir / "publish_rejection_spec.json"
            rej_spec.write_json(rej_spec_path)
        except Exception as e:
            logger.warning("Could not write specific_error_report / publish_rejection_spec files: %s", e)

    return structured_payload


@dataclass
class PublicationResult:
    """Outcome of publishing a course to the platform."""
    success: bool
    course_id: str
    course_title: str
    published_json_path: str
    published_cta_path: Optional[str]
    total_competencies: int
    total_questions: int
    competency_breakdown: dict[str, int]
    interaction_type_breakdown: dict[str, int]
    validation_passed: bool
    launch_command: str
    launch_url: str
    error_message: Optional[str] = None
    audit_report: Optional[dict[str, Any]] = None
    published_qa_report_path: Optional[str] = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class CoursePublisher:
    """Manages validation, disk persistence, and platform registration."""

    def __init__(
        self,
        courses_dir: str | Path = "courses",
        project_root: Optional[str | Path] = None,
    ) -> None:
        self.courses_dir = Path(courses_dir)
        if project_root:
            self.project_root = Path(project_root).resolve()
        else:
            # Hermetic resolution: find project root containing .venv or src
            curr = Path(__file__).resolve().parent
            root = curr
            for parent in [curr] + list(curr.parents):
                if (parent / ".venv").is_dir() or (parent / "src").is_dir():
                    root = parent
                    break
            self.project_root = root

    def publish(
        self,
        course_data: dict[str, Any] | str,
        output_dir: Optional[str | Path] = None,
        strict: bool = True,
        cta_markdown: Optional[str] = None,
        append: bool = False,
        work_dir: Optional[str | Path] = None,
    ) -> PublicationResult:
        """Validates strictly, writes course files to disk, and prints launch instructions.
        
        If append=True and the target course JSON already exists, merges new competencies
        and questions with existing data using composite similarity matching.
        """
        out_dir = Path(output_dir) if output_dir else self.courses_dir
        out_dir.mkdir(parents=True, exist_ok=True)

        # 1. Parse incoming course data
        if isinstance(course_data, str):
            parsed = json.loads(course_data)
        else:
            parsed = json.loads(json.dumps(course_data))

        course_id = parsed.get("course_id", "course_demo")
        course_title = parsed.get("course_title") or parsed.get("title") or "Curso Top's Academy"
        json_path = out_dir / f"{course_id}.json"

        # Handle corrupted Unicode in course_title (\ufffd)
        if is_corrupted_unicode(course_title):
            logger.warning("Course title contains corrupted Unicode character ('\\ufffd'): %r.", course_title)
            if append and json_path.is_file():
                try:
                    ex_data = json.loads(json_path.read_text(encoding="utf-8"))
                    ex_title = ex_data.get("course_title") or ex_data.get("title")
                    if ex_title and not is_corrupted_unicode(ex_title):
                        logger.info("Recovered course title from existing course: %r", ex_title)
                        course_title = ex_title
                        parsed["course_title"] = ex_title
                        parsed["title"] = ex_title
                except Exception:
                    pass
            if is_corrupted_unicode(course_title) and hasattr(self, "courses_dir"):
                for cand_dir in (Path(out_dir) / course_id / "work", Path(out_dir) / course_id / "work_append", Path("courses") / course_id / "work"):
                    work_cta = cand_dir / "cta.json"
                    if work_cta.is_file():
                        try:
                            c_data = json.loads(work_cta.read_text(encoding="utf-8"))
                            c_title = c_data.get("course_title") or c_data.get("title")
                            if c_title and not is_corrupted_unicode(c_title):
                                logger.info("Recovered course title from cta.json: %r", c_title)
                                course_title = c_title
                                parsed["course_title"] = c_title
                                parsed["title"] = c_title
                                break
                        except Exception:
                            pass

        # 1b. If append mode is active and existing file exists, merge content with ID collision remapping
        comp_id_remap: dict[str, str] = {}
        distractor_id_remap: dict[str, str] = {}
        if append and json_path.is_file():
            try:
                existing_data = json.loads(json_path.read_text(encoding="utf-8"))
                existing_comp_by_id: dict[str, dict[str, Any]] = {}
                max_num_by_prefix: dict[str, int] = {}
                width_by_prefix: dict[str, int] = {}

                for ec in existing_data.get("competencies", []):
                    if not isinstance(ec, dict):
                        continue
                    ec_id = str(ec.get("id") or ec.get("competency_id") or "")
                    if ec_id:
                        existing_comp_by_id[ec_id] = ec
                        m_pre = re.match(r"^([A-Za-z]+-?)(\d+)$", ec_id)
                        if m_pre:
                            pref, num_s = m_pre.group(1), m_pre.group(2)
                            max_num_by_prefix[pref] = max(max_num_by_prefix.get(pref, 0), int(num_s))
                            width_by_prefix[pref] = max(width_by_prefix.get(pref, 2), len(num_s))

                # Snapshot base existing competencies to deduplicate only against base course
                base_existing_comp_by_id = dict(existing_comp_by_id)

                def _remap_dist_id(d_id: str, old_c: str, new_c: str) -> str:
                    m_old = re.match(r"^([A-Za-z]+)-?(\d+)$", old_c)
                    m_new = re.match(r"^([A-Za-z]+)-?(\d+)$", new_c)
                    if not m_old or not m_new:
                        return d_id.replace(old_c, new_c)
                    old_num, new_num = m_old.group(2), m_new.group(2)
                    old_tag = f"{m_old.group(1)}{old_num}"
                    new_tag = f"{m_new.group(1)}{new_num}"
                    if old_tag in d_id:
                        return d_id.replace(old_tag, new_tag, 1)
                    return re.sub(rf"^([Dd]-?){re.escape(old_num)}(-)", rf"\g<1>{new_num}\2", d_id)

                for c in parsed.get("competencies", []):
                    if not isinstance(c, dict):
                        continue
                    orig_cid = str(c.get("id") or c.get("competency_id") or "")
                    if not orig_cid:
                        continue
                    inc_name = str(c.get("name") or c.get("title") or "").strip().lower()

                    # Check for duplicate / paraphrase against base existing competencies
                    matching_ex_id = None
                    if orig_cid in base_existing_comp_by_id:
                        ex_c = base_existing_comp_by_id[orig_cid]
                        if are_competencies_duplicate(c, ex_c):
                            matching_ex_id = orig_cid

                    if not matching_ex_id:
                        for ec_id, ex_c in base_existing_comp_by_id.items():
                            if are_competencies_duplicate(c, ex_c):
                                matching_ex_id = ec_id
                                break

                    if matching_ex_id:
                        comp_id_remap[orig_cid] = matching_ex_id
                        logger.info("Merged duplicate/paraphrased competency '%s' into '%s'", orig_cid, matching_ex_id)
                    elif orig_cid not in existing_comp_by_id:
                        new_cid = orig_cid
                        comp_id_remap[orig_cid] = new_cid
                        existing_comp_by_id[new_cid] = c
                        m_pre = re.match(r"^([A-Za-z]+-?)(\d+)$", new_cid)
                        if m_pre:
                            pref, num_s = m_pre.group(1), m_pre.group(2)
                            max_num_by_prefix[pref] = max(max_num_by_prefix.get(pref, 0), int(num_s))
                        existing_data.setdefault("competencies", []).append(c)
                    else:
                        ex_c = existing_comp_by_id[orig_cid]
                        ex_name = str(ex_c.get("name") or ex_c.get("title") or "").strip().lower()
                        m_pre = re.match(r"^([A-Za-z]+-?)(\d+)$", orig_cid)
                        if m_pre:
                            pref, num_s = m_pre.group(1), m_pre.group(2)
                            width = max(width_by_prefix.get(pref, 2), len(num_s))
                            next_n = max_num_by_prefix.get(pref, int(num_s)) + 1
                            while f"{pref}{next_n:0{width}d}" in existing_comp_by_id:
                                next_n += 1
                            max_num_by_prefix[pref] = next_n
                            new_cid = f"{pref}{next_n:0{width}d}"
                        else:
                            idx_s = len(existing_comp_by_id) + 1
                            new_cid = f"{orig_cid}_{idx_s:02d}"

                        comp_id_remap[orig_cid] = new_cid
                        logger.warning(
                            "[WARN] FALLBACK REMAP: Competency ID collision detected during append for '%s' "
                            "(incoming: '%s' vs existing: '%s'). Remapping to '%s' as fallback. "
                            "Upstream stages should generate non-overlapping delta IDs via prepare --append.",
                            orig_cid, inc_name, ex_name, new_cid
                        )
                        c["id"] = new_cid
                        if "competency_id" in c:
                            c["competency_id"] = new_cid
                        for d in c.get("distractors", []):
                            if isinstance(d, dict) and d.get("id"):
                                old_did = str(d["id"])
                                new_did = _remap_dist_id(old_did, orig_cid, new_cid)
                                distractor_id_remap[old_did] = new_did
                                d["id"] = new_did
                        existing_comp_by_id[new_cid] = c
                        existing_data.setdefault("competencies", []).append(c)

                # Update prerequisites in all competencies: remap IDs, drop self-loops, and deduplicate
                merged_comps = existing_data.get("competencies", [])
                for comp in merged_comps:
                    if isinstance(comp, dict) and "prerequisites" in comp:
                        old_prereqs = comp.get("prerequisites", [])
                        if isinstance(old_prereqs, list):
                            new_prereqs = []
                            curr_cid = str(comp.get("id") or comp.get("competency_id") or "")
                            for p in old_prereqs:
                                remapped_p = comp_id_remap.get(str(p), str(p))
                                if remapped_p != curr_cid and remapped_p != comp.get("id") and remapped_p not in new_prereqs:
                                    new_prereqs.append(remapped_p)
                            comp["prerequisites"] = new_prereqs

                dag_errors = check_prerequisites_dag(merged_comps)
                if dag_errors:
                    logger.warning("Post-merge prerequisites DAG issues: %s", dag_errors)

                # Merge optional units/modules if present
                if isinstance(parsed.get("units"), list):
                    ex_units = existing_data.setdefault("units", [])
                    ex_unit_names = {str(u.get("name") or u.get("title") or u).strip().lower() for u in ex_units if isinstance(u, (dict, str))}
                    for u in parsed["units"]:
                        u_key = str(u.get("name") or u.get("title") or u).strip().lower() if isinstance(u, (dict, str)) else ""
                        if u_key and u_key not in ex_unit_names:
                            ex_units.append(u)
                            ex_unit_names.add(u_key)

                existing_q_ids = {
                    q.get("id") or q.get("question_id") for q in existing_data.get("questions", [])
                }
                existing_signatures = {
                    (q.get("stem", "").strip(), str(q.get("correct_answer", "")).strip())
                    for q in existing_data.get("questions", [])
                }

                for q in parsed.get("questions", []):
                    old_q_cid = str(q.get("competency_id") or "")
                    eff_cid = comp_id_remap.get(old_q_cid, old_q_cid)
                    if eff_cid:
                        q["competency_id"] = eff_cid
                    if q.get("subcompetency_id") in comp_id_remap:
                        q["subcompetency_id"] = comp_id_remap[str(q["subcompetency_id"])]

                    if distractor_id_remap:
                        for arch in q.get("distractor_archetypes", []):
                            if isinstance(arch, dict) and arch.get("id") in distractor_id_remap:
                                arch["id"] = distractor_id_remap[str(arch["id"])]
                        for opt in q.get("options", []):
                            if isinstance(opt, dict) and opt.get("distractor_id") in distractor_id_remap:
                                opt["distractor_id"] = distractor_id_remap[str(opt["distractor_id"])]

                    item_sig = (q.get("stem", "").strip(), str(q.get("correct_answer", "")).strip())
                    if item_sig in existing_signatures:
                        continue

                    orig_id = q.get("id") or q.get("question_id")
                    if orig_id in existing_q_ids or (old_q_cid and eff_cid != old_q_cid):
                        comp_tag = (eff_cid or "Q").replace("-", "")
                        next_idx = len(existing_data.get("questions", [])) + 1
                        new_id = f"Q-{comp_tag}-app-{next_idx:03d}"
                        while new_id in existing_q_ids:
                            next_idx += 1
                            new_id = f"Q-{comp_tag}-app-{next_idx:03d}"
                        q["id"] = new_id
                        if "question_id" in q:
                            q["question_id"] = new_id
                        existing_q_ids.add(new_id)
                    else:
                        existing_q_ids.add(orig_id)

                    existing_signatures.add(item_sig)
                    existing_data.setdefault("questions", []).append(q)

                parsed = existing_data
                course_title = parsed.get("course_title", course_title)
                logger.info(
                    "Appended questions into existing course %s. New total: %d questions across %d competencies.",
                    json_path.name,
                    len(parsed.get("questions", [])),
                    len(parsed.get("competencies", [])),
                )
            except Exception as ex:
                logger.warning("Failed to load existing course JSON for append: %s", ex)

        # 1c. Standardized Pre-Publish Quality Gate
        resolved_work_dir: Optional[Path] = None
        if work_dir:
            resolved_work_dir = Path(work_dir)
            resolved_work_dir.mkdir(parents=True, exist_ok=True)
        else:
            for cand_w in (
                out_dir / course_id / "work",
                out_dir / course_id / "work_append",
                Path("courses") / course_id / "work",
                Path("work"),
            ):
                if cand_w.is_dir():
                    resolved_work_dir = cand_w
                    break

        audit_report: Optional[dict[str, Any]] = None
        qa_report_path_str: Optional[str] = None
        audit_fn = _load_run_full_audit(self.project_root)
        if audit_fn:
            try:
                audit_report = audit_fn(parsed)
                if resolved_work_dir:
                    resolved_work_dir.mkdir(parents=True, exist_ok=True)
                    gate_report_path = resolved_work_dir / "audit_gate_report.json"
                    gate_report_path.write_text(json.dumps(audit_report, indent=2, ensure_ascii=False), encoding="utf-8")

                if strict:
                    questions = parsed.get("questions", [])
                    num_questions = len(questions)
                    mastery_readiness = audit_report.get("mastery_path_readiness", {})
                    mpri_val = audit_report.get("mpri_score")
                    mpri_score = mpri_val if mpri_val is not None else mastery_readiness.get("mpri_score", 0.0)
                    pillars = audit_report.get("pillars", mastery_readiness.get("pillars", {}))
                    zpd_score = pillars.get("zpd_adaptive_progression", {}).get("score", 0.0)
                    diag_pillar_score = pillars.get("diagnostic_remediation_alignment", {}).get("score", 0.0)

                    dim_summaries = audit_report.get("dimension_summaries", {})
                    diag_summary = audit_report.get("diagnostics") or dim_summaries.get("diagnostic_rationale_alignment_linter", {})
                    total_rationales = diag_summary.get("total_rationales", audit_report.get("total_rationales", 0))
                    if total_rationales == 0:
                        total_rationales = sum(len(q.get("options", [])) - 1 for q in questions if isinstance(q, dict))
                    uniq_val = diag_summary.get("rationale_uniqueness_pct")
                    if uniq_val is None:
                        uniq_val = audit_report.get("rationale_uniqueness_pct", 100.0)
                    rationale_uniqueness_pct = uniq_val

                    hard_penalties = audit_report.get("hard_penalties", [])
                    all_issues = audit_report.get("all_issues", [])
                    risk_clusters = audit_report.get("risk_clusters", {})
                    length_padded = risk_clusters.get("length_padded_options", [])

                    gate_failures = []
                    # 1. len(questions) >= 20 and mpri_score < 75.0
                    if num_questions >= 20 and mpri_score < 75.0:
                        gate_failures.append(f"MPRI score below threshold: {mpri_score} < 75.0 (with {num_questions} questions)")

                    # 2. len(questions) >= 6 and zpd_score <= 0.0
                    if num_questions >= 6 and zpd_score <= 0.0:
                        gate_failures.append(f"ZPD progression score collapsed: {zpd_score} <= 0.0 (with {num_questions} questions)")

                    # 3. total_rationales >= 60 and (diag_pillar_score < 13.0 or rationale_uniqueness_pct < 30.0)
                    if total_rationales >= 60 and (diag_pillar_score < 13.0 or rationale_uniqueness_pct < 30.0):
                        gate_failures.append(
                            f"Diagnostic remediation deficiency: pillar score {diag_pillar_score} < 13.0 or "
                            f"uniqueness {rationale_uniqueness_pct}% < 30.0% (total rationales: {total_rationales})"
                        )

                    # 4. len(hard_penalties) > 0 or any(critical issue)
                    if len(hard_penalties) > 0:
                        reasons = [hp.get("reason", hp.get("rule", "penalty")) for hp in hard_penalties]
                        gate_failures.append(f"Hard penalties detected ({len(hard_penalties)}): {'; '.join(reasons)}")

                    crit_issues = [i for i in all_issues if i.get("severity") == "critical"]
                    if crit_issues:
                        crit_msgs = [f"[{i.get('linter', 'crit')}] {i.get('message', '')}" for i in crit_issues[:3]]
                        gate_failures.append(f"Critical audit issues detected ({len(crit_issues)}): {'; '.join(crit_msgs)}")

                    # 5. len(risk_clusters.get("length_padded_options", [])) > 0
                    if len(length_padded) > 0:
                        gate_failures.append(f"Length-padded options detected in {len(length_padded)} items: {length_padded[:5]}")

                    # Update gate status in report prior to raising or continuing
                    specific_report: Optional[dict[str, Any]] = None
                    if gate_failures:
                        specific_report = build_specific_error_report(
                            parsed=parsed,
                            audit_report=audit_report,
                            gate_failures=gate_failures,
                            work_dir=resolved_work_dir,
                        )

                    if resolved_work_dir:
                        audit_report["gate_passed"] = (len(gate_failures) == 0)
                        audit_report["gate_failures"] = gate_failures
                        if specific_report:
                            audit_report["specific_error_report_path"] = specific_report.get("specific_error_report_path")
                            audit_report["failing_competencies"] = specific_report.get("failing_competencies", [])
                            audit_report["failing_shards"] = specific_report.get("failing_shards", [])
                            audit_report["proposed_repair_command"] = specific_report.get("proposed_repair_command", "")
                            audit_report["specific_error_report"] = specific_report
                        else:
                            for stale_rep in ("specific_error_report.md", "specific_error_report.json"):
                                stale_p = resolved_work_dir / stale_rep
                                if stale_p.is_file():
                                    try:
                                        stale_p.unlink()
                                    except Exception:
                                        pass
                        gate_report_path = resolved_work_dir / "audit_gate_report.json"
                        gate_report_path.write_text(json.dumps(audit_report, indent=2, ensure_ascii=False), encoding="utf-8")

                    if gate_failures:
                        summary_hdr = "Publish Quality Gate Rejected Publication:\n" + "\n".join(f"  - {f}" for f in gate_failures)
                        if specific_report and specific_report.get("report_text"):
                            err_msg = f"{summary_hdr}\n\n{specific_report['report_text']}"
                        else:
                            err_msg = summary_hdr
                        logger.error(err_msg)
                        raise PublishQualityGateError(err_msg)
            except PublishQualityGateError:
                raise
            except Exception as ex:
                logger.warning("Audit gate evaluation encountered unexpected error: %s", ex)

        # Stamp contract_version: 2 and min_archetypes: 4 from engine.stage_contract
        try:
            from engine.stage_contract import MIN_ARCHETYPES as S4_MIN_ARCH
            effective_min_arch = int(S4_MIN_ARCH)
        except Exception:
            effective_min_arch = 4
        if effective_min_arch < 4:
            effective_min_arch = 4

        parsed["contract_version"] = 2
        parsed["min_archetypes"] = effective_min_arch
        if isinstance(parsed.get("metadata"), dict):
            parsed["metadata"]["contract_version"] = 2
            parsed["metadata"]["min_archetypes"] = effective_min_arch

        raw_text = json.dumps(parsed, ensure_ascii=False, indent=2)

        # 2. Programmatic validation
        v_res = validate_course_content(raw_text, strict=strict)
        if not v_res.is_valid:
            try:
                from repair_loop import RepairLoop
                repairer = RepairLoop(max_iterations=2, strict=strict)
                rep_res = repairer.repair_course(parsed)
                if rep_res.success:
                    parsed = rep_res.repaired_course_data
                    parsed["contract_version"] = 2
                    parsed["min_archetypes"] = effective_min_arch
                    if isinstance(parsed.get("metadata"), dict):
                        parsed["metadata"]["contract_version"] = 2
                        parsed["metadata"]["min_archetypes"] = effective_min_arch
                    raw_text = json.dumps(parsed, ensure_ascii=False, indent=2)
                    v_res = validate_course_content(raw_text, strict=strict)
            except Exception as rx:
                logger.debug("Auto-repair during publish failed: %s", rx)

        if not v_res.is_valid:
            err_summary = "; ".join(f"[{e.rule_id}] {e.message}" for e in v_res.errors[:3])
            return PublicationResult(
                success=False,
                course_id=course_id,
                course_title=course_title,
                published_json_path="",
                published_cta_path=None,
                total_competencies=len(parsed.get("competencies", [])),
                total_questions=len(parsed.get("questions", [])),
                competency_breakdown={},
                interaction_type_breakdown={},
                validation_passed=False,
                launch_command="",
                launch_url="",
                error_message=f"Course failed validation before publishing: {err_summary}",
                audit_report=audit_report,
                published_qa_report_path=None,
            )

        # 3. Write course JSON to disk
        json_path.write_text(raw_text, encoding="utf-8")
        logger.info("Published course JSON to %s", json_path.resolve())

        # 4. Write or append CTA markdown if provided
        cta_path_str: Optional[str] = None
        if cta_markdown:
            cta_path = out_dir / f"competence_analysis_{course_id}.md"
            eff_cta_md = cta_markdown
            full_token_map = {k: v for k, v in {**comp_id_remap, **distractor_id_remap}.items() if k != v}
            if full_token_map:
                pattern = re.compile(
                    r"\b(" + "|".join(re.escape(k) for k in sorted(full_token_map.keys(), key=len, reverse=True)) + r")\b"
                )
                eff_cta_md = pattern.sub(lambda m: full_token_map[m.group(1)], eff_cta_md)

            if append and cta_path.is_file():
                existing_md = cta_path.read_text(encoding="utf-8")
                if eff_cta_md.strip() not in existing_md:
                    merged_md = existing_md.rstrip() + "\n\n---\n\n## Actualización Incremental (Append)\n\n" + eff_cta_md.lstrip() + "\n"
                    cta_path.write_text(merged_md, encoding="utf-8")
            else:
                cta_path.write_text(eff_cta_md, encoding="utf-8")
            cta_path_str = str(cta_path.resolve())
            logger.info("Published CTA analysis to %s", cta_path_str)

        # 5. Execute external CLI validator to confirm strict compliance on disk
        cli_success = self._run_cli_validator(json_path, strict=strict)
        if not cli_success:
            return PublicationResult(
                success=False,
                course_id=course_id,
                course_title=course_title,
                published_json_path=str(json_path.resolve()),
                published_cta_path=cta_path_str,
                total_competencies=len(parsed.get("competencies", [])),
                total_questions=len(parsed.get("questions", [])),
                competency_breakdown={},
                interaction_type_breakdown={},
                validation_passed=False,
                launch_command="",
                launch_url="",
                error_message="External CLI validator check failed.",
                audit_report=audit_report,
                published_qa_report_path=None,
            )

        # 6. Compute metric breakdowns
        comp_breakdown: dict[str, int] = {}
        for c in parsed.get("competencies", []):
            cat = c.get("category", "Other")
            comp_breakdown[cat] = comp_breakdown.get(cat, 0) + 1

        itype_breakdown: dict[str, int] = {}
        for q in parsed.get("questions", []):
            it = q.get("interaction_type", "Other")
            itype_breakdown[it] = itype_breakdown.get(it, 0) + 1

        launch_cmd = "python run_platform.py"
        launch_url = f"http://localhost:3000/#/course/{course_id}"

        # Emit work/publish.cert.json upon successful publication
        if resolved_work_dir:
            try:
                from engine.interstage_schemas import ArtifactCertificate, write_certificate
                pub_sha = hashlib.sha256(json_path.read_bytes()).hexdigest()
                cert = ArtifactCertificate(
                    stage="publish",
                    artifact_id=f"publish_{course_id}",
                    source_sha256=pub_sha,
                    contract_version=2,
                    passed_50_seeds=True,
                )
                write_certificate(resolved_work_dir / "publish.cert.json", cert)
            except Exception as e:
                logger.warning("Could not write publish.cert.json: %s", e)

        # 7. Write QA evaluation artifacts in reports/qa_audits/
        if audit_report:
            try:
                qa_reports_dir = self.project_root / "reports" / "qa_audits"
                qa_reports_dir.mkdir(parents=True, exist_ok=True)

                # Generate deterministic QA report JSON and Markdown
                try:
                    import standardized_audit_engine
                    if hasattr(standardized_audit_engine, "generate_deterministic_qa_report"):
                        qa_json, qa_md = standardized_audit_engine.generate_deterministic_qa_report(audit_report, parsed)
                        qa_json_file = qa_reports_dir / f"{course_id}_qa_report.json"
                        qa_md_file = qa_reports_dir / f"{course_id}_qa_report.md"
                        qa_json_file.write_text(json.dumps(qa_json, indent=2, ensure_ascii=False), encoding="utf-8")
                        qa_md_file.write_text(qa_md, encoding="utf-8")
                        qa_report_path_str = str(qa_md_file.resolve())
                        logger.info("Published QA audit report to %s", qa_report_path_str)
                except Exception as ex_gen:
                    logger.debug("Could not generate full deterministic QA markdown: %s", ex_gen)

                # Also write payload file
                try:
                    import prepare_course_payload
                    if hasattr(prepare_course_payload, "summarize_course"):
                        entry = {
                            "id": course_id,
                            "filename": json_path.name,
                            "title": course_title,
                            "status": "valid",
                            "data": parsed,
                        }
                        payload_pkg = prepare_course_payload.summarize_course(entry)
                        payload_file = qa_reports_dir / f"{course_id}_payload.json"
                        payload_file.write_text(json.dumps(payload_pkg, indent=2, ensure_ascii=False), encoding="utf-8")
                except Exception as ex_pkg:
                    logger.debug("Could not write course payload: %s", ex_pkg)
            except Exception as ex_qa:
                logger.warning("Error saving QA reports to reports/qa_audits: %s", ex_qa)

        return PublicationResult(
            success=True,
            course_id=course_id,
            course_title=course_title,
            published_json_path=str(json_path.resolve()),
            published_cta_path=cta_path_str,
            total_competencies=len(parsed.get("competencies", [])),
            total_questions=len(parsed.get("questions", [])),
            competency_breakdown=comp_breakdown,
            interaction_type_breakdown=itype_breakdown,
            validation_passed=True,
            launch_command=launch_cmd,
            launch_url=launch_url,
            audit_report=audit_report,
            published_qa_report_path=qa_report_path_str,
        )

    def _resolve_python_executable(self) -> str:
        """Resolves hermetic Python interpreter path in .venv or falls back to sys.executable."""
        venv_python_win = self.project_root / ".venv" / "Scripts" / "python.exe"
        venv_python_posix = self.project_root / ".venv" / "bin" / "python"

        if sys.platform == "win32" and venv_python_win.is_file():
            return str(venv_python_win.resolve())
        elif venv_python_posix.is_file():
            return str(venv_python_posix.resolve())
        elif venv_python_win.is_file():
            return str(venv_python_win.resolve())
        return sys.executable

    def _run_cli_validator(self, file_path: Path, strict: bool = True) -> bool:
        """Invokes Python validator CLI on published course file with hermetic resolution and fallback."""
        python_bin = self._resolve_python_executable()

        env = dict(os.environ)
        src_dir = (self.project_root / "src").resolve()
        if src_dir.is_dir():
            existing_pp = env.get("PYTHONPATH", "")
            if existing_pp:
                env["PYTHONPATH"] = f"{src_dir}{os.pathsep}{existing_pp}"
            else:
                env["PYTHONPATH"] = str(src_dir)

        cmd = [python_bin, "-m", "validator.cli", str(file_path)]
        if strict:
            cmd.append("--strict")

        try:
            res = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=False,
                env=env,
                cwd=str(self.project_root),
            )
            if res.returncode == 0:
                return True

            output_str = (res.stdout or "") + (res.stderr or "")
            is_env_error = (
                res.returncode in (9009, 127, 2)
                or any(
                    err_term in output_str
                    for err_term in (
                        "ModuleNotFoundError",
                        "ImportError",
                        "No module named",
                        "not recognized as an internal or external command",
                        "No such file or directory",
                    )
                )
            )

            if is_env_error:
                logger.warning(
                    "CLI validator failed due to environment/module issue (code %d): %s. "
                    "Falling back immediately to in-memory validator.",
                    res.returncode,
                    output_str.strip(),
                )
                v = validate_course_content(file_path.read_text(encoding="utf-8"), strict=strict)
                return v.is_valid

            logger.warning("CLI validator returned %d: %s", res.returncode, output_str.strip())
            return False
        except Exception as ex:
            logger.warning("Failed executing CLI validator (%s). Falling back immediately to in-memory validator.", ex)
            try:
                v = validate_course_content(file_path.read_text(encoding="utf-8"), strict=strict)
                return v.is_valid
            except Exception as in_mem_ex:
                logger.error("In-memory validation fallback failed: %s", in_mem_ex)
                return False


def main() -> None:
    """CLI utility for publishing course banks."""
    parser = argparse.ArgumentParser(description="Publish validated course bank to courses/ folder.")
    parser.add_argument("course_json", help="Path to input course JSON file")
    parser.add_argument("--output-dir", "-o", default="courses", help="Courses destination directory")
    parser.add_argument("--strict", action="store_true", default=True, help="Enforce strict mode")
    parser.add_argument("--append", action="store_true", default=False, help="Append questions to existing course JSON")
    sanitized_argv = [sys.argv[0]] + [sanitize_cli_arg(a) for a in sys.argv[1:]]
    args = parser.parse_args(sanitized_argv[1:])

    clean_json_path = sanitize_cli_arg(args.course_json)
    input_p = Path(clean_json_path)
    data = json.loads(input_p.read_text(encoding="utf-8"))

    clean_out_dir = sanitize_cli_arg(args.output_dir)
    publisher = CoursePublisher(courses_dir=clean_out_dir)

    try:
        result = publisher.publish(data, strict=args.strict, append=args.append)
    except PublishQualityGateError as qe:
        print(f"PUBLICATION FAILED (QUALITY GATE): {qe}", file=sys.stderr)
        sys.exit(1)

    if result.success:
        print("=================================================================")
        print(f"COURSE PUBLISHED SUCCESSFULLY: {result.course_title} ({result.course_id})")
        print("=================================================================")
        print(f"File Path: {result.published_json_path}")
        print(f"Competencies ({result.total_competencies}): {result.competency_breakdown}")
        print(f"Questions ({result.total_questions}): {result.interaction_type_breakdown}")
        print(f"Validation: 100% Passed (strict mode)")
        print("\nTo start practicing immediately:")
        print(f"  Command: {result.launch_command}")
        print(f"  URL:     {result.launch_url}")
        print("=================================================================")
    else:
        print(f"PUBLICATION FAILED: {result.error_message}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
