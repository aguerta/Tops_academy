---
name: flash-duet-orchestrator
description: Orquesta refactorizaciones o implementaciones complejas mediante etapas secuenciales (Gates) en modo Flash Duet por defecto (Implementador -> Editor) o Flash Triad bajo solicitud explícita (Implementador -> Editor -> Auditor), instanciando los subagentes con Model="inherit", fronteras de escritura 100% disjuntas, Pre-Flight obligatorio, escalamiento BLOCKER Tier A/B y Orquestador Dispatch-Only.
---

# Flash Duet Orchestrator

Usa esta skill cuando el usuario solicite ejecutar un plan de ingeniería complejo con alta paralelización, control estricto de calidad y mínimo consumo de contexto en la conversación principal.

- **Modo por defecto (`Flash Duet`):** `Implementador -> Editor` (2 fases por stream).
- **Modo explícito (`Flash Triad`):** `Implementador -> Editor -> Auditor` (3 fases por stream). **Solo** se activa si el usuario solicita explícitamente usar *Flash Triad*.

## 1. Arquitectura de Roles

1. **Orquestador Principal (*Dispatch-Only & Escalation Resolver*):**
   - No edita código de producción directamente; mantiene únicamente `.agents/teamwork/<project>/{ORIGINAL_REQUEST.md,plan.md,GATE_STATUS.md}` y los `DISPATCH.md` de cada fase.
   - Define los subagentes de sesión vía `define_subagent`:
     - En **Flash Duet (default)**: `<prefix>_implementer` (`EnableWriteTools=True`) y `<prefix>_editor` (`EnableWriteTools=True`).
     - En **Flash Triad (solo explícito)**: añade `<prefix>_auditor` (`EnableWriteTools=True` restringido exclusivamente a su carpeta `stream_XX_audit/`).
   - Al instanciar los subagentes vía `invoke_subagent`, lanza todos los workers con `Model="inherit"` y aplica **Barrera Reactiva Silenciosa** mientras espera cierres de etapa.

2. **Particionado en Etapas (*Gates*) con Fronteras Disjuntas:**
   - Agrupa tareas en etapas secuenciales (`Stage 1 -> Stage 2 -> Stage 3`) solo cuando exista dependencia real de prerrequisito.
   - Dentro de una misma etapa, cada stream paralelo (`1A`, `1B`, ...) recibe un conjunto **100% disjunto** de archivos permitidos de escritura (`Exclusive Write Boundaries`).

3. **Flujo por Stream (`Model="inherit"`):**
   - **Fase 1 — Implementador (`<prefix>_implementer`):**
     - **Paso 0 (*Pre-Flight Sanity Check* obligatorio):** Lee los archivos reales y pruebas existentes antes de editar, y escribe `BRIEFING.md`.
     - **Protocolo `BLOCKER::` de 2 Niveles:** Si descubre que el código o un test fuera de su frontera contradice o bloquea la orden, detiene ediciones y envía `BLOCKER:: <archivo:línea> | <causa> | <opciones>` vía `send_message`:
       - *Tier A (conciliación técnica dentro del diseño aprobado):* El Orquestador resuelve y autoriza ajuste de frontera si no hay solapamiento.
       - *Tier B (cambio de alcance, ambigüedad de negocio o bloqueo del entorno vivo):* El Orquestador escala al Usuario antes de continuar.
     - Implementa, ejecuta `pytest` focalizado, escribe `handoff.md` y envía `DONE::`.
   - **Fase 2 — Editor (`<prefix>_editor`):**
     - Revisa `handoff.md` del Implementador, endurece casos borde, contratos entre streams (rutas Windows/POSIX, esquemas JSON, rendimiento) y amplía tests adversarios sin *scope creep*.
     - En **Flash Duet (default)**, además valida que el diff respeta la frontera exclusiva (cero scripts temporales o *lockfiles* residuales), ejecuta `pytest` final y cierra el stream con `DONE::`.
   - **Fase 3 — Auditor Forense (`<prefix>_auditor`, *Read-Only* en producción — solo en modo `Flash Triad` explícito):**
     - Verifica `git status` / `git diff` contra la frontera exclusiva (cero scripts temporales o *lockfiles* residuales).
     - Inspecciona tests contra falsos positivos o aserciones enmascaradas, ejecuta `pytest` de forma independiente y emite `PASS::` o `REJECT:: <archivo:línea>` (disparando remediación focalizada en el Editor y re-auditoría antes de cruzar el *Gate*).
