# Handoff Report: Survey and Architecture for `content-to-course` v2

**Agent:** `explorer_survey_skill`  
**Working Directory:** `g:\Mi unidad\Competence_analyser\.agents\teamwork\explorer_survey_skill`  
**Parent Orchestrator:** `8c6e51b9-04fd-4a8c-a9ab-21b3a1985725`  
**Date:** 2026-10-11  

---

## 1. Observation

1. **Ubicación y volumen de código de dominio actual:**
   - `.agents/skills/content-to-course/edos_synthesizer.py` (1,164 líneas, 91 KB): Es 100% código específico de EDOs, autovalores, matriz Jacobiana y macroeconomía dinámica (`EDOSSynthesizer.is_edos_comp`, `synthesize_mc7`, etc.).
   - `.agents/skills/content-to-course/batch_generator.py` (2,243 líneas, 140 KB): En las líneas 115–120 detecta `is_edos` inspeccionando cadenas de título/contenido. En las líneas 401–432 define `fallback_misconceptions` con reglas hardcodeadas de EDP (`H-01`, `H-04`, `HAB-01`, `HAB-04`, `HAB-08`, `C-02`). En las líneas 647–1200+ implementa `_synthesize_mc7_content`, `_synthesize_fib_content` y `_synthesize_ms_content` mediante cadenas `if code == "H-01": ... elif code == "H-02": ...`.
   - `.agents/skills/content-to-course/cta_analyzer.py` (1,001 líneas, 63 KB): En las líneas 281–380 (`_try_llm_generation`) intenta conectarse a APIs externas (Gemini, OpenAI, Anthropic) usando `urllib.request`. En las líneas 408–414 bifurca hacia `_analyze_edos_document` (líneas 415–560) o `_analyze_pde_document` (líneas 561–800+) devolviendo taxonomías de Markdown fijas y prefabricadas.
   - `.agents/skills/content-to-course/verifier.py` (1,009 líneas, 47 KB): El `BlindSolver` (líneas 200–550+) contiene más de 30 reglas regex hardcodeadas para deducir respuestas de EDP y EDO ("Cobb-Douglas", "Lagrange EDP", "2nd order classification", "Lotka-Volterra", etc.). En las líneas 114–148, `SymPyVerifier` tiene métodos específicos de dominio: `verify_characteristic_roots` y `verify_euler_homogeneity`.
   - `.agents/skills/content-to-course/run.py` (244 líneas): En las líneas 89–103 fuerza slugs de dominio (`if any(w in title ... cid = "sistemas_edos")`) y ejecuta un flujo secuencial monolítico sin soporte de etapas reanudables (`--stage`, `--from-stage`, `--review-cta`).
   - `.agents/skills/content-to-course/pdf_extractor.py` (480 líneas): Extrae únicamente texto plano con PyMuPDF/pdfplumber. No renderiza a imagen, no soporta PDFs manuscritos sin capa de texto (`Stats3 10-10.pdf` con 308 caracteres), ni maneja imágenes sueltas como `stats 3 3-10.png`.
   - `tests/test_skill.py` (556 líneas): 27 pruebas fuertemente acopladas a métodos de dominio (`test_blind_solver_cobb_douglas_degree`, `test_blind_solver_lagrange_first_order_pde`, `test_characteristic_roots_hyperbolic_parabolic_elliptic`, `test_cta_analyzer_full_taxonomy_decomposition`).

2. **Nuevo material de entrada (`content/estadistica3_Cano`):**
   - 3 PDFs Beamer: `EST3_LEC01_26_2.pdf` (13 págs), `EST3_LEC02_26_2.pdf` (26 págs), `EST3_LEC03_26_2.pdf` (29 págs). Presentan acentos descompuestos (`´`+vocal).
   - 1 PDF manuscrito: `Stats3 10-10.pdf` (9 págs, 3.5 MB, export OneNote con trazos vectoriales, sin texto extraíble).
   - 1 Imagen PNG: `stats 3 3-10.png` con resolución de **5941 × 3327 píxeles** (pizarra con derivaciones matriciales y tabla de regresión de software EViews). Supera los 2500 px.

3. **Plataforma web y calificación matemática:**
   - En `platform/src/types.ts` (línea 51), `FillBlankAnswer` solo admite `expression`, `accepted_equivalents` y `tolerance`.
   - En `platform/src/utils/mathEquivalence.ts` (líneas 109, 140), `checkMathEquivalence` busca únicamente `targetAnswer.expression`, no reconoce `canonical_algebraic` ni `value`, no normaliza coma decimal (`0,8333` -> `0.8333`), y usa tolerancia genérica `0.001` sin soporte de 4 decimales (`0.00005`) ni equivalencia directa de fracciones contra decimales.

4. **Estado de pruebas actuales de regresión:**
   - `python -m validator.cli courses/pde_course.json --strict` -> Exited 0 (pasa todas las 16 reglas).
   - `python -m validator.cli courses/sistemas_edos.json --strict` -> Exited 0 (pasa todas las 16 reglas).
   - `python -m pytest tests/test_validator.py tests/test_platform.py -q` -> 114 passed en 24.34 s.

---

## 2. Logic Chain

1. **De las Observaciones 1.1–1.5 al rediseño del motor:**
   El código actual no es un "generador universal", sino un ensamblador de plantillas prefijadas para dos materias específicas (EDP y EDO). Para que cualquier tema académico (como Estadística III) se convierta en curso interactivo Khan sin alterar código Python, es indispensable eliminar `edos_synthesizer.py` y `batch_generator.py` e introducir un motor genérico (`engine/sandbox.py`, `instantiate.py`, `assemble.py`, `invariants.py`, `diversity.py`).
2. **De la Observación 1.1 al contrato por etapas:**
   La presencia de llamadas a APIs externas en `cta_analyzer.py` y el fallback silencioso violan el principio R1. El LLM es el agente de Antigravity (no llamadas REST opacas en segundo plano). Cada etapa debe comunicarse mediante artefactos JSON en disco (`manifest.json`, `cta.json`, `templates/*.json`, `course.json`) validados contra esquemas JSON (`schemas/`), deteniéndose inmediatamente si falta un archivo (fail-fast).
3. **De la Observación 2 al módulo `ingest.py`:**
   Dado que `Stats3 10-10.pdf` carece de texto legible por parser y `stats 3 3-10.png` mide 5941×3327 px, un extractor de texto plano falla completamente. `ingest.py` debe renderizar páginas a PNG, aplicar teselado con 10% de solape a imágenes > 2500 px, registrar hashes SHA-256 en `manifest.json` para caché, y permitir que los subagentes transcriban a KaTeX estructurado.
4. **De la Observación 3 al refactor de la plataforma:**
   En estadística, las respuestas escalares (coeficientes, errores estándar, p-valores) son decimales de precisión fija (`0.8333`, `0.0030`, `5/6`) y a menudo los usuarios escriben comas decimales (`0,8333`). El refactor de `mathEquivalence.ts` y `types.ts` es obligatorio para evitar falsos negativos en la plataforma.
5. **De la Observación 4 al plan secuencial de dos fases:**
   Como los cursos legados (`pde_course.json` y `sistemas_edos.json`) y sus tests pasan actualmente con éxito, la Fase 1 debe implementar el motor v2, los esquemas, la ingesta, los ejemplos few-shot y el refactor de plataforma, congelando el código antes de ejecutar la Fase 2 sobre Estadística III.

---

## 3. Caveats

- **Costo temporal de la visión:** Transcribir 68 páginas Beamer + 9 manuscritas + 6 teselas + 1 overview (≈84 imágenes) requerirá paralelismo de subagentes (~9 subagentes procesando lotes de ~10 imágenes). El presupuesto de <10 min aplica a las etapas 1–3 de generación matemática; la visión se mide de forma desacoplada con mitigación por caché SHA-256.
- **Gráficos de distribuciones:** Conforme a lo acordado con el usuario, para pruebas t, F y p-valores no se generarán densidades de probabilidad en `CoordinatePlane` (`GraphSpec`); se usará KaTeX limpio y tablas `array`.
- **Validador global vs validador de la skill:** Las reglas nuevas `CTA-D1/D2`, `TPL-D1..D4` y la diversidad (≥0.5) se evalúan dentro de `check_cta.py`, `check_templates.py` e `invariants.py`. No se alteran las reglas del validador global (`src/validator`) para mantener la compatibilidad con los cursos legados de EDP y EDO (cuya diversidad ronda 0.09).

---

## 4. Conclusion

El diagnóstico del sistema confirma la viabilidad y necesidad estricta del rediseño v2 de `content-to-course`:
1. **Límites de archivo propuestos:**
   - Esquemas: `schemas/pages.schema.json`, `schemas/cta.schema.json`, `schemas/template.schema.json`.
   - Validadores: `check_pages.py`, `check_cta.py`, `check_templates.py`.
   - Ingesta: `ingest.py` (con renderizado, teselado con 10% de solape y caché SHA-256).
   - Motor: `engine/sandbox.py`, `engine/instantiate.py`, `engine/assemble.py`, `engine/render.py`, `engine/invariants.py`, `engine/diversity.py`.
   - Arbitraje & CLI: `judge.py`, `run.py` (etapas explícitas, fail-fast).
   - Ejemplos Few-Shot: `examples/edp/` y `examples/edo/` (2 competencias por tema).
   - Plataforma: `platform/src/types.ts` y `platform/src/utils/mathEquivalence.ts`.
2. **Eliminación total de lógica de dominio:**
   - `edos_synthesizer.py` y `batch_generator.py` se eliminan.
   - `verifier.py` se limpia de regex del `BlindSolver` y de funciones de dominio.
   - `tests/test_skill.py` se reescribe contra las invariantes y seguridad del motor genérico.
3. **Hoja de ruta secuencial:**
   - Fase 1 (Infraestructura de Código y Congelación): Implementación de Milestones 1 al 6, ejecución de regresiones completas y Code Freeze.
   - Fase 2 (Datos del Curso Nuevo): Ingesta y generación del curso de Estadística III sin modificar una sola línea de código Python o TypeScript.

El reporte completo de diseño se encuentra disponible en:
`g:\Mi unidad\Competence_analyser\.agents\teamwork\explorer_survey_skill\analysis.md`.

---

## 5. Verification Method

Para verificar independientemente las afirmaciones de este informe:

1. **Verificar el acoplamiento de dominio actual:**
   ```powershell
   Get-ChildItem -Path ".agents\skills\content-to-course" -Filter "*.py" | ForEach-Object {
       $m = Select-String -Path $_.FullName -Pattern "edo|pde|derivadas|jacobiana|eigen|euler|lagrange|cauchy|lotka" -CaseSensitive:$false
       if ($m) { Write-Output "$($_.Name): $($m.Count) matches" }
   }
   ```
   *Condición de invalidación:* Si no se encuentran coincidencias en `edos_synthesizer.py` o `batch_generator.py`.

2. **Verificar que los cursos legados pasan el validador estricto actual:**
   ```powershell
   python -m validator.cli courses/pde_course.json --strict
   python -m validator.cli courses/sistemas_edos.json --strict
   ```
   *Resultado esperado:* Ambos salen con código 0 (`VALID: Course passed all 16 validation rules`).

3. **Verificar la suite de tests de regresión del validador y la plataforma:**
   ```powershell
   python -m pytest tests/test_validator.py tests/test_platform.py -q
   ```
   *Resultado esperado:* 114 passed en < 30 s.

4. **Verificar las dimensiones de la imagen grande de Estadística III:**
   ```powershell
   python -c "from PIL import Image; im = Image.open('content/estadistica3_Cano/stats 3 3-10.png'); print(im.size)"
   ```
   *Resultado esperado:* `(5941, 3327)`, confirmando la necesidad de teselado (> 2500 px).
