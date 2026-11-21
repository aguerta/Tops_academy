### Descomposición Temporal y Forense Multi-Shard (`Pre` vs `Post` 1st Compile)
- **Total Shards Auditados:** `9` | **Mediana de Pared:** `240.0s`
- **Gold Standard Clean-Room:** `Shard Author shard_06` (`189.0s`, 0 fallos, 0 ediciones post-escritura)

| Shard | Duración Total (s) | Pre-1st-Compile (s) | Post-1st-Compile (s) | Compiles (Fails) | Edits | Errores / Códigos | Diagnóstico Causa Raíz |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- | :--- |
| **Shard Author shard_03** | `340.0s` | `89.0s` | `251.0s` | `3 (2)` | `0` | `[TPL-ORPHAN-VARS], [TPL-DYNAMIC-RATIONALE], [TPL-VAR]` | Remediación (2 fallos) |
| **Shard Author shard_08** | `339.0s` | `144.0s` | `195.0s` | `3 (2)` | `4` | `[TPL-ORPHAN-VARS], [VERIFIER-TAUTOLOGY-DETECTED], [TPL-HINTS-DUPLICATE]` | Remediación (2 fallos) |
| **Shard Author shard_07** | `280.0s` | `120.0s` | `160.0s` | `3 (2)` | `1` | `[TPL-STEM-GRAMMAR], [TPL-CROSS], [TPL-VAR]` | Remediación (2 fallos) |
| **Shard Author shard_01** | `276.0s` | `107.0s` | `169.0s` | `3 (2)` | `1` | `[TPL-DRY], [TPL-VAR], [TPL-STATIC-OPT]` | Remediación (2 fallos) |
| **Shard Author shard_05** | `240.0s` | `103.0s` | `137.0s` | `3 (2)` | `2` | `[VERIFIER-TAUTOLOGY-DETECTED], [INVARIANT], [TPL-D4]` | Remediación (2 fallos) |
| **Shard Author shard_04** | `229.0s` | `99.0s` | `130.0s` | `3 (2)` | `2` | `[TPL-VAR], [TPL-STATIC-OPT]` | Remediación (2 fallos) |
| **Shard Author shard_09** | `223.0s` | `111.0s` | `112.0s` | `2 (1)` | `0` | `[TPL-DYNAMIC-RATIONALE], [TPL-ORPHAN-VARS], [R-19]` | Remediación (1 fallos) |
| **Shard Author shard_02** | `215.0s` | `97.0s` | `118.0s` | `3 (2)` | `1` | `[TPL-ORPHAN-VARS], [INVARIANT], [TPL-KATEX-SYMPY-LEAK]` | Remediación (2 fallos) |
| **Shard Author shard_06** | `189.0s` | `133.0s` | `56.0s` | `2 (1)` | `2` | `[TPL-DYNAMIC-RATIONALE], [VERIFIER-TAUTOLOGY-DETECTED], [TPL-CONST-DISTRACTOR]` | Remediación (1 fallos) |

---

### Descomposición Temporal y Forense de Repair Engineers (Stage 3B Remediación)
- **Total Repair Engineers Auditados:** `2` | **Mediana de Pared:** `80.0s`

| Repair Engineer | Duración Total (s) | Pre-1st-Compile (s) | Post-1st-Compile (s) | Compiles (Fails) | Edits | Errores / Códigos | Diagnóstico Causa Raíz |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- | :--- |
| **Repair Engineer Hab-09** | `80.0s` | `67.0s` | `13.0s` | `1 (0)` | `6` | `0 errores` | Parche aplicado exitosamente |
| **Repair Engineer C-08** | `49.0s` | `33.0s` | `16.0s` | `1 (0)` | `1` | `0 errores` | Parche aplicado exitosamente |