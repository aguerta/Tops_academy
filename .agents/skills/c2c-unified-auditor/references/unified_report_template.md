# Contrato de Estructura: Reporte Unificado de Calidad y Rendimiento

El reporte consolidado emitido por la skill `c2c-unified-auditor` debe guardarse obligatoriamente en:
`reports/c2c_audits/merged_quality_and_performance_<course_id>.md`
y replicarse en:
`reports/audits_archive/<course_id>/merged_quality_and_performance.md`.

---

## Estructura Jerárquica Obligatoria y Anclas de la Tabla de Contenidos

El reporte debe incluir de forma explícita y al inicio la **Tabla de Contenidos** con los enlaces ancla exactos para navegación fluida en Markdown:

```markdown
# Reporte Unificado de Auditoría Integral: Calidad Pedagógica, Telemetría Forense y Rendimiento Multi-Agente
## Curso: [Título del Curso] (`[course_id]`)
### Plataforma Top's Academy — Pipeline Content-to-Course (C2C) v2

---

**Fecha de Consolidación:** [Fecha]  
**Identificador del Curso:** `[course_id]`  
**Conversación Orquestadora Auditada:** [`[conv_id]`](conversation://[conv_id])  
**Auditores:** Course QA Auditor & C2C Traceback Auditor (Top's Academy / Google Antigravity SDK)  
**Marco Normativo de Evaluación:** Quality Matters (QM), OSCQR, Mastery Learning y Telemetría Isomórfica Antigravity  
**Veredicto Final de Calidad:** **[Score] / 20.0 pts ([TIER]) — APROBADO PARA PRODUCCIÓN INMEDIATA**  
**Tiempo de Pared Global:** **[WallMin] minutos** | **Cómputo Total de Agentes:** **[CompMin] minutos** | **Speedup:** **[Speedup]x**  

---

## Tabla de Contenidos

- [PARTE I: AUDITORÍA TÉCNICA Y PEDAGÓGICA DE CALIDAD INSTRUCCIONAL (QA EVALUATOR)](#parte-i-auditoría-técnica-y-pedagógica-de-calidad-instruccional-qa-evaluator)
  - [1. Resumen Ejecutivo de Calidad Pedagógica](#1-resumen-ejecutivo-de-calidad-pedagógica)
  - [2. Desglose y Calificación por Dimensiones Normativas](#2-desglose-y-calificación-por-dimensiones-normativas)
  - [3. Análisis Cualitativo Detallado por Dimensión de Calidad](#3-análisis-cualitativo-detallado-por-dimensión-de-calidad)
    - [Dimensión 1: Arquitectura y Granularidad](#dimensión-1-arquitectura-y-granularidad)
    - [Dimensión 2: Calidad de Evaluación y Reactivos](#dimensión-2-calidad-de-evaluación-y-reactivos)
    - [Dimensión 3: Andamiaje y Feedback Progresivo](#dimensión-3-andamiaje-y-feedback-progresivo)
    - [Dimensión 4: Alineación Instruccional](#dimensión-4-alineación-instruccional)
    - [Dimensión 5: Accesibilidad y Ergonomía Técnica / KaTeX](#dimensión-5-accesibilidad-y-ergonomía-técnica--katex)
  - [4. Loop de Verificación Semántica sobre Muestras Estratificadas](#4-loop-de-verificación-semántica-sobre-muestras-estratificadas)
  - [5. Registro de Nuevas Reglas de Linting (`discovered_lint_rules`)](#5-registro-de-nuevas-reglas-de-linting-discovered_lint_rules)
- [PARTE II: AUDITORÍA FORENSE DE RENDIMIENTO, TELEMETRÍA Y BOTTLENECKS (RUN AUDITOR)](#parte-ii-auditoría-forense-de-rendimiento-telemetría-y-bottlenecks-run-auditor)
  - [6. Consolidación de Métricas de Rendimiento y Ratios Unitarios](#6-consolidación-de-métricas-de-rendimiento-y-ratios-unitarios)
  - [7. Descomposición Empírica del Tiempo: Inferencia LLM vs. Ejecución de Herramientas](#7-descomposición-empírica-del-tiempo-inferencia-llm-vs-ejecución-de-herramientas)
  - [8. Causa Raíz de la Latencia por Etapa](#8-causa-raíz-de-la-latencia-por-etapa)
    - [8.1. Direct CTA Architect](#81-direct-cta-architect)
    - [8.2. Shards de Autoría y el Fenómeno Straggler](#82-shards-de-autoría-y-el-fenómeno-straggler)
    - [8.3. Blind Judges y Llamadas Externas (Stage 5)](#83-blind-judges-y-llamadas-externas-stage-5)
    - [8.4. Fricción del Orquestador y Etapa de Publicación](#84-fricción-del-orquestador-y-etapa-de-publicación)
  - [9. Taxonomía Consolidada de Errores y Retrabajo](#9-taxonomía-consolidada-de-errores-y-retrabajo)
  - [10. Conclusión y Síntesis Global](#10-conclusión-y-síntesis-global)
```

---

## Contenido de las Secciones

### Parte I: Auditoría Técnica y Pedagógica (QA Evaluator)
1. **Resumen Ejecutivo:** Tabla resumen con total de competencias, reactivos, modelado DAG, cobertura de rationales, ausencia de telltales, andamiaje socrático, sintaxis KaTeX y puntaje final certificado.
2. **Desglose de Dimensiones:** Gráfico Mermaid `xychart-beta` con barras de puntuación obtenida vs. líneas de puntuación máxima y tabla de desglose.
3. **Análisis Cualitativo:** Evaluación detallada de cada una de las 5 dimensiones pedagógicas con estándares institucionales y hallazgos empíricos.
4. **Verificación Semántica:** Muestras de control representativas por competencia evaluadas en rigor matemático y conceptual.
5. **Nuevas Reglas de Linting:** Registro formal de patrones detectados para retroalimentar el catálogo de linters de la plataforma.

### Parte II: Auditoría Forense de Rendimiento (Run Auditor)
6. **Métricas de Rendimiento y Unit Economics:** Tabla exhaustiva de material de entrada, tokens (entrada, salida, caché, activos), tiempos de pared, tiempos de cómputo, speedup y ratios unitarios (tokens/pregunta, seg/pregunta, QPM).
7. **Descomposición Empírica:** Distribución porcentual y diagrama ASCII de tiempo LLM (inferencia + thinking) frente a tiempo de herramientas locales (I/O, Python, consola).
8. **Causa Raíz por Etapa:** Análisis forense pormenorizado del Direct CTA, autores de shards (stragglers), jueces ciegos y barreras del orquestador.
9. **Taxonomía Consolidada de Errores:** Tabla taxonómica categorizada con frecuencias, agentes involucrados y causas raíz.
10. **Conclusión y Síntesis Global:** Veredicto final integrado, diagnóstico del cuello de botella y recomendaciones operativas.
