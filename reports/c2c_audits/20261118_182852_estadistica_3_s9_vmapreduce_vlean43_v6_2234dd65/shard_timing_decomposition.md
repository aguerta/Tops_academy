### Descomposición Temporal y Forense Multi-Shard (`Pre` vs `Post` 1st Compile)
- **Total Shards Auditados:** `12` | **Mediana de Pared:** `166.0s`
- **Gold Standard Clean-Room:** `Shard Author shard_04` (`76.0s`, 0 fallos, 0 ediciones post-escritura)

| Shard | Duración Total (s) | Pre-1st-Compile (s) | Post-1st-Compile (s) | Compiles (Fails) | Edits | Errores / Códigos | Diagnóstico Causa Raíz |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- | :--- |
| **Shard Author shard_12** | `263.0s` | `101.0s` | `162.0s` | `4 (3)` | `4` | `[TPL-DYNAMIC-RATIONALE], [TPL-VAR], [VERIFIER-TAUTOLOGY-DETECTED]` | Remediación (3 fallos) |
| **Shard Author shard_09** | `239.0s` | `102.0s` | `137.0s` | `4 (3)` | `2` | `[TPL-CONST-DISTRACTOR], [TPL-HINTS-DUPLICATE], [INVARIANT]` | Remediación (3 fallos) |
| **Shard Author shard_01** | `224.0s` | `76.0s` | `148.0s` | `2 (1)` | `6` | `[TPL-DYNAMIC-RATIONALE], [TPL-D3], [R-19]` | Remediación (1 fallos) |
| **Shard Author shard_07** | `219.0s` | `90.0s` | `129.0s` | `4 (3)` | `2` | `[TPL-VAR], [R-15]` | Remediación (3 fallos) |
| **Shard Author shard_08** | `192.0s` | `88.0s` | `104.0s` | `3 (2)` | `1` | `[TPL-CONST-DISTRACTOR], [TPL-HINTS-DUPLICATE], [R-16]` | Remediación (2 fallos) |
| **Shard Author shard_10** | `166.0s` | `83.0s` | `83.0s` | `2 (1)` | `0` | `[TPL-ORPHAN-VARS], [TPL-STEM-GRAMMAR], [TPL-HINTS-DUPLICATE]` | Remediación (1 fallos) |
| **Shard Author shard_11** | `148.0s` | `76.0s` | `72.0s` | `2 (1)` | `0` | `[TPL-ORPHAN-VARS], [TPL-HINTS-DUPLICATE]` | Remediación (1 fallos) |
| **Shard Author shard_03** | `135.0s` | `64.0s` | `71.0s` | `2 (1)` | `0` | `[TPL-ORPHAN-VARS], [TPL-STEM-GRAMMAR], [TPL-CONST-DISTRACTOR]` | Remediación (1 fallos) |
| **Shard Author shard_02** | `132.0s` | `71.0s` | `61.0s` | `3 (2)` | `2` | `[TPL-STATIC-OPT], [TPL-D4]` | Remediación (2 fallos) |
| **Shard Author shard_05** | `114.0s` | `74.0s` | `40.0s` | `2 (1)` | `2` | `[VERIFIER-TAUTOLOGY-DETECTED], [TPL-CROSS], [R-19]` | Remediación (1 fallos) |
| **Shard Author shard_04** | `76.0s` | `61.0s` | `15.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_06** | `67.0s` | `36.0s` | `31.0s` | `2 (1)` | `1` | `[VERIFIER-TAUTOLOGY-DETECTED]` | Remediación (1 fallos) |

---

### Descomposición Temporal y Forense de Repair Engineers (Stage 3B Remediación)
- **Total Repair Engineers Auditados:** `2` | **Mediana de Pared:** `47.0s`

| Repair Engineer | Duración Total (s) | Pre-1st-Compile (s) | Post-1st-Compile (s) | Compiles (Fails) | Edits | Errores / Códigos | Diagnóstico Causa Raíz |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- | :--- |
| **Repair Engineer (C02)** | `47.0s` | `27.0s` | `20.0s` | `1 (0)` | `2` | `0 errores` | Parche aplicado exitosamente |
| **Repair Engineer (C28)** | `31.0s` | `16.0s` | `15.0s` | `1 (0)` | `1` | `0 errores` | Parche aplicado exitosamente |