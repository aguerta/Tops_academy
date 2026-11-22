### Descomposición Temporal y Forense Multi-Shard (`Pre` vs `Post` 1st Compile)
- **Total Shards Auditados:** `14` | **Mediana de Pared:** `239.0s`
- **Gold Standard Clean-Room:** `Shard Author shard_07` (`137.0s`, 0 fallos, 0 ediciones post-escritura)

| Shard | Duración Total (s) | Pre-1st-Compile (s) | Post-1st-Compile (s) | Compiles (Fails) | Edits | Errores / Códigos | Diagnóstico Causa Raíz |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- | :--- |
| **Shard Author shard_11** | `341.0s` | `133.0s` | `208.0s` | `4 (3)` | `3` | `[TPL-ORPHAN-VARS], [TPL-STEM-VARIANT-PARITY], [TPL-VAR]` | Remediación (3 fallos) |
| **Shard Author shard_10** | `317.0s` | `132.0s` | `185.0s` | `3 (2)` | `4` | `[TPL-ORPHAN-VARS], [TPL-DRY], [TPL-CONST-DISTRACTOR]` | Remediación (2 fallos) |
| **Shard Author shard_13** | `290.0s` | `98.0s` | `192.0s` | `4 (3)` | `5` | `[TPL-ORPHAN-VARS], [TPL-STEM-VARIANT-PARITY], [TPL-STATIC-OPT]` | Remediación (3 fallos) |
| **Shard Author shard_09** | `278.0s` | `115.0s` | `163.0s` | `3 (2)` | `1` | `[TPL-DYNAMIC-RATIONALE], [TPL-ORPHAN-VARS], [TPL-DRY]` | Remediación (2 fallos) |
| **Shard Author shard_03** | `270.0s` | `89.0s` | `181.0s` | `3 (2)` | `1` | `[TPL-AD-HOC-PERTURBATION], [TPL-UNBOUNDED-LOOP], [TPL-ORPHAN-VARS]` | Remediación (2 fallos) |
| **Shard Author shard_01** | `251.0s` | `97.0s` | `154.0s` | `2 (1)` | `0` | `[TPL-ORPHAN-VARS], [TPL-STEM-VARIANT-PARITY], [R-19]` | Remediación (1 fallos) |
| **Shard Author shard_06** | `239.0s` | `105.0s` | `134.0s` | `4 (3)` | `2` | `[TPL-DYNAMIC-RATIONALE], [TPL-ORPHAN-VARS], [TPL-DRY]` | Remediación (3 fallos) |
| **Shard Author shard_12** | `227.0s` | `106.0s` | `121.0s` | `2 (1)` | `0` | `[TPL-STEM-VARIANT-PARITY], [TPL-STEM-GRAMMAR], [TPL-CONST-DISTRACTOR]` | Remediación (1 fallos) |
| **Shard Author shard_08** | `218.0s` | `82.0s` | `136.0s` | `2 (1)` | `0` | `[TPL-STEM-GRAMMAR], [TPL-STEM-VARIANT-PARITY]` | Remediación (1 fallos) |
| **Shard Author shard_02** | `210.0s` | `97.0s` | `113.0s` | `2 (1)` | `0` | `[TPL-ORPHAN-VARS], [TPL-D4], [TPL-STEM-VARIANT-PARITY]` | Remediación (1 fallos) |
| **Shard Author shard_05** | `201.0s` | `75.0s` | `126.0s` | `3 (2)` | `2` | `[TPL-AD-HOC-PERTURBATION], [TPL-UNBOUNDED-LOOP], [TPL-STATIC-OPT]` | Remediación (2 fallos) |
| **Shard Author shard_14** | `174.0s` | `83.0s` | `91.0s` | `3 (2)` | `1` | `[TPL-VERIFIER-UNSOUND], [TPL-DRY], [TPL-VAR]` | Remediación (2 fallos) |
| **Shard Author shard_04** | `170.0s` | `83.0s` | `87.0s` | `2 (1)` | `0` | `[TPL-VAR], [TPL-STEM-VARIANT-PARITY]` | Remediación (1 fallos) |
| **Shard Author shard_07** | `137.0s` | `82.0s` | `55.0s` | `2 (1)` | `2` | `[TPL-ORPHAN-VARS], [TPL-DYNAMIC-RATIONALE], [TPL-STATIC-OPT]` | Remediación (1 fallos) |

---

### Descomposición Temporal y Forense de Repair Engineers (Stage 3B Remediación)
- **Total Repair Engineers Auditados:** `4` | **Mediana de Pared:** `90.0s`

| Repair Engineer | Duración Total (s) | Pre-1st-Compile (s) | Post-1st-Compile (s) | Compiles (Fails) | Edits | Errores / Códigos | Diagnóstico Causa Raíz |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- | :--- |
| **Repair Engineer Hab-07** | `100.0s` | `70.0s` | `30.0s` | `0 (0)` | `11` | `0 errores` | Parche aplicado exitosamente |
| **Repair Engineer Hab-07** | `90.0s` | `44.0s` | `46.0s` | `2 (1)` | `5` | `[TPL-DYNAMIC-RATIONALE], [TPL-ORPHAN-VARS], [TPL-STEM-GRAMMAR]` | Re-intento tras fallo (1 fallos) |
| **Repair Engineer C-08** | `47.0s` | `25.0s` | `22.0s` | `1 (0)` | `1` | `0 errores` | Parche aplicado exitosamente |
| **Repair Engineer C-04** | `33.0s` | `17.0s` | `16.0s` | `1 (0)` | `1` | `0 errores` | Parche aplicado exitosamente |