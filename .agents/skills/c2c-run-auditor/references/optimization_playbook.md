# Playbook de Optimización de Rendimiento para Content-to-Course

Este compendio traduce los diagnósticos de cuellos de botella detectados por `c2c-run-auditor` en acciones técnicas concretas para optimizar los tiempos y costos del pipeline.

---

## 1. Patrones de Diagnóstico & Palancas de Solución

### Diagnóstico 1: Turn Bloat en Subagentes Autores (> 3 turnos)
- **Síntoma**: Un autor de shard realiza 15 a 60 turnos en lugar de los 1–2 turnos prescritos por el Protocolo Atómico.
- **Causa Raíz**: 
  - El autor redacta plantilla por plantilla en llamadas separadas de `write_to_file`.
  - El autor valida iterativamente con `check_templates.py`, falla en KaTeX o variables, y entra en bucle de corrección en lugar de validar localmente todo de una vez.
- **Solución Recomendada**:
  - Enforce de **Escritura Masiva en 1 Turno**: Exigir que el subagente escriba todas las plantillas del shard en un único turno.
  - Suministrar ejemplos sintácticos canónicos con raw strings `r"..."` en el bundle del shard para erradicar errores de escape de backslashes (`\frac`, `\beta`).

---

### Diagnóstico 2: Straggler Effect en la Barrera de Sincronización
- **Síntoma**: De 6 subagentes en paralelo, 5 terminan en 120s, pero uno tarda 450s, bloqueando el avance del Director.
- **Causa Raíz**:
  - Desequilibrio en la complejidad pedagógica del shard (ej. un shard contiene competencias de alta densidad matemática o 12 distractores en grafo denso).
  - Shards particionados con tamaño desigual.
- **Solución Recomendada**:
  - Ajustar el particionador en `plan_shards.py` para usar granularidad adaptativa (4 competencias para grafos densos de distractores en lugar de 8 fijas).
  - Establecer un límite duro de turnos (`max_turns: 15`) en la configuración del subagente para forzar rescate rápido en caso de estancamiento.

---

### Diagnóstico 3: Fricción en Herramientas (Tool Errors >= 3)
- **Síntoma**: Comandos de consola o llamadas de lectura que arrojan código de salida $\neq 0$ o errores de archivo no encontrado.
- **Causa Raíz**:
  - El subagente intenta navegar directorios fuera de su SCOPE-LOCK.
  - Comandos lanzados con sintaxis de PowerShell incompatibles (ej. `/b` o comillas sin escapar).
- **Solución Recomendada**:
  - Asegurar que las rutas de archivo inyectadas en los bundles sean absolutas o canónicas respecto a la raíz del espacio de trabajo.
  - Bloquear herramientas no requeridas (ej. `list_dir`, `search_web`) en la definición del subagente `define_subagent` restringiendo los tool groups.

---

### Diagnóstico 4: Inflación de Tokens en el Director (Context Bloat)
- **Síntoma**: El Director acumula $> 1.5M$ de tokens de entrada en sus últimos turnos.
- **Causa Raíz**:
  - El Director lee archivos intermedios pesados completos (`corpus.md`, `cta.json`, `course.json`) con `view_file` en lugar de delegar la lectura a subagentes o verificar salidas sintéticas vía CLI.
- **Solución Recomendada**:
  - Aplicar el principio de **Director Orquestador Puro**: el Director solo lee los resúmenes CLI de `run.py` (código de salida y líneas de resumen de gates). Prohibido inspeccionar manualmente JSONs de más de 50 KB en el hilo principal.
