# Handoff — Stream 2D (Tests Automatizados Frente B: Manifest y Carga de Cursos)

**Fecha:** 2026-10-26  
**Stream:** 2D Tests  
**Estado:** COMPLETO (12/12 tests PASS en 1.45 s)

---

## 1. Resumen de Entregas

Se implementó el archivo [`tests/test_course_api_manifest.py`](file:///d:/Augusto/personal_portfolio/Tops_academy/tests/test_course_api_manifest.py) para validar de forma rigurosa y automatizada todos los criterios de aceptación del Frente B (AC-19, AC-22, AC-24, AC-25).

### Cobertura de Pruebas Implementada

1. **`TestCourseIndexContract` (Módulo `platform/server/courseIndex.cjs`):**
   - `test_course_index_file_exists`: Comprueba la existencia del módulo.
   - `test_get_manifest_structure_and_size`:
     - Valida que `getManifest()` devuelve un objeto con propiedad `courses`.
     - Valida que el tamaño JSON del manifest es **< 50 KB** (objetivo medido real: **2.52 KB**, muy inferior a 10 KB).
     - Valida estrictamente que **NINGÚN** elemento en `courses` tiene la clave `data`.
     - Valida los 9 campos requeridos en cada elemento: `id`, `filename`, `title`, `description`, `status`, `total_competencies`, `total_questions`, `bytes`, `etag`.
   - `test_get_course_data_valid_course`:
     - Valida que `getCourseData(id)` retorna el objeto completo con `competencies` y `questions` (con conteo > 0) y su `etag`.
   - `test_build_index_warm_cache_performance`:
     - Valida que `buildIndex()` se ejecuta en **< 100 ms** con caché caliente (medición real en Node: < 15 ms).
     - Valida que utiliza `cachedHits` y no re-parsea archivos innecesariamente (`parseCount == 0`).
   - `test_corrupted_json_handled_gracefully`:
     - Valida resiliencia en directorio temporal con archivos sintácticamente inválidos o con caracteres de control ilegales.
     - Confirma que se reportan como `status: "error"` con `error_message` descriptivo, sin tumbar el proceso ni alterar los cursos válidos.

2. **`TestCourseServerHttp` (Servidor HTTP `platform/server/courseServer.cjs`):**
   - `live_course_server`: Fixture que levanta una instancia efímera de `courseServer.cjs` en un puerto local dinámico libre (`PORT` asignado aleatoriamente por socket) y espera el endpoint `/healthz`.
   - `test_get_api_courses_and_courses_json_slim`:
     - Valida tanto `GET /api/courses` como `GET /api/courses.json`.
     - Confirma respuesta 200, Content-Type JSON, presencia de cabecera `ETag`, tamaño < 50 KB y ausencia de propiedad `data`.
   - `test_get_single_course_detail_with_etag`:
     - Valida `GET /api/courses/:id` devolviendo el curso individual con su cabecera `ETag` y sus preguntas.
   - `test_conditional_if_none_match_returns_304`:
     - Valida que enviar `If-None-Match` con el `ETag` actual tanto en `/api/courses` como en `/api/courses/:id` retorna **`304 Not Modified`** sin retransmitir payload.
   - `test_healthz_endpoint`:
     - Valida `GET /healthz` devolviendo 200 con `status: "ok"`, `pid`, `uptime_seconds` y métricas.
   - `test_non_existent_course_returns_404`:
     - Valida respuesta 404 ante solicitudes a cursos inexistentes.

3. **`TestBuildAndTemplates` (Build y Plantillas HTML):**
   - `test_platform_index_html_contains_manifest_marker_or_script`:
     - Valida que `platform/index.html` contiene `<!--COURSE_MANIFEST-->` o `<script id="course-manifest" type="application/json">`.
   - `test_dist_api_courses_json_slim_and_no_data`:
     - Valida que `platform/dist/api/courses.json` pesa **< 100 KB** (medido: **2.52 KB**, reduciendo en un 99.996% los 59.8 MB previos) y que no contiene el campo `data` incrustado en ningún curso.

---

## 2. Decisiones Técnicas y Hallazgos

1. **Subprocess Node Encoding:**
   - En Windows, `subprocess.run(..., text=True)` utiliza por omisión la codificación `cp1252`, lo que provocaba fallos de decodificación con símbolos matemáticos y caracteres UTF-8 en los cursos. Se configuró explícitamente `encoding="utf-8"` en todos los pipes de subprocess.
2. **Asignación de Puertos Efímeros:**
   - Para evitar colisiones en `PORT=5173`, la suite HTTP solicita un puerto libre al sistema operativo mediante socket bind (`port 0`), levantando `courseServer.cjs` aislado en ese puerto específico y esperando su disponibilidad en `/healthz`.
3. **Manejo de HTTP 304:**
   - Se gestiona la excepción nativa `urllib.error.HTTPError` que lanza Python al recibir respuestas con código `304`, verificando `e.code == 304`.

---

## 3. Verificación de Resultados

- `.\pytest.cmd -v tests/test_course_api_manifest.py`:
  - **12 passed in 1.45s (100% PASS)**.
- `.\pytest.cmd -q` (Suite completa del repositorio):
  - **1145 passed, 1 skipped** (0 failures).
- `npm run build` en `platform/`:
  - **PASS** (código 0 en 5.63s), emitiendo `dist/api/courses.json` de **2.52 kB** (gzip: **0.76 kB**).
- Frontera de escritura respetada estrictamente:
  - Solo se crearon/modificaron: `tests/test_course_api_manifest.py`, `stream_2D/BRIEFING.md` y `stream_2D/handoff.md`.
