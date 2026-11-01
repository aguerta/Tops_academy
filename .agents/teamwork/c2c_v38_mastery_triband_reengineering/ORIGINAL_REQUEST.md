# Solicitud Original (`c2c_v38_mastery_triband_reengineering`)

## 1. Contexto y Mandato del Usuario
Reingeniería integral de `content-to-course` (C2C v3.8) basada en la radiografía forense `d:\Augusto\Downloads\sintesis_forense_c2c_comparativa_y_radiografia_total.md` (24 defectos verificados + discrepancia `D7` + intervenciones `P0.1`–`P0.6`), incorporando los 4 cierres deterministas solicitados explícitamente por el usuario y ejecutada mediante `/flash-triad-orchestrator`:

1. **Brecha 1 (`[TPL-DYNAMIC-RATIONALE]` + Piso P4 en Stage 6):**
   - Prohibición determinista de `error_rationale` opcional/estático: retiro de 2-tupla `(did, val)` en `compile_shard.py --strict`, exigiendo 3-tupla `(did, val, error_rationale)` (`len >= 20`) e interpolación `@var@` obligatoria en distractores paramétricos/cuantitativos.
   - Verificación en dry-run (`check_templates.py`, `strict=True`, `seeds >= 15`): todo distractor con `content` variable entre semillas debe variar también su `error_rationale` renderizado (`len(unique_rationales) > 1`) y `rationale_uniqueness_pct >= 35%`.
   - Compuerta bloqueante en `course_publisher.py` (`strict=True`): `pillars["diagnostic_remediation_alignment"]["score"] >= 13.0 / 15.0` y `rationale_uniqueness_pct >= 30.0%` (cuando `total_rationales >= 60`).
2. **Matiz 2 (Fail-Fast `[KATEX-PROSE-OVERFLOW]` en Stage 1):**
   - Rechazo determinista de `\text{...}`, `\textrm{...}`, `\mathrm{...}` `> 45` caracteres directamente en `check_cta.py` (`validate_distractor_math` y `check_cta_katex`, cubriendo `name`, `description`, `description_latex`, `source_examples` y los 6 campos de cada distractor) para fallar en Stage 1 antes de heredar prosa larga hacia Stage 3.
3. **Matiz 3 (`--append` en 2 Capas — Stage 1 Semántico + Stage 6 Compuesto):**
   - Capa 1 (Stage 1): todo flujo `--append` pasa por `c2c_cta_harmonizer` con nodos `[BASE]` de solo lectura desde `delta_manifest.json` (`JACCARD_DUPLICATE_THRESHOLD = 0.30`).
   - Capa 2 (Stage 6, `course_publisher.py`): similitud determinista compuesta `content_stem_jaccard >= 0.38` (raíces de 5 letras sin stopwords) o `(content_stem_jaccard >= 0.28 and math_symbol_jaccard >= 0.50)` para capturar paráfrasis reales como `0.444`.
4. **Matiz 4 (Simetría `1A <-> 2A` y `[TPL-STATIC-OPT]` con `vars == {}`):**
   - `cta_merge.py:merge_cta_parts()` jamás escribe `work/cta.json` (1 o `N` partes); `run.py` usa el predicado único `needs_harmonize = (self.cta_mode == "mapreduce") or bool(part_files) or bool(is_append_mode)`.
   - `[TPL-STATIC-OPT]` en `check_templates.py` bloquea incondicionalmente `len(unique_correct) == 1` incluso si `vars = {}` está vacío.
