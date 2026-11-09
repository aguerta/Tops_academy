# Content-to-Course (C2C v3.3): Informe de Síntesis Forense Transversal
## Auditoría Agéntica Concurrente Multicorrida (3 Agentes Lead Especializados)

> **Fecha:** 2026-11-09  
> **Orquestador:** Chief Forensic Orchestrator (`c2c-run-auditor` v3.3)  
> **Modo Operativo:** Modo 3 — Orquestación Jerárquica Paralela (3 Subagentes Lead dedicados)  
> **Estado:** **APROBADO CON RECOMENDACIONES DE INFRAESTRUCTURA Y ENRUTAMIENTO**

---

## 1. Resumen Ejecutivo y Metodología Forense

La presente auditoría fue ejecutada bajo el protocolo **Modo 3 (Jerárquico Paralelo)** del skill `c2c-run-auditor`. Se analizaron tres corridas críticas de generación de cursos en la plataforma Top's Academy que representan tanto variaciones arquitectónicas fundamentales (**Direct CTA vs. MapReduce CTA** sobre el mismo corpus) como pruebas de esfuerzo a gran escala (**Multi-Documento Masivo con 75 subagentes**):

1. **Corrida 1 (`66915882`):** `saul_pc_sistemas_de_ecuaciones_vmapreduce5` — Pipeline MapReduce masivo sobre 6 PDFs académicos (93 páginas, 4.23 MB), 61 competencias, 1,490 preguntas. Auditado por *Forensic Lead Auditor 1* (`0b6a822a`).
2. **Corrida 2 (`3981c7eb`):** `solow_new_pipeline_mapreduce` — Pipeline MapReduce sobre el Modelo de Crecimiento de Solow (36 páginas, 1.49 MB), 21 competencias, 500 preguntas. Auditado por *Forensic Lead Auditor 2* (`c1b83174`).
3. **Corrida 3 (`539b37fa`):** `solow_new_pipeline_direct` — Pipeline Direct sobre el Modelo de Crecimiento de Solow (36 páginas, 1.49 MB), 15 competencias, 350 preguntas. Auditado por *Forensic Lead Auditor 3* (`f838b837`).

---

## 2. Matriz Comparativa Transversal de Telemetría y Rendimiento

| Dimensión / Métrica | Run 3: Solow Direct (`539b37fa`) | Run 2: Solow MapReduce (`3981c7eb`) | Run 1: Sistemas Ecuaciones MR (`66915882`) |
| :--- | :---: | :---: | :---: |
| **Arquitectura CTA** | **Direct (1 Architect)** | **MapReduce (3 Mappers + 1 Harm)** | **MapReduce (7 Mappers + 1 Harm)** |
| **Carga de Entrada (Workload)** | 2 PDFs / 36 pág (1.49 MB) | 2 PDFs / 36 pág (1.49 MB) | 6 PDFs / 93 pág (4.23 MB) |
| **Rendimiento Curricular** | 15 competencias (5H, 6C, 4H) | 21 competencias (7H, 9C, 5H) | 61 competencias (27H, 26C, 8H) |
| **Volumen de Preguntas Validadas**| 350 preguntas (10 shards) | 500 preguntas (15 shards) | 1,490 preguntas (44 shards) |
| **Tiempo de Pared ($T_{\text{wall}}$)** | **18.83 min** (1,130 s) | **41.88 min** (2,513 s) | **67.63 min** (4,058 s) |
| **Tiempo Cómputo ($T_{\text{compute}}$)** | 84.70 min (5,082 s) | 162.50 min (9,750 s) | 419.57 min (25,174 s) |
| **Factor de Speedup Concurrente** | **4.50x** | **3.88x** | **6.20x** |
| **Tokens Totales (Facturación)** | **11,155,512** | **33,418,639** | **83,906,248** |
| **Tokens Activos (In + Out)** | 2,351,164 | 4,111,291 | 12,558,734 |
| **Cache Read Tokens / Tasa Hit** | 8.80M (**78.9%**) | 29.31M (**87.7%**) | 71.35M (**85.0%**) |
| **Tokens Totales / Pregunta** | **31,872.9** tok/preg | **66,837.3** tok/preg | **56,312.9** tok/preg |
| **Tokens Activos / Pregunta** | **6,717.6** tok/preg | **8,222.6** tok/preg | **8,428.7** tok/preg |
| **Latencia / Pregunta ($T_{\text{wall}}$)**| **3.23 s/preg** | **5.03 s/preg** | **2.72 s/preg** |
| **Throughput de Generación (QPM)**| **18.58 preg/min** | **11.94 preg/min** | **22.03 preg/min** |
| **Subagentes Desplegados** | 16 subagentes | 26 subagentes | 75 subagentes |
| **Shard Clean-Room (Gold Standard)**| `shard_08` (230s, 0 reintentos) | `shard_02` (201s, 0 reintentos) | `shard_27` (174s, 0 reintentos) |
| **Top Straggler de Shards** | `shard_06` (472s, Post-compile) | `shard_01` (719s, Post-compile) | `shard_14` (796s, Post-compile) |
| **Errores Catalogados** | 15 (0 supervisor) | 27 (0 supervisor) | 68 (8 supervisor fixes) |
| **Veredicto Jueces Ciegos (Pase 1)**| **100%** (60/60 ítems) | **100%** (84/84 ítems) | **100%** (120/120 ítems) |

---

## 3. Hallazgos Forenses Clave y Análisis Arquitectónico

### 3.1. Duelo Direct vs. MapReduce en Corpus Idéntico (Solow 36 Páginas): El Efecto Látigo (Bullwhip Effect)
La comparación controlada entre `solow_new_pipeline_direct` y `solow_new_pipeline_mapreduce` (mismo documento fuente de 36 páginas, mismos modelos) aporta una evidencia concluyente sobre el coste de particionamiento:

1. **Ventaja de Direct en Latencia y Coste:**
   - `solow_direct` finalizó en **18.83 minutos**, superando a `solow_mapreduce` (41.88 min) por un factor de **2.22x en velocidad**.
   - Direct consumió **11.15M tokens vs 33.42M tokens**, logrando un **ahorro neto del 66.6% en tokens totales** (22.2M tokens evitados) y un costo por pregunta de 31,872 vs 66,837 tokens/item (**2.10x más eficiente**).
2. **El Mecanismo del Efecto Látigo (Bullwhip Effect):**
   - Al aplicar MapReduce a un documento de 36 páginas, los 3 mappers fragmentaron el corpus y sobre-granularizaron el mapa de competencias (21 competencias vs. 15 en Direct).
   - Esta sobre-fragmentación obligó a desplegar 15 shards de autoría en lugar de 10. La mayor contención en la barrera de sincronización y la necesidad de inventar micro-distractores teóricos para conceptos hiper-específicos detonó un straggler severo (`shard_01` con 719s de pared frente a 472s en Direct).
3. **Conclusión de Enrutamiento:**
   - Para documentos de longitud baja o media ($\le 50$ páginas), **Direct CTA es inequívocamente superior** en tiempo, coste y cohesión temática. MapReduce debe reservarse exclusivamente para corpus extensos ($> 50$ páginas).

### 3.2. Rendimiento en Ultra-Escala (Sistemas de Ecuaciones 93 Páginas, 75 Subagentes)
- La corrida `saul_pc_sistemas_de_ecuaciones_vmapreduce5` demostró la capacidad de escala del motor: generó **1,490 preguntas validadas en 67.63 minutos**, alcanzando el mayor throughput del sistema (**22.03 QPM**) y el menor tiempo de pared por pregunta (**2.72 segundos/pregunta**), con un factor de aceleración paralela de **6.2x**.
- **Mapeo MapReduce Óptimo:** La división en 7 mappers concurrentes (262s máximo) + 1 armonizador (140s) resolvió la ingesta de 6 PDFs complejos en sólo 6.7 minutos.

---

## 4. Patología Común: La Trampa de Remediación Post-Compilación

El análisis comparativo de los perfiles de tiempo (`shard_timing_profile.json`) revela un patrón patológico universal en las tres corridas:

```
[Clean-Room Standard]  |=================== Pre-Compile (170-220s) ===================|=> [Pass 1] (15s) -> Fin: ~200s
[Straggler Path]       |==== Pre-Compile (175-260s) ====|xx Compile Fail 1 xx|-- edit --|xx Compile Fail 2 xx| ... -> Fin: 470-796s
```

1. **El tiempo de redacción inicial (Pre-Compile) es homogéneo:**
   - Shard Clean-Room `shard_27` (Saul): Pre-compile = 173.0s.
   - Straggler Crítico `shard_14` (Saul): Pre-compile = 175.0s (idéntico al Clean-Room).
   - Shard Clean-Room `shard_02` (Solow MR): Pre-compile = 194.0s.
   - Straggler `shard_01` (Solow MR): Pre-compile = 259.0s.
2. **El 65% - 80% del tiempo de los stragglers se gasta en reintentos post-compilación:**
   - `shard_14` consumió **638.0s (80.2%)** en bucles de remediación con 5 fallos y 10 micro-ediciones.
   - `shard_01` consumió **468.0s (65.1%)** en 3 fallos de compilación intentando reparar reglas de balance de distractores (`[R-18]`/`[R-15]`).
   - `shard_06` consumió **211.0s (44.7%)** depurando paridad y dynamic rationales.
3. **Causa Raíz de los Fallos:**
   - La regla psicométrica `[R-15]` (longitud de distractores) y `[R-18]`/`[R-19]` (epsilon de separación y distractores plausibles) generan falsos positivos cuando los distractores contienen fórmulas LaTeX con comandos largos (`\operatorname`, `\mathbf`).
   - Escapes de barras invertidas en cadenas Python (`\beta`, `\frac`) provocan `ValueError` al convertir números con trailing slashes.

---

## 5. Análisis de Fricción Operativa y Gobernanza (Intervenciones del Supervisor)

- **Solow Direct (`539b37fa`):** **0 intervenciones**. Autonomía del 100%.
- **Solow MapReduce (`3981c7eb`):** **0 intervenciones**. Autonomía del 100%.
- **Sistemas de Ecuaciones (`66915882`):** **8 intervenciones manuales** ("Síndrome del Orquestador Reparador"):
  - **5 modificaciones en `run.py`:** El ensamblaje de 1,490 preguntas en la Etapa 4 excedió un timeout duro de subproceso de 5 segundos, obligando al orquestador a editar el script para ampliar el timeout.
  - **3 modificaciones en `judge.py`:** Búsqueda de rutas relativas inconsistentes al evaluar `verification/judge_responses_*.json`.
  - **Impacto:** Pérdida de 87 segundos de tiempo humano y 32.5k tokens innecesarios.

---

## 6. Recomendaciones Técnicas de Nivel P0/P1 para el Pipeline C2C v3.4

### [P0] Regla Heurística de Enrutamiento Automático del Corpus (Routing Rule)
- Implementar en `run.py` / `stage_02_shard.py`:
  $$\text{Modo CTA} = \begin{cases} \text{DIRECT}, & \text{si Páginas} \le 50 \text{ y Tamaño} \le 5.0\text{ MB} \\ \text{MAPREDUCE}, & \text{si Páginas} > 50 \text{ o Múltiples Archivos Docentes} \end{cases}$$
- Evita el Efecto Látigo en cursos medianos, reduciendo costes en un 66% y acelerando el tiempo de entrega en más de 2x.

### [P0] Eliminación de Cuellos de Botella de Infraestructura en `run.py` y `judge.py`
1. **Timeout Dinámico de Ensamblaje en `run.py`:**
   $$\text{Timeout}_{\text{assembly}} = \max\left(60\,\text{s},\, 10\,\text{s} + 0.2\,\text{s} \times N_{\text{preguntas}}\right)$$
   Elimina las 5 intervenciones del supervisor en corridas masivas ($> 1,000$ preguntas).
2. **Fijación Canónica de Rutas en `judge.py`:**
   Resolver siempre `Path(args.work_dir).resolve() / "verification"`. Elimina las 3 intervenciones por rutas relativas.

### [P1] Disyuntor Post-Compilación para Shard Authors (Circuit Breaker)
- Si un autor de shard falla 2 compilaciones consecutivas o excede 240 segundos en la fase de remediación, abortar inmediatamente el subagente y derivar la plantilla directamente al grupo de **Repair Engineers (Stage 3B)**.
- **Ahorro Estimado:** Evita que `shard_14` o `shard_01` retrasen la barrera durante 10-13 minutos; reduce el camino crítico de la Etapa 3 de 796s a ~350s (**56% de reducción en el cuello de botella**).

### [P1] Linter Local AST Pre-Escritura y Normalización de LaTeX
- Incorporar una validación estricta previa a la escritura de disco que:
  1. Convierta automáticamente cadenas matemáticas a raw-strings `r"..."`.
  2. Limpie comandos de formato LaTeX (`\operatorname`, `\mathbf`, `\frac`) antes de computar los ratios de longitud de distractores en `[R-15]`.
  3. Pre-evalúe la separación de distractores numéricos ($> 1.5\%$) antes de ejecutar `compile_shard.py`.

---

## 7. Registro de Informes Detallados

Los reportes completos generados por los tres subagentes Lead se encuentran accesibles en:
- **Sistemas de Ecuaciones (MapReduce):** [`reports/c2c_audits/forensic_lead_saul_pc_sistemas_de_ecuaciones_vmapreduce5.md`](file:///d:/Augusto/personal_portfolio/Tops_academy/reports/c2c_audits/forensic_lead_saul_pc_sistemas_de_ecuaciones_vmapreduce5.md)
- **Modelo de Solow (MapReduce):** [`reports/c2c_audits/forensic_lead_solow_new_pipeline_mapreduce.md`](file:///d:/Augusto/personal_portfolio/Tops_academy/reports/c2c_audits/forensic_lead_solow_new_pipeline_mapreduce.md)
- **Modelo de Solow (Direct):** [`reports/c2c_audits/forensic_lead_solow_new_pipeline_direct.md`](file:///d:/Augusto/personal_portfolio/Tops_academy/reports/c2c_audits/forensic_lead_solow_new_pipeline_direct.md)
- **Historial Longitudinal del Repositorio:** [`reports/c2c_audits/historical_benchmark.md`](file:///d:/Augusto/personal_portfolio/Tops_academy/reports/c2c_audits/historical_benchmark.md)
