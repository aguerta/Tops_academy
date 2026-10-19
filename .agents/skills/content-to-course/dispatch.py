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


def load_system_prompt(name_or_path: Union[str, Path], lean: bool = False) -> str:
    """Loads a system prompt markdown file.
    
    When lean=True (or C2C_LEAN_PROMPTS=1 env var is set), loads the lean static
    system prompt (<= 5 KB) containing role and hard rules from system_prompts/lean/.
    Otherwise loads the uncompressed prompt.
    """
    use_lean = lean or os.getenv("C2C_LEAN_PROMPTS", "").lower() in ("1", "true", "yes")
    p = Path(name_or_path)
    if not p.is_absolute():
        candidates = []
        if use_lean:
            candidates.extend([
                SKILL_DIR / "system_prompts" / "lean" / p.name,
                SKILL_DIR / "system_prompts" / f"{p.stem}_lean{p.suffix}",
            ])
        candidates.extend([
            SKILL_DIR / "system_prompts" / p.name,
            SKILL_DIR / p,
            Path.cwd() / p,
        ])
        for c in candidates:
            if c.is_file():
                return c.read_text(encoding="utf-8")
        raise FileNotFoundError(f"System prompt file not found: {name_or_path}")
    if not p.is_file():
        raise FileNotFoundError(f"System prompt file not found: {p}")
    return p.read_text(encoding="utf-8")


def get_type_definitions(lean: bool = False) -> List[Dict[str, Any]]:
    """Returns subagent type definitions for define_subagent registration.
    
    When lean=True, loads lean static system prompts strictly under 5 KB.
    """
    repair_prompt = "prompt_repair.md" if lean else "prompt_shard_author.md"
    return [
        {
            "name": "c2c_cta_architect",
            "description": "Cognitive Task Analysis Curriculum Architect for C2C v3.2 (pure positional tuples in cta_data.py)",
            "system_prompt": load_system_prompt("prompt_cta_architect.md", lean=lean),
            "enable_write_tools": True,
            "enable_subagent_tools": False,
            "enable_mcp_tools": False,
        },
        {
            "name": "c2c_shard_author",
            "description": "Shard Exercise Author for native Python parametric templates and compile_shard.py",
            "system_prompt": load_system_prompt("prompt_shard_author.md", lean=lean),
            "enable_write_tools": True,
            "enable_subagent_tools": False,
            "enable_mcp_tools": False,
        },
        {
            "name": "c2c_judge",
            "description": "Independent Blind Psychometric Evaluation Judge with Zero-Warmup in-prompt resolution",
            "system_prompt": load_system_prompt("prompt_blind_judge.md", lean=lean),
            "enable_write_tools": True,
            "enable_subagent_tools": False,
            "enable_mcp_tools": False,
        },
        {
            "name": "c2c_repair",
            "description": "Targeted Quality Repair Engineer for fixing failing templates or discordances",
            "system_prompt": load_system_prompt(repair_prompt, lean=lean),
            "enable_write_tools": True,
            "enable_subagent_tools": False,
            "enable_mcp_tools": False,
        },
    ]


def make_pointer_prompt(
    role_name: str = "",
    work_order_rel: str = "",
    done_signal: Optional[str] = None,
    extra_instructions: Optional[str] = None,
    role: Optional[str] = None,
    item_file_rel: Optional[str] = None,
) -> str:
    """Generates an ultra-compact pointer prompt (~150-250 bytes, strictly <= 300 bytes) referencing disk JSON payload.
    
    Under the Pointer-Prompt Protocol (R5 / P4), the Director never types large work orders
    into invoke_subagent.Prompt. Instead, a compact pointer references the disk JSON payload.
    """
    r_name = role or role_name
    w_rel = item_file_rel or work_order_rel
    parts = [
        f"You are {r_name}.",
        f"Your work order is `{w_rel}`. Read it first with `view_file`, then follow your system prompt.",
    ]
    if extra_instructions:
        parts.append(extra_instructions)
    if done_signal:
        parts.append(f"Finalize strictly with: `{done_signal}`.")
    prompt_str = " ".join(parts)
    return prompt_str


ROLE_SPECS: Dict[str, Dict[str, Any]] = {
    "cta": {
        "type_name": "c2c_cta_architect",
        "model": "flash",
        "system_prompt": "system_prompts/prompt_cta_architect.md",
        "read": [
            "work/ingestion_manifest.json",
            "work/pre_cta_manifest.json",
            "work/cta_data.py",
            "work/cta_parts/**",
            "work/cta/**",
            "work/cta.json",
            "content/**",
        ],
        "write": [
            "work/cta_data.py",
            "work/cta.json",
            "work/cta.md",
            "work/cta_parts/**",
            "work/cta/**",
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
            "work/ingestion_manifest.json",
            "work/pre_cta_manifest.json",
            "work/cta_data.py",
            "work/cta_parts/**",
            "work/cta/**",
            "work/cta.json",
            "content/**",
        ],
        "write": [
            "work/cta_data.py",
            "work/cta.json",
            "work/cta.md",
            "work/cta_parts/**",
            "work/cta/**",
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
            "work/shards/*.json",
            "work/templates/*.json",
        ],
        "forbidden": [
            "scratch/**",
            "work/scratch/**",
            "engine/*",
            "SKILL.md",
            ".check_attempts/**",
            ".agents/skills/content-to-course/check_templates.py",
            ".agents/skills/content-to-course/check_cta.py",
            "src/validator/**",
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
            "work/judges/judge_*.json",
            "work/judges/*.json",
            "work/judges/**",
        ],
        "forbidden": [
            "judge_ground_truth.json",
            "work/templates/*",
            "templates/*",
            "engine/*",
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
            ".agents/skills/content-to-course/compile_shard.py",
            "work/cta.json",
        ],
        "write": [
            "work/shards/*_data.py",
            "work/shards/*.json",
            "work/templates/*.json",
        ],
        "forbidden": [
            "engine/*",
            "SKILL.md",
            ".agents/skills/content-to-course/check_templates.py",
            ".agents/skills/content-to-course/check_cta.py",
            "src/validator/**",
        ],
        "turn_budget": 15,
    },
    "cta-map": {
        "type_name": "c2c_cta_architect",
        "model": "flash",
        "system_prompt": "system_prompts/prompt_cta_architect.md",
        "read": [
            "work/parts/part_*/**",
            "work/parts/part_manifest_*.json",
            "work/pre_cta_manifest.json",
            "work/ingestion_manifest.json",
        ],
        "write": [
            "work/cta_parts/part_*.py",
            "work/cta_parts/cta_part_*.json",
            "work/cta/cta_shard_*_data.py",
            "work/cta/cta_shard_*.json",
        ],
        "forbidden": [
            "código fuente",
            "SKILL.md",
        ],
        "turn_budget": 15,
    },
    "cta-reduce": {
        "type_name": "c2c_cta_harmonizer",
        "model": "flash",
        "system_prompt": "system_prompts/prompt_cta_harmonizer.md",
        "read": [
            "work/cta_outline.json",
            "work/duplicate_candidates.json",
            "work/cta_parts/*.json",
            "work/cta/cta_shard_*.json",
        ],
        "write": [
            "work/cta_harmonize.json",
            "work/cta.json",
            "work/cta.md",
        ],
        "forbidden": [
            "código fuente",
            "SKILL.md",
        ],
        "turn_budget": 10,
    },
}


def build_scope_header(
    role: str,
    read_paths: Optional[List[str]] = None,
    write_paths: Optional[List[str]] = None,
    forbidden_paths: Optional[List[str]] = None,
    done_signal: Optional[str] = None,
) -> str:
    """Builds a standardized Markdown Scope-Lock header with allowed/forbidden paths and DONE signal."""
    spec = ROLE_SPECS.get(role, {})
    r_paths = read_paths if read_paths is not None else spec.get("read", [])
    w_paths = write_paths if write_paths is not None else spec.get("write", [])
    f_paths = forbidden_paths if forbidden_paths is not None else spec.get("forbidden", [])

    lines = [
        "## 0. SCOPE-LOCK Y CONTRATO DE EJECUCIÓN",
        f"- **Rol:** `{role}`",
        "- READ permitido:",
    ]
    if r_paths:
        for p in r_paths:
            lines.append(f"  - `{p}`")
    else:
        lines.append("  - (Ninguno adicional fuera de este prompt)")

    lines.append("- WRITE permitido:")
    if w_paths:
        for p in w_paths:
            lines.append(f"  - `{p}`")
    else:
        lines.append("  - (Ninguno)")

    lines.append("- PROHIBIDO:")
    if f_paths:
        for p in f_paths:
            lines.append(f"  - `{p}`")
    else:
        lines.append("  - Modificar archivos fuera de las rutas de WRITE permitidas")

    if done_signal:
        lines.append(f"- **SEÑAL DE FINALIZACIÓN:** Responder estrictamente con `{done_signal}` al completar.")

    return "\n".join(lines)


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


def generate_define_subagent_specs(work_dir: Union[str, Path], lean: bool = False) -> Dict[str, Any]:
    """Writes individual subagent type spec files in work/dispatch/types/<type_name>.json
    and the consolidated index in work/dispatch/subagent_types.json.
    
    When lean=True, persists lean static system prompts strictly <= 5 KB.
    """
    work = Path(work_dir).resolve()
    types_dir = work / "dispatch" / "types"
    types_dir.mkdir(parents=True, exist_ok=True)

    types_list = list(get_type_definitions(lean=lean))
    type_files: List[str] = []

    for t_spec in types_list:
        t_name = t_spec["name"]
        clean_name = t_name.replace("-", "_")
        t_file = types_dir / f"{clean_name}.json"
        t_file.write_text(json.dumps(t_spec, indent=2, ensure_ascii=False), encoding="utf-8")
        type_files.append(t_file.resolve().as_posix())

    # Auxiliary type definition: c2c_cta_harmonizer for cta-reduce
    try:
        harmonizer_prompt = load_system_prompt("prompt_cta_harmonizer.md", lean=lean)
        harmonizer_spec = {
            "name": "c2c_cta_harmonizer",
            "description": "Cognitive Task Analysis Harmonizer for deduplicating and merging sectional CTA parts",
            "system_prompt": harmonizer_prompt,
            "enable_write_tools": True,
            "enable_subagent_tools": False,
            "enable_mcp_tools": False,
        }
        h_file = types_dir / "c2c_cta_harmonizer.json"
        h_file.write_text(json.dumps(harmonizer_spec, indent=2, ensure_ascii=False), encoding="utf-8")
        type_files.append(h_file.resolve().as_posix())
    except Exception as e:
        logger.warning("Could not write c2c_cta_harmonizer.json: %s", e)

    summary_payload = {
        "types": types_list,
        "type_files": type_files,
    }

    subagent_types_file = work / "dispatch" / "subagent_types.json"
    subagent_types_file.parent.mkdir(parents=True, exist_ok=True)
    subagent_types_file.write_text(json.dumps(summary_payload, indent=2, ensure_ascii=False), encoding="utf-8")

    return summary_payload


def dispatch_cta(
    work_dir: Union[str, Path],
    mode: Optional[str] = None,
    pointer: bool = False,
) -> Dict[str, Any]:
    """Generates dispatch payload and individual item files for CTA Architect (Load Inversion v3.21).
    
    Exige pre_cta_manifest.json o ingestion_manifest.json (cero fallbacks; si no existe, lanza BLOCKER).
    En modo direct y mapreduce: genera ítems concisos (< 2,500 caracteres) en work/dispatch/items/cta_XX.json
    sin duplicar el system prompt, inyectando tabla de documentos, rangos físicos 1..N y contrato compile_cta.py.
    When pointer=True, generates ultra-compact (~200 B) pointer prompts in the ready-made Subagents array.
    """
    work = Path(work_dir).resolve()
    work_rel = get_work_rel(work)
    use_pointer = pointer or os.getenv("C2C_POINTER_PROMPTS", "").lower() in ("1", "true", "yes")
    manifest_path = work / "pre_cta_manifest.json"
    if not manifest_path.is_file():
        alt_m = work / "ingestion_manifest.json"
        if alt_m.is_file():
            manifest_path = alt_m
        else:
            err_msg = "BLOCKER:: No existe pre_cta_manifest.json"
            logger.error(err_msg)
            raise FileNotFoundError(err_msg)

    manifest_data = json.loads(manifest_path.read_text(encoding="utf-8"))
    cta_mode = mode or manifest_data.get("cta_mode") or manifest_data.get("mode") or "direct"
    granularity = manifest_data.get("granularity", "standard")
    manifest_rel = f"{work_rel}/ingestion_manifest.json" if (work / "ingestion_manifest.json").is_file() else f"{work_rel}/pre_cta_manifest.json"

    total_physical_pages = manifest_data.get("total_pages")
    if total_physical_pages is None:
        raw_files = manifest_data.get("documents") or manifest_data.get("files") or []
        total_physical_pages = sum(f.get("total_pages", 0) for f in raw_files if isinstance(f, dict)) or 1

    items_dir = work / "dispatch" / "items"
    items_dir.mkdir(parents=True, exist_ok=True)

    subagents: List[Dict[str, Any]] = []
    item_files: List[str] = []

    if cta_mode == "mapreduce":
        subparts = manifest_data.get("subparts") or manifest_data.get("parts") or []
        if not subparts:
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

        # Swift-Dispatch SLA: Order subparts heaviest partition first
        subparts = sorted(
            subparts,
            key=lambda sp: sp.get("total_pages") or sp.get("slide_count") or sp.get("pages") or ((sp.get("page_range") or [1, 1])[1] - (sp.get("page_range") or [1, 1])[0] + 1),
            reverse=True,
        )

        for idx, sp in enumerate(subparts, start=1):
            part_idx = sp.get("part_index") or idx
            subpart_id = sp.get("subpart_id") or f"part_{part_idx:02d}"
            doc_name = sp.get("doc") or sp.get("doc_name") or sp.get("name") or "document.pdf"
            doc_path = sp.get("path") or sp.get("file") or doc_name
            c_type = sp.get("content_type") or sp.get("type") or "pdf"
            v_range = sp.get("page_range") or sp.get("valid_page_range") or [1, sp.get("total_pages", 1)]
            s_p = v_range[0] if len(v_range) > 0 else 1
            e_p = v_range[1] if len(v_range) > 1 else s_p
            total_p = sp.get("total_pages") or (e_p - s_p + 1)
            t_ref = sp.get("slice_path") or sp.get("text_ref") or sp.get("page_index_path") or sp.get("pages_dir") or doc_path
            if not t_ref or not doc_path:
                raise RuntimeError(f"BLOCKER:: Missing source path or slice for subpart {subpart_id}")

            out_py = f"{work_rel}/cta/cta_shard_{idx:02d}_data.py" if "cta_shard" in subpart_id else f"{work_rel}/cta_parts/{subpart_id}_data.py"
            json_target = f"{work_rel}/cta/cta_shard_{idx:02d}.json" if "cta_shard" in subpart_id else f"{work_rel}/cta_parts/{subpart_id}.json"

            subpart_table = "\n".join([
                "| Documento Subpart | Ruta Fuente | Tipo | Rango Físico (1..N) | Páginas | Referencia Texto |",
                "|---|---|---|---|---|---|",
                f"| `{doc_name}` | `{doc_path}` | `{c_type}` | **`{s_p}..{e_p}`** | {total_p} | `{t_ref}` |",
            ])

            compile_cmd = f"python .agents/skills/content-to-course/compile_cta.py --input {out_py} --output {json_target} --manifest {manifest_rel} --part {subpart_id}"
            read_paths = list(dict.fromkeys([manifest_rel, doc_path, t_ref]))
            scope_header = build_scope_header(
                role="cta-map",
                read_paths=read_paths,
                write_paths=[out_py, json_target],
                done_signal=f"DONE: {json_target}",
            )

            prompt_lines = [
                f"# Asignación de Tarea: Cognitive Task Analysis Architect ({subpart_id} - MapReduce C2C v3.21)",
                "",
                scope_header,
                "",
                "## 1. PARÁMETROS DE LA SUBPARTE",
                f"- **Manifest:** `{manifest_rel}`",
                f"- **CTA Mode:** `mapreduce` (Subpart: `{subpart_id}`)",
                f"- **Granularity:** `{granularity}`",
                f"- **Total Physical Pages:** {total_physical_pages}",
                f"- **Archivo Python de Salida:** `{out_py}`",
                f"- **Destino JSON Final:** `{json_target}`",
                "",
                "## 2. DOCUMENTO ASIGNADO A ESTA SUBPARTE Y RANGO DE PÁGINAS (1..N)",
                subpart_table,
                "",
                "> [!CRITICAL]",
                "> **REGLA MANDATORIA DE PAGINACIÓN `evidence.page`:**",
                f"> SIEMPRE usa el índice de página 1-indexed del archivo PDF (`{s_p}..{e_p}` según la tabla anterior), NUNCA la numeración impresa del libro o capítulo.",
                "",
                "## 3. DIRECTIVAS DE OPERACIÓN",
                f"1. Abre el material fuente asignado con `view_file`: `{doc_path}`.",
                f"2. Escribe las competencias en tuplas tabulares puras de 9 elementos en `{out_py}` (`COMPETENCIES = [...]`).",
                f"3. Ejecuta la compilación oficial determinista:",
                f"   ```bash",
                f"   {compile_cmd}",
                f"   ```",
                f"4. Si el compilador reporta errores, corrígelos quirúrgicamente con `replace_file_content` sobre `{out_py}`.",
                f"5. Sigue estrictamente todas las reglas de tu System Prompt `c2c_cta_architect` y finaliza con: `DONE: {json_target}`.",
            ]
            prompt_full = "\n".join(prompt_lines)

            item_file = items_dir / f"cta_{idx:02d}.json"
            item_data = {
                "TypeName": "c2c_cta_architect",
                "Role": f"Cognitive Task Analysis Architect {subpart_id}",
                "Model": "flash",
                "Workspace": "inherit",
                "Prompt": prompt_full,
                "work_order": prompt_full,
                "subpart_id": subpart_id,
                "output_python": out_py,
                "output_json": json_target,
            }
            item_file.write_text(json.dumps(item_data, indent=2, ensure_ascii=False), encoding="utf-8")

            if use_pointer:
                pointer_prompt = make_pointer_prompt(
                    role_name=f"Cognitive Task Analysis Architect {subpart_id}",
                    work_order_rel=f"{work_rel}/dispatch/items/{item_file.name}",
                    done_signal=f"DONE: {json_target}",
                )
                subagent_item = {
                    "TypeName": "c2c_cta_architect",
                    "Role": f"Cognitive Task Analysis Architect {subpart_id}",
                    "Model": "flash",
                    "Prompt": pointer_prompt,
                }
            else:
                subagent_item = item_data

            subagents.append(subagent_item)
            item_files.append(item_file.resolve().as_posix())

    else:
        # direct mode
        out_target = f"{work_rel}/cta_data.py"
        json_target = f"{work_rel}/cta.json"

        docs = manifest_data.get("documents") or manifest_data.get("files") or []
        doc_rows: List[Tuple[str, str, str, str, Any, str]] = []
        if isinstance(docs, list):
            for d in docs:
                if isinstance(d, dict):
                    d_name = d.get("doc_name") or d.get("name") or d.get("doc") or "document.pdf"
                    d_path = d.get("path") or d.get("file") or d_name
                    c_type = d.get("content_type") or d.get("type") or "pdf"
                    v_range = d.get("valid_page_range") or d.get("page_range") or [1, d.get("total_pages", 1)]
                    s_p = v_range[0] if len(v_range) > 0 else 1
                    e_p = v_range[1] if len(v_range) > 1 else s_p
                    tot = d.get("total_pages") or (e_p - s_p + 1)
                    t_ref = d.get("slice_path") or d.get("text_ref") or d.get("page_index_path") or d.get("pages_dir") or d_path
                    if not t_ref or not d_path:
                        raise RuntimeError(f"BLOCKER:: Missing source path or slice for document {d_name}")
                    doc_rows.append((d_name, d_path, c_type, f"{s_p}..{e_p}", tot, t_ref))
                elif isinstance(d, str):
                    doc_rows.append((d, d, "pdf", "1..N", "desconocido", d))
        elif isinstance(docs, dict):
            for d_name, d_info in docs.items():
                if isinstance(d_info, dict):
                    c_type = d_info.get("content_type") or d_info.get("type") or "pdf"
                    v_range = d_info.get("valid_page_range") or d_info.get("page_range") or [1, d_info.get("total_pages", 1)]
                    s_p = v_range[0] if len(v_range) > 0 else 1
                    e_p = v_range[1] if len(v_range) > 1 else s_p
                    tot = d_info.get("total_pages") or (e_p - s_p + 1)
                    d_path = d_info.get("path") or d_name
                    t_ref = d_info.get("slice_path") or d_info.get("text_ref") or d_info.get("page_index_path") or d_info.get("pages_dir") or d_path
                    if not t_ref or not d_path:
                        raise RuntimeError(f"BLOCKER:: Missing source path or slice for document {d_name}")
                    doc_rows.append((d_name, d_path, c_type, f"{s_p}..{e_p}", tot, t_ref))

        if len(doc_rows) > 10:
            table_lines = [
                "| # | Documento | Rango Físico (1..N) | Páginas |",
                "|---|---|---|---|",
            ]
            for i, r in enumerate(doc_rows, 1):
                table_lines.append(f"| {i} | `{r[0]}` | **`{r[3]}`** | {r[4]} |")
            doc_table_str = f"- **Total de documentos asignados:** {len(doc_rows)} archivos (ver `{manifest_rel}`).\n\n" + "\n".join(table_lines)
        else:
            table_lines = [
                "| Documento | Rango Físico (1..N) | Páginas | Referencia Texto |",
                "|---|---|---|---|",
            ]
            for r in doc_rows:
                table_lines.append(f"| `{r[0]}` | **`{r[3]}`** | {r[4]} | `{r[5]}` |")
            doc_table_str = "\n".join(table_lines)

        compile_cmd = f"python .agents/skills/content-to-course/compile_cta.py --input {out_target} --output {json_target} --manifest {manifest_rel}"
        scope_header = build_scope_header(
            role="cta",
            read_paths=[manifest_rel, "content/**"],
            write_paths=[out_target, json_target, f"{work_rel}/cta.md"],
            done_signal=f"DONE: {json_target}",
        )

        prompt_lines = [
            "# Asignación de Tarea: Cognitive Task Analysis Architect (C2C v3.21 Load Inversion)",
            "",
            scope_header,
            "",
            "## 1. PARÁMETROS DEL CURRÍCULO",
            f"- **Manifest:** `{manifest_rel}`",
            f"- **CTA Mode:** `{cta_mode}`",
            f"- **Granularity:** `{granularity}`",
            f"- **Total Physical Pages:** {total_physical_pages}",
            f"- **Archivo Python de Salida:** `{out_target}`",
            f"- **Destino JSON Final:** `{json_target}`",
            "",
            "## 2. DOCUMENTOS ASIGNADOS Y RANGOS DE PÁGINAS FÍSICAS (1..N)",
            doc_table_str,
            "",
            "> [!CRITICAL]",
            "> **REGLA MANDATORIA DE PAGINACIÓN `evidence.page`:**",
            "> SIEMPRE usa el índice de página 1-indexed del archivo PDF (`1..N` según la tabla anterior), NUNCA la numeración impresa del libro o capítulo.",
            "",
            "## 3. DIRECTIVAS DE OPERACIÓN",
            f"1. Abre el primer material fuente asignado con `view_file` para extraer conceptos, hechos y habilidades.",
            f"2. Escribe las competencias en tuplas tabulares puras de 9 elementos en `{out_target}` (`COMPETENCIES = [...]`).",
            f"3. Ejecuta la compilación oficial determinista:",
            f"   ```bash",
            f"   {compile_cmd}",
            f"   ```",
            f"4. Si el compilador reporta errores, corrígelos quirúrgicamente con `replace_file_content` sobre `{out_target}`.",
            f"5. Sigue estrictamente todas las reglas de tu System Prompt `c2c_cta_architect` y finaliza con: `DONE: {json_target}`.",
        ]
        prompt_full = "\n".join(prompt_lines)

        item_file = items_dir / "cta_01.json"
        item_data = {
            "TypeName": "c2c_cta_architect",
            "Role": "Cognitive Task Analysis Architect",
            "Model": "flash",
            "Workspace": "inherit",
            "Prompt": prompt_full,
            "work_order": prompt_full,
            "output_python": out_target,
            "output_json": json_target,
        }
        item_file.write_text(json.dumps(item_data, indent=2, ensure_ascii=False), encoding="utf-8")

        if use_pointer:
            pointer_prompt = make_pointer_prompt(
                role_name="Cognitive Task Analysis Architect",
                work_order_rel=f"{work_rel}/dispatch/items/{item_file.name}",
                done_signal=f"DONE: {json_target}",
            )
            subagents = [{
                "TypeName": "c2c_cta_architect",
                "Role": "Cognitive Task Analysis Architect",
                "Model": "flash",
                "Prompt": pointer_prompt,
            }]
        else:
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


def dispatch_authors(work_dir: Union[str, Path], pointer: bool = False) -> Dict[str, Any]:
    """Generates dispatch payload and individual item files for Shard Authors (Load Inversion v3.21).
    
    Exige work/shards/pre_shard_manifest.json y work/pre_cta_manifest.json (cero fallbacks).
    NO pre-siembra JSON en work/templates/ ni bundles en work/shards/bundles/.
    Inyecta especificación Turn-0 completa de competencias y 6 distractores (D-XX-01..06)
    directamente en el prompt conciso del autor, permitiendo autoría autónoma sin lectura de cta.json.
    When pointer=True, generates ultra-compact (~200 B) pointer prompts in the ready-made Subagents array,
    ordered heaviest unit first (Swift-Dispatch SLA).
    """
    work = Path(work_dir).resolve()
    work_rel = get_work_rel(work)
    use_pointer = pointer or os.getenv("C2C_POINTER_PROMPTS", "").lower() in ("1", "true", "yes")

    shard_manifest_path = work / "shards" / "pre_shard_manifest.json"
    if not shard_manifest_path.is_file():
        if (work / "pre_shard_manifest.json").is_file():
            shard_manifest_path = work / "pre_shard_manifest.json"
        else:
            err_msg = "BLOCKER:: No existe pre_shard_manifest.json"
            logger.error(err_msg)
            raise FileNotFoundError(err_msg)

    cta_manifest_path = work / "pre_cta_manifest.json"
    if not cta_manifest_path.is_file():
        if (work / "ingestion_manifest.json").is_file():
            cta_manifest_path = work / "ingestion_manifest.json"
        elif not (work / "cta.json").is_file():
            err_msg = "BLOCKER:: No existe pre_cta_manifest.json"
            logger.error(err_msg)
            raise FileNotFoundError(err_msg)

    manifest_rel = f"{work_rel}/ingestion_manifest.json" if (work / "ingestion_manifest.json").is_file() else f"{work_rel}/pre_cta_manifest.json"
    cta_rel = f"{work_rel}/cta.json"

    cta_file = work / "cta.json"
    cta_comps_by_id: Dict[str, Dict[str, Any]] = {}
    if cta_file.is_file():
        try:
            cta_data = json.loads(cta_file.read_text(encoding="utf-8"))
            raw_comps = cta_data.get("competencies", []) if isinstance(cta_data, dict) else (cta_data if isinstance(cta_data, list) else [])
            if isinstance(raw_comps, list):
                for c in raw_comps:
                    if isinstance(c, dict) and "id" in c:
                        cta_comps_by_id[c["id"]] = c
            elif isinstance(raw_comps, dict):
                for cid, c in raw_comps.items():
                    if isinstance(c, dict):
                        c_copy = dict(c)
                        c_copy.setdefault("id", cid)
                        cta_comps_by_id[cid] = c_copy
        except Exception as e:
            logger.warning("Could not read cta.json: %s", e)

    # Document map from pre_cta_manifest
    cta_manifest_data: Dict[str, Any] = {}
    if cta_manifest_path.is_file():
        try:
            cta_manifest_data = json.loads(cta_manifest_path.read_text(encoding="utf-8"))
        except Exception:
            pass
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
    manifest_comps_by_id: Dict[str, Dict[str, Any]] = {}
    shards_raw = shard_manifest_data.get("shards", [])
    if isinstance(shards_raw, dict):
        shard_list = [{"shard_id": k, "competency_ids": v} for k, v in shards_raw.items()]
    elif isinstance(shards_raw, list):
        shard_list = shards_raw
        for s_item in shard_list:
            if isinstance(s_item, dict):
                for c in s_item.get("competencies", []):
                    if isinstance(c, dict) and "id" in c:
                        manifest_comps_by_id[c["id"]] = c
    else:
        shard_list = []

    # Swift-Dispatch SLA: Sort shards heaviest unit first
    def _shard_weight(shard: Dict[str, Any]) -> int:
        if shard.get("estimated_questions"):
            return int(shard["estimated_questions"]) * 10
        c_ids = shard.get("competency_ids") or []
        if not c_ids and "competencies" in shard:
            raw_c = shard["competencies"]
            c_ids = [c["id"] if isinstance(c, dict) and "id" in c else str(c) for c in raw_c]
        w = 0
        for cid in c_ids:
            c_obj = cta_comps_by_id.get(cid) or manifest_comps_by_id.get(cid, {})
            t = str(c_obj.get("type", "knowledge")).lower()
            w += 30 if t in ("skill", "habilidad", "hab") else 20
        return w if w > 0 else (len(c_ids) * 20)

    shard_list = sorted(shard_list, key=_shard_weight, reverse=True)

    items_dir = work / "dispatch" / "items"
    items_dir.mkdir(parents=True, exist_ok=True)

    subagents: List[Dict[str, Any]] = []
    item_files: List[str] = []

    for idx, s in enumerate(shard_list, start=1):
        s_idx = s.get("shard_index") or idx
        s_id = s.get("shard_id") or f"shard_{s_idx:02d}"
        c_ids = s.get("competency_ids") or []
        if not c_ids and "competencies" in s:
            raw_c = s["competencies"]
            c_ids = [c["id"] if isinstance(c, dict) and "id" in c else str(c) for c in raw_c]

        out_py = f"{work_rel}/shards/{s_id}_data.py"
        target_json = f"{work_rel}/shards/{s_id}.json"

        # Structured Turn-0 specification for each assigned competency
        comp_blocks = []
        source_doc_set: Set[str] = set()

        for cid in c_ids:
            c_obj = cta_comps_by_id.get(cid) or manifest_comps_by_id.get(cid, {})
            c_name = c_obj.get("name", cid)
            raw_type = str(c_obj.get("type", "knowledge")).lower()
            if raw_type in ("skill", "habilidad", "hab"):
                comp_type = "skill"
                quota = 30
            else:
                comp_type = "knowledge"
                quota = 20

            desc_latex = c_obj.get("description_latex") or c_obj.get("description") or "(Definición pedagógica según fuentes del curso)"

            # Evidence
            ev_list = []
            raw_ev = c_obj.get("evidence", [])
            if isinstance(raw_ev, dict):
                raw_ev = [raw_ev]
            if isinstance(raw_ev, list):
                for ev in raw_ev:
                    if isinstance(ev, dict):
                        doc = ev.get("doc") or ev.get("document") or ""
                        sec = ev.get("section_heading") or ev.get("section") or ""
                        page = ev.get("page") or ev.get("page_or_slide") or ev.get("slide") or 1
                        resolved_doc = doc_paths_by_name.get(doc, doc)
                        if resolved_doc:
                            source_doc_set.add(resolved_doc)
                        ev_desc = f"`{resolved_doc or doc}` (pág. {page}" + (f", sección: '{sec}'" if sec else "") + ")"
                        ev_list.append(ev_desc)
            ev_str = "; ".join(ev_list) if ev_list else "Consultar material fuente en `content/`"

            # 6 Distractors D-XX-01..06
            raw_distractors = c_obj.get("distractors", [])
            d_lines = []
            if isinstance(raw_distractors, list):
                for d in raw_distractors:
                    if isinstance(d, dict):
                        did = d.get("id") or "D-XX"
                        dname = d.get("name") or did
                        dw = d.get("wrong_belief") or d.get("rationale") or "Creencia errónea no especificada"
                        d_omit = d.get("omitted_step") or "N/A"
                        d_warn = d.get("common_misconception_warning")
                        line_entry = f"    - **`{did}`** (`{dname}`): Creencia errónea: *\"{dw}\"* | Paso omitido: `{d_omit}`"
                        if d_warn:
                            line_entry += f" | Advertencia: *\"{d_warn}\"*"
                        d_lines.append(line_entry)
            if not d_lines:
                d_lines.append("    - *(Distractores no provistos en manifiesto; sintetizar 6 distractores canónicos D-XX-01..06)*")
            distractors_block = "\n".join(d_lines)

            block = (
                f"### Competencia: `{cid}`\n"
                f"- **Tipo:** `{comp_type}` (Cuota requerida: **{quota}** reactivos)\n"
                f"- **Nombre:** {c_name}\n"
                f"- **Descripción (LaTeX):** {desc_latex}\n"
                f"- **Evidencia Fuente:** {ev_str}\n"
                f"- **6 Distractores Canónicos (D-XX-01..06):**\n"
                f"{distractors_block}"
            )
            comp_blocks.append(block)

        source_doc_list = sorted(source_doc_set) if source_doc_set else ["content/**"]
        scope_header = build_scope_header(
            role="author",
            read_paths=source_doc_list + [".agents/skills/content-to-course/compile_shard.py"],
            write_paths=[out_py, target_json],
            forbidden_paths=[
                "scratch/**",
                "work/scratch/**",
                "engine/*",
                "SKILL.md",
                ".check_attempts/**",
                ".agents/skills/content-to-course/check_templates.py",
                ".agents/skills/content-to-course/check_cta.py",
                "src/validator/**",
            ],
            done_signal=f"DONE: {target_json}",
        )

        compile_cmd = f"python .agents/skills/content-to-course/compile_shard.py --input {out_py} --output {target_json} --cta {cta_rel} --manifest {manifest_rel}"

        prompt_lines = [
            f"# Asignación de Tarea: Shard Exercise Author `{s_id}` (C2C v3.21 Load Inversion)",
            "",
            scope_header,
            "",
            "## 1. ESPECIFICACIÓN DEL SHARD",
            f"- **Shard ID:** `{s_id}`",
            f"- **Manifest:** `{work_rel}/shards/pre_shard_manifest.json`",
            f"- **Archivo Python de Salida:** `{out_py}`",
            f"- **Destino JSON Final:** `{target_json}`",
            f"- **Documentos Fuente Asignados:**",
        ]
        for sdoc in source_doc_list:
            prompt_lines.append(f"  - `{sdoc}`")

        prompt_lines.extend([
            "",
            "## 2. ESPECIFICACIÓN TURN-0 COMPLETA DE COMPETENCIAS Y DISTRACTORES",
            "\n\n".join(comp_blocks),
            "",
            "## 3. INSTRUCCIONES DE EJECUCIÓN",
            f"1. Escribe ÚNICAMENTE las funciones generadoras/verificadoras y la lista de tuplas en `{out_py}` (`TEMPLATES = [...]`).",
            f"2. Utiliza estrictamente los 6 distractores canónicos definidos arriba para cada competencia.",
            f"3. Ejecuta la compilación oficial determinista:",
            f"   ```bash",
            f"   {compile_cmd}",
            f"   ```",
            f"4. Si el compilador reporta errores con línea exacta, corrígelos quirúrgicamente con `replace_file_content` sobre `{out_py}`.",
            f"5. Sigue todas las directivas de tu System Prompt `c2c_shard_author` y finaliza estrictamente con: `DONE: {target_json}`.",
        ])
        prompt_full = "\n".join(prompt_lines)

        item_file = items_dir / f"author_{idx:02d}.json"
        item_data = {
            "TypeName": "c2c_shard_author",
            "Role": f"Shard Author {s_id}",
            "Model": "flash",
            "Workspace": "inherit",
            "shard_id": s_id,
            "assigned_competencies": c_ids,
            "output_python": out_py,
            "output_json": target_json,
            "compile_command": compile_cmd,
            "Prompt": prompt_full,
            "work_order": prompt_full,
        }
        item_file.write_text(json.dumps(item_data, indent=2, ensure_ascii=False), encoding="utf-8")

        if use_pointer:
            pointer_prompt = make_pointer_prompt(
                role_name=f"Shard Author {s_id}",
                work_order_rel=f"{work_rel}/dispatch/items/{item_file.name}",
                done_signal=f"DONE: {target_json}",
            )
            subagent_item = {
                "TypeName": "c2c_shard_author",
                "Role": f"Shard Author {s_id}",
                "Model": "flash",
                "Prompt": pointer_prompt,
            }
        else:
            subagent_item = item_data

        subagents.append(subagent_item)
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


def dispatch_judges(
    work_dir: Union[str, Path],
    pointer: bool = False,
    max_items_per_judge: int = 12,
) -> Dict[str, Any]:
    """Generates dispatch payload and individual item files for Blind Judges (Load Inversion v3.21).
    
    Zero-Warmup In-Prompt payload: inyecta los ítems del batch (question_id, question_type, stem_es, options)
    directamente dentro del Prompt sin duplicar el system prompt.
    When pointer=True, generates ultra-compact (~200 B) pointer prompts in the ready-made Subagents array,
    enforcing native batch slicing <= 12 items per judge (Swift-Dispatch SLA).
    """
    work = Path(work_dir).resolve()
    work_rel = get_work_rel(work)
    use_pointer = pointer or os.getenv("C2C_POINTER_PROMPTS", "").lower() in ("1", "true", "yes")

    # Native Batch Slicing: ensure batches are sliced at <= max_items_per_judge (default 12)
    unsplit = work / "verification" / "judge_batch.json"
    if not unsplit.is_file():
        unsplit = work / "judge_batch.json"

    batch_files = sorted(work.glob("verification/judge_batch_*.json"))
    if not batch_files:
        batch_files = sorted(work.glob("judge_batch_*.json"))
    split_batches = [bf for bf in batch_files if bf.name not in ("judge_batch.json", "judge_redispatch_batch.json")]

    if not split_batches and not unsplit.is_file():
        shards_dir = work / "shards"
        shard_files = list(shards_dir.glob("shard_*.json")) if shards_dir.is_dir() else []
        if shard_files:
            extracted_items = []
            for sf in sorted(shard_files):
                try:
                    s_data = json.loads(sf.read_text(encoding="utf-8"))
                    if isinstance(s_data, list):
                        qs = s_data
                    elif isinstance(s_data, dict):
                        qs = s_data.get("questions") or s_data.get("items") or []
                    else:
                        qs = []
                    for q in qs:
                        if isinstance(q, dict):
                            b_item = {
                                "id": q.get("id") or q.get("question_id"),
                                "question_id": q.get("id") or q.get("question_id"),
                                "stem": q.get("prompt") or q.get("stem") or q.get("stem_es") or "",
                                "stem_es": q.get("prompt") or q.get("stem_es") or q.get("stem") or "",
                                "options": q.get("options") or q.get("distractors") or [],
                            }
                            extracted_items.append(b_item)
                except Exception as e:
                    logger.warning("Could not extract items from %s: %s", sf, e)
            if extracted_items:
                v_dir = work / "verification"
                v_dir.mkdir(parents=True, exist_ok=True)
                unsplit = v_dir / "judge_batch.json"
                unsplit.write_text(json.dumps(extracted_items, indent=2, ensure_ascii=False), encoding="utf-8")

    needs_split = False
    if not split_batches and unsplit.is_file():
        needs_split = True
    elif split_batches and max_items_per_judge > 0:
        for bf in split_batches:
            try:
                b_cnt = len(json.loads(bf.read_text(encoding="utf-8")))
                if b_cnt > max_items_per_judge:
                    needs_split = True
                    break
            except Exception:
                pass

    if needs_split and unsplit.is_file():
        from judge import split_judge_batch
        split_batches = split_judge_batch(work, max_judges=8, items_per_judge=max_items_per_judge)

    if not split_batches and unsplit.is_file():
        split_batches = [unsplit]

    # Swift-Dispatch SLA: Sort batches heaviest unit first
    def _batch_count(bf: Path) -> int:
        try:
            d = json.loads(bf.read_text(encoding="utf-8"))
            return len(d) if isinstance(d, list) else len(d.get("items", []))
        except Exception:
            return 0

    split_batches = sorted(split_batches, key=_batch_count, reverse=True)

    items_dir = work / "dispatch" / "items"
    items_dir.mkdir(parents=True, exist_ok=True)

    subagents: List[Dict[str, Any]] = []
    item_files: List[str] = []

    for idx, bf in enumerate(split_batches, start=1):
        m = re.search(r"judge_batch_(\d+)", bf.name)
        j_id = m.group(1) if m else f"{idx:02d}"

        # Extract items for in-prompt payload (strictly blind: zero ground truth)
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
                    if "graph" in item:
                        cleaned_item["graph"] = item["graph"]
                    items_payload.append(cleaned_item)
        except Exception as e:
            logger.warning("Could not read judge batch %s: %s", bf, e)

        items_json_str = json.dumps(items_payload, indent=2, ensure_ascii=False)

        j_tag = f"judge_{j_id}"
        out_target = f"{work_rel}/verification/judge_responses_{j_id}.json"
        alt_out_target = f"{work_rel}/judges/{j_tag}.json"

        scope_header = build_scope_header(
            role="judge",
            read_paths=["Items inyectados en este prompt"],
            write_paths=[out_target, alt_out_target, f"{work_rel}/judge_responses_{j_id}.json"],
            forbidden_paths=[
                "judge_ground_truth.json",
                "work/templates/*",
                "templates/*",
                "engine/*",
                "search_web",
                "read_url_content",
                "navegación por internet",
            ],
            done_signal=f"DONE: {out_target}",
        )

        prompt_lines = [
            f"# Asignación de Evaluación a Ciegas: Blind Judge `{j_tag}` (C2C v3.21 Zero-Warmup Load Inversion)",
            "",
            scope_header,
            "",
            "## 1. PROTOCOLO ZERO-WARMUP EN 1 SOLO TURNO",
            f"- **Judge ID:** `{j_tag}`",
            f"- **Lote Asignado:** `{bf.name}`",
            f"- **Ruta de Salida Obligatoria:** `{out_target}` (o `{alt_out_target}`)",
            f"- **NO EJECUTES `view_file` para leer el lote:** Todos los reactivos ya están inyectados abajo.",
            f"- **NO EJECUTES `run_command`:** Resuelve analíticamente desde primeros principios.",
            f"- **Completa tu tarea en 1 SOLO TURNO** escribiendo directamente el archivo de respuestas con `write_to_file`.",
            f"- Sigue estrictamente todas las reglas de tu System Prompt `c2c_judge` y finaliza con: `DONE: {out_target}`.",
            "",
            "## 2. ÍTEMS A EVALUAR (ZERO-WARMUP IN-PROMPT PAYLOAD)",
            "```json",
            items_json_str,
            "```",
        ]
        prompt_full = "\n".join(prompt_lines)

        item_file = items_dir / f"judge_{idx:02d}.json"
        item_data = {
            "TypeName": "c2c_judge",
            "Role": f"Blind Judge {j_id}",
            "Model": "flash",
            "Workspace": "inherit",
            "batch_file": bf.name,
            "items_count": len(items_payload),
            "output_target": out_target,
            "Prompt": prompt_full,
            "items": items_payload,
        }
        item_file.write_text(json.dumps(item_data, indent=2, ensure_ascii=False), encoding="utf-8")

        if use_pointer:
            pointer_prompt = make_pointer_prompt(
                role_name=f"Blind Judge {j_id}",
                work_order_rel=f"{work_rel}/dispatch/items/{item_file.name}",
                done_signal=f"DONE: {out_target}",
            )
            subagent_item = {
                "TypeName": "c2c_judge",
                "Role": f"Blind Judge {j_id}",
                "Model": "flash",
                "Prompt": pointer_prompt,
            }
        else:
            subagent_item = item_data

        subagents.append(subagent_item)
        item_files.append(item_file.resolve().as_posix())

    dispatch_dir = work / "dispatch"
    dispatch_dir.mkdir(parents=True, exist_ok=True)
    judges_audit_file = dispatch_dir / "judges.json"
    judges_audit = {
        "stage": "judges",
        "dispatched_at": datetime.now(timezone.utc).isoformat(),
        "subagents_count": len(subagents),
        "max_items_per_judge": max_items_per_judge,
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
    pointer: bool = False,
) -> Dict[str, Any]:
    """Generates invoke_subagent payload with strict SCOPE-LOCK for the given role."""
    use_pointer = pointer or os.getenv("C2C_POINTER_PROMPTS", "").lower() in ("1", "true", "yes")

    if role in ("vision", "vision-legacy"):
        raise ValueError(f"Stages 'vision' and 'vision-legacy' have been removed in C2C v3.2. Use Direct PDF Ingestion instead.")

    if role in ("cta", "cta-direct", "cta-map", "c2c_cta_architect"):
        mode = "mapreduce" if role == "cta-map" else None
        return dispatch_cta(work_dir, mode=mode, pointer=use_pointer)

    if role in ("author", "authors", "c2c_shard_author"):
        return dispatch_authors(work_dir, pointer=use_pointer)

    if role in ("judge", "judges", "c2c_judge"):
        return dispatch_judges(work_dir, pointer=use_pointer)

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
        shard_jsons = sorted(list((work / "cta_parts").glob("*.json")) + list((work / "cta").glob("cta_shard_*.json")))
        shard_json_rel_list = [f"{work_rel}/{p.relative_to(work).as_posix()}" for p in shard_jsons] if shard_jsons else [f"{work_rel}/cta_parts/*.json"]
        shard_json_lines = "\n".join(f"- `{p}`" for p in shard_json_rel_list)
        compile_cmd = f"python .agents/skills/content-to-course/cta_merge.py --work \"{work.resolve().as_posix()}\""

        scope_header = build_scope_header(
            role="cta-reduce",
            read_paths=[f"{work_rel}/cta_outline.json", f"{work_rel}/duplicate_candidates.json"] + shard_json_rel_list,
            write_paths=[f"{work_rel}/cta_harmonize.json", f"{work_rel}/cta.json", f"{work_rel}/cta.md"],
            done_signal=f"DONE: {work_rel}/cta.json",
        )

        prompt_text = (
            f"# Asignación de Tarea: CTA Harmonizer (MapReduce Harmonization v3.21)\n\n"
            f"{scope_header}\n\n"
            f"## 1. FRAGMENTOS CTA A FUSIONAR Y ARMONIZAR\n"
            f"{shard_json_lines}\n\n"
            f"## 2. INSTRUCCIONES DE EJECUCIÓN\n"
            f"1. Analiza los fragmentos curriculares y deduplica competencias.\n"
            f"2. Emite la armonización en `{work_rel}/cta_harmonize.json` si se requiere o ejecuta el merge oficial determinista:\n"
            f"   ```bash\n"
            f"   {compile_cmd}\n"
            f"   ```\n"
            f"3. Sigue todas las directivas de tu System Prompt `c2c_cta_architect` y finaliza estrictamente con: `DONE: {work_rel}/cta.json`.\n"
        )
        item_data = {
            "TypeName": spec["type_name"],
            "Role": "CTA Harmonizer",
            "Model": spec["model"],
            "Prompt": prompt_text,
        }
        subagents.append(item_data)
        dispatched_ids.append("harmonizer")
        items_dir = work / "dispatch" / "items"
        items_dir.mkdir(parents=True, exist_ok=True)
        item_file = items_dir / "cta_harmonize_01.json"
        item_file.write_text(json.dumps(item_data, indent=2, ensure_ascii=False), encoding="utf-8")

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
                for disc in jr.get("disagreements", []) or jr.get("discordances", []):
                    cid = disc.get("cid") or disc.get("competency_id")
                    if cid:
                        failing_targets.setdefault(cid, {})["judge_disagreement"] = disc
            except Exception as e:
                logger.warning("Error reading judge_report.json: %s", e)

        # Fix comp_to_shard resolution: read pre_shard_manifest.json FIRST, fallback to shard_*.json
        shard_map: Dict[str, str] = {}
        pre_shard_manifest = work / "shards" / "pre_shard_manifest.json"
        if pre_shard_manifest.is_file():
            try:
                sm_data = json.loads(pre_shard_manifest.read_text(encoding="utf-8"))
                shards_info = sm_data.get("shards", [])
                if isinstance(shards_info, list):
                    for s in shards_info:
                        s_id = s.get("shard_id") or "shard_01"
                        c_ids = s.get("competency_ids") or []
                        if not c_ids and "competencies" in s:
                            c_ids = [c.get("id") for c in s["competencies"] if isinstance(c, dict) and "id" in c]
                        for cid in c_ids:
                            if cid:
                                shard_map[cid] = s_id
                elif isinstance(shards_info, dict):
                    for s_id, comps in shards_info.items():
                        if isinstance(comps, list):
                            for c in comps:
                                cid = c.get("id") if isinstance(c, dict) else str(c)
                                if cid:
                                    shard_map[cid] = s_id
            except Exception as e:
                logger.warning("Error reading pre_shard_manifest.json in repair: %s", e)

        for sf in sorted((work / "shards").glob("shard_*.json")):
            try:
                sdata = json.loads(sf.read_text(encoding="utf-8"))
                s_id = sdata.get("shard_id", sf.stem)
                for cid in sdata.get("competency_ids", []):
                    if cid and cid not in shard_map:
                        shard_map[cid] = s_id
                if "competencies" in sdata and isinstance(sdata["competencies"], list):
                    for c in sdata["competencies"]:
                        cid = c.get("id") if isinstance(c, dict) else str(c)
                        if cid and cid not in shard_map:
                            shard_map[cid] = s_id
            except Exception:
                pass

        if ids is not None:
            ids_str = {str(i) for i in ids}
            failing_targets = {cid: data for cid, data in failing_targets.items() if cid in ids_str}

        if not failing_targets and ids:
            for cid in ids:
                failing_targets[str(cid)] = {"manual_request": True}

        manifest_rel = f"{work_rel}/ingestion_manifest.json" if (work / "ingestion_manifest.json").is_file() else f"{work_rel}/pre_cta_manifest.json"
        cta_rel = f"{work_rel}/cta.json"

        items_dir = work / "dispatch" / "items"
        items_dir.mkdir(parents=True, exist_ok=True)
        item_files: List[str] = []

        for idx, (cid, diag) in enumerate(failing_targets.items(), start=1):
            shard_id = shard_map.get(cid, "shard_01")
            out_py = f"{work_rel}/shards/{shard_id}_data.py"
            out_json = f"{work_rel}/shards/{shard_id}.json"
            compile_cmd = (
                f"python .agents/skills/content-to-course/compile_shard.py "
                f"--input {out_py} --output {out_json} --cta {cta_rel} --manifest {manifest_rel}"
            )
            scope_header = build_scope_header(
                role="repair",
                read_paths=[out_py, f"{work_rel}/templates/{cid}.json", cta_rel],
                write_paths=[out_py, out_json],
                forbidden_paths=[
                    "engine/*",
                    "SKILL.md",
                    ".agents/skills/content-to-course/check_templates.py",
                    ".agents/skills/content-to-course/check_cta.py",
                    "src/validator/**",
                ],
                done_signal=f"DONE: {out_json}",
            )
            diag_str = json.dumps(diag, indent=2, ensure_ascii=False)
            prompt_text = (
                f"# Asignación de Tarea: Targeted Repair Engineer `{cid}` (C2C v3.21 Load Inversion)\n\n"
                f"{scope_header}\n\n"
                f"## 1. REPARACIÓN ASIGNADA\n"
                f"- **Competencia Afectada:** `{cid}`\n"
                f"- **Shard Asociado:** `{shard_id}`\n"
                f"- **Archivo Python Objetivo:** `{out_py}`\n"
                f"- **Destino JSON Final:** `{out_json}`\n\n"
                f"## 2. DIAGNÓSTICO DEL FALLO\n"
                f"```json\n{diag_str}\n```\n\n"
                f"## 3. INSTRUCCIONES DE REPARACIÓN\n"
                f"1. Corrige la tupla de `{cid}` en `{out_py}` usando quirúrgicamente `replace_file_content`.\n"
                f"2. Compila y certifica la corrección ejecutando:\n"
                f"   ```bash\n"
                f"   {compile_cmd}\n"
                f"   ```\n"
                f"3. Sigue todas las directivas de tu System Prompt `c2c_repair` y finaliza con: `DONE: {out_json}`.\n"
            )
            item_file = items_dir / f"repair_{idx:02d}.json"
            item_data = {
                "TypeName": spec["type_name"],
                "Role": f"Repair Engineer {cid}",
                "Model": spec["model"],
                "competency_id": cid,
                "shard_id": shard_id,
                "output_python": out_py,
                "output_json": out_json,
                "compile_command": compile_cmd,
                "diagnostics": diag,
                "Prompt": prompt_text,
                "work_order": prompt_text,
            }
            item_file.write_text(json.dumps(item_data, indent=2, ensure_ascii=False), encoding="utf-8")

            if use_pointer:
                pointer_prompt = make_pointer_prompt(
                    role_name=f"Repair Engineer {cid}",
                    work_order_rel=f"{work_rel}/dispatch/items/{item_file.name}",
                    done_signal=f"DONE: {out_json}",
                )
                sub_item = {
                    "TypeName": spec["type_name"],
                    "Role": f"Repair Engineer {cid}",
                    "Model": spec["model"],
                    "Prompt": pointer_prompt,
                }
            else:
                sub_item = item_data

            subagents.append(sub_item)
            dispatched_ids.append(cid)
            item_files.append(item_file.resolve().as_posix())

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


def dispatch_repair(
    work_dir: Union[str, Path],
    ids: Optional[List[Union[str, int]]] = None,
    pointer: bool = False,
) -> Dict[str, Any]:
    """Generates dispatch payload and individual item files for Targeted Repair Engineers (Load Inversion v3.21)."""
    return build_dispatch(role="repair", work_dir=work_dir, ids=ids, pointer=pointer)


def pre_stage5_cleanup(work_dir: Union[str, Path]) -> Dict[str, Any]:
    """Protocol for clearing stale/errored subagents prior to Stage 5 verification (P4 / R5 SLA).
    
    Instructs the Director to execute manage_subagents(kill_all) so that stale 429
    or aborted subagent entries do not mislead Stage 5 decisions. Also cleans up
    transient failure markers in state.json.
    """
    work = Path(work_dir).resolve()
    from budget_guard import update_state_checkpoint, load_state_checkpoint

    state = load_state_checkpoint(work)
    subagents = state.get("subagents", {})
    cleared = []
    for s_name, s_info in list(subagents.items()):
        if isinstance(s_info, dict) and s_info.get("status") in ("errored", "aborted"):
            s_info["status"] = "purged_pre_stage5"
            cleared.append(s_name)

    state["subagents"] = subagents
    (work / "state.json").write_text(json.dumps(state, indent=2, ensure_ascii=False), encoding="utf-8")
    update_state_checkpoint(work, "pre_stage5_cleanup", "completed", metadata={"purged_subagents": cleared})
    msg = (
        "[+] Pre-Stage-5 Cleanup executed.\n"
        "    SLA Requirement: Run `manage_subagents(Action='kill_all')` before dispatching Stage 5 judges.\n"
        f"    Purged {len(cleared)} stale subagent error records."
    )
    return {"status": "ok", "purged": cleared, "message": msg}


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
    disp.add_argument("--pointer", action="store_true", help="Generate pointer-prompt work orders referencing disk JSON")

    # check subcommand
    chk = subparsers.add_parser("check", help="Run scope violation check")
    chk.add_argument("--role", required=True, choices=list(ROLE_SPECS.keys()), help="Subagent role")
    chk.add_argument("--work-dir", required=True, help="Course working directory")

    # define-types subcommand
    dt = subparsers.add_parser("define-types", help="Print and persist define_subagent payloads for all c2c types")
    dt.add_argument("--work-dir", default=None, help="Optional course working directory to persist type files")
    dt.add_argument("--lean", action="store_true", help="Use lean static system prompts (<= 5 KB)")

    # dispatch-cta subcommand
    dc = subparsers.add_parser("dispatch-cta", help="Dispatch CTA Architect using pre_cta_manifest.json")
    dc.add_argument("--work-dir", required=True, help="Course working directory")
    dc.add_argument("--mode", default=None, help="CTA mode: direct or mapreduce")
    dc.add_argument("--pointer", action="store_true", help="Generate pointer-prompt work orders referencing disk JSON")

    # dispatch-authors subcommand
    da = subparsers.add_parser("dispatch-authors", help="Dispatch Shard Authors using pre_shard_manifest.json")
    da.add_argument("--work-dir", required=True, help="Course working directory")
    da.add_argument("--pointer", action="store_true", help="Generate pointer-prompt work orders referencing disk JSON")

    # dispatch-judges subcommand
    dj = subparsers.add_parser("dispatch-judges", help="Dispatch Blind Judges with Zero-Warmup in-prompt payload")
    dj.add_argument("--work-dir", required=True, help="Course working directory")
    dj.add_argument("--pointer", action="store_true", help="Generate pointer-prompt work orders referencing disk JSON")
    dj.add_argument("--max-items-per-judge", type=int, default=12, help="Maximum items per judge batch (default: 12)")

    # dispatch-repair subcommand
    dr = subparsers.add_parser("dispatch-repair", help="Dispatch Targeted Repair Engineers")
    dr.add_argument("--work-dir", required=True, help="Course working directory")
    dr.add_argument("--ids", nargs="*", help="Optional specific IDs to repair")
    dr.add_argument("--pointer", action="store_true", help="Generate pointer-prompt work orders referencing disk JSON")

    # checkpoint subcommand
    cp = subparsers.add_parser("checkpoint", help="Record stage checkpoint in state.json")
    cp.add_argument("--work-dir", required=True, help="Course working directory")
    cp.add_argument("--stage", required=True, help="Pipeline stage name")
    cp.add_argument("--status", default="completed", help="Status of stage (completed/in_progress/failed)")

    # cleanup-subagents subcommand
    cl = subparsers.add_parser("cleanup-subagents", help="Execute Pre-Stage-5 subagent cleanup protocol")
    cl.add_argument("--work-dir", required=True, help="Course working directory")

    # status subcommand
    st = subparsers.add_parser("status", help="Read state.json and show pipeline progress")
    st.add_argument("--work-dir", required=True, help="Course working directory")

    args = parser.parse_args()

    if args.action == "define-types":
        target_work = args.work_dir or Path.cwd() / "work"
        res = generate_define_subagent_specs(target_work, lean=args.lean)
        print(json.dumps(res, indent=2, ensure_ascii=False))

    elif args.action == "dispatch-cta":
        res = dispatch_cta(args.work_dir, mode=args.mode, pointer=args.pointer)
        print(json.dumps(res, indent=2, ensure_ascii=False))

    elif args.action == "dispatch-authors":
        res = dispatch_authors(args.work_dir, pointer=args.pointer)
        print(json.dumps(res, indent=2, ensure_ascii=False))

    elif args.action == "dispatch-judges":
        res = dispatch_judges(args.work_dir, pointer=args.pointer, max_items_per_judge=args.max_items_per_judge)
        print(json.dumps(res, indent=2, ensure_ascii=False))

    elif args.action == "dispatch-repair":
        res = dispatch_repair(args.work_dir, ids=args.ids, pointer=args.pointer)
        print(json.dumps(res, indent=2, ensure_ascii=False))

    elif args.action == "checkpoint":
        from budget_guard import update_state_checkpoint
        state = update_state_checkpoint(args.work_dir, args.stage, args.status)
        print(json.dumps(state, indent=2, ensure_ascii=False))

    elif args.action == "cleanup-subagents":
        res = pre_stage5_cleanup(args.work_dir)
        print(json.dumps(res, indent=2, ensure_ascii=False))

    elif args.action == "status":
        from budget_guard import load_state_checkpoint
        state = load_state_checkpoint(args.work_dir)
        print(json.dumps(state, indent=2, ensure_ascii=False))

    elif args.action == "build":
        payload = build_dispatch(
            role=args.role,
            work_dir=args.work_dir,
            ids=args.ids,
            ready_only=args.ready_only,
            pointer=args.pointer,
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
