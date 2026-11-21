### Descomposición Temporal y Forense Multi-Shard (`Pre` vs `Post` 1st Compile)
- **Total Shards Auditados:** `9` | **Mediana de Pared:** `239.0s`
- **Gold Standard Clean-Room:** `Shard Author shard_09` (`97.0s`, 0 fallos, 0 ediciones post-escritura)

| Shard | Duración Total (s) | Pre-1st-Compile (s) | Post-1st-Compile (s) | Compiles (Fails) | Edits | Errores / Códigos | Diagnóstico Causa Raíz |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- | :--- |
| **Shard Author shard_02** | `359.0s` | `104.0s` | `255.0s` | `3 (2)` | `0` | `[TPL-DYNAMIC-RATIONALE], [INVARIANT], [TPL-VAR]` | Remediación (2 fallos) |
| **Shard Author shard_07** | `313.0s` | `153.0s` | `160.0s` | `3 (2)` | `1` | `[TPL-ORPHAN-VARS], [TPL-DRY], [R-19]` | Remediación (2 fallos) |
| **Shard Author shard_08** | `290.0s` | `138.0s` | `152.0s` | `4 (3)` | `12` | `SyntaxError en shard_08_data.py (Línea 102, Columna 89): unterminated triple-quoted string literal (detected at line 825) , SyntaxError en shard_08_data.py (Línea 628, Columna 11): '[' was never closed , [TPL-ORPHAN-VARS]` | Remediación (3 fallos) |
| **Shard Author shard_06** | `280.0s` | `132.0s` | `148.0s` | `3 (2)` | `2` | `[TPL-DYNAMIC-RATIONALE], [R-19], [TPL-VAR]` | Remediación (2 fallos) |
| **Shard Author shard_05** | `239.0s` | `96.0s` | `143.0s` | `3 (2)` | `3` | `[TPL-VERIFIER-UNSOUND], [VERIFIER-TAUTOLOGY-DETECTED], [INVARIANT]` | Remediación (2 fallos) |
| **Shard Author shard_01** | `229.0s` | `115.0s` | `114.0s` | `2 (1)` | `0` | `[TPL-DYNAMIC-RATIONALE], [TPL-STATIC-OPT], [TPL-VAR]` | Remediación (1 fallos) |
| **Shard Author shard_03** | `219.0s` | `108.0s` | `111.0s` | `2 (2)` | `0` | `[TPL-ORPHAN-VARS], [TPL-D4], [TPL-VAR]` | Remediación (2 fallos) |
| **Shard Author shard_04** | `204.0s` | `107.0s` | `97.0s` | `2 (1)` | `0` | `[TPL-VAR], [TPL-D4]` | Remediación (1 fallos) |
| **Shard Author shard_09** | `97.0s` | `69.0s` | `28.0s` | `2 (1)` | `2` | `[TPL-ORPHAN-VARS], [TPL-STEM-GRAMMAR]` | Remediación (1 fallos) |

---

### Descomposición Temporal y Forense de Repair Engineers (Stage 3B Remediación)
- **Total Repair Engineers Auditados:** `3` | **Mediana de Pared:** `90.0s`

| Repair Engineer | Duración Total (s) | Pre-1st-Compile (s) | Post-1st-Compile (s) | Compiles (Fails) | Edits | Errores / Códigos | Diagnóstico Causa Raíz |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- | :--- |
| **Repair Engineer Hab-09** | `102.0s` | `67.0s` | `35.0s` | `2 (1)` | `9` | `[TPL-STEM-VARIANT-PARITY]` | Re-intento tras fallo (1 fallos) |
| **Repair Engineer shard_06 (C-08, C-09)** | `90.0s` | `74.0s` | `16.0s` | `1 (0)` | `12` | `0 errores` | Parche aplicado exitosamente |
| **Repair Engineer C-05** | `62.0s` | `32.0s` | `30.0s` | `2 (1)` | `2` | `[TPL-STEM-VARIANT-PARITY]` | Re-intento tras fallo (1 fallos) |