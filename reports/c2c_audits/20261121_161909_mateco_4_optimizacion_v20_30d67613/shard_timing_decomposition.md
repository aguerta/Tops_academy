### Descomposición Temporal y Forense Multi-Shard (`Pre` vs `Post` 1st Compile)
- **Total Shards Auditados:** `13` | **Mediana de Pared:** `286.0s`
- **Gold Standard Clean-Room:** `Shard Author shard_13` (`197.0s`, 0 fallos, 0 ediciones post-escritura)

| Shard | Duración Total (s) | Pre-1st-Compile (s) | Post-1st-Compile (s) | Compiles (Fails) | Edits | Errores / Códigos | Diagnóstico Causa Raíz |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- | :--- |
| **Shard Author shard_12** | `390.0s` | `157.0s` | `233.0s` | `3 (2)` | `0` | `[TPL-ORPHAN-VARS], [TPL-DRY], [VERIFIER-TAUTOLOGY-DETECTED]` | Remediación (2 fallos) |
| **Shard Author shard_09** | `345.0s` | `127.0s` | `218.0s` | `3 (2)` | `0` | `[TPL-DYNAMIC-RATIONALE], [TPL-CROSS], [TPL-STEM-VARIANT-PARITY]` | Remediación (2 fallos) |
| **Shard Author shard_10** | `321.0s` | `137.0s` | `184.0s` | `3 (2)` | `2` | `[TPL-DYNAMIC-RATIONALE], [TPL-DRY], [TPL-VAR]` | Remediación (2 fallos) |
| **Shard Author shard_04** | `314.0s` | `115.0s` | `199.0s` | `3 (2)` | `1` | `[TPL-DRY], [TPL-VAR], [TPL-ORPHAN-VARS]` | Remediación (2 fallos) |
| **Shard Author shard_01** | `312.0s` | `112.0s` | `200.0s` | `4 (3)` | `7` | `SyntaxError en shard_01_data.py (Línea 665, Columna 28): unexpected character after line continuation character , [TPL-STEM-VARIANT-PARITY], [TPL-STATIC-OPT]` | Remediación (3 fallos) |
| **Shard Author shard_03** | `298.0s` | `121.0s` | `177.0s` | `4 (3)` | `2` | `[TPL-ORPHAN-VARS], [TPL-STATIC-OPT], [TPL-VAR]` | Remediación (3 fallos) |
| **Shard Author shard_02** | `286.0s` | `125.0s` | `161.0s` | `2 (1)` | `0` | `[TPL-ORPHAN-VARS], [TPL-DRY], [TPL-VAR]` | Remediación (1 fallos) |
| **Shard Author shard_11** | `283.0s` | `136.0s` | `147.0s` | `2 (1)` | `0` | `[TPL-ORPHAN-VARS], [TPL-STEM-VARIANT-PARITY]` | Remediación (1 fallos) |
| **Shard Author shard_06** | `281.0s` | `119.0s` | `162.0s` | `3 (3)` | `1` | `[TPL-DYNAMIC-RATIONALE], [TPL-ORPHAN-VARS], [TPL-STEM-GRAMMAR]` | Remediación (3 fallos) |
| **Shard Author shard_05** | `252.0s` | `122.0s` | `130.0s` | `2 (1)` | `0` | `[TPL-DYNAMIC-RATIONALE], [TPL-STEM-VARIANT-PARITY], [INVARIANT]` | Remediación (1 fallos) |
| **Shard Author shard_08** | `249.0s` | `115.0s` | `134.0s` | `2 (1)` | `0` | `[INVARIANT], [TPL-STEM-VARIANT-PARITY], [TPL-VAR]` | Remediación (1 fallos) |
| **Shard Author shard_07** | `222.0s` | `90.0s` | `132.0s` | `3 (2)` | `7` | `[INVARIANT], [TPL-VAR], [TPL-DRY]` | Remediación (2 fallos) |
| **Shard Author shard_13** | `197.0s` | `102.0s` | `95.0s` | `2 (1)` | `0` | `[TPL-DYNAMIC-RATIONALE], [TPL-KATEX], [TPL-CROSS]` | Remediación (1 fallos) |

---

### Descomposición Temporal y Forense de Repair Engineers (Stage 3B Remediación)
- **Total Repair Engineers Auditados:** `1` | **Mediana de Pared:** `32.0s`

| Repair Engineer | Duración Total (s) | Pre-1st-Compile (s) | Post-1st-Compile (s) | Compiles (Fails) | Edits | Errores / Códigos | Diagnóstico Causa Raíz |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- | :--- |
| **Repair Engineer C-01** | `32.0s` | `17.0s` | `15.0s` | `1 (0)` | `1` | `0 errores` | Parche aplicado exitosamente |