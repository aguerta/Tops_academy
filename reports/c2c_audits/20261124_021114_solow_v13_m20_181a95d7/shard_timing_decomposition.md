### Descomposición Temporal y Forense Multi-Shard (`Pre` vs `Post` 1st Compile)
- **Total Shards Auditados:** `14` | **Mediana de Pared:** `149.0s`
- **Gold Standard Clean-Room:** `Shard Author shard_06` (`106.0s`, 0 fallos, 0 ediciones post-escritura)

| Shard | Duración Total (s) | Pre-1st-Compile (s) | Post-1st-Compile (s) | Compiles (Fails) | Edits | Errores / Códigos | Diagnóstico Causa Raíz |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- | :--- |
| **Shard Author shard_02** | `197.0s` | `96.0s` | `101.0s` | `2 (1)` | `2` | `[TPL-ORPHAN-VARS], [TPL-D4]` | Remediación (1 fallos) |
| **Shard Author shard_13** | `189.0s` | `132.0s` | `57.0s` | `2 (1)` | `7` | `[TPL-DYNAMIC-RATIONALE], [TPL-AD-HOC-PERTURBATION], [TPL-UNBOUNDED-LOOP]` | Remediación (1 fallos) |
| **Shard Author shard_11** | `188.0s` | `101.0s` | `87.0s` | `2 (1)` | `8` | `[TPL-STATIC-OPT], [R-19]` | Remediación (1 fallos) |
| **Shard Author shard_14** | `188.0s` | `93.0s` | `95.0s` | `2 (1)` | `0` | `[INVARIANT]` | Remediación (1 fallos) |
| **Shard Author shard_07** | `158.0s` | `82.0s` | `76.0s` | `2 (1)` | `0` | `[INVARIANT], [TPL-PLACEHOLDER-ANSWER-LEAK], [TPL-STEM-EQUATION-PARITY]` | Remediación (1 fallos) |
| **Shard Author shard_09** | `152.0s` | `134.0s` | `18.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_05** | `149.0s` | `80.0s` | `69.0s` | `2 (1)` | `3` | `[TPL-STEM-EQUATION-PARITY]` | Remediación (1 fallos) |
| **Shard Author shard_04** | `142.0s` | `89.0s` | `53.0s` | `2 (1)` | `4` | `[TPL-STEM-EQUATION-PARITY], [INVARIANT], [TPL-PLACEHOLDER-ANSWER-LEAK]` | Remediación (1 fallos) |
| **Shard Author shard_03** | `134.0s` | `71.0s` | `63.0s` | `2 (1)` | `8` | `[TPL-AD-HOC-PERTURBATION], [TPL-UNBOUNDED-LOOP], [TPL-ORPHAN-VARS]` | Remediación (1 fallos) |
| **Shard Author shard_01** | `131.0s` | `81.0s` | `50.0s` | `2 (1)` | `3` | `[INVARIANT], [TPL-PLACEHOLDER-ANSWER-LEAK], [TPL-DIGIT-PLACEHOLDER-CONCAT]` | Remediación (1 fallos) |
| **Shard Author shard_08** | `124.0s` | `82.0s` | `42.0s` | `2 (1)` | `3` | `[TPL-DYNAMIC-RATIONALE], [TPL-ORPHAN-VARS], [TPL-TAUTOLOGICAL-IDENTITY]` | Remediación (1 fallos) |
| **Shard Author shard_12** | `124.0s` | `107.0s` | `17.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_10** | `123.0s` | `106.0s` | `17.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_06** | `106.0s` | `89.0s` | `17.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |

---

### Descomposición Temporal y Forense de Repair Engineers (Stage 3B Remediación)
- **Total Repair Engineers Auditados:** `4` | **Mediana de Pared:** `74.0s`

| Repair Engineer | Duración Total (s) | Pre-1st-Compile (s) | Post-1st-Compile (s) | Compiles (Fails) | Edits | Errores / Códigos | Diagnóstico Causa Raíz |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- | :--- |
| **Repair Engineer Hab-02** | `79.0s` | `39.0s` | `40.0s` | `1 (0)` | `4` | `0 errores` | Parche aplicado exitosamente |
| **Repair Engineer C-10** | `74.0s` | `40.0s` | `34.0s` | `2 (1)` | `7` | `[TPL-MS-CONDITIONAL-DISTRACTOR]` | Re-intento tras fallo (1 fallos) |
| **Repair Engineer PRE-01** | `40.0s` | `28.0s` | `12.0s` | `1 (0)` | `1` | `0 errores` | Parche aplicado exitosamente |
| **Repair Engineer C-04** | `33.0s` | `23.0s` | `10.0s` | `1 (0)` | `1` | `0 errores` | Parche aplicado exitosamente |