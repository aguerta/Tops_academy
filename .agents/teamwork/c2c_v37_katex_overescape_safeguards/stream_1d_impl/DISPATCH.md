# DISPATCH — Stream 1D (Fase 1: Implementador)

- **Parent Conversation ID:** `da4d9acf-34da-4bc8-930b-6fb3d28b5744`
- **Stream Folder:** `d:\Augusto\personal_portfolio\Tops_academy\.agents\teamwork\c2c_v37_katex_overescape_safeguards\stream_1d_impl`

## Frontera Exclusiva de Escritura (`Exclusive Write Boundary`)
SOLO tienes permiso de escritura sobre:
1. `d:\Augusto\personal_portfolio\Tops_academy\run_platform.py`
2. `d:\Augusto\personal_portfolio\Tops_academy\FUTURE_MILESTONES.md`
3. `d:\Augusto\personal_portfolio\Tops_academy\docs\future_milestones\FUTURE_MILESTONES.md`
4. `d:\Augusto\personal_portfolio\Tops_academy\tests\test_platform_katex_admission_guard.py` `[NEW]`
5. `d:\Augusto\personal_portfolio\Tops_academy\.agents\teamwork\c2c_v37_katex_overescape_safeguards\stream_1d_impl\BRIEFING.md` `[NEW]`
6. `d:\Augusto\personal_portfolio\Tops_academy\.agents\teamwork\c2c_v37_katex_overescape_safeguards\stream_1d_impl\handoff.md` `[NEW]`

PROHIBIDO tocar cualquier otro archivo.

## Especificación Técnica

### 1. `run_platform.py`
Implementa el **Guardián de Admisión en Runtime (Punto 4 del Protocolo de Protección Definitivo)**:
1. Añade una función determinista `repair_platform_course_katex(content: str) -> tuple[str, int]`:
   - En el texto JSON crudo `content`, reemplaza secuencias de 4 barras seguidas de comando alfabético (`r"\\\\\\\\([a-zA-Z]+)"` -> `r"\\\\\1"`), reemplaza `r"\\\\centernot\s*\\\\(?:Rightarrow|implies)\b"` -> `r"\\\\nRightarrow"` (y `r"\\\\centernot\b"` -> `r"\\\\not"`), y repara `\\text{textVar[barx_n] = O(n)}` -> `\\text{Var}[\\bar{x}_n] = O(n)`.
   - Preserva intactos los saltos de fila legítimos en matrices (`\\\\ ` seguidos de espacio, dígito, signo o corchete).
   - Retorna `(repaired_content, total_fixes_applied)`.
2. En `validate_platform_course(content: str) -> tuple[bool, dict | str]`:
   - En **Pass 1 (Raw lexical check)**, además de `control_char_regex`, verifica si existen secuencias de sobreescape KaTeX en el JSON crudo (`overescape_match = re.search(r"\\\\\\\\([a-zA-Z]+)", content)`) o `\\centernot` (`re.search(r"\\\\centernot\b", content)`):
     - Si detecta sobreescape: retorna `(False, f"Contains over-escaped LaTeX command sequence '\\\\\\\\{overescape_match.group(1)}' (R-23)")`.
     - Si detecta `\centernot`: retorna `(False, "Contains unsupported KaTeX macro '\\\\centernot' (R-23)")`.
   - En **Pass 4**, al iterar sobre `questions`, verifica también que los campos textuales en memoria (`stem`, `detailed_solution`, `solution`, `hints`, `options[*].content`, `options[*].error_rationale`) no contengan `r"\\\\([a-zA-Z]+)"` ni saltos `\\` dentro de bloques inline `$ ... $` fuera de entornos `\begin{...matrix|cases|aligned|array|split|gathered}... \end{...}`.
3. En `scan_courses() -> list[dict]`:
   - Al leer cada archivo `f` en `COURSES_DIR`, si `validate_platform_course(content)` falla con mensaje que contenga `"R-23"`, invoca `repaired_content, fixes = repair_platform_course_katex(content)`. Si `fixes > 0`, vuelve a validar `is_valid, payload = validate_platform_course(repaired_content)` y, si pasa, persiste `f.write_text(repaired_content, encoding="utf-8")` para auto-reparar el curso antes de servirlo al cliente web.

### 2. `FUTURE_MILESTONES.md` y `docs/future_milestones/FUTURE_MILESTONES.md`
En la sección `5. Salvaguarda Anti-Sobreescape y Validación Léxica KaTeX en JSON` -> `Protocolo de Protección Definitivo (Safeguards a Implementar)` (líneas ~280-284 en ambos archivos, manteniéndolos 100% sincronizados):
- Actualiza el encabezado a `Protocolo de Protección Definitivo (Safeguards Implementados — ✅ COMPLETADO):` y marca cada uno de los 4 numerales (`1.` a `4.`) con `✅ **IMPLEMENTADO:**` detallando brevemente el módulo y regla aplicados (`R-23` en `lexical_scanner.py`, `rules.py`, `invariants.py`; `sanitize_katex_syntax` en `assemble.py` + `compile_shard.py`; invariante inline `\\` en `$ ... $`; y Guardián de Admisión + auto-reparación en `run_platform.py`).

### 3. `tests/test_platform_katex_admission_guard.py`
Crea una suite de pruebas verificando:
- `validate_platform_course` rechaza JSON con `\\\\frac`, `\\\\text`, `\\\\to`, `\\\\mathbb`, `\\\\right`, `\\\\alpha`, `\\\\centernot` y `$a \\ b$` inline fuera de matriz, reportando `R-23`.
- `validate_platform_course` acepta JSON con matrices `\begin{bmatrix} 1 & 2 \\ 3 & 4 \end{bmatrix}` y `\begin{pmatrix} 0 & 1/2 \\ 1/2 & 0 \end{pmatrix}` en modo inline `$ ... $` y display `$$ ... $$`.
- `repair_platform_course_katex` repara deterministamente `\\\\frac`, `\\\\to`, `\\\\centernot\\\\Rightarrow` y preserva intactos los saltos `\\\\ ` de matrices.
- `scan_courses` (usando `monkeypatch` sobre `COURSES_DIR` con un directorio temporal) auto-repara un curso con sobreescape `R-23` y lo sirve como `"status": "valid"`.
- Los 4 cursos reales en `courses/*.json` pasan `validate_platform_course` al 100%.

## Verificación
Ejecuta:
```powershell
pytest tests/test_platform_katex_admission_guard.py tests/test_platform.py -q
```
Escribe `BRIEFING.md` antes de editar, `handoff.md` al terminar y responde con `DONE:: Stream 1D Impl completado`.
