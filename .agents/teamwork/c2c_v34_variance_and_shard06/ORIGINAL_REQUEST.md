# Solicitud Original y Acuerdos de Diseño (`c2c_v34_variance_and_shard06`)

1. **Objetivo:** Resolver de raíz la falla de compilación y reparación en `shard_06` (`Hab-06`: corrupción regex en `sanitize_katex_syntax` y sobreescritura silenciosa de `error_rationale` en `assemble_question`) y eliminar todas las causas estructurales de varianza temporal entre shards (3.8 min vs 9–11 min).
2. **Invariantes Inviolables:**
   - **Preservación estricta del Milestone 3 (`FUTURE_MILESTONES.md` y `plan_shards.py`):** Mantener los **4 arquetipos disjuntos por competencia** (*1. Directo/Frontal, 2. Inverso/Diagnóstico, 3. Perturbación/Estática Comparativa, 4. Frontera/Casos Límite*). La reducción de varianza se logra mediante herencia DRY de `error_rationale` desde `cta.json` en `compile_shard.py` e inyección completa de fórmulas en Turno 0, **nunca** reduciendo el número de plantillas por competencia.
   - **100% Agnóstico al Dominio:** Ningún archivo de producción puede contener lógica ni referencias hardcodeadas a un curso o libro específico (como Greene o teoría asintótica); todo aplica genéricamente a cualquier material en `content/`.
   - **Alcance de Verificación:** No ejecutar la corrida completa del curso `asyntotic_estatistics_v4`; validar compilando limpiamente `shard_06_data.py` (`--strict`, 0 errores) y pasando toda la suite `pytest`.
3. **Orquestación:** `/flash-triad-orchestrator` (`Implementador -> Mejorador -> Auditor` en `Model="flash"`) con fronteras de escritura 100% disjuntas por etapa.
