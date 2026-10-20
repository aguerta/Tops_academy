# Límites de la Plataforma y Transformación en un Arnés de Aprendizaje Profundo (Learning Harness)

**Contexto:** Diagnóstico de los 7 puntos ciegos cognitivos de Top's Academy bajo el principio de **procesamiento apropiado para la transferencia (*****transfer-appropriate processing*****)** y especificación de las modificaciones programáticas en el motor (`engine/`) y esquemas (`schemas/`) para convertir la plataforma en un simulador de exigencia analítica quirúrgica.

---

## 1. Los 7 Puntos Ciegos Estructurales

1. **Recuperación Libre (*Free Recall*) vs. Reconocimiento (*Recognition*):** Con 7 opciones múltiples, la respuesta correcta siempre está visible. Se entrena reconocimiento y descarte, no evocación desde la memoria a largo plazo frente a una hoja en blanco.
2. **Traducción y Construcción Gráfico-Visual (*Dual Channels & Drawing Effect*):** Renderizado exclusivo de texto/LaTeX; incapacidad de evaluar diagramas de fase, curvas de nivel o retratos de estabilidad.
3. **Encadenamiento de Derivaciones Largas y Demostraciones (*Bundling & Proofs*):** Se evalúa el resultado final o un eslabón aislado, sin auditar demostraciones de 10 pasos ni detectar el renglón exacto donde se violó un supuesto.
4. **Profundidad Explicativa Causal y Argumentación (*Illusion of Explanatory Depth*):** Leer explicaciones prefabricadas produce alta fluidez de procesamiento, creando la ilusión de maestría sin capacidad de articular el mecanismo causal de principio a fin.
5. **Formulación de Modelos desde Problemas No Estructurados (*Adaptive Expertise*):** Los problemas ya vienen estructurados y enmarcados. No se entrena la distinción entre características superficiales y estructura profunda ni la selección de supuestos.
6. **Implementación Computacional, Simulación y Trabajo Empírico (*Shop Time*):** El sandbox interno usa SymPy, pero el alumno nunca programa ni simula procesos numéricos no lineales.
7. **Automonitoreo sin Pistas y Desempeño con Retroalimentación Diferida (*Delayed Feedback*):** La disponibilidad inmediata de pistas genera dependencia y atrofia el automonitoreo en condiciones reales de evaluación.

---

## 2. Palancas Programáticas para el Rediseño de la Plataforma (Learning Harness)

### 2.1. Entrada Simbólica Abierta (*Free-Response Symbolic Inputs*)
- **Cambio en Esquemas:** Crear tipos de pregunta `open_symbolic` o `numeric_input` en `schemas/template.schema.json`.
- **Motor Backend:** Caja de texto matemática evaluada dinámicamente mediante `SymPy` (comparación de equivalencia algebraica mediante `simplify(user_expr - correct_expr) == 0`).
- **Efecto Cognitivo:** Elimina la conjetura por descarte y fuerza el cálculo algebraico completo.

### 2.2. Validador de Pasos Intermedios (*Step-by-Step Proof Grader*)
- **Cambio en Sandbox:** Extender `engine/sandbox.py` para recibir y auditar hitos intermedios obligatorios (ej. Paso 1: Solución homogénea $y_h$; Paso 2: Solución particular $y_p$; Paso 3: Constantes por condiciones de frontera).
- **Efecto Cognitivo:** Entrena el encadenamiento (*bundling*) e impide avanzar si se arrastra un error algebraico temprano.

### 2.3. Generador de Perturbaciones y Violación Deliberada de Supuestos (*Boundary Testing*)
- **Cambio en Autores:** Programar distractores que no varíen signos al azar, sino que calculen los resultados que se obtendrían al ignorar un supuesto específico (ej. olvidar una condición inicial o asumir coeficientes constantes en EDOs de coeficientes variables).
- **Efecto Cognitivo:** Retroalimentación inmediata que diagnostica la falacia conceptual del estudiante.

### 2.4. Módulo Gráfico Interactivo y Validación de Retratos de Fase (*Canvas / Visual Assertions*)
- **Cambio en Frontend:** Integrar componentes interactivos SVG / Canvas para arrastrar vectores del campo de pendientes, marcar isoclinas nulas o seleccionar bosquejos cualitativos de retratos de fase.
- **Efecto Cognitivo:** Activa el canal visoespacial y fuerza la traducción bidireccional entre álgebra y geometría.

### 2.5. Verificación de Artefactos de Simulación (*Notebook / Script Attachment*)
- **Cambio en Pipeline:** Exigir en competencias avanzadas la carga o ejecución de mini-scripts en Python o Julia que simulen trayectorias numéricas (Runge-Kutta, perturbaciones Monte Carlo).
- **Efecto Cognitivo:** Conecta la deducción teórica con el trabajo computacional empírico.

### 2.6. Andamiaje con Retardo y Escalera de Fricción (*Delayed Scaffolding*)
- **Cambio en Lógica de Hints:** Bloquear pistas durante los primeros 5 minutos de enfrentamiento con el problema. Habilitar pista conceptual de alto nivel al primer fallo y pistas operativas solo tras esfuerzo sostenido.
- **Efecto Cognitivo:** Entrena la resistencia a la frustración y el automonitoreo metacognitivo.
