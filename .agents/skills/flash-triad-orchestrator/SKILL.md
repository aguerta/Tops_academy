---
name: flash-triad-orchestrator
description: Orquesta refactorizaciones o implementaciones complejas mediante etapas secuenciales (Gates) de tríadas paralelas en Model="flash" (Implementador -> Mejorador -> Auditor) con fronteras de escritura 100% disjuntas, Pre-Flight obligatorio, escalamiento BLOCKER Tier A/B y Orquestador Dispatch-Only.
---

# Flash Triad Orchestrator (`Implementador -> Mejorador -> Auditor`)

Usa esta skill cuando el usuario solicite ejecutar un plan de ingeniería complejo con alta paralelización, control estricto de calidad y mínimo consumo de contexto en la conversación principal.

## 1. Arquitectura de Roles

1. **Orquestador Principal (*Dispatch-Only & Escalation Resolver*):**
   - No edita código de producción directamente; mantiene únicamente `.agents/teamwork/<project>/{ORIGINAL_REQUEST.md,plan.md,GATE_STATUS.md}` y los `DISPATCH.md` de cada fase.
   - Define 3 subagentes de sesión vía `define_subagent`: `<prefix>_implementer` (`EnableWriteTools=True`), `<prefix>_improver` (`EnableWriteTools=True`) y `<prefix>_auditor` (`EnableWriteTools=True` restringido exclusivamente a su carpeta `stream_XX_audit/`).
   - Lanza todos los workers con `Model="flash"` y aplica **Barrera Reactiva Silenciosa** mientras espera cierres de etapa.

2. **Particionado en Etapas (*Gates*) con Fronteras Disjuntas:**
   - Agrupa tareas en etapas secuenciales (`Stage 1 -> Stage 2 -> Stage 3`) solo cuando exista dependencia real de prerrequisito.
   - Dentro de una misma etapa, cada stream paralelo (`1A`, `1B`, ...) recibe un conjunto **100% disjunto** de archivos permitidos de escritura (`Exclusive Write Boundaries`).

3. **Tríada por Stream (`Model="flash"`):**
   - **Fase 1 — Implementador:**
     - **Paso 0 (*Pre-Flight Sanity Check* obligatorio):** Lee los archivos reales y pruebas existentes antes de editar, y escribe `BRIEFING.md`.
     - **Protocolo `BLOCKER::` de 2 Niveles:** Si descubre que el código o un test fuera de su frontera contradice o bloquea la orden, detiene ediciones y envía `BLOCKER:: <archivo:línea> | <causa> | <opciones>` vía `send_message`:
       - *Tier A (conciliación técnica dentro del diseño aprobado):* El Orquestador resuelve y autoriza ajuste de frontera si no hay solapamiento.
       - *Tier B (cambio de alcance, ambigüedad de negocio o bloqueo del entorno vivo):* El Orquestador escala al Usuario antes de continuar.
     - Implementa, ejecuta `pytest` focalizado, escribe `handoff.md` y envía `DONE::`.
   - **Fase 2 — Mejorador:**
     - Revisa `handoff.md` del Implementador, endurece casos borde, contratos entre streams (rutas Windows/POSIX, esquemas JSON, rendimiento) y amplía tests adversarios sin *scope creep*.
   - **Fase 3 — Auditor Forense (*Read-Only* en producción):**
     - Verifica `git status` / `git diff` contra la frontera exclusiva (cero scripts temporales o *lockfiles* residuales).
     - Inspecciona tests contra falsos positivos o aserciones enmascaradas, ejecuta `pytest` de forma independiente y emite `PASS::` o `REJECT:: <archivo:línea>` (disparando remediación focalizada en el Mejorador y re-auditoría antes de cruzar el *Gate*).
