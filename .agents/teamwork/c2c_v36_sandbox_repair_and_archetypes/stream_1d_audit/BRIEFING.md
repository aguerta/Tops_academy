# BRIEFING — Stream 1D (Fase 3: Auditor Forense `audit_1d`)

## 1. Misión del Auditor
Auditar de manera independiente y forense la implementación y mejoras introducidas en el Stream 1D:
- **Objetivo:** Blindaje de la compuerta semántica `[M3-ARCHETYPES]` en `compile_shard.py`, soporte modular limpio de parches `shard_fixes/<CID>.py`, actualización canónica de prompts de autor (`prompt_shard_author.md` y `lean/prompt_shard_author.md`) y suite de tests en `tests/test_m3_archetypes_semantic_gate.py`.
- **Fase previa revisada:**
  - `stream_1d_impl/handoff.md`: Implementación base de detección de stems clonados, AST checks para `arch` en generadores y prompts canónicos.
  - `stream_1d_impr/handoff.md`: Hardening contra evasión trivial (`_ = arch`, clones matemáticos con `(correct, vars)` idénticos) y soporte modular por competencia para parches sin falsos positivos de shards base rotos.

## 2. Puntos Críticos a Auditar
1. **Compuerta `[M3-ARCHETYPES]` en `compile_shard.py`**:
   - Detección de stems clonados (`distinct_stems < min(eff_min_arch, len(tpls))`).
   - Detección estática en AST de funciones generadoras que declaran `arch` pero no lo usan legítimamente en el cuerpo (rechazo de `_ = arch`, `arch == arch`, etc.).
   - Detección dinámica en sandbox de clones matemáticos (evaluación con `seed=100` y `seed=101` para verificar varianza en `(correct, vars)`).
   - Aislamiento modular de `shard_fixes/<CID>.py` para evitar falsos positivos por código base obsoleto.
2. **Prompts de Autor**:
   - Ejemplo Canónico H-01 en `prompt_shard_author.md` y `lean/prompt_shard_author.md` con 4 arquetipos activos (`arch == 1, 2, 3, 4`) y 4 listas independientes de stems (`stems_h01_1..4`).
3. **Calidad de Tests Unitarios**:
   - Inspección de `tests/test_m3_archetypes_semantic_gate.py` verificando que no existan aserciones vacías ni falsos positivos.
4. **Ejecución Independiente de Tests**:
   - Ejecución de la suite completa requerida mediante pytest en `.venv`.
