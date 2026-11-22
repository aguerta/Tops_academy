"""Comprehensive regression tests for M20 v4.4 pipeline & QA hardening."""

import asyncio
import importlib.util
import json
import os
import re
import sys
import time
import types
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple

import pytest

_ROOT = Path(__file__).resolve().parents[2]
_C2C_DIR = _ROOT / ".agents" / "skills" / "content-to-course"
_QA_SCRIPTS_DIR = _ROOT / ".agents" / "skills" / "course-qa-evaluator" / "scripts"
_AUDIT_SCRIPTS_DIR = _ROOT / ".agents" / "skills" / "c2c-run-auditor" / "scripts"
_WORKFLOW_PATH = _C2C_DIR / "workflows" / "c2c_wave_workflow.py"

if str(_C2C_DIR) not in sys.path:
    sys.path.insert(0, str(_C2C_DIR))

import check_cta  # noqa: E402
import check_templates  # noqa: E402
import plan_shards  # noqa: E402
from engine import shard_compiler_steps as scs  # noqa: E402
from engine.shard_locator import ShardDataLineLocator  # noqa: E402
from engine.template_healing import auto_heal_template_data, heal_katex_display_str  # noqa: E402


def _load_module_isolated(name: str, file_path: Path, extra_sys_path: Optional[Path] = None) -> Any:
    if extra_sys_path and str(extra_sys_path) not in sys.path:
        sys.path.insert(0, str(extra_sys_path))
    spec = importlib.util.spec_from_file_location(name, str(file_path))
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def _load_workflow(
    args_dict: Dict[str, Any],
    agent_fn: Optional[Callable[..., Any]] = None,
    run_cli_fn: Optional[Callable[..., Any]] = None,
) -> Tuple[Any, List[str]]:
    phases: List[str] = []
    source = _WORKFLOW_PATH.read_text(encoding="utf-8")
    marker = 'if "parallel" in globals():'
    if marker in source:
        source = source.split(marker, 1)[0]

    async def _default_agent(*args: Any, **kwargs: Any) -> str:
        return "DONE: ok"

    async def _noop_cli(*args: Any, **kwargs: Any) -> str:
        return "ok"

    async def _default_parallel(items: List[Any], fn: Callable[[Any], Any]) -> List[Any]:
        return await asyncio.gather(*(fn(item) for item in items))

    mod = types.ModuleType("c2c_wave_workflow_v44_test")
    mod.__file__ = str(_WORKFLOW_PATH)
    mod.__dict__.update({
        "__name__": "c2c_wave_workflow_v44_test",
        "__file__": str(_WORKFLOW_PATH),
        "args": args_dict,
        "phase": lambda msg: phases.append(str(msg)),
        "log": lambda msg: None,
        "agent": agent_fn or _default_agent,
        "parallel": _default_parallel,
        "run_cli": run_cli_fn or _noop_cli,
    })
    exec(compile(source, str(_WORKFLOW_PATH), "exec"), mod.__dict__)
    return mod, phases


def _make_valid_comp(
    cid: str,
    ctype: str,
    name: str,
    desc: str = "",
    modalities: Optional[List[str]] = None,
    prereqs: Optional[List[str]] = None,
    bloom: str = "Evaluate",
) -> Dict[str, Any]:
    clean = cid.replace("-", "")
    is_skill = ctype == "skill"
    n_dist = 6 if is_skill else 3
    dists = []
    for i in range(1, n_dist + 1):
        dists.append({
            "id": f"D-{clean}-{i:02d}",
            "name": f"Error {i} en {cid}",
            "wrong_belief": None if (is_skill and i <= 2) else f"Creencia incorrecta {i} para {cid}",
            "correct_belief": f"Comprension correcta {i} para {cid}",
            "omitted_step": f"Paso omitido {i} en {cid}" if (is_skill and i <= 2) else None,
            "trigger": "Al plantear la ecuacion",
            "manifestation": f"$x + {i}$",
            "error_type": "skipped_step" if (is_skill and i <= 2) else "conceptual_swap",
            "severity": "medium",
            "origin": "source",
            "evidence": {"doc": "notes.pdf", "page": 1},
            "remediation_hint": "Verifica paso a paso las hipotesis del teorema y contrasta el dominio antes de derivar.",
        })
    assumptions = (
        [{"id": f"A-{clean}-01", "statement_latex": "$x > 0$ estrictamente positivo", "violation_consequence": "Dominio matematico invalido fuera del intervalo positivo."}]
        if ctype in ("concept", "skill")
        else []
    )
    return {
        "id": cid,
        "type": ctype,
        "name": name,
        "description_latex": desc or f"Enunciado tecnico preciso para {cid} cubriendo {name}.",
        "bloom": bloom,
        "prerequisites": prereqs or [],
        "evidence": [{"doc": "notes.pdf", "page": 1}],
        "distractors": dists,
        "assumptions": assumptions,
        "recommended_modalities": modalities or (["open_symbolic", "proof_dag", "adversarial_break"] if is_skill else ["multiple_select", "adversarial_break"]),
    }


def _make_manifest_data(comps: List[Dict[str, Any]]) -> Dict[str, Any]:
    return {
        "course_id": "test_v44",
        "files": [{"doc": "notes.pdf", "total_pages": 20, "valid_page_range": [1, 20]}],
        "competencies": [c["id"] for c in comps],
    }


# ---------------------------------------------------------------------------
# 1. Workflow resilience: concurrency cap, retry, repair close-guard, modes
# ---------------------------------------------------------------------------


def test_run_wave_from_manifest_bounds_concurrency(tmp_path: Path) -> None:
    manifest = tmp_path / "authors.json"
    manifest.write_text(
        json.dumps({"Subagents": [{"Role": f"Author {i}", "Prompt": f"Work {i}. DONE: ok"} for i in range(10)]}),
        encoding="utf-8",
    )
    active = 0
    peak = 0

    async def _tracked_agent(**kwargs: Any) -> str:
        nonlocal active, peak
        active += 1
        peak = max(peak, active)
        await asyncio.sleep(0.015)
        active -= 1
        return "DONE: ok"

    wf, _ = _load_workflow({"work_dir": str(tmp_path), "max_concurrency": 3, "startup_stagger_s": 0.0}, agent_fn=_tracked_agent)
    res = asyncio.run(wf.run_wave_from_manifest(str(manifest), "Test Bounded"))
    assert len(res) == 10
    assert peak <= 3
    assert wf.DEFAULT_MAX_CONCURRENCY == 12


def test_run_wave_from_manifest_retries_collapse(tmp_path: Path) -> None:
    manifest = tmp_path / "judges.json"
    manifest.write_text(
        json.dumps({"Subagents": [{"Role": "Judge 01", "Prompt": "Audit. DONE: report.md"}]}),
        encoding="utf-8",
    )
    attempts = 0

    async def _flaky_agent(**kwargs: Any) -> str:
        nonlocal attempts
        attempts += 1
        if attempts == 1:
            return "429 RESOURCE_EXHAUSTED: capacity exhausted"
        return "DONE: report.md"

    wf, _ = _load_workflow(
        {"work_dir": str(tmp_path), "worker_max_retries": 2, "retry_backoff_s": 0.01, "startup_stagger_s": 0.0},
        agent_fn=_flaky_agent,
    )
    res = asyncio.run(wf.run_wave_from_manifest(str(manifest), "Judge Retry"))
    assert attempts == 2
    assert res == ["DONE: report.md"]


def test_run_wave_from_manifest_propagates_cancelled_error(tmp_path: Path) -> None:
    manifest = tmp_path / "authors.json"
    manifest.write_text(
        json.dumps({"Subagents": [{"Role": "Author 01", "Prompt": "Work. DONE: ok"}]}),
        encoding="utf-8",
    )
    attempts = 0

    async def _cancelled_agent(**kwargs: Any) -> str:
        nonlocal attempts
        attempts += 1
        raise asyncio.CancelledError()

    wf, _ = _load_workflow(
        {"work_dir": str(tmp_path), "worker_max_retries": 2, "retry_backoff_s": 0.01, "startup_stagger_s": 0.0},
        agent_fn=_cancelled_agent,
    )
    with pytest.raises(asyncio.CancelledError):
        asyncio.run(wf.run_wave_from_manifest(str(manifest), "Cancel Check"))
    assert attempts == 1


def test_repair_close_guard_retries_missing_check_runs(tmp_path: Path) -> None:
    work_dir = tmp_path / "work"
    dispatch_dir = work_dir / "dispatch"
    shards_dir = work_dir / "shards"
    dispatch_dir.mkdir(parents=True)
    shards_dir.mkdir(parents=True)

    repair_manifest = dispatch_dir / "repair.json"
    repair_manifest.write_text(
        json.dumps({
            "Subagents": [{
                "Role": "Repair 01",
                "shard_id": "shard_01",
                "assigned_competencies": ["Hab-07"],
                "Prompt": "Fix Hab-07 and finish with DONE: ok",
            }]
        }),
        encoding="utf-8",
    )

    repair_calls = 0

    async def _repair_agent(**kwargs: Any) -> str:
        nonlocal repair_calls
        repair_calls += 1
        if repair_calls == 2:
            # On retry, simulate check_runs >= 1 by writing compiled shard json
            (shards_dir / "shard_01.json").write_text("{}", encoding="utf-8")
        return "DONE: fixed"

    cli_calls: List[str] = []

    async def _fake_cli(cmd: str, label: str = "", env_extra: Any = None) -> str:
        cli_calls.append(cmd)
        if "dispatch-repair" in cmd:
            repair_manifest.write_text(
                json.dumps({
                    "Subagents": [{
                        "Role": "Repair 01 Retry",
                        "shard_id": "shard_01",
                        "assigned_competencies": ["Hab-07"],
                        "Prompt": "Retry Hab-07 DONE: ok",
                    }]
                }),
                encoding="utf-8",
            )
            fresh_ts = time.time() + 1.0
            os.utime(repair_manifest, (fresh_ts, fresh_ts))
        return "ok"

    wf, _ = _load_workflow(
        {"work_dir": str(work_dir), "mode": "repair", "startup_stagger_s": 0.0},
        agent_fn=_repair_agent,
        run_cli_fn=_fake_cli,
    )
    wf.run_cli = _fake_cli
    summary = asyncio.run(wf.run_c2c_workflow())
    assert summary["retried_repair_ids"] == ["Hab-07"]
    assert repair_calls == 2
    assert any("dispatch-repair" in c and "--ids Hab-07" in c for c in cli_calls)


def test_cta_pipeline_and_full_pipeline_orchestration(tmp_path: Path) -> None:
    work_dir = tmp_path / "work"
    dispatch_dir = work_dir / "dispatch"
    shards_dir = work_dir / "shards"
    dispatch_dir.mkdir(parents=True)
    shards_dir.mkdir(parents=True)
    (work_dir / "cta.json").write_text('{"competencies": []}', encoding="utf-8")
    (dispatch_dir / "cta.json").write_text(
        json.dumps({"Subagents": [{"Role": "CTA Mapper 01", "Prompt": "Map CTA. DONE: part_01.json"}]}),
        encoding="utf-8",
    )

    cli_cmds: List[str] = []
    agent_roles: List[str] = []
    matrix_round = 0

    async def _agent_fn(**kwargs: Any) -> str:
        role = str(kwargs.get("role") or kwargs.get("Role") or "")
        agent_roles.append(role)
        if "Repair" in role:
            (shards_dir / "shard_01.json").write_text("{}", encoding="utf-8")
        return "DONE: ok"

    async def _cli_fn(cmd: str, label: str = "", env_extra: Any = None) -> str:
        nonlocal matrix_round
        cli_cmds.append(cmd)
        def _w_fresh(p: Path, data: Any) -> None:
            p.write_text(json.dumps(data), encoding="utf-8")
            ts = time.time() + 1.0
            os.utime(p, (ts, ts))

        if "--stage cta" in cmd and not (work_dir / ".harm_done").exists():
            (work_dir / ".harm_done").write_text("1", encoding="utf-8")
            _w_fresh(
                dispatch_dir / "cta_reduce.json",
                {"Subagents": [{"Role": "CTA Harmonizer", "Prompt": "Harmonize. DONE: cta.json"}]},
            )
        elif "dispatch-authors" in cmd:
            _w_fresh(
                dispatch_dir / "authors.json",
                {"Subagents": [{"Role": "Author 01", "Prompt": "Write. DONE: ok"}]},
            )
        elif "dispatch-judges" in cmd:
            _w_fresh(
                dispatch_dir / "judges.json",
                {"Subagents": [{"Role": "Judge 01", "Prompt": "Judge. DONE: ok"}]},
            )
        elif "--stage gates" in cmd:
            if matrix_round == 0:
                _w_fresh(work_dir / "repair_matrix.json", {"failing_competencies": ["Hab-01"]})
                return "FAIL: dispatch-repair needed for Hab-01"
            _w_fresh(work_dir / "repair_matrix.json", {"failing_competencies": []})
        elif "--stage repair-matrix" in cmd:
            matrix_round += 1
            failing = ["Hab-01"] if matrix_round == 1 else []
            _w_fresh(work_dir / "repair_matrix.json", {"failing_competencies": failing})
        elif "dispatch-repair" in cmd:
            _w_fresh(
                dispatch_dir / "repair.json",
                {"Subagents": [{"Role": "Repair 01", "shard_id": "shard_01", "assigned_competencies": ["Hab-01"], "Prompt": "Repair. DONE: ok"}]},
            )
        elif "--stage" in cmd and "rejudge" in cmd and "compare" not in cmd:
            _w_fresh(
                dispatch_dir / "judges.json",
                {"Subagents": [{"Role": "Rejudge 01", "Prompt": "Rejudge. DONE: ok"}]},
            )
        return "ok"

    wf, _ = _load_workflow(
        {
            "work_dir": str(work_dir),
            "mode": "full_pipeline",
            "comps_per_shard": 2,
            "max_repair_rounds": 2,
            "startup_stagger_s": 0.0,
        },
        agent_fn=_agent_fn,
        run_cli_fn=_cli_fn,
    )
    wf.run_cli = _cli_fn
    summary = asyncio.run(wf.run_c2c_workflow())

    assert summary["mode"] == "full_pipeline"
    assert summary["cta_workers_completed"] == 1
    assert summary["harmonizer_completed"] == 1
    assert summary["repair_rounds_executed"] == 1
    assert summary["remaining_failing_ids"] == []
    assert "CTA Harmonizer" in agent_roles
    assert "Repair 01" in agent_roles
    assert any("--stage shard" in c and "--comps-per-shard 2" in c for c in cli_cmds)


def test_post_cta_pipeline_clears_stale_repair_matrix_after_round_1(tmp_path: Path) -> None:
    work_dir = tmp_path / "work"
    dispatch_dir = work_dir / "dispatch"
    shards_dir = work_dir / "shards"
    dispatch_dir.mkdir(parents=True)
    shards_dir.mkdir(parents=True)
    (work_dir / "cta.json").write_text('{"competencies": []}', encoding="utf-8")

    repair_matrix_calls = 0

    async def _agent_fn(**kwargs: Any) -> str:
        role = str(kwargs.get("role") or kwargs.get("Role") or "")
        if "Repair" in role:
            (shards_dir / "shard_01.json").write_text("{}", encoding="utf-8")
        return "DONE: ok"

    async def _cli_fn(cmd: str, label: str = "", env_extra: Any = None) -> str:
        nonlocal repair_matrix_calls
        if "dispatch-authors" in cmd:
            (dispatch_dir / "authors.json").write_text(
                json.dumps({"Subagents": [{"Role": "Author 01", "Prompt": "Write. DONE: ok"}]}),
                encoding="utf-8",
            )
        elif "dispatch-judges" in cmd:
            (dispatch_dir / "judges.json").write_text(
                json.dumps({"Subagents": [{"Role": "Judge 01", "Prompt": "Judge. DONE: ok"}]}),
                encoding="utf-8",
            )
        elif "--stage gates" in cmd:
            # Real `--stage gates` never overwrites repair_matrix.json
            if repair_matrix_calls == 0:
                return "FAIL: dispatch-repair needed for Hab-01"
            return "PASS: all gates clean"
        elif "--stage repair-matrix" in cmd:
            repair_matrix_calls += 1
            (work_dir / "repair_matrix.json").write_text(
                json.dumps({"failing_competencies": ["Hab-01"]}),
                encoding="utf-8",
            )
        elif "dispatch-repair" in cmd:
            (dispatch_dir / "repair.json").write_text(
                json.dumps({"Subagents": [{"Role": "Repair 01", "shard_id": "shard_01", "assigned_competencies": ["Hab-01"], "Prompt": "Repair. DONE: ok"}]}),
                encoding="utf-8",
            )
        elif "--stage" in cmd and "rejudge" in cmd and "compare" not in cmd:
            (dispatch_dir / "judges.json").write_text(
                json.dumps({"Subagents": [{"Role": "Rejudge 01", "Prompt": "Rejudge. DONE: ok"}]}),
                encoding="utf-8",
            )
        return "ok"

    wf, _ = _load_workflow(
        {
            "work_dir": str(work_dir),
            "mode": "post_cta_pipeline",
            "max_repair_rounds": 2,
            "startup_stagger_s": 0.0,
        },
        agent_fn=_agent_fn,
        run_cli_fn=_cli_fn,
    )
    wf.run_cli = _cli_fn
    summary = asyncio.run(wf.run_c2c_workflow())

    assert repair_matrix_calls == 1
    assert summary["repair_rounds_executed"] == 1
    assert summary["remaining_failing_ids"] == []
    assert not (work_dir / "repair_matrix.json").exists()


# ---------------------------------------------------------------------------
# 2. plan_shards default 3 + explicit 2 cap, prompt_repair & SKILL alignment
# ---------------------------------------------------------------------------


def test_plan_shards_default_three_and_explicit_two_caps_skills(tmp_path: Path) -> None:
    assert plan_shards.DEFAULT_COMPS_PER_SHARD == 3
    comps = [
        {"id": f"C-{i:02d}", "type": "concept", "name": f"Concepto Teorico Alpha {i}", "bloom": "Understand", "prerequisites": []}
        for i in range(1, 4)
    ] + [
        {"id": f"Hab-{i:02d}", "type": "skill", "name": f"Habilidad Aplicada Beta {i}", "bloom": "Analyze", "prerequisites": []}
        for i in range(1, 5)
    ]
    work_dir = tmp_path / "work"
    work_dir.mkdir(parents=True)
    cta_file = work_dir / "cta.json"
    cta_file.write_text(json.dumps({"course_id": "test_shard", "competencies": comps}), encoding="utf-8")
    (work_dir / "pre_cta_manifest.json").write_text(
        json.dumps({"course_id": "test_shard", "files": [{"doc": "notes.pdf", "total_pages": 10}]}),
        encoding="utf-8",
    )

    # Default K=2 keeps DEFAULT_COMPS_PER_SHARD = 3 for non-skill and 2 for skills
    out_def = work_dir / "shards_default"
    manifest_def = plan_shards.plan_shards(cta_file, out_def, templates_per_modality=2)
    def _comp_id(entry: Any) -> str:
        return entry.get("id", "") if isinstance(entry, dict) else str(entry)

    non_skill_counts = [
        len(s["competencies"])
        for s in manifest_def["shards"]
        if any(_comp_id(c).startswith("C-") for c in s["competencies"])
    ]
    assert max(non_skill_counts) == 3

    # Explicit max_comps=2 caps both non-skill and skill shards at <= 2
    out_two = work_dir / "shards_two"
    manifest_two = plan_shards.plan_shards(cta_file, out_two, max_comps=2, templates_per_modality=2)
    all_counts = [len(s["competencies"]) for s in manifest_two["shards"]]
    assert max(all_counts) <= 2


def test_prompt_repair_no_max4_edit_cap_and_epistemic_sweep() -> None:
    repair_md = (_C2C_DIR / "system_prompts" / "prompt_repair.md").read_text(encoding="utf-8")
    lean_repair_md = (_C2C_DIR / "system_prompts" / "lean" / "prompt_repair.md").read_text(encoding="utf-8")
    subtypes = (_C2C_DIR / "subagent_types.json").read_text(encoding="utf-8")
    skill_md = (_C2C_DIR / "SKILL.md").read_text(encoding="utf-8")

    for text in (repair_md, lean_repair_md, subtypes):
        assert "máximo 4 llamadas `edit_file`" not in text
        assert "check_runs >= 1" in text
        assert "compile_shard.py" in text

    assert "Epistemic Sweep" in repair_md and "plantillas hermanas de la competencia" in repair_md
    assert "full_pipeline" in skill_md
    assert "comps_per_shard" in skill_md
    assert "cta_pipeline" in skill_md


# ---------------------------------------------------------------------------
# 3. Template healing + compiler proper-noun comma + MS pre-interp verifier
# ---------------------------------------------------------------------------


def test_heal_katex_display_str_preserves_eval_and_heals_display() -> None:
    sample = "Considere $2@c@$ y $@a@@b@$, con $x**2$, $sqrt(x)$ y paso $1e-05$ fuera 2*x"
    healed = heal_katex_display_str(sample)
    assert r"2 \cdot @c@" in healed
    assert r"@a@ \cdot @b@" in healed
    assert r"x^{2}" in healed
    assert r"\sqrt{x}" in healed
    assert r"1 \times 10^{-5}" in healed
    # Prose outside $...$ stays untouched
    assert healed.endswith("fuera 2*x")

    tpl = {
        "id": "T-01",
        "interaction_type": "fill_in_the_blank",
        "stem": "Calcule $2@c@$ cuando $y = x**2$",
        "hints": ["Recuerde $@a@@b@$"],
        "solution": "Usando $sqrt(x)$ y error $1e-05$",
        "generate_py": "def generate(rng):\n    return {'vars': {'c': 3, 'a': 2, 'b': 4, 'x': 9}, 'correct': '2*@c@', 'accepted_equivalents': ['x**2']}",
    }
    auto_heal_template_data([tpl])
    assert r"2 \cdot @c@" in tpl["stem"]
    assert r"x^{2}" in tpl["stem"]
    assert r"@a@ \cdot @b@" in tpl["hints"][0]
    assert r"\sqrt{x}" in tpl["solution"]
    assert r"1 \times 10^{-5}" in tpl["solution"]
    assert "'correct': '2*@c@'" in tpl["generate_py"]
    assert "'accepted_equivalents': ['x**2']" in tpl["generate_py"]


def test_heal_katex_display_str_preserves_euler_and_escaped_dollar() -> None:
    euler_text = "Compare $2e-1$, $3e+2$, y $2e-3$ frente a $1e-05$ y $2.5E+08$."
    healed_euler = heal_katex_display_str(euler_text)
    assert "$2e-1$" in healed_euler
    assert "$3e+2$" in healed_euler
    assert "$2e-3$" in healed_euler
    assert r"$1 \times 10^{-5}$" in healed_euler
    assert r"$2.5 \times 10^{8}$" in healed_euler
    assert heal_katex_display_str("$1e-00$") == r"$1 \times 10^{0}$"

    escaped_currency = r"El costo es \$100 y la curva es $x**2$ con paso $1e-05$."
    healed_currency = heal_katex_display_str(escaped_currency)
    assert r"\$100 y la curva es $x^{2}$" in healed_currency
    assert r"$1 \times 10^{-5}$" in healed_currency


def test_shard_compiler_proper_noun_comma_allowed_and_ms_pre_interp_fallback() -> None:
    comp_map = {
        "C-01": {
            "id": "C-01",
            "type": "concept",
            "bloom": "Evaluate",
            "distractors": [
                {"id": "D-C01-01"},
                {"id": "D-C01-02"},
                {"id": "D-C01-03"},
            ],
        }
    }

    def gen_ok(rng: Any) -> Dict[str, Any]:
        k = rng.choice([2, 3, 4, 5, 6, 7])
        k_star = k * 2
        return {
            "vars": {"k": k, "k_star": k_star},
            "options": [
                {"value": "El modelo con $k=@k@$ alcanza $k^*=@k_star@$", "is_correct": True},
                {"value": "El crecimiento requiere $k^*=@k_star@$ para $k=@k@$", "is_correct": True},
                {"value": "Confunde $k=@k@$ con equilibrio nulo", "is_correct": False, "distractor_id": "D-C01-01", "error_rationale": "Usó $k+1$ en lugar de duplicar el valor parametrico $k=@k@$."},
                {"value": "Asume tasa nula cuando $k=@k@$", "is_correct": False, "distractor_id": "D-C01-02", "error_rationale": "Anuló erróneamente la acumulación positiva para $k=@k@$."},
            ],
        }

    def ver_pre_interp(inst: Dict[str, Any]) -> bool:
        # Written expecting concrete interpolated @k@ / @k_star@ inside options + checks is_correct/rationale/did
        v = inst["vars"]
        k = v["k"]
        k_star = v["k_star"]
        opts = inst["options"]
        if k_star != 2 * k or sum(1 for o in opts if o.get("is_correct")) != 2:
            return False
        true_ok = all("@k@" not in str(o.get("value", "")) and str(k_star) in str(o.get("value", "")) for o in opts if o.get("is_correct"))
        false_ok = all(
            str(k_star) not in str(o.get("value", ""))
            and len(str(o.get("error_rationale") or "").strip()) >= 20
            and str(o.get("distractor_id") or "") in {"D-C01-01", "D-C01-02"}
            for o in opts if not o.get("is_correct")
        )
        return true_ok and false_ok

    tpl = {
        "id": "T-C01-01",
        "cid": "C-01",
        "qtype": "multiple_select",
        "gen": gen_ok,
        "ver": ver_pre_interp,
        "band": ("medium", "Evaluate"),
        "stems": [
            "En el equilibrio de largo plazo, Solow demostró que con $k=@k@$ converge hacia $@k_star@$. ¿Qué afirma el teorema?",
            "Para la tasa de ahorro dada, Solow mostró que si $k=@k@$ entonces el nivel estacionario es $@k_star@$.",
            "Bajo los supuestos neoclásicos, Solow verificó que $k=@k@$ implica $@k_star@$. Identifique dos consecuencias.",
        ],
        "hints": [
            "Compare el parámetro $k=@k@$ con su trayectoria.",
            "Verifique la condición de estado estacionario con $@k_star@$.",
            "Sustituya $k=@k@$ para obtener $2k=@k_star@$.",
        ],
        "sol": "En el modelo, Solow demuestra que para $k=@k@$ el valor estacionario cumple $k^*=2k=@k_star@$.",
        "archetype": "perturbation",
        "rats": {
            "D-C01-01": "Usó $k+1$ en lugar de duplicar $k=@k@$.",
            "D-C01-02": "Anuló erróneamente la acumulación para $k=@k@$.",
        },
    }

    t_out: Dict[str, List[Dict[str, Any]]] = {}
    g_out: Dict[str, List[Any]] = {}
    dup_errs: List[str] = []
    ver_errs: List[str] = []
    s5_errs: List[str] = []
    dummy_locator = ShardDataLineLocator("")
    res = scs.compile_tuple_records_to_templates(
        tuple_records=[{"tuple": tpl, "locator": dummy_locator, "file_path": Path("shard_01.py"), "orig_idx": 0}],
        cta_comp_map=comp_map,
        strict=True,
        module_rats={},
        norm_shard_id="shard_01",
        templates_by_cid=t_out,
        gen_callables_by_cid=g_out,
        deferred_hints_dup_errors=dup_errs,
        deferred_verifier_errors=ver_errs,
        step5_err_fn=lambda msg, **kw: s5_errs.append(msg),
        fail_fn=lambda msg: s5_errs.append(msg),
    )
    assert res is None
    assert s5_errs == [], f"Unexpected Step5 errors: {s5_errs}"
    assert ver_errs == [], f"Unexpected verifier errors: {ver_errs}"
    assert "T-C01-01" in [x["id"] for x in t_out["C-01"]]


# ---------------------------------------------------------------------------
# 4. check_cta prefix mismatch (H-/F-) & D1 overlap + check_templates Bloom
# ---------------------------------------------------------------------------


def test_check_cta_prefix_mismatch_and_d1_disambiguation() -> None:
    c_h = _make_valid_comp(
        "H-01", "fact", "Axioma de Kolmogorov sobre medida unitaria",
        desc="Probabilidad asignada al espacio muestral completo normalizada exactamente igual a uno.",
        bloom="Remember", modalities=["fill_in_the_blank", "multiple_select"], prereqs=[],
    )
    c_f = _make_valid_comp(
        "F-02", "fact", "Identidad de Wald para sumas aleatorias",
        desc="Valor esperado de suma aleatoria con tiempo de parada finito independiente.",
        bloom="Remember", modalities=["fill_in_the_blank", "multiple_select"], prereqs=["H-01"],
    )
    c_fact = _make_valid_comp(
        "Fact-03", "fact", "Desigualdad de Chebyshev en colas",
        desc="Cota superior cuadratica basada en varianza poblacional respecto al promedio.",
        bloom="Remember", modalities=["fill_in_the_blank", "multiple_select"], prereqs=["H-01"],
    )
    c_skill = _make_valid_comp(
        "Hab-01", "skill", "Calculo de estimadores maximo verosimiles",
        desc="Derivacion algebraica de log-verosimilitud concava y solucion numerica optima.",
        bloom="Evaluate", prereqs=["Fact-03"],
    )
    c_c = _make_valid_comp(
        "C-01", "concept", "Interpretacion geometrica de ortogonalidad",
        desc="Proyeccion minima cuadratica en subespacios lineales cerrados de Hilbert.",
        bloom="Evaluate", prereqs=["Fact-03"],
    )

    # Both H- (Hecho) and Fact- pass with zero prefix errors; F- passes prefix check in _validate_competencies_rules
    cta_ok = {"contract_version": 2, "competencies": [c_h, c_fact, c_c, c_skill]}
    ok_flag, ok_errs = check_cta.validate_cta_rules(
        cta_ok, manifest_data=_make_manifest_data(cta_ok["competencies"]), enforce_bloom_gate=False,
    )
    assert ok_flag, f"Expected H-/Fact- valid: {ok_errs}"
    assert not any("[CTA-PREFIX-TYPE-MISMATCH]" in e for e in ok_errs)

    f_errs = check_cta._validate_competencies_rules([c_f], require_assumptions=False, require_modalities=False)
    assert not any("[CTA-PREFIX-TYPE-MISMATCH]" in e for e in f_errs)

    # H-02 typed as concept triggers hard blocking FAIL: [CTA-PREFIX-TYPE-MISMATCH]
    c_bad_prefix = _make_valid_comp(
        "H-02", "concept", "Geometria espectral de matrices simetricas",
        desc="Diagonalizacion ortogonal real mediante autovalores reales positivos.",
        bloom="Evaluate",
    )
    pfx_flag, pfx_errs = check_cta.validate_cta_rules(
        {"contract_version": 2, "competencies": [c_bad_prefix]},
        manifest_data=_make_manifest_data([c_bad_prefix]),
        enforce_bloom_gate=False,
    )
    assert pfx_flag is False
    assert any("[CTA-PREFIX-TYPE-MISMATCH]" in e for e in pfx_errs)

    # Severe same-category overlap triggers [CTA-OVERLAP-HIGH]
    c_dup1 = _make_valid_comp("C-01", "concept", "Teorema del limite central asintotico", bloom="Evaluate")
    c_dup2 = _make_valid_comp("C-02", "concept", "Teorema del limite central y convergencia", bloom="Evaluate")
    high_flag, high_errs = check_cta.validate_cta_rules(
        {"contract_version": 2, "competencies": [c_dup1, c_dup2]},
        manifest_data=_make_manifest_data([c_dup1, c_dup2]),
        enforce_bloom_gate=False,
    )
    assert not high_flag
    assert any("[CTA-OVERLAP-HIGH]" in e for e in high_errs)

    # Indexed pair ("Error Tipo I" vs "Error Tipo II") passes cleanly without false overlap errors
    c_idx1 = _make_valid_comp(
        "C-02", "concept", "Error Tipo I en contraste bilateral",
        desc="Probabilidad alfa de rechazar hipotesis nula verdadera bajo distribucion gaussiana.",
        bloom="Evaluate", prereqs=["Fact-03"],
    )
    c_idx2 = _make_valid_comp(
        "C-03", "concept", "Error Tipo II en contraste bilateral",
        desc="Probabilidad beta de no rechazar hipotesis alternativa falsa en muestras finitas.",
        bloom="Evaluate", prereqs=["Fact-03"],
    )
    idx_flag, idx_errs = check_cta.validate_cta_rules(
        {"contract_version": 2, "competencies": [c_h, c_fact, c_c, c_idx1, c_idx2]},
        manifest_data=_make_manifest_data([c_h, c_fact, c_c, c_idx1, c_idx2]),
        enforce_bloom_gate=False,
    )
    assert idx_flag, f"Unexpected errors on indexed pair: {idx_errs}"
    assert not any("[CTA-OVERLAP-HIGH]" in e for e in idx_errs)

    # Moderate overlap triggers non-blocking [CTA-OVERLAP-WARN]
    warns: List[str] = []
    c_w1 = _make_valid_comp(
        "C-02", "concept", "Criterio de convexidad global",
        desc="Evaluacion de matriz hessiana definida positiva con gradiente estacionario en optimizacion concava.",
        bloom="Evaluate", prereqs=["Fact-03"],
    )
    c_w2 = _make_valid_comp(
        "C-03", "concept", "Condiciones de optimalidad interior",
        desc="Analisis de matriz hessiana definida con gradiente estacionario en optimizacion acotada.",
        bloom="Evaluate", prereqs=["Fact-03"],
    )
    warn_flag, warn_errs = check_cta.validate_cta_rules(
        {"contract_version": 2, "competencies": [c_h, c_fact, c_c, c_w1, c_w2]},
        manifest_data=_make_manifest_data([c_h, c_fact, c_c, c_w1, c_w2]),
        enforce_bloom_gate=False,
        warnings_out=warns,
    )
    assert warn_flag, f"Unexpected errors: {warn_errs}"
    assert any("[CTA-OVERLAP-WARN]" in w for w in warns)


def test_check_templates_bloom_superior_target_non_blocking_warning(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    tpl_file = tmp_path / "C-01.json"
    tpls = [
        {
            "id": f"T-C01-0{i}",
            "competency_id": "C-01",
            "bloom": "Apply",
            "difficulty": "medium",
            "interaction_type": "fill_in_the_blank",
            "stem": f"Calcule el valor estacionario cuando $a=@a@$ y $b=@b@$ en escenario {i} inciso A.",
            "stem_variants": [
                f"Calcule el valor estacionario cuando $a=@a@$ y $b=@b@$ en escenario {i} inciso A.",
                f"Determine el nivel cuando $a=@a@$ y $b=@b@$ en escenario {i} inciso B.",
                f"Encuentre el resultado cuando $a=@a@$ y $b=@b@$ en escenario {i} inciso C.",
            ],
            "hints": [
                f"Use la sustitucion directa con $a=@a@$ para caso {i}.",
                f"Combine $a=@a@$ y $b=@b@$ en la identidad {i}.",
                f"Verifique la suma $@a@ + @b@$ del modelo {i}.",
            ],
            "solution": f"Sumando $a=@a@$ y $b=@b@$ en escenario {i} se obtiene el resultado exacto $@ans@$.",
            "distractor_ids": [],
            "generate_py": (
                "def generate(rng):\n"
                f"    a = rng.randint({i}, {i + 6})\n"
                "    b = rng.randint(2, 9)\n"
                "    ans = a + b\n"
                "    return {'vars': {'a': a, 'b': b, 'ans': ans}, 'correct': str(ans), 'accepted_equivalents': []}\n"
            ),
            "cross_check_py": "def cross_check(inst):\n    assert int(inst['correct']) == inst['vars']['a'] + inst['vars']['b']\n    return True\n",
        }
        for i in range(1, 5)
    ]
    tpl_file.write_text(json.dumps(tpls, ensure_ascii=False), encoding="utf-8")
    warns: List[str] = []
    valid, errors = check_templates.check_templates_file_or_dir(
        tpl_file,
        cta_path=None,
        num_dry_run_seeds=5,
        strict=False,
        auto_fix=False,
        attempts_dir=tmp_path / ".attempts",
        warnings_out=warns,
    )
    assert valid is True, f"Expected non-blocking Bloom warning only, got errors: {errors}"
    assert any("[BLOOM-SUPERIOR-TARGET]" in w for w in warns)
    captured = capsys.readouterr()
    assert "[BLOOM-SUPERIOR-TARGET]" in captured.err


# ---------------------------------------------------------------------------
# 5. Course QA Evaluator: d5_fb residues, $3=3$ rationale, static warning, SKILL
# ---------------------------------------------------------------------------


def test_qa_evaluator_residues_fb_tautology_rationale_static_warning_and_skill() -> None:
    sae = _load_module_isolated("sae_v44_test", _QA_SCRIPTS_DIR / "standardized_audit_engine.py", _QA_SCRIPTS_DIR)

    # d5_fb breakdown includes template_vars and blind_repl counts
    rubric = sae.compute_deterministic_rubric_scores(
        summaries={
            "blind_string_replacement_linter": {"blind_string_replacement_count": 5},
            "template_variable_residue_linter": {"template_variable_residue_count": 0},
        },
        total_comps=1,
        total_questions=10,
        hard_penalties=[],
    )
    d5_fb = rubric["dimension_scores"]["technical_ergonomics"]["feedback"]
    assert rubric["dimension_scores"]["technical_ergonomics"]["score"] == 1.5
    assert "template_vars=0, blind_repl=5" in d5_fb

    # R-TAUTOLOGICAL-PARAM-EQUALITY-IN-RATIONALE + static_misconception_warning_uninstantiated_params
    course_data = {
        "course_id": "test_qa_v44",
        "title": "Test QA",
        "competencies": [{"id": "Hab-04", "type": "skill", "name": "Ecuaciones dinamicas", "bloom": "Evaluate"}],
        "questions": [
            {
                "id": "Q-Hab04-01",
                "competency_id": "Hab-04",
                "interaction_type": "multiple_choice_7_options",
                "bloom": "Evaluate",
                "stem": "Resuelva $t_1^2 - 24 = 0$ considerando el horizonte positivo.",
                "options": [
                    {"id": "opt_1", "text": "$\\sqrt{24}$", "is_correct": True, "error_rationale": "Correcto: sustituye $24$ correctamente."},
                    {"id": "opt_2", "text": "$3$", "is_correct": False, "error_rationale": "Error algebraico porque mantuvo $3=3$ al despejar."},
                ],
                "hints": ["Identifique el termino constante $24$.", "Despeje $t_1^2$.", "Tome la raiz positiva."],
                "detailed_solution": {
                    "solution_steps": "De $t_1^2 = 24$ resulta $t_1 = \\sqrt{24}$.",
                    "misconception_warning": "Un error frecuente es olvidar los signos al despejar $t_1^2 - 60 = 0$.",
                },
            },
            {
                "id": "Q-Hab04-02",
                "competency_id": "Hab-04",
                "interaction_type": "multiple_choice_7_options",
                "bloom": "Evaluate",
                "stem": "Resuelva $t_1^2 - 15 = 0$ considerando el horizonte positivo.",
                "options": [
                    {"id": "opt_1", "text": "$\\sqrt{15}$", "is_correct": True, "error_rationale": "Correcto."},
                    {"id": "opt_2", "text": "$5$", "is_correct": False, "error_rationale": "Error de factorizacion en $15$."},
                ],
                "hints": ["Identifique el termino constante $15$.", "Despeje $t_1^2$.", "Tome la raiz positiva."],
                "detailed_solution": {
                    "solution_steps": "De $t_1^2 = 15$ resulta $t_1 = \\sqrt{15}$.",
                    "misconception_warning": "Un error frecuente es olvidar los signos al despejar $t_1^2 - 60 = 0$.",
                },
            },
        ],
    }
    res = sae.run_full_audit(course_data)
    scaf_sm = res["dimension_summaries"]["scaffolding_hints_linter"]
    erg_sm = res["dimension_summaries"]["katex_frontend_ergonomics_linter"]
    assert scaf_sm["static_misconception_warning_uninstantiated_count"] == 2
    assert erg_sm["tautological_identity_items_count"] == 1
    msgs = [i["message"] for i in res["all_issues"]]
    assert any("[static_misconception_warning_uninstantiated_params]" in m for m in msgs)
    assert any("[R-TAUTOLOGICAL-PARAM-EQUALITY-IN-RATIONALE]" in m for m in msgs)

    qa_skill_md = (_ROOT / ".agents" / "skills" / "course-qa-evaluator" / "SKILL.md").read_text(encoding="utf-8")
    assert "reports/qa_audits/<course_id>_qa_report.md" in qa_skill_md
    assert "reports/audits_archive/<course_id>/" in qa_skill_md


# ---------------------------------------------------------------------------
# 6. Run Auditor: filter WARNING lines in first_compile_rules + separate 429
# ---------------------------------------------------------------------------


def test_run_auditor_filters_warning_lines_and_separates_429() -> None:
    ae = _load_module_isolated("ae_v44_test", _AUDIT_SCRIPTS_DIR / "audit_engine.py", _AUDIT_SCRIPTS_DIR)
    ta = _load_module_isolated("ta_v44_test", _AUDIT_SCRIPTS_DIR / "traceback_analyzer.py", _AUDIT_SCRIPTS_DIR)

    auditor = ae.ExecutionAuditor([], "root-v44")
    auditor.brain_dir = _ROOT
    records = [
        {
            "type": "PLANNER_RESPONSE",
            "step_index": 1,
            "created_at": "2026-11-21T10:00:00Z",
            "input_tokens": 100,
            "output_tokens": 50,
            "tool_calls": [
                {
                    "name": "run_command",
                    "args": {"CommandLine": "python compile_shard.py work/shards/shard_01.py"},
                }
            ],
        },
        {
            "type": "TOOL_RESPONSE",
            "step_index": 2,
            "created_at": "2026-11-21T10:00:05Z",
            "content": (
                "WARNING: [TPL-ORPHAN-VARS] Variable no usada 'tmp'\n"
                "INFO: [PRECHECK] Saltando cache\n"
                "FAIL: [VERIFIER-TAUTOLOGY-DETECTED] Verificador no refuto mutacion\n"
                "Command exited with code 1."
            ),
        },
    ]
    metrics = auditor._analyze_conversation(records, "author-v44", "Author 01")
    assert metrics["compile_first_passed"] is False
    assert metrics["first_compile_rules"] == ["VERIFIER-TAUTOLOGY-DETECTED"]

    steps = [
        {
            "type": "ERROR_MESSAGE",
            "step_index": 3,
            "content": "429 RESOURCE_EXHAUSTED: You have exhausted your capacity for this model.",
        },
        {
            "type": "ERROR_MESSAGE",
            "step_index": 4,
            "content": "Response exceeded the output token limit before completion.",
        },
    ]
    cats = ta.ForensicsEngine.classify_error_taxonomy({"worker-01": steps})
    assert len(cats["API Rate Limit (429 RESOURCE_EXHAUSTED)"]) == 1
    assert len(cats["Token Limit Cutoff (Model Truncation)"]) == 1

    cta_turns_rate_limit = [{"step_index": 1, "output_tokens": 100, "results": [{"type": "ERROR_MESSAGE", "content": "429 RESOURCE_EXHAUSTED"}]}]
    cta_turns_cutoff = [{"step_index": 1, "output_tokens": 8000, "results": [{"type": "ERROR_MESSAGE", "content": "exceeded the output token limit"}]}]
    assert ta.ForensicsEngine.audit_cta_architect([], cta_turns_rate_limit)["cutoff_detected"] is False
    assert ta.ForensicsEngine.audit_cta_architect([], cta_turns_cutoff)["cutoff_detected"] is True
