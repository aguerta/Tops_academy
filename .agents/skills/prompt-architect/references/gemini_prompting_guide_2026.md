# Guía de Prompt Engineering para Modelos Frontier (Gemini 3+, Gemini 3.8 Flash, Gemini 4)

Este documento consolida las directrices oficiales de diseño de prompts de Google DeepMind para modelos de la familia Gemini 3, Gemini 3.8 Flash y Gemini 4, actualizadas para entornos agenticos y de producción en 2026.

---

## 1. Principios Fundamentales de Prompting

### 1.1 Precisión y Franqueza (Directness)
- Formular el objetivo de manera clara, concisa e inequívoca.
- **Evitar el lenguaje persuasivo, emocional o enfático en mayúsculas** (e.g. evitar `¡MUY IMPORTANTE!`, `POR FAVOR NO OLVIDES`, `CRITICAL RULE`). Los modelos modernos instruction-tuned responden significativamente mejor a especificaciones deterministas y técnicas.
- Definir explícitamente cualquier término ambiguo, parámetro de entrada o umbral numérico.

### 1.2 Delimitadores Estructurales Consistentes
- Separar semánticamente las distintas secciones del prompt utilizando etiquetas XML (`<role>`, `<instructions>`, `<constraints>`, `<context>`, `<task>`, `<output_format>`, `<examples>`) o encabezados Markdown estructurados.
- Mantener la misma convención de delimitadores a lo largo de todo el prompt; no mezclar formatos arbitrariamente.
- Colocar las reglas de comportamiento críticas, la definición de persona (`<role>`) y las restricciones en la **Instrucción de Sistema (System Instruction)** o al inicio absoluto del prompt.

### 1.3 Control Semántico de Verbosidad y Tono (Deprecación de Hiperparámetros)
- **Deprecación de Sampling Parameters:** En Gemini 3.6+, Gemini 3.8 Flash y Gemini 4, los parámetros `temperature`, `top_p` y `top_k` están formalmente deprecados o son ignorados por el motor de inferencia, emitiendo cabeceras de advertencia (y errores HTTP 400 en futuras versiones).
- **Control Semántico:** El determinismo, la creatividad, la extensión y el tono deben regularse mediante instrucciones semánticas explícitas dentro del bloque `<constraints>`:
  - `Verbosity: Low` (respuestas directas, telegráficas, sin introducciones ni despedidas).
  - `Verbosity: Medium` (explicaciones balanceadas con soporte técnico conciso).
  - `Verbosity: High` (análisis exhaustivo paso a paso, derivaciones completas).
  - `Tone: Technical / Formal / Conversational / Socratic`.

---

## 2. Tipos de Entrada y Estrategia de Prefijos

### 2.1 Tipos de Entrada
1. **Pregunta (`Question Input`):** Consulta que el modelo debe responder directamente.
2. **Tarea (`Task Input`):** Acción concreta o procedimiento a ejecutar sobre datos.
3. **Entidad (`Entity Input`):** Clasificación, transformación o extracción sobre un objeto específico.
4. **Completado Parcial (`Partial Input Completion`):** Proporcionar el inicio exacto del patrón deseado para que el modelo continúe la secuencia de forma determinista.

### 2.2 Estrategia de Prefijos
- **Prefijo de Entrada (`Input Prefix`):** Delimita componentes semánticos (e.g., `Texto:`, `Documento Fuente:`, `Código:`).
- **Prefijo de Salida (`Output Prefix`):** Dirige el inicio de la generación (e.g., `JSON:` o `Respuesta:`), reduciendo la charla introductoria y asegurando que el modelo arranque inmediatamente con la estructura requerida.
- **Prefijo de Ejemplo (`Example Prefix`):** Estandariza etiquetas en ejemplos few-shot (e.g., `Entrada:`, `Salida:`).

---

## 3. Ejemplos Few-Shot: Reglas de Oro

### 3.1 Cantidad Óptima
- Incluir de **2 a 4 ejemplos variados y de alta calidad**.
- Más de 4 ejemplos puede provocar *overfitting* al patrón sintáctico de los ejemplos y elevar la latencia y costo de tokens innecesariamente.

### 3.2 Patrones Positivos vs. Anti-Patrones (Regla Crítica)
- **SIEMPRE mostrar el patrón POSITIVO a seguir.**
- **NUNCA incluir ejemplos negativos o "anti-patrones"** (e.g. "Ejemplo de lo que NO debes hacer: ..."). Los modelos LLM son motores predictivos de distribución de tokens; exponer un ejemplo erróneo aumenta la probabilidad condicionada de que el modelo replique dicho error.
- En su lugar, formular la restricción de forma afirmativa:
  - *Incorrecto:* `Don't end haikus with a question: [Ejemplo con pregunta]`
  - *Correcto:* `Always end haikus with an assertion: [Ejemplo con afirmación]`

### 3.3 Consistencia de Formato
- Garantizar que la estructura sintáctica, espaciado, saltos de línea y etiquetas de todos los bloques `<example>` sean exactamente idénticos al esquema de salida especificado en `<output_format>`.

---

## 4. Arquitectura de Contextos Largos y RAG (Long-Context Architecture)

### 4.1 Posicionamiento de Contexto Primero (Context First, Task Last)
Cuando se suministran grandes volúmenes de datos (documentos, expedientes, código fuente, transacciones):
1. **Colocar TODO el `<context>` al PRINCIPIO del prompt de usuario.**
2. **Colocar la consulta específica o `<task>` al FINAL ABSOLUTO del prompt.**
3. **Frase de Anclaje (Context Anchoring):** Interpolar una frase de transición entre el contexto y la tarea:
   `"Con base en la información proporcionada en el <context> anterior, responde a la siguiente tarea: ..."`
- *Justificación Técnica:* Los modelos frontier procesan y atienden con mayor precisión las instrucciones inmediatas previas a la generación cuando el material de referencia ya ha sido consumido y estructurado en su ventana de atención.

### 4.2 Cláusula de Grounding Estricto (Zero-Hallucination RAG)
Para asistentes que deben responder exclusivamente a partir del material proporcionado sin inventar hechos:
```xml
<grounding_contract>
Eres un asistente estrictamente anclado y limitado a la información proporcionada en el <context>.
En tus respuestas, apóyate ÚNICAMENTE en los hechos directamente mencionados en dicho contexto.
NO debes utilizar tu conocimiento previo, sentido común ni extrapolaciones.
No asumas ni infieras más allá de lo explícitamente redactado; reporta los hechos con fidelidad exacta.
Trata el contexto como el límite absoluto de la verdad; cualquier detalle no contenido en el contexto debe ser considerado completamente falso e infundado.
Si la respuesta exacta no está contenida explícitamente en el texto, debes declarar inequívocamente: "La información no se encuentra disponible en el material suministrado."
</grounding_contract>
```

### 4.3 Anclaje Temporal
Para modelos con herramientas de búsqueda web (`Grounding with Google Search`), cláusula recomendada por la fuente (sección *Gemini 3 Flash strategies*):
```text
For time-sensitive user queries that require up-to-date information, you MUST follow the provided current time (date and year) when formulating search queries in tool calls. Remember it is 2026 this year.
```
Cláusula de fecha de corte — **solo si coincide con el modelo destino** (la fuente la da para Gemini 3 Flash; verificar el valor real de otros modelos):
```text
Your knowledge cutoff date is January 2025.
```

---

## 5. Razonamiento Nativo vs. CoT Visible

- Modelos como Gemini 2.5, Gemini 3 y Gemini 3.8 Flash integran **tokens de pensamiento interno (Thinking Tokens)** de forma nativa.
- **No forzar bloques visibles `<thinking>` o cadenas de pensamiento redundantes en la salida del usuario** a menos que se requiera una pista de auditoría explícita en un log de sistema.
- Para activar el máximo esfuerzo de razonamiento en tareas complejas, utilizar una directiva de cierre concisa en el prompt:
  ```xml
  <final_instruction>
  Piensa de forma rigurosa y valida todas las restricciones antes de emitir tu respuesta final.
  </final_instruction>
  ```

---

## 6. Salidas Estructuradas y Herramientas Nativas

1. **Structured Outputs (JSON Schema):**
   - Cuando se requiere JSON en producción, definir el JSON Schema estricto en la configuración de la API (`response_schema`) en combinación con la etiqueta `<output_format>`.
2. **Code Execution (Python Sandbox):**
   - Habilitar la herramienta nativa de ejecución de código para cualquier tarea que involucre aritmética, conteo de palabras/tokens, álgebra simbólica o manipulación tabular, evitando alucinaciones de cálculo numérico por pura predicción de tokens.
