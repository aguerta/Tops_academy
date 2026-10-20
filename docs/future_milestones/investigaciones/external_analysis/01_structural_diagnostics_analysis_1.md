## Diagnóstico

**La pipeline exige al LLM producir demasiada estructura, programar generadores y corregir incompatibilidades dentro de conversaciones largas.** Las optimizaciones actuales —más paralelismo, instrucciones más estrictas y escritura por bloques— alivian síntomas, pero conservan ese coste de base.

Revisé el código actual, los prompts y las auditorías históricas. Estas son las causas principales.

### 1. El contrato multiplica el output antes de generar preguntas

Por competencia se exigen:

- ≥6 plantillas: 2 MC7, 2 FIB y 2 MS.
- 3–5 variantes de enunciado por plantilla.
- Generador Python y función de comprobación.
- Pistas, solución y distractores.

Para 22 competencias eso implica **al menos 132 plantillas y 396–660 variantes de enunciado**, además del código y las explicaciones.

La parametrización ya permite generar preguntas determinísticamente, pero sigue habiendo mucha repetición en la **autoría de las plantillas**. El LLM asume simultáneamente funciones de diseñador pedagógico, programador, serializador y depurador.

**Propuesta:** introducir una representación de autoría compacta: parámetros, relación matemática, concepciones erróneas, textos pedagógicos y referencias a componentes reutilizables. Un compilador debe producir IDs, JSON, ensamblaje y estructuras repetidas. Mantener Python personalizado como extensión para casos que lo necesiten.

Referencia: [contrato de autoría](/home/vercel-sandbox/workspace/repos/github.com/aguerta/tops_academy/.agents/skills/content-to-course/system_prompts/prompt_shard_author.md).

### 2. Escribir a disco no elimina el coste de generación

Los prompts presentan `write_to_file` como protección frente al límite de output. **El contenido de los argumentos de una herramienta también lo genera el modelo y consume salida.**

Escribir un script ayuda cuando ese script expresa repetición de forma compacta. Si contiene cientos de cadenas y diccionarios redactados íntegramente, el coste persiste. Dividirlo en bloques evita truncamientos, pero añade llamadas y contexto acumulado.

Esto crea una tensión real:

- Bloques grandes: riesgo de truncamiento y repetición del trabajo.
- Bloques pequeños: más turnos y latencia.
- Shards grandes: amortizan instrucciones, pero acumulan más generación y reparación.

**Propuesta:** dimensionar bloques por **tokens de salida estimados**, con margen respecto al límite del modelo; guardar cada unidad completada y reintentar únicamente la unidad fallida. “Dos competencias” no es un presupuesto estable.

### 3. El propio contexto de autoría introduce errores

Encontré un defecto reproducible en el ejemplo MC7 que se inserta en los shards: afirma siempre que una ecuación es elíptica, aunque sus parámetros permiten un discriminante positivo.

**Ejecuté sus funciones con las 50 semillas usadas por defecto en el validador: falla su propia comprobación en 14/50 casos.** Por ejemplo, `A=3, B=7, C=4` produce discriminante `1`.

Esto proporciona al autor un patrón incorrecto que puede copiar y después tener que reparar. No demuestra que explique todos los errores históricos, pero sí una fuente concreta de fricción.

También hay contratos contradictorios: la skill describe aprovechar `corpus.md`, mientras el prompt de CTA directo prohíbe leerlo.

**Propuesta:** una única fuente de contratos que genere prompts, ejemplos y validaciones. Todos los ejemplos suministrados deben pasar las mismas comprobaciones que las plantillas reales.

Referencia: [ejemplos y particionador](/home/vercel-sandbox/workspace/repos/github.com/aguerta/tops_academy/.agents/skills/content-to-course/plan_shards.py).

### 4. El control de eficiencia depende demasiado del prompt

`dispatch.py` comunica un **“presupuesto sugerido”** de turnos. El payload de autores contiene tipo, rol, modelo y prompt; no establece ahí un límite ejecutable de turnos o salida.

El director debe seguir coordinando etapas, esperando agentes y decidiendo cuándo reparar. La complejidad operativa queda parcialmente dentro del razonamiento del LLM.

**Propuesta:** llevar ese control a una máquina de estados:

- Límites efectivos de tokens, tiempo y reintentos.
- Artefactos versionados y checkpoints.
- Validación automática al recibir una unidad.
- Reparaciones con diagnóstico y fragmento afectado.
- Escalamiento cuando se agota el presupuesto.

Las instrucciones siguen siendo útiles; el cumplimiento debe comprobarse y controlarse desde el ejecutor.

Referencia: [dispatch.py](/home/vercel-sandbox/workspace/repos/github.com/aguerta/tops_academy/.agents/skills/content-to-course/dispatch.py:460).

### 5. El paralelismo no está balanceado por trabajo esperado

El particionador calcula pesos por complejidad, pero **distribuye por cantidad de competencias contiguas**. Los pesos se registran después; no gobiernan la asignación.

Una habilidad matemática compleja puede costar mucho más que un hecho. Además, el gate global de plantillas obliga a esperar al último autor.

**Propuesta:** mantener el orden pedagógico como metadato y programar trabajos según coste estimado: output previsto, complejidad matemática y probabilidad de reparación. Usar una cola con concurrencia limitada y avanzar validaciones independientes conforme terminan unidades.

### 6. Las métricas actuales pueden conducir a optimizaciones equivocadas

La auditoría de Solow registra:

| Dato | Inconsistencia |
|---|---|
| Duración total: 832 s | Autores individuales: hasta 1962 s |
| Total: 22 competencias | Asignaciones de shards: 29 |
| Aceleración: 11,18× | Depende de duraciones que no concuerdan |

Además, sumar caché y otros tokens exige conocer la semántica del proveedor; ese total no equivale automáticamente a coste económico.

**No usaría esas cifras para prometer porcentajes de mejora.** Los reportes sugieren muchos turnos y reparaciones, pero no constituyen un benchmark fiable.

Referencia: [auditoría histórica](/home/vercel-sandbox/workspace/repos/github.com/aguerta/tops_academy/reports/c2c_audits/20261013_002234_solow_growth_model_c4802280/report.md).

## Qué haría primero

1. **Corregir ejemplos, contradicciones y telemetría.** Es la base para reducir errores evitables y medir correctamente.
2. **Reducir el contrato de salida mediante compilación y reutilización.** Aquí veo el mayor potencial estructural.
3. **Implementar ejecución con presupuestos y reparación incremental.**
4. **Ajustar tamaño de tareas y modelos mediante experimentos comparables.** Un modelo rápido puede resultar más lento en total si provoca más reparaciones.

Mediría **tokens de salida por plantilla aceptada, aceptación al primer intento, tokens gastados en reparación y latencia total p50/p95**, manteniendo cobertura y calidad pedagógica. Preguntas por minuto puede mejorar simplemente generando más variantes.

Finalmente, conservaría la evaluación independiente: hoy se muestrean dos preguntas por competencia, lo que no garantiza cubrir los tres formatos ni todas las plantillas. La optimización debe demostrar calidad equivalente.

**Mi prioridad sería reducir cuánto debe inventar y serializar el modelo en cada unidad de trabajo.** Después optimizaría el paralelismo.

No modifiqué el repositorio ni ejecuté una generación completa; la comprobación nueva fue la reproducción del fallo del ejemplo y la revisión de consistencia de la telemetría.