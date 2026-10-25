# DISPATCH — Stream 1D (Fase 1: Implementador `impl_1d`)

## 1. Rol y Frontera Exclusiva de Escritura (`Exclusive Write Boundaries`)
Eres el **Implementador del Stream 1D** bajo `/flash-triad-orchestrator`.
- **Carpeta de Gobernanza:** `.agents/teamwork/c2c_v36_sandbox_repair_and_archetypes/stream_1d_impl/`
- **Archivos de Producción Permitidos (ÚNICOS que puedes modificar):**
  1. `.agents/skills/content-to-course/compile_shard.py`
  2. `.agents/skills/content-to-course/system_prompts/prompt_shard_author.md`
  3. `.agents/skills/content-to-course/system_prompts/lean/prompt_shard_author.md`
  4. `tests/test_m3_archetypes_semantic_gate.py`
- **Artefactos de Gobernanza Permitidos:**
  - `.agents/teamwork/c2c_v36_sandbox_repair_and_archetypes/stream_1d_impl/BRIEFING.md`
  - `.agents/teamwork/c2c_v36_sandbox_repair_and_archetypes/stream_1d_impl/handoff.md`
- **PROHIBIDO** editar cualquier otro archivo del repositorio. Nunca pases `ArtifactMetadata` a `write_file` o `edit_file`.

## 2. Paso 0 Obligatorio (*Pre-Flight Sanity Check*)
Antes de realizar cualquier edición:
1. Lee `.agents/skills/content-to-course/compile_shard.py` (líneas 1640–1705), `.agents/skills/content-to-course/system_prompts/prompt_shard_author.md` (líneas 240–320), `.agents/skills/content-to-course/system_prompts/lean/prompt_shard_author.md` (líneas 1–260) y `tests/test_shard06_and_dry_archetypes.py`.
2. Escribe `.agents/teamwork/c2c_v36_sandbox_repair_and_archetypes/stream_1d_impl/BRIEFING.md` confirmando líneas y firmas reales. Si detectas un bloqueo fuera de tu frontera, detén ediciones y envía `BLOCKER:: <archivo:línea> | <causa> | <opciones>` al Orquestador (`d603756a-7e58-4466-b883-cbc391586154`).

## 3. Especificación Técnica de Implementación

### A. Blindaje de la Compuerta `[M3-ARCHETYPES]` en `compile_shard.py` (líneas 1650–1680)
1. **Problema Raíz Detectado en la Auditoría:**
   - En `compile_shard.py:1655`, la compuerta `[M3-ARCHETYPES]` evalúa:
     `distinct_tuples = {(t.get("stem_es", "").strip(), t.get("generator_code", "").strip()) for t in tpls}`
   - Como `compile_shard.py` nombra al wrapper de cada tupla `def gen_h03_1`, `def gen_h03_2`, `def gen_h03_3`, `def gen_h03_4`, la cadena `generator_code` **siempre es distinta** por el nombre de la función wrapper!
   - Eso permitió dos violaciones graves del estándar de 4 arquetipos por competencia:
     1. **Enunciados (`stems`) clonados (`shard_12` y `shard_14`):** El autor pasó la **misma lista `stems_h03`** a las 4 tuplas de `TEMPLATES` (`stem_es` idéntico en las 4 tuplas), y `compile_shard.py` lo dejó pasar porque `generator_code` tenía distinto nombre de función!
     2. **Parámetro `arch` ignorado en `_gen_*(rng, arch=1)` (`11/25` competencias):** El autor escribió `def _gen_h01(rng, arch=1):` pero dentro de la función `_gen_h01` **nunca usó `arch`**, por lo que las 4 tuplas (`arch=1, 2, 3, 4`) producen exactamente las mismas variables y respuestas numéricas para una misma semilla!
2. **Solución Exacta en `compile_shard.py` (dentro del bloque `if strict_mode:` / `[M3-ARCHETYPES]`, líneas 1650–1675):**
   - **Verificación 1 — Enunciados (`stem_es`) distintos por arquetipo:**
     - Calcula `distinct_stems = {t.get("stem_es", "").strip() for t in tpls if t.get("stem_es", "").strip()}`.
     - Si `len(tpls) >= 2` y `len(distinct_stems) < min(eff_min_arch, len(tpls))` (por ejemplo, cuando pasan la misma lista `stems` a las 4 tuplas de modo que `len(distinct_stems) < len(tpls)`):
       - Registra un error `[M3-ARCHETYPES]`:
         `f"[M3-ARCHETYPES] Competencia '{cid}' repite el mismo enunciado (stem_es) entre sus tuplas ({len(distinct_stems)} enunciados únicos de {len(tpls)} tuplas). Cada arquetipo (1=Directo, 2=Inverso, 3=Perturbación, 4=Frontera) debe tener su propia lista de enunciados distinta."`
   - **Verificación 2 — Prohibición de función `_gen_*` que declara `arch` pero lo ignora (o 4 tuplas con código generador semánticamente idéntico):**
     - Normaliza el `generator_code` de cada tupla en `tpls` reemplazando el nombre del wrapper `def gen_<cid>_<idx>(` por `def _gen_wrapper_(`:
       `norm_gen_codes = {re.sub(r"def\s+gen_[a-zA-Z0-9_]+_\d+\s*\(", "def _gen_wrapper_(", t.get("generator_code", "").strip()) for t in tpls}`
     - Si `len(norm_gen_codes) < min(eff_min_arch, 2)` (es decir, todas las tuplas tienen exactamente el mismo cuerpo de generador incluso con el mismo `arch`), recházalo con `[M3-ARCHETYPES]`.
     - Además, inspecciona con `ast.parse(source_text)` (el AST del `shard_XX_data.py` que ya está disponible en `compile_shard_file`) cualquier función definida en el shard que tenga un argumento llamado `arch` (ej. `def _gen_*(rng, arch=1):`). Si el nombre `arch` aparece en los argumentos de la función (`[a.arg for a in node.args.args]`), verifica si `arch` es referenciado al menos una vez en el cuerpo (`body`) de esa función (`any(isinstance(sub, ast.Name) and sub.id == "arch" and isinstance(sub.ctx, ast.Load) for sub in ast.walk_body)`).
     - Si una función `_gen_*` recibe el parámetro `arch` pero **jamás lo lee en su cuerpo** (`arch` ignorado), y esa función es invocada por las tuplas de `cid`, emite un error `[M3-ARCHETYPES]` claro y accionable:
       `f"[M3-ARCHETYPES] Competencia '{cid}': la función generadora '{func_name}' recibe el parámetro 'arch' pero nunca lo utiliza en su cuerpo, produciendo salidas idénticas en los 4 arquetipos. Ramifica con 'if arch == 1 / elif arch == 2 / elif arch == 3 / else' para variar el problema matemático por arquetipo."`
     - **Cuidado con compatibilidad de tests existentes:** Si un test unitario existente usa 4 funciones separadas (`_gen_1(rng)`, `_gen_2(rng)`...) sin argumento `arch`, o usa `_gen_*(rng, arch=1)` donde `arch` SÍ se lee en el cuerpo (aunque sea en `if arch == 1:` o indexación), pasará al 100%! Verifica en tu Paso 0 `tests/test_shard06_and_dry_archetypes.py` y `tests/test_compile_shard.py` para asegurarte de que ningún test existente use un `arch` mudo no intencional (y si `test_shard06_and_dry_archetypes.py` tiene un snippet con `arch=1`, compruébalo en tu Paso 0 antes de editar!).

### B. Actualizar el Ejemplo Canónico 1 en `system_prompts/prompt_shard_author.md` y `system_prompts/lean/prompt_shard_author.md`
1. En `.agents/skills/content-to-course/system_prompts/prompt_shard_author.md` (líneas 245–305) y `.agents/skills/content-to-course/system_prompts/lean/prompt_shard_author.md` (si contiene el ejemplo de `_gen_h01`):
   - Actualmente el Ejemplo 1 (`H-01` Carnot) define `def _gen_h01(rng, arch=1):` sin usar `arch` y pasa la misma variable `stems_h01` a las 4 tuplas de `TEMPLATES`.
   - Actualízalo para que:
     1. Dentro de `def _gen_h01(rng, arch=1):`, `arch` se utilice explícitamente (ej. variando el régimen de temperaturas o la incógnita/escala según `arch == 1, 2, 3, 4`).
     2. Defina 4 listas de enunciados concisas (`stems_h01_1`, `stems_h01_2`, `stems_h01_3`, `stems_h01_4` correspondientes a Directo, Inverso, Perturbación y Frontera) y pase cada una a su tupla correspondiente (`arch=1, 2, 3, 4`) en `TEMPLATES`.
     3. Añade una nota breve recordando que `[M3-ARCHETYPES]` bloquea pasar la misma lista `stems` a las 4 tuplas o declarar `arch=1` sin usarlo dentro de `_gen_*`.

## 4. Verificación y Entrega
1. Crea `tests/test_m3_archetypes_semantic_gate.py` con tests unitarios que verifiquen:
   - Que un shard en modo `strict_mode=True, min_archetypes=4` que pasa la **misma lista `stems`** a las 4 tuplas de `TEMPLATES` es rechazado con `[M3-ARCHETYPES]`.
   - Que un shard en modo `strict_mode=True, min_archetypes=4` que define `def _gen_h01(rng, arch=1):` sin leer `arch` en el cuerpo de `_gen_h01` es rechazado con `[M3-ARCHETYPES]`.
   - Que un shard en modo `strict_mode=True, min_archetypes=4` con 4 `stems` distintos y `_gen_h01(rng, arch=1)` que sí utiliza `arch` (ramificando en `arch`) compila y aprueba `PASS` al 100%.
2. Ejecuta `.venv\Scripts\python.exe -m pytest tests/test_m3_archetypes_semantic_gate.py tests/test_shard06_and_dry_archetypes.py tests/test_compile_shard.py tests/test_shard_compiler_hardening.py -q`.
3. Escribe `.agents/teamwork/c2c_v36_sandbox_repair_and_archetypes/stream_1d_impl/handoff.md` y envía `DONE:: Stream 1D Implementer completado` a `d603756a-7e58-4466-b883-cbc391586154`.
