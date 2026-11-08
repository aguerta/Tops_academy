# DISPATCH — Stream 1F (Fase A: Implementador Ortogonal)

- **Parent Conversation ID:** `cbe0c4d9-d376-429c-92b2-ffaeec91ae7f`
- **Stream Folder:** `d:\Augusto\personal_portfolio\Tops_academy\.agents\teamwork\c2c_v40_formal_mas_con_menos\stream_1f_impl`

## Frontera Exclusiva de Escritura (`Exclusive Write Boundary`)
SOLO tienes permiso de escritura sobre:
1. `d:\Augusto\personal_portfolio\Tops_academy\.agents\skills\content-to-course\repair_loop.py`
2. `d:\Augusto\personal_portfolio\Tops_academy\src\validator\psychometric_checker.py`
3. `d:\Augusto\personal_portfolio\Tops_academy\src\validator\rules.py`
4. `d:\Augusto\personal_portfolio\Tops_academy\src\validator\lexical_scanner.py`
5. `d:\Augusto\personal_portfolio\Tops_academy\tests\test_validator.py`
6. `d:\Augusto\personal_portfolio\Tops_academy\tests\test_katex_overescape_validator_r23.py`
7. `d:\Augusto\personal_portfolio\Tops_academy\.agents\teamwork\c2c_v40_formal_mas_con_menos\stream_1f_impl\BRIEFING.md` `[NEW]`
8. `d:\Augusto\personal_portfolio\Tops_academy\.agents\teamwork\c2c_v40_formal_mas_con_menos\stream_1f_impl\handoff.md` `[NEW]`

PROHIBIDO tocar cualquier otro archivo.

## Guardias Obligatorias
- **Zero-Domain (`test_skill.py`):** En `repair_loop.py` NO pueden aparecer (ni siquiera en comentarios) las subcadenas en minúsculas: `edo`, `pde`, `derivadas`, `jacobiana`, `eigen`, `euler`, `cobb_douglas`, `lotka`, `lagrange`, `regresi`. Escribe comentarios en inglés.
- **Compatibilidad con Cursos Publicados (`courses/*.json`):** `test_katex_overescape_validator_r23.py` ejecuta `validate_course_content(..., strict=True)` sobre los cursos reales publicados en `courses/*.json`! Asegúrate de que cualquier nueva regla en `src/validator/` NO genere falsos positivos sobre los cursos reales publicados en `courses/*.json` (y mantén intacta la velocidad zero-copy `< 10 s` de `lexical_scanner.py`).
- **Pytest sin contención de CPU:** Usa `-o addopts=""` al correr tus 2 suites.

## Especificación Técnica (Fase 1 + Fase 2: Linters Psicométricos Anti-Gaming en `src/validator/` y `repair_loop.py` Slicing/2D)

1. **Nuevas Reglas Deterministas Reutilizables en `src/validator/rules.py` y `src/validator/psychometric_checker.py`:**
   - Exporta funciones puras rápidas (invocables tanto desde `validate_course_content` como individualmente por ítem desde Stage 3/4) que detecten:
     * **`check_vacuous_quantifiers(text)` (`R-24`):** Detecta cuantificadores ligados inmediatamente a una constante numérica literal, ej. `\forall \varepsilon = 0.05` o `\exists \delta = 0.1` (`r"\\(?:forall|exists)\s+(?:\\[a-zA-Z]+|[a-zA-Z])\s*=\s*[-+]?\d+(?:\.\d+)?"`).
     * **`check_hint_answer_leak(hints, correct_text)` (`R-25`):** Verifica que `hints[0]` y `hints[1]` (las dos primeras pistas socráticas) no filtren literalmente `correct_text` cuando `len(correct_text.strip()) >= 15` (ignorando espacios/delimitadores `$` triviales).
     * **`check_option_parenthetical_telltale(option_text)` (`R-26`):** Detecta paréntesis auto-inculpatorios en el texto visible de opciones como `(sesgo...)`, `(confusión con...)`, `(error al...)`, `(omitiendo...)`, `(despeje erróneo...)`.
     * **`check_numeric_newton_dot(text)` (`R-27`):** Detecta `\dot{5}` / `\ddot{12}` sobre literales puramente numéricos (`r"\\d?dot\{\s*[-+]?\d+(?:\.\d+)?\s*\}"`).
   - Integra estas verificaciones en `psychometric_checker.py` / `rules.py` verificando que los cursos reales publicados en `courses/*.json` sigan pasando `test_real_published_courses_zero_r23_errors` en `< 10 s` sin falsos positivos!

2. **Alineación de `repair_loop.py` con *Competence Slicing* `< 2 KB`, Matriz 2D y Esquemas Duales:**
   - Al construir lotes/órdenes de remediación en `repair_loop.py`:
     * Soporta leer tanto `"grouped_by_rule"` como `"groups"`, y tanto `"failing_shards"` como `"affected_shards"`, con `status` case-insensitive (`str(status).upper() in ("REJECTED", "FAIL", "FAILED")`).
     * Trunca/recorta el contexto por competencia a un *Competence Slice* compacto (`< 2 KB`: solo la definición, `assumptions` y distractores de la competencia afectada, jamás volcando `cta.json` completo) y adjunta la recomendación explícita de la **Matriz 2D** (`edit_file` si `1 <= errores < 6` y `affected_line_count <= 5`; `ModularSplicing` `shard_fixes/<shard>/<CID>.py` si `errores >= 6` o `affected_line_count > 5`).

3. **Pruebas Exhaustivas en `test_validator.py` y `test_katex_overescape_validator_r23.py`:**
   - Añade pruebas unitarias positivas y negativas para `R-24` (cuantificadores vacuos), `R-25` (fuga en pistas 1–2), `R-26` (paréntesis delatores), `R-27` (`\dot{5}` numérico) y `repair_loop.py` (slicing `< 2 KB`, lectura dual `grouped_by_rule`/`failing_shards` y recomendación Matriz 2D), comprobando que los cursos publicados reales sigan pasando sin regresiones.

## Verificación y Entrega
```powershell
& ".venv\Scripts\python.exe" -m pytest -o addopts="" tests/test_validator.py tests/test_katex_overescape_validator_r23.py -q
```
Escribe `BRIEFING.md` antes de editar, `handoff.md` al terminar, y envía `DONE:: Stream 1F (<N> passed)` a `cbe0c4d9-d376-429c-92b2-ffaeec91ae7f`.
