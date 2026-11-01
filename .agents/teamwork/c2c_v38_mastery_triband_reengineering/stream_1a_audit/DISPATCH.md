# DISPATCH — Stream 1A (Fase 3: Auditor Forense Read-Only)

- **Parent Conversation ID:** `eecd58a3-e3a5-4adc-9cf1-0a5c9a7f5589`
- **Stream Folder:** `d:\Augusto\personal_portfolio\Tops_academy\.agents\teamwork\c2c_v38_mastery_triband_reengineering\stream_1a_audit`
- **Impl Handoff:** `d:\Augusto\personal_portfolio\Tops_academy\.agents\teamwork\c2c_v38_mastery_triband_reengineering\stream_1a_impl\handoff.md`
- **Impr Handoff:** `d:\Augusto\personal_portfolio\Tops_academy\.agents\teamwork\c2c_v38_mastery_triband_reengineering\stream_1a_impr\handoff.md`

## Frontera Exclusiva de Escritura (`Exclusive Write Boundary`)
SOLO tienes permiso de escritura sobre:
1. `d:\Augusto\personal_portfolio\Tops_academy\.agents\teamwork\c2c_v38_mastery_triband_reengineering\stream_1a_audit\audit_report.md` `[NEW]`

PROHIBIDO tocar cualquier archivo de producción o `tests/`.

## Protocolo de Auditoría Forense (Stream 1A)
*(Nota de concurrencia Gate 1: los Streams paralelos `1B, 1C, 1D` continúan activos sobre sus fronteras disjuntas; `git status` mostrará cambios legítimos en sus archivos).*

1. **Higiene y Frontera de Stream 1A:**
   - Ejecuta `git status --short` y verifica cero scripts temporales sueltos ni `.c2c_subagent_lock.json` activos en el workspace, y que los cambios de `Stream 1A` se limiten a `partition_corpus.py`, `ingest.py`, `prepare.py`, `compile_cta.py`, `cta_merge.py`, `check_cta.py` y sus 7 suites asignadas.
2. **Inspección de Código en Producción (`read_file` en bloques amplios `400-800` líneas):**
   - `partition_corpus.py` / `ingest.py` / `prepare.py`: confirma `MAX_DIRECT_PAGES = 25`, promoción automática `> 25` págs o multi-PDF a `mapreduce`, `k_parts = max(2, ceil(P/20))` sin tope de 4, emisión completa de claves compatibles en `pre_cta_manifest.json` (con `.as_posix()`), y `"existing_competencies"` en `delta_manifest.json` (`--append`).
   - `cta_merge.py`: confirma simetría absoluta (`merge_cta_parts` **jamás** escribe `work/cta.json` ni `work/cta.md` para `1` o `N` partes), `prepare_harmonize_from_single_draft` exportada y funcional, `JACCARD_DUPLICATE_THRESHOLD = 0.30` sin filtro `type1 == type2`, y `apply_harmonize` leyendo `"duplicate_decisions"` sin candado Jaccard, soportando absorción `[BASE]` en `--append` y `check_prerequisites_dag(..., allowed_prereq_ids=existing_competency_ids)`.
   - `check_cta.py` / `compile_cta.py`: confirma Fail-Fast `[KATEX-PROSE-OVERFLOW]` (llaves balanceadas, `<= 45` pasa, `>= 46` falla con `[KATEX-PROSE-OVERFLOW]`, nunca `R-23`, cubriendo `name`, `description`, `description_latex`, `source_examples` y los 6 campos de distractor), `connected_components == 1` (con ancla virtual `"__BASE_COURSE__"` en `--append`) y `num_roots <= max(1, floor(0.20 * N))`.
   - Confirma **0 subcadenas Zero-Domain prohibidas** en los 6 archivos `.py` de `Stream 1A` (`edo`, `pde`, `derivadas`, `jacobiana`, `eigen`, `euler`, `cobb_douglas`, `lotka`, `lagrange`, `regresi`).
3. **Inspección de Tests y Ejecución Independiente:**
   - Verifica las 7 suites contra aserciones debilitadas o falsos positivos y ejecuta:
     ```powershell
     & ".venv\Scripts\python.exe" -m pytest tests/test_cta_mapreduce.py tests/test_cta_merge_prereq_scoping.py tests/test_c2c_v321_comp1_cta.py tests/test_cta_healing.py tests/test_cta_sweetspot_and_autoheal.py tests/test_fast_ingest_and_cta_append.py tests/test_handouts.py -q
     ```
4. Escribe `audit_report.md` en `stream_1a_audit/` y envía `PASS:: Stream 1A (<N> passed)` o `REJECT:: Stream 1A | <archivo:línea> | <causa>` a `eecd58a3-e3a5-4adc-9cf1-0a5c9a7f5589`.
