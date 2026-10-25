# DISPATCH — Stream 1D (Phase 2: Improver `impr_1d`)

## 1. Rol y Misión
Eres el **Mejorador (Phase 2 Improver)** del **Stream 1D (Prompts & Dispatch Sweet-Spot + Milestone 3 Anti-1-Tuple Hardening)** dentro de `/flash-triad-orchestrator`.
Debes leer primero:
1. `.agents/teamwork/c2c_v35_sweetspot_cta_and_shards/stream_1d_impl/BRIEFING.md`
2. `.agents/teamwork/c2c_v35_sweetspot_cta_and_shards/stream_1d_impl/handoff.md`

Tu misión es auditar el trabajo de `impl_1d` y eliminar de raíz las **3 causas de prompt y dispatch** por las cuales en `v5` algunos shards (`shard_02`, `shard_09`, `shard_19`) emitieron solo 1 tupla por competencia en lugar de los 4 arquetipos disjuntos del Milestone 3, mientras otros (`shard_08`, `shard_10`, `shard_16`, `shard_17`) escribieron 400–470 líneas por no tener un patrón compacto de 4 arquetipos.

## 2. Frontera Exclusiva de Escritura (100% Disjunta)
- **ARCHIVOS DE PRODUCCIÓN PERMITIDOS:**
  - `.agents/skills/content-to-course/dispatch.py`
  - `.agents/skills/content-to-course/system_prompts/prompt_cta_architect.md`
  - `.agents/skills/content-to-course/system_prompts/lean/prompt_cta_architect.md`
  - `.agents/skills/content-to-course/system_prompts/prompt_shard_author.md`
  - `.agents/skills/content-to-course/system_prompts/lean/prompt_shard_author.md`
  - `.agents/skills/content-to-course/system_prompts/prompt_repair.md`
  - `.agents/skills/content-to-course/system_prompts/lean/prompt_repair.md`
- **ARCHIVOS DE TEST PERMITIDOS:**
  - `tests/test_dispatch_turn0_and_milestone3_prompts.py`
- **ARCHIVOS DE GOBERNANZA PERMITIDOS:**
  - `.agents/teamwork/c2c_v35_sweetspot_cta_and_shards/stream_1d_impr/handoff.md`
- **PROHIBIDO TOCAR:** `subagent_types.json` (pertenece a Stream 2A en Gate 2) o cualquier otro archivo fuera de esta lista.

## 3. Requerimientos Técnicos Exactos para Fase 2 (`impr_1d`)

### A. Eliminar el Escape Hatch de 1 Tupla y Mostrar el Patrón Compacto de 4 Arquetipos en `prompt_shard_author.md` (Full y Lean)
1. **En `.agents/skills/content-to-course/system_prompts/prompt_shard_author.md`:**
   - **Línea ~43:** Elimina la frase permisiva `"(o 1 tupla por competencia en casos de evaluación atómica básica)"`. Debe decir tajantemente que **CADA competencia asignada DEBE definir mínimo 4 tuplas en `TEMPLATES` (los 4 arquetipos disjuntos: 1. Directo, 2. Inverso, 3. Perturbación, 4. Frontera)**, validado por `compile_shard.py` (`[M3-ARCHETYPES]`). Advertir explícitamente: *"PROHIBIDO emitir 1 sola tupla por competencia o meter 4 `stem_variants` dentro de 1 sola tupla; `compile_shard.py` rechazará con `FAIL: [M3-ARCHETYPES]` cualquier competencia con `< 4` tuplas en `TEMPLATES`."*
   - **Ejemplo de Código en `prompt_shard_author.md` (Secciones 4/6):**
     - En lugar de mostrar una sola tupla para `"H-01"` en `TEMPLATES = [...]`, muestra el **Patrón Compacto Parametrizado de 4 Arquetipos (~50–65 líneas por competencia)**:
       - Un helper compartido `def _gen_h01(rng, arch):` (~15 líneas) que calcula las variables comunes y ramifica `if arch == 1: ... elif arch == 2: ...` (o parametriza el cálculo) retornando `{"vars": ..., "correct": r"$@ans@$", "distractors": [r"$@d1@$", r"$@d2@$", r"$@d3@$", r"$@d4@$", r"$@d5@$", r"$@d6@$"]}`.
       - 4 wrappers de 1 línea:
         ```python
         def gen_h01_1(rng): return _gen_h01(rng, 1)
         def gen_h01_2(rng): return _gen_h01(rng, 2)
         def gen_h01_3(rng): return _gen_h01(rng, 3)
         def gen_h01_4(rng): return _gen_h01(rng, 4)
         def ver_ok(res): return True
         ```
       - 4 tuplas compactas de 9 elementos en `TEMPLATES` para `"H-01"` (pasando `[]` en posición 7 `target_misconceptions` y omitiendo el 10mo elemento `hints`, ya que `compile_shard.py` los auto-hereda desde `cta.json`!).
2. **En `.agents/skills/content-to-course/system_prompts/lean/prompt_shard_author.md`:**
   - Actualiza el bloque de ejemplo `TEMPLATES = [...]` y las reglas de `4 Arquetipos Disjuntos por Competencia (Milestone 3)` para:
     1. Dejar claro que **`TEMPLATES` exige 4 tuplas por competencia (`[M3-ARCHETYPES]`; 1 tupla o 4 stems en 1 tupla = `FAIL`)**.
     2. Mostrar en el snippet de ejemplo el patrón `def _gen_h01(rng, arch): ...` + `def gen_h01_1(rng): return _gen_h01(rng, 1)` (`1..4`) + las 4 tuplas de `"H-01"` en `TEMPLATES` con `[]` en posición 7 y sin 10mo elemento `hints`.
     3. **COTA ESTRICTA DE TAMAÑO:** Mantén `lean/prompt_shard_author.md <= 4,750` bytes (compactando prosa redundante si hace falta) y preserva todas las subcadenas obligatorias verificadas por `test_prompts_contract_alignment.py`, `test_c2c_v321_comp4_prompts.py` y `test_dispatch_turn0_and_milestone3_prompts.py`.

### B. Endurecer `dispatch.py` (`dispatch_authors`) con `--min-archetypes 4` y Estampado en `pre_shard_manifest.json`
1. En `dispatch_authors` (`.agents/skills/content-to-course/dispatch.py`):
   - Al leer `pre_shard_manifest.json`, estampa `"min_archetypes": 4` en el nivel raíz de `manifest_data` y en cada `shard` dentro de `manifest_data["shards"]` (si no está definido), y persiste `pre_shard_manifest.json` de vuelta a disco (`manifest_path.write_text(json.dumps(manifest_data, indent=2, ensure_ascii=False), encoding="utf-8")`).
   - En `compile_cmd` de `dispatch_authors`, incluye `--min-archetypes 4`:
     `compile_cmd = f'{venv_py} .agents/skills/content-to-course/compile_shard.py {shard_py_rel} --work {work_rel} --shard {shard_id} --strict --min-archetypes 4'`
   - En la **Instrucción 2** de `dispatch_authors`:
     Indica explícitamente:
     `"2. **4 Arquetipos Disjuntos OBLIGATORIOS por Competencia (\`[M3-ARCHETYPES]\`):** DEBES definir **4 tuplas en \`TEMPLATES\` por cada competencia asignada** (1. Directo, 2. Inverso, 3. Perturbación, 4. Frontera). Emitir 1 sola tupla por competencia o poner 4 \`stem_variants\` dentro de 1 tupla es rechazado con \`FAIL: [M3-ARCHETYPES]\`. Para mantener el archivo compacto (~55-75 líneas/competencia), usa un helper parametrizado \`def _gen_<cid>(rng, arch):\` + 4 wrappers \`def gen_<cid>_1(rng): return _gen_<cid>(rng, 1)\` (1..4) y tuplas de 9 elementos con \`[]\` en \`target_misconceptions\` (auto-heredado de \`cta.json\`)."`

### C. Ampliar Pruebas en `tests/test_dispatch_turn0_and_milestone3_prompts.py`
- Agrega verificaciones en `tests/test_dispatch_turn0_and_milestone3_prompts.py`:
  1. Que `prompt_shard_author.md` NO contenga la frase permisiva `"o 1 tupla por competencia"` y SÍ documente `[M3-ARCHETYPES]` y el patrón `_gen_h01(rng, arch)`.
  2. Que `lean/prompt_shard_author.md` documente `[M3-ARCHETYPES]`, muestre las 4 tuplas / wrappers `gen_h01_1`..`gen_h01_4`, y pese `<= 4,750` bytes.
  3. Que `dispatch_authors` incluya `--min-archetypes 4` en `compile_cmd`, mencione `[M3-ARCHETYPES]` en sus directivas, y estampe `"min_archetypes": 4` en `pre_shard_manifest.json`.

## 4. Verificación y Handoff
1. Ejecuta:
   `.venv\Scripts\python.exe -m pytest tests/test_dispatch_turn0_and_milestone3_prompts.py tests/test_dispatch_scope.py tests/test_prompts_contract_alignment.py tests/test_c2c_v321_comp4_prompts.py -q`
2. Normaliza CRLF a LF en los archivos de tu frontera.
3. Escribe `.agents/teamwork/c2c_v35_sweetspot_cta_and_shards/stream_1d_impr/handoff.md` y envía `DONE::` al Orquestador (`7d2e6386-9933-4c70-9e50-a3cf214925f6`).
