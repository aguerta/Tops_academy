# BRIEFING — Stream 1A (Pre-Flight Sanity Check)

## 1. Identificación y Fronteras
- **Agente:** `impl_1a` (Phase 1 Implementer — Stream 1A)
- **Orquestador:** `7d2e6386-9933-4c70-9e50-a3cf214925f6`
- **Carpeta de Gobernanza:** `.agents/teamwork/c2c_v35_sweetspot_cta_and_shards/stream_1a_impl/`
- **Archivos de Producción Permitidos:**
  1. `.agents/skills/content-to-course/compile_cta.py`
  2. `.agents/skills/content-to-course/check_cta.py`
  3. `.agents/skills/content-to-course/cta_merge.py`
  4. `tests/test_cta_sweetspot_and_autoheal.py`
- **Artefactos de Gobernanza Permitidos:**
  - `BRIEFING.md`
  - `handoff.md`

## 2. Verificación de Firmas y Ubicaciones Reales en Código Existente

### A. `compile_cta.py`
- `CtaDataLineLocator`: L80–L240. Actualmente solo indexa líneas iniciales de tupla de competencia (`comp_lines`) y el primer distractor por nombre en `distractor_lines`. Requiere almacenar rangos exactos `(start_line, end_line)` en `self.competency_lines`, rangos por campo en `self.element_lines`, rangos por distractor y subcampo en `self.distractor_lines` y `self.distractor_field_lines`, e implementar `resolve_error_location(err_msg, cid) -> Tuple[int, int, str]`.
- `compile_cta`: L1000–L1377. Pasa `json_locator = JsonLineLocator(json_str)` a `check_cta_part` y `validate_cta_rules` (causando números de línea virtuales del JSON). Requiere pasar el `CtaDataLineLocator(source_text)` real de Python, integrar `discover_cta_fix_files`, calcular `source_sha256` considerando fixes, gestionar el estado en `.check_attempts/compile_cta_<target_id>.json` y `pass_cta_<target_id>.json`, y aplicar Tier-0 auto-heal de KaTeX antes de validar.
- `render_compact_cta_errors`: L1505–L1737. Actualmente sobrescribe un único `work/cta_repair_pack.json` compartido y emite mensajes genéricos sin la directiva de umbral dinámico (< 6 vs >= 6). Requiere aislamiento en `<part_id>_repair_pack.json`, inclusión de `"error_count"`, y la directiva oficial de umbral (< 6 errores: `edit_file` obligatorio; >= 6: modular `cta_fixes/<CID>.py` o rewrite completo).

### B. `check_cta.py`
- `RAW_LATEX_PATTERNS`: L26–L34. Lista actual restringida de comandos LaTeX macros. Debe ampliarse con el catálogo exhaustivo de comandos (`\lim`, `\xrightarrow`, `\infty`, `\sum`, `\prod`, etc.).
- `check_cta_katex`: L351–L463. Valida campos de competencias y distractores llamando `validate_katex_syntax`. Actualmente invoca `locator.get_line(...)` que funcionará directamente con `CtaDataLineLocator`.
- `_validate_competencies_rules`: L466–L613. Formatea errores de cuotas CTA-D1, CTA-D2 y evidencia usando `locator`.
- `validate_cta_rules` (L664–L709) y `check_cta_part` (L615–L662): Reciben `locator`. Al recibir `CtaDataLineLocator` en lugar de `JsonLineLocator`, reportarán líneas de código Python exactas.

### C. `cta_merge.py`
- `normalize_orphan_math`: L161–L314. Aplica transformaciones atómicas sobre texto fuera de `$ ... $`. Si una expresión multitérmino contiene comandos desnudos (`\lim_{n\to\infty} \frac{\sigma^2}{n} = 0`), las sustituciones individuales fragmentan la fórmula o anidan `$`. Se añadirá `auto_wrap_bare_latex_in_cta_field(text: str) -> str` al inicio de la normalización para detectar y envolver expresiones matemáticas que contienen comandos LaTeX en `$ ... $`.
- `sanitize_competency_math`: L317–L380. Itera sobre campos de competencia y distractor llamando a `normalize_orphan_math`.

## 3. Estado de Dependencias y Bloqueos (Tier A / Tier B)
- **Evaluación de Bloqueos:** CERO bloqueos. Todos los puntos de integración residen en los 3 archivos de producción asignados y en el nuevo archivo de tests.
- **Plan de Acción:** Proceder con la implementación de Tier-0 Auto-Heal en `cta_merge.py` y `compile_cta.py`, AST Exact Line Locator en `compile_cta.py` y `check_cta.py`, y gestión modular de fixes, repair pack y `.check_attempts` en `compile_cta.py`.
