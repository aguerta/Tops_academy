# Solución al conflicto KaTeX y Python en LLMs

**User**: Hay un problema con una codebase y es que como genera código Python para autogenerar competencias para generar problemas en la plataforma y a la vez esta plataforma necesita utilizar Katex para renderizar los problemas, los LLMs al hacer las competencias alucinan y a veces ponen doble brackets o hacen mal el código Katex o hacen código Python, pero cuando se quiere renderizar Katex hay un problemón porque no se sabe si es Python o es Katex. Y se ha creado un montón de tests, hay toda una suite de tests, pero es un problema persistente y no he encontrado solución. ¿Cómo podría lograr de que esto se solucione? Analiza el pipeline de la skill course to content y encuentra la solución.

Necesito que busques en internet proyectos o ideas o librerías o qué han hecho otros desarrolladores que se han topado con este problema y cómo lo han solucionado

**Gemini**: Este problema es un clásico en plataformas educativas automatizadas (como sistemas estilo PrairieLearn, EdX, Khan Academy o generadores basados en LLMs). El conflicto surge por una colisión sintáctica fundamental: **las llaves `{}` son compartidas por los f-strings / diccionarios / sets de Python y por los comandos / entornos de KaTeX/LaTeX**, además del conflicto entre delimitadores de Markdown (`$`, `$$`) e interpolación en plantillas.

Tratar de resolver esto solo con *prompt engineering* o con regex a posteriori siempre falla porque el LLM confunde los niveles de abstracción (cree que está escribiendo LaTeX dentro de un f-string de Python y duplica o des-duplica llaves aleatoriamente: `{{ \frac{a}{b} }}` vs `\frac{a}{b}`).

La solución en arquitecturas de generación consiste en **desacoplar completamente la representación matemática de la sintaxis del lenguaje de ejecución**.

---

### Diagnóstico de la falla en el Pipeline

**Colisión de escape**: Si el LLM genera Python directamente con f-strings (`f"El resultado es {x} y la fórmula es \frac{{{a}}}{{{b}}}"`), la carga cognitiva y de tokenización se dispara. Los tokenizadores dividen las secuencias `{{` y `}}` de forma inconsistente, provocando alucinaciones.

**Ambigüedad de parsers**: KaTeX falla con `ParseError` si recibe llaves dobles o caracteres de escape de Python no procesados (`\\frac` vs `\frac`), y Python falla con `KeyError` o `ValueError` si interpreta sintaxis LaTeX como formato.

**Falta de tipado estructural**: El pipeline está tratando el enunciado, el código ejecutable y las expresiones matemáticas como un solo string continuo.

---

### Cómo lo resuelven otros desarrolladores y proyectos

#### 1. Arquitectura "AST / Structured Output" con Slots (La solución más robusta)
En lugar de pedirle al LLM un bloque monolítico de Python que contenga cadenas con LaTeX dentro, se le fuerza a escupir un **esquema estructurado (JSON Schema / Pydantic con Structured Outputs de la API)**:
**Por qué funciona**: El LLM nunca tiene que preocuparse por escapar llaves de LaTeX para complacer al parser de Python, porque están en campos aislados.

---

#### 2. Cambio de Delimitadores de Plantilla (Sustituir f-strings por Jinja2 Custom o Delimitadores Neutros)
El mayor causante de `{{` y `}}` alucinados es usar motores de plantillas basados en llaves (Jinja2 estándar, `str.format()` o `f-strings`).
Plataformas de evaluación técnica configuran un motor de plantillas con delimitadores que **no colisionen ni con LaTeX (`{}`) ni con Markdown ni con Python**.
En Jinja2, se redefinen los delimitadores:
Al obligar al prompt a usar `<<% var %>>` o `@PARAM@` para interpolar Python:
- KaTeX mantiene sus llaves `{}` intactas (`\frac{1}{2}`).
- El LLM ya no intenta adivinar si debe poner `{{` para escapar Python o `{` para KaTeX.

---

#### 3. El Pipeline de Ejecución de Dos Fases (Sandbox Execution + Render Phase)
Desacoplar la fase de cómputo en Python (produciendo un diccionario de parámetros numéricos/simbólicos puros) de la fase declarativa de renderizado KaTeX.

---

#### 4. Post-procesamiento y Normalización Automática (Parser Heurístico)
Validación temprana antes de guardar o renderizar.

---

### Plan de Acción Recomendado para la Skill

1. **Definir separación por contrato**: Prohíbe en el prompt generar código Python que imprima strings con KaTeX embebido. Pídele al LLM que separe:
   - `setup_code`: variables y cálculo de soluciones en Python.
   - `problem_statement`: enunciado en Markdown con KaTeX estándar y slots de reemplazo `<<variable>>` o `@PARAM@`.
2. **Migrar fuera de los f-strings**: Si el pipeline actual toma un string del LLM y hace `eval(f"...")`, elimínalo. Ese es el origen de la ambigüedad.
3. **Validación semántica en la suite de tests**: En lugar de solo tests de integración, valida:
   - Que `setup_code` compile con `ast.parse()`.
   - Que `problem_statement` pase por un validador sintáctico de KaTeX (ej. llamando a la CLI de KaTeX o usando `pykatex` / comprobador de balanceo de delimitadores LaTeX) antes de guardarlo en base de datos.
