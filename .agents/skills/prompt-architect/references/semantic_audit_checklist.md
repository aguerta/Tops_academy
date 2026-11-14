# Checklist de auditoría semántica

Se aplica **después** de `audit_prompt.py`. El pre-scan es heurístico (expresiones regulares); este checklist es la fuente de verdad del veredicto. Responder cada ítem con **Sí / No / N/A** y citar la línea o sección del prompt como evidencia. Todo "No" se convierte en hallazgo con severidad.

Severidad: **Alta** = puede producir salida incorrecta, inválida o insegura. **Media** = degrada calidad o consistencia. **Baja** = estilo o eficiencia.

## A. Objetivo y alcance
- A1. ¿El objetivo se puede expresar en una oración y coincide con lo que pide la salida?
- A2. ¿Todos los términos de dominio, umbrales y parámetros ambiguos están definidos?
- A3. ¿Hay un solo objetivo, o mezcla tareas que convendría encadenar? (ver `iteration_and_decomposition.md` §2)

## B. Instrucciones
- B1. ¿Las instrucciones están en positivo (qué hacer) y no solo como prohibiciones?
- B2. ¿Existen instrucciones contradictorias? (Alta si sí.) ¿Está definida la precedencia cuando chocan?
- B3. ¿El orden de los pasos coincide con el orden real de ejecución?
- B4. ¿Hay énfasis por volumen (mayúsculas, "CRÍTICO", emojis de alarma) donde bastaría una directiva precisa?

## C. Contexto y grounding
- C1. Con contexto largo: ¿contexto primero, tarea al final, frase de anclaje entre ambos?
- C2. ¿Está explícito si se permite conocimiento general o solo el material provisto?
- C3. ¿Qué hace el modelo cuando la información falta? (respuesta fija, `BLOCKED`, campo null)
- C4. ¿Las cláusulas específicas de modelo (fecha de corte, año) corresponden al modelo destino?

## D. Formato de salida
- D1. ¿El formato es verificable mecánicamente (esquema JSON, secciones fijas, señal final)?
- D2. ¿Los ejemplos usan exactamente el mismo formato que la especificación?
- D3. Para JSON complejo: ¿se recomienda `response_schema` nativo además del prompt?

## E. Ejemplos
- E1. ¿Hay 2–4 ejemplos? (0 = hallazgo Media; la fuente recomienda incluirlos siempre.)
- E2. ¿Son variados (casos normales, borde, de rechazo) y no copias con valores cambiados?
- E3. ¿Todos muestran el patrón correcto? (Un ejemplo negativo es Alta.)

## F. Seguridad
- F1. ¿Toda entrada externa (texto del usuario, archivos, salida de otros agentes) está delimitada y declarada como datos?
- F2. ¿Puede un contenido de entrada redefinir rutas, rol o formato? (Alta si sí.)

## G. Agentes y subagentes (N/A si no usa herramientas)
- G1. Scope-lock: ¿rutas de lectura y escritura exactas?
- G2. ¿Distingue lecturas (ejecutar sin preguntar) de escrituras (verificar / confirmar)?
- G3. Errores: ¿reintento acotado en transitorios, cambio de estrategia en lógicos, salida `BLOCKED`?
- G4. Contrato de turnos y presupuesto definidos y coherentes con las herramientas permitidas.
- G5. Señal de finalización única y parseable por el orquestador.
- G6. ¿La verbosidad durante la ejecución está fijada (silencio entre herramientas vs. notas de progreso)?
- G7. ¿Precisión requerida explícita (casos borde exhaustivos vs. estimación aceptable)?

## H. Parámetros y razonamiento
- H1. ¿Sin temperature/top_p/top_k para Gemini 3.6+/3.8/4?
- H2. ¿Evita forzar razonamiento visible salvo que se necesite traza de auditoría?
- H3. Para cálculo o conteo: ¿indica usar ejecución de código cuando esté disponible?

## I. Coherencia con el pipeline (Top's Academy)
- I1. ¿Rutas, nombres de archivo, IDs de regla (ej. `TPL-D3`) y esquemas coinciden con el código/skill que consume la salida? Verificar leyendo el consumidor.
- I2. ¿Existe una versión `lean/` del mismo prompt? Si sí, ¿las reglas compartidas son consistentes entre ambas?

## Veredicto
- **Listo para producción:** 0 hallazgos Alta y ≤ 2 Media.
- **Requiere refactorización:** 1 Alta o ≥ 3 Media.
- **Crítico:** ≥ 2 Alta.

Si el veredicto semántico difiere del puntaje del pre-scan, prevalece el semántico; explicar la diferencia en el reporte.
