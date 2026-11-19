# HANDOFF: Iteración Paralela de los 5 Prompts Completos C2C (Pares Improver + Blind Auditor)

> **Proyecto:** `d:\Augusto\personal_portfolio\Tops_academy`
> **Venv Python:** `.\.venv\Scripts\python.exe` (Windows PowerShell)
> **Estado de Promoción:** Las 5 propuestas auditadas hasta R7 ya fueron **promovidas** a los system prompts completos (no lean) en `.agents/skills/content-to-course/system_prompts/prompt_*.md`.
> **Estado del Pipeline `.py` (Fase 2 Milestone 20 + `2 <= M <= 4` + `K = 2` + Anti-Clon COMPLETADA):** Los validadores, compiladores, orquestador y mensajería `.py` ya están alineados en disco con Milestone 20, obligatoriedad `2 <= M <= 4` en `CTA_CONTRACT_VERSION >= 2`, piso `K = 2` (escalable a `K = 3`) por modalidad recomendada, 4 candados deterministas anti-clon (`[TPL-CLONE-AST]`, `[TPL-CLONE-BAND]`, `[TPL-CLONE-STEM]`, `[TPL-CLONE-SYMPY]`) y cuotas dinámicas Stage 4 (`max(30, N*4)` en Skill / `max(20, N*3)` en Concept/Fact) junto con `tests/engine/test_m20_pipeline_alignment.py` y `tests/engine/test_k_per_modality_and_anti_clone.py`. Toda regla nueva descrita abajo **ya está activa en código real**.

---

## 1. Estado Inicial Verificado al Abrir la Nueva Sesión

| Archivo Promovido (No-Lean) | Bytes (`CR=0`) | `audit_prompt.py --pipeline-check` (post-promoción) | Blind Auditor R7 (pre-promoción: conteo exacto y hallazgos) |
|:---|---:|:---:|:---|
| `.agents/skills/content-to-course/system_prompts/prompt_cta_architect.md` | 14,046 B | `0 Alta / 0 Media / 0 Baja` (`4/4`) | **0 Alta / 0 Media / 1 Baja** — Baja (`A2`): etiqueta `Lean v4.2` vs 14,047 B (~3,487–4,359 tok, > `--lean` 500–1,500 tok y docstring `<= 5 KB` en `dispatch.py:103,133`). Sandbox R7: PASS Ex 1 (`part_01` + slice `[1..3]`), Ex 2 (`--append`), Ex 3 (`Negative Knowledge`). *(Post-R7 en promoción: solo se cambió encabezado a `M20 v4.3`; aún sin re-auditoría ciega.)* |
| `.agents/skills/content-to-course/system_prompts/prompt_cta_harmonizer.md` | 10,254 B | `0 Alta / 0 Media / 0 Baja` (`4/4`) | **0 Alta / 0 Media / 1 Baja** — Baja (`A2`): etiqueta `Lean v4.2` vs 10,255 B (~2,550–3,187 tok, > `--lean` 500–1,500 tok y docstring `<= 5 KB` en `dispatch.py:103,133`). Sandbox R7: `SUCCESS` (`rc=0`) en Ex 1 (Multi-PDF), Ex 2 (`2A`/`2B` `--append` `[BASE]`+`drop_ids`), Ex 3 (no-op). *(Post-R7 en promoción: solo encabezado `M20 v4.3`; sin re-auditoría ciega.)* |
| `.agents/skills/content-to-course/system_prompts/prompt_shard_author.md` | 27,801 B | `0 Alta / 0 Media / 0 Baja` (`4/4`) | **0 Alta / 0 Media / 2 Baja** — Baja 1 (`A1`/`I2`): 27,791 B (~6,911–8,638 tok) supera `~12 KB` (`semantic_audit_checklist.md:8`) y omite en el encabezado si sustituye al estándar o al `lean/`; Baja 2 (`I1`): L50 hardcodea `>= 15`, `>= 10`, `>= 0.50` en vez de `<<S4_UNIQ_SKILL>>`, `<<S4_UNIQ_OTHER>>`, `<<S4_RATIO>>`. Sandbox R7: `precheck rc=0`, `compile_shard --strict` 50 sem. `rc=0`, `validate strict=True` `0` err, QA `20.0/20.0 PLATINUM MASTERY`. *(Post-R7 en promoción: solo espaciado `TEMPLATES = [` y `H1 = [..H4 = [` para tests CI; sin re-auditoría ciega.)* |
| `.agents/skills/content-to-course/system_prompts/prompt_repair.md` | 18,281 B | `0 Alta / 0 Media / 0 Baja` (`4/4`) | **0 Alta / 0 Media / 2 Baja** — Baja 1 (`A2`): etiqueta `Lean v4.2` vs 18,282 B (~4,552–5,690 tok, > `--lean` 500–1,500 tok y docstring `<= 5 KB` en `dispatch.py:103,133`); Baja 2 (`I1`): L42–43 hardcodean `>=15` y `>=10` en `<stems>` en vez de `<<S4_UNIQ_SKILL>>`/`<<S4_UNIQ_OTHER>>`. Sandbox R7: AST `OK` (3/3), `S_C3` sin fugas (`inv_ok=True`), Ex 2 `PASS` en `shard_fixes` y standalone (`precheck rc=0`, `compile_shard rc=0`). *(Post-R7 en promoción: solo encabezado `M20 v4.3`; sin re-auditoría ciega.)* |
| `.agents/skills/content-to-course/system_prompts/prompt_blind_judge.md` | 13,950 B | `0 Alta / 0 Media / 0 Baja` (`4/4`) | **0 Alta / 0 Media / 1 Baja** — Baja (`A2`): etiqueta `Lean v4.3` vs 13,953 B (~3,470–4,337 tok, > `--lean` 500–1,500 tok y docstring `<= 5 KB` en `dispatch.py:103,133`). Sandbox R7: SymPy `OK` (13/13), `judge.py` 11/11 válidos `agreement_rate=1.0 passed=True` + 2 `BLOCKED`. *(Post-R7 en promoción: solo encabezado `M20 v4.3`; sin re-auditoría ciega.)* |

> **Nota crítica de honestidad:** Ninguno de los 5 archivos promovidos en `system_prompts/prompt_*.md` ha recibido aún re-auditoría ciega posterior a la promoción. En particular, siguen abiertos para la nueva sesión: los 2 hallazgos `Baja` de `prompt_shard_author.md` (tamaño vs `~12 KB` / falta de rol en encabezado + hardcoding `15`/`10`/`0.50`), el hardcoding `15`/`10` en `prompt_repair.md` y el docstring obsoleto `<= 5 KB` en `dispatch.py:103,133`.

### Alcance y Reglas Inviolables
1. **Solo editar los 5 archivos no-lean** en `.agents/skills/content-to-course/system_prompts/prompt_{cta_architect,cta_harmonizer,shard_author,repair,blind_judge}.md`.
2. **NO tocar** `.agents/skills/content-to-course/system_prompts/lean/*.md`, `.agents/skills/content-to-course/subagent_types.json`, `courses/**`, ni archivos `.py` durante esta sesión de prompts (la Fase 2 `.py` Milestone 20 ya está aplicada en disco).
3. **Sin presupuesto de 13 KB ni `<= 5 KB`:** El usuario eliminó la cuota JSON; estos son los prompts **completos** (`M20 v4.3`). Solo aplica mantener cada archivo por debajo del techo técnico de lectura atómica `read_file` (`< 46,080` B) y compilado `< 75,000` B en `test_system_prompts_shard_author_contract_and_budgets`.
4. **LF puro obligatorio:** `0` bytes `\r` en todos los `.md` editados.
5. **Quick Wins ya identificados al arrancar:**
   - Sustituir `15` / `10` / `0.50` en reglas de stems/diversidad (`prompt_shard_author.md:50`, `prompt_repair.md:42-43`) por `<<S4_UNIQ_SKILL>>`, `<<S4_UNIQ_OTHER>>`, `<<S4_RATIO>>`, ya que `load_system_prompt()` en `dispatch.py:123` llama a `render_contract_tokens()` (`engine/stage_contract.py:91-97`) para inyectarlos en tiempo de ejecución.
   - Confirmar que los prompts reflejen las **validaciones M20 + `2 <= M <= 4` + `K = 2` + Anti-Clon recién activadas en `.py`**: `[CTA-MODALITY-MISSING]`, `[CTA-MODALITY-RANGE]`, `[CTA-MODALITY-INVALID]` (`compile_cta.py` / `check_cta.py`), recorte `<= 4` en `cta_merge.py`, piso `count(m) >= K` (`[CTA-MODALITY-PLAN]`) y 4 candados anti-clon (`[TPL-CLONE-AST]`, `[TPL-CLONE-BAND]`, `[TPL-CLONE-STEM]`, `[TPL-CLONE-SYMPY]` en `compile_shard.py`), `[CANVAS-INVARIANT-KIND]` + `[CANVAS-INEQUALITY]` + `VALID_CANVAS_INVARIANT_KINDS` (`engine/assemble.py` / `engine/invariants.py`), `R-20` en `unstructured_model` e `invariant_canvas` + `R-19` anti-fuga en `point_coords` y `kink_at` (`src/validator/rules.py` / `engine/invariants.py`), y `[TPL-FIB-KATEX]` / `[VER-SIGNATURE]` (`MS`/`M20 estructurado`).

---

## 2. Plancito de Ejecución: 5 Pares Paralelos (Improver + Blind Auditor Nuevo por Prompt)

Para acelerar al máximo sin mezclar contextos ni sesgar al juez:

### Paso 0 — Definir 2 Tipos de Subagente en el Turno 1 (`Model="inherit"`)
Define exactamente dos tipos de subagente mediante `define_subagent`:

1. **`c2c_prompt_improver`** (`EnableWriteTools=True`, `EnableMCPTools=False`, `EnableSubagentTools=False`):
   - **Rol:** Edita exclusivamente el archivo `.agents/skills/content-to-course/system_prompts/prompt_<role>.md` asignado (preservando `\n` puro / `CR=0` y respetando los literales exigidos por tests si aplica).
   - **Reglas:** Lee únicamente los archivos autorizados en su Manifiesto de Par. Ejecuta `audit_prompt.py --pipeline-check` sobre su prompt y ejecuta todos los ejemplos few-shot de su propio prompt dentro de `tempfile.TemporaryDirectory()` con `.\.venv\Scripts\python.exe`.
   - **Scope:** Prohibido leer/modificar otros prompts, `lean/`, `subagent_types.json`, `courses/` o `.py` del repo.

2. **`c2c_prompt_blind_auditor`** (`EnableWriteTools=True`, `EnableMCPTools=False`, `EnableSubagentTools=False`):
   - **System Prompt Base:** Usar literalmente `.agents/skills/prompt-architect/references/semantic_auditor_subagent.md` más la regla obligatoria de **ejecución real en sandbox** (`tempfile.TemporaryDirectory()`) y **STRICT READ-ONLY WORKSPACE** (jamás crear, editar o borrar archivos en el repositorio ni en `brain/*/scratch`).
   - **Regla de Ceguera Total:** JAMÁS pasarle al auditor puntajes/reportes de `audit_prompt.py`, ediciones hechas por el Improver, ni hallazgos de rondas previas. Solo recibe: (a) ruta exacta de **su único prompt**, (b) regla de arquitectura vigente (Milestone 20 + autonomía CTA vía `recommended_modalities`, prompts completos `M20 v4.3` sin restricción `--lean` de 500–1,500 tok ni `<= 5 KB`), y (c) su Manifiesto exacto de lectura + pruebas sandbox.

### Paso 1 — Ola 1: Lanzar 5 Blind Auditors Nuevos en Paralelo
Invocar simultáneamente 5 subagentes `c2c_prompt_blind_auditor` (`Model="inherit"`, uno por archivo):
- `Auditor-R1 CTA Architect` -> `prompt_cta_architect.md`
- `Auditor-R1 CTA Harmonizer` -> `prompt_cta_harmonizer.md`
- `Auditor-R1 Shard Author` -> `prompt_shard_author.md`
- `Auditor-R1 Repair` -> `prompt_repair.md`
- `Auditor-R1 Blind Judge` -> `prompt_blind_judge.md`
Terminar el turno sin hacer polling y esperar las 5 respuestas.

### Paso 2 — Ola 2: Lanzar Improvers Dedicados en Paralelo (Solo Prompts con `> 0` Hallazgos)
- Todo prompt cuyo Blind Auditor devuelva **`0 Alta / 0 Media / 0 Baja` + 100% ejemplos PASS en sandbox** queda **SELLADO (DONE)**.
- Para cada prompt con algún hallazgo (`Alta`, `Media` o `Baja`) o fallo de ejecución, instanciar un subagente **`c2c_prompt_improver` NUEVO** en paralelo (`Model="inherit"`).
- Darle al Improver: los hallazgos exactos de **su propio auditor**, su Manifiesto de Lectura (compartido + par) y exigirle al terminar: `CR=0`, `audit_prompt.py --pipeline-check` en `0/0/0` + `4/4`, y 100% ejemplos pasando en sandbox.

### Paso 3 — Ola 3+: Blind Auditor Completamente Nuevo por Cada Prompt Editado
- Por cada prompt modificado en el Paso 2, instanciar un **`c2c_prompt_blind_auditor` COMPLETAMENTE NUEVO** en paralelo (`invoke_subagent` fresco; **prohibido reutilizar la conversación del auditor anterior** ni enviarle qué cambió el Improver).
- Repetir Pasos 2 y 3 **únicamente sobre los prompts que aún no estén en `0/0/0`** hasta que los 5 alcancen simultáneamente **`0 Alta / 0 Media / 0 Baja`** y ejecución sandbox verde.

### Paso 4 — Cierre de Verificación de Prompts y Validación M20 Integral
Con los 5 prompts en `0/0/0`, ejecutar en el coordinador:
```powershell
.\.venv\Scripts\python.exe ".agents/skills/prompt-architect/scripts/audit_prompt.py" --path ".agents/skills/content-to-course/system_prompts/prompt_cta_architect.md" ".agents/skills/content-to-course/system_prompts/prompt_cta_harmonizer.md" ".agents/skills/content-to-course/system_prompts/prompt_shard_author.md" ".agents/skills/content-to-course/system_prompts/prompt_repair.md" ".agents/skills/content-to-course/system_prompts/prompt_blind_judge.md" --pipeline-check --format markdown
.\.venv\Scripts\python.exe -m pytest tests/engine/test_m20_pipeline_alignment.py tests/pipeline/test_pipeline_reparations.py tests/quality/test_ab30_remediations.py -k "test_m20_pipeline_alignment or test_prompt_shard_author_file or test_system_prompts_shard_author_contract_and_budgets" -q
.\.venv\Scripts\python.exe -c "import pathlib; d=pathlib.Path('.agents/skills/content-to-course/system_prompts'); [print(p.name, p.stat().st_size, 'CR=', p.read_bytes().count(b'\x0d')) for p in sorted(d.glob('prompt_*.md')) if p.name in {'prompt_cta_architect.md','prompt_cta_harmonizer.md','prompt_shard_author.md','prompt_repair.md','prompt_blind_judge.md'}]"
```
La Fase 2 de alineamiento `.py` Milestone 20 ya está aplicada en el repositorio; tras cerrar todos los prompts en `0/0/0`, corre también la batería completa de verificación descrita en [HANDOFF.md](file:///d:/Augusto/personal_portfolio/Tops_academy/HANDOFF.md) (y consulta al usuario antes de sincronizar `system_prompts/lean/*.md` y `subagent_types.json`).

---

## 3. Manifiesto Exacto Compartido: Archivos de Prompt Engineering (Obligatorio para Todos)

### Leer (todos los Improvers y todos los Blind Auditors)
- `.agents/skills/prompt-architect/references/semantic_audit_checklist.md` (criterios `A1`–`I3`; recuerda al auditor que estos 5 archivos son **prompts completos `M20 v4.3`**, NO variantes micro `--lean` 500–1,500 tok)
- `.agents/skills/prompt-architect/references/audit_rubric.md` (severidades `Alta` / `Media` / `Baja`)
- `.agents/skills/prompt-architect/references/gemini_prompting_guide_2026.md` (directrices Frontier Gemini 4 / Nov 2026)
- `.agents/skills/prompt-architect/references/agentic_workflows_guide.md` (control agéntico, append-only, anti-reflection, tools)
- *Solo para el Improver como CLI caja negra (NO leer su código fuente ni compartir salida al auditor):*
  `.\.venv\Scripts\python.exe .agents/skills/prompt-architect/scripts/audit_prompt.py --path <su_prompt> --pipeline-check --format markdown`

### Prohibido Leer para Todos (No gastar contexto innecesario)
- `.agents/skills/prompt-architect/SKILL.md`, `.agents/skills/prompt-architect/tests/**`, `.agents/skills/prompt-architect/references/agentic_si_template_original.md`, `.agents/skills/prompt-architect/references/iteration_and_decomposition.md`, `.agents/skills/prompt-architect/templates/**`
- `courses/**`, `content/**`, `reports/**`, `.agents/teamwork/**`, `platform/src/components/**`
- `.agents/skills/content-to-course/system_prompts/lean/**`, `subagent_types.json`, `HANDOFF*.md`
- Todo `.py` que no pertenezca explícitamente al par asignado abajo.

---

## 4. Manifiesto Exacto por Par (Qué Leer, Qué NO Leer y Qué Ejecutar)

> Rutas relativas a `d:\Augusto\personal_portfolio\Tops_academy\`. Cuando se listan rangos de líneas, leer **solo esos bloques** (archivos grandes como `compile_shard.py` o `check_templates.py` miden > 200 KB).

### Par 1 — `prompt_cta_architect.md`
- **Leer:**
  1. `.agents/skills/content-to-course/system_prompts/prompt_cta_architect.md` (completo)
  2. `.agents/skills/content-to-course/schemas/cta.schema.json` (completo, 5.5 KB)
  3. `.agents/skills/content-to-course/compile_cta.py`: `L690-725` (`cta_fixes` `candidate_dirs`), `L1140-1230` (`_MODALITY_ALIASES`, `_CANONICAL_MODALITIES`, `_normalize_recommended_modalities` con rechazo `ValueError("[CTA-MODALITY-INVALID] ...")`, `CTA_CONTRACT_VERSION`), `L1470-1565` (`L1537 cid=raw_id`, `recommended_modalities`, tupla `10..11`), `L2000-2025` (`require_assumptions`)
  4. `.agents/skills/content-to-course/check_cta.py`: `L310-355` (`CTA-D1`, DAG `max_roots`), `L705-885` (`_VALID_RECOMMENDED_MODALITIES` 9 modalidades canónicas, validación `[CTA-MODALITY-INVALID]` en `L800-816`, reglas `distractors`, `assumptions`, `description_latex`, `remediation_hint`)
  5. `.agents/skills/content-to-course/dispatch.py`: `L100-145`, `L195-270`, `L355-385`, `L930-1010` (`ROLE_SPECS["cta"|"cta-direct"|"cta-map"]`, pointer prompt y `Doc:` slice)
  6. `.agents/skills/content-to-course/c2c_hook_guard.py`: `L225-275`, `L1395-1420`, `L1775-1830` (Matriz 2D `cta`)
  7. `.agents/skills/content-to-course/prepare.py`: `L115-145`, `L280-325` (`next_ids_by_prefix`) y `.agents/skills/content-to-course/ingest.py`: `L330-355` (`files[*].doc`, `valid_page_range`)
- **NO leer:** `compile_shard.py`, `check_templates.py`, `cta_merge.py`, `judge.py`, `engine/*`, `src/validator/*`, `platform/*`, `plan_shards.py`, `run.py`, `course_publisher.py`, `shard_precheck.py`.
- **Nota de contrato vigente:** Confirmar que `recommended_modalities` sea obligatorio (`2 <= M <= 4` en `CTA_CONTRACT_VERSION >= 2`, `[CTA-MODALITY-MISSING]` / `[CTA-MODALITY-RANGE]`), documentando únicamente las 9 modalidades canónicas aceptadas (más shorthands `MC7`, `MS`, `FIB`) y `[CTA-MODALITY-INVALID]` ante alias o tipos desconocidos.
- **Ejecución Sandbox (`tempfile.TemporaryDirectory()`):**
  - Extraer los bloques Python de Ejemplo 1 (`part_01` completo + variante slice `valid_page_range`), Ejemplo 2 (`cta_data.py` modo `--append` con `existing_competency_ids=["C-01"]` + `cta_merge.parse_next_ids_by_prefix`), y Ejemplo 3 (`part_02`, *Negative Knowledge*). Compilar todos con `compile_cta.py` + `check_cta.py` -> exigir `rc=0` y `warnings=[]`.

---

### Par 2 — `prompt_cta_harmonizer.md`
- **Leer:**
  1. `.agents/skills/content-to-course/system_prompts/prompt_cta_harmonizer.md` (completo)
  2. `.agents/skills/content-to-course/cta_merge.py`: `L70-95` (`MAX_DISTRACTORS_PER_COMPETENCY`, `DISTRACTOR_DEDUP_JACCARD_THRESHOLD`), `L1145-1185` (`[BASE]`, `read_only_base`), `L1780-1825` (`apply_harmonize`), `L1885-2385` (orden `#1 rename`, `#2 drop_duplicate_distractors`, `#3 merge`, Caso A `[BASE]` inmutable vs Caso B unión `recommended_modalities`, `drop_ids`, `keep_separate`)
  3. `.agents/skills/content-to-course/dispatch.py`: `L380-415`, `L650-710` (`generate_define_subagent_specs` -> `c2c_cta_harmonizer.json`), `L1220-1340` (`dispatch_cta_reduce`, prohibido leer `cta_reduce_01.json`)
  4. `.agents/skills/content-to-course/check_cta.py`: `L310-355` (`root_ratio <= max(1, floor(0.20 * n))`, DAG conexo), `L705-725`, `L800-816` (`_VALID_RECOMMENDED_MODALITIES` y `[CTA-MODALITY-INVALID]` para validar que las fusiones preserven modalidades canónicas)
  5. `.agents/skills/content-to-course/schemas/cta.schema.json` (completo)
- **NO leer:** `compile_cta.py`, `compile_shard.py`, `check_templates.py`, `judge.py`, `engine/*`, `c2c_hook_guard.py`, `src/validator/*`, `platform/*`, `plan_shards.py`, `run.py`, `course_publisher.py`, `shard_precheck.py`, `prepare.py`, `ingest.py`.
- **Ejecución Sandbox (`tempfile.TemporaryDirectory()`):**
  - Extraer los 3 payloads JSON de ejemplos (Ex 1 Multi-PDF `merge` + `keep_separate` + `add_prerequisites` + `rename` + `drop_duplicate_distractors`, Ex 2 `--append` hacia `[BASE]` con `drop_ids`, Ex 3 no-op `[]`) y ejecutarlos contra `cta_merge.py apply --work <tmp>` sobre fixtures compatibles -> exigir `rc=0` y `SUCCESS` en todos.

---

### Par 3 — `prompt_shard_author.md`
- **Leer:**
  1. `.agents/skills/content-to-course/system_prompts/prompt_shard_author.md` (completo)
  2. `.agents/skills/content-to-course/shard_precheck.py` (completo, 161 líneas — incl. `L125 [VER-SIGNATURE]` `(MC/FIB/open_symbolic)` vs `(MS/M20 estructurado)`)
  3. `.agents/skills/content-to-course/engine/stage_contract.py` (completo — tokens `<<S4_*>>`, `<<S4_TPL_PER_MOD>>`, `<<S4_MIN_MODS>>`, `<<S4_MAX_MODS>>`, cuotas dinámicas `max(30, N*4)` / `max(20, N*3)`)
  4. `.agents/skills/content-to-course/compile_shard.py`: `L55-100`, `L1870-1895`, `L2215-2250` (`shard_fixes/`), `L2755-2785` (Form-C), `L3275-3365` (`[TPL-FIB-KATEX]`, `[TPL-ORPHAN-VARS]`), `L3475-3520` (`[TPL-DYNAMIC-RATIONALE]`), `L3800-3850` (5 mutaciones `MS`), `L3920-3940` (`sol >= 60c`), `L4980-5080` (`[CTA-MODALITY-PLAN]` piso `K` por modalidad + `_check_intra_competency_anti_clone` 4 candados)
  5. `.agents/skills/content-to-course/check_templates.py`: `L1300-1350` (`[KATEX-TEXT-PROSE]` `<= 2 pal / <= 20c`), `L2750-2815` (diversidad M20 en `invariant_canvas` con `inequality`, `geometry` y `target_state`), `L3375-3445` (`TPL-STATIC-OPT`, claves únicas), `L3700-3720` (`<= 20%`)
  6. `.agents/skills/content-to-course/engine/assemble.py`: `L20-25`, `L979-1210` (`_coerce_num_if_numeric`, `_assemble_invariant_canvas`, `[CANVAS-INVARIANT-KIND]`, `[CANVAS-INEQUALITY]` validando `curve_id` en curvas declaradas y estilos/sombras, interpolación + coerción recursiva en `target_state`), `L1530-1705` (despacho 6 modalidades M20)
  7. `.agents/skills/content-to-course/engine/invariants.py`: `L115-135` (`VALID_CANVAS_INVARIANT_KINDS`), `L885-915` (`[KATEX-PROSE-OVERFLOW] <= 45c`), `L1414-1600` (KaTeX en `unstructured_model` e `invariant_canvas` cartesian/tree, `[CANVAS-INVARIANT-KIND]`, `[CANVAS-INEQUALITY]` y anti-fuga en `point_coords` + `kink_at` excluyendo `fixed_points`)
  8. `src/validator/rules.py`: `L270-300`, `L1375-1566` (paridad `R-20` en `unstructured_model`/`invariant_canvas` y `R-19` anti-fuga en `point_coords`/`kink_at`)
  9. `.agents/skills/content-to-course/dispatch.py`: `L100-145` (`render_contract_tokens`), `L265-298`, `L1715-1835` (`C2C_INLINE_AUTHOR_ORDER=1`, reglas Turn-0)
  10. `.agents/skills/content-to-course/c2c_hook_guard.py`: `L225-275`, `L1465-1490`, `L1765-1890` (`L1813` modalidades CTA, Matriz 2D `shard`, `Test-Path`/`Get-ChildItem`)
  11. `platform/src/types.ts`: `L160-440` (interfaces TypeScript exactas M20)
- **NO leer:** `compile_cta.py`, `check_cta.py`, `cta_merge.py`, `judge.py`, `prepare.py`, `ingest.py`, `partition_corpus.py`, `course_publisher.py`, `run.py`, `src/validator/core.py`, `platform/src/components/**`.
- **Invariante CI (solo Improver):** Preservar los literales `"compile_shard.py"`, `"TEMPLATES = ["`, `"H1 = ["`, `"H2 = ["`, `"H3 = ["`, `"H4 = ["`, `"pre_shard_manifest.json"`, `"BLOCKED:"`, `"edit_file"` y tamaño compilado `< 75,000` B (`test_pipeline_reparations.py:360`, `test_ab30_remediations.py:757`).
- **Ejecución Sandbox (`tempfile.TemporaryDirectory()`):**
  - Extraer ambos bloques Python (Ex 1 `Hab-01` clásico `M=3, K=2 => 6` y Ex 2 `C-02` M20 `M=2, K=2 => 4`); correr `shard_precheck.precheck_source`, `compile_shard.py --strict --min-archetypes 4 --templates-per-modality 2 --fail-total` (50 semillas dry-run -> exigir `rc=0` y **0 warnings**), `instantiate_competency` + `check_instance_invariants` / `validate_course_content(..., strict=True)` (`0` errores en las nuevas reglas `R-20`/`R-19`, `[CANVAS-INVARIANT-KIND]`/`[CANVAS-INEQUALITY]` y los 4 candados anti-clon) y `standardized_audit_engine.run_full_audit` (`20.0/20.0`).

---

### Par 4 — `prompt_repair.md`
- **Leer:**
  1. `.agents/skills/content-to-course/system_prompts/prompt_repair.md` (completo)
  2. `.agents/skills/content-to-course/shard_precheck.py` (completo, 161 líneas — incl. `L125 [VER-SIGNATURE]`)
  3. `.agents/skills/content-to-course/engine/stage_contract.py` (completo, 112 líneas — tokens `<<S4_*>>`)
  4. `.agents/skills/content-to-course/dispatch.py`: `L100-145`, `L325-356` (`turn_budget=15`), `L540-560` (`_locate_competency_line_range`), `L2870-2925`, `L3055-3180` (`repair_<cid_norm>_data.md`, `repair_<shard_id>_data.md`, `repair_slices/` con `recommended_modalities`)
  5. `.agents/skills/content-to-course/c2c_hook_guard.py`: `L225-275`, `L1395-1435` (`[REPAIR-NO-FULL-CTA]`), `L1765-1835` (`L1813` modalidades CTA, Matriz 2D `<40`/`>=40`/`450`/`250`)
  6. `.agents/skills/content-to-course/compile_shard.py`: `L1870-1895`, `L2215-2235`, `L2445-2460` (`shard_fixes/`), `L3275-3365` (`[TPL-FIB-KATEX]`), `L3475-3520`, `L3800-3850`, `L4190-4240`
  7. `.agents/skills/content-to-course/check_templates.py`: `L1300-1350`, `L2750-2815` (diversidad M20 en `invariant_canvas`), `L3375-3445`
  8. `.agents/skills/content-to-course/engine/assemble.py`: `L979-1210` (`[CANVAS-INVARIANT-KIND]`, `[CANVAS-INEQUALITY]`, interpolación recursiva de `target_state`)
  9. `.agents/skills/content-to-course/engine/invariants.py`: `L115-135` (`VALID_CANVAS_INVARIANT_KINDS`), `L885-915`, `L1414-1600` (KaTeX `unstructured_model`/`invariant_canvas`, anti-fuga `point_coords` y `kink_at`)
  10. `src/validator/rules.py`: `L1375-1566` (`R-20` en `unstructured_model`/`invariant_canvas`, `R-19` en `point_coords`/`kink_at`) y `.agents/skills/content-to-course/plan_shards.py:L143` (`[TPL-FIB-KATEX]`)
  11. `platform/src/types.ts`: `L160-440`
- **NO leer:** `compile_cta.py`, `check_cta.py`, `cta_merge.py`, `judge.py`, `prepare.py`, `ingest.py`, `course_publisher.py`, `run.py`, `platform/src/components/**`.
- **Nota para Improver/Auditor de Par 4:** Verificar que la Matriz de Diagnósticos / `<contracts>` cubra los fallos reparables recién activados (`[CTA-MODALITY-PLAN]` piso `K` por modalidad, `[TPL-CLONE-AST]`, `[TPL-CLONE-BAND]`, `[TPL-CLONE-STEM]`, `[TPL-CLONE-SYMPY]`, `[CANVAS-INVARIANT-KIND]`, `[CANVAS-INEQUALITY]`, `R-20` en `unstructured_model`/`invariant_canvas`, `R-19` en `point_coords` y `kink_at`, `[TPL-FIB-KATEX]` y `[VER-SIGNATURE]`).
- **Ejecución Sandbox (`tempfile.TemporaryDirectory()`):**
  - `ast.parse` + `shard_precheck.precheck_source` sobre los 3 bloques Python; instanciar `S_C3` (Ex 3) y comprobar `validate_katex_syntax` + `check_instance_invariants(..., "invariant_canvas")` (`0` fugas `(target_x, target_y)`); compilar Ex 2 (`C-02`, `M=2, K=2 => 2 FIB + 2 MS`, 4 arquetipos) vía `shard_fixes/shard_01/C-02.py` **y** standalone `shard_01_data.py` con `compile_shard.py --strict --min-archetypes 4 --templates-per-modality 2 --fail-total` (50 semillas -> `rc=0`, `0` warnings).

---

### Par 5 — `prompt_blind_judge.md`
- **Leer:**
  1. `.agents/skills/content-to-course/system_prompts/prompt_blind_judge.md` (completo)
  2. `.agents/skills/content-to-course/judge.py`: `L40-70` (`_build_mc7_judge_contract`), `L273-415` (`_sanitize_m20_judge_item`), `L745-770`, `L1035-1095` (`check_judge_completeness`), `L1170-1295` (`emit_judge_redispatch`), `L1370-1580` (`_check_single_answer_match`, `_check_m20_answer_match`), `L1581-1700` (`resolve_neuro_symbolic_verdict`), `L1740-2085` (`compare_judge_responses` y `BLOCKED` campos)
  3. `.agents/skills/content-to-course/dispatch.py`: `L295-325` (`ROLE_SPECS["judge"]`, `enable_subagent_tools=False`), `L2090-2205` (`dispatch_judges`, Modo Inline vs Pointer)
  4. `platform/src/types.ts`: `L119-440` (`QuestionOption`, `ProofDagSpec`, `AdversarialBreakSpec`, `UnstructuredModelSpec`, `TreeInvariantsSpec`, `InvariantCanvasSpec`, `ConceptMatchingSpec`)
  5. *(Opcional acotado)* `.agents/skills/content-to-course/engine/invariants.py`: `L115-130` (`VALID_CANVAS_INVARIANT_KINDS`) y `L1570-1595` (`giveaway` en `invariant_canvas` aplica tanto a `point_coords` como a `kink_at`).
- **NO leer:** `compile_cta.py`, `check_cta.py`, `cta_merge.py`, `compile_shard.py`, `check_templates.py`, `shard_precheck.py`, `c2c_hook_guard.py`, `src/validator/*`, `course_publisher.py`, `run.py`, `platform/src/components/**`.
- **Ejecución Sandbox (`tempfile.TemporaryDirectory()` o inline Python `.\.venv\Scripts\python.exe -`):**
  - Parsear los 4 JSON de salida (`item_01`..`item_13`), comprobar matemáticamente cada respuesta con `sympy`/`fractions`, validar `_sanitize_m20_judge_item` en los 7 ítems M20, `_validate_ground_truth_item` + `_check_single_answer_match` en los 11 ítems válidos (`11/11 match=True`), contrato `MC7`, `compare_judge_responses` (`agreement_rate=1.0`, `passed=True`) y los 2 `BLOCKED` (`item_05` `epistemic_insufficiency`, `item_06` `giveaway`).
