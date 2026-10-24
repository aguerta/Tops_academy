# Pre-Flight Briefing — Stream 1C (Fase 3: Auditor Forense `audit_1c`)

- **Subagente:** Auditor Forense Stream 1C (`audit_1c`)
- **Fase:** Fase 3 (Auditor Forense)
- **Fecha:** 2026-10-24
- **Orquestador Conversation ID:** `526cfac0-d37b-49c9-bf09-00b5c520add2`

## 1. Contexto y Objetivos Recibidos
Se recibieron y analizaron los handoffs de Fase 1 (`impl_1c`) y Fase 2 (`impr_1c`).
Objetivos a auditar forensemente:
1. **Inyección Turn-0 en `dispatch.py` (`dispatch_authors`):**
   - Inyección de `correct_belief`, `manifestation`, `remediation_hint` y distractores de `cta.json`.
   - Directriz explícita Turn-0 autosuficiente (prohibición de leer PDFs en Turno 1).
   - Especificación de 4 arquetipos disjuntos del Milestone 3 en formato DRY compacto de distractores.
   - Cero hardcoding de cursos o dominios específicos.
2. **Resiliencia en `dispatch_repair` (`dispatch.py`):**
   - Limpieza exhaustiva de `pass_<shard_id>.json` y variantes de contador (`.check_attempts/`).
3. **System Prompts de Autor y Reparación (Full + Lean):**
   - `lean/prompt_shard_author.md` <= 4,750 bytes y <= 5,120 bytes.
   - `lean/prompt_repair.md` <= 5,000 bytes.
   - 100% sintaxis Python AST válida en snippets de código.
   - Coherencia de los 4 arquetipos disjuntos, formato DRY y corte inmediato Post-PASS.
4. **Batería de Tests Unitarios:**
   - Auditoría de `tests/test_dispatch_turn0_and_milestone3_prompts.py` verificando ausencia de falsos positivos, tests vacíos o aserciones triviales/debilitadas.
   - Ejecución independiente de pytest.
5. **Aislamiento de Frontera:**
   - Garantizar que los cambios del Stream 1C no contaminen otros streams ni archivos fuera de su frontera.
