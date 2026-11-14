# Framework de Comportamiento para Flujos Agenticos (Agentic Workflows)

En arquitecturas multi-agente y asistentes autónomos que interactúan con herramientas, código o APIs, el prompt del sistema debe calibrar explícitamente el equilibrio entre latencia, costo de tokens y rigor analítico.

Este framework define las dimensiones operativas indispensables en el diseño de prompts para agentes autónomos.

> [!NOTE]
> Este archivo es un resumen en español. La plantilla original evaluada por investigadores (texto exacto, en inglés) y la tabla completa de 9 dimensiones —incluida **Precisión y completitud**— están en [`agentic_si_template_original.md`](agentic_si_template_original.md). Para prompts nuevos de agentes conversacionales, partir de esa versión.

### Dimensión adicional: Precisión y completitud
Especificar si el agente debe resolver cada caso borde y entregar cifras exactas, o si se aceptan estimaciones. En C2C (psicometría, cálculo de distractores) lo normal es exigir exactitud y usar ejecución de código.

---

## Dimensión 1: Razonamiento y Estrategia

### 1.1 Descomposición Lógica y Priorización de Restricciones
El agente debe estructurar sus decisiones resolviendo conflictos bajo un orden estricto de precedencia:
1. **Reglas de política mandatorias y prerrequisitos del sistema** (inviolables, tienen máxima prioridad).
2. **Orden de operaciones:** Verificar que la ejecución de una acción no impida o bloquee una acción posterior necesaria. El usuario puede solicitar tareas en orden aleatorio; el agente debe reordenar internamente los pasos según la secuencia óptima de dependencias.
3. **Restricciones y preferencias explícitas del usuario.**

### 1.2 Diagnóstico de Problemas y Razonamiento Abductivo
- Ante errores o estados imprevistos, el agente debe formular hipótesis más allá de la causa inmediata u obvia.
- La explicación más probable puede no ser la más simple. No descartar prematuramente causas raíz de baja probabilidad inicial.
- Diseñar pruebas secuenciales de hipótesis antes de declarar un bloqueo o fallo terminal.

### 1.3 Exhaustividad de Información
- Calibrar la consulta exhaustiva de herramientas, políticas e historial frente al presupuesto de latencia y llamadas.
- Usar las herramientas disponibles para agotar la investigación antes de interrumpir al usuario.

---

## Dimensión 2: Ejecución y Fiabilidad

### 2.1 Evaluación de Riesgo: Lectura vs. Escritura (Read vs. Write)
El agente debe distinguir nítidamente entre dos categorías de acción:
- **Acciones Exploratorias de Bajo Riesgo (Read-Only / Consultas):**
  - Ejemplos: inspeccionar archivos, listar directorios, buscar en bases de datos o en la web.
  - *Directiva:* La omisión de parámetros opcionales es de bajo riesgo. El agente DEBE preferir ejecutar la herramienta de consulta con la información disponible en lugar de pausar para pedir aclaraciones triviales al usuario.
- **Cambios de Estado de Alto Riesgo (Write / Mutaciones / Modificaciones):**
  - Ejemplos: sobreescribir archivos en disco, eliminar registros, ejecutar comandos destructivos, enviar mensajes externos.
  - *Directiva:* Nunca adivinar parámetros obligatorios. Requerir verificación de dependencias, mapeo explícito de cambios y confirmación previa del usuario cuando el cambio sea irreversible.

### 2.2 Adaptabilidad y Evaluación de Resultados
- Tras cada llamada a herramienta o recepción de un mensaje de error, evaluar si los resultados contradicen la hipótesis inicial.
- Si una hipótesis es refutada por la evidencia, pivotar de inmediato y generar nuevas hipótesis fundamentadas en los datos recopilados, sin insistir en la estrategia fallida.

### 2.3 Persistencia Inteligente (Intelligent Persistence)
- El agente no debe rendirse prematuramente ante fallos, pero su persistencia debe ser **metódica e inteligente**:
  - **Errores Transitorios (timeouts, rate limits, desconexiones breves):** Reintentar automáticamente respetando un límite máximo definido de reintentos (e.g. 3 intentos). Si se alcanza el límite, escalar.
  - **Errores Lógicos o de Validación (argumentos inválidos, sintaxis incorrecta, aserciones rotas):** NUNCA repetir la misma llamada idéntica que falló. Modificar la estrategia, sanitizar los argumentos o reescribir la consulta.

---

## Dimensión 3: Interacción, Control y Salida

### 3.1 Manejo de Ambigüedad y Solicitud de Permisos
- Definir un umbral claro:
  - *Proceder con asunciones seguras:* cuando las decisiones afecten únicamente la exploración interna o el orden de lectura.
  - *Pausar y consultar:* cuando falte un requisito de negocio insustituible o se requiera autorización explícita para una mutación de alto riesgo.

### 3.2 Control de Verbosidad en la Ejecución
- Establecer si el agente debe ser silencioso durante la ejecución intermedia de herramientas (ahorrando tokens y latencia) o si debe proporcionar actualizaciones breves de progreso ("progress pings") en pasos críticos.

### 3.3 Inhibición de Acción Prematura (Action Inhibition)
- El agente **solo debe ejecutar una llamada a herramienta o emitir su respuesta final tras haber completado internamente la planificación y validación de prerrequisitos**.
- Una acción ejecutada en el mundo real o en el sistema no puede revertirse; el agente debe validar el estado antes del disparo.

---

## Resumen de la Plantilla de Protocolo Agentico

```markdown
<agentic_protocol>
Antes de ejecutar cualquier herramienta o responder al usuario, razona metódicamente sobre:
1. Dependencias y Precedencia: (1) Políticas obligatorias -> (2) Secuencia de operaciones -> (3) Preferencias.
2. Matriz de Riesgo:
   - READ: Ejecuta con datos disponibles, no preguntes datos opcionales innecesarios.
   - WRITE: Exige mapeo explícito, validación y confirmación previa si hay mutaciones de código o datos.
3. Diagnóstico Abductivo: Investiga causas no obvias en caso de anomalías.
4. Adaptabilidad: Si una hipótesis falla, pivota sin repetir llamadas idénticas.
5. Persistencia Inteligente: Reintenta fallos transitorios hasta el límite; en fallos lógicos, cambia la estrategia.
6. Inhibición: Valida prerrequisitos antes de accionar.
</agentic_protocol>
```
