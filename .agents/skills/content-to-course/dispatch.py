"""Scope Isolation, Subagent Dispatch Payload Generator, and Scope Check (C2C v3.2).

Provides zero-bundle dispatch and non-truncating payloads for C2C pipeline subagents:
- c2c_cta_architect: Cognitive Task Analysis Curriculum Architect
- c2c_shard_author: Shard Exercise Authors (pure Python tuples & compile_shard.py)
- c2c_judge: Independent Blind Evaluation Judges (Zero-Warmup In-Prompt resolution)
- c2c_repair: Targeted Repair subagents
"""

from __future__ import annotations

import argparse
import fnmatch
import json
import logging
import os
import re
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union, Set

if sys.platform == "win32":
    try:
        if sys.stdout and hasattr(sys.stdout, "reconfigure"):
            sys.stdout.reconfigure(encoding="utf-8")
        if sys.stderr and hasattr(sys.stderr, "reconfigure"):
            sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

logger = logging.getLogger("dispatch")

# Directory of the skill
SKILL_DIR = Path(__file__).parent.resolve()


def load_system_prompt(name_or_path: Union[str, Path]) -> str:
    """Loads the 100% full, uncompressed content of a system prompt markdown file.
    
    PROHIBIDO truncar, resumir o comprimir los system_prompts/*.md.
    """
    p = Path(name_or_path)
    if not p.is_absolute():
        candidates = [
            SKILL_DIR / "system_prompts" / p.name,
            SKILL_DIR / p,
            Path.cwd() / p,
        ]
        for c in candidates:
            if c.is_file():
                return c.read_text(encoding="utf-8")
        raise FileNotFoundError(f"System prompt file not found: {name_or_path}")
    if not p.is_file():
        raise FileNotFoundError(f"System prompt file not found: {p}")
    return p.read_text(encoding="utf-8")


def get_type_definitions() -> List[Dict[str, Any]]:
    """Returns subagent type definitions for define_subagent registration with 100% full system prompts."""
    return [
        {
            "name": "c2c_cta_architect",
            "description": "Cognitive Task Analysis Curriculum Architect for C2C v3.2 (pure positional tuples in cta_data.py)",
            "system_prompt": load_system_prompt("prompt_cta_architect.md"),
            "enable_write_tools": True,
            "enable_subagent_tools": False,
            "enable_mcp_tools": False,
        },
        {
            "name": "c2c_shard_author",
            "description": "Shard Exercise Author for native Python parametric templates and compile_shard.py",
            "system_prompt": load_system_prompt("prompt_shard_author.md"),
            "enable_write_tools": True,
            "enable_subagent_tools": False,
            "enable_mcp_tools": False,
        },
        {
            "name": "c2c_judge",
            "description": "Independent Blind Psychometric Evaluation Judge with Zero-Warmup in-prompt resolution",
            "system_prompt": load_system_prompt("prompt_blind_judge.md"),
            "enable_write_tools": True,
            "enable_subagent_tools": False,
            "enable_mcp_tools": False,
        },
        {
            "name": "c2c_repair",
            "description": "Targeted Quality Repair Engineer for fixing failing templates or discordances",
            "system_prompt": load_system_prompt("prompt_shard_author.md"),
            "enable_write_tools": True,
            "enable_subagent_tools": False,
            "enable_mcp_tools": False,
        },
    ]


ROLE_SPECS: Dict[str, Dict[str, Any]] = {
    "cta": {
        "type_name": "c2c_cta_architect",
        "model": "flash",
        "system_prompt": "system_prompts/prompt_cta_architect.md",
        "read": [
            "work/pre_cta_manifest.json",
            "work/cta_data.py",
            "work/cta_parts/**",
            "work/cta.json",
            "content/**",
        ],
        "write": [
            "work/cta_data.py",
            "work/cta.json",
            "work/cta.md",
            "work/cta_parts/**",
        ],
        "forbidden": [
            "engine/*",
            "SKILL.md",
            "scripts Python auxiliares en scratch/",
        ],
        "turn_budget": 20,
    },
    "cta-direct": {
        "type_name": "c2c_cta_architect",
        "model": "flash",
        "system_prompt": "system_prompts/prompt_cta_architect.md",
        "read": [
            "work/pre_cta_manifest.json",
            "work/cta_data.py",
            "work/cta_parts/**",
            "work/cta.json",
            "content/**",
        ],
        "write": [
            "work/cta_data.py",
            "work/cta.json",
            "work/cta.md",
            "work/cta_parts/**",
        ],
        "forbidden": [
            "engine/*",
            "SKILL.md",
            "scripts Python auxiliares en scratch/",
        ],
        "turn_budget": 20,
    },
    "author": {
        "type_name": "c2c_shard_author",
        "model": "flash",
        "system_prompt": "system_prompts/prompt_shard_author.md",
        "read": [
            "content/**",
            "work/pre_cta_manifest.json",
            "work/shards/pre_shard_manifest.json",
            "work/shards/*_data.py",
            "work/templates/*.json",
            ".agents/skills/content-to-course/compile_shard.py",
            "work/cta.json",
        ],
        "write": [
            "work/shards/*_data.py",
            "work/templates/*.json",
        ],
        "forbidden": [
            "scratch/**",
            "work/scratch/**",
            "engine/*",
            "SKILL.md",
            ".check_attempts/**",
        ],
        "turn_budget": 30,
    },
    "judge": {
        "type_name": "c2c_judge",
        "model": "flash",
        "system_prompt": "system_prompts/prompt_blind_judge.md",
        "read": [
            "work/verification/judge_batch_*.json",
            "work/judge_batch_*.json",
        ],
        "write": [
            "work/verification/judge_responses_*.json",
            "work/judge_responses_*.json",
        ],
        "forbidden": [
            "judge_ground_truth.json",
            "work/templates/*",
            "templates/*",
            "search_web",
            "read_url_content",
            "navegación por internet",
        ],
        "turn_budget": 5,
    },
    "repair": {
        "type_name": "c2c_repair",
        "model": "flash",
        "system_prompt": "system_prompts/prompt_shard_author.md",
        "read": [
            "work/shards/*",
            "work/reports/templates_report.json",
            "work/judge_report.json",
            "work/templates/*.json",
        ],
        "write": [
            "work/shards/*_data.py",
            "work/templates/*.json",
        ],
        "forbidden": [
            "engine/*",
            "SKILL.md",
        ],
        "turn_budget": 15,
    },
    "cta-map": {
        "type_name": "c2c_cta_architect",
        "model": "flash",
        "system_prompt": "system_prompts/prompt_cta_architect.md",
        "read": [
            "work/sections/section_*.md",
            "work/pre_cta_manifest.json",
        ],
        "write": [
            "work/cta_parts/part_*.py",
            "work/cta_parts/cta_part_*.json",
        ],
        "forbidden": [
            "código fuente",
            "SKILL.md",
        ],
        "turn_budget": 15,
    },
    "cta-reduce": {
        "type_name": "c2c_cta_architect",
        "model": "flash",
        "system_prompt": "system_prompts/prompt_cta_architect.md",
        "read": [
            "work/cta_outline.json",
            "work/duplicate_candidates.json",
        ],
        "write": [
            "work/cta_harmonize.json",
            "work/cta.json",
        ],
        "forbidden": [
            "código fuente",
            "SKILL.md",
        ],
        "turn_budget": 10,
    },
}


def get_work_rel(work_dir: Union[str, Path]) -> str:
    """Returns normalized relative POSIX path for work_dir within cwd, falling back to 'work'."""
    p = Path(work_dir)
    if not p.is_absolute():
        p_str = p.as_posix()
        if p_str == "work" or p_str.startswith("courses/"):
            return p_str
        resolved = (Path.cwd() / p).resolve()
    else:
        resolved = p.resolve()

    try:
        rel = resolved.relative_to(Path.cwd().resolve())
        return rel.as_posix()
    except ValueError:
        return "work"


def generate_define_subagent_specs(work_dir: Union[str, Path]) -> Dict[str, Any]:
    """Writes individual subagent type spec files in work/dispatch/types/<type_name>.json
    and the consolidated index in work/dispatch/subagent_types.json.
    
    Each individual file is < 20 KB and contains the 100% full system prompt,
    enabling parallel view_file calls without truncation.
    """
    work = Path(work_dir).resolve()
    types_dir = work / "dispatch" / "types"
    types_dir.mkdir(parents=True, exist_ok=True)

    types_list = get_type_definitions()
    type_files: List[str] = []

    for t_spec in types_list:
        t_name = t_spec["name"]
        clean_name = t_name.replace("-", "_")
        t_file = types_dir / f"{clean_name}.json"
        t_file.write_text(json.dumps(t_spec, indent=2, ensure_ascii=False), encoding="utf-8")
        type_files.append(t_file.resolve().as_posix())

    summary_payload = {
        "types": types_list,
        "type_files": type_files,
    }

    subagent_types_file = work / "dispatch" / "subagent_types.json"
    subagent_types_file.parent.mkdir(parents=True, exist_ok=True)
    subagent_types_file.write_text(json.dumps(summary_payload, indent=2, ensure_ascii=False), encoding="utf-8")

    return summary_payload


def dispatch_cta(work_dir: Union[str, Path], mode: Optional[str] = None) -> Dict[str, Any]:
    """Generates dispatch payload and individual item files for CTA Architect.
    
    Exige work/pre_cta_manifest.json (cero fallbacks; si no existe, lanza/retorna BLOCKER:: No existe pre_cta_manifest.json).
    - En modo direct: genera work/dispatch/items/cta_01.json (< 46,080 bytes) formateando de forma compacta
      si hay > 50 documentos para garantizar que view_file nunca trunque ni se pierda un solo byte del system prompt.
    - En modo mapreduce: genera un ítem por subpart en work/dispatch/items/cta_01.json, cta_02.json, ..., cta_MM.json,
      pasando a cada subagente únicamente el documento/rango de páginas de su subpart y el comando
      compile_cta.py --work "<work_dir>" --part <subpart_id>.
    """
    work = Path(work_dir).resolve()
    work_rel = get_work_rel(work)
    manifest_path = work / "pre_cta_manifest.json"
    if not manifest_path.is_file():
        err_msg = "BLOCKER:: No existe pre_cta_manifest.json"
        logger.error(err_msg)
        raise FileNotFoundError(err_msg)

    manifest_data = json.loads(manifest_path.read_text(encoding="utf-8"))
    cta_mode = mode or manifest_data.get("cta_mode") or "direct"

    sys_prompt_full = load_system_prompt("prompt_cta_architect.md")
    items_dir = work / "dispatch" / "items"
    items_dir.mkdir(parents=True, exist_ok=True)

    subagents: List[Dict[str, Any]] = []
    item_files: List[str] = []

    if cta_mode == "mapreduce":
        subparts = manifest_data.get("subparts") or []
        if not subparts:
            # Fallback derivation from files
            files_list = manifest_data.get("files") or manifest_data.get("documents") or []
            subparts = [
                {
                    "subpart_id": f"part_{i+1:02d}",
                    "subpart_index": i,
                    "doc": f.get("doc") or f.get("doc_name") or f.get("name") or "document.pdf",
                    "path": f.get("path") or f.get("file") or f.get("doc") or "document.pdf",
                    "page_range": f.get("valid_page_range") or f.get("page_range") or [1, f.get("total_pages", 1)],
                    "total_pages": f.get("total_pages", 1),
                }
                for i, f in enumerate(files_list)
            ]
        if not subparts:
            subparts = [
                {
                    "subpart_id": "part_01",
                    "subpart_index": 0,
                    "doc": "material_fuente.pdf",
                    "path": "material_fuente.pdf",
                    "page_range": [1, 1],
                    "total_pages": 1,
                }
            ]

        for idx, sp in enumerate(subparts, start=1):
            subpart_id = sp.get("subpart_id") or f"part_{idx:02d}"
            doc_name = sp.get("doc") or sp.get("doc_name") or sp.get("name") or "document.pdf"
            doc_path = sp.get("path") or sp.get("file") or doc_name
            v_range = sp.get("page_range") or sp.get("valid_page_range") or [1, sp.get("total_pages", 1)]
            total_p = sp.get("total_pages") or (v_range[1] if len(v_range) > 1 else 1)
            out_target = f"{work_rel}/cta_parts/{subpart_id}_data.py"

            subpart_table = "\n".join([
                "| Documento Subpart | Ruta Fuente | Rango de Páginas Válidas (1-indexed) | Total Páginas |",
                "|---|---|---|---|",
                f"| `{doc_name}` | `{doc_path}` | **`{v_range[0]}..{v_range[1]}`** | {total_p} |",
            ])

            compile_cmd = f"python .agents/skills/content-to-course/compile_cta.py --work \"{work.resolve().as_posix()}\" --part {subpart_id}"

            prompt_lines = [
                f"# Asignación de Tarea para Cognitive Task Analysis Architect ({subpart_id} - MapReduce C2C v3.2)",
                "",
                "## 1. SCOPE-LOCK Y CONTEXTO DE EJECUCIÓN",
                f"- **Manifiesto de Entrada OBLIGATORIO:** `{manifest_path.resolve().as_posix()}` (o `{work_rel}/pre_cta_manifest.json`)",
                f"- **Modo CTA:** `mapreduce` (Subpart: `{subpart_id}`)",
                f"- **Ruta de Salida Obligatoria:** `{out_target}`",
                "",
                "## 2. DOCUMENTO ASIGNADO A ESTA SUBPARTE Y RANGO DE PÁGINAS (1..N)",
                subpart_table,
                "",
                "> [!CRITICAL]",
                "> **REGLA MANDATORIA DE PAGINACIÓN `evidence.page`:**",
                f"> SIEMPRE usa el índice de página 1-indexed del archivo PDF (`{v_range[0]}..{v_range[1]}` según la tabla anterior), NUNCA la numeración impresa del libro o capítulo.",
                "",
                "## 3. DIRECTIVAS DE OPERACIÓN",
                f"- Turno 1 MANDATORIO: Abre el material fuente asignado con `view_file`: `{doc_path}`.",
                f"- Escribe las competencias en tuplas tabulares puras de 9 elementos en `{out_target}` (`COMPETENCIES = [...]`).",
                "- Prohibido crear scripts auxiliares en Python o emitir competencias en el chat conversacional.",
                f"- Compila con determinismo ejecutando el compilador oficial:",
                f"  ```bash",
                f"  {compile_cmd}",
                f"  ```",
                f"- Si el compilador reporta errores, corrígelos con `replace_file_content` sobre `{out_target}`.",
                f"- Al certificar PASS, termina estrictamente con: `DONE: {out_target}`.",
                "",
                "---",
                "",
                sys_prompt_full,
            ]
            prompt_full = "\n".join(prompt_lines)

            item_file = items_dir / f"cta_{idx:02d}.json"
            item_data = {
                "TypeName": "c2c_cta_architect",
                "Role": f"Cognitive Task Analysis Architect {subpart_id}",
                "Model": "flash",
                "Workspace": "inherit",
                "Prompt": prompt_full,
            }
            item_file.write_text(json.dumps(item_data, indent=2, ensure_ascii=False), encoding="utf-8")
            subagents.append(item_data)
            item_files.append(item_file.resolve().as_posix())

    else:
        # direct mode
        out_target = f"{work_rel}/cta_data.py"

        # Build document rows
        docs = manifest_data.get("documents") or manifest_data.get("files") or []
        doc_rows: List[Tuple[str, str, str, Any]] = []
        if isinstance(docs, list):
            for d in docs:
                if isinstance(d, dict):
                    d_name = d.get("doc_name") or d.get("name") or d.get("doc") or "document.pdf"
                    d_path = d.get("path") or d.get("file") or d_name
                    v_range = d.get("valid_page_range") or d.get("page_range") or [1, d.get("total_pages", 1)]
                    total_p = d.get("total_pages") or (v_range[1] if len(v_range) > 1 else 1)
                    doc_rows.append((d_name, d_path, f"{v_range[0]}..{v_range[1]}", total_p))
                elif isinstance(d, str):
                    doc_rows.append((d, d, "1..N", "desconocido"))
        elif isinstance(docs, dict):
            for d_name, d_info in docs.items():
                if isinstance(d_info, dict):
                    v_range = d_info.get("valid_page_range") or d_info.get("page_range") or [1, d_info.get("total_pages", 1)]
                    total_p = d_info.get("total_pages") or (v_range[1] if len(v_range) > 1 else 1)
                    d_path = d_info.get("path") or d_name
                    doc_rows.append((d_name, d_path, f"{v_range[0]}..{v_range[1]}", total_p))

        # Compact formatting if > 50 documents to keep payload strictly < 46,080 bytes
        if len(doc_rows) > 50:
            table_lines = [
                "| # | Documento | Rango Válido (1-indexed) | Total Páginas |",
                "|---|---|---|---|",
            ]
            for i, r in enumerate(doc_rows, 1):
                table_lines.append(f"| {i} | `{r[0]}` | **`{r[2]}`** | {r[3]} |")
            doc_table_str = (
                f"- **Total de documentos asignados:** {len(doc_rows)} archivos (ver rutas completas en `pre_cta_manifest.json`).\n\n"
                + "\n".join(table_lines)
            )
        else:
            table_lines = [
                "| Documento | Ruta Fuente | Rango de Páginas Válidas (1-indexed) | Total Páginas |",
                "|---|---|---|---|",
            ]
            for r in doc_rows:
                table_lines.append(f"| `{r[0]}` | `{r[1]}` | **`{r[2]}`** | {r[3]} |")
            doc_table_str = "\n".join(table_lines)

        compile_cmd = f"python .agents/skills/content-to-course/compile_cta.py --work \"{work.resolve().as_posix()}\""

        prompt_lines = [
            "# Asignación de Tarea para Cognitive Task Analysis Architect (C2C v3.2)",
            "",
            "## 1. SCOPE-LOCK Y CONTEXTO DE EJECUCIÓN",
            f"- **Manifiesto de Entrada OBLIGATORIO:** `{manifest_path.resolve().as_posix()}` (o `{work_rel}/pre_cta_manifest.json`)",
            f"- **Modo CTA:** `{cta_mode}`",
            f"- **Ruta de Salida Obligatoria:** `{out_target}`",
            "",
            "## 2. TABLA DE DOCUMENTOS Y RANGOS DE PÁGINAS VÁLIDAS (1..N)",
            doc_table_str,
            "",
            "> [!CRITICAL]",
            "> **REGLA MANDATORIA DE PAGINACIÓN `evidence.page`:**",
            "> SIEMPRE usa el índice de página 1-indexed del archivo PDF (`1..N` según `valid_page_range` en la tabla anterior), NUNCA la numeración impresa del libro o capítulo.",
            "> (Ejemplo: si un PDF tiene 20 páginas impresas del 241 al 260, debes citar páginas entre `1` y `20`).",
            "",
            "## 3. DIRECTIVAS DE OPERACIÓN",
            f"- Turno 1 MANDATORIO: Abre el primer material fuente asignado con `view_file`.",
            f"- Escribe las competencias en tuplas tabulares puras de 9 elementos en `{out_target}`.",
            f"- Prohibido crear scripts auxiliares en Python o emitir competencias en el chat conversacional.",
            f"- Compila con determinismo ejecutando el compilador oficial:",
            f"  ```bash",
            f"  {compile_cmd}",
            f"  ```",
            f"- Si el compilador reporta errores, corrígelos quirúrgicamente con `replace_file_content` sobre `{out_target}`.",
            f"- Termina estrictamente con `DONE: {work_rel}/cta.json`.",
            "",
            "---",
            "",
            sys_prompt_full,
        ]
        prompt_full = "\n".join(prompt_lines)

        item_file = items_dir / "cta_01.json"
        item_data = {
            "TypeName": "c2c_cta_architect",
            "Role": "Cognitive Task Analysis Architect",
            "Model": "flash",
            "Workspace": "inherit",
            "Prompt": prompt_full,
        }
        item_file.write_text(json.dumps(item_data, indent=2, ensure_ascii=False), encoding="utf-8")
        subagents = [item_data]
        item_files = [item_file.resolve().as_posix()]

    dispatch_dir = work / "dispatch"
    dispatch_dir.mkdir(parents=True, exist_ok=True)
    cta_audit_file = dispatch_dir / "cta.json"
    cta_audit = {
        "stage": "cta",
        "cta_mode": cta_mode,
        "dispatched_at": datetime.now(timezone.utc).isoformat(),
        "subagents_count": len(subagents),
        "item_files": item_files,
        "Subagents": subagents,
    }
    cta_audit_file.write_text(json.dumps(cta_audit, indent=2, ensure_ascii=False), encoding="utf-8")

    return {"Subagents": subagents, "item_files": item_files}


def dispatch_authors(work_dir: Union[str, Path]) -> Dict[str, Any]:
    """Generates dispatch payload and individual item files for Shard Authors.
    
    Exige work/shards/pre_shard_manifest.json y work/pre_cta_manifest.json
    (cero fallbacks; si falta alguno, lanza/retorna BLOCKER:: No existe ...).
    NO pre-siembra JSON en work/templates/ ni bundles en work/shards/bundles/.
    Inyecta: 100% de prompt_shard_author.md, competencias asignadas, rutas a PDFs/imágenes,
    e instrucción de escribir tuplas en work/shards/shard_XX_data.py y compilar con compile_shard.py.
    """
    work = Path(work_dir).resolve()
    work_rel = get_work_rel(work)

    shard_manifest_path = work / "shards" / "pre_shard_manifest.json"
    if not shard_manifest_path.is_file():
        err_msg = "BLOCKER:: No existe pre_shard_manifest.json"
        logger.error(err_msg)
        raise FileNotFoundError(err_msg)

    cta_manifest_path = work / "pre_cta_manifest.json"
    if not cta_manifest_path.is_file():
        err_msg = "BLOCKER:: No existe pre_cta_manifest.json"
        logger.error(err_msg)
        raise FileNotFoundError(err_msg)

    cta_file = work / "cta.json"
    cta_comps_by_id: Dict[str, Dict[str, Any]] = {}
    if cta_file.is_file():
        try:
            cta_data = json.loads(cta_file.read_text(encoding="utf-8"))
            for c in cta_data.get("competencies", []):
                if isinstance(c, dict) and "id" in c:
                    cta_comps_by_id[c["id"]] = c
        except Exception as e:
            logger.warning("Could not read cta.json: %s", e)

    # Document map from pre_cta_manifest
    cta_manifest_data = json.loads(cta_manifest_path.read_text(encoding="utf-8"))
    doc_paths_by_name: Dict[str, str] = {}
    docs = cta_manifest_data.get("documents", [])
    if isinstance(docs, list):
        for d in docs:
            if isinstance(d, dict):
                dn = d.get("doc_name") or d.get("name") or d.get("doc")
                dp = d.get("path") or d.get("file") or dn
                if dn:
                    doc_paths_by_name[dn] = dp
    elif isinstance(docs, dict):
        for dn, dinfo in docs.items():
            if isinstance(dinfo, dict):
                doc_paths_by_name[dn] = dinfo.get("path") or dn

    shard_manifest_data = json.loads(shard_manifest_path.read_text(encoding="utf-8"))
    shards_raw = shard_manifest_data.get("shards", [])
    if isinstance(shards_raw, dict):
        shard_list = [{"shard_id": k, "competency_ids": v} for k, v in shards_raw.items()]
    elif isinstance(shards_raw, list):
        shard_list = shards_raw
    else:
        shard_list = []

    sys_prompt_full = load_system_prompt("prompt_shard_author.md")

    items_dir = work / "dispatch" / "items"
    items_dir.mkdir(parents=True, exist_ok=True)

    subagents: List[Dict[str, Any]] = []
    item_files: List[str] = []

    for idx, s in enumerate(shard_list, start=1):
        s_id = s.get("shard_id") or f"shard_{idx:02d}"
        c_ids = s.get("competency_ids") or []
        if not c_ids and "competencies" in s:
            c_ids = [c.get("id") for c in s["competencies"] if "id" in c]

        # Detailed competency breakdown
        comp_details = []
        source_doc_set: Set[str] = set()
        for cid in c_ids:
            c_obj = cta_comps_by_id.get(cid, {})
            c_name = c_obj.get("name", cid)
            c_type = c_obj.get("type", "concept")
            evidence = c_obj.get("evidence", [])
            ev_list = []
            if isinstance(evidence, list):
                for ev in evidence:
                    if isinstance(ev, dict):
                        doc = ev.get("doc", "")
                        page = ev.get("page", 1)
                        resolved_path = doc_paths_by_name.get(doc, doc)
                        ev_list.append(f"`{resolved_path}` (pág. {page})")
                        if resolved_path:
                            source_doc_set.add(resolved_path)
            ev_str = ", ".join(ev_list) if ev_list else "Ver materiales del curso"
            comp_details.append(f"- **`{cid}`** ({c_type}): {c_name} | Evidencia: {ev_str}")

        source_doc_lines = "\n".join(f"- `{p}`" for p in sorted(source_doc_set)) if source_doc_set else "- Consultar archivos en `content/`"
        comp_details_str = "\n".join(comp_details)

        prompt_lines = [
            f"# Asignación de Tarea para Shard Exercise Author: `{s_id}`",
            "",
            "## 1. SCOPE-LOCK Y CONTRATO DE AUTORÍA NATIVA EN PYTHON (C2C v3.2)",
            f"- **Shard Asignado:** `{s_id}`",
            f"- **Archivo Python de Salida OBLIGATORIO:** `{work_rel}/shards/{s_id}_data.py`",
            f"- **Manifiesto de Shards:** `{shard_manifest_path.resolve().as_posix()}`",
            f"- **Manifiesto de Documentos:** `{cta_manifest_path.resolve().as_posix()}`",
            f"- **Compilador Oficial:** `.agents/skills/content-to-course/compile_shard.py`",
            "",
            "## 2. COMPETENCIAS ASIGNADAS AL SHARD",
            comp_details_str,
            "",
            "## 3. DOCUMENTOS FUENTE ASIGNADOS",
            source_doc_lines,
            "",
            "## 4. INSTRUCCIONES DE EJECUCIÓN OBLIGATORIAS",
            f"1. Escribe ÚNICAMENTE las funciones generadoras/verificadoras y la lista de tuplas en `{work_rel}/shards/{s_id}_data.py` (`TEMPLATES = [...]`).",
            f"2. Ejecuta la compilación y certificación estricta en un solo comando CLI:",
            f"   ```bash",
            f"   python .agents/skills/content-to-course/compile_shard.py --work \"{work.resolve().as_posix()}\" --shard {s_id} --strict",
            f"   ```",
            f"3. Si el compilador reporta errores mapeados a línea, corrígelos quirúrgicamente con `replace_file_content` sobre `{work_rel}/shards/{s_id}_data.py`.",
            f"4. Prohibido crear archivos en `scratch/**` o usar `.format()` con LaTeX.",
            f"5. Al certificar PASS, finaliza estrictamente con:",
            f"   `DONE: {work_rel}/shards/{s_id}_data.py`",
            "",
            "---",
            "",
            sys_prompt_full,
        ]
        prompt_full = "\n".join(prompt_lines)

        item_file = items_dir / f"author_{idx:02d}.json"
        item_data = {
            "TypeName": "c2c_shard_author",
            "Role": f"Shard Author {s_id}",
            "Model": "flash",
            "Workspace": "inherit",
            "Prompt": prompt_full,
        }
        item_file.write_text(json.dumps(item_data, indent=2, ensure_ascii=False), encoding="utf-8")
        subagents.append(item_data)
        item_files.append(item_file.resolve().as_posix())

    dispatch_dir = work / "dispatch"
    dispatch_dir.mkdir(parents=True, exist_ok=True)
    authors_audit_file = dispatch_dir / "authors.json"
    authors_audit = {
        "stage": "authors",
        "dispatched_at": datetime.now(timezone.utc).isoformat(),
        "subagents_count": len(subagents),
        "item_files": item_files,
        "Subagents": subagents,
    }
    authors_audit_file.write_text(json.dumps(authors_audit, indent=2, ensure_ascii=False), encoding="utf-8")

    # Also write author.json for backward compatibility with run.py
    author_compat_file = dispatch_dir / "author.json"
    author_compat_file.write_text(json.dumps(authors_audit, indent=2, ensure_ascii=False), encoding="utf-8")

    return {"Subagents": subagents, "item_files": item_files}


def dispatch_judges(work_dir: Union[str, Path]) -> Dict[str, Any]:
    """Generates dispatch payload and individual item files for Blind Judges.
    
    Zero-Warmup In-Prompt payload: inyecta los ítems del batch (question_id, question_type, stem_es, options)
    directamente dentro del Prompt junto con el 100% de prompt_blind_judge.md.
    El juez NO usa view_file para leer judge_batch_XX.json y resuelve en 1 solo turno.
    """
    work = Path(work_dir).resolve()
    work_rel = get_work_rel(work)

    # Search for judge batches
    batch_files = sorted(work.glob("verification/judge_batch_*.json"))
    if not batch_files:
        batch_files = sorted(work.glob("judge_batch_*.json"))
    split_batches = [bf for bf in batch_files if bf.name != "judge_batch.json"]

    if not split_batches:
        unsplit = work / "verification" / "judge_batch.json"
        if not unsplit.is_file():
            unsplit = work / "judge_batch.json"
        if unsplit.is_file():
            split_batches = [unsplit]

    sys_prompt_full = load_system_prompt("prompt_blind_judge.md")

    items_dir = work / "dispatch" / "items"
    items_dir.mkdir(parents=True, exist_ok=True)

    subagents: List[Dict[str, Any]] = []
    item_files: List[str] = []

    for idx, bf in enumerate(split_batches, start=1):
        m = re.search(r"judge_batch_(\d+)", bf.name)
        j_id = m.group(1) if m else f"{idx:02d}"

        # Extract items for in-prompt payload
        items_payload: List[Dict[str, Any]] = []
        try:
            b_data = json.loads(bf.read_text(encoding="utf-8"))
            raw_items = b_data.get("items", []) if isinstance(b_data, dict) else (b_data if isinstance(b_data, list) else [])
            for item in raw_items:
                if isinstance(item, dict):
                    q_id = item.get("question_id") or item.get("item_id") or item.get("id")
                    cleaned_item = {
                        "question_id": q_id,
                        "item_id": item.get("item_id") or q_id,
                        "question_type": item.get("question_type") or item.get("interaction_type") or "multiple_choice",
                        "stem_es": item.get("stem_es") or item.get("stem") or "",
                        "options": item.get("options") or item.get("choices") or [],
                    }
                    if "answer_contract" in item:
                        cleaned_item["answer_contract"] = item["answer_contract"]
                    items_payload.append(cleaned_item)
        except Exception as e:
            logger.warning("Could not read judge batch %s: %s", bf, e)

        items_json_str = json.dumps(items_payload, indent=2, ensure_ascii=False)

        prompt_lines = [
            f"# Asignación de Evaluación a Ciegas para Blind Judge: `{j_id}`",
            "",
            "## 1. PROTOCOLO ZERO-WARMUP EN 1 SOLO TURNO (OBLIGATORIO)",
            f"- **Lote Asignado:** `{bf.name}`",
            f"- **Archivo de Respuestas de Salida:** `{work_rel}/verification/judge_responses_{j_id}.json`",
            "- READ permitido:",
            "  - Items inyectados en este prompt",
            f"- WRITE permitido:",
            f"  - {work_rel}/verification/judge_responses_{j_id}.json",
            "- PROHIBIDO:",
            "  - judge_ground_truth.json",
            "  - templates/*",
            "  - engine/*",
            "  - search_web",
            "  - read_url_content",
            "- **NO EJECUTES `view_file` para leer el archivo de lote:** Todos los reactivos ya están inyectados abajo.",
            "- **NO EJECUTES `run_command`:** Resuelve analíticamente desde primeros principios.",
            "- **Completa tu tarea en 1 SOLO TURNO** escribiendo directamente el archivo de respuestas con `write_to_file`.",
            f"- Cierra estrictamente con: `DONE: {work_rel}/verification/judge_responses_{j_id}.json`.",
            "",
            "## 2. ÍTEMS A EVALUAR (ZERO-WARMUP IN-PROMPT PAYLOAD)",
            "```json",
            items_json_str,
            "```",
            "",
            "---",
            "",
            sys_prompt_full,
        ]
        prompt_full = "\n".join(prompt_lines)

        item_file = items_dir / f"judge_{idx:02d}.json"
        item_data = {
            "TypeName": "c2c_judge",
            "Role": f"Blind Judge {j_id}",
            "Model": "flash",
            "Workspace": "inherit",
            "Prompt": prompt_full,
        }
        item_file.write_text(json.dumps(item_data, indent=2, ensure_ascii=False), encoding="utf-8")
        subagents.append(item_data)
        item_files.append(item_file.resolve().as_posix())

    dispatch_dir = work / "dispatch"
    dispatch_dir.mkdir(parents=True, exist_ok=True)
    judges_audit_file = dispatch_dir / "judges.json"
    judges_audit = {
        "stage": "judges",
        "dispatched_at": datetime.now(timezone.utc).isoformat(),
        "subagents_count": len(subagents),
        "item_files": item_files,
        "Subagents": subagents,
    }
    judges_audit_file.write_text(json.dumps(judges_audit, indent=2, ensure_ascii=False), encoding="utf-8")

    judge_compat_file = dispatch_dir / "judge.json"
    judge_compat_file.write_text(json.dumps(judges_audit, indent=2, ensure_ascii=False), encoding="utf-8")

    return {"Subagents": subagents, "item_files": item_files}


def build_dispatch(
    role: str,
    work_dir: Union[str, Path],
    ids: Optional[List[Union[str, int]]] = None,
    ready_only: bool = False,
) -> Dict[str, Any]:
    """Generates invoke_subagent payload with strict SCOPE-LOCK for the given role."""
    if role in ("vision", "vision-legacy"):
        raise ValueError(f"Stages 'vision' and 'vision-legacy' have been removed in C2C v3.2. Use Direct PDF Ingestion instead.")

    if role in ("cta", "cta-direct", "cta-map", "c2c_cta_architect"):
        mode = "mapreduce" if role == "cta-map" else None
        return dispatch_cta(work_dir, mode=mode)

    if role in ("author", "authors", "c2c_shard_author"):
        return dispatch_authors(work_dir)

    if role in ("judge", "judges", "c2c_judge"):
        return dispatch_judges(work_dir)

    if role not in ROLE_SPECS:
        raise ValueError(f"Unknown role: '{role}'. Available roles: {list(ROLE_SPECS.keys())}")

    work = Path(work_dir).resolve()
    work_rel = get_work_rel(work_dir)
    spec = ROLE_SPECS[role]
    sys_prompt = spec["system_prompt"]
    turn_budget = spec["turn_budget"]
    forbidden = list(spec["forbidden"])

    dispatch_dir = work / "dispatch"
    dispatch_dir.mkdir(parents=True, exist_ok=True)
    state_file = dispatch_dir / "state.json"

    state: Dict[str, Any] = {"dispatched": {}}
    if state_file.is_file():
        try:
            state = json.loads(state_file.read_text(encoding="utf-8"))
        except Exception as e:
            logger.warning("Could not read dispatch state: %s", e)

    dispatched_ids: List[str] = state.get("dispatched", {}).get(role, [])
    subagents: List[Dict[str, Any]] = []

    # CTA-REDUCE
    if role == "cta-reduce":
        sys_text = load_system_prompt(sys_prompt)
        prompt_text = (
            f"# Asignación de Tarea para CTA Harmonizer\n\n"
            f"## SCOPE-LOCK (OBLIGATORIO)\n"
            f"- READ: `{work_rel}/cta_outline.json`, `{work_rel}/duplicate_candidates.json`\n"
            f"- WRITE: `{work_rel}/cta_harmonize.json`\n\n"
            f"{sys_text}\n\n"
            f"Termina estrictamente con: DONE: {work_rel}/cta_harmonize.json"
        )
        subagents.append({
            "TypeName": spec["type_name"],
            "Role": "CTA Harmonizer",
            "Model": spec["model"],
            "Prompt": prompt_text,
        })
        dispatched_ids.append("harmonizer")

    # REPAIR
    elif role == "repair":
        templates_report_file = work / "reports" / "templates_report.json"
        judge_report_file = work / "judge_report.json"
        failing_targets: Dict[str, Dict[str, Any]] = {}

        if templates_report_file.is_file():
            try:
                tr = json.loads(templates_report_file.read_text(encoding="utf-8"))
                for res in tr.get("results", []):
                    if res.get("status") == "fail":
                        cid = res.get("cid") or res.get("competency_id")
                        if cid:
                            failing_targets.setdefault(cid, {})["template_errors"] = res.get("errors", [])
            except Exception as e:
                logger.warning("Error reading templates_report.json: %s", e)

        if judge_report_file.is_file():
            try:
                jr = json.loads(judge_report_file.read_text(encoding="utf-8"))
                for disc in jr.get("disagreements", []):
                    cid = disc.get("cid") or disc.get("competency_id")
                    if cid:
                        failing_targets.setdefault(cid, {})["judge_disagreement"] = disc
            except Exception as e:
                logger.warning("Error reading judge_report.json: %s", e)

        shard_map: Dict[str, str] = {}
        for sf in sorted((work / "shards").glob("shard_*.json")):
            try:
                sdata = json.loads(sf.read_text(encoding="utf-8"))
                s_id = sdata.get("shard_id", sf.stem)
                for cid in sdata.get("competency_ids", []):
                    shard_map[cid] = s_id
            except Exception:
                pass

        if ids is not None:
            ids_str = {str(i) for i in ids}
            failing_targets = {cid: data for cid, data in failing_targets.items() if cid in ids_str}

        if not failing_targets and ids:
            for cid in ids:
                failing_targets[str(cid)] = {"manual_request": True}

        sys_text = load_system_prompt(sys_prompt)
        for cid, diag in failing_targets.items():
            shard_id = shard_map.get(cid, "shard_01")
            prompt_text = (
                f"# Asignación de Tarea para Targeted Repair Engineer: `{cid}`\n\n"
                f"## SCOPE-LOCK\n"
                f"- READ: `{work_rel}/shards/{shard_id}_data.py`, `{work_rel}/templates/{cid}.json`\n"
                f"- WRITE: `{work_rel}/shards/{shard_id}_data.py`\n\n"
                f"### Diagnóstico del Fallo:\n"
                f"```json\n{json.dumps(diag, indent=2, ensure_ascii=False)}\n```\n\n"
                f"{sys_text}\n\n"
                f"Corrige la tupla en `{work_rel}/shards/{shard_id}_data.py` con `replace_file_content` y ejecuta compile_shard.py.\n"
                f"Termina estrictamente con: DONE: {work_rel}/shards/{shard_id}_data.py"
            )
            subagents.append({
                "TypeName": spec["type_name"],
                "Role": f"Repair Engineer {cid}",
                "Model": spec["model"],
                "Prompt": prompt_text,
            })
            dispatched_ids.append(cid)

    payload = {"Subagents": subagents}

    snap = snapshot_work_dir(work)
    snap_file = dispatch_dir / f"{role}_snapshot.json"
    snap_payload = {k: list(v) for k, v in snap.items()}
    snap_file.write_text(json.dumps(snap_payload, indent=2, ensure_ascii=False), encoding="utf-8")

    audit_file = dispatch_dir / f"{role}.json"
    audit_payload = {
        "role": role,
        "dispatched_at": datetime.now(timezone.utc).isoformat(),
        "subagents_count": len(subagents),
        "Subagents": subagents,
    }
    audit_file.write_text(json.dumps(audit_payload, indent=2, ensure_ascii=False), encoding="utf-8")

    state.setdefault("dispatched", {})[role] = list(sorted(set(dispatched_ids)))
    state_file.write_text(json.dumps(state, indent=2, ensure_ascii=False), encoding="utf-8")

    return payload


def snapshot_work_dir(work_dir: Union[str, Path]) -> Dict[str, Tuple[int, float]]:
    """Takes a snapshot of all files and their sizes/mtimes in work_dir."""
    work = Path(work_dir).resolve()
    snapshot: Dict[str, Tuple[int, float]] = {}
    if not work.is_dir():
        return snapshot

    for root, _, files in os.walk(work):
        root_path = Path(root)
        for fname in files:
            fpath = root_path / fname
            try:
                st = fpath.stat()
                rel = fpath.relative_to(work).as_posix()
                snapshot[rel] = (st.st_size, st.st_mtime)
            except OSError:
                pass
    return snapshot


def _is_allowed_path(rel_path: str, role: str) -> bool:
    """Checks whether rel_path is an allowed write destination for the specified role."""
    norm = rel_path.replace("\\", "/").lstrip("/")

    if (
        norm.startswith("dispatch/")
        or norm.startswith("work/dispatch/")
        or norm in ("timings.json", "work/timings.json", "order.json", "work/order.json")
        or norm.startswith("__pycache__/")
        or norm.startswith(".pytest_cache/")
        or norm.startswith(".git/")
    ):
        return True

    spec = ROLE_SPECS.get(role)
    if not spec:
        return False

    write_patterns = spec.get("write", [])
    candidates = [norm]
    if norm.startswith("work/"):
        candidates.append(norm[5:])
    else:
        candidates.append(f"work/{norm}")

    for pattern in write_patterns:
        pat_clean = pattern.replace("\\", "/").lstrip("/")
        pat_candidates = [pat_clean]
        if pat_clean.startswith("work/"):
            pat_candidates.append(pat_clean[5:])
        else:
            pat_candidates.append(f"work/{pat_clean}")

        for cand in candidates:
            for pat in pat_candidates:
                if fnmatch.fnmatch(cand, pat):
                    return True
                wildcard_pat = re.sub(r"<[^>]+>", "*", pat)
                wildcard_pat = re.sub(r"_XX\b", "_*", wildcard_pat)
                wildcard_pat = re.sub(r"XX\b", "*", wildcard_pat)
                if fnmatch.fnmatch(cand, wildcard_pat):
                    return True

    return False


def scope_check(
    work_dir: Union[str, Path],
    role: str,
    snapshot: Optional[Dict[str, Tuple[int, float]]] = None,
) -> Tuple[bool, List[str]]:
    """Detects files created or modified outside the permitted write paths for role."""
    work = Path(work_dir).resolve()
    if not snapshot:
        snap_file = work / "dispatch" / f"{role}_snapshot.json"
        if snap_file.is_file():
            try:
                raw_snap = json.loads(snap_file.read_text(encoding="utf-8"))
                snapshot = {k: (v[0], v[1]) for k, v in raw_snap.items()}
            except Exception as e:
                logger.warning("Could not load snapshot file %s: %s", snap_file, e)
    if snapshot is None:
        snapshot = {}

    current_snapshot = snapshot_work_dir(work)
    violations: List[str] = []

    for rel_path, (size, mtime) in current_snapshot.items():
        if rel_path not in snapshot:
            if not _is_allowed_path(rel_path, role):
                violations.append(rel_path)
        else:
            old_size, old_mtime = snapshot[rel_path]
            if (size, mtime) != (old_size, old_mtime):
                if not _is_allowed_path(rel_path, role):
                    violations.append(rel_path)

    violations.sort()
    is_clean = len(violations) == 0
    return is_clean, violations


def main() -> None:
    """CLI utility for subagent dispatch and scope checking."""
    parser = argparse.ArgumentParser(description="Subagent Scope-Lock & Dispatch Generator (C2C v3.2)")
    subparsers = parser.add_subparsers(dest="action", required=True)

    # dispatch subcommand
    disp = subparsers.add_parser("build", help="Generate invoke_subagent payload for role")
    disp.add_argument("--role", required=True, choices=list(ROLE_SPECS.keys()), help="Subagent role")
    disp.add_argument("--work-dir", required=True, help="Course working directory")
    disp.add_argument("--ready-only", action="store_true", help="Dispatch only ready sections")
    disp.add_argument("--ids", nargs="*", help="Optional specific IDs to dispatch")

    # check subcommand
    chk = subparsers.add_parser("check", help="Run scope violation check")
    chk.add_argument("--role", required=True, choices=list(ROLE_SPECS.keys()), help="Subagent role")
    chk.add_argument("--work-dir", required=True, help="Course working directory")

    # define-types subcommand
    dt = subparsers.add_parser("define-types", help="Print and persist define_subagent payloads for all c2c types")
    dt.add_argument("--work-dir", default=None, help="Optional course working directory to persist type files")

    # dispatch-cta subcommand
    dc = subparsers.add_parser("dispatch-cta", help="Dispatch CTA Architect using pre_cta_manifest.json")
    dc.add_argument("--work-dir", required=True, help="Course working directory")
    dc.add_argument("--mode", default=None, help="CTA mode: direct or mapreduce")

    # dispatch-authors subcommand
    da = subparsers.add_parser("dispatch-authors", help="Dispatch Shard Authors using pre_shard_manifest.json")
    da.add_argument("--work-dir", required=True, help="Course working directory")

    # dispatch-judges subcommand
    dj = subparsers.add_parser("dispatch-judges", help="Dispatch Blind Judges with Zero-Warmup in-prompt payload")
    dj.add_argument("--work-dir", required=True, help="Course working directory")

    args = parser.parse_args()

    if args.action == "define-types":
        target_work = args.work_dir or Path.cwd() / "work"
        res = generate_define_subagent_specs(target_work)
        print(json.dumps(res, indent=2, ensure_ascii=False))

    elif args.action == "dispatch-cta":
        res = dispatch_cta(args.work_dir, mode=args.mode)
        print(json.dumps(res, indent=2, ensure_ascii=False))

    elif args.action == "dispatch-authors":
        res = dispatch_authors(args.work_dir)
        print(json.dumps(res, indent=2, ensure_ascii=False))

    elif args.action == "dispatch-judges":
        res = dispatch_judges(args.work_dir)
        print(json.dumps(res, indent=2, ensure_ascii=False))

    elif args.action == "build":
        payload = build_dispatch(
            role=args.role,
            work_dir=args.work_dir,
            ids=args.ids,
            ready_only=args.ready_only,
        )
        print(json.dumps(payload, indent=2, ensure_ascii=False))

    elif args.action == "check":
        is_clean, violations = scope_check(args.work_dir, args.role, None)
        if is_clean:
            print(f"[+] Scope-check PASSED for role '{args.role}'.")
            sys.exit(0)
        else:
            print(f"[-] Scope-check FAILED for role '{args.role}'. {len(violations)} violations detected:")
            for v in violations:
                print(f"    * {v}")
            sys.exit(1)


if __name__ == "__main__":
    main()
