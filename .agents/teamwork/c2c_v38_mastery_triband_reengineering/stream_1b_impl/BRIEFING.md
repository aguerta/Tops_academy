# Pre-Flight Briefing — Stream 1B (Fase 1: Implementador)

**Fecha:** 2026-10-31  
**Parent Conversation ID:** `eecd58a3-e3a5-4adc-9cf1-0a5c9a7f5589`  
**Stream Folder:** `d:\Augusto\personal_portfolio\Tops_academy\.agents\teamwork\c2c_v38_mastery_triband_reengineering\stream_1b_impl`  

---

## 1. Archivos en Frontera Exclusiva de Escritura
1. `d:\Augusto\personal_portfolio\Tops_academy\.agents\skills\content-to-course\compile_shard.py`
2. `d:\Augusto\personal_portfolio\Tops_academy\.agents\skills\content-to-course\c2c_hook_guard.py`
3. `d:\Augusto\personal_portfolio\Tops_academy\tests\test_m3_archetypes_semantic_gate.py`
4. `d:\Augusto\personal_portfolio\Tops_academy\tests\test_compile_shard.py`
5. `d:\Augusto\personal_portfolio\Tops_academy\tests\test_shard_compiler_hardening.py`
6. `d:\Augusto\personal_portfolio\Tops_academy\tests\test_shard06_and_dry_archetypes.py`
7. `d:\Augusto\personal_portfolio\Tops_academy\tests\test_invariants_and_shard_overescape_r23.py`
8. `d:\Augusto\personal_portfolio\Tops_academy\tests\test_latex_engine.py`
9. `d:\Augusto\personal_portfolio\Tops_academy\tests\test_hook_post_pass_and_write_isolation.py`
10. `d:\Augusto\personal_portfolio\Tops_academy\tests\test_watchdog_and_hooks.py`
11. `d:\Augusto\personal_portfolio\Tops_academy\.agents\teamwork\c2c_v38_mastery_triband_reengineering\stream_1b_impl\BRIEFING.md`
12. `d:\Augusto\personal_portfolio\Tops_academy\.agents\teamwork\c2c_v38_mastery_triband_reengineering\stream_1b_impl\handoff.md`

---

## 2. Diagnóstico Pre-Flight y Contratos Exactos

### A. `compile_shard.py`
- **Líneas 342–387 (`ShardDataLineLocator._analyze_tuple_node`):**
  - Actualmente detecta heurísticamente si es Form-A o Form-B mirando el índice 2.
  - Se retirará el esquema `Form-A`. La tupla debe corresponder estrictamente al contrato 9-tupla `Form-B`:
    `(tpl_id, cid, qtype, gen_fn, ver_fn, (difficulty, bloom), stems, hints, solution)`.
- **Líneas 1334–1447 (Unpacking de Tuplas en `compile_shard`):**
  - Actualmente soporta tuplas `Form-A` de 9 o 10 elementos mediante rama `else:` (inyectando `KC`, `medium`, `Understand`).
  - Se retira `Form-A`. Se rechaza cualquier tupla que no sea `Form-B` de 9 elementos.
  - El elemento `[5]` (`difficulty_bloom`) debe ser obligatoriamente una 2-tupla/lista `(difficulty, bloom)`:
    `difficulty in {"easy", "medium", "hard"}` y `bloom in {"Remember", "Understand", "Apply", "Analyze", "Evaluate", "Create"}`.
    Strings sueltos o tipos no tupla/lista serán rechazados de forma determinista.
- **Líneas 154–163 y Líneas 1504–1528 (`hints` y `_format_socratic_step`):**
  - Actualmente `_format_socratic_step` sintetiza pistas copiando `wrong_belief` o `omitted_step` desde `cta.json`.
  - Se eliminará `_format_socratic_step` y todo fallback sintético.
  - Se exigirá que el autor provea explícitamente entre 3 y 5 pistas (`3 <= len(hints) <= 5`), cada una con `len(h.strip()) >= 25` caracteres, sin muletillas anti-socráticas (`"Evita el error común"`, `"Recuerda no confundir"`, etc.) ni copias literales de `wrong_belief`.
- **Líneas 505–738 (`build_adapted_mc7_generator`):**
  - Contiene multiplicadores mágicos (`multipliers = [1.333, 0.667, ...]`), generación de `"Opción alterna N"` y asignación posicional `0..5`.
  - Se eliminarán por completo estos fallbacks posicionales y multiplicadores. Todo `distractor_id` debe existir en `cta.json`.
  - En `--strict`:
    - En `MC7`: distractores como 3-tupla `(distractor_id, value, error_rationale)` (o dict equivalente) con `len(error_rationale.strip()) >= 20`.
    - En `MS`: toda opción falsa (`is_correct=False`) debe incluir `distractor_id` válido de `cta.json` y `error_rationale` con `>= 20` chars.
    - **Compuerta `[TPL-DYNAMIC-RATIONALE]`:** Si `vars` no está vacío y el distractor o la plantilla interpola variables paramétricas `@var@`, exigir que `error_rationale` contenga al menos un token `@var@` perteneciente a `vars`. Abortar con `[TPL-DYNAMIC-RATIONALE]` si es 100% estático.
- **Guardia KaTeX para `FIB`:**
  - Rechazar delimitadores `$` externos en `correct`, `value` o `canonical_algebraic` en `fill_in_the_blank` (`FIB`).
- **Extracción de `distractor_ids` en `MS`:**
  - En dry-run para `MS`, extraer `distractor_id` de las opciones falsas y poblar `tpl["distractor_ids"]`.
- **Líneas 741–785 y Líneas 1495–1503 (`generate_rich_stem_variants`):**
  - Se eliminará por completo `generate_rich_stem_variants`.
  - Se exigirá que el autor proporcione `stems` genuinos con `len(stems) >= 3` enunciados distintos por plantilla.
- **Líneas 1652–1837 (`[M3-ARCHETYPES]` Gate y `ver_fn` no trivial):**
  - Cambiar default de `--min-archetypes` a `3`.
  - Inspección AST de `ver_fn`: rechazar verificadores triviales que retornen `True` constante sin inspeccionar argumentos.
  - En `--strict` (con `min_archetypes >= 3`):
    - `>= 3` plantillas por competencia.
    - Cobertura completa de las 3 bandas `{"easy", "medium", "hard"}`.
    - `>= 2` niveles `bloom` distintos.
    - Práctica activa: `>= 2` plantillas `qtype in {"FIB", "MS"}` para `Hab-*` (Skill), y `>= 1` para `C-*` / `H-*` (Concept / Misconception).
  - En `_eval_tuple_output`: incluir huella de `"options"` para `MS` (donde `correct` es `None`), evitando falsas colisiones.

### B. `c2c_hook_guard.py`
- **Líneas 825–836:**
  - Actualizar el mensaje de advertencia / razón de denegación de Rule C mencionando el nuevo contrato `Form-B` Tri-Banda Multimodal (`--min-archetypes 3`, bandas `easy/medium/hard`, `>= 2 Bloom`, `FIB`/`MS` obligatorio y 3-tupla `(did, val, error_rationale_@var@)`).
  - Preservar stdlib pura, `try ... except BaseException:` y `sys.exit(0)`.

### C. Suites de Tests
- Actualizar fixtures en `test_m3_archetypes_semantic_gate.py`, `test_compile_shard.py`, `test_shard_compiler_hardening.py`, `test_shard06_and_dry_archetypes.py`, etc., al contrato `Form-B` Tri-Banda.
- Añadir tests específicos que certifiquen el rechazo de `Form-A`, de `(difficulty)` sin `bloom`, de 2-tupla `(did, val)`, de distractores sin `@var@` en `error_rationale` (`[TPL-DYNAMIC-RATIONALE]`), de `ver_fn` trivial, de `$` externos en `FIB`, y la validación de las 3 bandas y multimodalidad.

---

## 3. Riesgos y Mitigaciones
1. **Regla Zero-Domain:**
   - Riesgo: Introducir palabras prohibidas en minúsculas en `.py` dentro de `.agents/skills/content-to-course/` (`edo`, `pde`, `derivadas`, `jacobiana`, `eigen`, `euler`, `cobb_douglas`, `lotka`, `lagrange`, `regresi`).
   - Mitigación: Escribir comentarios exclusivamente en inglés limpio en `compile_shard.py` y `c2c_hook_guard.py`, evitando palabras en español como "puedo", "quedo", "regresión".
2. **Romper compatibilidad en tests de hardening y circuit breaker:**
   - Mitigación: Los tests de circuit breaker que prueban fallos intencionales (ej. `TEMPLATES = 'broken'`) seguirán fallando por formato de tupla o sintaxis; los tests que esperan `PASS` se migrarán a `Form-B` Tri-Banda con 3 plantillas y 3-tuplas.
3. **Guardias de Hooks:**
   - No ejecutar flags `--help` ni scripts interactivos; ejecutar siempre con `.venv\Scripts\python.exe -m pytest ... -q`.
