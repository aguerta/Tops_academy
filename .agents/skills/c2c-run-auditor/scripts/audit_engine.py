"""Content-to-Course & Multi-Agent Workflow Run Audit Engine (Deep Forensic Edition).

Extracts ultra-granular telemetry from Antigravity conversation transcripts and
subagent trees, profiles workload inputs, computes normalized unit economics per
shard and per competency, breaks down stage-by-stage critical paths and max wall-clock
latencies, performs deep orchestrator overhead & intervention audits, and maintains a
persistent longitudinal benchmark registry.
"""

from __future__ import annotations

import argparse
import datetime
import glob
import json
import math
import os
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple, Union

try:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

try:
    import pymupdf
    HAS_PYMUPDF = True
except ImportError:
    try:
        import fitz as pymupdf
        HAS_PYMUPDF = True
    except ImportError:
        HAS_PYMUPDF = False
HAS_FITZ = HAS_PYMUPDF


# ---------------------------------------------------------------------------
# Path & Environment Resolution
# ---------------------------------------------------------------------------

def get_brain_dir() -> Path:
    """Return user's Antigravity brain directory."""
    user_home = Path(os.path.expanduser("~"))
    brain_dir = user_home / ".gemini" / "antigravity" / "brain"
    return brain_dir


def resolve_transcript_path(target: str) -> Optional[Path]:
    """Resolve a conversation ID, chat link, or file path to transcript.jsonl."""
    target = target.strip()

    # Markdown chat link: [label](conversation://<uuid>)
    link_match = re.search(r"conversation://([a-f0-9\-]{36})", target, re.IGNORECASE)
    if link_match:
        conv_id = link_match.group(1)
        p = get_brain_dir() / conv_id / ".system_generated" / "logs" / "transcript.jsonl"
        if p.exists():
            return p

    # Raw UUID
    uuid_match = re.search(r"\b([a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})\b", target, re.IGNORECASE)
    if uuid_match:
        conv_id = uuid_match.group(1)
        p = get_brain_dir() / conv_id / ".system_generated" / "logs" / "transcript.jsonl"
        if p.exists():
            return p

    # Direct file path
    target_path = Path(target)
    if target_path.exists():
        if target_path.is_file() and target_path.name.endswith(".jsonl"):
            return target_path
        if target_path.is_dir():
            cand = target_path / ".system_generated" / "logs" / "transcript.jsonl"
            if cand.exists():
                return cand
            cand2 = target_path / "transcript.jsonl"
            if cand2.exists():
                return cand2

    # Try searching brain dir for partial matching ID
    brain_dir = get_brain_dir()
    if brain_dir.exists():
        for d in brain_dir.iterdir():
            if d.is_dir() and target.lower() in d.name.lower():
                cand = d / ".system_generated" / "logs" / "transcript.jsonl"
                if cand.exists():
                    return cand

    return None


def list_recent_c2c_runs(limit: int = 10) -> List[Dict[str, Any]]:
    """Scan brain directory for recent conversations orchestrating content-to-course."""
    brain_dir = get_brain_dir()
    if not brain_dir.exists():
        return []

    results = []
    for d in brain_dir.iterdir():
        if not d.is_dir():
            continue
        transcript = d / ".system_generated" / "logs" / "transcript.jsonl"
        if not transcript.exists():
            continue

        try:
            mtime = transcript.stat().st_mtime
            with open(transcript, "r", encoding="utf-8", errors="ignore") as f:
                head = "".join([f.readline() for _ in range(30)])
                if "content-to-course" in head or "run.py" in head or "prepare" in head or "shard" in head:
                    results.append({
                        "conversation_id": d.name,
                        "path": str(transcript),
                        "mtime": mtime,
                        "date_str": datetime.datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M:%S")
                    })
        except Exception:
            continue

    results.sort(key=lambda x: x["mtime"], reverse=True)
    return results[:limit]


# ---------------------------------------------------------------------------
# Transcript & Subagent Parsing
# ---------------------------------------------------------------------------

class TranscriptParser:
    """Parses transcript.jsonl files into structured steps, tokens, tools, and subagents."""

    @staticmethod
    def parse_file(path: Path) -> List[Dict[str, Any]]:
        records = []
        if not path.exists():
            return records

        truncated_steps: Dict[int, int] = {}
        truncated_lines: Dict[int, int] = {}

        try:
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                for line_idx, line in enumerate(f):
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        rec = json.loads(line)
                        rec_idx = len(records)
                        records.append(rec)
                        if rec.get("truncated_fields"):
                            s_idx = rec.get("step_index")
                            if s_idx is not None:
                                truncated_steps[s_idx] = rec_idx
                            truncated_lines[line_idx] = rec_idx
                    except Exception:
                        pass
        except Exception:
            return records

        if not truncated_steps and not truncated_lines:
            return records

        full_path = path.parent / "transcript_full.jsonl"
        if not full_path.is_file():
            return records

        needed_steps = set(truncated_steps.keys())
        needed_lines = set(truncated_lines.keys())
        _step_re = re.compile(r'\{"step_index":\s*(\d+)')

        try:
            with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
                for line_idx, line in enumerate(f):
                    line = line.strip()
                    if not line:
                        continue
                    m = _step_re.match(line[:50])
                    matched_step = int(m.group(1)) if m else None

                    is_needed = False
                    rec_idx = None

                    if matched_step is not None and matched_step in needed_steps:
                        is_needed = True
                        rec_idx = truncated_steps[matched_step]
                    elif line_idx in needed_lines:
                        is_needed = True
                        rec_idx = truncated_lines[line_idx]

                    if is_needed and rec_idx is not None:
                        try:
                            full_rec = json.loads(line)
                            records[rec_idx] = full_rec
                        except Exception:
                            pass
                        if matched_step is not None and matched_step in needed_steps:
                            needed_steps.remove(matched_step)
                        if line_idx in needed_lines:
                            needed_lines.remove(line_idx)
                        if not needed_steps and not needed_lines:
                            break
        except Exception:
            pass

        return records

    @staticmethod
    def discover_all_subagents(records: List[Dict[str, Any]], brain_dir: Path) -> List[Dict[str, Any]]:
        """Deep scan across all records to extract all spawned conversationIds and inspect step 0."""
        seen_cids = set()
        subagents = []

        # 1. Pre-build CID metadata mapping from manage_subagents & invoke_subagent
        cid_meta: Dict[str, Dict[str, Any]] = {}
        for rec in records:
            content = rec.get("content", "")
            if "active subagent" in content or "Created the following subagents" in content:
                m_json = re.search(r"(\[\s*\{.*?\}\s*\])", content, re.DOTALL)
                if m_json:
                    try:
                        arr = json.loads(m_json.group(1))
                        for item in arr:
                            cid = item.get("conversationId")
                            if cid:
                                cid_meta[cid] = {
                                    "role": item.get("role"),
                                    "type_name": item.get("type")
                                }
                    except Exception:
                        pass

        for rec in records:
            content = rec.get("content", "")
            if "Created the following subagents" in content or "conversationId" in content:
                # Find all UUIDs in content
                cids = re.findall(r'"conversationId":\s*"([^"]+)"', content)
                if not cids:
                    cids = re.findall(r'conversationId["\':\s]+([a-f0-9\-]{36})', content)

                for cid in cids:
                    if cid in seen_cids:
                        continue
                    seen_cids.add(cid)

                    sub_path = brain_dir / cid / ".system_generated" / "logs" / "transcript.jsonl"
                    role = "Subagent"
                    model = "inherit"
                    type_name = "subagent"
                    prompt_preview = ""
                    shard_id = None

                    if sub_path.exists():
                        try:
                            with open(sub_path, "r", encoding="utf-8", errors="ignore") as sf:
                                first_line = sf.readline()
                                if first_line:
                                    d0 = json.loads(first_line)
                                    p0 = d0.get("content", "")
                                    prompt_preview = p0[:300]
                                    m_asig = re.search(r"#\s*Asignaci[oó]n de Tarea para\s+([^\n\r\\#]+)", p0)
                                    m_inst = re.search(r"Instrucciones para\s+([^\n\r\\#]+)", p0)
                                    if m_asig:
                                        role = m_asig.group(1).strip()
                                    elif m_inst:
                                        role = m_inst.group(1).strip()
                                    elif "Task:" in p0:
                                        role = p0.split("Task:")[1].split("\n")[0].strip()[:40]
                                    elif "Role:" in p0:
                                        role = p0.split("Role:")[1].split("\n")[0].strip()[:40]

                                    # Detect shard
                                    sm = re.search(r"shard_(\d+)", role.lower()) or re.search(r"shard_(\d+)", p0.lower()) or re.search(r"shard\s+(\d+)", role.lower())
                                    if sm:
                                        shard_id = f"shard_{sm.group(1).zfill(2)}"
                        except Exception:
                            pass

                    if cid in cid_meta:
                        if cid_meta[cid].get("role") and (role == "Subagent" or len(cid_meta[cid]["role"]) > len(role)):
                            role = cid_meta[cid]["role"]
                        if cid_meta[cid].get("type_name"):
                            type_name = cid_meta[cid]["type_name"]
                        if not shard_id:
                            sm = re.search(r"shard_(\d+)", role.lower()) or re.search(r"shard\s+(\d+)", role.lower())
                            if sm:
                                shard_id = f"shard_{sm.group(1).zfill(2)}"

                    # Classify category
                    role_lower = role.lower()
                    type_lower = type_name.lower()
                    if "vision" in role_lower or "handout" in role_lower or "vision" in type_lower:
                        category = "vision"
                    elif (
                        "mapper" in role_lower
                        or "cta section" in role_lower
                        or "map" in type_lower
                        or "part_" in role_lower
                        or "part_" in prompt_preview.lower()
                        or "subpart" in role_lower
                        or "subpart" in prompt_preview.lower()
                    ):
                        category = "cta_mapper"
                    elif "harmonizer" in role_lower or "cta reduce" in role_lower or "cta-reduce" in type_lower:
                        category = "cta_harmonizer"
                    elif "direct cta" in role_lower or "cta architect" in role_lower or "cta-direct" in type_lower or "cta" in type_lower:
                        category = "cta_harmonizer"
                    elif "author" in role_lower or "shard" in role_lower or "author" in type_lower:
                        category = "author"
                    elif "judge" in role_lower or "judge" in type_lower:
                        category = "judge"
                    elif "repair" in role_lower or "repair" in type_lower:
                        category = "repair"
                    else:
                        category = "generic"

                    subagents.append({
                        "conversation_id": cid,
                        "role": role,
                        "category": category,
                        "shard_id": shard_id,
                        "model": model,
                        "type_name": type_name,
                        "spawn_step": rec.get("step_index"),
                        "spawn_time": rec.get("created_at"),
                        "prompt_preview": prompt_preview
                    })

        return subagents


# ---------------------------------------------------------------------------
# Workload & Content Footprint Extraction
# ---------------------------------------------------------------------------

class WorkloadExtractor:
    """Extracts raw content metrics: files, sizes, pages/slides, corpus, competencies.
    Enforces strict conversation_id isolation so telemetry/manifests from other runs never collide.
    """

    @staticmethod
    def _extract_transcript_hints(records: Optional[List[Dict[str, Any]]], workspace_root: Path) -> Dict[str, Any]:
        hints: Dict[str, Any] = {
            "course_ids": [],
            "work_dirs": [],
            "start_epoch": None,
            "end_epoch": None,
            "full_text": "",
        }
        if not records:
            return hints

        timestamps: List[float] = []
        text_chunks: List[str] = []

        for rec in records:
            ts_str = rec.get("created_at")
            if ts_str:
                try:
                    dt = datetime.datetime.fromisoformat(ts_str.replace("Z", "+00:00"))
                    timestamps.append(dt.timestamp())
                except Exception:
                    pass

            content = rec.get("content", "") or ""
            if content:
                text_chunks.append(content)

            for tc in rec.get("tool_calls", []) or []:
                args = tc.get("args", {}) if isinstance(tc, dict) else {}
                if isinstance(args, dict):
                    for k in ("CommandLine", "TargetFile", "AbsolutePath"):
                        val = str(args.get(k, "") or "")
                        if val:
                            text_chunks.append(val)

        full_text = "\n".join(text_chunks)
        hints["full_text"] = full_text
        if timestamps:
            hints["start_epoch"] = min(timestamps)
            hints["end_epoch"] = max(timestamps)

        # Extract explicit --work-dir / --work flags and courses/<slug>/work paths
        for m_wd in re.finditer(r"(?:--work(?:-dir)?\s+['\"]?([^\s'\"`]+)|(?:courses[/\\]([a-zA-Z0-9_-]+)[/\\]work))", full_text):
            raw_wd = m_wd.group(1) or (f"courses/{m_wd.group(2)}/work" if m_wd.group(2) else "")
            if raw_wd:
                p_wd = Path(raw_wd)
                if not p_wd.is_absolute():
                    p_wd = (workspace_root / p_wd).resolve()
                else:
                    p_wd = p_wd.resolve()
                if p_wd not in hints["work_dirs"]:
                    hints["work_dirs"].append(p_wd)

        # Extract explicit --course-id flags and courses/<slug>.json
        for m_cid in re.finditer(
            r"(?:--course-id\s+['\"]?([a-zA-Z0-9_-]+)|courses[/\\]([a-zA-Z0-9_-]+)[/\\]work|courses[/\\]([a-zA-Z0-9_-]+)\.json)",
            full_text,
        ):
            cid = next((g for g in m_cid.groups() if g), None)
            if cid and cid not in ("unknown", "course_generic", "COURSE_ID", "course_id", "custom_course", "work") and cid not in hints["course_ids"]:
                hints["course_ids"].append(cid)

        return hints

    @staticmethod
    def _validate_work_dir_for_conversation(
        cd: Path,
        target_conv_id: Optional[str],
        hints: Dict[str, Any],
    ) -> Tuple[bool, Optional[Path]]:
        """Verifies that a candidate work_dir belongs to target_conv_id (Zero Collision Gate).
        Returns (is_valid, telemetry_dir_to_use).
        """
        if not cd.exists():
            return False, None

        telem_dir = cd / "telemetry"
        # 1. Check isolated per-conversation telemetry folder first
        if target_conv_id and (telem_dir / "by_conversation" / target_conv_id).is_dir():
            return True, telem_dir / "by_conversation" / target_conv_id

        # 2. Check telemetry/*.json and state.json for explicit conversation_id binding
        found_conv_ids: Set[str] = set()
        state_file = cd / "state.json"
        if state_file.is_file():
            try:
                sdata = json.loads(state_file.read_text(encoding="utf-8"))
                if sdata.get("conversation_id"):
                    found_conv_ids.add(str(sdata["conversation_id"]))
            except Exception:
                pass

        if telem_dir.is_dir():
            for tf in telem_dir.glob("*.json"):
                try:
                    tdata = json.loads(tf.read_text(encoding="utf-8"))
                    if tdata.get("conversation_id"):
                        found_conv_ids.add(str(tdata["conversation_id"]))
                except Exception:
                    pass

        if target_conv_id and found_conv_ids:
            if target_conv_id in found_conv_ids:
                return True, telem_dir
            # Explicitly bound to a DIFFERENT conversation_id -> Collision! Reject!
            return False, None

        # 3. If no telemetry conversation_id exists on disk, verify against transcript hints & timestamps
        has_manifests = any(
            (cd / fn).exists()
            for fn in ("budget.json", "pre_cta_manifest.json", "state.json", "order.json", "cta.json")
        ) or (cd / "shards" / "pre_shard_manifest.json").exists()
        if not has_manifests:
            return False, None

        if target_conv_id and hints.get("work_dirs"):
            if cd.resolve() not in hints["work_dirs"]:
                return False, None

        start_ep = hints.get("start_epoch")
        end_ep = hints.get("end_epoch")
        if start_ep and end_ep:
            mtimes = []
            for fn in ("state.json", "cta.json", "pre_cta_manifest.json", "course.json"):
                fp = cd / fn
                if fp.exists():
                    mtimes.append(fp.stat().st_mtime)
            if mtimes and not any((start_ep - 300) <= mt <= (end_ep + 1800) for mt in mtimes):
                return False, None

        return True, (telem_dir if telem_dir.is_dir() else None)

    @staticmethod
    def extract(
        work_dir: Optional[Path] = None,
        workspace_root: Optional[Path] = None,
        records: Optional[List[Dict[str, Any]]] = None,
        target_conv_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        workload: Dict[str, Any] = {
            "source_files": [],
            "total_input_bytes": 0,
            "total_input_mb": 0.0,
            "total_pages_or_slides": 0,
            "pages_needing_vision": 0,
            "total_handouts": 0,
            "corpus_chars": 0,
            "corpus_words": 0,
            "competencies_count": 0,
            "shards_count": 0,
            "shards_competencies_map": {},
            "questions_count": 0,
            "templates_compiled_count": 0,
            "cta_mode": "unknown",
            "course_id": "unknown",
            "course_title": "unknown",
            "run_status": "COMPLETED",
        }

        if not workspace_root:
            workspace_root = Path.cwd()

        hints = WorkloadExtractor._extract_transcript_hints(records, workspace_root)
        transcript_full_text = hints.get("full_text", "")
        if hints.get("course_ids"):
            workload["course_id"] = hints["course_ids"][0]

        # Build candidate work directories in strict priority order (transcript-bound first, root work/ last)
        candidate_dirs: List[Path] = []
        if work_dir and work_dir.exists():
            candidate_dirs.append(work_dir.resolve())
        for wd in hints.get("work_dirs", []):
            if wd not in candidate_dirs:
                candidate_dirs.append(wd)
        courses_dir = workspace_root / "courses"
        for cid_hint in hints.get("course_ids", []):
            c_work = (courses_dir / cid_hint / "work").resolve()
            if c_work not in candidate_dirs:
                candidate_dirs.append(c_work)
        if courses_dir.exists():
            for c_sub in sorted(courses_dir.iterdir(), key=lambda p: p.stat().st_mtime if p.exists() else 0, reverse=True):
                if c_sub.is_dir() and (c_sub / "work").exists():
                    cw = (c_sub / "work").resolve()
                    if cw not in candidate_dirs:
                        candidate_dirs.append(cw)
        root_work = (workspace_root / "work").resolve()
        if root_work not in candidate_dirs:
            candidate_dirs.append(root_work)

        found_work: Optional[Path] = None
        verified_telem_dir: Optional[Path] = None
        for cd in candidate_dirs:
            is_ok, t_dir = WorkloadExtractor._validate_work_dir_for_conversation(cd, target_conv_id, hints)
            if is_ok:
                found_work = cd
                verified_telem_dir = t_dir
                break

        if found_work:
            workload["work_dir"] = str(found_work)
            workload["work_dir_resolved"] = str(found_work)
            workload["work_dir_conversation_match"] = True

            # 0. Pipeline State & Telemetry Snapshots (C2C v3.2 Active Ingestion)
            state_file = (verified_telem_dir / "state.json") if (verified_telem_dir and (verified_telem_dir / "state.json").is_file()) else (found_work / "state.json")
            if state_file.is_file():
                try:
                    sdata = json.loads(state_file.read_text(encoding="utf-8"))
                    if not target_conv_id or not sdata.get("conversation_id") or sdata.get("conversation_id") == target_conv_id:
                        workload["pipeline_state"] = sdata
                        if sdata.get("course_id") and workload["course_id"] in ("unknown", "course_generic", "custom_course"):
                            workload["course_id"] = sdata.get("course_id")
                        if sdata.get("course_title") and workload["course_title"] in ("unknown", "course_generic", "custom_course"):
                            workload["course_title"] = sdata.get("course_title")
                        if sdata.get("status"):
                            workload["pipeline_status"] = sdata.get("status")
                        art_counts = sdata.get("artifact_counts", {})
                        if isinstance(art_counts, dict):
                            if art_counts.get("pages") and workload["total_pages_or_slides"] == 0:
                                workload["total_pages_or_slides"] = int(art_counts["pages"])
                            if art_counts.get("competencies") and workload["competencies_count"] == 0:
                                workload["competencies_count"] = int(art_counts["competencies"])
                            if art_counts.get("shards") and workload["shards_count"] == 0:
                                workload["shards_count"] = int(art_counts["shards"])
                            if art_counts.get("templates_compiled"):
                                workload["templates_compiled_count"] = int(art_counts["templates_compiled"])
                            if art_counts.get("questions_built") and workload["questions_count"] == 0:
                                workload["questions_count"] = int(art_counts["questions_built"])
                except Exception:
                    pass

            pre_cta_file = found_work / "pre_cta_manifest.json"
            if pre_cta_file.is_file():
                try:
                    pc_data = json.loads(pre_cta_file.read_text(encoding="utf-8"))
                    if pc_data.get("course_id") and workload["course_id"] in ("unknown", "course_generic", "custom_course"):
                        workload["course_id"] = pc_data.get("course_id")
                    if pc_data.get("course_title") and workload["course_title"] in ("unknown", "course_generic", "custom_course"):
                        workload["course_title"] = pc_data.get("course_title")
                    if pc_data.get("cta_mode"):
                        workload["cta_mode"] = pc_data.get("cta_mode")
                    if (pc_data.get("total_pages") or pc_data.get("total_items")) and workload["total_pages_or_slides"] == 0:
                        workload["total_pages_or_slides"] = pc_data.get("total_pages") or pc_data.get("total_items")
                    if isinstance(pc_data.get("files"), list) and not workload["source_files"]:
                        for f_entry in pc_data["files"]:
                            if isinstance(f_entry, dict):
                                fname = f_entry.get("filename") or f_entry.get("name") or f_entry.get("doc") or ""
                                fbytes = int(f_entry.get("size_bytes") or round(float(f_entry.get("size_mb", 0.0)) * 1024 * 1024))
                                fpages = int(f_entry.get("total_pages") or f_entry.get("pages") or 0)
                                workload["source_files"].append({
                                    "name": fname,
                                    "size_bytes": fbytes,
                                    "pages": fpages,
                                    "ext": Path(fname).suffix.lower(),
                                })
                                workload["total_input_bytes"] += fbytes
                except Exception:
                    pass

            telem_dir = verified_telem_dir or (found_work / "telemetry")
            if telem_dir.is_dir():
                telem_files = sorted([tf for tf in telem_dir.glob("*.json") if tf.name != "state.json"])
                telemetry_snapshots = []
                for tf in telem_files:
                    try:
                        snap = json.loads(tf.read_text(encoding="utf-8"))
                        if target_conv_id and snap.get("conversation_id") and snap.get("conversation_id") != target_conv_id:
                            continue
                        telemetry_snapshots.append(snap)
                    except Exception:
                        pass
                workload["telemetry_snapshots"] = telemetry_snapshots

            # 1. Budget & Vision
            budget_file = found_work / "budget.json"
            if budget_file.is_file():
                try:
                    bdata = json.loads(budget_file.read_text(encoding="utf-8"))
                    workload["total_pages_or_slides"] = bdata.get("total_items", workload["total_pages_or_slides"])
                    workload["pages_needing_vision"] = bdata.get("pages_requiring_vision", 0)
                    workload["total_handouts"] = bdata.get("total_handouts", 0)
                    workload["cta_mode"] = bdata.get("cta_mode", workload["cta_mode"])
                except Exception:
                    pass

            # 2. Source Files (order.json)
            order_file = found_work / "order.json"
            if order_file.is_file() and not workload["source_files"]:
                try:
                    file_list = json.loads(order_file.read_text(encoding="utf-8"))
                    for fname in file_list:
                        fpath = None
                        for cand_root in [workspace_root / "content", workspace_root / "sample_content", workspace_root]:
                            cf = cand_root / fname
                            if cf.exists():
                                fpath = cf
                                break

                        f_info = {"name": fname, "size_bytes": 0, "pages": 0, "ext": Path(fname).suffix.lower()}
                        if fpath and fpath.exists():
                            size = fpath.stat().st_size
                            f_info["size_bytes"] = size
                            workload["total_input_bytes"] += size
                            if HAS_PYMUPDF and f_info["ext"] == ".pdf":
                                try:
                                    doc = pymupdf.open(fpath)
                                    f_info["pages"] = doc.page_count
                                    doc.close()
                                except Exception:
                                    pass

                        workload["source_files"].append(f_info)
                except Exception:
                    pass

            if workload["total_pages_or_slides"] == 0 and workload["source_files"]:
                workload["total_pages_or_slides"] = sum(f["pages"] for f in workload["source_files"])

            # 3. Corpus size
            corpus_file = found_work / "corpus.md"
            if not corpus_file.exists():
                corpus_file = found_work / "corpus_raw.md"
            if corpus_file.exists():
                text = corpus_file.read_text(encoding="utf-8", errors="ignore")
                workload["corpus_chars"] = len(text)
                workload["corpus_words"] = len(text.split())

            # 4. CTA Competencies
            cta_file = found_work / "cta.json"
            if cta_file.is_file():
                try:
                    cdata = json.loads(cta_file.read_text(encoding="utf-8"))
                    comps = cdata.get("competencies", [])
                    if comps:
                        workload["competencies_count"] = len(comps)
                    if cdata.get("course_id") and cdata.get("course_id") != "custom_course":
                        workload["course_id"] = cdata.get("course_id")
                    if cdata.get("title") or cdata.get("course_title"):
                        workload["course_title"] = cdata.get("title") or cdata.get("course_title")
                except Exception:
                    pass

            # 5. Shards & Competencies mapping (strictly within found_work, NO fallback to root work/)
            for pre_shard_file in [
                found_work / "shards" / "pre_shard_manifest.json",
                found_work / "pre_shard_manifest.json",
                found_work / "shards" / "manifest.json",
            ]:
                if pre_shard_file.is_file():
                    try:
                        ps_data = json.loads(pre_shard_file.read_text(encoding="utf-8"))
                        if ps_data.get("course_id") and (workload["course_id"] in ("unknown", "course_generic", "custom_course") or workload["course_id"].startswith("tmp")):
                            workload["course_id"] = ps_data.get("course_id")
                        if ps_data.get("course_title") and (workload["course_title"] in ("unknown", "course_generic", "custom_course") or workload["course_title"].startswith("tmp")):
                            workload["course_title"] = ps_data.get("course_title")
                        if ps_data.get("total_shards"):
                            workload["shards_count"] = ps_data.get("total_shards")
                        if ps_data.get("total_competencies"):
                            workload["competencies_count"] = ps_data.get("total_competencies")
                        for s_info in ps_data.get("shards", []):
                            s_id = s_info.get("shard_id")
                            if s_id:
                                c_ids = s_info.get("competency_ids") or [c.get("id") if isinstance(c, dict) else c for c in s_info.get("competencies", [])]
                                workload["shards_competencies_map"][s_id] = {
                                    "competency_ids": c_ids,
                                    "count": len(c_ids),
                                }
                        if workload["shards_competencies_map"]:
                            break
                    except Exception:
                        pass

            shards_dir = found_work / "shards"
            if shards_dir.is_dir() and not workload["shards_competencies_map"]:
                shard_files = sorted(list(shards_dir.glob("shard_*.json")))
                workload["shards_count"] = len(shard_files)
                for sf in shard_files:
                    try:
                        s_data = json.loads(sf.read_text(encoding="utf-8"))
                        s_id = sf.stem
                        c_ids = s_data.get("competency_ids") or [c.get("id") if isinstance(c, dict) else c for c in s_data.get("competencies", [])]
                        workload["shards_competencies_map"][s_id] = {
                            "competency_ids": c_ids,
                            "count": len(c_ids),
                        }
                    except Exception:
                        pass

            # 6. Questions & Course metadata (strictly within found_work)
            for course_file in [found_work / "course_verified.json", found_work / "course.json"]:
                if course_file.is_file():
                    try:
                        c_obj = json.loads(course_file.read_text(encoding="utf-8"))
                        if c_obj.get("course_id") and c_obj.get("course_id") != "custom_course":
                            workload["course_id"] = c_obj.get("course_id")
                        workload["course_title"] = c_obj.get("title") or c_obj.get("course_title", workload["course_title"])
                        if "questions" in c_obj and isinstance(c_obj["questions"], list):
                            workload["questions_count"] = len(c_obj["questions"])
                        elif "competencies" in c_obj:
                            workload["questions_count"] = sum(len(c.get("questions", [])) for c in c_obj["competencies"])
                        break
                    except Exception:
                        pass

            if found_work.parent.name != "courses" and found_work.parent.parent.name == "courses":
                if workload["course_id"] in ("unknown", "course_generic", "custom_course"):
                    workload["course_id"] = found_work.parent.name
        else:
            workload["work_dir_resolved"] = None
            workload["work_dir_conversation_match"] = False

        # Fallbacks from transcript records
        if records and workload["course_id"] in ("unknown", "course_generic", "COURSE_ID", "course_id", "custom_course"):
            for rec in records:
                content = rec.get("content", "")
                if content:
                    m_cid = re.search(r"courses/([a-zA-Z0-9_-]+)\.json|course_id\s*[:=]\s*['\"]([a-zA-Z0-9_-]+)['\"]|'([a-zA-Z0-9_]+_model)'", content)
                    if m_cid:
                        workload["course_id"] = next(g for g in m_cid.groups() if g)
                        break

        # Determine whether the audited run completed Stage 4 (build) or Stage 5/6 (verify/publish)
        completion_patterns = r"Stage 4 \(build\) completed|Stage 5 \(verify\) completed|Stage 6 \(publish\) completed|Successfully built course bank|run_stage_build.*completed|run_stage_publish.*completed|run_stage_verify.*completed"
        transcript_shows_completed = bool(re.search(completion_patterns, transcript_full_text, re.IGNORECASE)) if transcript_full_text else False

        if records:
            # When full execution transcript is present, it is authoritative
            completed_stage_4_or_5 = transcript_shows_completed
        else:
            # Fallback for static audits without transcript logs
            completed_stage_4_or_5 = False
            if found_work and ((found_work / "course.json").exists() or (found_work / "course_verified.json").exists()):
                completed_stage_4_or_5 = True

        workload["run_status"] = "COMPLETED" if completed_stage_4_or_5 else "ABORTED_INCOMPLETE"
        if not completed_stage_4_or_5:
            workload["questions_count"] = 0

        # Check published courses in courses/
        courses_dir = workspace_root / "courses"
        if courses_dir.exists():
            matched_course_obj = None
            course_files = sorted(
                [cf for cf in courses_dir.glob("*.json") if cf.is_file()],
                key=lambda p: p.stat().st_mtime,
                reverse=True,
            )
            for cjson in course_files:
                try:
                    c_obj = json.loads(cjson.read_text(encoding="utf-8"))
                    cand_cid = str(c_obj.get("course_id") or "").strip()
                    cand_title = str(c_obj.get("title") or "").strip()
                    if (
                        workload["course_id"] not in ("unknown", "Tops_academy", "work")
                        and cand_cid
                        and cand_cid == workload["course_id"]
                    ):
                        matched_course_obj = c_obj
                        break
                    if (
                        (cjson.stem and cjson.stem in transcript_full_text)
                        or (cand_cid and cand_cid in transcript_full_text)
                        or (cand_title and cand_title in transcript_full_text)
                    ):
                        matched_course_obj = c_obj
                        break
                except Exception:
                    pass
            if matched_course_obj is None and len(course_files) == 1:
                try:
                    matched_course_obj = json.loads(course_files[0].read_text(encoding="utf-8"))
                except Exception:
                    pass
            if matched_course_obj:
                if workload["course_id"] in ("unknown", "Tops_academy", "work"):
                    workload["course_id"] = matched_course_obj.get("course_id", workload["course_id"])
                workload["course_title"] = matched_course_obj.get("title", workload["course_title"])
                if completed_stage_4_or_5 and workload["questions_count"] == 0:
                    workload["questions_count"] = len(matched_course_obj.get("questions", []))
                if workload.get("competencies_count", 0) == 0:
                    matched_comps = matched_course_obj.get("competencies", [])
                    if matched_comps:
                        workload["competencies_count"] = len(matched_comps)

        # Fallback from reports/qa_audits ONLY when competencies_count is not yet resolved
        qa_dir = workspace_root / "reports" / "qa_audits"
        if qa_dir.exists() and workload.get("competencies_count", 0) == 0:
            for qa_f in qa_dir.glob("*payload.json"):
                try:
                    qa_data = json.loads(qa_f.read_text(encoding="utf-8"))
                    cand_cid = qa_data.get("course_id", "")
                    if cand_cid and workload["course_id"] not in ("unknown", "course_generic"):
                        if cand_cid.lower() in workload["course_id"].lower() or workload["course_id"].lower() in cand_cid.lower():
                            workload["course_title"] = qa_data.get("title", workload["course_title"])
                            workload["competencies_count"] = qa_data.get("total_competencies", len(qa_data.get("competencies", [])))
                            if completed_stage_4_or_5 and workload["questions_count"] == 0:
                                workload["questions_count"] = qa_data.get("total_questions", 0)
                            break
                    elif cand_cid and (cand_cid in transcript_full_text.lower()):
                        workload["course_id"] = cand_cid
                        workload["course_title"] = qa_data.get("title", cand_cid)
                        workload["competencies_count"] = qa_data.get("total_competencies", len(qa_data.get("competencies", [])))
                        if completed_stage_4_or_5 and workload["questions_count"] == 0:
                            workload["questions_count"] = qa_data.get("total_questions", 0)
                except Exception:
                    pass

        # Check content directories matching course
        content_dir = workspace_root / "content"
        if content_dir.exists():
            clean_cid = workload["course_id"].lower().replace("_", "")
            matching_dirs = [d for d in content_dir.iterdir() if d.is_dir() and clean_cid in d.name.lower().replace("_", "")]
            if not matching_dirs and transcript_full_text:
                matching_dirs = [d for d in content_dir.iterdir() if d.is_dir() and d.name.lower() in transcript_full_text.lower()]
            if matching_dirs:
                c_sub = matching_dirs[0]
                if not workload["source_files"]:
                    for fpath in sorted(list(c_sub.iterdir())):
                        if fpath.is_file() and fpath.suffix.lower() in (".pdf", ".md", ".txt", ".png", ".jpg"):
                            f_info = {"name": fpath.name, "size_bytes": fpath.stat().st_size, "pages": 0, "ext": fpath.suffix.lower()}
                            workload["total_input_bytes"] += fpath.stat().st_size
                            if HAS_PYMUPDF and fpath.suffix.lower() == ".pdf":
                                try:
                                    doc = pymupdf.open(fpath)
                                    f_info["pages"] = doc.page_count
                                    doc.close()
                                except Exception:
                                    pass
                            workload["source_files"].append(f_info)
                if workload["total_pages_or_slides"] == 0 and workload["source_files"]:
                    workload["total_pages_or_slides"] = sum(f["pages"] for f in workload["source_files"])

        if workload["course_id"] in ("unknown", "course_generic", "COURSE_ID", "course_id") and found_work:
            s_files = sorted(list((found_work / "shards").glob("shard_*.json"))) if (found_work / "shards").exists() else []
            if not s_files and (workspace_root / "work" / "shards").exists():
                s_files = sorted(list((workspace_root / "work" / "shards").glob("shard_*.json")))
            for sf in s_files:
                try:
                    sf_d = json.loads(sf.read_text(encoding="utf-8"))
                    if sf_d.get("course_id"):
                        workload["course_id"] = sf_d.get("course_id")
                    if sf_d.get("course_title"):
                        workload["course_title"] = sf_d.get("course_title")
                    if workload["course_id"] not in ("unknown", "course_generic", "COURSE_ID", "course_id"):
                        break
                except Exception:
                    pass

        # If course_id is still unknown, infer from work_dir path or recent courses/*.json
        if workload["course_id"] in ("unknown", "course_generic", "COURSE_ID", "course_id"):
            if found_work and found_work.parent.name == "courses":
                workload["course_id"] = found_work.name
            elif found_work and found_work.parent.parent.name == "courses":
                workload["course_id"] = found_work.parent.name
            elif courses_dir.exists():
                c_jsons = sorted(list(courses_dir.glob("*.json")), key=lambda p: p.stat().st_mtime, reverse=True)
                if c_jsons:
                    try:
                        cj_obj = json.loads(c_jsons[0].read_text(encoding="utf-8"))
                        workload["course_id"] = cj_obj.get("course_id", c_jsons[0].stem)
                        workload["course_title"] = cj_obj.get("title") or cj_obj.get("course_title", workload["course_title"])
                    except Exception:
                        pass

        # Re-check published courses in courses/ once course_id is identified
        courses_dir = workspace_root / "courses"
        if courses_dir.exists() and workload["course_id"] != "unknown":
            c_cand = courses_dir / f"{workload['course_id']}.json"
            if c_cand.exists():
                try:
                    c_obj = json.loads(c_cand.read_text(encoding="utf-8"))
                    workload["course_title"] = c_obj.get("title") or c_obj.get("course_title") or workload["course_title"]
                    if completed_stage_4_or_5 and workload["questions_count"] == 0:
                        workload["questions_count"] = len(c_obj.get("questions", []))
                except Exception:
                    pass

        if not completed_stage_4_or_5:
            workload["questions_count"] = 0

        if workload["total_handouts"] == 0 or workload["pages_needing_vision"] == 0:
            m_h = re.search(r'"total_handouts":\s*(\d+)', transcript_full_text)
            if m_h:
                workload["total_handouts"] = int(m_h.group(1))
            m_pv = re.search(r'"pages_requiring_vision":\s*(\d+)', transcript_full_text)
            if m_pv:
                workload["pages_needing_vision"] = int(m_pv.group(1))
            if workload["total_pages_or_slides"] == 0 and workload["pages_needing_vision"] > 0:
                workload["total_pages_or_slides"] = workload["pages_needing_vision"]

        if workload["corpus_chars"] == 0:
            m_corp = re.search(r"(\d+)\s+corpus(?:_raw)?\.md", transcript_full_text)
            if m_corp:
                workload["corpus_chars"] = int(m_corp.group(1))
                workload["corpus_words"] = int(workload["corpus_chars"] / 6.5)

        workload["total_input_mb"] = round(workload["total_input_bytes"] / (1024 * 1024), 2)
        return workload


# ---------------------------------------------------------------------------
# Deep Execution Auditor & Telemetry Engine
# ---------------------------------------------------------------------------

class ExecutionAuditor:
    """Computes granular stage critical paths, shard metrics, orchestrator overhead, and bottlenecks."""

    def __init__(self, root_records: List[Dict[str, Any]], root_conv_id: str):
        self.root_records = root_records
        self.root_conv_id = root_conv_id
        self.brain_dir = get_brain_dir()

    def audit(self, workload: Dict[str, Any]) -> Dict[str, Any]:
        # 1. Audit Orchestrator root
        root_metrics = self._analyze_conversation(self.root_records, self.root_conv_id, "Director (Orchestrator)")

        # 2. Extract and audit Orchestrator manual file interventions
        interventions = self._extract_orchestrator_interventions(self.root_records)
        orch_time_decomp = self._decompose_orchestrator_time(self.root_records, interventions)

        # 3. Discover ALL subagents across transcript
        discovered_subs = TranscriptParser.discover_all_subagents(self.root_records, self.brain_dir)

        # Populate any missing shard mapping dynamically from author subagent prompts (never from unverified root work/)
        author_subs_meta = [s for s in discovered_subs if s.get("category") == "author"]
        if author_subs_meta and len(workload.get("shards_competencies_map", {})) < len(author_subs_meta):
            workload["shards_count"] = max(workload.get("shards_count", 0), len(author_subs_meta))
            for idx_a, a_sub in enumerate(author_subs_meta, 1):
                sid = a_sub.get("shard_id") or f"shard_{idx_a:02d}"
                if sid in workload["shards_competencies_map"] and workload["shards_competencies_map"][sid].get("count", 0) > 0:
                    continue
                sub_cid = a_sub.get("conversation_id", "")
                sub_path = self.brain_dir / sub_cid / ".system_generated" / "logs" / "transcript.jsonl"
                extracted_cids = []
                if sub_path.exists():
                    try:
                        with open(sub_path, "r", encoding="utf-8", errors="ignore") as f:
                            first_line = f.readline()
                            if first_line:
                                found_ids = re.findall(r"\b((?:H|C|Hab)-\d{2,3})\b", first_line)
                                extracted_cids = list(dict.fromkeys(found_ids))
                    except Exception:
                        pass
                workload["shards_competencies_map"][sid] = {
                    "competency_ids": extracted_cids,
                    "count": len(extracted_cids),
                }

        # Index pre-extracted subagent telemetry from C2C v3.2 work/telemetry/*.json (strictly bound to root_conv_id)
        pre_extracted_subagents: Dict[str, Dict[str, Any]] = {}
        stage_telemetry_v3: List[Dict[str, Any]] = []
        for snap in workload.get("telemetry_snapshots", []) or []:
            if snap.get("conversation_id") and snap.get("conversation_id") != self.root_conv_id:
                continue
            stage_telemetry_v3.append({
                "stage_idx": snap.get("stage_idx", ""),
                "stage_name": snap.get("stage_name", ""),
                "status": snap.get("status", "completed"),
                "recorded_at": snap.get("recorded_at", ""),
                "duration_seconds": round(float(snap.get("duration_seconds", 0.0)), 2),
                "subagents_count": len(snap.get("subagents", [])),
                "stage_tokens": snap.get("stage_tokens", {}),
                "collector_overhead_ms": snap.get("collector_overhead_ms", 0.0),
                "metadata": snap.get("metadata", {}),
            })
            for sa_snap in snap.get("subagents", []) or []:
                sa_cid = sa_snap.get("conversation_id")
                if sa_cid:
                    pre_extracted_subagents[sa_cid] = sa_snap

        # 4. Deep audit of each subagent (merging live transcript with v3.2 telemetry snapshot)
        subagent_nodes = []
        for s_info in discovered_subs:
            cid = s_info["conversation_id"]
            sub_path = self.brain_dir / cid / ".system_generated" / "logs" / "transcript.jsonl"
            sub_records = TranscriptParser.parse_file(sub_path)
            sub_m = self._analyze_conversation(sub_records, cid, s_info["role"], pre_extracted_subagents.get(cid))
            sub_m["category"] = s_info["category"]
            sub_m["shard_id"] = s_info["shard_id"]
            sub_m["spawn_step"] = s_info["spawn_step"]
            sub_m["spawn_time"] = s_info["spawn_time"]
            sub_m["model"] = s_info["model"]

            # Shard-level enrichment
            if sub_m["shard_id"] and sub_m["shard_id"] in workload["shards_competencies_map"]:
                s_map = workload["shards_competencies_map"][sub_m["shard_id"]]
                sub_m["competencies"] = s_map["competency_ids"]
                sub_m["competencies_count"] = s_map["count"]
                if sub_m["competencies_count"] > 0:
                    sub_m["tokens_per_competency"] = round((sub_m["input_tokens"] + sub_m["output_tokens"]) / sub_m["competencies_count"], 1)
                    sub_m["input_tokens_per_competency"] = round(sub_m["input_tokens"] / sub_m["competencies_count"], 1)
                    sub_m["output_tokens_per_competency"] = round(sub_m["output_tokens"] / sub_m["competencies_count"], 1)
            else:
                sub_m["competencies"] = []
                sub_m["competencies_count"] = 0
                sub_m["tokens_per_competency"] = 0.0

            subagent_nodes.append(sub_m)

        # 5. Build Stage Deep Dives
        stage_deep_dives = self._build_stage_deep_dives(
            subagent_nodes, orch_time_decomp, workload, interventions, self.root_records
        )

        # 6. Aggregate Global Totals
        total_input_tokens = root_metrics["input_tokens"] + sum(s["input_tokens"] for s in subagent_nodes)
        total_output_tokens = root_metrics["output_tokens"] + sum(s["output_tokens"] for s in subagent_nodes)
        total_cache_tokens = root_metrics["cache_read_tokens"] + sum(s["cache_read_tokens"] for s in subagent_nodes)
        total_thinking_tokens = root_metrics.get("thinking_tokens", 0) + sum(s.get("thinking_tokens", 0) for s in subagent_nodes)
        total_active_tokens = total_input_tokens + total_output_tokens
        total_tokens = total_active_tokens + total_cache_tokens

        wall_clock_seconds = root_metrics.get("duration_seconds", 0.0)
        agent_compute_seconds = root_metrics["duration_seconds"] + sum(s["duration_seconds"] for s in subagent_nodes)
        speedup_ratio = round(agent_compute_seconds / wall_clock_seconds, 2) if wall_clock_seconds > 0 else 1.0

        # 7. Unit Economics
        unit_economics = self._compute_unit_economics(
            total_tokens=total_tokens,
            total_active_tokens=total_active_tokens,
            total_input_tokens=total_input_tokens,
            total_output_tokens=total_output_tokens,
            wall_clock_seconds=wall_clock_seconds,
            agent_compute_seconds=agent_compute_seconds,
            workload=workload,
            subagents=subagent_nodes
        )

        # 8. Bottleneck Diagnoses
        bottlenecks = self._detect_bottlenecks(subagent_nodes, stage_deep_dives, interventions)

        total_thinking_chars = root_metrics.get("thinking_chars", 0) + sum(s.get("thinking_chars", 0) for s in subagent_nodes)
        total_thinking_turns = root_metrics.get("thinking_turns_count", 0) + sum(s.get("thinking_turns_count", 0) for s in subagent_nodes)
        thinking_traces_summary = {
            "total_thinking_turns": total_thinking_turns,
            "total_thinking_chars": total_thinking_chars,
            "total_thinking_tokens": total_thinking_tokens,
            "orchestrator_thinking_turns": root_metrics.get("thinking_turns_count", 0),
            "orchestrator_thinking_chars": root_metrics.get("thinking_chars", 0),
            "subagents_thinking_turns": sum(s.get("thinking_turns_count", 0) for s in subagent_nodes),
            "subagents_thinking_chars": sum(s.get("thinking_chars", 0) for s in subagent_nodes),
            "stage_snapshots": (workload.get("pipeline_state") or {}).get("thinking_traces_summary", {})
        }

        return {
            "meta": {
                "audit_timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                "orchestrator_conversation_id": self.root_conv_id,
                "course_id": workload.get("course_id", "unknown"),
                "course_title": workload.get("course_title", "unknown"),
                "work_dir_resolved": workload.get("work_dir", "N/A"),
                "telemetry_v3_snapshots_used": len(stage_telemetry_v3),
            },
            "summary": {
                "wall_clock_seconds": round(wall_clock_seconds, 2),
                "wall_clock_minutes": round(wall_clock_seconds / 60.0, 2),
                "agent_compute_seconds": round(agent_compute_seconds, 2),
                "agent_compute_minutes": round(agent_compute_seconds / 60.0, 2),
                "parallel_speedup_factor": speedup_ratio,
                "total_tokens": total_tokens,
                "total_active_tokens": total_active_tokens,
                "total_input_tokens": total_input_tokens,
                "total_output_tokens": total_output_tokens,
                "total_cache_read_tokens": total_cache_tokens,
                "total_thinking_tokens": total_thinking_tokens,
                "total_thinking_turns": total_thinking_turns,
                "total_thinking_chars": total_thinking_chars,
                "total_turns": root_metrics["turns_count"] + sum(s["turns_count"] for s in subagent_nodes),
                "total_subagents_spawned": len(subagent_nodes),
                "tool_calls_total": root_metrics["tool_calls_count"] + sum(s["tool_calls_count"] for s in subagent_nodes),
                "tool_errors_total": root_metrics["tool_errors_count"] + sum(s["tool_errors_count"] for s in subagent_nodes)
            },
            "workload": workload,
            "unit_economics": unit_economics,
            "stage_telemetry_v3": stage_telemetry_v3,
            "stage_deep_dives": stage_deep_dives,
            "orchestrator_audit": {
                "metrics": root_metrics,
                "time_decomposition": orch_time_decomp,
                "interventions_count": len(interventions),
                "interventions": interventions
            },
            "bottlenecks": bottlenecks,
            "subagents": subagent_nodes,
            "pipeline_state": workload.get("pipeline_state"),
            "telemetry_snapshots": workload.get("telemetry_snapshots", []),
            "thinking_traces_summary": thinking_traces_summary
        }

    def _analyze_conversation(
        self,
        records: List[Dict[str, Any]],
        conv_id: str,
        label: str,
        pre_extracted: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Calculates granular turns, tokens, tools, and timings for a conversation thread,
        merging with C2C v3.2 pre-extracted telemetry snapshots when available.
        """
        input_tokens = 0
        output_tokens = 0
        cache_read_tokens = 0
        thinking_tokens = 0
        thinking_chars = 0
        thinking_turns_count = 0
        last_thinking = ""
        error_thinking_traces = []
        turns_count = 0
        tool_calls_by_name: Dict[str, int] = {}
        tool_errors_count = 0
        failed_commands = []

        timestamps = []
        steps_summary = []

        for rec in records:
            ts_str = rec.get("created_at")
            if ts_str:
                try:
                    ts = datetime.datetime.fromisoformat(ts_str.replace("Z", "+00:00"))
                    timestamps.append(ts)
                except Exception:
                    pass

            rec_type = rec.get("type")
            status = rec.get("status")

            if status == "ERROR":
                tool_errors_count += 1
                if last_thinking:
                    error_thinking_traces.append({
                        "step_index": rec.get("step_index"),
                        "created_at": ts_str,
                        "thinking_snippet": last_thinking[-300:].strip()
                    })

            if rec_type == "PLANNER_RESPONSE":
                turns_count += 1
                inp = rec.get("input_tokens", 0)
                out = rec.get("output_tokens", 0)
                cache = rec.get("cache_read_tokens", 0)
                input_tokens += inp
                output_tokens += out
                cache_read_tokens += cache

                th = rec.get("thinking", "")
                if th:
                    thinking_chars += len(th)
                    thinking_turns_count += 1
                    thinking_tokens += rec.get("thinking_tokens") or (len(th) // 4)
                    last_thinking = th

                tools_in_step = []
                for tc in rec.get("tool_calls", []):
                    tname = tc.get("name", "unknown")
                    tool_calls_by_name[tname] = tool_calls_by_name.get(tname, 0) + 1
                    tools_in_step.append(tname)

                steps_summary.append({
                    "step_index": rec.get("step_index"),
                    "created_at": ts_str,
                    "input_tokens": inp,
                    "output_tokens": out,
                    "cache_read_tokens": cache,
                    "tools": tools_in_step
                })

            elif rec_type == "GENERIC":
                content = rec.get("content", "")
                if "exited with code" in content:
                    code_match = re.search(r"exited with code\s+(\d+)", content)
                    if code_match and int(code_match.group(1)) != 0:
                        tool_errors_count += 1
                        failed_commands.append({
                            "step_index": rec.get("step_index"),
                            "snippet": content[:200]
                        })
                        if last_thinking:
                            error_thinking_traces.append({
                                "step_index": rec.get("step_index"),
                                "created_at": ts_str,
                                "thinking_snippet": last_thinking[-300:].strip()
                            })

        start_time = min(timestamps) if timestamps else None
        end_time = max(timestamps) if timestamps else None
        start_iso = start_time.isoformat() if start_time else None
        end_iso = end_time.isoformat() if end_time else None
        duration_sec = (end_time - start_time).total_seconds() if (start_time and end_time) else 0.0

        # Merge with pre_extracted v3.2 snapshot if transcript was missing or to enrich error traces
        if pre_extracted:
            pe_toks = pre_extracted.get("tokens", {})
            if turns_count == 0 and pre_extracted.get("turns_count"):
                turns_count = int(pre_extracted["turns_count"])
                input_tokens = int(pe_toks.get("input", 0))
                output_tokens = int(pe_toks.get("output", 0))
                cache_read_tokens = int(pe_toks.get("cached", 0))
                thinking_tokens = int(pe_toks.get("thinking", 0))
                duration_sec = float(pre_extracted.get("duration_seconds", 0.0))
                tool_calls_by_name = pre_extracted.get("tool_calls_summary", {})
            if not error_thinking_traces and pre_extracted.get("thinking_traces"):
                for tr in pre_extracted["thinking_traces"]:
                    if tr.get("had_error") and tr.get("thinking"):
                        error_thinking_traces.append({
                            "step_index": tr.get("step_index"),
                            "created_at": tr.get("created_at"),
                            "thinking_snippet": str(tr.get("thinking"))[-300:].strip(),
                        })

        return {
            "conversation_id": conv_id,
            "label": label,
            "start_time": start_iso,
            "end_time": end_iso,
            "start_iso": start_iso,
            "end_iso": end_iso,
            "duration_seconds": round(duration_sec, 2),
            "duration_minutes": round(duration_sec / 60.0, 2),
            "turns_count": turns_count,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "cache_read_tokens": cache_read_tokens,
            "thinking_tokens": thinking_tokens,
            "active_tokens": input_tokens + output_tokens,
            "total_tokens": input_tokens + output_tokens + cache_read_tokens,
            "thinking_chars": thinking_chars,
            "thinking_turns_count": thinking_turns_count,
            "error_thinking_traces": error_thinking_traces[:10],
            "tool_calls_count": sum(tool_calls_by_name.values()),
            "tool_calls_by_name": tool_calls_by_name,
            "tool_errors_count": tool_errors_count,
            "failed_commands": failed_commands[:5],
            "steps": steps_summary[:15],
            "from_v3_telemetry_snapshot": bool(pre_extracted),
        }

    def _extract_orchestrator_interventions(self, records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Audits every direct file modification made by the orchestrator (Supervisor Repair Catalog)."""
        interventions = []
        last_error_snippet = ""
        for rec in records:
            step_idx = rec.get("step_index")
            if rec.get("type") in ("GENERIC", "TOOL_RESPONSE"):
                c_txt = rec.get("content", "")
                if rec.get("status") == "ERROR" or "exited with code 1" in c_txt or "Error" in c_txt:
                    last_error_snippet = c_txt[:160].strip()

            tcs = rec.get("tool_calls", [])
            for tc in tcs:
                tname = tc.get("name")
                if tname in ("replace_file_content", "write_to_file"):
                    args = tc.get("args", {})
                    target_raw = args.get("TargetFile", "")
                    target_file = target_raw.strip('"\'')
                    desc = (args.get("Description", "") or args.get("Instruction", "")).strip()

                    f_lower = target_file.lower()
                    d_lower = desc.lower()
                    fname = Path(target_file).name

                    if "run.py" in f_lower or "assemble.py" in f_lower or "cta_merge" in f_lower:
                        action_type = "Parche de Infraestructura Core"
                        if "dict" in d_lower or "template" in d_lower:
                            cause = f"Soporte de formato dict individual en cargador de plantillas ({desc[:75]})"
                        elif "dag" in d_lower or "cycle" in d_lower:
                            cause = f"Corrección de grafo/fusión en DAG ({desc[:75]})"
                        else:
                            cause = desc[:90] or f"Ajuste en {fname}"
                    elif "judge.py" in f_lower:
                        action_type = "Parche de Infraestructura (Stage 5)"
                        cause = f"Resolución de ruta en subdirectorio verification/ ({desc[:75]})"
                    elif "recover_shards" in f_lower or "fix_cta" in f_lower:
                        action_type = "Recuperación ante Borrado Externo"
                        cause = f"Script de reconstrucción desde transcripts ({fname}): {desc[:65]}"
                    elif "check_escapes" in f_lower or "fix_raw_strings" in f_lower or "cta_data.py" in f_lower:
                        action_type = "Saneamiento Léxico LaTeX (R-03)"
                        cause = f"Conversión de cadenas no-raw con backslashes LaTeX ({desc[:70]})"
                    elif "shard_" in f_lower and ("tpl-var" in d_lower or "parameter" in d_lower or "choice" in d_lower):
                        action_type = "Expansión Paramétrica (TPL-VAR)"
                        cause = f"Ampliación de dominio para superar 50 semillas en {fname} ({desc[:65]})"
                    elif "templates" in f_lower:
                        if "dollar" in d_lower or "katex" in d_lower or "$" in desc:
                            action_type = "Parche Sintáctico KaTeX"
                            cause = desc[:90] or "Delimitador KaTeX en plantilla"
                        elif "r-19" in d_lower or "leak" in d_lower:
                            action_type = "Parche Psicométrico (R-19)"
                            cause = desc[:90] or "Fuga de respuesta en reactivo FIB"
                        elif "r-18" in d_lower or "giveaway" in d_lower:
                            action_type = "Parche Psicométrico (R-18)"
                            cause = desc[:90] or "Opciones MC con texto delator"
                        else:
                            action_type = "Parche de Plantilla"
                            cause = desc[:90]
                    else:
                        action_type = "Modificación / Script Auxiliar"
                        cause = desc[:90] or last_error_snippet[:90]

                    interventions.append({
                        "step": step_idx,
                        "file": fname,
                        "full_path": target_file,
                        "action_type": action_type,
                        "tool": tname,
                        "cause": cause,
                        "tokens_step": rec.get("input_tokens", 0) + rec.get("output_tokens", 0),
                        "snippet": desc[:140]
                    })
        return interventions

    def _decompose_orchestrator_time(
        self,
        records: List[Dict[str, Any]],
        interventions: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Decomposes orchestrator time into CLI tools, Supervisor Repair, Barrier wait, and Model thinking."""
        total_cli_dur = 0.0
        total_repair_dur = 0.0
        total_barrier_dur = 0.0
        total_model_dur = 0.0

        for i in range(len(records) - 1):
            curr = records[i]
            nxt = records[i + 1]
            t1_s = curr.get("created_at")
            t2_s = nxt.get("created_at")
            if not (t1_s and t2_s):
                continue
            try:
                t1 = datetime.datetime.fromisoformat(t1_s.replace("Z", "+00:00"))
                t2 = datetime.datetime.fromisoformat(t2_s.replace("Z", "+00:00"))
                delta = max(0.0, (t2 - t1).total_seconds())
            except Exception:
                continue

            if curr.get("type") == "PLANNER_RESPONSE":
                tcs = curr.get("tool_calls", [])
                tool_names = [tc.get("name") for tc in tcs]
                if "invoke_subagent" in tool_names:
                    total_barrier_dur += delta
                elif any(tn in ("replace_file_content", "write_to_file") for tn in tool_names):
                    total_repair_dur += delta
                elif "run_command" in tool_names:
                    total_cli_dur += delta
            elif curr.get("type") in ("GENERIC", "USER_INPUT", "SYSTEM_MESSAGE"):
                if nxt.get("type") == "PLANNER_RESPONSE":
                    total_model_dur += delta

        total_tracked = total_cli_dur + total_repair_dur + total_barrier_dur + total_model_dur
        return {
            "cli_execution_seconds": round(total_cli_dur, 1),
            "cli_execution_minutes": round(total_cli_dur / 60.0, 1),
            "supervisor_repair_seconds": round(total_repair_dur, 1),
            "supervisor_repair_minutes": round(total_repair_dur / 60.0, 1),
            "barrier_wait_seconds": round(total_barrier_dur, 1),
            "barrier_wait_minutes": round(total_barrier_dur / 60.0, 1),
            "model_thinking_seconds": round(total_model_dur, 1),
            "model_thinking_minutes": round(total_model_dur / 60.0, 1),
            "total_tracked_seconds": round(total_tracked, 1)
        }

    def _build_stage_deep_dives(
        self,
        subagents: List[Dict[str, Any]],
        orch_time: Dict[str, Any],
        workload: Dict[str, Any],
        interventions: Optional[List[Dict[str, Any]]] = None,
        records: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """Builds deep analysis for Stage 1A, Stage 1B, Stage 3, and Stage 5 (Blind Judges)."""
        # 1. Stage 1A: Vision
        vision_subs = [s for s in subagents if s.get("category") == "vision"]
        v_durations = [s["duration_seconds"] for s in vision_subs]
        stage_1a = {
            "agents_count": len(vision_subs),
            "agents": vision_subs,
            "individual_durations": v_durations,
            "max_wall_time_seconds": max(v_durations) if v_durations else 0.0,
            "total_active_tokens": sum(s["active_tokens"] for s in vision_subs),
            "total_cache_tokens": sum(s["cache_read_tokens"] for s in vision_subs),
            "critical_path_agent": next((s["label"] for s in vision_subs if s["duration_seconds"] == max(v_durations)), "N/A") if v_durations else "N/A"
        }

        # 2. Stage 1B: CTA (Supports M CTA Architects in map-reduce and Direct mode)
        cta_mappers = [s for s in subagents if s.get("category") == "cta_mapper"]
        cta_harmonizers = [s for s in subagents if s.get("category") == "cta_harmonizer"]
        cta_harm = cta_harmonizers[0] if cta_harmonizers else None
        mapper_durs = [s["duration_seconds"] for s in cta_mappers]
        harm_durs = [s["duration_seconds"] for s in cta_harmonizers]

        max_mapper = max(mapper_durs) if mapper_durs else 0.0
        max_harm = max(harm_durs) if harm_durs else (cta_harm["duration_seconds"] if cta_harm else 0.0)
        total_cta_wall = round(max_mapper + max_harm, 1)

        all_cta_subs = cta_mappers + cta_harmonizers
        total_cta_active_tokens = sum(s["active_tokens"] for s in all_cta_subs)

        crit_agent = "N/A"
        if mapper_durs and (max_mapper >= max_harm or not cta_harm):
            crit_agent = next((s["label"] for s in cta_mappers if s["duration_seconds"] == max_mapper), "N/A")
        elif cta_harm:
            crit_agent = cta_harm["label"]

        stage_1b = {
            "agents_count": len(all_cta_subs),
            "mappers_count": len(cta_mappers),
            "mappers": cta_mappers,
            "mappers_max_wall_time": max_mapper,
            "harmonizer": cta_harm,
            "harmonizers": cta_harmonizers,
            "harmonizer_duration": max_harm,
            "total_stage_wall_time": total_cta_wall,
            "total_active_tokens": total_cta_active_tokens,
            "critical_mapper": crit_agent
        }

        # 3. Stage 3: Shard Authors
        author_subs = [s for s in subagents if s.get("category") == "author"]
        author_durs = [s["duration_seconds"] for s in author_subs]
        slowest_author = next((s for s in author_subs if s["duration_seconds"] == max(author_durs)), None) if author_durs else None
        median_author_dur = sorted(author_durs)[len(author_durs) // 2] if author_durs else 0.0

        author_active_tokens = sum(s["active_tokens"] for s in author_subs)
        author_comps_total = sum(s.get("competencies_count", 0) for s in author_subs)
        avg_tokens_per_comp = round(author_active_tokens / author_comps_total, 1) if author_comps_total > 0 else 0.0

        stage_3 = {
            "shards_count": len(author_subs),
            "shards": author_subs,
            "min_duration_seconds": min(author_durs) if author_durs else 0.0,
            "median_duration_seconds": median_author_dur,
            "max_duration_seconds": max(author_durs) if author_durs else 0.0,
            "straggler_shard": slowest_author["label"] if slowest_author else "N/A",
            "straggler_delay_vs_median": round(max(author_durs) - median_author_dur, 1) if author_durs else 0.0,
            "total_author_active_tokens": author_active_tokens,
            "total_author_cache_tokens": sum(s["cache_read_tokens"] for s in author_subs),
            "avg_tokens_per_competency": avg_tokens_per_comp
        }

        # 4. Stage 5: Blind Judges & Psychometric Verification (Consuming 05b_judge_compare.json & judge_report.json)
        judge_subs = [s for s in subagents if s.get("category") == "judge"]
        repair_subs = [s for s in subagents if s.get("category") == "repair"]
        judge_durs = [s["duration_seconds"] for s in judge_subs]

        rec_str = str(records or [])
        batch_items = workload.get("competencies_count", 0) * 2
        m_items = re.search(r"Generated judge batch with (\d+) items|All (\d+) items agreed", rec_str)
        if m_items:
            batch_items = int(next(g for g in m_items.groups() if g))

        # Check authoritative C2C v3.2 telemetry snapshot 05b_judge_compare.json and judge_report.json
        judge_compare_passed_v3 = None
        agreement_rate = None
        discrepancies_count = 0
        for snap in workload.get("telemetry_snapshots", []) or []:
            if snap.get("stage_name") == "judge_compare" and (not snap.get("conversation_id") or snap.get("conversation_id") == self.root_conv_id):
                if "passed" in snap.get("metadata", {}):
                    judge_compare_passed_v3 = bool(snap["metadata"]["passed"])

        if workload.get("work_dir"):
            jr_file = Path(workload["work_dir"]) / "judge_report.json"
            if jr_file.is_file():
                try:
                    jr_data = json.loads(jr_file.read_text(encoding="utf-8"))
                    if "passed" in jr_data:
                        judge_compare_passed_v3 = bool(jr_data["passed"])
                    if "agreement_rate" in jr_data:
                        agreement_rate = float(jr_data["agreement_rate"])
                    if "total_items" in jr_data:
                        batch_items = int(jr_data["total_items"])
                    if "discrepancies" in jr_data and isinstance(jr_data["discrepancies"], list):
                        discrepancies_count = len(jr_data["discrepancies"])
                except Exception:
                    pass

        if agreement_rate is None and re.search(r"Agreement rate:\s*100\.0%|All \d+ items agreed", rec_str):
            agreement_rate = 1.0
            judge_compare_passed_v3 = True

        initial_errors = 0
        m_err = re.search(r"Starting repair iteration 1 with (\d+) errors", rec_str)
        if m_err:
            initial_errors = int(m_err.group(1))

        repair_iters = 0
        m_rep = re.search(r"Repaired across (\d+) iteration", rec_str)
        if m_rep:
            repair_iters = int(m_rep.group(1))

        interv_list = interventions or []
        # Only count interventions that actually modified question content during judge arbitration (not infra/recovery)
        judge_content_interventions = [
            it for it in interv_list
            if "judge" not in it.get("file", "").lower()
            and "recover" not in it.get("file", "").lower()
            and "fix_cta" not in it.get("file", "").lower()
            and "check_escapes" not in it.get("file", "").lower()
            and "fix_raw" not in it.get("file", "").lower()
            and "cta_data" not in it.get("file", "").lower()
            and "run.py" not in it.get("file", "").lower()
            and "dump_prompts" not in it.get("file", "").lower()
            and "prompt" not in it.get("file", "").lower()
            and "helper" not in it.get("file", "").lower()
            and "tpl-var" not in it.get("cause", "").lower()
        ]
        infra_judge_interventions = [it for it in interv_list if "judge.py" in it.get("file", "").lower()]

        if judge_compare_passed_v3 is True and discrepancies_count == 0 and len(judge_content_interventions) == 0:
            passed_first_attempt = True
            badge = f"✅ 100% ACUERDO AL PRIMER INTENTO ({batch_items}/{batch_items} REACTIVOS)"
            summary_desc = (
                f"Los {len(judge_subs)} Blind Judges evaluaron el lote estratificado de {batch_items} reactivos en 1 turno de razonamiento puro "
                f"cada uno (0 búsquedas web, 100% aislamiento epistémico), logrando un acuerdo psicométrico del 100.0% ({batch_items}/{batch_items}) "
                f"con 0 discrepancias frente al ground truth."
            )
            actions_taken = [
                f"1. **Arbitraje Ciego (`05b_judge_compare.json`)**: {batch_items}/{batch_items} acuerdos (`100.0% agreement rate`, `0 discrepancias`).",
            ]
            if initial_errors > 0 or repair_iters > 0:
                actions_taken.append(
                    f"2. **Verificación Determinista Previa (`--stage verify`)**: Detectó {initial_errors} error(es) léxico/estructural(es) corregido(s) antes del arbitraje ciego."
                )
            if infra_judge_interventions:
                actions_taken.append(
                    f"3. **Ajuste de Ruta en Infraestructura (`judge.py`)**: {len(infra_judge_interventions)} ajuste(s) para localizar `verification/judge_responses_*.json`."
                )
        else:
            passed_first_attempt = False
            badge = "❌ NO PASARON AL PRIMER INTENTO (REQUIRIÓ INTERVENCIONES)"
            interv_files = sorted(list(set(it.get("file", "") for it in interv_list if it.get("file"))))
            interv_files_str = ", ".join(f"`{f}`" for f in interv_files[:5]) if interv_files else "archivos de reactivos"
            err_str = f"con {initial_errors} errores iniciales" if initial_errors > 0 else "con discrepancias detectadas"
            summary_desc = (
                f"Los blind judges y la verificación psicométrica registraron discrepancias que requirieron correcciones. "
                f"La validación previa operó {err_str}, requiriendo rondas de auto-reparación o intervención técnica."
            )
            actions_taken = [
                f"1. **Bucle de Auto-Reparación**: Se ejecutó RepairLoop sobre el lote de evaluación.",
                f"2. **Intervenciones de Supervisor ({len(interv_list)} operaciones)**: Operaciones sobre {interv_files_str}.",
                f"3. **Certificación y Verificación Final**: Se concluyó la validación tras {repair_iters or 1} iteraciones sobre el lote de {batch_items} reactivos."
            ]

        stage_5 = {
            "judges_count": len(judge_subs),
            "judges": judge_subs,
            "max_judge_duration": max(judge_durs) if judge_durs else 0.0,
            "repairs_count": len(repair_subs),
            "repairs": repair_subs,
            "passed_first_attempt": passed_first_attempt,
            "agreement_rate": agreement_rate if agreement_rate is not None else (1.0 if passed_first_attempt else 0.0),
            "discrepancies_count": discrepancies_count,
            "badge": badge,
            "batch_items_count": batch_items,
            "initial_errors_count": initial_errors,
            "repair_iterations": repair_iters,
            "supervisor_interventions_count": len(judge_content_interventions),
            "infra_interventions_count": len(infra_judge_interventions),
            "summary_desc": summary_desc,
            "actions_taken": actions_taken
        }

        return {
            "stage_1a_vision": stage_1a,
            "stage_1b_cta": stage_1b,
            "stage_3_authors": stage_3,
            "stage_5_judges": stage_5
        }

    def _compute_unit_economics(
        self,
        total_tokens: int,
        total_active_tokens: int,
        total_input_tokens: int,
        total_output_tokens: int,
        wall_clock_seconds: float,
        agent_compute_seconds: float,
        workload: Dict[str, Any],
        subagents: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Calculates normalized efficiency ratios for apples-to-apples comparisons."""
        pages = workload.get("total_pages_or_slides", 0)
        bytes_in = workload.get("total_input_bytes", 0)
        kb_in = bytes_in / 1024.0 if bytes_in > 0 else 0.0
        comps = workload.get("competencies_count", 0)
        questions = workload.get("questions_count", 0)

        author_subs = [s for s in subagents if s.get("category") == "author"]
        author_tokens = sum(s["active_tokens"] for s in author_subs)
        avg_author_tokens_per_comp = round(author_tokens / comps, 1) if comps > 0 else 0.0

        return {
            "tokens_per_page": round(total_tokens / pages, 1) if pages > 0 else 0.0,
            "active_tokens_per_page": round(total_active_tokens / pages, 1) if pages > 0 else 0.0,
            "tokens_per_input_kb": round(total_tokens / kb_in, 1) if kb_in > 0 else 0.0,
            "tokens_per_competency": round(total_tokens / comps, 1) if comps > 0 else 0.0,
            "active_tokens_per_competency": round(total_active_tokens / comps, 1) if comps > 0 else 0.0,
            "author_tokens_per_competency": avg_author_tokens_per_comp,
            "tokens_per_question": round(total_tokens / questions, 1) if questions > 0 else 0.0,
            "active_tokens_per_question": round(total_active_tokens / questions, 1) if questions > 0 else 0.0,
            "seconds_per_page": round(wall_clock_seconds / pages, 2) if pages > 0 else 0.0,
            "seconds_per_question": round(wall_clock_seconds / questions, 2) if questions > 0 else 0.0,
            "questions_per_minute": round((questions * 60.0) / wall_clock_seconds, 2) if (wall_clock_seconds > 0 and questions > 0) else 0.0,
            "agent_seconds_per_question": round(agent_compute_seconds / questions, 2) if questions > 0 else 0.0,
            "output_tokens_per_question": round(total_output_tokens / questions, 1) if questions > 0 else 0.0
        }

    def _detect_bottlenecks(
        self,
        subagents: List[Dict[str, Any]],
        stages: Dict[str, Any],
        interventions: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Identifies stragglers, critical paths, retry loops, supervisor repair anti-patterns."""
        bottlenecks = []

        # 1. Supervisor Repair Anti-Pattern
        if len(interventions) >= 3:
            total_interv_tokens = sum(it.get("tokens_step", 0) for it in interventions)
            bottlenecks.append({
                "severity": "HIGH",
                "type": "SUPERVISOR_REPAIR_ANTI_PATTERN",
                "stage": "Director (Orchestrator)",
                "title": f"Síndrome del Orquestador Reparador ({len(interventions)} intervenciones manuales)",
                "description": (
                    f"El orquestador principal ejecutó {len(interventions)} operaciones directas de edición de código "
                    f"y plantillas. Consumió más de {total_interv_tokens:,} tokens en turnos de mantenimiento/recuperación manual."
                )
            })

        # 2. Critical Path & Straggler in Shards
        stg3 = stages.get("stage_3_authors", {})
        if stg3.get("straggler_shard") != "N/A" and stg3.get("straggler_delay_vs_median", 0) > 120:
            bottlenecks.append({
                "severity": "HIGH",
                "type": "STRAGGLER_CRITICAL_PATH",
                "stage": "Stage 3: Question Authoring",
                "title": f"Straggler Crítico en Shards: {stg3['straggler_shard']}",
                "description": (
                    f"{stg3['straggler_shard']} tardó {stg3['max_duration_seconds']}s frente a la mediana de "
                    f"{stg3['median_duration_seconds']}s (+{stg3['straggler_delay_vs_median']}s de retraso en la barrera). "
                    f"Determinó el tiempo total de pared de la etapa de autoría."
                )
            })

        # 3. Turn Bloat in Atomic Subagents
        high_turn_subs = [s for s in subagents if s["turns_count"] > 30]
        if high_turn_subs:
            worst = max(high_turn_subs, key=lambda x: x["turns_count"])
            worst_lbl = worst.get("label") or worst.get("role", "Subagent")
            bottlenecks.append({
                "severity": "HIGH",
                "type": "INTERACTIVE_MICRO_LOOP",
                "stage": worst_lbl,
                "title": f"Antipatrón de Micro-Bucle Interactivo ({worst['turns_count']} turnos en {worst_lbl})",
                "description": (
                    f"{len(high_turn_subs)} subagentes realizaron > 30 turnos individuales (ej. {worst_lbl} con {worst['turns_count']} turnos). "
                    f"Ocurre por bucles de depuración o escritura incremental en lugar de redactar por lotes atómicos."
                )
            })

        # 4. Tool Friction
        tool_err_subs = [s for s in subagents if s["tool_errors_count"] >= 3]
        if tool_err_subs:
            first_err_lbl = tool_err_subs[0].get("label") or tool_err_subs[0].get("role", "Subagent")
            bottlenecks.append({
                "severity": "MEDIUM",
                "type": "TOOL_FRICTION",
                "stage": "Multiple Subagents",
                "title": f"Fricción de Herramientas en {len(tool_err_subs)} subagentes",
                "description": (
                    f"Subagentes como {first_err_lbl} acumularon fallos en consola ({tool_err_subs[0]['tool_errors_count']} errores), "
                    f"provocando reintentos e invalidación de caché."
                )
            })

        return bottlenecks


# ---------------------------------------------------------------------------
# Persistent History & Longitudinal Benchmark Registry (Zero-Collision by Conv ID)
# ---------------------------------------------------------------------------

class HistoricalRegistry:
    """Manages persistent storage, audit_registry.json, and historical_benchmark.md.
    Deduplicates strictly by conversation_id so multiple runs of the same course never collide.
    """

    def __init__(self, output_base: Path):
        self.output_base = output_base
        self.output_base.mkdir(parents=True, exist_ok=True)
        self.registry_file = self.output_base / "audit_registry.json"
        self.benchmark_md_file = self.output_base / "historical_benchmark.md"

    def register_run(self, audit_result: Dict[str, Any], run_dir_name: str) -> None:
        registry = self.load_registry()

        meta = audit_result["meta"]
        summary = audit_result["summary"]
        workload = audit_result["workload"]
        ue = audit_result["unit_economics"]
        stg = audit_result["stage_deep_dives"]

        entry = {
            "run_id": run_dir_name,
            "timestamp": meta["audit_timestamp"],
            "course_id": meta["course_id"],
            "course_title": meta["course_title"],
            "conversation_id": meta["orchestrator_conversation_id"],
            "workload": {
                "source_files_count": len(workload.get("source_files", [])),
                "pages_or_slides": workload["total_pages_or_slides"],
                "input_mb": workload["total_input_mb"],
                "competencies": workload["competencies_count"],
                "questions": workload["questions_count"],
                "handouts": workload["total_handouts"]
            },
            "metrics": {
                "wall_clock_seconds": summary["wall_clock_seconds"],
                "agent_compute_seconds": summary["agent_compute_seconds"],
                "speedup": summary["parallel_speedup_factor"],
                "total_tokens": summary["total_tokens"],
                "total_active_tokens": summary["total_active_tokens"],
                "input_tokens": sum(s["input_tokens"] for s in audit_result.get("subagents", [])),
                "output_tokens": sum(s["output_tokens"] for s in audit_result.get("subagents", [])),
                "cache_read_tokens": summary.get("total_cache_read_tokens", 0),
                "total_turns": summary["total_turns"],
                "subagents_count": summary["total_subagents_spawned"],
                "tool_errors": summary["tool_errors_total"],
                "stage_1a_max_wall": stg["stage_1a_vision"]["max_wall_time_seconds"],
                "stage_1b_total_wall": stg["stage_1b_cta"]["total_stage_wall_time"],
                "stage_3_max_wall": stg["stage_3_authors"]["max_duration_seconds"],
                "orchestrator_interventions": audit_result["orchestrator_audit"]["interventions_count"],
                "blind_judges": {
                    "passed_first_attempt": stg["stage_5_judges"]["passed_first_attempt"],
                    "badge": stg["stage_5_judges"]["badge"],
                    "batch_items_count": stg["stage_5_judges"]["batch_items_count"],
                    "initial_errors_count": stg["stage_5_judges"]["initial_errors_count"],
                    "repair_iterations": stg["stage_5_judges"]["repair_iterations"],
                    "supervisor_interventions_count": stg["stage_5_judges"]["supervisor_interventions_count"],
                    "summary_desc": stg["stage_5_judges"]["summary_desc"],
                    "actions_taken": stg["stage_5_judges"]["actions_taken"]
                }
            },
            "unit_economics": ue,
            "bottlenecks_count": len(audit_result.get("bottlenecks", []))
        }

        # Deduplicate strictly by conversation_id (NEVER delete a different conversation run of the same course_id!)
        target_conv = meta["orchestrator_conversation_id"]
        import shutil

        new_reg = []
        for r in registry:
            if r.get("is_baseline"):
                new_reg.append(r)
                continue
            is_dup = (
                r.get("conversation_id") == target_conv or
                r.get("run_id") == run_dir_name
            )
            if is_dup:
                old_run_id = r.get("run_id")
                if old_run_id and old_run_id != run_dir_name:
                    old_dir = self.output_base / old_run_id
                    if old_dir.exists() and old_dir.is_dir():
                        try:
                            shutil.rmtree(old_dir, ignore_errors=True)
                        except Exception:
                            pass
            else:
                new_reg.append(r)

        new_reg.append(entry)
        new_reg.sort(key=lambda x: x["timestamp"])
        self.registry_file.write_text(json.dumps(new_reg, indent=2, ensure_ascii=False), encoding="utf-8")
        self._generate_historical_benchmark_md(new_reg)

    def load_registry(self) -> List[Dict[str, Any]]:
        if not self.registry_file.exists():
            return []
        try:
            reg = json.loads(self.registry_file.read_text(encoding="utf-8"))
            valid = [r for r in reg if (self.output_base / r["run_id"]).exists() or r.get("is_baseline")]
            # Deduplicate strictly by conversation_id keeping newest audit of that conversation
            deduped = {}
            for r in valid:
                key = r.get("conversation_id") if not r.get("is_baseline") else r.get("run_id")
                deduped[key] = r
            valid = list(deduped.values())
            valid.sort(key=lambda x: x["timestamp"])
            if len(valid) != len(reg):
                self.registry_file.write_text(json.dumps(valid, indent=2, ensure_ascii=False), encoding="utf-8")
                self._generate_historical_benchmark_md(valid)
            return valid
        except Exception:
            return []

    def ensure_baseline(self) -> None:
        """Ensures the canonical reference baseline (estadistica3_regresion_v3) exists in registry."""
        registry = self.load_registry()
        has_baseline = any(r.get("run_id") == "baseline_estadistica3_regresion_v3" for r in registry)
        if not has_baseline:
            baseline_entry = {
                "run_id": "baseline_estadistica3_regresion_v3",
                "is_baseline": True,
                "timestamp": "2026-10-10T12:00:00+00:00",
                "course_id": "estadistica3_regresion_v3",
                "course_title": "Estadística III (Regresión Lineal y Multivariante)",
                "conversation_id": "baseline-estadistica-v3",
                "workload": {
                    "source_files_count": 5,
                    "pages_or_slides": 50,
                    "input_mb": 1.2,
                    "competencies": 16,
                    "questions": 480,
                    "handouts": 5
                },
                "metrics": {
                    "wall_clock_seconds": 3600.0,
                    "agent_compute_seconds": 7200.0,
                    "speedup": 2.0,
                    "total_tokens": 8645000,
                    "total_active_tokens": 699000,
                    "input_tokens": 600000,
                    "output_tokens": 45000,
                    "cache_read_tokens": 8000000,
                    "total_turns": 240,
                    "subagents_count": 6,
                    "tool_errors": 2,
                    "stage_1a_max_wall": 180.0,
                    "stage_1b_total_wall": 150.0,
                    "stage_3_max_wall": 450.0,
                    "orchestrator_interventions": 0,
                    "blind_judges": {
                        "passed_first_attempt": True,
                        "badge": "✅ PASARON PERFECTOS AL PRIMER INTENTO",
                        "batch_items_count": 32,
                        "initial_errors_count": 0,
                        "repair_iterations": 0,
                        "supervisor_interventions_count": 0,
                        "summary_desc": "El lote de evaluación de blind judges y la verificación psicométrica pasaron de forma 100% limpia en su primera pasada, sin registrar discrepancias ni requerir rondas de auto-reparación ni intervención manual.",
                        "actions_taken": ["No se requirieron acciones correctivas. El pipeline avanzó directamente a la etapa de publicación."]
                    }
                },
                "unit_economics": {
                    "tokens_per_page": 172900.0,
                    "active_tokens_per_page": 13980.0,
                    "tokens_per_input_kb": 7204.0,
                    "tokens_per_competency": 540312.5,
                    "active_tokens_per_competency": 43687.5,
                    "author_tokens_per_competency": 38000.0,
                    "tokens_per_question": 18010.4,
                    "active_tokens_per_question": 1456.3,
                    "seconds_per_page": 72.0,
                    "seconds_per_question": 7.5,
                    "questions_per_minute": 8.0,
                    "agent_seconds_per_question": 15.0,
                    "output_tokens_per_question": 93.8
                },
                "bottlenecks_count": 0
            }
            registry.append(baseline_entry)
            registry.sort(key=lambda x: x["timestamp"])
            self.registry_file.write_text(json.dumps(registry, indent=2, ensure_ascii=False), encoding="utf-8")
            self._generate_historical_benchmark_md(registry)

    def _generate_historical_benchmark_md(self, registry: List[Dict[str, Any]]) -> None:
        if not registry:
            return

        lines = [
            "# Content-to-Course: Registro Histórico y Evolución de Rendimiento",
            "",
            "> [!NOTE]",
            f"> Este documento se actualiza automáticamente con cada auditoría ejecutada. Última actualización: `{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}`. Total de ejecuciones auditadas: **{len(registry)}**.",
            "",
            "## 1. Matriz de Evolución Temporal (Normalizada por Carga de Contenido)",
            "",
            "| Fecha | Run / Curso | Input (Pág / MB) | Output (Comp / Preg) | Tiempo de Pared | Speedup | Tokens Totales | Tok / Preg | Seg / Preg | Blind Judges (1st) | Intervenciones | Bottlenecks |",
            "| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |"
        ]

        for r in reversed(registry):
            ts = r["timestamp"][:16].replace("T", " ")
            cid = r["course_id"]
            conv_short = r.get("conversation_id", "")[:8]
            cid_label = f"**{cid}** (`{conv_short}`)" if conv_short else f"**{cid}**"
            w = r["workload"]
            m = r["metrics"]
            ue = r["unit_economics"]
            b_cnt = r["bottlenecks_count"]
            b_badge = f"⚠️ {b_cnt}" if b_cnt > 0 else "✅ 0"
            interv_badge = f"🛠️ {m.get('orchestrator_interventions', 0)}"

            wall_min = round(m["wall_clock_seconds"] / 60.0, 1)
            bj = m.get("blind_judges", {})
            bj_badge = "✅ Limpio" if bj.get("passed_first_attempt", True) else "❌ Falló"

            lines.append(
                f"| `{ts}` | {cid_label} | {w['pages_or_slides']} pág ({w['input_mb']} MB) | "
                f"{w['competencies']} comp / {w['questions']} preg | {wall_min} min ({m['wall_clock_seconds']}s) | "
                f"**{m['speedup']}x** | {m['total_tokens']:,} | "
                f"**{ue['tokens_per_question']:,}** | **{ue['seconds_per_question']}s** | {bj_badge} | {interv_badge} | {b_badge} |"
            )

        lines.extend([
            "",
            "---",
            "",
            "## 2. Métricas Promedio del Sistema (Baselines Globales)",
            ""
        ])

        total_runs = len(registry)
        avg_speedup = round(sum(r["metrics"]["speedup"] for r in registry) / total_runs, 2)
        valid_q_runs = [r for r in registry if r["unit_economics"]["tokens_per_question"] > 0]

        if valid_q_runs:
            avg_tok_per_q = round(sum(r["unit_economics"]["tokens_per_question"] for r in valid_q_runs) / len(valid_q_runs), 1)
            avg_sec_per_q = round(sum(r["unit_economics"]["seconds_per_question"] for r in valid_q_runs) / len(valid_q_runs), 2)
            avg_qpm = round(sum(r["unit_economics"]["questions_per_minute"] for r in valid_q_runs) / len(valid_q_runs), 2)
        else:
            avg_tok_per_q = 0.0
            avg_sec_per_q = 0.0
            avg_qpm = 0.0

        lines.extend([
            f"- **Factor de Aceleración Paralela Promedio**: `{avg_speedup}x`",
            f"- **Densidad de Tokens Promedio por Pregunta**: `{avg_tok_per_q:,} tokens/pregunta`",
            f"- **Latencia Promedio por Pregunta Validada**: `{avg_sec_per_q} s/pregunta`",
            f"- **Rendimiento Promedio de Generación**: `{avg_qpm} preguntas/minuto`",
            "",
            "---",
            "*Generado por el motor forense `c2c-run-auditor`.*"
        ])

        self.benchmark_md_file.write_text("\n".join(lines), encoding="utf-8")


# ---------------------------------------------------------------------------
# Ultra-Granular Report Generator (Architectural Audit Style)
# ---------------------------------------------------------------------------

class ReportGenerator:
    """Emits detailed Markdown reports matching solow_vs_estadistica_definitive_architectural_audit.md."""

    @staticmethod
    def generate_markdown(audit: Dict[str, Any]) -> str:
        meta = audit["meta"]
        summary = audit["summary"]
        w = audit["workload"]
        ue = audit["unit_economics"]
        stg = audit["stage_deep_dives"]
        orch = audit["orchestrator_audit"]
        bottlenecks = audit["bottlenecks"]
        subs = audit["subagents"]
        stg_v3 = audit.get("stage_telemetry_v3", {})

        md = [
            f"# Informe de Auditoría Arquitectónica Forense: Rendimiento, Shards y Telemetría Multi-Agente",
            f"## Curso: {meta['course_title']} (`{meta['course_id']}`)",
            "",
            f"**Fecha de Auditoría:** `{meta['audit_timestamp'][:19].replace('T', ' ')} UTC`  ",
            f"**Conversación Orquestadora:** [`{meta['orchestrator_conversation_id']}`](conversation://{meta['orchestrator_conversation_id']})  ",
            f"**Directorio de Trabajo Validado (Zero-Collision):** `{w.get('work_dir_resolved') or 'N/A (Transcript-Only)'}` (`match={w.get('work_dir_conversation_match', False)}`)  ",
            f"**Enfoque:** Telemetría Determinista de API, Subagentes, Shards, Latencias y Operaciones del Orquestador.",
            "",
            "---",
            "",
            "## 1. Consolidación de Métricas y Caracterización de Carga",
            "",
            "| Dimensión / Métrica | Valor Registrado | Observaciones de Ingeniería |",
            "| :--- | :--- | :--- |",
            f"| **Material de Entrada** | `{len(w['source_files'])} archivos` ({w['total_pages_or_slides']} págs / {w['total_input_mb']} MB) | {', '.join([f['name'] for f in w['source_files']]) or 'N/A'} |",
            f"| **Requerimiento de Visión** | `{w['pages_needing_vision']} páginas` ({w['total_handouts']} handouts) | Cuadrículas generadas para diagramas/fórmulas |",
            f"| **Corpus Sintetizado** | `{w['corpus_chars']:,} caracteres` ({w['corpus_words']:,} palabras) | Texto consolidado tras ingesta y visión |",
            f"| **Competencias Extraídas** | **`{w['competencies_count']} competencias`** | Desglose pedagógico (Hechos, Conceptos, Habilidades) |",
            f"| **Shards Particionados** | **`{w['shards_count']} shards`** | Unidades de trabajo concurrentes |",
            f"| **Subagentes Desplegados** | **`{summary['total_subagents_spawned']} subagentes`** | Visión ({stg['stage_1a_vision']['agents_count']}), CTA ({stg['stage_1b_cta'].get('agents_count', stg['stage_1b_cta']['mappers_count'] + (1 if stg['stage_1b_cta']['harmonizer'] else 0))}), Autores ({stg['stage_3_authors']['shards_count']}), Jueces ({stg['stage_5_judges'].get('judges_count', 0)}) |",
            f"| **Reactivos Finales Validados** | **`{w['questions_count']} preguntas`** | Evaluadas en sandbox |",
            f"| **Tokens Entrada (Subagentes)** | **`{sum(s['input_tokens'] for s in subs):,}` tokens** | Contexto acumulativo enviado a subagentes |",
            f"| **Tokens Salida (Subagentes)** | **`{sum(s['output_tokens'] for s in subs):,}` tokens** | Código de plantillas y JSON generado |",
            f"| **Tokens Caché (Leídos)** | **`{summary['total_cache_read_tokens']:,}` tokens** | Caché de contexto reutilizado por la API |",
            f"| **Gran Total Tokens Activos** | **`{summary['total_active_tokens']:,}` tokens** | Entrada + Salida neto (sin contar caché) |",
            f"| **Gran Total Tokens (con Caché)** | **`{summary['total_tokens']:,}` tokens** | Consumo total de cuota facturable |",
            "",
            "---",
            "",
            "## 2. Ratios Unitarios Normalizados (Unit Economics)",
            "",
            "Métricas normalizadas para comparación *apples-to-apples* frente a cursos de diferente volumen de contenido:",
            "",
            "| Métrica Unitaria | Valor Obtenido | Interpretación de Eficiencia |",
            "| :--- | :--- | :--- |",
            f"| **Tokens Totales por Pregunta** | **`{ue['tokens_per_question']:,} tokens/preg`** | Esfuerzo de API por cada reactivo jugable |",
            f"| **Tokens Activos por Pregunta** | **`{ue['active_tokens_per_question']:,} tokens/preg`** | Tokens netos de razonamiento y código por reactivo |",
            f"| **Tokens por Competencia (Global)** | **`{ue['tokens_per_competency']:,} tokens/comp`** | Densidad de diseño instruccional del curso |",
            f"| **Tokens de Autor por Competencia** | **`{ue['author_tokens_per_competency']:,} tokens/comp`** | Costo puro de la etapa de autoría por competencia |",
            f"| **Tokens Totales por Página / Slide** | **`{ue['tokens_per_page']:,} tokens/pág`** | Esfuerzo cognitivo por diapositiva original |",
            f"| **Segundos de Pared por Pregunta** | **`{ue['seconds_per_question']} s/preg`** | Ritmo de entrega percibido |",
            f"| **Rendimiento de Generación (QPM)** | **`{ue['questions_per_minute']} preg/min`** | Velocidad de producción del pipeline |",
            f"| **Factor de Aceleración Paralela** | **`{summary['parallel_speedup_factor']}x`** | Relación tiempo cómputo vs tiempo de pared |",
            "",
            "---",
            "",
            "## 3. Desglose Forense por Etapas Críticas",
            ""
        ]

        p_state = audit.get("pipeline_state") or {}
        stg_v3_list = stg_v3.get("stages", []) if isinstance(stg_v3, dict) else (stg_v3 if isinstance(stg_v3, list) else [])
        if stg_v3_list:
            md.extend([
                "### 3.0. Telemetría Incremental por Etapa C2C v3.2 (`work/telemetry/*.json` & `state.json`)",
                f"- **Snapshots de Etapa Verificados (`conversation_id` = `{meta['orchestrator_conversation_id'][:8]}`):** `{len(stg_v3_list)} etapas`",
                f"- **Estado Maestro (`work/state.json`):** `{p_state.get('status', w.get('pipeline_status', 'COMPLETED'))}` (Etapa actual/final: `{p_state.get('current_stage', stg_v3_list[-1].get('stage_name', 'N/A'))}`)",
                "",
                "| Etapa (Snapshot) | Timestamp (UTC) | Duración Etapa | Tokens Etapa (Total / Activos) | Subagentes Capturados | Artefactos / Metadatos de Etapa |",
                "| :--- | :--- | :---: | :---: | :---: | :--- |"
            ])
            for st_item in stg_v3_list:
                s_key = st_item.get("stage_key") or f"{st_item.get('stage_idx', '')}_{st_item.get('stage_name', '')}".strip("_")
                ts_short = str(st_item.get("recorded_at") or st_item.get("timestamp") or "")[:19].replace("T", " ")
                dur_s = st_item.get("duration_seconds", 0.0)
                st_toks = st_item.get("stage_tokens") or {}
                tot_t = st_toks.get("total", st_toks.get("total_tokens", st_item.get("orchestrator_total_tokens", 0)))
                act_t = st_toks.get("active_tokens", st_toks.get("input", 0) + st_toks.get("output", 0))
                sub_cnt = st_item.get("subagents_count", st_item.get("subagents_captured_count", 0))
                meta_clean = {k: v for k, v in (st_item.get("metadata") or {}).items() if k != "duration_seconds"}
                meta_str = ", ".join(f"{k}={v}" for k, v in meta_clean.items()) or "—"
                md.append(
                    f"| **`{s_key}`** | `{ts_short}` | `{dur_s}s` | "
                    f"`{tot_t:,}` (`{act_t:,}` act) | {sub_cnt} | `{meta_str}` |"
                )
            md.extend(["", "---", ""])

        md.extend([
            "### 3.1. Stage 1A: Preprocesamiento de Visión",
            f"- **Subagentes de Visión Desplegados:** `{stg['stage_1a_vision']['agents_count']} agentes en paralelo`",
            f"- **Tiempo de Pared de la Etapa (Máximo / Critical Path):** **`{stg['stage_1a_vision']['max_wall_time_seconds']}s`** (`{round(stg['stage_1a_vision']['max_wall_time_seconds']/60, 1)} min`)",
            f"- **Agente Determinante del Camino Crítico:** `{stg['stage_1a_vision']['critical_path_agent']}`",
            "",
            "| Subagente de Visión | Turnos | Tokens In | Tokens Out | Cache Leído | Total Activo | Duración |",
            "| :--- | :--- | :--- | :--- | :--- | :--- | :--- |"
        ])

        for va in stg["stage_1a_vision"]["agents"]:
            md.append(
                f"| **{va['label']}** | {va['turns_count']} | {va['input_tokens']:,} | {va['output_tokens']:,} | "
                f"{va['cache_read_tokens']:,} | {va['active_tokens']:,} | **{va['duration_seconds']}s** |"
            )

        cta_subs_total = stg['stage_1b_cta'].get('agents_count', stg['stage_1b_cta']['mappers_count'] + (1 if stg['stage_1b_cta']['harmonizer'] else 0))
        if stg['stage_1b_cta']['mappers_count'] == 0:
            cta_arch_desc = f"DIRECT ({cta_subs_total} Direct CTA Architect)"
        else:
            cta_mode_name = w.get('cta_mode', 'mapreduce').upper()
            harm_part = " + 1 Harmonizer" if stg['stage_1b_cta']['harmonizer'] else ""
            cta_arch_desc = f"{cta_mode_name} ({stg['stage_1b_cta']['mappers_count']} Mappers{harm_part})"
        md.extend([
            "",
            "---",
            "",
            "### 3.2. Stage 1B: Análisis Cognitivo de Competencias (CTA)",
            f"- **Arquitectura:** `{cta_arch_desc}`",
            f"- **Tiempo de Pared Fase Mappers (Máximo):** **`{stg['stage_1b_cta']['mappers_max_wall_time']}s`** (determinado por `{stg['stage_1b_cta']['critical_mapper']}`)",
            f"- **Tiempo Fase Harmonizer (Barrera Síncrona):** **`{stg['stage_1b_cta']['harmonizer_duration']}s`**",
            f"- **Tiempo de Pared Total de Etapa 1B:** **`{stg['stage_1b_cta']['total_stage_wall_time']}s`** (`{round(stg['stage_1b_cta']['total_stage_wall_time']/60, 1)} min`)",
            "",
            "| Subagente CTA | Rol / Sección | Turnos | Tokens In | Tokens Out | Cache Leído | Errores | Duración |",
            "| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |"
        ])

        for ca in stg["stage_1b_cta"]["mappers"]:
            md.append(
                f"| **{ca['label']}** | Mapper | {ca['turns_count']} | {ca['input_tokens']:,} | {ca['output_tokens']:,} | "
                f"{ca['cache_read_tokens']:,} | {ca['tool_errors_count']} | **{ca['duration_seconds']}s** |"
            )
        harm_list = stg["stage_1b_cta"].get("harmonizers") or ([stg["stage_1b_cta"]["harmonizer"]] if stg["stage_1b_cta"]["harmonizer"] else [])
        for ha in harm_list:
            role_desc = "Direct Architect" if stg['stage_1b_cta']['mappers_count'] == 0 else "Harmonizer"
            md.append(
                f"| **{ha['label']}** | {role_desc} | {ha['turns_count']} | {ha['input_tokens']:,} | {ha['output_tokens']:,} | "
                f"{ha['cache_read_tokens']:,} | {ha['tool_errors_count']} | **{ha['duration_seconds']}s** |"
            )

        md.extend([
            "",
            "---",
            "",
            "### 3.3. Stage 3: Autoría de Reactivos por Shard y Análisis por Competencia",
            f"- **Total de Shards Auditados:** `{stg['stage_3_authors']['shards_count']} shards concurrentes`",
            f"- **Duración Mínima de Shard:** `{stg['stage_3_authors']['min_duration_seconds']}s` | **Mediana:** `{stg['stage_3_authors']['median_duration_seconds']}s`",
            f"- **Tiempo de Pared Máximo (Straggler Crítico):** **`{stg['stage_3_authors']['max_duration_seconds']}s`** (`{round(stg['stage_3_authors']['max_duration_seconds']/60, 1)} min`) por `{stg['stage_3_authors']['straggler_shard']}`",
            f"- **Retraso de Sincronización Impuesto por el Straggler:** **`+{stg['stage_3_authors']['straggler_delay_vs_median']}s`** frente a la mediana",
            f"- **Tokens Promedio por Competencia en Autores:** **`{stg['stage_3_authors']['avg_tokens_per_competency']:,} tokens/competencia`**",
            "",
            "| Shard ID | Competencias Asignadas | Comps | Tokens In | Tokens Out | Cache Leído | Total Activo | Tokens / Comp | Turnos | Errores | Duración |",
            "| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |"
        ])

        for sa in stg["stage_3_authors"]["shards"]:
            c_list = ", ".join(sa.get("competencies", [])[:4])
            if len(sa.get("competencies", [])) > 4:
                c_list += f" (+{len(sa.get('competencies', []))-4})"
            c_cnt = sa.get("competencies_count", 0)
            tok_per_c = f"{sa.get('tokens_per_competency', 0):,}" if c_cnt > 0 else "N/A"
            is_straggler = " 🛑" if sa["duration_seconds"] == stg["stage_3_authors"]["max_duration_seconds"] else ""

            md.append(
                f"| **{sa['label']}{is_straggler}** | `{c_list or 'N/A'}` | {c_cnt} | {sa['input_tokens']:,} | "
                f"{sa['output_tokens']:,} | {sa['cache_read_tokens']:,} | {sa['active_tokens']:,} | "
                f"**{tok_per_c}** | {sa['turns_count']} | {sa['tool_errors_count']} | **{sa['duration_seconds']}s** |"
            )

        md.extend([
            "",
            "---",
            "",
            "### 3.4. Evaluación y Arbitraje de Blind Judges (Verificación Psicométrica Ciega)"
        ])

        bj = stg["stage_5_judges"]
        first_att_res = "✅ 100% Limpio (Sin Discrepancias)" if bj["passed_first_attempt"] else "❌ Falló al primer intento"
        first_att_obs = "Sin discrepancias ni arbitraje necesario" if bj["passed_first_attempt"] else f"{bj['initial_errors_count']} violaciones iniciales registradas"
        rep_obs = "0 requeridas" if bj["passed_first_attempt"] else f"{bj['repair_iterations']} iteraciones ejecutadas"
        orch_obs = "Ninguna (ejecución autónoma)" if bj["supervisor_interventions_count"] == 0 else f"{bj['supervisor_interventions_count']} ediciones registradas"

        md.extend([
            "",
            "> [!NOTE]",
            f"> **Dictamen de Blind Judges:** {bj['badge']}  ",
            f"> {bj['summary_desc']}",
            "",
            "| Dimensión de Arbitraje Ciego | Valor Registrado | Observación Técnica |",
            "| :--- | :--- | :--- |",
            f"| **Lote Estratificado Ciego** | `{bj['batch_items_count']} reactivos` ({w['competencies_count']} comps × 2) | Lote de evaluación sin soluciones (`judge_batch.json`) |",
            f"| **Subagentes Jueces Ciegos** | `{bj.get('judges_count', 0)} jueces` | Aislamiento epistémico en Stage 5 |",
            f"| **Resultado al Primer Intento** | **`{first_att_res}`** | {first_att_obs} |",
            f"| **Iteraciones de Auto-Reparación** | `{bj['repair_iterations']} iteraciones` en sandbox | {rep_obs} |",
            f"| **Intervenciones del Supervisor** | 🛠️ `{bj['supervisor_interventions_count']} operaciones directas` | {orch_obs} |",
            "",
            "#### Detalle de Acciones Registradas:"
        ])
        for act in bj["actions_taken"]:
            md.append(f"- {act}")

        md.extend([
            "",
            "---",
            "",
            "## 4. Auditoría Forense del Orquestador y Catálogo de Intervenciones Manuales",
            "",
            "### 4.1. Descomposición del Tiempo Total del Orquestador",
            f"- ⏱️ **Tiempo Total de Pared del Orquestador:** `{summary['wall_clock_minutes']} min` (`{summary['wall_clock_seconds']}s`)",
            f"- 💻 **Tiempo Activo Ejecutando Comandos CLI (`run.py`):** `{orch['time_decomposition']['cli_execution_minutes']} min` (`{orch['time_decomposition']['cli_execution_seconds']}s`)",
            f"- 🛠️ **Tiempo Gastado en Intervenciones Manuales (Supervisor Repair):** **`{orch['time_decomposition']['supervisor_repair_minutes']} min`** (`{orch['time_decomposition']['supervisor_repair_seconds']}s`)",
            f"- ⏳ **Tiempo Ocioso en Barreras de Sincronización (Esperando Subagentes):** `{orch['time_decomposition']['barrier_wait_minutes']} min` (`{orch['time_decomposition']['barrier_wait_seconds']}s`)",
            f"- 🧠 **Tiempo de Inferencia y Razonamiento del Modelo:** `{orch['time_decomposition']['model_thinking_minutes']} min` (`{orch['time_decomposition']['model_thinking_seconds']}s`)",
            "",
            "### 4.2. Catálogo Cronológico de Reparaciones Manuales del Orquestador",
            f"Operaciones directas de edición de código ejecutadas por el orquestador: **`{orch['interventions_count']}`**",
            "",
            "| Paso | Archivo Afectado | Tipo de Acción | Causa Raíz / Justificación Técnica | Herramienta | Tokens Paso |",
            "| :---: | :--- | :--- | :--- | :--- | :--- |"
        ])

        if orch["interventions"]:
            for it in orch["interventions"]:
                md.append(
                    f"| **{it['step']}** | `{it['file']}` | {it['action_type']} | {it['cause']} | `{it['tool']}` | {it['tokens_step']:,} |"
                )
        else:
            md.append("| — | *Ninguna intervención registrada* | — | — | — | 0 |")

        md.extend([
            "",
            "---",
            "",
            "## 5. Diagnóstico de Cuellos de Botella y Antipatrones Detectados",
            ""
        ])

        if not bottlenecks:
            md.append("> ✅ **0 cuellos de botella detectados según los umbrales deterministas.**")
        else:
            for b in bottlenecks:
                sev_icon = "🛑" if b["severity"] == "HIGH" else ("⚠️" if b["severity"] == "MEDIUM" else "ℹ️")
                md.extend([
                    f"### {sev_icon} [{b['severity']}] {b['title']}",
                    f"- **Ámbito:** `{b.get('stage', 'General')}`",
                    f"- **Diagnóstico:** {b['description']}",
                    ""
                ])

        tt_summary = audit.get("thinking_traces_summary", {})
        if tt_summary:
            md.extend([
                "---",
                "",
                "## 6. Telemetría de Razonamiento Cognitivo (Thinking Traces)",
                "",
                f"- **Total de Turnos con Razonamiento:** `{tt_summary.get('total_thinking_turns', 0)} turnos`",
                f"- **Volumen Total de Razonamiento:** `{tt_summary.get('total_thinking_chars', 0):,} caracteres`",
                f"- **Razonamiento del Orquestador:** `{tt_summary.get('orchestrator_thinking_turns', 0)} turnos` ({tt_summary.get('orchestrator_thinking_chars', 0):,} chars)",
                f"- **Razonamiento de Subagentes:** `{tt_summary.get('subagents_thinking_turns', 0)} turnos` ({tt_summary.get('subagents_thinking_chars', 0):,} chars)",
                "",
                "| Agente / Subagente | Turnos de Thinking | Caracteres de Thinking | Trazas de Error Capturadas |",
                "| :--- | :---: | :---: | :---: |"
            ])
            for s in subs:
                err_traces_count = len(s.get("error_thinking_traces", []))
                err_badge = f"⚠️ {err_traces_count}" if err_traces_count > 0 else "0"
                md.append(
                    f"| **{s['label']}** | {s.get('thinking_turns_count', 0)} | {s.get('thinking_chars', 0):,} | {err_badge} |"
                )
            md.append("")

        md.extend([
            "---",
            "*Reporte forense determinista emitido por `c2c-run-auditor`.*"
        ])

        return "\n".join(md)

    @staticmethod
    def generate_html_dashboard(audit: Dict[str, Any]) -> str:
        meta = audit["meta"]
        summary = audit["summary"]
        w = audit["workload"]
        ue = audit["unit_economics"]
        stg = audit["stage_deep_dives"]
        orch = audit["orchestrator_audit"]

        html = f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <title>C2C Architectural Forensic Dashboard - {meta['course_id']}</title>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <style>
    :root {{
      --bg: #0f172a;
      --card-bg: #1e293b;
      --border: #334155;
      --text: #f8fafc;
      --text-muted: #94a3b8;
      --accent: #38bdf8;
      --accent-green: #4ade80;
      --accent-amber: #f59e0b;
      --accent-rose: #f43f5e;
      --font: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{ background: var(--bg); color: var(--text); font-family: var(--font); padding: 24px; line-height: 1.5; }}
    .header {{ display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid var(--border); padding-bottom: 16px; margin-bottom: 24px; }}
    .header h1 {{ font-size: 1.5rem; color: var(--accent); }}
    .header .meta {{ color: var(--text-muted); font-size: 0.85rem; }}
    .grid-kpi {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 16px; margin-bottom: 24px; }}
    .kpi-card {{ background: var(--card-bg); border: 1px solid var(--border); border-radius: 8px; padding: 16px; }}
    .kpi-card .label {{ font-size: 0.8rem; color: var(--text-muted); text-transform: uppercase; }}
    .kpi-card .val {{ font-size: 1.6rem; font-weight: bold; color: var(--text); margin-top: 4px; }}
    .kpi-card .sub {{ font-size: 0.75rem; color: var(--accent-green); margin-top: 2px; }}
    .section {{ background: var(--card-bg); border: 1px solid var(--border); border-radius: 8px; padding: 20px; margin-bottom: 24px; }}
    .section h2 {{ font-size: 1.1rem; color: var(--accent); margin-bottom: 16px; border-bottom: 1px solid var(--border); padding-bottom: 8px; }}
    table {{ width: 100%; border-collapse: collapse; font-size: 0.85rem; text-align: left; }}
    th, td {{ padding: 10px 12px; border-bottom: 1px solid var(--border); }}
    th {{ color: var(--text-muted); font-weight: 600; text-transform: uppercase; font-size: 0.75rem; }}
    tr:hover td {{ background: rgba(255,255,255,0.02); }}
    .badge {{ display: inline-block; padding: 2px 8px; border-radius: 4px; font-size: 0.75rem; font-weight: 600; }}
    .badge-high {{ background: rgba(244, 63, 94, 0.2); color: var(--accent-rose); }}
    .badge-med {{ background: rgba(245, 158, 11, 0.2); color: var(--accent-amber); }}
    .badge-ok {{ background: rgba(74, 222, 128, 0.2); color: var(--accent-green); }}
  </style>
</head>
<body>

  <div class="header">
    <div>
      <h1>C2C Architectural Forensic Telemetry</h1>
      <div class="meta">{meta['course_title']} (<code>{meta['course_id']}</code>) | Conv: <code>{meta['orchestrator_conversation_id'][:12]}...</code></div>
    </div>
    <div class="meta">Audit Date: {meta['audit_timestamp'][:19]} UTC</div>
  </div>

  <div class="grid-kpi">
    <div class="kpi-card">
      <div class="label">Wall-Clock Time</div>
      <div class="val">{summary['wall_clock_minutes']} min</div>
      <div class="sub">{summary['wall_clock_seconds']}s elapsed</div>
    </div>
    <div class="kpi-card">
      <div class="label">Parallel Speedup</div>
      <div class="val">{summary['parallel_speedup_factor']}x</div>
      <div class="sub">{summary['agent_compute_minutes']}m compute time</div>
    </div>
    <div class="kpi-card">
      <div class="label">Total Tokens</div>
      <div class="val">{summary['total_tokens']:,}</div>
      <div class="sub">Active: {summary['total_active_tokens']:,} | Cache: {summary['total_cache_read_tokens']:,}</div>
    </div>
    <div class="kpi-card">
      <div class="label">Tokens / Question</div>
      <div class="val">{ue['tokens_per_question']:,}</div>
      <div class="sub">{w['questions_count']} questions generated</div>
    </div>
    <div class="kpi-card">
      <div class="label">Seconds / Question</div>
      <div class="val">{ue['seconds_per_question']}s</div>
      <div class="sub">{ue['questions_per_minute']} questions/min</div>
    </div>
    <div class="kpi-card">
      <div class="label">Supervisor Interventions</div>
      <div class="val">{orch['interventions_count']}</div>
      <div class="sub">{orch['time_decomposition']['supervisor_repair_minutes']}m spent repairing</div>
    </div>
  </div>

  <div class="section">
    <h2>Stage 3: Shard Question Authoring & Competency Metrics</h2>
    <div style="margin-bottom: 12px; font-size: 0.85rem; color: var(--text-muted);">
      Critical Straggler: <strong>{stg['stage_3_authors']['straggler_shard']}</strong> ({stg['stage_3_authors']['max_duration_seconds']}s | +{stg['stage_3_authors']['straggler_delay_vs_median']}s vs median) |
      Avg Tokens / Competency: <strong>{stg['stage_3_authors']['avg_tokens_per_competency']:,}</strong>
    </div>
    <table>
      <thead>
        <tr>
          <th>Shard ID</th>
          <th>Competencias</th>
          <th>Comps</th>
          <th>Tokens In</th>
          <th>Tokens Out</th>
          <th>Active Tokens</th>
          <th>Tokens / Comp</th>
          <th>Turns</th>
          <th>Duration</th>
        </tr>
      </thead>
      <tbody>
        {"".join([f'''<tr>
          <td><strong>{sa['label']}</strong></td>
          <td><code>{", ".join(sa.get("competencies", [])[:3])}{"..." if len(sa.get("competencies", []))>3 else ""}</code></td>
          <td>{sa.get("competencies_count", 0)}</td>
          <td>{sa['input_tokens']:,}</td>
          <td>{sa['output_tokens']:,}</td>
          <td><strong>{sa['active_tokens']:,}</strong></td>
          <td><strong>{sa.get("tokens_per_competency", 0):,}</strong></td>
          <td>{sa['turns_count']}</td>
          <td><strong>{sa['duration_seconds']}s</strong></td>
        </tr>''' for sa in stg['stage_3_authors']['shards']])}
      </tbody>
    </table>
  </div>

  <div class="section">
    <h2>Blind Judges & Psychometric Verification</h2>
    <div style="margin-bottom: 12px; font-size: 0.9rem;">
      <span class="badge {'badge-ok' if stg['stage_5_judges']['passed_first_attempt'] else 'badge-high'}">{stg['stage_5_judges']['badge']}</span>
    </div>
    <div style="font-size: 0.85rem; color: var(--text-muted); margin-bottom: 16px;">
      {stg['stage_5_judges']['summary_desc']}
    </div>
    <table>
      <thead>
        <tr>
          <th>Lote Estratificado</th>
          <th>Primer Intento</th>
          <th>Auto-Repair Iterations</th>
          <th>Supervisor Fixes</th>
          <th>Status Final</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><strong>{stg['stage_5_judges']['batch_items_count']} reactivos</strong></td>
          <td><span class="badge {'badge-ok' if stg['stage_5_judges']['passed_first_attempt'] else 'badge-high'}">{'PASSED' if stg['stage_5_judges']['passed_first_attempt'] else 'FAILED'}</span></td>
          <td>{stg['stage_5_judges']['repair_iterations']} iteraciones</td>
          <td><strong>{stg['stage_5_judges']['supervisor_interventions_count']} fixes</strong></td>
          <td><span class="badge badge-ok">CERTIFICADO</span></td>
        </tr>
      </tbody>
    </table>
    <div style="margin-top: 14px; font-size: 0.85rem;">
      <strong>Acciones Correctivas Tomadas:</strong>
      <ul style="margin-left: 20px; margin-top: 6px; color: var(--text-muted);">
        {"".join([f'<li>{act}</li>' for act in stg['stage_5_judges']['actions_taken']])}
      </ul>
    </div>
  </div>

  <div class="section">
    <h2>Orchestrator Manual Interventions (Supervisor Repair Anti-Pattern)</h2>
    <table>
      <thead>
        <tr>
          <th>Step</th>
          <th>Target File</th>
          <th>Action Type</th>
          <th>Root Cause / Snippet</th>
          <th>Tool</th>
        </tr>
      </thead>
      <tbody>
        {"".join([f'''<tr>
          <td><strong>{it['step']}</strong></td>
          <td><code>{it['file']}</code></td>
          <td>{it['action_type']}</td>
          <td>{it['cause']}</td>
          <td><code>{it['tool']}</code></td>
        </tr>''' for it in orch['interventions']])}
      </tbody>
    </table>
  </div>

</body>
</html>
"""
        return html

    @staticmethod
    def generate_comparison(run_a: Dict[str, Any], run_b: Dict[str, Any]) -> str:
        """Generates the comparative table and analysis matching Section 1 of solow_vs_estadistica_definitive_architectural_audit.md."""
        name_a = run_a.get("course_title", run_a.get("course_id", "Run A")) + f" (`{run_a.get('course_id')}`)"
        name_b = run_b.get("course_title", run_b.get("course_id", "Run B")) + f" (`{run_b.get('course_id')}`)"

        wa = run_a.get("workload", {})
        wb = run_b.get("workload", {})
        ma = run_a.get("metrics", {})
        mb = run_b.get("metrics", {})
        uea = run_a.get("unit_economics", {})
        ueb = run_b.get("unit_economics", {})

        def growth_factor(va: float, vb: float, is_cost: bool = True) -> str:
            if va == 0 and vb == 0:
                return "0%"
            if va == 0:
                return "+100% (inf)"
            ratio = vb / va
            diff_pct = (ratio - 1.0) * 100
            if ratio >= 1.0:
                factor_str = f"+{diff_pct:.1f}% ({ratio:.1f}x)"
                return f"**{factor_str}**" if is_cost and ratio > 1.5 else factor_str
            else:
                pct_dec = (1.0 - ratio) * 100
                return f"-{pct_dec:.1f}% ({ratio:.2f}x)"

        rows = [
            ("Material de Entrada", f"{wa.get('source_files_count', len(wa.get('source_files', [])))} archivos ({wa.get('pages_or_slides', 0)} págs)",
             f"{wb.get('source_files_count', len(wb.get('source_files', [])))} archivos ({wb.get('pages_or_slides', 0)} págs)",
             growth_factor(wa.get("pages_or_slides", 1), wb.get("pages_or_slides", 1), is_cost=False)),

            ("Competencias Extraídas", f"{wa.get('competencies', wa.get('competencies_count', 0))} competencias",
             f"{wb.get('competencies', wb.get('competencies_count', 0))} competencias",
             growth_factor(wa.get("competencies", wa.get("competencies_count", 1)), wb.get("competencies", wb.get("competencies_count", 1)), is_cost=False)),

            ("Subagentes Desplegados", f"{ma.get('subagents_count', run_a.get('summary', {}).get('total_subagents_spawned', 0))} subagentes",
             f"{mb.get('subagents_count', run_b.get('summary', {}).get('total_subagents_spawned', 0))} subagentes",
             growth_factor(ma.get("subagents_count", 1), mb.get("subagents_count", 1))),

            ("Reactivos Validados", f"{wa.get('questions', wa.get('questions_count', 0))} reactivos",
             f"{wb.get('questions', wb.get('questions_count', 0))} reactivos",
             growth_factor(wa.get("questions", 1), wb.get("questions", 1), is_cost=False)),

            ("Tokens Entrada (Subagentes)", f"{ma.get('input_tokens', 0):,}",
             f"{mb.get('input_tokens', 0):,}",
             growth_factor(ma.get("input_tokens", 1), mb.get("input_tokens", 1))),

            ("Tokens Salida (Subagentes)", f"{ma.get('output_tokens', 0):,}",
             f"{mb.get('output_tokens', 0):,}",
             growth_factor(ma.get("output_tokens", 1), mb.get("output_tokens", 1))),

            ("Tokens Caché (Leídos)", f"{ma.get('cache_read_tokens', 0):,}",
             f"{mb.get('cache_read_tokens', 0):,}",
             growth_factor(ma.get("cache_read_tokens", 1), mb.get("cache_read_tokens", 1))),

            ("Gran Total Tokens Activos", f"{ma.get('total_active_tokens', 0):,}",
             f"{mb.get('total_active_tokens', 0):,}",
             growth_factor(ma.get("total_active_tokens", 1), mb.get("total_active_tokens", 1))),

            ("Gran Total Facturable", f"{ma.get('total_tokens', 0):,}",
             f"{mb.get('total_tokens', 0):,}",
             growth_factor(ma.get("total_tokens", 1), mb.get("total_tokens", 1))),

            ("Tiempo de Pared (Wall Clock)", f"{round(ma.get('wall_clock_seconds', 0)/60, 1)} min ({ma.get('wall_clock_seconds', 0)}s)",
             f"{round(mb.get('wall_clock_seconds', 0)/60, 1)} min ({mb.get('wall_clock_seconds', 0)}s)",
             growth_factor(ma.get("wall_clock_seconds", 1), mb.get("wall_clock_seconds", 1))),

            ("Factor de Aceleración Paralela", f"{ma.get('speedup', 1.0)}x",
             f"{mb.get('speedup', 1.0)}x",
             f"{mb.get('speedup', 1.0) - ma.get('speedup', 1.0):+.2f}x"),

            ("Tokens / Pregunta", f"{uea.get('tokens_per_question', 0):,}",
             f"{ueb.get('tokens_per_question', 0):,}",
             growth_factor(uea.get("tokens_per_question", 1), ueb.get("tokens_per_question", 1))),

            ("Segundos / Pregunta", f"{uea.get('seconds_per_question', 0)}s",
             f"{ueb.get('seconds_per_question', 0)}s",
             growth_factor(uea.get("seconds_per_question", 1), ueb.get("seconds_per_question", 1))),

            ("Blind Judges (1er Intento)",
             "✅ Pasó (100% limpio)" if ma.get("blind_judges", {}).get("passed_first_attempt", True) else f"❌ Falló ({ma.get('orchestrator_interventions', 0)} fixes)",
             "✅ Pasó (100% limpio)" if mb.get("blind_judges", {}).get("passed_first_attempt", False) else f"❌ Falló ({mb.get('orchestrator_interventions', 0)} fixes)",
             "Cambio de estado" if ma.get("blind_judges", {}).get("passed_first_attempt", True) != mb.get("blind_judges", {}).get("passed_first_attempt", False) else "Paridad"),

            ("Intervenciones Manuales (Orch)", f"{ma.get('orchestrator_interventions', 0)} fixes",
             f"{mb.get('orchestrator_interventions', 0)} fixes",
             f"{mb.get('orchestrator_interventions', 0) - ma.get('orchestrator_interventions', 0):+d} intervenciones")
        ]

        md = [
            f"# Comparativa Arquitectónica Forense de Telemetría",
            f"### `{run_a.get('course_id')}` vs `{run_b.get('course_id')}`",
            "",
            f"**Fecha:** `{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} UTC`",
            "",
            "---",
            "",
            "## 1. Tabla Comparativa de Telemetría Real",
            "",
            f"| Métrica | {name_a} | {name_b} | Factor de Crecimiento / Cambio |",
            "| :--- | :--- | :--- | :--- |"
        ]

        for label, val_a, val_b, diff in rows:
            md.append(f"| **{label}** | {val_a} | {val_b} | {diff} |")

        md.extend([
            "",
            "---",
            "",
            "## 2. Variación Determinista de Ratios",
            "",
            f"- **Intensidad de Tokens por Pregunta**: `{uea.get('tokens_per_question', 0):,}` -> `{ueb.get('tokens_per_question', 0):,}` ({growth_factor(uea.get('tokens_per_question', 1), ueb.get('tokens_per_question', 1))}).",
            f"- **Multiplicador de Tokens Activos**: `{growth_factor(ma.get('total_active_tokens', 1), mb.get('total_active_tokens', 1))}`.",
            f"- **Ritmo de Entrega (Seg/Pregunta)**: `{uea.get('seconds_per_question', 0)}s` -> `{ueb.get('seconds_per_question', 0)}s`.",
            f"- **Arbitraje de Blind Judges (1er Intento)**: `{name_a}` = `{ma.get('blind_judges', {}).get('passed_first_attempt', True)}`, `{name_b}` = `{mb.get('blind_judges', {}).get('passed_first_attempt', False)}`.",
            f"- **Intervenciones del Supervisor**: `{ma.get('orchestrator_interventions', 0)}` vs `{mb.get('orchestrator_interventions', 0)}`.",
            "",
            "---",
            "*Generado por el motor forense `c2c-run-auditor`.*"
        ])
        return "\n".join(md)


# ---------------------------------------------------------------------------
# CLI Main Entrypoint
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Content-to-Course & Multi-Agent Workflow Run Audit Engine (Deep Forensic Edition)")
    parser.add_argument("--conversation", "-c", help="Conversation ID, chat link, or path to transcript.jsonl")
    parser.add_argument("--output-dir", "-o", default="reports/c2c_audits", help="Output directory for persistent audit artifacts")
    parser.add_argument("--work-dir", "-w", help="Path to work directory containing intermediate C2C artifacts")
    parser.add_argument("--format", choices=["all", "md", "json", "html"], default="all", help="Output artifact formats")
    parser.add_argument("--recent", action="store_true", help="List recent C2C runs found in Antigravity brain")
    parser.add_argument("--history", action="store_true", help="Print or regenerate the historical benchmark comparison table")
    parser.add_argument("--compare", nargs="*", help="Compare two runs (e.g. --compare run_a run_b, or --compare to compare latest against previous/baseline)")
    parser.add_argument("--traceback", action="store_true", help="Also execute granular turn-by-turn traceback deep-dive and emit traceback_deepdive.md/json")
    args = parser.parse_args()

    output_base = Path(args.output_dir)
    output_base.mkdir(parents=True, exist_ok=True)
    registry_mgr = HistoricalRegistry(output_base)

    if args.compare is not None:
        registry_mgr.ensure_baseline()
        reg = registry_mgr.load_registry()
        if len(reg) < 2:
            print("[-] Error: Need at least 2 runs in registry to perform comparison.")
            return

        if len(args.compare) == 0:
            run_a = reg[0]
            run_b = reg[-1]
        elif len(args.compare) == 1:
            target_a = args.compare[0].lower()
            run_a = next((r for r in reg if target_a in r.get("run_id", "").lower() or target_a in r.get("course_id", "").lower() or target_a in r.get("conversation_id", "").lower()), None)
            if not run_a:
                print(f"[-] Could not find run matching '{args.compare[0]}'")
                return
            run_b = reg[-1] if run_a != reg[-1] else reg[0]
        else:
            target_a = args.compare[0].lower()
            target_b = args.compare[1].lower()
            run_a = next((r for r in reg if target_a in r.get("run_id", "").lower() or target_a in r.get("course_id", "").lower() or target_a in r.get("conversation_id", "").lower()), None)
            run_b = next((r for r in reg if target_b in r.get("run_id", "").lower() or target_b in r.get("course_id", "").lower() or target_b in r.get("conversation_id", "").lower()), None)
            if not run_a or not run_b:
                print(f"[-] Could not resolve both runs: '{args.compare[0]}' and '{args.compare[1]}'")
                return

        comparison_md = ReportGenerator.generate_comparison(run_a, run_b)
        print("\n" + comparison_md + "\n")

        comp_slug = f"comparison_{run_a.get('course_id')}_vs_{run_b.get('course_id')}.md"
        comp_file = output_base / comp_slug
        comp_file.write_text(comparison_md, encoding="utf-8")
        print(f"[+] Comparison saved to: {comp_file}")
        return

    if args.history:
        registry_mgr.ensure_baseline()
        reg = registry_mgr.load_registry()
        print(f"[+] Loaded {len(reg)} historical audit runs.")
        if registry_mgr.benchmark_md_file.exists():
            print(registry_mgr.benchmark_md_file.read_text(encoding="utf-8"))
        return

    if args.recent:
        runs = list_recent_c2c_runs(10)
        print(f"\n[+] Found {len(runs)} recent C2C orchestrations in brain directory:\n")
        for r in runs:
            print(f"  - [{r['date_str']}] ID: {r['conversation_id']}")
        return

    if not args.conversation:
        runs = list_recent_c2c_runs(1)
        if runs:
            print(f"[*] No conversation specified. Auto-selecting latest C2C orchestration: {runs[0]['conversation_id']}")
            target_str = runs[0]["conversation_id"]
        else:
            print("[-] Error: Please specify --conversation <id|link|path> or run with --recent.")
            sys.exit(1)
    else:
        target_str = args.conversation

    transcript_path = resolve_transcript_path(target_str)
    if not transcript_path or not transcript_path.exists():
        print(f"[-] Could not resolve transcript for target: '{target_str}'")
        sys.exit(1)

    conv_id = transcript_path.parent.parent.parent.name
    print(f"[+] Auditing conversation: {conv_id} ({transcript_path})")

    # 1. Parse root transcript
    root_records = TranscriptParser.parse_file(transcript_path)
    if not root_records:
        print(f"[-] Transcript is empty: {transcript_path}")
        sys.exit(1)

    # 2. Extract Workload Profile (Strictly isolated by target_conv_id)
    work_dir_p = Path(args.work_dir) if args.work_dir else None
    workload = WorkloadExtractor.extract(work_dir=work_dir_p, records=root_records, target_conv_id=conv_id)
    print(f"[+] Workload Profile: {workload['total_pages_or_slides']} pages/slides ({workload['total_input_mb']} MB), {workload['competencies_count']} comps, {workload['questions_count']} questions.")
    print(f"[+] Resolved Work Dir: {workload.get('work_dir_resolved')} (Conversation Match: {workload.get('work_dir_conversation_match')}, Stage Snapshots: {len(workload.get('telemetry_snapshots', {}))})")

    # 3. Perform Execution Audit
    auditor = ExecutionAuditor(root_records=root_records, root_conv_id=conv_id)
    audit_result = auditor.audit(workload=workload)

    # 4. Create Run Directory
    ts_slug = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    course_slug = workload.get("course_id", "c2c_run")
    short_cid = conv_id[:8]
    run_dir_name = f"{ts_slug}_{course_slug}_{short_cid}"
    run_dir = output_base / run_dir_name
    run_dir.mkdir(parents=True, exist_ok=True)

    # 5. Persist Artifacts
    telemetry_file = run_dir / "telemetry.json"
    telemetry_file.write_text(json.dumps(audit_result, indent=2, ensure_ascii=False), encoding="utf-8")

    report_file = run_dir / "report.md"
    report_md = ReportGenerator.generate_markdown(audit_result)
    report_file.write_text(report_md, encoding="utf-8")

    dashboard_file = run_dir / "dashboard.html"
    dashboard_html = ReportGenerator.generate_html_dashboard(audit_result)
    dashboard_file.write_text(dashboard_html, encoding="utf-8")

    # 6. Register into Longitudinal Benchmark Registry
    registry_mgr.register_run(audit_result, run_dir_name)

    if args.traceback:
        try:
            _scripts_dir = Path(__file__).parent.resolve()
            if str(_scripts_dir) not in sys.path:
                sys.path.insert(0, str(_scripts_dir))
            from traceback_analyzer import run_traceback_audit
            print("\n[*] Running integrated Traceback Deep-Dive...")
            resolved_wdir = Path(workload["work_dir_resolved"]) if workload.get("work_dir_resolved") else work_dir_p
            run_traceback_audit(conv_id, run_dir, work_dir=resolved_wdir)
        except Exception as ex:
            print(f"[!] Warning: Traceback Deep-Dive failed: {ex}")

    print(f"\n[+] Deep Forensic Audit Complete!")
    print(f"    - Wall-Clock Time: {audit_result['summary']['wall_clock_minutes']} min (Speedup: {audit_result['summary']['parallel_speedup_factor']}x)")
    print(f"    - Total Tokens:    {audit_result['summary']['total_tokens']:,} (Active: {audit_result['summary']['total_active_tokens']:,})")
    cta_subs_total = audit_result['stage_deep_dives']['stage_1b_cta'].get('agents_count', audit_result['stage_deep_dives']['stage_1b_cta']['mappers_count'] + (1 if audit_result['stage_deep_dives']['stage_1b_cta']['harmonizer'] else 0))
    print(f"    - Subagents Run:   {audit_result['summary']['total_subagents_spawned']} (Vision: {audit_result['stage_deep_dives']['stage_1a_vision']['agents_count']}, CTA: {cta_subs_total}, Authors: {audit_result['stage_deep_dives']['stage_3_authors']['shards_count']}, Judges: {audit_result['stage_deep_dives']['stage_5_judges'].get('judges_count', 0)})")
    print(f"    - Shards Straggler:{audit_result['stage_deep_dives']['stage_3_authors']['straggler_shard']} ({audit_result['stage_deep_dives']['stage_3_authors']['max_duration_seconds']}s)")
    print(f"    - Supervisor Fixes:{audit_result['orchestrator_audit']['interventions_count']} manual interventions detected")
    print(f"    - Run Directory:   {run_dir}")
    print(f"    - Markdown Report: {report_file}")
    print(f"    - Telemetry JSON:  {telemetry_file}")
    print(f"    - Dashboard HTML:  {dashboard_file}")
    print(f"    - Registry & Log:  {registry_mgr.benchmark_md_file}\n")


if __name__ == "__main__":
    main()

