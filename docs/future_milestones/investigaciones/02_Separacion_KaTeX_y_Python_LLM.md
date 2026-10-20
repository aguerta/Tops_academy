# Arquitectura de Desacoplamiento y Validación Estricta para Generación de Problemas Educativos con Python y KaTeX

La generación automatizada de problemas académicos mediante modelos de lenguaje de gran escala (LLM) presenta un punto crítico de falla cuando se combinan, en un único paso inferencial, la lógica computacional en Python y la notación matemática para su posterior renderizado en KaTeX. La persistencia de errores como la duplicación espuria de llaves (`{{...}}`), la interpolación accidental de variables no resueltas y la producción de código LaTeX malformado no responde a la falta de cobertura en las baterías de pruebas, sino a un defecto estructural del pipeline: la colisión sintáctica entre múltiples lenguajes de plantilla dentro del espacio de representación de los tokens del modelo.

Cuando un sistema instruye al modelo a construir código Python que a su vez concatena o emite cadenas con marcado KaTeX, el LLM colapsa las reglas de escape de Python con las macros de KaTeX y los delimitadores del motor de renderizado web. La solución definitiva a este desacople requiere una reingeniería profunda del pipeline *course-to-content*, basada en la separación absoluta entre la lógica de computación del problema y su plantilla de presentación, la adopción de decodificación restringida mediante esquemas tipados, la selección de delimitadores ortogonales y la integración de motores de validación sintáctica embebidos de alto rendimiento.

---

## 1. Diagnóstico de la Colisión Léxica y Ambigüedad de Metacódigo

El problema en los pipelines de generación de contenido técnico surge cuando el modelo debe generar metacódigo: código ejecutable diseñado para generar texto estructurado. Dentro del flujo de generación autorregresiva, los caracteres de llave (`{` y `}`) cumplen funciones semánticas totalmente opuestas dependiendo del contexto:
- En Python, los *f-strings* o `str.format()` interpretan las llaves simples como expresiones ejecutables, obligando a duplicarlas (`{{` y `}}`) para escapar un carácter literal.
- Por el contrario, KaTeX utiliza llaves simples obligatorias para agrupar argumentos posicionales de macros matemáticas, tales como `\frac{a}{b}` o `\sqrt{x}`.
- Al mismo tiempo, muchos entornos de renderizado frontend y plataformas de evaluación emplean motores basados en plantillas como Mustache o Jinja2, que reservan la secuencia de doble llave (`{{ variable }}`) para interpolación.

Esta sobrecarga contextual genera una interferencia severa en la atención autorregresiva del modelo. Cuando el LLM redacta código Python que imprime cadenas KaTeX, sobrecompensa las reglas de escape duplicando llaves en cadenas normales (produciendo salidas como `\frac{{x}}{{y}}` que degradan la salida gráfica de KaTeX) o, por el contrario, emite expresiones LaTeX directas dentro de f-strings, provocando excepciones inmediatas de sintaxis en el intérprete de Python.

Las suites de pruebas basadas en expresiones regulares fallan consistentemente en detectar o corregir estas fallas porque la gramática de LaTeX es recursiva y dependiente del contexto. Las expresiones regulares convencionales son incapaces de verificar la coherencia de árboles sintácticos con anidamiento arbitrario, lo que permite que combinaciones sutilmente inválidas superen las pruebas unitarias y lleguen a la capa de visualización en el navegador.

---

## 2. Paradigma de Separación entre Computación y Presentación (Patrón PrairieLearn)

La arquitectura adoptada por plataformas de educación adaptativa y evaluación algorítmica a gran escala, como el sistema de código abierto *PrairieLearn*, aborda este conflicto eliminando de raíz la generación de texto de presentación dentro del código de cómputo. En lugar de permitir que un script de Python ensamble cadenas con enunciados o fórmulas matemáticas, la lógica se desacopla en dos componentes completamente independientes y aislados:

1. **Módulo de Servidor Puramente Algorítmico:** Función generadora que ejecuta cálculos numéricos o simbólicos mediante bibliotecas como NumPy o SymPy. Tiene prohibido interactuar con HTML, generar etiquetas de visualización o realizar concatenaciones de cadenas destinadas a la interfaz. Su única responsabilidad consiste en popular un diccionario serializable en JSON con los parámetros aleatorizados del problema y las respuestas correctas computadas.
2. **Plantilla Declarativa Estática:** Contiene la totalidad de la redacción pedagógica y el marcado KaTeX. No contiene lógica de programación ni estructuras complejas de control; únicamente define puntos de inyección pasivos para los valores computados por el backend. Cuando el estudiante solicita un nuevo problema, el sistema ejecuta la función en Python, serializa el diccionario resultante e inyecta los datos en la plantilla estática mediante un mecanismo de sustitución determinista.

Para trasladar este principio a un pipeline automatizado por modelos de lenguaje, es necesario aplicar decodificación restringida (*constrained decoding*) a nivel gramatical mediante herramientas como *Instructor*, *BAML* o esquemas JSON forzados con validación Pydantic (`response_format: { type: "json_schema", strict: True }`):

```python
from pydantic import BaseModel, Field

class CompetenceProblemContract(BaseModel):
    competence_id: str = Field(description="Identificador único de la competencia evaluada.")
    python_pure_logic: str = Field(
        description="Código Python que define únicamente la función generate_parameters() -> dict. "
                    "Debe realizar cálculos numéricos o simbólicos (SymPy). Prohibido usar f-strings "
                    "con LaTeX, HTML o sentencias de impresión."
    )
    statement_markdown: str = Field(
        description="Enunciado en Markdown con fórmulas matemáticas KaTeX estándar ($ o $$). "
                    "Usa exclusivamente el token delimitador @PARAM_<nombre>@ para insertar "
                    "los valores calculados por Python."
    )
    solution_markdown: str = Field(
        description="Explicación detallada de la solución con fórmulas KaTeX y tokens @PARAM_<nombre>@."
    )
```

Al utilizar esta arquitectura tipada, el modelo opera en modos cognitivos aislados durante la generación de cada campo. En `python_pure_logic`, el contexto semántico está acotado exclusivamente a la sintaxis del lenguaje de programación; en `statement_markdown`, el modelo redacta prosa y notación matemática KaTeX sin la presión de coordinar las secuencias de escape de Python.

---

## 3. Reingeniería de Delimitadores y Sustitución Determinista

El segundo vector de falla reside en el mecanismo empleado para fusionar los datos computados con la plantilla visual. El uso de delimitadores universales de plantillas basados en llaves duplica el riesgo de colisión con KaTeX.

En pipelines basados en microservicios o interfaces desacopladas, el enfoque más robusto consiste en emplear tokens de sustitución textual que no existan ni en la gramática de Python ni en la especificación de KaTeX. La utilización de marcadores simétricos como `@PARAM_NAME@` o marcas XML personalizadas como `<eval-var name="var_name"/>` evita cualquier tipo de ambigüedad durante la generación y el reemplazo posterior. KaTeX no reserva el carácter arroba para la definición de funciones ni altera las etiquetas XML externas a los bloques de dólares, lo que permite realizar la interpolación final mediante una simple pasada lexicográfica determinista una vez ejecutado el código Python.

Asimismo, cuando los parámetros computados por Python involucran estructuras algebraicas complejas, fracciones o matrices, estos no deben ser representados mediante cadenas construidas manualmente en el código. El código Python debe apoyarse en el módulo `sympy.latex()` para generar representaciones LaTeX canónicas garantizadas matemáticamente. Esto descarga al modelo de lenguaje de la tarea de ensamblar matrices o expresiones algebraicas complejas carácter por carácter, dejando dicha tarea en manos de un motor simbólico determinista.

---

## 4. Verificación Sintáctica Temprana y Análisis AST en Tiempo Real

### Validación Estricta de KaTeX mediante QuickJS Embebido (`pykatex`)
La verificación sintáctica de KaTeX del lado del servidor requiere la ejecución de la misma lógica de parseo que se utiliza en el navegador. La biblioteca `pykatex` resuelve esta necesidad al incrustar el motor JavaScript ultraligero QuickJS dentro de una extensión de Python en C. Al ejecutar directamente el archivo empaquetado oficial `katex.min.js`, `pykatex` garantiza una paridad absoluta con el comportamiento del cliente web.

En su modo de parseo rápido (*fast mode*), `pykatex` prescinde de la generación visual de HTML y se limita a compilar el árbol de sintaxis de la expresión matemática. Esta modalidad alcanza rendimientos de hasta **15,000 ecuaciones por segundo** y es completamente segura para entornos concurrentes. Si el modelo genera macros no permitidas, llaves no balanceadas o duplicaciones indebidas como `\sqrt{{x}}`, `pykatex` intercepta la llamada y extrae la descripción técnica de la excepción `katex.ParseError`, detallando la posición exacta del error en la cadena.

### Aislamiento de Ecuaciones mediante AST de Markdown
Para someter las fórmulas al validador estricto sin generar falsos positivos derivados del texto conversacional del enunciado, se utiliza `markdown-it-py` complementado con extensiones matemáticas como `mdit_py_plugins.dollarmath` o `texmath`. Esta herramienta transforma el enunciado en un árbol de sintaxis abstracta (AST) donde cada fragmento textual queda tipado. El pipeline recorre el árbol resultante, extrae de manera aislada los nodos de tipo matemático (`math_inline` y `math_block`) e ignora el resto del contenido en prosa.

### Inspección Estática de Python con el Módulo Nativo `ast`
Antes de autorizar la ejecución en sandbox del código generado por el LLM, el fragmento de código debe ser analizado mediante el módulo nativo `ast` de Python. Comprueba que las funciones requeridas existan, audita las sentencias de importación para limitar el acceso exclusivamente a bibliotecas autorizadas (`math`, `random`, `sympy`, `numpy`) y rechaza de forma inmediata la presencia de primitivas peligrosas como `eval()`, `exec()` o manipulación de archivos del sistema operativo.

---

## 5. Implementación de Referencia del Orquestador Desacoplado

```python
import ast
from pydantic import BaseModel, Field
import pykatex
from markdown_it import MarkdownIt
from mdit_py_plugins.dollarmath import dollarmath_plugin

class ProblemDefinition(BaseModel):
    competence_id: str
    python_code: str = Field(description="Código Python con función generate() -> dict")
    template_markdown: str = Field(description="Plantilla Markdown con KaTeX y tokens @PARAM@")

class CourseToContentOrchestrator:
    def __init__(self):
        self.md_parser = MarkdownIt().use(dollarmath_plugin)

    def validate_python_ast(self, code: str) -> tuple[bool, str | None]:
        try:
            parsed_ast = ast.parse(code)
            for node in ast.walk(parsed_ast):
                if isinstance(node, (ast.Import, ast.ImportFrom)):
                    for alias in node.names:
                        root_module = alias.name.split('.')[0]
                        if root_module not in {"math", "random", "sympy", "numpy"}:
                            return False, f"Importación prohibida detectada: {root_module}"
                elif isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                    if node.func.id in {"eval", "exec", "open", "__import__", "compile"}:
                        return False, f"Uso de llamada bloqueada: {node.func.id}"
            return True, None
        except SyntaxError as exc:
            return False, f"Error de sintaxis en código Python (línea {exc.lineno}): {exc.msg}"

    def execute_in_sandbox(self, code: str) -> tuple[bool, dict | None, str | None]:
        safe_globals = {
            "__builtins__": {
                "range": range, "len": len, "abs": abs, "min": min, "max": max,
                "round": round, "int": int, "float": float, "str": str,
                "dict": dict, "list": list, "tuple": tuple, "bool": bool
            }
        }
        local_env = {}
        try:
            compiled = compile(code, "<llm_generated_code>", "exec")
            exec(compiled, safe_globals, local_env)
            if "generate" not in local_env or not callable(local_env["generate"]):
                return False, None, "El código Python debe definir la función 'generate()'."
            params = local_env["generate"]()
            if not isinstance(params, dict):
                return False, None, "La función 'generate()' debe retornar un diccionario."
            return True, params, None
        except Exception as exc:
            return False, None, f"Fallo durante la ejecución en sandbox: {str(exc)}"

    def interpolate_tokens(self, template: str, params: dict) -> str:
        rendered = template
        for key, value in params.items():
            rendered = rendered.replace(f"@{key}@", str(value))
        return rendered

    def extract_and_validate_katex(self, markdown_text: str) -> tuple[bool, list[str]]:
        tokens = self.md_parser.parse(markdown_text)
        equations_to_test = []
        for token in tokens:
            if token.type in {"math_inline", "math_block"}:
                equations_to_test.append(token.content)
            elif token.children:
                for child in token.children:
                    if child.type in {"math_inline", "math_block"}:
                        equations_to_test.append(child.content)

        if not equations_to_test:
            return True, []

        validation_results = pykatex.validate_batch(equations_to_test, fast=True)
        errors = [
            f"Fórmula fallida '{res.equation}': {res.error}"
            for res in validation_results if not res.valid
        ]
        return len(errors) == 0, errors

    def process_generation_payload(self, payload: ProblemDefinition) -> dict:
        is_py_valid, py_error = self.validate_python_ast(payload.python_code)
        if not is_py_valid:
            return {"status": "rejected", "stage": "python_ast", "feedback": py_error}

        is_exec_ok, params, exec_error = self.execute_in_sandbox(payload.python_code)
        if not is_exec_ok:
            return {"status": "rejected", "stage": "python_sandbox", "feedback": exec_error}

        interpolated_markdown = self.interpolate_tokens(payload.template_markdown, params)

        is_katex_valid, katex_errors = self.extract_and_validate_katex(interpolated_markdown)
        if not is_katex_valid:
            feedback_str = " | ".join(katex_errors)
            return {"status": "rejected", "stage": "katex_validation", "feedback": feedback_str}

        return {
            "status": "approved",
            "content": interpolated_markdown,
            "params": params
        }
```

---

## 6. Conclusiones y Plan de Transición Arquitectónica

1. **Reemplazo inmediato de la generación libre por esquemas de decodificación restringida:** Toda llamada al LLM para la creación de competencias debe estar regida por Pydantic / BAML con campos disjuntos.
2. **Adopción del estándar de parametrización estricta:** Reconfigurar el contrato de ejecución al estilo *PrairieLearn*, donde el script de Python únicamente computa datos puros y funciones algebraicas serializadas mediante `SymPy`.
3. **Erradicación de llaves para la interpolación dinámica de variables:** Sustituir cualquier uso de delimitadores basados en llaves dobles (`{{...}}`) por tokens ortogonales `@PARAM_NAME@`.
4. **Despliegue de validación nativa temprana con `pykatex`:** Validación en microsegundos con QuickJS y reinyectar el mensaje exacto del compilador en caso de fallo.
