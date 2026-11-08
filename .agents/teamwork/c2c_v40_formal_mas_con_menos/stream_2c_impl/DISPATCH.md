# DISPATCH — Stream 2C (Fase A: Implementador Ortogonal — Gate 2)

- **Parent Conversation ID:** `cbe0c4d9-d376-429c-92b2-ffaeec91ae7f`
- **Stream Folder:** `d:\Augusto\personal_portfolio\Tops_academy\.agents\teamwork\c2c_v40_formal_mas_con_menos\stream_2c_impl`

## Frontera Exclusiva de Escritura (`Exclusive Write Boundary`)
SOLO tienes permiso de escritura sobre:
1. `d:\Augusto\personal_portfolio\Tops_academy\tests\test_forensic_replay_ab30cf91.py`
2. `d:\Augusto\personal_portfolio\Tops_academy\tests\test_forensic_shard06_and_variance_v34.py`
3. `d:\Augusto\personal_portfolio\Tops_academy\tests\test_sweetspot_v35_cta_and_shards.py`
4. `d:\Augusto\personal_portfolio\Tops_academy\tests\test_c2c_v40_formal_certification.py` `[NEW]`
5. `d:\Augusto\personal_portfolio\Tops_academy\.agents\teamwork\c2c_v40_formal_mas_con_menos\stream_2c_impl\BRIEFING.md` `[NEW]`
6. `d:\Augusto\personal_portfolio\Tops_academy\.agents\teamwork\c2c_v40_formal_mas_con_menos\stream_2c_impl\handoff.md` `[NEW]`

PROHIBIDO tocar cualquier archivo de producción (`.agents/skills/content-to-course/**`, `src/**`) u otros tests! Si encuentras un bug real en un archivo de producción fuera de tu frontera, reporta de inmediato `BLOCKER:: Stream 2C | <archivo:línea> | <causa> | <fix propuesto>` vía `send_message`.

## Especificación Técnica (Gate 2 — Replays Forenses + Suite Maestra Neuro-Simbólica `test_c2c_v40_formal_certification.py`)

1. **Alineación de las 3 Suites de Replay Forense (`ab30cf91`, `v34`, `v35`):**
   - Actualiza las aserciones de contrato que verificaban `min_archetypes == 3` en `dispatch_authors` / `pre_shard_manifest.json` / prompts (como `test_forensic_replay_ab30cf91.py:L1050-L1095` y `test_sweetspot_v35_cta_and_shards.py:L796`) al nuevo contrato `min_archetypes == 4` (`CONTRACT_VERSION == 2`), y actualiza cualquier fixture con verificador tautológico para que cumpla Refutación Estricta de Distractores sin debilitar ninguna prueba forense histórica.

2. **Creación de `tests/test_c2c_v40_formal_certification.py` `[NEW]` (Certificación Integral Fase 1 + Fase 2 + Property-Based Testing `Hypothesis` + `Z3`):**
   - Construye una suite de certificación de extremo a extremo rápida (`< 4 s`) que verifique empíricamente las **10 patologías erradicadas** y las garantías formales:
     1) **Bug `np.bool_(False)` erradicado:** Verifica en `sandbox.py` que un `cross_check` que devuelve `np.bool_(False)` (vía `np.isclose(1.0, 2.0)`), `None` o `0` lanza `SandboxExecutionError` tanto en `execute_sandbox_instance` como en `execute_sandbox_batch`, mientras `np.bool_(True)` y `True` aprueban.
     2) **Triple Contrato `ver_*`:** Verifica que `return v["a"] > 0` (`[VERIFIER-TAUTOLOGY-DETECTED]`), `try: ... except: return True` (`[VERIFIER-SWALLOWED-EXCEPTION]`), `raise RuntimeError("CAUGHT_5570")` (`[TPL-DEBUG-ARTIFACT]`) y `while cand in seen: cand += 0.35` (`[TPL-AD-HOC-PERTURBATION]`) son todos bloqueados deterministamente en `compile_shard.py`.
     3) **DSL `Form-C` ("Más con Menos"):** Compila una competencia `Hab-01` completa con **4 arquetipos reales** (`direct`, `inverse`, `perturbation`, `boundary_or_edge_case` atado a `assumption_id="A-Hab-01-01"`) escrita en **`<= 65` líneas** usando `fmt`, `RATS`, stems `(2 contextos, 2 preguntas)` y `ver(cand, v)` 2-arg, comprobando que el `<CID>.json` resultante pesa **`< 15 KB`** (poda AST) y emite `shard_01.cert.json`.
     4) **Verificación Simbólica `Z3`/`SymPy`:** Verifica que `ans / 3` (`ast.Div`) es atrapado por `[DIAG-MAGIC-MULT]` / `Zero_Magic_Mult_Universal` y que colisiones algebraicas fuera de las primeras semillas son detectadas simbólicamente.
     5) **Property-Based Testing (`hypothesis`):** Usa `@given(...)` de `hypothesis` (`max_examples=100`) para probar las propiedades formales de:
        - `decidir_estrategia_edicion` / Matriz 2D en `c2c_hook_guard` (cuando `affected_line_count > 5` y sin `SyntaxError`, jamás permite `write_file` monolítico y redirige a `ModularSplicing`),
        - Gobernanza síncrona de presupuesto (`turn_count > 40`, `est_tokens > 5_000_000`, `streak >= 3` siempre abortan),
        - `resolve_neuro_symbolic_verdict` en `judge.py` ($\alpha_{\text{Kernel}} = 0$: `kernel_refuted=True` jamás produce `PASS`, y `kernel_verified=True` resiste falsos `math_error` estocásticos pero respeta `epistemic_insufficiency`).
     6) **Paridad Inter-Etapa (`RejectionSpec`):** Verifica que `publish_rejection_spec.json` con `"status": "rejected"` y `"failing_shards"` desbloquea Regla B en `c2c_hook_guard.py` únicamente para el shard afectado, manteniendo bloqueados los demás shards con `pass_shard_XX.json`.

## Verificación y Entrega
```powershell
& ".venv\Scripts\python.exe" -m pytest -o addopts="" tests/test_forensic_replay_ab30cf91.py tests/test_forensic_shard06_and_variance_v34.py tests/test_sweetspot_v35_cta_and_shards.py tests/test_c2c_v40_formal_certification.py -q
```
Escribe `BRIEFING.md` antes de editar, `handoff.md` al terminar, y envía `DONE:: Stream 2C (<N> passed)` a `cbe0c4d9-d376-429c-92b2-ffaeec91ae7f`.
