# Pre-Flight Briefing: Stream 1B Improver (`impr_1b`)

**Fecha:** 2026-10-24  
**Agente:** Mejorador Senior (`impr_1b`)  
**Stream:** 1B (Compilador de Shards, Arquetipos DRY y Shard 06)  
**Fase:** Fase 2 (Endurecimiento y Casos Borde)  

---

## 1. Verificación Pre-Flight y Revisión del Implementador (`impl_1b`)

Se inspeccionaron detalladamente los artefactos y cambios entregados por el Implementador:
1. `.agents/teamwork/c2c_v34_variance_and_shard06/stream_1b_impl/handoff.md`: Confirma 40 tests pasando en 7.29s sobre 3 suites (`test_shard06_and_dry_archetypes.py`, `test_compile_shard.py`, `test_shard_compiler_hardening.py`).
2. `.agents/skills/content-to-course/compile_shard.py`: Incorporó el wrapper dinámico `build_adapted_mc7_generator` para los 4 arquetipos de Milestone 3, el parámetro `--output` no destructivo con `compiled_status`, inferencia de `work_dir` por lockfile activo y creación/limpieza de `pass_<shard_id>.json`.
3. `.agents/skills/content-to-course/check_templates.py`: Añadió `auto_heal_template_data` con protección contra desescape de backslashes mediante lambdas en `re.sub`, `_wrap_bare_latex_in_rationale`, `_strip_giveaway_prefix`, `format_invariant_error_diagnostic` quirúrgico (R-20) y paridad de rutas en `render_compact_aggregated_errors`.
4. `tests/test_shard06_and_dry_archetypes.py`: Suite con 9 tests cubriendo arquetipos DRY, receipt CLI, lifecycle de pass marker, inferencia de workspace, diagnósticos de ruta y KaTeX wrapping.

---

## 2. Hallazgos de Análisis y Casos Borde Identificados

A partir de la inspección de código y los requisitos de `DISPATCH.md`, se identificaron los siguientes casos borde críticos a endurecer:

### Caso Borde 1: Subíndices y Superíndices Anidados en KaTeX (`_wrap_bare_latex_in_rationale`)
- **Problema:** La expresión regular `bare_pattern` usaba `[^{}]*` para capturar argumentos entre llaves (`\{[^{}]*\}` y `_\{[^{}]*\}`). Ante expresiones matemáticas con llaves anidadas como `\hat{\beta}_{\text{ML}}`, `\sigma^2_{x_i}`, `\hat{\beta}_1^{(k)}` o `\sqrt{\frac{A}{B}}`, el regex se detenía prematuramente en la primera llave de cierre interna. Esto generaba expresiones corruptas con llaves desbalanceadas (ej: `$\hat{\beta}_{\text}$ML}`) rompiendo la validación R-20.
- **Acción:** Reemplazar el escaneo ingenuo por un analizador de balanceo de llaves con contador de profundidad (`depth`), permitiendo cualquier nivel de anidamiento de subíndices, superíndices y macros KaTeX sin corromper la sintaxis.

### Caso Borde 2: Validación Real de `shard_06_data.py` en Modo Strict (0 Errores)
- **Problema:** Es necesario garantizar formalmente en el banco de pruebas unitarias que los archivos reales de producción `courses/asyntotic_estatistics_v4/work/shards/shard_06_data.py` compilen limpiamente contra `courses/asyntotic_estatistics_v4/work/cta.json` con 0 errores bajo `--strict` y 50 semillas, verificando que los 6 distractores hereden sus rationales socráticas sin fallar ninguna regla (R-17, R-20, R-22, TPL-D1..D4).
- **Acción:** Implementar un test de integración en `tests/test_shard06_and_dry_archetypes.py` que clone el entorno de shard_06 en un `tmp_path` aislado y verifique la compilación limpia al 100%.

### Caso Borde 3: Herencia DRY en Tuplas de 3 Elementos vs Diccionarios
- **Problema:** En generadores que retornan tuplas `(vars_dict, ans_str, dists_list)` donde `dists_list` contiene una mezcla heterogénea de arquetipos (tuplas invertidas, tuplas compactas, diccionarios sin rationale, cadenas escalares bare), el wrapper debe mapear unívocamente cada distractor a su ID y rationale pedagógica de `cta.json`, evitando colisiones y garantizando completitud MC7 (1 correcta + 6 distractores).
- **Acción:** Fortalecer el parser posicional y el anclaje numérico de candidatos adicionales usando extracción regex `[-+]?(?:\d*\.\d+|\d+)` en vez de tokenización manual, garantizando estabilidad y determinismo.

### Caso Borde 4: Limpieza Incondicional de `pass_<shard_id>.json` ante Fallos Tempranos
- **Problema:** Si la compilación fallaba antes de invocar `_fail` (por ejemplo, manifest no encontrado o shard data file inexistente), un marcador `pass_<shard_id>.json` previo podría persistir erróneamente en el directorio `.check_attempts/`.
- **Acción:** Asegurar que `pass_<norm_shard_id>.json` se desvincule incondicionalmente en todas las ramas de fallo temprano en `compile_shard.py`.

---

## 3. Plan de Endurecimiento y Verificación
1. **Endurecer `_wrap_bare_latex_in_rationale` en `check_templates.py`:** Implementar `_scan_latex_balanced_span` para soportar anidamientos arbitrarios de subíndices y superíndices en KaTeX.
2. **Refinar `build_adapted_mc7_generator` en `compile_shard.py`:** Optimizar la extracción de ancla numérica y el soporte de tuplas de 3 elementos con arquetipos mixtos.
3. **Garantizar desvinculación incondicional de pass marker en `compile_shard.py`:** Proteger las rutas de salida tempranas.
4. **Expandir `tests/test_shard06_and_dry_archetypes.py`:**
   - Test de compilación real de `shard_06_data.py` (aislado en tmp_path, strict=True, 50 seeds).
   - Test de KaTeX con subíndices/superíndices anidados (`\hat{\beta}_{\text{ML}}`, `\sigma^2_{x_i}`, `\frac{n-k}{2}`, etc.).
   - Test de tupla de 3 elementos con arquetipos heterogéneos.
5. **Ejecutar suite completa de tests de regresión y verificar 100% PASS.**
