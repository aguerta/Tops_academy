# HANDOFF: Experimento P1.4 (K=4 estable) — estadistica_3, Arms A/B/C/D

Estado a las 13:55 (local, 2026-11-27). Todo lo de abajo fue observado en archivos/salidas salvo lo marcado **[NO VERIFICADO]**.

## 1. Objetivo
Hacer que C2C con `K=4` (`templates_per_modality=4`) sea tan estable en costo y tiempo como `K=3`. Meta-análisis previo: `C:\Users\augus\.gemini\antigravity\brain\08e90bb9-fbc8-4fbc-924f-9d1ae8002060\meta_analysis_k3_vs_k4.md`. Diseño del experimento: `...\brain\08e90bb9-...\experiment_p1_4_k4_hab_structure.md`.
Orden del usuario: ejecutar el experimento completo, SOLO en `estadistica_3` (no `mateco_4` hasta su visto bueno), comparar A/B/C/D y dar Go/No-Go.

## 2. Reglas duras
- Un arm a la vez, NUNCA en paralelo (HTTP 429 de cuota).
- NO tocar `content/` (inmutable).
- course_id distinto por arm. El `cta.json` congelado es idéntico en todos (copiado de `courses/estadistica_3_test_k4/work/cta.json`).
- Sin commitear: los cambios de código P1.4 están sin commit (ver `git status`). Pedir permiso antes de commitear.
- PowerShell: sin `&&` (usar `;`), sin `rg`, pytest con `-n 0`, Python en `.venv\Scripts\python.exe`. Evitar `\"` anidados en `python -c`.

## 3. Arms
| Arm | Qué cambia | course_id / work_dir |
|---|---|---|
| A | Control: K=4 plano | `est3_exp_arm_a` |
| B | Tope M<=3 con K>=4. **Equivale a A** en estadistica_3 (las 23 competencias tienen `len(recommended_modalities)==3`). No se corre. | — |
| C | `--split-heavy-skills`: skill de una sola competencia con >=12 plantillas se parte en `shard_XXa/b` (part1: direct_recall, multi_step_calc; part2: perturbation, boundary_or_edge_case; K=ceil(K/2)) | `est3_exp_arm_c` |
| D | `--adaptive-k`: skills K, concept/fact min(3,K) | `est3_exp_arm_d` |

Los flags se leen del manifest/shards ya planificados; NO pasarlos de nuevo al workflow.

## 4. Estado por arm
### Arm A — HECHO (certificado y publicado)
- QA 19.9/20 (PLATINUM), MPRI 100, 23 competencias.
- Wall 85.97 min, compute 176.20 min, speedup 2.05x; costo $19.40; tokens activos 6,532,949 (total 41,939,576).
- Autores (25 shards): min/med/max 109/155/219 s (straggler shard_16); costo $8.78. Reparaciones: 4 ($0.58). Jueces: 12, 143 ítems, 100% acuerdo, $1.62. Orquestador $7.49.
- Mezcla: MC7 0%, FIB 11.81%, MS 16.46%, M20 71.73%. Warning BLOOM-SUPERIOR-TARGET 64.5%.
- **Contaminado**: 2 pausas por cuota y ~71 intervenciones manuales (según auditor). El conteo de preguntas del Run Auditor salió 0; calcular desde `courses/est3_exp_arm_a.json`.
- Artefactos: `reports/qa_audits/est3_exp_arm_a_qa_report.md`, `reports/c2c_audits/20261127_134710_est3_exp_arm_a_08e90bb9/{report.md,telemetry.json}`, `courses/est3_exp_arm_a.json`.

### Arm C — PAUSADO por cuota 429 (task-424)
- Workflow abortó con "completed 20/27 workers"; cuota reinicia ~4h52m después de ~13:53 (≈18:45 local). **No relanzar antes**: **[verificar con el usuario que la cuota ya reinició]**.
- En `courses/est3_exp_arm_c/work/templates/` hay 25 archivos: C-01..C-08 y `Hab-*__part*.json`. **Faltan**: `Hab-02__part1`, `Hab-06__part2`, `Hab-10__part2` (los 3 shards pendientes de autoría, más posiblemente 4 hasta llegar a 27 shards — contar con `shards/` vs `shards/*.cert.json`; hay 27 shard JSON y 21 `.cert.json` al momento del chequeo).
- `run.py` ya contiene el merge de `__part*.json` → `<cid>.json` (en torno a L1097-1105, dentro de `run_stage_templates`). **[NO VERIFICADO que funcione end-to-end]**: ver si también se aplica en `run_stage_build` y si el chequeo `missing_cids` (~L1102) pasa. Si Stage 3/4 falla con "missing templates", ahí está la causa; el merge debe producir `templates/<cid>.json` con `{"competency_id", "templates":[...]}`, IDs únicos (part2 offset +6), y borrar los parts.

### Arm D — PENDIENTE (dir preparado, 17 shards, `adaptive_k=True`). Correr solo después de terminar y publicar C.

## 5. Comandos
Reanudar Arm C (misma config; la lógica solo relanza shards sin `shard_XX.cert.json`):
```
run_workflow ScriptPath=d:/Augusto/personal_portfolio/Tops_academy/.agents/skills/content-to-course/workflows/c2c_wave_workflow.py
Args={"author_concurrency":9,"mode":"post_cta_pipeline","templates_per_modality":4,"work_dir":"courses/est3_exp_arm_c/work"}
```
Si llega a jueces/reparaciones y cae por cuota: mismo Args con `"mode":"repair_and_rejudge"` (así se reanudó Arm A).
Al terminar el workflow (por arm X = c, luego d):
```
.venv\Scripts\python.exe .agents\skills\content-to-course\run.py --stage certify --work-dir courses\est3_exp_arm_X\work
.venv\Scripts\python.exe .agents\skills\content-to-course\run.py --stage publish --work-dir courses\est3_exp_arm_X\work --course-id est3_exp_arm_X
```
Arm D: mismo Args cambiando `work_dir` a `courses/est3_exp_arm_d/work`.
Tests (deben dar 16 passed): `.venv\Scripts\python.exe -m pytest tests/pipeline/test_c2c_hardening_workflow.py tests/pipeline/test_p1_4_shard_arms.py -n 0 -q`

## 6. Cambios de código P1.4 (sin commit)
- `plan_shards.py`: `split_heavy_skills`, `adaptive_k`, flags CLI `--split-heavy-skills`, `--adaptive-k`.
- `compile_shard.py`: K/min_archetypes por shard; nombres `<cid>__part<N>.json`; IDs con offset `(part-1)*6`.
- `run.py` (`run_stage_templates`): K por shard, lookup de `__part`, merge de parts.
- `dispatch.py`: contrato stage4 por shard, aviso `[SPLIT-SHARD PART n/2]`, compile con K/min-arch por shard.
- `workflows/c2c_wave_workflow.py`: `_find_pending_shards` considera hecho si existe `shard_XX.cert.json` no vacío (o `shard_XX.json` con clave `"templates"`).
- Test nuevo: `tests/pipeline/test_p1_4_shard_arms.py`.
- Hay además muchos otros archivos modificados de sprints 1-2 (budget_guard, judge, cta_merge, etc.), también sin commit.

## 7. Entregable final
Escribir `C:\Users\augus\.gemini\antigravity\brain\08e90bb9-fbc8-4fbc-924f-9d1ae8002060\experiment_p1_4_results.md` con comparación A vs C vs D (B≡A): QA, wall, compute, costo, tokens activos, tiempo de autores (min/med/max, straggler), costo Stage 3, reparaciones, desacuerdos de jueces, preguntas (desde `courses/<id>.json`) y QPM. Comparar con históricos: `estadistica_3_test_k4` (18.45/20, 948 preg, $10.67, 34.29 QPM) y `estadistica_3_test_k3` (17.70/20, 666 preg, $8.39, 43.39 QPM). Declarar la contaminación por cuota (usar tiempos/costos por etapa, no wall total). Incluir Go/No-Go. Reportar solo números observados. No correr `mateco_4` sin aprobación.

---

# ANEXO: Contexto resumido del meta-análisis K3 vs K4

> Documento fuente completo (leer ante dudas): [meta_analysis_k3_vs_k4.md](file:///C:/Users/augus/.gemini/antigravity/brain/08e90bb9-fbc8-4fbc-924f-9d1ae8002060/meta_analysis_k3_vs_k4.md) (v2.0, corregido por auditoría escéptica). Diseño del experimento: [experiment_p1_4_k4_hab_structure.md](file:///C:/Users/augus/.gemini/antigravity/brain/08e90bb9-fbc8-4fbc-924f-9d1ae8002060/experiment_p1_4_k4_hab_structure.md).

**Base:** 7 corridas del 2026-11-27 (pares K3/K4 de solow, estadistica_3, mateco_4 + rincon_only_k3). Evidencia direccional (n=3 pares, corridas con carga solapada), no estadística cerrada.

**Conclusión:** K4 mejora el costo unitario (−8.7% a −18.1% $/plantilla; −10.3% a −16.8% $/pregunta). El problema es el **riesgo de cola** en costo y tiempo: p. ej. estadistica_3 K3 $8.39/15.4 min/QA 17.70 vs K4 $10.67/27.7 min/QA 18.45; mateco_4 K3 $11.60 vs K4 $24.34.

**Causas raíz y estado**
| Causa | Estado |
|---|---|
| Explosión CTA multi-PDF (mateco_4: 27→57 competencias, truncamiento del Harmonizer, bug `rec_min>rec_max`) | P0.1 hecho |
| Fatiga de generación monolítica en `Hab-*` (Pass-1 21.7% vs 49.1% en C/H; shards de 40–60 KB) | **P1.4 = este experimento**; P0.5/P1.1/P1.2 hechos |
| Falsos `kernel_override` en M20 y falta de LQAS en rejudge | P0.3, P0.4 hechos |
| Código muerto Stage 6B | P0.3 hecho |
| Barreras síncronas `batch=9` | P0.2 hecho (`Semaphore(9)`) |
| Sin circuit-breaker 429 ni presupuesto por curso | P1.3 hecho |
| P2.1–P2.3 (doble punto `..`, `allow_calculator`, muestreo de jueces) | NO hechos |

**Qué decide el experimento:** si dividir las skills pesadas (Arm C) o usar K adaptativo (Arm D) sube el Pass-1 de `Hab-*` (línea base 21.7%, objetivo 50–60%) y estabiliza costo/tiempo.

**Criterio Go/No-Go (estadistica_3, K4 estabilizado):** costo $9.30–$10.80, wall 14–18 min, 1–2 rondas de repair, Pass-1 50–60%. Los wall de A y C están contaminados por pausas de cuota; comparar por etapa.

**Advertencias:** no relajar `TPL-STEM-EQUATION-PARITY`; no subir concurrencia a 12; no tocar solo `assemble.py` para `allow_calculator`; el 429 es de la cuenta, por eso un arm a la vez.
