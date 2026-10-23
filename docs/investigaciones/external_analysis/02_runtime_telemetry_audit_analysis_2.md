## Diagnóstico principal

**La pipeline acumula demasiado trabajo generativo y demasiados ciclos de reparación en etapas que se esperan entre sí.** El paralelismo actual reduce parte del tiempo, pero cada autor sigue ejecutando una tarea serial muy grande.

Además, **el supuesto resultado de 13,9 minutos está mal medido**.

[Informe completo con evidencias y propuestas](outputs/c2c-performance/diagnostico.md) · [Cálculos reproducibles](outputs/c2c-performance/reconstruction.json)

## 1. Primero: no está demostrado que ya haya bajado de 20 minutos

| Corrida | Reportado | Lo que sostienen los timestamps |
|---|---:|---|
| `e8ab9fd6` | 61,9 min | Intervalo consistente de **61,9 min** |
| `c4802280` | 13,9 min | **Al menos 46,6 min observados**, sin publicación final acreditada |

En la segunda, el registro del orquestador termina justo cuando comienzan los autores. Estos continúan **32,7 minutos adicionales**. El auditor calcula el tiempo global sólo con el intervalo del padre.

También encontré que:

- El **95,8 % de tiempo en inferencia** es una constante del generador de reportes.
- El ahorro de **más del 55 % por usar shards grandes** aparece como texto fijo.
- El auditor puede declarar «jueces perfectos al primer intento» **sin ningún juez registrado**.
- La segunda corrida declara 22 competencias, pero sus shards asignan **29 distintas**.

Por tanto, esos indicadores no sirven todavía para demostrar mejoras.

## 2. Dónde se van realmente los minutos

La corrida de 61,9 minutos permite reconstruir esta ruta:

| Etapa | Tiempo |
|---|---:|
| Preparación e intervalos entre etapas/cola final | 6,6 min |
| CTA | **20,8 min** |
| Autoría paralela —manda el último autor— | **28,0 min** |
| Jueces | 6,6 min |
| **Total** | **61,9 min** |

**CTA y autoría concentran el 78,8 % del tiempo. Cada una supera por sí sola el presupuesto completo.**

## 3. Las causas raíces

### A. Cada autor construye demasiadas piezas desde cero

El contrato exige al menos **seis plantillas por competencia**, con código generador, distractores, variantes, pistas y soluciones.

Para 22 competencias son **132 plantillas como mínimo**. Un shard de ocho concentra **48 plantillas en un solo agente**.

Pedir «escríbelo en un único script» reduce llamadas, pero no elimina ese volumen de trabajo ni sus errores.

**Cambio necesario:** trasladar escaping, estructura, opciones, identificadores y ensamblado a constructores deterministas. Reservar al modelo el contenido matemático y pedagógico específico.

### B. Las reparaciones multiplican los intercambios

En la primera corrida, los autores acumularon:

- **226 turnos**.
- **81 ejecuciones de checks**.
- **43 checks fallidos**.

Los errores repetidos incluyen diversidad, variables sin sustituir y sintaxis matemática. En la siguiente corrida, los autores llegan a **468 turnos**.

El código actual ya incorpora mensajes prescriptivos y comprobación de paridad. La siguiente mejora debe ser **reparación localizada, diagnóstico agrupado y reutilización de resultados válidos**, evitando reconstruir todo el lote.

### C. La CTA sigue siendo una barrera serial costosa

Pasó de **20,8 a 11,4 minutos**, pero continúa consumiendo una parte enorme del presupuesto. Hubo truncamiento de salida y posterior reescritura.

**Cambio necesario:** artefactos incrementales, bloques pequeños y contratos estables. Comparar CTA directa con análisis por secciones; no asumir que añadir agentes siempre acelera.

### D. El reparto no optimiza la duración

El planner calcula pesos de competencias, pero reparte principalmente por **cantidad y orden consecutivo**, sin utilizarlos para equilibrar la asignación.

En la corrida reciente, **todos los autores duran entre 31,6 y 32,7 minutos**. El problema ya no es un único rezagado.

**Cambio necesario:** experimentar con tamaños de tarea y reparto por complejidad, usando la concurrencia realmente disponible.

### E. Los presupuestos son sugerencias

El código actual comunica **25 turnos sugeridos**; no implementa un deadline efectivo de ejecución. Tampoco puede garantizar mediante texto que el agente deje de navegar, reparar o explorar.

**Cambio necesario:** límites y checkpoints en el orquestador real, con estados explícitos de incompleto; nunca publicar sin validación para cumplir el reloj.

## 4. Qué priorizaría

1. **Corregir la telemetría:** medir hasta publicación validada, incluyendo hijos y reintentos.
2. **Reducir el trabajo generativo por plantilla.**
3. **Reducir reparaciones y regeneración innecesaria.**
4. **Optimizar CTA y reparto mediante experimentos comparables.**
5. Después, optimizar validación local, jueces y entorno.

Para pasar de 61,9 a 20 minutos hace falta reducir **un 67,7 %** del tiempo. Incluso haciendo que el autor más lento alcance la mediana y que el juez lento iguale al rápido, quedarían **49,9 minutos**.

**Conclusión:** llegar a menos de 20 minutos requiere reducir sustancialmente el trabajo de CTA y autoría. Ajustar únicamente paralelismo, prompts o velocidad de Python no alcanza según estos registros.