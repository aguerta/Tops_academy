# Limitaciones de la Plataforma de Estudio y Habilidades No Testeadas

**Contexto:** Análisis cognitivo y arquitectónico de la plataforma Top's Academy frente a la ciencia del aprendizaje (*Learning Architect Framework*). Identifica las familias de habilidades que el paradigma actual (plantillas parametrizadas, renderizado texto/LaTeX, preguntas cerradas de 7 alternativas con pistas progresivas) no puede evaluar por diseño.

---

## 1. Habilidades que la Plataforma NO Puede Testear (Puntos Ciegos Estructurales)

### A. Pensamiento Gráfico-Visual, Espacial y Traducción entre Representaciones (*Dual Channels & The Drawing Effect*)
- **Punto Ciego Técnico:** El motor opera únicamente en el canal verbal-simbólico mediante texto y LaTeX (`engine/render.py`). Puede evaluar algebraicamente sobre un estado estacionario o un estimador, pero no puede pedir trazar una curva, ajustar una pendiente o leer un gráfico crudo sin texto descriptivo.
- **Déficit Cognitivo:** La memoria de trabajo tiene canales separados para información verbal y visoespacial (*Dual Channels*). Se desaprovecha el **efecto del dibujo (*****Drawing Effect*****)**, que genera tres trazos de memoria simultáneos: visual, motor y semántico. Además, la experticia avanzada requiere **múltiples representaciones (*****Multiple Representations*****)** para traducir fluidamente de ecuaciones a geometría (ej. retrato de fase en EDOs).

### B. Generación Abierta, Recuerdo Libre (*Free Recall*) y Construcción de Demostraciones
- **Punto Ciego Técnico:** Todos los ejercicios se validan mediante formatos cerrados de opción múltiple (`mc` de 7 opciones) o selección múltiple (`ms`), donde la respuesta correcta ya está visible en la pantalla.
- **Déficit Cognitivo:** Se testea **reconocimiento (*****recognition*****)** o recuerdo con pistas (*cued recall*), pero nunca **recuperación libre (*****free recall*****)** ni **generación pura (*****Generation Effect*****)**. Riesgos:
  - *Confundir reconocimiento con recuerdo*: Fácil descartar distractores, difícil derivar en una hoja en blanco.
  - *Ilusión de profundidad explicativa (Illusion of Explanatory Depth)*: Creer que se domina una demostración porque se aciertan preguntas sobre sus partes.

### C. Formulación de Modelos, Abstracción de la Realidad y Crítica de Supuestos (*Figuring Out the Game*)
- **Punto Ciego Técnico:** Los generadores (`engine/instantiate.py`) entregan problemas donde el modelo matemático ya fue seleccionado, las variables están limpias y los supuestos cerrados.
- **Déficit Cognitivo:** En exámenes reales o práctica profesional, los estudiantes deben saber **crear modelos desde situaciones ambiguas**, **criticar supuestos** y **decidir qué información descartar (*****Learning as "less"*****)**. La plataforma salta directamente a la fase de ejecución técnica.

### D. Habilidades Transversales (*Cross-Cutting Skills*), Casos Difusos y Riesgo de *Overfitting* a Plantillas
- **Punto Ciego Técnico:** El análisis CTA divide el curso en compartimentos discretos (`H-XX`, `C-XX`, `Hab-XX`) y genera variaciones numéricas sobre una misma plantilla fija.
- **Déficit Cognitivo:**
  - *Pérdida de fronteras difusas (Fuzzy Boundaries)*: No se entrenan casos donde no es obvio qué herramienta aplicar o donde se combinan sub-habilidades.
  - *Atención que bloquea el aprendizaje*: Repetir instancias nacidas de la misma plantilla automatiza el reconocimiento de pistas superficiales (*surface features*) produciendo *routine expertise* (sobreajuste a la plataforma) en lugar de *adaptive expertise* (capacidad de resolver problemas inéditos).

### E. Autodiagnóstico de Errores y Monitoreo sin Red (*Self-Monitoring & Delayed Feedback*)
- **Punto Ciego Técnico:** Retroalimentación inmediata de acierto/error y entre 3 y 5 pistas (`hints`) al alcance de un clic. Solo se evalúa la opción final marcada, sin auditar el procedimiento.
- **Déficit Cognitivo:** El feedback inmediato es útil al inicio, pero en niveles intermedios y avanzados atrofia la **metacognición y automonitoreo (*****self-monitoring*****)**. En condiciones de **feedback diferido o sin feedback**, se obliga al estudiante a auditar su propio trabajo antes de saber el resultado.

### F. Argumentación Escrita, Empiria con Ruido y Trabajo Computacional (*Shop Time*)
- **Punto Ciego Técnico:** Entorno individual, determinista y cerrado con respuesta única canónica.
- **Déficit Cognitivo:** No entrena procesos deliberativos lentos propios de la escritura matemática formal, ni el manejo de datos reales con ruido (econometría empírica), ni la implementación computacional (simulaciones en Julia/R/Python).

---

## 2. Parcheo Táctico y Rutinas Complementarias
- **Recuperación a Libro Cerrado:** Tapar las opciones de la pantalla antes de resolver en papel.
- **Boceto Obligatorio en Papel / GeoGebra:** Graficar antes de responder preguntas de dinámica o estática comparativa.
- **Auto-Explicación Escrita:** Anotar formalmente por qué cada paso de una demostración es válido.
- **Cuadernos de Simulación (DGP):** Simular trayectorias numéricas en Python/Julia para complementar la teoría abstracta.
