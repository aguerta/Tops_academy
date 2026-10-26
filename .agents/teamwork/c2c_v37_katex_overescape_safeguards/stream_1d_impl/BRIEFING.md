# BRIEFING — Stream 1D (Fase 1: Implementador)

**Fecha:** 2026-10-25  
**Stream:** `stream_1d_impl`  
**Frontera Exclusiva de Escritura:**
- `run_platform.py`
- `FUTURE_MILESTONES.md`
- `docs/future_milestones/FUTURE_MILESTONES.md`
- `tests/test_platform_katex_admission_guard.py`
- `.agents/teamwork/c2c_v37_katex_overescape_safeguards/stream_1d_impl/BRIEFING.md`
- `.agents/teamwork/c2c_v37_katex_overescape_safeguards/stream_1d_impl/handoff.md`

---

## 1. Hallazgos del Pre-Flight Sanity Check

1. **`run_platform.py`:**
   - Actualmente contiene `validate_platform_course` con Pass 1 (chequeo léxico de caracteres de control ASCII `< 32`), Pass 2 (JSON syntax), Pass 3 (metadata obligatoria) y Pass 4 (tipo de reactivo).
   - `scan_courses()` escanea la carpeta `courses/` y marca como `"status": "valid"` o `"status": "error"`.
   - Se requiere incorporar:
     * `repair_platform_course_katex(content: str) -> tuple[str, int]`:
       - Colapso de 4 barras seguidas de comando alfabético (`\\\\\\\\([a-zA-Z]+)` $\to$ `\\\\\1`).
       - Mapeo de `\\centernot` (`\\centernot\Rightarrow` $\to$ `\\nRightarrow`, `\\centernot` $\to$ `\\not`).
       - Reparación de `\text{textVar[barx_n] = O(n)}` $\to$ `\text{Var}[\bar{x}_n] = O(n)`.
       - Preservación intacta de saltos de matriz `\\\\ ` (espacio, dígito, signo o corchete).
     * En `validate_platform_course(content: str)`:
       - **Pass 1:** Detección de sobreescape KaTeX en texto crudo (`\\\\\\\\([a-zA-Z]+)`) y macro no soportada `\\centernot\b`, retornando `False` con mención explícita a `R-23`.
       - **Pass 4:** Validación en memoria sobre campos textuales (`stem`, `detailed_solution`, `solution`, `hints`, `options[*].content`, `options[*].error_rationale`) para impedir comandos con doble barra (`\\\\([a-zA-Z]+)`) y saltos `\\` dentro de bloques inline `$ ... $` fuera de entornos matriciales/sistemas (`matrix`, `bmatrix`, `pmatrix`, `cases`, `aligned`, `array`, `split`, `gathered`).
     * En `scan_courses()`:
       - Intercepción de errores de validación con `"R-23"`.
       - Auto-reparación vía `repair_platform_course_katex` y persistencia en disco si la reparación resulta válida, sirviendo el curso en estado `"status": "valid"`.

2. **`FUTURE_MILESTONES.md` y `docs/future_milestones/FUTURE_MILESTONES.md`:**
   - Ambos archivos están idénticos en líneas 269-285 (Milestone 4, ítem 5).
   - Se actualizará el encabezado del Protocolo de Protección Definitivo a `Protocolo de Protección Definitivo (Safeguards Implementados — ✅ COMPLETADO):` y se marcarán los 4 puntos como `✅ **IMPLEMENTADO:**` detallando los módulos correspondientes (`lexical_scanner.py`, `rules.py`, `invariants.py`, `assemble.py`, `compile_shard.py`, `run_platform.py`).

3. **`tests/test_platform_katex_admission_guard.py`:**
   - Archivo nuevo a crear. Probará:
     * Rechazo de `\\\\frac`, `\\\\text`, `\\\\to`, `\\\\mathbb`, `\\\\right`, `\\\\alpha`, `\\\\centernot` y `$a \\ b$` inline fuera de matriz, reportando `R-23`.
     * Aceptación de matrices en inline `$ ... $` y display `$$ ... $$`.
     * Reparación determinista y preservación de saltos de matriz.
     * Auto-reparación en `scan_courses` con directorio temporal (`monkeypatch`).
     * Validación al 100% de los 4 cursos reales en `courses/*.json`.

4. **Compatibilidad con Suite Existente:**
   - La suite `tests/test_platform.py` seguirá pasando al 100% sin ninguna regresión.

---

## 2. Plan de Acción y Alineación

- Procederemos de inmediato a implementar las modificaciones en `run_platform.py`.
- Actualizaremos sincronizadamente `FUTURE_MILESTONES.md` y `docs/future_milestones/FUTURE_MILESTONES.md`.
- Crearemos `tests/test_platform_katex_admission_guard.py`.
- Ejecutaremos `pytest tests/test_platform_katex_admission_guard.py tests/test_platform.py -q`.
- Generaremos `handoff.md` y emitiremos `DONE:: Stream 1D Impl completado`.
