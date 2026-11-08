# DISPATCH — Stream 1A (Fase A: Implementador Ortogonal)

- **Parent Conversation ID:** `cbe0c4d9-d376-429c-92b2-ffaeec91ae7f`
- **Stream Folder:** `d:\Augusto\personal_portfolio\Tops_academy\.agents\teamwork\c2c_v40_formal_mas_con_menos\stream_1a_impl`

## Frontera Exclusiva de Escritura (`Exclusive Write Boundary`)
SOLO tienes permiso de escritura sobre:
1. `d:\Augusto\personal_portfolio\Tops_academy\.agents\skills\content-to-course\schemas\cta.schema.json`
2. `d:\Augusto\personal_portfolio\Tops_academy\.agents\skills\content-to-course\compile_cta.py`
3. `d:\Augusto\personal_portfolio\Tops_academy\.agents\skills\content-to-course\cta_merge.py`
4. `d:\Augusto\personal_portfolio\Tops_academy\.agents\skills\content-to-course\check_cta.py`
5. `d:\Augusto\personal_portfolio\Tops_academy\tests\test_cta_mapreduce.py`
6. `d:\Augusto\personal_portfolio\Tops_academy\tests\test_cta_merge_prereq_scoping.py`
7. `d:\Augusto\personal_portfolio\Tops_academy\tests\test_c2c_v321_comp1_cta.py`
8. `d:\Augusto\personal_portfolio\Tops_academy\tests\test_cta_healing.py`
9. `d:\Augusto\personal_portfolio\Tops_academy\tests\test_cta_sweetspot_and_autoheal.py`
10. `d:\Augusto\personal_portfolio\Tops_academy\tests\test_fast_ingest_and_cta_append.py`
11. `d:\Augusto\personal_portfolio\Tops_academy\tests\test_handouts.py`
12. `d:\Augusto\personal_portfolio\Tops_academy\.agents\teamwork\c2c_v40_formal_mas_con_menos\stream_1a_impl\BRIEFING.md` `[NEW]`
13. `d:\Augusto\personal_portfolio\Tops_academy\.agents\teamwork\c2c_v40_formal_mas_con_menos\stream_1a_impl\handoff.md` `[NEW]`

PROHIBIDO tocar cualquier otro archivo.

## Guardias Obligatorias
- **Zero-Domain (`test_skill.py`):** En NINGÚN `.py` de `content-to-course/` pueden aparecer (ni siquiera en comentarios o docstrings) las subcadenas en minúsculas: `edo`, `pde`, `derivadas`, `jacobiana`, `eigen`, `euler`, `cobb_douglas`, `lotka`, `lagrange`, `regresi`. Escribe comentarios/docstrings en `.py` en inglés (cuidado con `puedo`/`quedo` -> `edo`).
- **Windows `cp1252` Safety:** Si usas `pykatex.renderToString`, reemplaza `"\u0332"` por `"^"` en `str(exc)` antes de formatear errores.
- **Pytest sin contención de CPU:** Usa siempre `-o addopts=""` al correr tus 7 suites.

## Especificación Técnica (Fase 1 + Fase 2: Stage 1 CTA Formal, `assumptions`, `cta_fixes/` y DAG Monótono)

1. **Contrato de Supuestos Explícitos (`assumptions` en `schemas/cta.schema.json`, `compile_cta.py` y `check_cta.py`):**
   - Extiende `schemas/cta.schema.json` para que cada competencia acepte opcionalmente `"assumptions"`: array de objetos `{"id": str, "name"?: str, "statement_latex": str, "role_in_proof"?: str, "violation_consequence": str}`.
   - En `compile_cta.py`:
     * Soporta tanto las 6-tuplas existentes `(comp_type, title, desc, bloom, prereqs, distractors)` como **7-tuplas** `(comp_type, title, desc, bloom, prereqs, distractors, assumptions)` y diccionarios con clave `"assumptions"` (aceptando también elementos de `assumptions` como 3-tuplas compactas `(id_or_name, statement_latex, violation_consequence)` o dicts, auto-asignando `id` como `f"A-{cid}-01"` si no empieza por `A-`).
     * Añade parámetro `require_assumptions: bool = False` (y flag CLI `--require-assumptions`, además de activarse si el módulo `cta_data.py` define `CTA_CONTRACT_VERSION = 2`). Cuando `require_assumptions=True` (o `CTA_CONTRACT_VERSION >= 2`), toda competencia de tipo `Skill` o `Concept` debe declarar `>= 1` supuesto válido con `statement_latex` y `violation_consequence` no vacíos (`len >= 10`); si se omite o está vacío, reporta `[CTA-ASSUMPTIONS-MISSING]` mapeado a la línea exacta de esa competencia en `cta_data.py` mediante `CtaDataLineLocator`! (Las llamadas programáticas legacy con `require_assumptions=False` y sin `CTA_CONTRACT_VERSION` siguen pasando con 6-tuplas para preservar el 100% de los tests históricos).
   - En `cta_merge.py`: renderiza los `assumptions` en `cta.md` cuando estén presentes y presérvalos intactos al fusionar partes Map-Reduce o al ejecutar `--append`.

2. **Persistencia 2D (`affected_line_count`, `has_syntax_error`, `error_sha256`), `ModularSplicing` `cta_fixes/<CID>.py` y Recibo `cta.cert.json` (`compile_cta.py`):**
   - Al escribir `.check_attempts/compile_cta*.json` (~`L1691`), incluye siempre:
     * `"affected_line_count"`: entero con el número de líneas fuente distintas reportadas en los errores (`0` si `passed=True`).
     * `"has_syntax_error"`: booleano (`True` si ocurrió `SyntaxError`).
     * `"error_sha256"`: hash SHA-256 hex de las firmas normalizadas ordenadas `rule_tag:line` (`""` si `passed=True`).
   - Implementa `ModularSplicing` en `compile_cta.py`: si existen archivos `work/cta_fixes/<CID>.py` (o `<input_dir>/cta_fixes/<CID>.py` cuando el input vive en `work/`), carga cada módulo `<CID>.py` (que define `COMPETENCY = ...` como tupla o dict para ese `CID` o índice) y reemplaza limpiamente esa competencia antes de validar y exportar `cta.json`.
   - Cuando la compilación final de `cta.json` aprueba (`passed=True`), emite `cta.cert.json` junto a `cta.json` con `{"schema_version": 1, "stage": "cta", "artifact_id": "cta", "source_sha256": <hex>, "cta_sha256": <hex_of_cta_json>, "compiler_sha256": <hex_of_compile_cta_py>, "contract_version": 2, "passed_50_seeds": True, "created_at": <ISO8601>}`.

3. **Saneamiento KaTeX No-Destructivo + Validación `pykatex` (`cta_merge.py` y `compile_cta.py`):**
   - Corrige `auto_wrap_bare_latex_in_cta_field` / `auto_balance_math_delimiters` en `cta_merge.py` para que **jamás** corrompa cadenas parcialmente delimitadas como `r"Sea P(Y \ge $\delta) = 0.95$"` (si una cadena ya contiene delimitadores `$` desbalanceados o comandos LaTeX pegados a `$` internos, repáralos simétricamente solo si el resultado pasa `pykatex.renderToString(span, False)`; si no, NO mutar destructivamente y dejar que `check_cta_katex` reporte la línea exacta con `[CTA-KATEX]`).
   - En `check_cta.py` (`check_cta_katex`), integra validación rápida con `pykatex.renderToString(math_span, is_display)` (importado con fallback seguro si no estuviera disponible, limpiando `\u0332` -> `^` en el mensaje de `pykatex.ParseError`) además de los invariantes existentes, validando también `statement_latex` y `violation_consequence` dentro de `assumptions`.

4. **Certificación Formal del DAG Curricular y Monotonicidad Epistémica $K_t \subseteq K_{t+1}$ (`check_cta.py` y `cta_merge.py`):**
   - En `check_cta.py`: asegura detección determinista de ciclos dirigidos en `prerequisites` reportando la ruta exacta del ciclo (ej. `C-01 -> C-02 -> C-01`) y 100% integridad referencial (cero IDs huérfanos).
   - En `cta_merge.py` (modo `--append` / fusión incremental): garantiza por construcción la **Monotonicidad Epistémica** ($K_t \subseteq K_{t+1}$): ninguna competencia previamente existente en `base_cta` puede ser eliminada ni perder sus `distractors` o `assumptions` previos al hacer append (si hay intento de sobrescritura destructiva, preserva la definición base certificada y solo añade competencias nuevas con IDs disjuntos).

5. **Pruebas Exhaustivas en tus 7 Suites:**
   - Mantén el 100% de los tests existentes pasando y añade casos de prueba positivos y adversarios para:
     * `assumptions` en 7-tuplas/dicts y bloqueo `[CTA-ASSUMPTIONS-MISSING]` con `require_assumptions=True` / `CTA_CONTRACT_VERSION = 2` (mapeando línea exacta).
     * `affected_line_count` (1 regla fallando en >5 líneas reporta `affected_line_count > 5`), `cta_fixes/<CID>.py` splicing y emisión de `cta.cert.json`.
     * KaTeX no-destructivo sobre `r"P(Y \ge $\delta) ...$"` + detección con `pykatex`.
     * Detección de ciclos exactos en DAG y monotonicidad $K_t \subseteq K_{t+1}$ en `--append`.

## Verificación y Entrega
```powershell
& ".venv\Scripts\python.exe" -m pytest -o addopts="" tests/test_cta_mapreduce.py tests/test_cta_merge_prereq_scoping.py tests/test_c2c_v321_comp1_cta.py tests/test_cta_healing.py tests/test_cta_sweetspot_and_autoheal.py tests/test_fast_ingest_and_cta_append.py tests/test_handouts.py -q
```
Escribe `BRIEFING.md` antes de editar, `handoff.md` al terminar, y envía `DONE:: Stream 1A (<N> passed)` a `cbe0c4d9-d376-429c-92b2-ffaeec91ae7f`.
