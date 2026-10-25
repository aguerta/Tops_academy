# Rúbrica Normativa de Auditoría de Calidad Pedagógica y Psicométrica

Esta rúbrica establece los estándares formales de evaluación para cursos en la plataforma **Top's Academy**, basados en **Quality Matters (QM)**, **OSCQR** y **Mastery Learning**.

---

## 1. Escala de Calificación y Dimensiones (Total: 20 Puntos)

### Dimensión 1: Arquitectura y Granularidad (0 a 4 puntos)
- **4.0 pts (Excelente)**: Módulo altamente atómico enfocado en micro-habilidades claras; prerrequisitos explícitos modelados en grafo (DAG); carga cognitiva perfectamente balanceada entre Hechos [H], Conceptos [C] y Habilidades [Hab].
- **2.0 - 3.0 pts (Aceptable)**: Módulo comprensible pero con unidades densas, conceptos implícitos o falta de delimitación modular jerárquica clara.
- **0.0 - 1.0 pts (Crítico)**: Contenido enciclopédico monolítico sin división funcional; mezcla caótica de teoría y aplicaciones complejas.

### Dimensión 2: Calidad de Evaluación y Reactivos (0 a 5 puntos)
- **5.0 pts (Excelente)**: Variedad equilibrada de tipos de ítem (opción múltiple de 7 alternativas, selección múltiple, fill-in-the-blank) y cumplimiento estricto del estándar de al menos 4 arquetipos diferenciados por micro-competencia (`min_archetypes: 4`); distractores plausibles que capturan conceptos erróneos frecuentes de la literatura con `error_rationale` diagnóstico al 100%; evalúa aplicación profunda evitando la mecanización algorítmica; cero fugas de respuestas (*Answer Leaks*).
- **3.0 - 4.0 pts (Aceptable)**: Preguntas pertinentes pero con distractores predecibles, o **monocultivo de un único arquetipo paramétrico repetitivo** donde solo varían coeficientes numéricos e induce mecanización del alumno (-1.0 a -1.5 pts).
- **0.0 - 2.0 pts (Crítico)**: Metainformación delatora visible en opciones (*"despejando erróneamente..."*, rótulos *"Trayectoria exacta:"*, justificaciones parentéticas diagnósticas como `(confusión con...)`), **Phantom Keying** (distractores con el valor idéntico a la clave bajo prefijos sintéticos tipo *"Opción alterna X:"*) (-2.0 a -3.0 pts), o fuga del valor de respuesta en el enunciado.

### Dimensión 3: Andamiaje y Feedback Progresivo (0 a 5 puntos)
- **5.0 pts (Excelente)**: Retroalimentación inmediata con explicaciones pedagógicas de error; exactamente 3 a 5 pistas escalonadas socráticas en prosa por reactivo (Pista 1: Conceptual $\to$ Pista 2: Procedimental $\to$ Pista 3: Cálculo operativo paso a paso) que guían el razonamiento sin regalar la respuesta; solución detallada completa con advertencia de ideas preconcebidas erróneas (*misconception warning*).
- **3.0 - 4.0 pts (Aceptable)**: Explica la respuesta correcta pero las pistas intermedias son escasas, revelan la solución prematuramente o contienen fórmulas en texto plano sin delimitar en KaTeX. **Pistas deficientes aisladas (stub hints de una sola palabra o tags snake_case)** (-1.0 a -1.5 pts).
- **0.0 - 2.0 pts (Crítico)**: Solo indica "correcto/incorrecto" sin pistas escalonadas, pistas estáticas alucinadas que repiten textos no aplicables al tema, o **inyección masiva de códigos de prerrequisito (ej. `["C-02", "H-02"]`) como pistas** en lugar de prosa socrática.

### Dimensión 4: Alineación Instruccional (0 a 4 puntos)
- **4.0 pts (Excelente)**: Congruencia semántica absoluta entre el objetivo declarado, la teoría desarrollada y los ítems de prueba; alineación con taxonomía de Bloom (énfasis en Aplicación y Análisis); cero preguntas huérfanas o contaminación cruzada inter-dominio.
- **2.0 - 3.0 pts (Aceptable)**: Leve desfase: la teoría aborda conceptos no evaluados, o el examen evalúa detalles periféricos no enfatizados en la lección.
- **0.0 - 1.0 pts (Crítico)**: Desconexión severa: el test evalúa competencias o fórmulas ajenas no enseñadas en el contenido de la lección (ej. problemas de otros dominios inyectados como relleno).

### Dimensión 5: Accesibilidad y Ergonomía Técnica / KaTeX (0 a 2 puntos)
- **2.0 pts (Excelente)**: Expresiones matemáticas formalmente compilables en KaTeX con delimitadores balanceados (`$...$` / `$$...$$`); ausencia total de triples delimitadores (`$$$`) o llaves dobles espurias (`{{...}}`); notación de derivadas preservada intacta ($\phi''(k)$); ausencia de variables de plantilla sin interpolar en modo matemático (`{sigma2}`, `${dep_var}`); ausencia de colisiones de signos algebraicos (`|x - -4|`, `+ -8`); prosa clara, sintaxis limpia y formato fluido.
- **1.0 pt (Aceptable)**: Errores menores de escape de caracteres, deslices tipográficos aislados o dobles signos menos esporádicos que no impiden el renderizado global (-0.3 a -0.6 pts).
- **0.0 pts (Crítico)**: Fórmulas rotas en LaTeX, delimitadores abiertos sin cierre, residuos de f-strings en múltiples fórmulas, texto ilegible o colapso del renderizador.

---

## 2. Penalizaciones Duras Automáticas (Hard Deductions)

Se aplican deducciones directas acumulativas sobre la nota final consolidada:
- **-2.0 puntos**: Si el banco de ejercicios por unidad tiene menos de 3 problemas prácticos reales e independientes.
- **-1.0 punto**: Por cada ejercicio que carezca por completo de pistas progresivas (`hints = 0`).
- **-2.0 puntos**: Si se detecta al menos una "pregunta huérfana" crítica (concepto evaluado que no aparece en el corpus teórico o contaminación inter-dominio).

> [!NOTE]
> La nota final nunca podrá ser inferior a **0.0** ni superior a **20.0**.

---

## 3. Rangos de Certificación de Calidad (Quality Tiers)

- **EXCELENTE (17.0 - 20.0 pts)**: Aprobado para producción inmediata. Cumple los más altos estándares pedagógicos.
- **ACEPTABLE (14.0 - 16.9 pts)**: Aprobado con observaciones menores. Requiere pulido sintáctico o ajuste leve de andamiaje.
- **DEFICIENTE (11.0 - 13.9 pts)**: Requiere reingeniería curricular previa a su publicación.
- **CRÍTICO (0.0 - 10.9 pts)**: Rechazado categóricamente. Debe ser retirado de la plataforma o generado desde cero ("cuenta nueva").

---

## 4. Esquema JSON de Salida Estructurada

Cada auditoría debe generar obligatoriamente un bloque de razonamiento `<analysis>...</analysis>` y un bloque JSON estricto:

```json
{
  "course_metadata": {
    "course_id": "string",
    "unit_title": "string",
    "detected_objective": "string",
    "total_competencies": 0,
    "total_questions": 0
  },
  "dimension_scores": {
    "architecture_granularity": {
      "score": 0.0,
      "max": 4.0,
      "feedback": "string"
    },
    "assessment_quality": {
      "score": 0.0,
      "max": 5.0,
      "feedback": "string"
    },
    "scaffolding_hints": {
      "score": 0.0,
      "max": 5.0,
      "feedback": "string"
    },
    "instructional_alignment": {
      "score": 0.0,
      "max": 4.0,
      "feedback": "string"
    },
    "technical_ergonomics": {
      "score": 0.0,
      "max": 2.0,
      "feedback": "string"
    }
  },
  "penalties_applied": [
    {
      "reason": "string",
      "deduction": 0.0
    }
  ],
  "final_score": 0.0,
  "quality_tier": "CRÍTICO (0-10) | DEFICIENTE (11-13) | ACEPTABLE (14-16) | EXCELENTE (17-20)",
  "remediation_actions": [
    "string"
  ]
}
```
