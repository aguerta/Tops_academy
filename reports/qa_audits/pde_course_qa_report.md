# Informe de Auditoría Técnica Pedagógica y de Calidad Instruccional
**Estado en Plataforma:** Activo (Vigente)  
**Fecha de Eliminación:** Nulo  
**Curso:** Ecuaciones en derivadas parciales (`pde_course`)  
**Estándares de Referencia:** Quality Matters (QM), OSCQR, Marco Pedagógico de Dominio (Mastery Learning)  
**Fecha de Evaluación:** Octubre 2026  
**Auditor:** Agente de Aseguramiento de Calidad Instruccional (In-House QA Agent)

---

## 1. Resumen Ejecutivo y Veredicto

| Métrica | Resultado |
|---|---|
| **Puntaje Base (Subtotal Dimensiones)** | **9.2 / 20.0 pts** |
| **Penalizaciones Duras Aplicadas** | **-2.0 pts** (Preguntas Huérfanas Críticas) |
| **Calificación Final Consolidada** | **7.2 / 20.0 pts** |
| **Nivel de Calidad (Quality Tier)** | **CRÍTICO (0 - 10 pts)** |
| **Estado de Publicación Recomendado** | **RECHAZADO / BLOQUEADO PARA PUBLICACIÓN HASTA REMEDIACIÓN** |

El curso `pde_course` cuenta con una sólida fundamentación matemática de partida (21 competencias clasificadas en Hechos, Conceptos y Habilidades, con un banco de 500 preguntas). Sin embargo, la auditoría técnica y pedagógica revela deficiencias severas que vulneran los principios fundamentales del aprendizaje para el dominio (Mastery Learning):
1. **85.7% de distractores con retroalimentación vacía** (1,500 de 1,750 distractores en opción múltiple repiten la plantilla genérica `"Distractor basado en misconception de..."`).
2. **Pistas progresivas alucinadas y plantilla idéntica**: 129 de 129 reactivos de selección múltiple (100%) comparten exactamente el mismo trío de pistas, de las cuales la Pista 2 alucina el "principio de superposición" en contenidos donde no aplica (homogeneidad, orden/grado, Lagrange).
3. **Fugas técnicas de variables de plantilla**: 12 reactivos exponen marcadores no renderizados (`{k_val}`) y llaves dobles (`{{yy}}`, `{{my}}`).
4. **Preguntas huérfanas críticas**: Reactivos que evalúan conceptos no explicados en el curso (frecuencia angular en osciladores espaciales de 2do orden y vector normal a superficies implícitas).
5. **Inflación por clonación artificial**: De las 500 preguntas, únicamente existen 138 enunciados únicos; 106 enunciados se repiten entre 2 y 15 veces idénticos.

---

## 2. Metadatos del Curso

- **Identificador del Curso:** `pde_course`
- **Título de la Unidad:** Ecuaciones en derivadas parciales
- **Competencias Totales:** 21 (7 Hechos `H`, 6 Conceptos `C`, 8 Habilidades `Hab`)
- **Total de Preguntas en Banco:** 500 reactivos
- **Distribución de Tipos de Reactivo:**
  - `multiple_choice_7_options`: 250 (50.0%)
  - `multiple_select`: 129 (25.8%)
  - `fill_in_the_blank`: 121 (24.2%)
- **Macro-Objetivo Terminal Inferido:**
  > Formular, clasificar analíticamente, reducir operacionalmente y resolver con precisión cuantitativa ecuaciones en derivadas parciales de primer y segundo orden (lineales y cuasilineales) aplicadas a modelos económicos y dinámicos, aplicando el Teorema de Euler a funciones homogéneas de producción, ejecutando la separación de variables, resolviendo sistemas característicos de Charpit-Lagrange con multiplicadores algebraicos, deduciendo superficies integrales explícitas ante condiciones iniciales de Cauchy mediante inversión paramétrica, y descomponiendo operadores diferenciales de segundo orden en cascada para aislar componentes homogéneos y particulares.

---

## 3. Evaluación Detallada por Dimensiones

### Dimensión 1: Arquitectura y Granularidad
**Calificación: 2.5 / 4.0 puntos**

- **Estructura Curricular:**
  - *Fortaleza:* La taxonomía cognitiva de base (CTA) desglosa adecuadamente el dominio en Hechos conceptuales (H-01 a H-07), Conceptos estructurales (C-01 a C-06) y Habilidades de resolución procedimental (Hab-01 a Hab-08).
  - *Deficiencia:* La organización en el archivo de entrega es puramente plana y monolítica. No existe estructuración en módulos o unidades temáticas jerárquicas (p.ej., *Unidad 1: Homogeneidad y Euler; Unidad 2: Métodos de 1er Orden y Lagrange; Unidad 3: Problema de Cauchy; Unidad 4: EDPs de 2do Orden y Reducción en Cascada*).
- **Objetivos de Micro-Aprendizaje:**
  - No existen objetivos de aprendizaje explícitos por lección formulados con verbos de desempeño observables (Bloom / Webb DOK); solo se proveen descripciones sintéticas de la competencia.
- **Grafo de Dependencias:**
  - El curso carece de metadatos de prerrequisitos y dependencias (`prerequisites`, `leads_to`), lo que impide que el motor de dominio active andamiaje adaptativo real ante lagunas del estudiante.

---

### Dimensión 2: Calidad de Evaluación y Reactivos
**Calificación: 2.0 / 5.0 puntos**

- **Variedad Formal vs. Autenticidad Psicométrica:**
  - Aunque formalmente se cubren tres modalidades de interacción (`multiple_choice_7_options`, `multiple_select`, `fill_in_the_blank`), los reactivos de 7 opciones están saturados de opciones sintéticamente alteradas sin plausibilidad cognitiva real.
- **Justificaciones de Distractores (Error Rationale):**
  - **Fallo Crítico:** De los 1,750 distractores en opción múltiple, **1,500 (85.7%)** contienen el texto genérico `"Distractor basado en misconception de [Nombre de Competencia]"`.
  - No se explica por qué la opción es errónea ni qué error de cálculo o concepción matemática representa (ej. error de signo, inversión de derivadas, confusión de grado con orden).
- **Clonación e Inflación Artificial del Banco:**
  - El banco exhibe únicamente **138 enunciados únicos para 500 preguntas**. 106 enunciados se repiten de forma casi exacta. Por ejemplo:
    - *Problema de Cauchy en Hab-06 (`Q-Hab06-411` a `Q-Hab06-425`):* El enunciado `Para la EDP Ux + Uy = 1 con condición inicial de Cauchy U(x, 0) = x^2, ¿cuál es la solución explícita?` se repite **15 veces idéntico**, únicamente permutando el orden de las opciones.
    - *Multiplicadores de Lagrange en Hab-05:* El enunciado `Para la EDP (x - y)Ux + (y - U)Uy = U - x...` se repite **15 veces**.
    - Preguntas conceptuales en C-01 a C-06 se clonan hasta 10 veces cada una.

---

### Dimensión 3: Andamiaje y Feedback Progresivo
**Calificación: 1.5 / 5.0 puntos**

- **Cumplimiento Nominal vs. Deficiencia Pedagógica:**
  - Si bien el 100% de los reactivos registra formalmente 3 pistas (`hints_count = 3`, 0 preguntas con 0 pistas), la calidad del andamiaje es sumamente precaria.
- **Alucinación y Boilerplate en Selección Múltiple:**
  - Las 129 preguntas `multiple_select` (100%) tienen exactamente el mismo bloque de pistas:
    1. *"Analice cada afirmación de manera independiente evaluando sus hipótesis analíticas."*
    2. *"Recuerde que el principio de superposición exige linealidad estricta del operador."*
    3. *"Verifique la consistencia lógica de las definiciones frente a los casos particulares."*
  - En **108 de estas 129 preguntas (83.7%)**, la Pista 2 alude al "principio de superposición" en contenidos como Definición de Homogeneidad (H-01), Taxonomía de Grado y Orden (H-02), o Multiplicadores de Lagrange (Hab-05), lo cual es pedagógicamente engañoso y falso para el estudiante.
- **Fuga de Variables de Plantilla en Pistas:**
  - En 12 preguntas (ej. `Q-H03-043`, `Q-H03-046`, `Q-H03-047`, `Q-H03-048`, `Q-H03-056`, `Q-Hab02-292`, `Q-Hab02-293`, `Q-Hab02-294`, `Q-Hab02-303`, `Q-Hab02-310`, `Q-Hab02-313`, `Q-Hab02-315`), la Pista 2 expone texto corrupto de plantilla:
    > `"Calcule $U_{{yy}} = m^2 \cos({k_val} x) e^{{my}} = m^2 U$."`
  - Esto denota una falla en el renderizador del generador algorítmico, exponiendo `{k_val}` y llaves dobles sin compilar.

---

### Dimensión 4: Alineación Instruccional
**Calificación: 2.0 / 4.0 puntos**

- **Ausencia de Teoría Integrada:**
  - El curso carece de textos o lecciones instruccionales expositivas; opera únicamente como un banco de reactivos respaldado en las breves descripciones de cada competencia.
- **Detección de Preguntas Huérfanas Críticas:**
  - **`Q-C03-184` (y clones):** Pregunta por la *"frecuencia angular $m$ de las soluciones trigonométricas $\cos(mx)$ y $\sin(mx)$"* para la EDO espacial $X''(x) + 4 X(x) = 0$. El concepto de frecuencia angular de osciladores armónicos de 2do orden no está explicado ni definido en C-03 (que solo define el ansatz $U=fg$ y la constante $\lambda$) ni en los hechos previos.
  - **`Q-C02-161` y `Q-C02-163`:** Evalúa el vector normal a la superficie integral implícita $U(x,y) - u = 0$ exigiendo ingresar el coeficiente escalar constante $c_3 = -1$. El gradiente de superficies implícitas no se introduce en la competencia C-02.
  - **`Q-H03-043`:** Evalúa la anulación de la ecuación de Laplace $U_{xx} + U_{yy} = 0$ dentro de H-03 ("Identidad de Verificación de Solución" de 1er orden), antes de introducir las EDPs de segundo orden (H-05 y H-06).
- **Desalineación Temática Interna:**
  - En `Hab-05` ("Construcción de Integrales Primeras mediante Multiplicadores de Lagrange"), 7 reactivos evalúan integración directa de EDPs simples con coeficientes constantes ($2 U_x + 4 U_y = 0$), reactivos que pertenecen a Hab-04 y no utilizan multiplicadores de Lagrange.

---

### Dimensión 5: Accesibilidad y Ergonomía Técnica / LaTeX
**Calificación: 1.2 / 2.0 puntos**

- **Notación Matemática y LaTeX:**
  - Las fórmulas matemáticas emplean correctamente delimitadores `$ ... $` y se encuentran balanceadas en la gran mayoría de casos.
- **Fallas de Formateo y Exposición de Código:**
  - Presencia de 12 preguntas con marcadores `{k_val}` sin renderizar y llaves dobles residuales (`{{yy}}`, `{{my}}`).
  - La redacción en los reactivos clonados es rígida y carente de contexto aplicado real.

---

## 4. Penalizaciones Duras Aplicadas

| Criterio de Penalización Dura | Condición Verificada | Descuento |
|---|---|---|
| **Banco < 3 ejercicios prácticos por unidad** | Todas las competencias tienen $\ge 20$ preguntas | 0.0 pts |
| **Ejercicios sin pistas progresivas (`hints = 0`)** | 0 preguntas carecen de pistas (todas tienen 3) | 0.0 pts |
| **Detección de Preguntas Huérfanas Críticas** | Detectadas preguntas huérfanas críticas (`Q-C03-184`, `Q-C02-161`) | **-2.0 pts** |
| **Total Deducciones Duras** | | **-2.0 pts** |

---

## 5. Cálculo del Puntaje Final Consolidado

$$\text{Subtotal por Dimensiones} = 2.5 + 2.0 + 1.5 + 2.0 + 1.2 = 9.2 \text{ pts}$$
$$\text{Deducciones Duras} = -2.0 \text{ pts}$$
$$\mathbf{Puntaje\ Final} = 9.2 - 2.0 = \mathbf{7.2\ /\ 20.0\ pts}$$

**Quality Tier:** **CRÍTICO (0 - 10)**

---

## 6. Plan de Remediación Inmediata

1. **Reestructuración Modular y Grafo de Competencias:**
   - Dividir las 21 competencias en 4 unidades jerárquicas:
     - *Unidad 1:* Funciones Homogéneas, Teorema de Euler y Aplicaciones Económicas (H-01, C-01, Hab-01).
     - *Unidad 2:* EDPs Cuasilineales de 1er Orden y Método de Lagrange (H-02, H-03, H-04, C-02, C-04, Hab-02, Hab-04, Hab-05).
     - *Unidad 3:* Problema de Cauchy y Curvas Características (C-05, Hab-06).
     - *Unidad 4:* EDPs de 2do Orden, Separación de Variables y Operadores (H-05, H-06, H-07, C-03, C-06, Hab-03, Hab-07, Hab-08).
   - Añadir metadatos formales de prerrequisitos entre unidades y micro-objetivos medibles (Bloom).

2. **Remediación Integral del Andamiaje y Pistas:**
   - Eliminar la plantilla idéntica en las 129 preguntas `multiple_select`. Reemplazar la Pista 2 alucinada sobre "principio de superposición" por pistas específicas sobre la definición analítica de cada reactivo.
   - Diseñar pistas progresivas socráticas de 3 niveles:
     - *Nivel 1 (Orientación/Concepto):* Recordar la definición o principio rector.
     - *Nivel 2 (Estrategia/Paso Clave):* Guiar la sustitución o el cálculo algebraico intermedio.
     - *Nivel 3 (Resolución Guiada):* Mostrar el paso previo inmediato a la conclusión sin regalar la respuesta.

3. **Corrección de Bugs de Renderizado de Plantillas:**
   - Subsanar el script generador para reemplazar `{k_val}`, `{{yy}}` y `{{my}}` por los valores numéricos y sintaxis LaTeX limpia en las 12 preguntas afectadas de H-03 y Hab-02.

4. **Sustitución de Rationale Genérico por Feedback Constructivo:**
   - Reescribir los 1,500 distractores con `"error_rationale"` genérico. Cada distractor debe explicar detalladamente el fallo (ej. *"Se invirtió el orden de los coeficientes característicos"*, *"Se sumaron exponentes en lugar de aplicar el grado a la escala homogénea"*).

5. **Diversificación Real del Banco de Preguntas:**
   - Reemplazar las copias clónicas (donde sólo cambia el orden de las opciones) por generadores paramétricos que varíen funciones, coeficientes numéricos y contextos de aplicación.

6. **Eliminación y Realineación de Preguntas Huérfanas y Desalineadas:**
   - En `Q-C03-184`, reformular la pregunta para evaluar estrictamente la constante de separación $\lambda$ o incluir una píldora conceptual previa sobre EDOs armónicas.
   - En `Q-C02-161`, incluir en la teoría de C-02 la deducción del vector normal implícito $(U_x, U_y, -1)$.
   - En `Hab-05`, reubicar las 7 preguntas de integración directa elemental hacia `Hab-04`.
