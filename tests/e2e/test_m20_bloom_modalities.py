"""Playwright E2E tests for Milestone 20 Core:
- Loads real C2C-compiled m20_canonical_course.json via route interception (courses/ stays 100% clean)
- Verifies Smart Blank-First curtain visibility/skip across all 9 modalities
- Exercises palette insertion, algebraic equivalence, Fibonacci/profit & symbolic ds traps
- Verifies alternative valid ProofDAG topological ordering + justifications + fallacy rejection
- Verifies AdversarialBreak (find_fallacy & counterexample), UnstructuredModel Stage 0 phase locks/error counting
- Verifies InvariantCanvas (cartesian piecewise kink & extensive-form tree info sets) & ConceptMatching
- Verifies zero horizontal overflow at 1280x800 and 640x720 and zero console/page errors
"""

from __future__ import annotations

import copy
import json
import os
import re
import shutil
import socket
import subprocess
import sys
import time
import urllib.request
from pathlib import Path
from typing import Any, Dict, List, Tuple

import pytest
from playwright.sync_api import sync_playwright, expect


ROOT_DIR = Path(__file__).resolve().parent.parent.parent
PLATFORM_DIR = ROOT_DIR / "platform"
FIXTURE_COURSE_PATH = ROOT_DIR / "tests" / "fixtures" / "m20_canonical_cases" / "m20_canonical_course.json"


def _find_free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 0))
        return int(s.getsockname()[1])


def _resolve_chromium_executable() -> str | None:
    for env_key in ("LOCALAPPDATA", "USERPROFILE"):
        base = os.environ.get(env_key, "")
        if not base:
            continue
        ms_dir = Path(base) / ("ms-playwright" if env_key == "LOCALAPPDATA" else "AppData/Local/ms-playwright")
        if ms_dir.is_dir():
            for chrome_dir in sorted(ms_dir.glob("chromium-*"), reverse=True):
                for sub in ("chrome-win64", "chrome-win"):
                    exe = chrome_dir / sub / "chrome.exe"
                    if exe.is_file():
                        return str(exe)
    return None


@pytest.fixture(scope="module")
def vite_server_url():
    """Start an isolated static Vite preview server for this module on a free port and clean up reliably."""
    port = _find_free_port()
    npx_cmd = shutil.which("npx.cmd") or shutil.which("npx") or "npx"
    proc = subprocess.Popen(
        [npx_cmd, "vite", "preview", "--port", str(port), "--strictPort", "--host", "127.0.0.1"],
        cwd=str(PLATFORM_DIR),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        shell=False,
    )
    base_url = f"http://127.0.0.1:{port}"
    deadline = time.time() + 25.0
    ready = False
    while time.time() < deadline:
        try:
            with urllib.request.urlopen(base_url, timeout=1.0) as resp:
                if resp.status == 200:
                    ready = True
                    break
        except Exception:
            time.sleep(0.3)

    if not ready:
        proc.terminate()
        raise RuntimeError(f"Vite dev server failed to become ready at {base_url}")

    yield base_url

    try:
        if os.name == "nt":
            subprocess.run(
                ["taskkill", "/F", "/T", "/PID", str(proc.pid)],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                check=False,
            )
        else:
            proc.terminate()
            proc.wait(timeout=5)
    except Exception:
        pass


@pytest.fixture(scope="module")
def m20_browser():
    """Chromium browser adhering to CONOCIMIENTO_TRIBAL.md §4.2 (ignore --hide-scrollbars)."""
    headless = os.environ.get("HEADLESS", "1").lower() not in ("0", "false", "no")
    exec_path = _resolve_chromium_executable()
    launch_kwargs: Dict[str, Any] = {
        "headless": headless,
        "args": [
            "--no-sandbox",
            "--disable-dev-shm-usage",
            "--disable-gpu",
            "--window-size=1280,800",
        ],
        "ignore_default_args": ["--hide-scrollbars"],
    }
    if exec_path:
        launch_kwargs["executable_path"] = exec_path

    with sync_playwright() as p:
        browser = p.chromium.launch(**launch_kwargs)
        yield browser
        browser.close()


def _attach_course_routes(context, course_data: Dict[str, Any], course_id: str) -> None:
    payload = json.dumps(course_data, ensure_ascii=False)
    summary = {
        "id": course_id,
        "filename": f"{course_id}.json",
        "title": course_data.get("title") or course_data.get("course_title") or course_id,
        "description": course_data.get("description", ""),
        "competencies_count": len(course_data.get("competencies", [])),
        "questions_count": len(course_data.get("questions", [])),
        "status": "valid",
        "etag": f"etag-{course_id}-m20",
        "bytes": len(payload.encode("utf-8")),
    }
    manifest = json.dumps({"generated_at": "2026-11-18T00:00:00Z", "courses": [summary]}, ensure_ascii=False)
    safe_manifest = manifest.replace("<", "\\u003c")

    def handle_document(route):
        if route.request.resource_type == "document":
            resp = route.fetch()
            html = resp.text()
            html = re.sub(
                r'<script\s+id="course-manifest"[^>]*>[\s\S]*?</script>',
                f'<script id="course-manifest" type="application/json">{safe_manifest}</script>',
                html,
            )
            headers = {k: v for k, v in resp.headers.items() if k.lower() not in ("content-length", "content-encoding")}
            route.fulfill(status=resp.status, headers=headers, body=html)
            return
        route.continue_()

    def handle_route(route):
        path = route.request.url.split("?")[0].rstrip("/")
        if (
            path.endswith("/api/courses.json")
            or path.endswith("/api/courses")
            or path.endswith("/courses/index.json")
        ):
            route.fulfill(status=200, content_type="application/json", body=manifest)
            return
        if (
            path.endswith(f"/api/courses/{course_id}.json")
            or path.endswith(f"/api/courses/{course_id}")
            or path.endswith(f"/courses/{course_id}.json")
        ):
            route.fulfill(
                status=200,
                content_type="application/json",
                headers={"ETag": f'"{summary["etag"]}"'},
                body=payload,
            )
            return
        route.continue_()

    context.route(re.compile(r"^http://127\.0\.0\.1:\d+/?(\?.*)?$"), handle_document)
    context.route("**/api/courses**", handle_route)
    context.route("**/courses/**", handle_route)


def _new_tracked_page(browser, course_data: Dict[str, Any], course_id: str, width: int = 1280, height: int = 800):
    context = browser.new_context(
        viewport={"width": width, "height": height},
        ignore_https_errors=True,
        service_workers="block",
    )
    _attach_course_routes(context, course_data, course_id)
    page = context.new_page()
    console_errors: List[str] = []
    page_errors: List[str] = []

    def on_console(msg):
        if msg.type == "error" and "favicon.ico" not in msg.text:
            console_errors.append(msg.text)

    page.on("console", on_console)
    page.on("pageerror", lambda exc: page_errors.append(str(exc)))
    return context, page, console_errors, page_errors


def _open_course_from_library(page, base_url: str, course_title: str) -> None:
    if page.url.startswith("http"):
        page.evaluate("try { sessionStorage.clear(); } catch {}")
    page.goto(base_url, wait_until="domcontentloaded")
    card = page.locator("[data-testid='course-card']").filter(has_text=course_title).first
    expect(card).to_be_visible(timeout=20000)
    btn = card.locator("button").first
    expect(btn).to_be_visible(timeout=10000)
    btn.click()
    expect(page.locator("[data-testid='completion-tracker-summary']")).to_be_visible(timeout=15000)


def _launch_competency_practice(page, comp_id: str) -> None:
    page.evaluate("sessionStorage.clear();")
    trigger = page.locator(f"[data-testid='competency-{comp_id}']")
    expect(trigger).to_be_visible(timeout=10000)
    trigger.click()
    start_btn = page.locator("[data-testid='start-practice-btn']")
    if start_btn.count() > 0:
        expect(start_btn.first).to_be_visible(timeout=5000)
        start_btn.first.click()
    expect(page.locator("[data-testid='check-btn']")).to_be_visible(timeout=10000)


def _load_compiled_canonical_course() -> Dict[str, Any]:
    assert FIXTURE_COURSE_PATH.is_file(), f"Missing canonical fixture at {FIXTURE_COURSE_PATH}"
    return json.loads(FIXTURE_COURSE_PATH.read_text(encoding="utf-8"))


def _build_deterministic_e2e_projection(base_course: Dict[str, Any]) -> Tuple[Dict[str, Any], Dict[str, Dict[str, Any]]]:
    """Selects 1 real compiled question per modality/submode, each isolated in its own competency."""
    questions = base_course["questions"]

    def _pick(predicate):
        for q in questions:
            if predicate(q):
                return copy.deepcopy(q)
        raise AssertionError("Expected canonical question not found in compiled fixture")

    selected_specs = [
        ("Hab-01", "Skill", _pick(lambda q: q.get("interaction_type") == "open_symbolic" and q.get("competency_id") == "Hab-01")),
        ("Hab-02", "Skill", _pick(lambda q: q.get("interaction_type") == "fill_in_the_blank" and q.get("competency_id") == "Hab-01")),
        ("C-01", "Concept", _pick(lambda q: q.get("interaction_type") == "proof_dag" and q.get("competency_id") == "C-02")),
        ("Hab-03", "Skill", _pick(lambda q: q.get("interaction_type") == "adversarial_break" and (q.get("adversarial_break") or {}).get("mode") == "find_fallacy")),
        ("C-02", "Concept", _pick(lambda q: q.get("interaction_type") == "adversarial_break" and (q.get("adversarial_break") or {}).get("mode") == "counterexample")),
        ("Hab-04", "Skill", _pick(lambda q: q.get("interaction_type") == "unstructured_model" and ((q.get("unstructured_model") or {}).get("phase3_formulation") or {}).get("input_mode") == "select")),
        ("Hab-05", "Skill", _pick(lambda q: q.get("interaction_type") == "invariant_canvas" and (q.get("invariant_canvas") or {}).get("mode") == "cartesian")),
        ("C-03", "Concept", _pick(lambda q: q.get("interaction_type") == "invariant_canvas" and (q.get("invariant_canvas") or {}).get("mode") == "tree")),
        ("C-04", "Concept", _pick(lambda q: q.get("interaction_type") == "concept_matching")),
    ]

    proj_comps: List[Dict[str, Any]] = []
    proj_questions: List[Dict[str, Any]] = []
    by_comp: Dict[str, Dict[str, Any]] = {}

    for new_cid, category, q in selected_specs:
        q["competency_id"] = new_cid
        proj_comps.append(
            {
                "id": new_cid,
                "code": new_cid,
                "name": f"Modality Probe {new_cid}: {q['interaction_type']}",
                "category": category,
                "description": f"Deterministic E2E probe for {q['interaction_type']}",
                "mastery_target": 0.9,
            }
        )
        proj_questions.append(q)
        by_comp[new_cid] = q

    proj_course = {
        "schema_version": "1.0.0",
        "version": "1.0.0",
        "course_id": "m20_e2e_projection",
        "course_title": "M20 E2E Modalities Projection",
        "title": "M20 E2E Modalities Projection",
        "description": "Deterministic single-question-per-competency projection from compiled canonical course.",
        "language": "es",
        "created_at": base_course.get("created_at", "2026-11-18T00:00:00Z"),
        "competencies": proj_comps,
        "questions": proj_questions,
    }
    return proj_course, by_comp


def _retry_click(page) -> None:
    btn = page.locator("[data-testid='check-btn']")
    expect(btn).to_be_visible()
    btn.click()


def test_full_compiled_canonical_course_loads_cleanly(m20_browser, vite_server_url):
    """Loads the real 100-question compiled canonical course without touching courses/ on disk."""
    course = _load_compiled_canonical_course()
    context, page, console_errors, page_errors = _new_tracked_page(
        m20_browser, course, course_id="m20_canonical_course"
    )
    try:
        _open_course_from_library(page, vite_server_url, course["title"])
        for cid in ("Hab-01", "Hab-02", "C-01", "C-02"):
            expect(page.locator(f"[data-testid='competency-block-{cid}']")).to_be_visible()
        _launch_competency_practice(page, "Hab-01")
        assert not console_errors, f"Console errors: {console_errors}"
        assert not page_errors, f"Page errors: {page_errors}"
    finally:
        context.close()


def test_all_bloom_superior_modalities_smart_blank_first_and_grading(m20_browser, vite_server_url):
    """Verifies Smart Blank-First, ds traps, wrong->Try again->right flows across all 6 modalities + FIB ds."""
    base_course = _load_compiled_canonical_course()
    proj_course, by_comp = _build_deterministic_e2e_projection(base_course)
    context, page, console_errors, page_errors = _new_tracked_page(
        m20_browser, proj_course, course_id="m20_e2e_projection"
    )
    try:
        # 1. open_symbolic (Hab-01): skip curtain, palette click, ds trap, algebraically equivalent expression
        q_os = by_comp["Hab-01"]
        _open_course_from_library(page, vite_server_url, proj_course["title"])
        _launch_competency_practice(page, "Hab-01")
        expect(page.locator("[data-testid='blank-first-curtain']")).to_have_count(0)
        expect(page.locator("[data-testid='symbolic-input-root']")).to_be_visible()
        page.locator("[data-testid='math-keypad-toggle-btn']").click()
        expect(page.locator("[data-testid='math-keypad-popover']")).to_be_visible()
        page.locator("[data-testid='math-keypad-key-0']").click()
        page.locator("[data-testid='math-keypad-close-btn']").click()
        trap_os = q_os["diagnostic_distractors"][0]
        page.locator("[data-testid='symbolic-input']").fill(trap_os["expression"])
        page.locator("[data-testid='check-btn']").click()
        expect(page.locator("[data-testid='feedback-toast']")).to_be_visible()
        expect(page.locator("[data-testid='error-rationale-box']")).to_contain_text("Error de signo al derivar")
        _retry_click(page)
        equiv_expr = (q_os["correct_answer"]["accepted_equivalents"] or [q_os["correct_answer"]["value"]])[-1]
        page.locator("[data-testid='symbolic-input']").fill(equiv_expr)
        page.locator("[data-testid='check-btn']").click()
        expect(page.locator("[data-testid='good-work-toast']")).to_be_visible()

        # 2. fill_in_the_blank with ds (Hab-02): skip curtain, ds trap diagnostic, right value
        q_fib = by_comp["Hab-02"]
        _open_course_from_library(page, vite_server_url, proj_course["title"])
        _launch_competency_practice(page, "Hab-02")
        expect(page.locator("[data-testid='blank-first-curtain']")).to_have_count(0)
        trap_fib = q_fib["diagnostic_distractors"][0]
        page.locator("[data-testid='fill-blank-input']").fill(str(trap_fib["value"]))
        page.locator("[data-testid='check-btn']").click()
        expect(page.locator("[data-testid='feedback-toast']")).to_be_visible()
        expect(page.locator("[data-testid='error-rationale-box']")).to_contain_text("maximizado las pérdidas")
        _retry_click(page)
        page.locator("[data-testid='fill-blank-input']").fill(str(q_fib["correct_answer"]["value"]))
        page.locator("[data-testid='check-btn']").click()
        expect(page.locator("[data-testid='good-work-toast']")).to_be_visible()

        # 3. proof_dag (C-01, Roy's Identity): curtain shown, fallacy rejected, alt topo order + justifications accepted
        q_dag = by_comp["C-01"]
        dag_spec = q_dag["proof_dag"]
        steps_by_id = {s["id"]: s for s in dag_spec["steps"]}
        _open_course_from_library(page, vite_server_url, proj_course["title"])
        _launch_competency_practice(page, "C-01")
        expect(page.locator("[data-testid='blank-first-curtain']")).to_be_visible()
        page.locator("[data-testid='lift-curtain-btn']").click()
        expect(page.locator("[data-testid='proof-dag-root']")).to_be_visible()
        page.locator("[data-testid='proof-add-S_BAD']").click()
        page.locator("[data-testid='proof-just-S_BAD']").select_option(steps_by_id["S_BAD"]["justification"])
        page.locator("[data-testid='check-btn']").click()
        expect(page.locator("[data-testid='feedback-toast']")).to_be_visible()
        expect(page.locator("[data-testid='feedback-toast']")).to_contain_text("signo negativo")
        _retry_click(page)
        page.locator("[data-testid='proof-remove-S_BAD']").click()
        for sid in ("S1", "S3", "S2", "S4", "S5"):
            page.locator(f"[data-testid='proof-add-{sid}']").click()
            page.locator(f"[data-testid='proof-just-{sid}']").select_option(steps_by_id[sid]["justification"])
        page.locator("[data-testid='check-btn']").click()
        expect(page.locator("[data-testid='good-work-toast']")).to_be_visible()

        # 4. adversarial_break find_fallacy (Hab-03): no curtain, wrong step -> error, right step+reason -> pass
        q_adv_f = by_comp["Hab-03"]
        adv_f = q_adv_f["adversarial_break"]
        fallacy_id = next(s["id"] for s in adv_f["steps"] if s["is_fallacy"])
        non_fallacy_id = next(s["id"] for s in adv_f["steps"] if not s["is_fallacy"])
        corr_reason_id = next(r["id"] for r in adv_f["reason_options"] if r["is_correct"])
        _open_course_from_library(page, vite_server_url, proj_course["title"])
        _launch_competency_practice(page, "Hab-03")
        expect(page.locator("[data-testid='blank-first-curtain']")).to_have_count(0)
        page.locator(f"[data-testid='adv-step-{non_fallacy_id}']").click()
        page.locator(f"[data-testid='adv-reason-{corr_reason_id}']").click()
        page.locator("[data-testid='check-btn']").click()
        expect(page.locator("[data-testid='feedback-toast']")).to_be_visible()
        _retry_click(page)
        page.locator(f"[data-testid='adv-step-{fallacy_id}']").click()
        page.locator("[data-testid='check-btn']").click()
        expect(page.locator("[data-testid='good-work-toast']")).to_be_visible()

        # 5. adversarial_break counterexample (C-02): no curtain, live readouts, trap/invalid witness -> error, sample_witness -> pass
        q_adv_c = by_comp["C-02"]
        adv_c = q_adv_c["adversarial_break"]
        _open_course_from_library(page, vite_server_url, proj_course["title"])
        _launch_competency_practice(page, "C-02")
        expect(page.locator("[data-testid='blank-first-curtain']")).to_have_count(0)
        if adv_c.get("computed_readouts"):
            expect(page.locator("[data-testid='adv-computed-readouts']")).to_be_visible()
        # Trigger trap_predicates if C-02 is the concave floor contour question (a1, a2, b1, b2)
        input_ids = [inp["id"] for inp in adv_c["inputs"]]
        if set(input_ids) >= {"a1", "a2", "b1", "b2"} and adv_c.get("trap_predicates"):
            k_lvl = int(adv_c["sample_witness"]["a2"]) + 1
            page.locator("[data-testid='adv-input-a1']").fill("0.5")
            page.locator("[data-testid='adv-input-a2']").fill(str(k_lvl - 0.4))
            page.locator("[data-testid='adv-input-b1']").fill("2")
            page.locator("[data-testid='adv-input-b2']").fill(str(k_lvl - 2))
            if adv_c.get("computed_readouts"):
                ro_text = page.locator("[data-testid='adv-computed-readouts']").inner_text()
                assert "—" not in ro_text, f"Expected live readout computation, got: {ro_text}"
        elif input_ids == ["x"]:
            import re as _re
            trap_expr = ((adv_c.get("trap_predicates") or [{}])[0]).get("expr", "")
            m_stat = _re.search(r"abs\(x\s*-\s*([0-9.]+)\)", trap_expr)
            wrong_x = m_stat.group(1) if m_stat else "-5"
            page.locator("[data-testid='adv-input-x']").fill(wrong_x)
            if adv_c.get("computed_readouts"):
                ro_text = page.locator("[data-testid='adv-computed-readouts']").inner_text()
                assert "—" not in ro_text, f"Expected live readout computation, got: {ro_text}"
        else:
            for inp in adv_c["inputs"]:
                page.locator(f"[data-testid='adv-input-{inp['id']}']").fill("-999")
        page.locator("[data-testid='check-btn']").click()
        expect(page.locator("[data-testid='feedback-toast']")).to_be_visible()
        _retry_click(page)
        for iid, wval in adv_c["sample_witness"].items():
            page.locator(f"[data-testid='adv-input-{iid}']").fill(str(wval))
        page.locator("[data-testid='check-btn']").click()
        expect(page.locator("[data-testid='good-work-toast']")).to_be_visible()

        # 6. unstructured_model Stage 0 (Hab-04): no curtain, phase locks, wrong attempt blocks & counts
        q_um = by_comp["Hab-04"]
        um = q_um["unstructured_model"]
        _open_course_from_library(page, vite_server_url, proj_course["title"])
        _launch_competency_practice(page, "Hab-04")
        expect(page.locator("[data-testid='blank-first-curtain']")).to_have_count(0)
        expect(page.locator("[data-testid='stage0-phase-1']")).to_have_attribute("data-phase-state", "active")
        expect(page.locator("[data-testid='stage0-phase-2']")).to_have_attribute("data-phase-state", "locked")
        expect(page.locator("[data-testid='stage0-phase-3']")).to_have_attribute("data-phase-state", "locked")
        # Deliberately wrong role on first variable
        roles = um["phase1_variables"]["roles"]
        first_item = um["phase1_variables"]["items"][0]
        wrong_role = next(r for r in roles if r != first_item["correct_role"])
        for it in um["phase1_variables"]["items"]:
            role_val = wrong_role if it["id"] == first_item["id"] else it["correct_role"]
            page.locator(f"[data-testid='stage0-select-{it['id']}']").select_option(role_val)
        page.locator("[data-testid='check-btn']").click()
        expect(page.locator("[data-testid='feedback-toast']")).to_be_visible()
        expect(page.locator("[data-testid='stage0-phase-2']")).to_have_attribute("data-phase-state", "locked")
        _retry_click(page)
        for it in um["phase1_variables"]["items"]:
            page.locator(f"[data-testid='stage0-select-{it['id']}']").select_option(it["correct_role"])
        page.locator("[data-testid='check-btn']").click()
        expect(page.locator("[data-testid='stage0-phase-1']")).to_have_attribute("data-phase-state", "completed")
        expect(page.locator("[data-testid='stage0-phase-2']")).to_have_attribute("data-phase-state", "active")
        expect(page.locator("[data-testid='stage0-phase-notice']")).to_be_visible()
        for opt in um["phase2_assumptions"]["options"]:
            if opt["is_required"]:
                page.locator(f"[data-testid='stage0-p2-{opt['id']}']").click()
        page.locator("[data-testid='check-btn']").click()
        expect(page.locator("[data-testid='stage0-phase-2']")).to_have_attribute("data-phase-state", "completed")
        expect(page.locator("[data-testid='stage0-phase-3']")).to_have_attribute("data-phase-state", "active")
        p3_corr = next(o for o in um["phase3_formulation"]["options"] if o["is_correct"])
        page.locator(f"[data-testid='stage0-p3-{p3_corr['id']}']").click()
        page.locator("[data-testid='check-btn']").click()
        expect(page.locator("[data-testid='good-work-toast']")).to_be_visible()

        # 7. invariant_canvas cartesian (Hab-05): check disabled until interacted, wrong value -> error, target kink coords -> pass
        q_cart = by_comp["Hab-05"]
        target_pt = q_cart["invariant_canvas"]["target_state"]["points"]["pt_kink"]
        _open_course_from_library(page, vite_server_url, proj_course["title"])
        _launch_competency_practice(page, "Hab-05")
        expect(page.locator("[data-testid='blank-first-curtain']")).to_have_count(0)
        expect(page.locator("[data-testid='check-btn']")).to_be_disabled()
        page.locator("[data-testid='canvas-pt-pt_kink-x']").fill("0")
        page.locator("[data-testid='canvas-pt-pt_kink-y']").fill("0")
        expect(page.locator("[data-testid='check-btn']")).to_be_enabled()
        page.locator("[data-testid='check-btn']").click()
        expect(page.locator("[data-testid='feedback-toast']")).to_be_visible()
        _retry_click(page)
        page.locator("[data-testid='canvas-pt-pt_kink-x']").fill(str(target_pt["x"]))
        page.locator("[data-testid='canvas-pt-pt_kink-y']").fill(str(target_pt["y"]))
        page.locator("[data-testid='check-btn']").click()
        expect(page.locator("[data-testid='good-work-toast']")).to_be_visible()

        # 8. invariant_canvas tree (C-03): check disabled until interacted, wrong edge -> error, required edges + info_set -> pass
        q_tree = by_comp["C-03"]
        ti = q_tree["invariant_canvas"]["tree_invariants"]
        edges_tree = q_tree["invariant_canvas"].get("edges") or []
        req_edge_set = set(ti["required_edges"])
        wrong_edge = next((e["id"] for e in edges_tree if e["id"] not in req_edge_set), None)
        _open_course_from_library(page, vite_server_url, proj_course["title"])
        _launch_competency_practice(page, "C-03")
        expect(page.locator("[data-testid='blank-first-curtain']")).to_have_count(0)
        expect(page.locator("[data-testid='check-btn']")).to_be_disabled()
        if wrong_edge:
            page.locator(f"[data-testid='tree-edge-btn-{wrong_edge}']").click()
        else:
            page.locator(f"[data-testid='tree-edge-btn-{ti['required_edges'][0]}']").click()
        expect(page.locator("[data-testid='check-btn']")).to_be_enabled()
        page.locator("[data-testid='check-btn']").click()
        expect(page.locator("[data-testid='feedback-toast']")).to_be_visible()
        _retry_click(page)
        if wrong_edge:
            page.locator(f"[data-testid='tree-edge-btn-{wrong_edge}']").click()
            for eid in ti["required_edges"]:
                page.locator(f"[data-testid='tree-edge-btn-{eid}']").click()
        for grp in ti["required_info_sets"]:
            for nid in grp:
                page.locator(f"[data-testid='tree-node-toggle-{nid}']").click()
            page.locator("[data-testid='tree-create-infoset-btn']").click()
        page.locator("[data-testid='check-btn']").click()
        expect(page.locator("[data-testid='good-work-toast']")).to_be_visible()

        # 9. concept_matching (C-04): curtain shown, <option> has no raw $ or \, KaTeX assigned badge renders, distractor -> error, exact pairs -> pass
        q_cm = by_comp["C-04"]
        cm = q_cm["concept_matching"]
        _open_course_from_library(page, vite_server_url, proj_course["title"])
        _launch_competency_practice(page, "C-04")
        expect(page.locator("[data-testid='blank-first-curtain']")).to_be_visible()
        page.locator("[data-testid='lift-curtain-btn']").click()
        expect(page.locator("[data-testid='concept-matching-root']")).to_be_visible()
        first_select = page.locator(f"[data-testid='matching-select-{cm['premises'][0]['id']}']")
        option_texts = first_select.locator("option").all_inner_texts()
        for opt_txt in option_texts:
            assert "$" not in opt_txt and "\\" not in opt_txt, f"Raw LaTeX leaked in <option>: {opt_txt}"
        dist_target_id = next(t["id"] for t in cm["targets"] if t.get("is_distractor"))
        for idx, pr in enumerate(cm["premises"]):
            tid = dist_target_id if idx == 0 else cm["correct_pairs"][pr["id"]]
            page.locator(f"[data-testid='matching-select-{pr['id']}']").select_option(tid)
        expect(page.locator(f"[data-testid='matching-assigned-{cm['premises'][0]['id']}']")).to_be_visible()
        page.locator("[data-testid='check-btn']").click()
        expect(page.locator("[data-testid='feedback-toast']")).to_be_visible()
        _retry_click(page)
        for pr in cm["premises"]:
            page.locator(f"[data-testid='matching-select-{pr['id']}']").select_option(cm["correct_pairs"][pr["id"]])
        page.locator("[data-testid='check-btn']").click()
        expect(page.locator("[data-testid='good-work-toast']")).to_be_visible()

        assert not console_errors, f"Console errors during modality flow: {console_errors}"
        assert not page_errors, f"Page errors during modality flow: {page_errors}"
    finally:
        context.close()


@pytest.mark.parametrize("width,height", [(1280, 800), (640, 720)])
def test_m20_viewport_no_horizontal_overflow(m20_browser, vite_server_url, width: int, height: int):
    """Ensures zero horizontal overflow on 1280x800 and 640x720 viewports across M20 widgets."""
    base_course = _load_compiled_canonical_course()
    proj_course, _ = _build_deterministic_e2e_projection(base_course)
    context, page, console_errors, page_errors = _new_tracked_page(
        m20_browser, proj_course, course_id="m20_e2e_projection", width=width, height=height
    )
    try:
        widgets = [
            ("Hab-01", False, "[data-testid='symbolic-input-root']"),
            ("C-01", True, "[data-testid='proof-dag-root']"),
            ("Hab-03", False, "[data-testid='adversarial-arena-root']"),
            ("Hab-04", False, "[data-testid='stage0-modeler-root']"),
            ("Hab-05", False, "[data-testid='invariant-canvas-root']"),
            ("C-03", False, "[data-testid='invariant-canvas-root']"),
            ("C-04", True, "[data-testid='concept-matching-root']"),
        ]
        for cid, has_curtain, root_sel in widgets:
            _open_course_from_library(page, vite_server_url, proj_course["title"])
            _launch_competency_practice(page, cid)
            if has_curtain:
                curtain = page.locator("[data-testid='lift-curtain-btn']")
                if curtain.is_visible():
                    curtain.click()
            expect(page.locator(root_sel)).to_be_visible(timeout=10000)
            metrics = page.evaluate(
                "() => ({ sw: document.documentElement.scrollWidth, iw: window.innerWidth })"
            )
            assert metrics["sw"] <= metrics["iw"] + 1, (
                f"Horizontal overflow in {cid} at {width}x{height}: scrollWidth={metrics['sw']} > innerWidth={metrics['iw']}"
            )
        assert not console_errors, f"Console errors at {width}x{height}: {console_errors}"
        assert not page_errors, f"Page errors at {width}x{height}: {page_errors}"
    finally:
        context.close()


def test_iron_exam_replaces_course_challenge_with_metacognitive_audit(m20_browser, vite_server_url):
    """Modo Hierro replaces Course Challenge as single integrative exam, hides aids, and persists 80/20 mastery."""
    base_course = _load_compiled_canonical_course()
    proj_course, by_comp = _build_deterministic_e2e_projection(base_course)

    context, page, console_errors, page_errors = _new_tracked_page(
        m20_browser, proj_course, course_id="m20_e2e_projection", width=1280, height=800
    )
    try:
        _open_course_from_library(page, vite_server_url, proj_course["title"])

        # Single exam entry card labeled Modo Hierro
        card = page.locator("[data-testid='course-challenge-card']")
        expect(card).to_have_count(1)
        expect(card).to_contain_text("MODO HIERRO")
        card.locator("button").first.click()

        start_btn = page.locator("[data-testid='start-challenge-btn']")
        expect(start_btn).to_be_visible(timeout=10000)
        expect(page.locator("[data-testid='iron-briefing-card']")).to_be_visible()
        start_btn.click()

        expect(page.locator("[data-testid='iron-exam-session']")).to_be_visible(timeout=10000)
        expect(page.locator("[data-testid='iron-timer']")).to_be_visible()
        # Closed-book exam must not expose hints, curtain, immediate feedback, or Socratic tutor
        expect(page.locator("[data-testid='hints-toggle']")).to_have_count(0)
        expect(page.locator("[data-testid='blank-first-curtain']")).to_have_count(0)
        expect(page.locator("[data-testid='feedback-toast']")).to_have_count(0)
        expect(page.locator("[data-testid='socratic-tutor-container']")).to_have_count(0)

        # Find open_symbolic & fill_in_the_blank item indices robustly in shuffled Iron Exam order
        nav_buttons = page.locator("[data-testid^='iron-nav-item-']")
        total_items = nav_buttons.count()
        assert total_items >= 2
        q_os = by_comp["Hab-01"]
        equiv_expr = (q_os["correct_answer"].get("accepted_equivalents") or [q_os["correct_answer"]["value"]])[-1]

        answered_correct_once = False
        answered_wrong_once = False
        for i in range(total_items):
            page.locator(f"[data-testid='iron-nav-item-{i}']").click()
            sym = page.locator("[data-testid='symbolic-input']")
            if sym.count() > 0 and not answered_correct_once:
                sym.first.fill(equiv_expr)
                page.locator("[data-testid='iron-confidence-high']").click()
                page.locator("[data-testid='iron-flag-btn']").click()
                answered_correct_once = True
                continue
            fib = page.locator("[data-testid='fill-blank-input']")
            if fib.count() > 0 and not answered_wrong_once:
                page.locator("[data-testid='iron-confidence-high']").click()
                fib.first.fill("999999")  # deliberately wrong with high confidence => illusion of competence
                answered_wrong_once = True
            if answered_correct_once and answered_wrong_once:
                break

        # Verify zero horizontal overflow at 1280x800 and 640x720
        for w, h in [(1280, 800), (640, 720)]:
            page.set_viewport_size({"width": w, "height": h})
            m = page.evaluate("() => ({ sw: document.documentElement.scrollWidth, iw: window.innerWidth })")
            assert m["sw"] <= m["iw"] + 2, f"Overflow in IronExam at {w}x{h}: {m}"
        page.set_viewport_size({"width": 1280, "height": 800})

        # Submit -> Metacognitive Modal -> Confirm
        page.locator("[data-testid='iron-submit-exam-btn']").click()
        modal = page.locator("[data-testid='metacognitive-modal']")
        expect(modal).to_be_visible()
        page.locator("[data-testid='meta-global-confidence-high']").click()
        page.locator("[data-testid='metacognitive-confirm-btn']").click()

        # CompletionScreen with Deferred Review & Metacognitive Audit Summary
        expect(page.locator("[data-testid='completion-screen']")).to_be_visible(timeout=10000)
        expect(page.locator("[data-testid='metacognitive-audit-summary']")).to_be_visible()
        expect(page.locator("[data-testid='iron-deferred-review']")).to_be_visible()
        illusions_text = page.locator("[data-testid='meta-illusions-count']").inner_text().strip()
        assert int(illusions_text) >= 1, f"Expected >= 1 illusion of competence, got {illusions_text}"

        # Back to course & verify non-zero 80/20 mastery percentage persists across reload
        page.locator("button:has-text('Back to course')").first.click()
        expect(page.locator("[data-testid='course-challenge-card']")).to_contain_text("11%")
        page.reload()
        page.locator("[data-testid='course-card']").filter(has_text=proj_course["title"]).first.click()
        expect(page.locator("[data-testid='course-challenge-card']")).to_contain_text("11%")
        assert not console_errors, f"Console errors in Iron Exam: {console_errors}"
        assert not page_errors, f"Page errors in Iron Exam: {page_errors}"
    finally:
        context.close()
