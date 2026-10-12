# Informe de Auditoría Técnico-Pedagógica de Calidad Instruccional

**Estado en Plataforma:** Activo (Vigente)  
**Fecha de Eliminación:** Nulo  
**Curso:** Sistemas de Ecuaciones Diferenciales Ordinarias y Aplicaciones Macroeconómicas Dinámicas (`sistemas_edos`)  
**Fecha de Auditoría:** 12 de Octubre, 2026  
**Auditor:** In-House Course QA Agent (Plataformas de Aprendizaje para el Dominio / Mastery Learning)  
**Marco de Evaluación:** Quality Matters (QM), OSCQR & Mastery Learning Framework  
**Puntaje Final Consolidado:** **5.5 / 20.0**  
**Nivel de Calidad (Quality Tier):** **CRÍTICO (0 - 10)**

---

## 1. Resumen Ejecutivo del Veredicto

El curso **"Sistemas de Ecuaciones Diferenciales Ordinarias y Aplicaciones Macroeconómicas Dinámicas"** (`sistemas_edos`) ha sido evaluado bajo los estándares de *Mastery Learning*, *Quality Matters (QM)* y *OSCQR*. Tras una inspección forense exhaustiva y programática de sus 20 competencias y 470 reactivos, el curso obtiene una calificación final de **5.5 / 20.0**, ubicándose en el nivel **CRÍTICO**.

A pesar de presentar una taxonomía modular declarativamente bien estructurada (Hechos, Conceptos, Habilidades) y un andamiaje formal de 3 pistas progresivas por reactivo, el curso sufre de colapsos pedagógicos y psicométricos estructurales:
1. **Falsa granularidad y redundancia masiva:** De 470 preguntas nominales, solo existen 84 escenarios únicos. El banco está inflado por clonaciones clónicas masivas y permutaciones cosméticas de opciones.
2. **Fuga flagrante de respuestas (Answer Leaks):** En al menos 5 reactivos de tipo *fill-in-the-blank*, el enunciado revela la respuesta directamente al estudiante (*"Si el equilibrio de reposo satisface $x^* = 3$, ingrese el valor de $x^*$"*).
3. **Pregunta huérfana crítica masiva (Contaminación cruzada):** Un reactivo de selección múltiple sobre dinámicas de Goodwin e IS-LM fue inyectado de forma indiscriminada **72 veces en 12 competencias ajenas**, evaluando modelos macroeconómicos complejos en unidades básicas de álgebra lineal pura (inversión de matrices 2x2, autovectores generalizados, etc.).
4. **Colapso del feedback formativo:** El 100% de los reactivos de opción múltiple con 7 alternativas (1,410 distractores) utiliza un texto genérico de relleno (*"Distractor basado en misconception de..."*), anulando la retroalimentación diagnóstica al error.
5. **Pistas delatoras en distractores:** 476 opciones de respuesta incluyen la confesión del error en su propio texto (*"sumando erróneamente..."*, *"olvidando permutar..."*), permitiendo al estudiante descartarlas por deducción léxica trivial.
6. **Anomalías en sintaxis LaTeX:** 68 incidencias de dobles signos negativos (`- -4`, `+ -4`, `e^{--1t}`) derivadas de interpolación defectuosa de cadenas.

### Tabla Resumen de Dimensiones

| Dimensión Evaluada | Puntaje Obtenido | Puntaje Máximo | Cumplimiento (%) | Diagnóstico Sintético |
| :--- | :---: | :---: | :---: | :--- |
| **1. Arquitectura y Granularidad** | **2.8** | 4.0 | 70.0% | 20 competencias estructuradas, pero infladas con solo 84 escenarios únicos y sin unidades previas que fundamenten la macroeconomía dinámica. |
| **2. Calidad de Evaluación y Reactivos** | **1.8** | 5.0 | 36.0% | Fuga de respuestas en enunciado, metadatos delatores en 476 opciones, claves contradictorias entre opciones matemáticamente idénticas. |
| **3. Andamiaje y Feedback Progresivo** | **2.3** | 5.0 | 46.0% | Formalmente 3 pistas por ítem, pero 1,410 distractores (100% de MC7) tienen rationales genéricos sin valor formativo; pistas circulares en ítems filtrados. |
| **4. Alineación Instruccional** | **1.5** | 4.0 | 37.5% | Pregunta huérfana masiva replicada 72 veces en 12 competencias no pertinentes; desalineación entre habilidades y tipo de problema evaluado. |
| **5. Accesibilidad y Ergonomía Técnica** | **1.1** | 2.0 | 55.0% | Entornos matriciales correctos, pero 68 errores de dobles negativos (`- -4`, `+ -4`, `e^{--1t}`) que degradan la ergonomía matemática. |
| **Subtotal Rúbrica** | **9.5** | 20.0 | 47.5% | - |
| **Penalizaciones Duras** | **-4.0** | - | - | **-2.0** por banco < 3 problemas prácticos reales en unidades; **-2.0** por pregunta huérfana crítica masiva. |
| **TOTAL FINAL** | **5.5** | **20.0** | **27.5%** | **Nivel CRÍTICO** |

---

## 2. Auditoría Granular por Dimensiones

### Dimensión 1: Arquitectura y Granularidad (2.8 / 4.0 pts)
* **Descomposición de Habilidades:** El curso organiza 20 competencias atómicas:
  * **8 Hechos (Fact):** H-01 (Polinomio característico), H-02 (Fórmula cuadrática espectral), H-03 (Inversa 2x2), H-04 (Solución particular constante), H-05 (Autovalores complejos), H-06 (Autovector generalizado), H-07 (Matriz Jacobiana), H-08 (Tasas de variación proporcional).
  * **5 Conceptos (Concept):** C-01 (Superposición), C-02 (Plano traza-determinante), C-03 (Hiperbolicidad y Hartman-Grobman), C-04 (Bloque triangular), C-05 (Leyes de exceso de demanda).
  * **7 Habilidades (Skill):** Hab-01 (Reducción matricial), Hab-02 (Estados estacionarios), Hab-03 (Diagnóstico espectral directo), Hab-04 (Subespacios propios), Hab-05 (Coeficientes indeterminados), Hab-06 (Linealización local), Hab-07 (Conversión log-diferencial).
* **Deficiencias Estructurales:**
  * **Falsa Granularidad:** Aunque se reportan 470 preguntas, solo existen 84 escenarios de preguntas únicos en todo el curso. En cada una de las 7 habilidades (Hab-01 a Hab-07), los 30 reactivos reportados consisten en exactamente 3 problemas base repetidos entre 7 y 15 veces mediante permutaciones mecánicas de opciones.
  * **Ausencia de Secuencia de Prerrequisitos:** No se introducen módulos teóricos previos que formalicen el modelo macroeconómico de ajuste IS-LM o el modelo de ciclo distributivo de Goodwin antes de exigir su evaluación en problemas prácticos.

### Dimensión 2: Calidad de Evaluación y Reactivos (1.8 / 5.0 pts)
* **Fuga Directa de Respuesta en el Enunciado (Answer Leaks):**
  En 5 reactivos de tipo *fill_in_the_blank*, el enunciado literalmente provee la respuesta numérica que luego solicita ingresar:
  * `Q-H04-061`: *"En un sistema lineal $\dot{X} = AX + B$, las isoclinas de reposo son $-x + 2y = 4$ y $2x - y = 4$. Si el equilibrio de reposo satisface $x^* = 3$, ingrese el valor de $x^*$."* (Respuesta: `3`).
  * `Q-H04-062`: *"Si el equilibrio de reposo satisface $x^* = 4$, ingrese el valor de $x^*$."* (Respuesta: `4`).
  * `Q-H04-068`: *"Si el equilibrio de reposo satisface $x^* = 2$, ingrese el valor de $x^*$."* (Respuesta: `2`).
  * `Q-H04-071` y `Q-H04-075`: *"Si el equilibrio de reposo satisface $x^* = 5$, ingrese el valor de $x^*$."* (Respuesta: `5`).
  Esto destruye por completo la validez evaluativa de estos ítems.
* **Metainformación Delatora en Distractores (476 ocurrencias):**
  En los reactivos de opción múltiple, el texto de la opción incluye la explicación metacognitiva del error, permitiendo al estudiante descartar distractores sin resolver el problema matemático:
  * Ejemplo en `Q-H03-041`:
    * Opción A: *"olvidando permutar los elementos diagonales entre sí."*
    * Opción B: *"invirtiendo de forma escalar los elementos diagonales como si la matriz fuera diagonal."*
    * Opción F: *"multiplicando erróneamente por $-\det(A)$ en lugar de dividir entre el determinante."*
* **Contradicciones Lógicas y Opciones Idénticas:**
  * En `Q-H01-002`: La Opción C ($\lambda^2 - 5 = 0$) está marcada como correcta (`True`), mientras que la Opción G ($\lambda^2 + 0\lambda - 5 = 0$, que es una identidad matemática exacta) está marcada como incorrecta (`False`).
  * En más de 30 reactivos (p. ej., `Q-H03-041`, `Q-Hab06-411` a `Q-Hab06-440`), un distractor incorrecto comparte exactamente la misma expresión matricial o escalar que la alternativa correcta (e.g., $J^* = \begin{bmatrix}0 & -3 \\ 2 & 0\end{bmatrix}$ presente tanto en la opción errónea E como en la correcta G en `Q-Hab06-411`).

### Dimensión 3: Andamiaje y Feedback Progresivo (2.3 / 5.0 pts)
* **Pistas Progresivas:** Todos los 470 reactivos cuentan nominalmente con 3 niveles de pistas (`hints_count: 3`) y solución detallada.
* **Colapso del Feedback Correctivo (1,410 distractores sin feedback):**
  * En el 100% de las 235 preguntas `multiple_choice_7_options`, los 6 distractores incorrectos por pregunta (1,410 distractores en total, el 85.4% de las opciones incorrectas del curso) contienen la misma plantilla genérica en el campo `error_rationale`:
    > `"Distractor basado en misconception de [Nombre de la Competencia]."`
  * Ninguno de estos 1,410 distractores explica cuál fue el error algebraico, conceptual o procedimental.
* **Pistas Circulares:** En las preguntas con fuga de respuesta (Q-H04-061 a Q-H04-075), la tercera pista afirma: *"La coordenada solicitada es $x^* = 3$"*, reproduciendo la tautología sin guiar en la resolución del sistema algebraico.

### Dimensión 4: Alineación Instruccional (1.5 / 4.0 pts)
* **Inyección Masiva de Pregunta Huérfana Contaminante (72 ocurrencias):**
  El reactivo de selección múltiple con enunciado:
  > *"Considere las aplicaciones dinámicas macroeconómicas (Modelo IS-LM Dinámico y Ciclos de Goodwin). Seleccione todas las proposiciones formalmente válidas:"*
  fue insertado como comodín 72 veces en **12 competencias distintas**:
  * H-03 (*Inversa Matricial 2x2*): 5 veces.
  * H-04 (*Solución Particular Constante*): 5 veces.
  * H-05 (*Base Real para Autovalores Complejos Conjugados*): 5 veces.
  * H-06 (*Definición de Autovector Generalizado*): 5 veces.
  * H-08 (*Álgebra de Tasas de Variación Proporcional*): 5 veces.
  * C-01 (*Principio de Superposición y Partición*): 5 veces.
  * C-04 (*Desacoplamiento Causal Unidireccional*): 5 veces.
  * C-05 (*Leyes de Movimiento por Exceso de Demanda*): 5 veces.
  * Hab-01 (*Reducción Estructural Matricial*): 8 veces.
  * Hab-02 (*Inversión Algebraica para Estados Estacionarios*): 8 veces.
  * Hab-05 (*Ajuste por Coeficientes Indeterminados*): 8 veces.
  * Hab-07 (*Conversión Log-Diferencial de Variables Ratio*): 8 veces.
  En unidades básicas de álgebra lineal (como calcular una inversa $2 \times 2$ o definir un autovector generalizado), se evalúan proposiciones sobre la participación salarial $u^* = 1 - (\alpha + n)\sigma$, la dinámica presa-depredador de Goodwin y la velocidad de ajuste monetario $c_2$. Esto representa una desconexión pedagógica severa.
* **Desalineación de Habilidades Prácticas:**
  * En `Hab-04` (*Resolución de Subespacios Propios para Trayectorias Explícitas*), 8 reactivos evalúan regiones del plano traza-determinante (tema de C-02), sin involucrar el cálculo de autovectores $(A - \lambda I)v = 0$.
  * En `Hab-03` (*Diagnóstico Espectral Directo*), 8 reactivos evalúan definiciones teóricas de polinomios característicos y fórmulas de Viète.
  * En `Hab-06` (*Linealización Diferencial*), 8 reactivos evalúan el teorema de Hartman-Grobman de forma puramente teórica en lugar de computar derivadas parciales evaluadas en el punto interior.

### Dimensión 5: Accesibilidad y Ergonomía Técnica / LaTeX (1.1 / 2.0 pts)
* **Entornos Matemáticos:** Las matrices y vectores están correctamente tipografiados en su mayoría con entornos `\begin{bmatrix} ... \end{bmatrix}` y delimitadores `$`.
* **Anomalías de Concatenación Algebraica (68 incidencias):**
  Se detectaron 68 expresiones con signos dobles negativos sin simplificar generadas por interpolación de cadenas `f"{a} - {b}"` donde `b` ya era negativo:
  * `$\lambda^2 + 7\lambda - -4 = 0$` (Q-H01-002, opción A)
  * `$\lambda^2 - -9\lambda + -4 = 0$` (Q-H01-002, opción B)
  * `$\lambda^2 - -5 = 0$` (Q-H01-002, opción D)
  * `$\lambda^2 - -4\lambda + -9 = 0$` (Q-H01-004, opción B)
  * `$\lambda^2 + 2\lambda - -4 = 0$` (Q-H01-005, opción C)
  * `$e^{--1t}$` (Q-H05-081, opción B)
  Estas expresiones representan una degradación técnica que entorpece la lectura y el rigor matemático.

---

## 3. Verificación de Penalizaciones Duras

| Criterio de Penalización | Condición Detectada | Descuento Aplicado |
| :--- | :--- | :---: |
| **Banco < 3 ejercicios prácticos por unidad** | Al descontar la pregunta comodín macroeconómica ajena y los clones idénticos, la competencia C-01 tiene 0 problemas prácticos de cálculo; H-08 tiene solo 1 problema práctico real; y Hab-01 a Hab-07 presentan solo 2 problemas prácticos únicos inflados artificialmente. | **-2.0 pts** |
| **Ejercicio sin pistas progresivas (hints = 0)** | 0 ejercicios con hints = 0 (470 de 470 tienen formalmente 3 pistas). | **0.0 pts** |
| **Pregunta huérfana crítica detectada** | Detectada masivamente: reactivo sobre IS-LM y Goodwin inyectado 72 veces en 12 competencias no pertinentes de álgebra lineal básica. | **-2.0 pts** |
| **Total Deducciones Duras** | - | **-4.0 pts** |

---

## 4. Registro Forense de Evidencias

### 4.1 Fuga Directa de Respuesta (Answer Leaks)
```text
Reactivo: Q-H04-061 (fill_in_the_blank)
Enunciado: "En un sistema lineal \dot{X} = AX + B, las isoclinas de reposo son -x + 2y = 4 y 2x - y = 4. 
            Si el equilibrio de reposo satisface x^* = 3, ingrese el valor de x^*."
Respuesta esperada: 3
Fallo: La pregunta indica explícitamente el valor buscado dentro del enunciado condicional.

Reactivo: Q-H04-062 (fill_in_the_blank)
Enunciado: "...Si el equilibrio de reposo satisface x^* = 4, ingrese el valor de x^*."
Respuesta esperada: 4
```

### 4.2 Distractores Genéricos en Reactivos de Opción Múltiple
```text
Reactivo: Q-H01-002 (multiple_choice_7_options)
Distractor A: error_rationale = "Distractor basado en misconception de Polinomio Característico Canónico 2x2."
Distractor B: error_rationale = "Distractor basado en misconception de Polinomio Característico Canónico 2x2."
Distractor D: error_rationale = "Distractor basado en misconception de Polinomio Característico Canónico 2x2."
Distractor E: error_rationale = "Distractor basado en misconception de Polinomio Característico Canónico 2x2."
Distractor F: error_rationale = "Distractor basado en misconception de Polinomio Característico Canónico 2x2."
Distractor G: error_rationale = "Distractor basado en misconception de Polinomio Característico Canónico 2x2."
Total en el curso: 1,410 distractores (100% de los reactivos MC7) presentan este mismo texto de relleno.
```

### 4.3 Inyección de Pregunta Huérfana Masiva
```text
Enunciado: "Considere las aplicaciones dinámicas macroeconómicas (Modelo IS-LM Dinámico y Ciclos de Goodwin). 
            Seleccione todas las proposiciones formalmente válidas:"
Competencias contaminadas (72 ocurrencias en total):
- H-03 (Inversa Matricial 2x2): Q-H03-050, Q-H03-051, Q-H03-053, Q-H03-056, Q-H03-057
- H-05 (Autovalores Complejos Conjugados): Q-H05-088, Q-H05-089, Q-H05-090, Q-H05-095, Q-H05-097
- H-06 (Autovector Generalizado): Q-H06-102, Q-H06-103, Q-H06-105, Q-H06-106, Q-H06-113
- H-08 (Tasas de Variación Proporcional): Q-H08-150, Q-H08-153, Q-H08-155, Q-H08-156, Q-H08-158
- C-01 (Principio de Superposición): Q-C01-162, Q-C01-164, Q-C01-170, Q-C01-171, Q-C01-172
- C-04 (Bloque Triangular): Q-C04-227, Q-C04-228, Q-C04-233, Q-C04-234, Q-C04-235
- C-05 (Leyes de Movimiento): Q-C05-242, Q-C05-244, Q-C05-253, Q-C05-254, Q-C05-259
- Hab-01, Hab-02, Hab-05, Hab-07: 8 ocurrencias en cada una.
```

### 4.4 Anomalías de Sintaxis Algebraica (LaTeX)
```text
Q-H01-002 (Opción A): "$\lambda^2 + 7\lambda - -4 = 0$..."
Q-H01-002 (Opción B): "$\lambda^2 - -9\lambda + -4 = 0$..."
Q-H01-002 (Opción D): "$\lambda^2 - -5 = 0$..."
Q-H01-004 (Opción B): "$\lambda^2 - -4\lambda + -9 = 0$..."
Q-H01-005 (Opción C): "$\lambda^2 + 2\lambda - -4 = 0$..."
Q-H05-081 (Opción B): "$X_h(t) = e^{--1t} [c_1 \cos(2t) + c_2 \sin(2t)]$..."
Total detectado: 68 incidencias.
```

---

## 5. Plan de Remediación Inmediata

1. **Remediación Crítica 1: Erradicar la Pregunta Comodín Huérfana (Prioridad Urgente)**
   * Eliminar las 72 instancias del reactivo macroeconómico de Goodwin e IS-LM de las 12 competencias ajenas (H-03, H-05, H-06, H-08, C-01, C-04, Hab-01, Hab-02, Hab-05, Hab-07).
   * Generar reactivos de selección múltiple auténticamente contextualizados a los objetivos de cada competencia (e.g., propiedades algebraicas de $A^{-1}$ en H-03; bases reales y rotaciones en H-05; cadenas de Jordan en H-06).

2. **Remediación Crítica 2: Reparar Enunciados con Fuga de Respuesta (Prioridad Urgente)**
   * Reformular de inmediato Q-H04-061, Q-H04-062, Q-H04-068, Q-H04-071 y Q-H04-075.
   * *Ejemplo de corrección para Q-H04-061:*
     * *Enunciado erróneo:* `"En un sistema lineal \dot{X} = AX + B, las isoclinas de reposo son -x + 2y = 4 y 2x - y = 4. Si el equilibrio de reposo satisface x^* = 3, ingrese el valor de x^*."`
     * *Enunciado corregido:* `"En un sistema lineal \dot{X} = AX + B, las isoclinas de reposo están dadas por las ecuaciones -x + 2y = 4 y 2x - y = 4. Resuelva el sistema simultáneo de reposo y determine el valor de la coordenada de equilibrio x^*. Ingrese el número entero."`

3. **Remediación Crítica 3: Escribir Rationales Pedagógicos Específicos (Prioridad Alta)**
   * Reemplazar los 1,410 textos comodín en `error_rationale` por explicaciones pedagógicas puntuales del error (e.g., *"Error: sumó los elementos cruzados en lugar de la diagonal principal al calcular la traza"*).

4. **Remediación Crítica 4: Limpiar Metadatos en Opciones de Respuesta (Prioridad Alta)**
   * Remover de los 476 textos de alternativas palabras delatoras como *"erróneamente"*, *"olvidando"*, *"confundiendo"* o *"permutando"*. Las opciones deben presentar únicamente la solución matemática o afirmación conceptual, reservando la explicación del error para el feedback posterior.

5. **Remediación Técnica 5: Sanitizar la Generación de Sintaxis LaTeX (Prioridad Alta)**
   * Incorporar una función de normalización algebraica en el script generador para colapsar dobles signos (`- -a` $\to$ `+ a`, `+ -a` $\to$ `- a`, `--a` $\to$ `+a`).

6. **Remediación Psicométrica 6: Resolver Contradicciones de Opciones (Prioridad Media)**
   * Garantizar que dos opciones que expresan la misma relación matemática no reciban calificaciones booleanas opuestas (como en Q-H01-002 con $\lambda^2 - 5 = 0$ vs $\lambda^2 + 0\lambda - 5 = 0$).

7. **Remediación Arquitectónica 7: Diversificar el Banco de Ejercicios Prácticos (Prioridad Media)**
   * Rediseñar las competencias de habilidad (Hab-01 a Hab-07) para que dispongan de al menos 5 a 8 problemas prácticos genuinamente independientes y parametrizados, erradicando la clonación artificial de 1 o 2 reactivos base.
