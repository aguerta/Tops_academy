---
name: c2c-run-auditor
description: >-
  Audita detalladamente cualquier ejecución de Content to Course u orquestaciones multi-agente
  en Google Antigravity SDK. Extrae telemetría ultra-granular de tokens (input, output, cache,
  thinking) por subagente y por turno, latencias, descomposición de llamadas a herramientas,
  detección de cuellos de botella (camino crítico y stragglers), perfilado de la carga de entrada
  (páginas, diapositivas, peso en MB) y mantiene un registro histórico persistente con métricas
  unitarias normalizadas (tokens/pregunta, seg/pregunta, throughput).
triggers:
  - "auditar run de content to course"
  - "auditar conversacion"
  - "audit c2c run"
  - "profile workflow"
  - "analizar bottlenecks"
  - "telemetria de tokens por subagente"
  - "auditar rendimiento de c2c"
  - "comparar performance de cursos"
inputs:
  target:
    type: string
    description: ID o prefijo de la conversación (UUID), enlace de chat markdown, ruta a transcript.jsonl, slug del curso o 'recent' para selección interactiva.
    required: false
  output_dir:
    type: string
    description: Carpeta destino para almacenar los reportes persistentes (default 'reports/c2c_audits').
    default: reports/c2c_audits
  work_dir:
    type: string
    description: Carpeta de trabajo intermedia del curso si no es la estándar 'work/' (opcional).
    required: false
  format:
    type: string
    description: Formatos a generar ('all', 'md', 'json', 'html').
    default: all
outputs:
  report_file:
    type: string
    description: Ruta absoluta al informe Markdown detallado de la corrida.
  telemetry_file:
    type: string
    description: Ruta al archivo JSON con el árbol y telemetría granular de todos los agentes.
  dashboard_file:
    type: string
    description: Ruta al dashboard HTML interactivo con visualización de línea de tiempo y métricas.
  registry_file:
    type: string
    description: Ruta al registro histórico consolidado de auditorías (audit_registry.json).
  benchmark_file:
    type: string
    description: Ruta al tablero comparativo longitudinal en Markdown (historical_benchmark.md).
---

# C2C Run Auditor Skill (Google Antigravity SDK Telemetry & Optimization Engine)

Herramienta de auditoría forense y análisis de rendimiento para pipelines de orquestación multi-agente en Antigravity, especializada en **Content-to-Course**. Permite a ingenieros de prompts y optimizadores de workflows inspeccionar cualquier corrida con máxima granularidad, evaluar cuellos de botella y registrar la evolución de eficiencia del sistema a lo largo del tiempo.

---

## 1. Arquitectura de Telemetría y Persistencia

```mermaid
flowchart TD
    User["Invocación: Target (UUID, Chat Link, Curso o 'recent')"] --> Resolver["1. Target Resolver"]
    Resolver --> Parser["2. Transcript Parser (< 400 ms)\n(Stream de transcript.jsonl del Director y de cada Subagente)"]
    
    subgraph Engine ["scripts/audit_engine.py"]
        Parser --> Workload["3. Workload Profiler\n- Archivos fuente originales & peso (MB)\n- Páginas / Slides (PyMuPDF / budget.json)\n- Handouts, Competencias & Preguntas"]
        Workload --> Metrics["4. Granular Metrics Computer\n- Tokens: In / Out / Cache / Thinking\n- Tiempos: Inferencia vs Tools vs Espera\n- Turnos y desglose de herramientas"]
        Metrics --> Stages["5. Stage Classifier (Etapas 0 a 6 C2C)"]
        Stages --> Bottlenecks["6. Bottleneck & Straggler Analyzer\n- Identificación de Camino Crítico\n- Desviaciones > 1.5x mediana\n- Inflación de contexto & fallos en tools"]
        Bottlenecks --> UnitEcon["7. Unit Economics Normalizados\n(Tokens/Pregunta, Seg/Pregunta, Preg/Minuto)"]
    end
    
    UnitEcon --> Persistence["8. Repositorio Persistente (reports/c2c_audits/)"]
    Persistence --> RunDir["reports/c2c_audits/<timestamp>_<course>_<id>/"]
    RunDir --> RepMD["report.md (Informe Ejecutivo & Forense)"]
    RunDir --> TelJSON["telemetry.json (Dataset completo en JSON)"]
    RunDir --> DashHTML["dashboard.html (Dashboard interactivo autónomo)"]
    
    Persistence --> Registry["Registro Histórico Longitudinal"]
    Registry --> RegJSON["audit_registry.json (Índice acumulativo de todas las corridas)"]
    Registry --> BenchMD["historical_benchmark.md (Matriz comparativa de evolución temporal)"]
```

---

## 2. Protocolo de Ejecución del Agente

> [!IMPORTANT]
> **Invocación Determinista Directa (< 5 segundos):** El motor `audit_engine.py` es completamente autónomo y resiliente. NO ejecutes scripts manuales en `scratch/` ni inspecciones intermedias de transcripciones. Ejecuta el CLI directamente en el primer turno.

Cuando el usuario solicita auditar una corrida, el agente debe seguir estos pasos deterministas:

### Paso 1: Resolver y Ejecutar Directamente
- Para auditoría ejecutiva de telemetría, unit economics y dashboard:
  ```bash
  python .agents/skills/c2c-run-auditor/scripts/audit_engine.py --conversation <ID_O_ENLACE>
  ```
- Para auditoría integral completa con **Traceback Deep-Dive** (turnos de subagentes, bottlenecks de CTA/shards, fugas web de jueces y taxonomía de errores):
  ```bash
  python .agents/skills/c2c-run-auditor/scripts/audit_engine.py --conversation <ID_O_ENLACE> --traceback
  ```
- Para análisis forense granular directo de traceback exclusivamente:
  ```bash
  python .agents/skills/c2c-run-auditor/scripts/traceback_analyzer.py --conversation <ID_O_ENLACE>
  ```
- Si el usuario no especificó ID o solicita ver las corridas recientes:
  ```bash
  python .agents/skills/c2c-run-auditor/scripts/audit_engine.py --recent
  ```

### Paso 2: Resiliencia y Deduplicación Canónica
El motor maneja de forma autónoma:
1. **Auto-descubrimiento estructurado de subagentes:** Extrae roles y tipos de los JSON de `manage_subagents` y headers `# Asignación de Tarea para <Rol>`, mapeando cada shard de visión, CTA y autoría.
2. **Resiliencia post-publicación:** Si la carpeta temporal `work/` ya fue eliminada, el motor resuelve el curso publicado en `courses/<course_id>.json` (preguntas validadas), reconstruye la carga desde logs y calcula unit economics sin errores.
3. **Deduplicación canónica por corrida:** Mantiene estrictamente **1 sola entrada por conversación** en `audit_registry.json` y `historical_benchmark.md`, reemplazando automáticamente auditorías preliminares y evitando duplicados artificiales.

### Paso 3: Presentar el Resumen Ejecutivo Inmediato
Inmediatamente tras la ejecución del CLI (< 1.5s), el agente lee el `report.md` emitido y presenta al usuario:
- **Ficha de Carga (Workload Context)**: Cuántas páginas/slides, archivos fuente y preguntas/competencias se procesaron.
- **Métricas Clave de Rendimiento**:
  - Tiempo de pared (*wall-clock*) y factor de aceleración (*speedup*).
  - Tokens totales y densidad normalizada: **Tokens por pregunta** y **Segundos por pregunta**.
- **Diagnóstico Principal de Cuellos de Botella**:
  - Identificar si hubo subagentes *stragglers* (rezagados).
  - Reportar exceso de turnos o errores en herramientas.
- **Dictamen de Blind Judges (Verificación Ciega)**:
  - Indicar explícitamente si el lote estratificado pasó 100% perfecto al primer intento sin discrepancias.
  - En caso contrario, catalogar detalladamente las acciones tomadas: fallos psicométricos iniciales (R-18/R-19), rondas de auto-reparación e intervenciones directas del supervisor.
- **Enlaces Clicables**:
  - Enlace al informe Markdown generado: `[report.md](file:///.../report.md)`
  - Enlace al dashboard HTML: `[dashboard.html](file:///.../dashboard.html)`
  - Enlace a la evolución histórica: `[historical_benchmark.md](file:///.../historical_benchmark.md)`

---

## 3. Guía de Interpretación de Unit Economics

Para comparar justamente corridas de diferente tamaño y complejidad pedagógica:

| Métrica | Definición | Interpretación Óptima | Alerta / Anomalía |
| :--- | :--- | :--- | :--- |
| **Tokens / Pregunta** | $\frac{\text{Tokens Totales}}{\text{Preguntas Finales}}$ | 15,000 – 35,000 tokens/preg | $> 50,000$: Prompts sobrecargados o bucles de reescritura |
| **Segundos / Pregunta** | $\frac{\text{Segundos de Pared}}{\text{Preguntas Finales}}$ | 2 – 5 s/preg | $> 10$ s/preg: Straggler en barrera o validaciones lentas |
| **Throughput (QPM)** | $\frac{\text{Preguntas} \times 60}{\text{Segundos de Pared}}$ | 12 – 30 preguntas/min | $< 6$ preg/min: Cuello de botella en etapa de autores |
| **Speedup Concurrente** | $\frac{\text{Tiempo Cómputo}}{\text{Tiempo Pared}}$ | $> 2.5\times$ en fan-out de autores | $\approx 1.0\times$: Subagentes operando de forma secuencial |
| **Tokens / Página** | $\frac{\text{Tokens Totales}}{\text{Páginas Fuente}}$ | $30,000 – 80,000$ tokens/pág | $> 200,000$: Lectura redundante de corpus o transcripción dispersa |

---

## 4. Opciones de los CLIs del Sistema

### 4.1. CLI Global: `audit_engine.py`
```text
Uso: audit_engine.py [-h] [--conversation CONVERSATION] [--output-dir OUTPUT_DIR]
                     [--work-dir WORK_DIR] [--format {all,md,json,html}]
                     [--recent] [--history] [--compare [RUN_A] [RUN_B]]
                     [--traceback]

Opciones:
  -c, --conversation   UUID, chat link o ruta al transcript del orquestador.
  -o, --output-dir     Directorio raíz para los reportes (default: reports/c2c_audits).
  -w, --work-dir       Directorio de trabajo con artefactos intermedios del run.
  --recent             Muestra las ejecuciones recientes de C2C en el brain.
  --history            Muestra el histórico comparativo y matriz longitudinal.
  --compare            Genera la comparativa forense entre dos corridas (o versus baseline).
  --traceback          Ejecuta además el análisis forense profundo de traceback en la misma corrida.
  --format             Formatos a emitir: all, md, json, html.
```

### 4.2. CLI de Traceback Granular: `traceback_analyzer.py`
```text
Uso: traceback_analyzer.py [-h] [-c CONVERSATION] [-o OUTPUT_DIR] [--recent]

Opciones:
  -c, --conversation   UUID, chat link o ruta al transcript del orquestador.
  -o, --output-dir     Directorio raíz para los reportes (default: reports/c2c_audits).
  --recent             Muestra las conversaciones recientes encontradas en el brain.
```

