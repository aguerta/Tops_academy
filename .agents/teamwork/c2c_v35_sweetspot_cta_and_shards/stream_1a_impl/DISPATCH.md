# DISPATCH — Stream 1A (Fase 1: Implementador `impl_1a`)

## 1. Rol y Frontera Exclusiva de Escritura (`Exclusive Write Boundaries`)
Eres el **Implementador del Stream 1A** bajo `/flash-triad-orchestrator`.
- **Carpeta de Gobernanza:** `.agents/teamwork/c2c_v35_sweetspot_cta_and_shards/stream_1a_impl/`
- **Archivos de Producción Permitidos (ÚNICOS que puedes modificar):**
  1. `.agents/skills/content-to-course/compile_cta.py`
  2. `.agents/skills/content-to-course/check_cta.py`
  3. `.agents/skills/content-to-course/cta_merge.py`
  4. `tests/test_cta_sweetspot_and_autoheal.py` *(nuevo archivo de tests unitarios)*
- **Artefactos de Gobernanza Permitidos:**
  - `.agents/teamwork/c2c_v35_sweetspot_cta_and_shards/stream_1a_impl/BRIEFING.md`
  - `.agents/teamwork/c2c_v35_sweetspot_cta_and_shards/stream_1a_impl/handoff.md`
- **PROHIBIDO** editar cualquier otro archivo del repositorio. Nunca pases `ArtifactMetadata` a `write_file` o `edit_file`.

## 2. Paso 0 Obligatorio (*Pre-Flight Sanity Check*)
Antes de realizar cualquier edición:
1. Lee `.agents/skills/content-to-course/compile_cta.py` (especialmente `CtaDataLineLocator` L190–L350, `compile_cta` L1050–L1480 y `render_compact_cta_errors` L1530–L1650), `.agents/skills/content-to-course/check_cta.py` (validación `[CTA-KATEX]` y formateo de errores L1–L450) y `.agents/skills/content-to-course/cta_merge.py` (`normalize_orphan_math` L40–L110).
2. Escribe `.agents/teamwork/c2c_v35_sweetspot_cta_and_shards/stream_1a_impl/BRIEFING.md` confirmando líneas y firmas reales. Si detectas un bloqueo fuera de tu frontera, detén ediciones y envía `BLOCKER:: <archivo:línea> | <causa> | <opciones>` al Orquestador (`7d2e6386-9933-4c70-9e50-a3cf214925f6`).

## 3. Especificación Técnica de Implementación

### A. Tier-0 Auto-Heal de KaTeX Huérfano en Distractores (`cta_merge.py` y `compile_cta.py`)
1. **Problema:** En `asyntotic_estatistics_v5`, `part_01` y `part_02` fallaron la 1.ª compilación con `[CTA-KATEX: Comandos LaTeX sin delimitar por '$...$']` porque algunos campos de distractor (`manifestation`, `wrong_belief`, `correct_belief`, `omitted_step`, `remediation_hint` o `description_latex`) tenían comandos LaTeX desnudos (`\lim`, `\frac`, `\sigma`, `\xrightarrow`, `\sqrt`, `\sum`, `\hat`, `\bar`, `\theta`, `\alpha`, `\beta`, `\to`, `\infty`, `\text`, etc.) sin envolver en `$ ... $` (por ejemplo: `r"\lim_{n\to\infty} \frac{\sigma^2}{n} = 0"` o prosa mixta con un comando LaTeX suelto fuera de `$ ... $`).
2. **Solución:**
   - En `cta_merge.py` (`normalize_orphan_math` / nuevo helper exportable `auto_wrap_bare_latex_in_cta_field(text: str) -> str`) y en `compile_cta.py`:
     - Si una cadena contiene comandos LaTeX (los mismos que detecta `LATEX_CMD_RE` en `check_cta.py`, ej. `\(?:frac|dfrac|tfrac|sqrt|sum|prod|int|oint|lim|infty|partial|nabla|alpha|beta|gamma|delta|epsilon|varepsilon|zeta|eta|theta|vartheta|iota|kappa|lambda|mu|nu|xi|pi|rho|sigma|tau|upsilon|phi|varphi|chi|psi|omega|Gamma|Delta|Theta|Lambda|Xi|Pi|Sigma|Upsilon|Phi|Psi|Omega|cdot|times|div|pm|mp|leq|geq|neq|approx|equiv|sim|simeq|propto|in|notin|subset|subseteq|cup|cap|forall|exists|Rightarrow|implies|iff|Leftrightarrow|to|rightarrow|leftarrow|xrightarrow|hat|bar|tilde|vec|dot|ddot|mathcal|mathbb|mathbf|boldsymbol|text|operatorname|left|right|begin|end)\b`) **fuera** de bloques `$ ... $` o `$$ ... $$`:
       - Si toda la cadena carece de `$` y es una expresión matemática o empieza con comando/símbolo LaTeX, envolverla en `$ ... $` (o envolver los segmentos contiguos que contienen comandos/subíndices/superíndices LaTeX en `$ ... $`) de manera que `check_cta.py` valide con **0 errores `[CTA-KATEX]`**.
       - Aplicar esta normalización determinista en memoria sobre las competencias y distractores en `compile_cta.py` **antes** de ejecutar `check_cta` / `validate_cta_data` y antes de escribir `cta.json` / `part_XX.json`.

### B. Mapeo AST Exacto a Línea Python por Elemento y Distractor (`CtaDataLineLocator` en `compile_cta.py` y `check_cta.py`)
1. **Problema:** `compile_cta.py` pasaba un `JsonLineLocator` en memoria a `check_cta.py`, por lo que los errores reportaban números de línea de `cta.json` (`Línea 305, 929, 1437`) o solo mapeaban el primer distractor (`D-H03-03`) a la línea de apertura `(` de toda la competencia (`L159`), impidiendo usar `edit_file` con precisión.
2. **Solución en `CtaDataLineLocator` (`compile_cta.py`):**
   - Al analizar cada nodo tupla en `COMPETENCIES`:
     - Guardar en `self.competency_lines[cid]` el rango `(start_line, end_line)`.
     - Guardar en `self.element_lines[cid]` un diccionario mapeando cada índice `0..8` (y nombre de campo: `type`, `id`, `name`, `description_latex`, `bloom`, `doc`, `page`, `prerequisites`, `distractors`) a `(elt.lineno, elt.end_lineno)`.
     - Para el elemento `8` (lista de tuplas de distractores), recorrer cada tupla de distractor `d_idx` (`0..k-1`, correspondiente a `D-{cid}-{d_idx+1:02d}` y también `D-{cid.replace('-', '')}-{d_idx+1:02d}`):
       - Guardar en `self.distractor_lines[did]` el rango `(d_node.lineno, d_node.end_lineno)` y el mapa por sub-campo (`0: "name"`, `1: "wrong_belief"`, `2: "correct_belief"`, `3: "manifestation"`, `4: "remediation_hint"`, `5: "omitted_step"`) a `(sub_elt.lineno, sub_elt.end_lineno)`.
     - Añadir un método `locator.resolve_error_location(err_msg: str, cid: Optional[str] = None) -> Tuple[int, int, str]` que:
       - Detecte si `err_msg` menciona un distractor `D-[A-Za-z0-9-]+-\d+` (y opcionalmente un campo como `manifestation`, `wrong_belief`, `correct_belief`, `omitted_step`, `remediation_hint`, `name`) o un campo de competencia (`description_latex`, `evidence`, `page`, `prerequisites`, `bloom`), y devuelva `(start_line, end_line, snippet_3_to_5_lines)` del archivo `.py` real!
   - En `render_compact_cta_errors` (`compile_cta.py`), usar `locator.resolve_error_location(...)` para que **cada error** muestre la línea exacta del archivo Python (`cta_data.py` o `part_XX_data.py`, `StartLine..EndLine`) y el snippet real de Python (nunca líneas del JSON virtual).

### C. Splicing Modular `cta_fixes/<CID>.py`, Aislamiento de `repair_pack` y Estado `.check_attempts` (`compile_cta.py`)
1. **Soporte de `cta_fixes/<CID>.py`:**
   - Implementar `discover_cta_fix_files(work_p: Path, target_py: Path, expected_cids: Optional[List[str]] = None)` buscando archivos `.py` en `target_py.parent / "cta_fixes"` y `work_p / "cta_fixes"` (y `work_p / "cta_parts" / "cta_fixes"`).
   - Cada archivo `cta_fixes/<CID>.py` puede definir `COMPETENCIES = [ ( ... ) ]` o `COMPETENCY = ( ... )` (tupla de 9 elementos). Si existe, reemplaza en memoria la tupla correspondiente a `<CID>` en `COMPETENCIES` antes de validar y compilar (y se incluye en el cálculo de `source_sha256` para que `compile_cta.py` detecte el cambio y no emita `[NO-CHANGE]`).
2. **Aislamiento Concurrente del Repair Pack:**
   - En `render_compact_cta_errors` / `compile_cta`: cuando se compila una subparte (`--part <part_id>` o cuando el archivo de entrada está en `cta_parts/<stem>_data.py` o `cta/<stem>_data.py`), escribir el repair pack en `<target_py.parent>/<part_id>_repair_pack.json` (ej. `work/cta_parts/part_01_repair_pack.json`) en lugar de sobrescribir un único `work/cta_repair_pack.json` compartido. En modo directo (`cta_data.py`), mantener `work/cta_repair_pack.json`. Incluir `"error_count": len(unique_errors)` dentro del JSON del repair pack.
3. **Contrato `.check_attempts/compile_cta_<target_id>.json` y `pass_cta_<target_id>.json`:**
   - Determinar `target_id`: `part_id` normalizado (ej. `part_01`) si es subparte, o `"cta_data"` si es `cta_data.py`.
   - En `work_p / ".check_attempts" / f"compile_cta_{target_id}.json"` (además de mantener compatibilidad si ya usa otro archivo de intentos), persistir en cada fallo:
     - `"distinct_compiles"`, `"same_error_streak"`, `"last_source_sha256"`, `"last_err_hash"`, `"last_errors"`, **`"error_count": int`** (conteo de errores deduplicados) y **`"has_syntax_error": bool`**.
   - Cuando la compilación CTA pasa con `0` errores, eliminar `compile_cta_{target_id}.json` y escribir `work_p / ".check_attempts" / f"pass_cta_{target_id}.json"` con `{"target_id": target_id, "status": "PASS", "source_sha256": source_sha256, "competency_count": len(competencies)}`. Si falla, eliminar `pass_cta_{target_id}.json` si existía.
4. **Directiva Dinámica del Umbral Oficial `< 6` en `render_compact_cta_errors`:**
   - Cuando `1 <= error_count < 6` (sin `SyntaxError`): imprimir instrucción obligatoria:
     `[UMBRAL OFICIAL < 6 ERRORES ({error_count}/5)]: Usa OBLIGATORIAMENTE edit_file (replace_file_content) quirúrgico en 1 turno paralelo sobre las líneas exactas de '{py_name}' indicadas arriba. PROHIBIDO reescribir todo el archivo con write_file.`
   - Cuando `error_count >= 6`: imprimir instrucción:
     `[UMBRAL OFICIAL >= 6 ERRORES ({error_count})]: Si los errores se concentran en 1-2 competencias, escribe el reemplazo modular en 'cta_fixes/<CID>.py' con write_file(Overwrite=True); si abarcan >= 3 competencias, reescribe '{py_name}' en 1 sola llamada write_file(Overwrite=True).`

## 4. Verificación y Entrega
1. Crea `tests/test_cta_sweetspot_and_autoheal.py` probando exhaustivamente:
   - Que una competencia con distractores conteniendo `\lim`, `\frac`, `\sigma` sin `$ ... $` (como en `asyntotic_estatistics_v5`) es auto-curada en Tier 0 por `compile_cta.py` y pasa con `0` errores.
   - Que ante errores reales (`1..5` vs `>= 6`), `CtaDataLineLocator` reporta la línea exacta de la tupla de distractor/campo en Python (no la línea de `cta.json`), escribe `cta_parts/part_01_repair_pack.json` aislado de `part_02_repair_pack.json`, graba `"error_count"` en `.check_attempts/compile_cta_part_01.json`, y emite la directiva `< 6` (`edit_file`) vs `>= 6` (`cta_fixes` / `write_file`).
   - Que `cta_fixes/<CID>.py` reemplaza limpiamente en memoria una competencia rota y genera `pass_cta_<target_id>.json` al aprobar.
2. Ejecuta `.venv\Scripts\python.exe -m pytest tests/test_cta_sweetspot_and_autoheal.py tests/test_compile_cta.py -q`.
3. Escribe `.agents/teamwork/c2c_v35_sweetspot_cta_and_shards/stream_1a_impl/handoff.md` y envía `DONE:: Stream 1A Implementer completado` a `7d2e6386-9933-4c70-9e50-a3cf214925f6`.
