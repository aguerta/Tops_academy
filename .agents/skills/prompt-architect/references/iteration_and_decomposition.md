# Iteración, descomposición y casos especiales

Contenido de `prompting-strategies.md` / `prompting-strategies (1).md` que complementa la guía principal.

## 1. Estrategias de iteración (cuando el prompt no da el resultado esperado)

1. **Reformular.** Palabras distintas con el mismo significado producen respuestas distintas.
   `Version 1: How do I bake a pie?` · `Version 2: Suggest a recipe for a pie.` · `Version 3: What's a good pie recipe?`
2. **Cambiar a una tarea análoga.** Si el modelo no respeta las opciones ("¿A qué categoría pertenece La Odisea: thriller, sci-fi, mitología, biografía?" → responde con un párrafo), reencuadrar como **problema de opción múltiple** ("Multiple choice problem: ... Options: ...") hace que responda solo con la opción.
3. **Reordenar el contenido.** Probar variantes: `[examples][context][input]`, `[input][examples][context]`, `[examples][input][context]`. Para contexto largo, el punto de partida recomendado es contexto primero y tarea al final.
4. **Completado parcial.** Dar el inicio del formato deseado (`I. Introduction\n *`) o un prefijo de salida (`JSON:`) para fijar la forma de la respuesta.
5. **Quitar instrucciones si los ejemplos bastan.** La fuente indica que, con ejemplos claros, parte de las instrucciones puede eliminarse.

## 2. Descomposición de prompts complejos

| Técnica | Cuándo usarla | Aplicación en C2C |
|:---|:---|:---|
| **Una instrucción por prompt** | Muchas instrucciones heterogéneas; se elige el prompt según la entrada. | Prompts separados por rol (transcriber, cta_architect, shard_author, judge, repair). |
| **Encadenar prompts** | Pasos secuenciales: la salida de uno es la entrada del siguiente. | transcripción → CTA → plantillas → juez → reparación. |
| **Agregar respuestas** | Tareas paralelas sobre partes distintas de los datos y luego se combinan. | Shards/jueces en paralelo + harmonizer. |

Señal de que hay que descomponer: el prompt mezcla objetivos con criterios de éxito distintos, o la auditoría muestra que instrucciones del final se ignoran.

## 3. Entradas multimodales

- Tratar texto, imágenes, audio, video y PDF como **entradas de igual categoría**.
- Las instrucciones deben **referenciar explícitamente cada modalidad** ("En la imagen de la página 3...", "Según el PDF adjunto...").
- Para C2C (PDF, tinta manuscrita, imágenes grandes): indicar qué hacer con contenido ilegible (ej. marcar `[ILEGIBLE]` o `BLOCKED`) en lugar de dejar que el modelo lo complete.

## 4. Planificación y autocrítica explícitas (opcional)

Con modelos que tienen razonamiento nativo (Gemini 2.5+/3+), en general **no hace falta** pedir el plan en la salida. Para tareas muy complejas, la fuente propone:

```text
Before providing the final answer, please:
1. Parse the stated goal into distinct sub-tasks.
2. Check if the input information is complete.
3. Create a structured outline to achieve the goal.
```

```text
Before returning your final response, review your generated output against the user's original constraints.
1. Did I answer the user's *intent*, not just their literal words?
2. Is the tone authentic to the requested persona?
```

Alternativa de menor costo: "Think very hard before answering" (más tokens de pensamiento, sin texto visible extra).

## 5. Herramientas para evitar alucinaciones

- **Grounding con Google Search:** habilitar cuando el modelo puede necesitar hechos recientes u oscuros.
- **Code execution:** habilitar para cualquier aritmética, conteo o cálculo.
- **Cosas a evitar (fuente):** depender del modelo para hechos factuales sin grounding; usar con cuidado en matemática y lógica sin herramienta de código.

## 6. Parámetros: resolución de conflictos entre fuentes

Las fuentes no coinciden; regla de precedencia: **la fuente más reciente y específica del modelo manda.**

| Recomendación | Fuente | Estado |
|:---|:---|:---|
| "Si hay respuesta de fallback, sube la temperatura." | Guía general (antigua) | **Obsoleta** para Gemini 3.6+/3.8/4: el parámetro se ignora. Reformular el prompt o revisar el filtro de seguridad. |
| Ajustar temperature/topK/topP por tarea. | Guía general | Solo modelos previos a Gemini 3. |
| Mantener temperature en 1.0 por defecto. | Sección Gemini 3 | Gemini 3.0–3.5. |
| No enviar temperature/top_p/top_k. | Nota Gemini 4 / 3.6+ | **Vigente** para 3.6+, 3.8 Flash y 4. |
| `max_output_tokens`, `stop_sequences` | Guía general | Vigentes; elegir secuencias de parada que no aparezcan en el contenido. |

Las cláusulas específicas de modelo (ej. "Your knowledge cutoff date is January 2025", recomendada para Gemini 3 Flash) **solo se incluyen si coinciden con el modelo destino**; verificar el valor real del modelo antes de usarlas.
