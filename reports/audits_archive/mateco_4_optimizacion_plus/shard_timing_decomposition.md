### Descomposición Temporal y Forense Multi-Shard (`Pre` vs `Post` 1st Compile)
- **Total Shards Auditados:** `13` | **Mediana de Pared:** `231.0s`
- **Gold Standard Clean-Room:** `Shard Author shard_07` (`130.0s`, 0 fallos, 0 ediciones post-escritura)

| Shard | Duración Total (s) | Pre-1st-Compile (s) | Post-1st-Compile (s) | Compiles (Fails) | Edits | Errores / Códigos | Diagnóstico Causa Raíz |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- | :--- |
| **Shard Author shard_02** | `330.0s` | `135.0s` | `195.0s` | `4 (3)` | `7` | `[TPL-CONST-DISTRACTOR], [R-15], [R-19]` | Remediación (3 fallos) |
| **Shard Author shard_09** | `264.0s` | `112.0s` | `152.0s` | `3 (2)` | `1` | `[TPL-ORPHAN-VARS], [TPL-KATEX], [TPL-DYNAMIC-RATIONALE]` | Remediación (2 fallos) |
| **Shard Author shard_12** | `264.0s` | `106.0s` | `158.0s` | `3 (3)` | `2` | `[TPL-VAR], [R-19], [R-16]` | Remediación (3 fallos) |
| **Shard Author shard_03** | `262.0s` | `90.0s` | `172.0s` | `3 (2)` | `0` | `[TPL-D3], [TPL-VAR], [VERIFIER-TAUTOLOGY-DETECTED]` | Remediación (2 fallos) |
| **Shard Author shard_01** | `260.0s` | `100.0s` | `160.0s` | `4 (3)` | `5` | `[TPL-VERIFIER-UNSOUND], [DIAG-MAGIC-MULT], [TPL-VAR]` | Remediación (3 fallos) |
| **Shard Author shard_11** | `259.0s` | `142.0s` | `117.0s` | `2 (1)` | `0` | `[TPL-STEM-GRAMMAR], [TPL-ASM]` | Remediación (1 fallos) |
| **Shard Author shard_08** | `231.0s` | `125.0s` | `106.0s` | `2 (1)` | `0` | `[TPL-AD-HOC-PERTURBATION], [TPL-UNBOUNDED-LOOP], [TPL-DRY]` | Remediación (1 fallos) |
| **Shard Author shard_10** | `215.0s` | `109.0s` | `106.0s` | `2 (1)` | `0` | `[TPL-DYNAMIC-RATIONALE], [TPL-STEM-GRAMMAR], [TPL-CONST-DISTRACTOR]` | Remediación (1 fallos) |
| **Shard Author shard_06** | `190.0s` | `107.0s` | `83.0s` | `2 (1)` | `0` | `[TPL-DYNAMIC-RATIONALE], [TPL-ORPHAN-VARS]` | Remediación (1 fallos) |
| **Shard Author shard_04** | `188.0s` | `95.0s` | `93.0s` | `2 (1)` | `0` | `[TPL-AD-HOC-PERTURBATION], [TPL-UNBOUNDED-LOOP], [DIAG-MAGIC-MULT]` | Remediación (1 fallos) |
| **Shard Author shard_13** | `188.0s` | `100.0s` | `88.0s` | `2 (1)` | `0` | `[VERIFIER-TAUTOLOGY-DETECTED], [TPL-CONST-DISTRACTOR], [TPL-CROSS]` | Remediación (1 fallos) |
| **Shard Author shard_05** | `165.0s` | `93.0s` | `72.0s` | `2 (1)` | `0` | `[TPL-STEM-GRAMMAR], [TPL-VERIFIER-UNSOUND], [TPL-CONST-DISTRACTOR]` | Remediación (1 fallos) |
| **Shard Author shard_07** | `130.0s` | `70.0s` | `60.0s` | `2 (1)` | `2` | `[TPL-DYNAMIC-RATIONALE], [TPL-DRY], [TPL-VAR]` | Remediación (1 fallos) |

---

### Descomposición Temporal y Forense de Repair Engineers (Stage 3B Remediación)
- **Total Repair Engineers Auditados:** `10` | **Mediana de Pared:** `61.0s`

| Repair Engineer | Duración Total (s) | Pre-1st-Compile (s) | Post-1st-Compile (s) | Compiles (Fails) | Edits | Errores / Códigos | Diagnóstico Causa Raíz |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- | :--- |
| **Repair Engineer shard_11 (C-14, C-15)** | `283.0s` | `148.0s` | `135.0s` | `3 (2)` | `9` | `[R-15], [R-16], [R-19]` | Re-intento tras fallo (2 fallos) |
| **Repair Engineer Hab-03** | `102.0s` | `81.0s` | `21.0s` | `1 (0)` | `5` | `0 errores` | Parche aplicado exitosamente |
| **Repair Engineer C-04** | `70.0s` | `48.0s` | `22.0s` | `1 (0)` | `4` | `0 errores` | Parche aplicado exitosamente |
| **Repair Engineer Hab-03** | `63.0s` | `47.0s` | `16.0s` | `1 (0)` | `1` | `0 errores` | Parche aplicado exitosamente |
| **Repair Engineer Hab-07** | `61.0s` | `41.0s` | `20.0s` | `1 (0)` | `1` | `0 errores` | Parche aplicado exitosamente |
| **Repair Engineer C-04** | `58.0s` | `41.0s` | `17.0s` | `1 (0)` | `3` | `0 errores` | Parche aplicado exitosamente |
| **Repair Engineer Hab-03** | `58.0s` | `43.0s` | `15.0s` | `1 (1)` | `1` | `0 errores` | Re-intento tras fallo (1 fallos) |
| **Repair Engineer Hab-13** | `45.0s` | `31.0s` | `14.0s` | `1 (0)` | `1` | `0 errores` | Parche aplicado exitosamente |
| **Repair Engineer Hab-19** | `42.0s` | `31.0s` | `11.0s` | `1 (0)` | `2` | `0 errores` | Parche aplicado exitosamente |
| **Repair Engineer C-17** | `37.0s` | `24.0s` | `13.0s` | `1 (0)` | `2` | `0 errores` | Parche aplicado exitosamente |