### Descomposición Temporal y Forense Multi-Shard (`Pre` vs `Post` 1st Compile)
- **Total Shards Auditados:** `18` | **Mediana de Pared:** `129.0s`
- **Gold Standard Clean-Room:** `Shard Author shard_11` (`79.0s`, 0 fallos, 0 ediciones post-escritura)

| Shard | Duración Total (s) | Pre-1st-Compile (s) | Post-1st-Compile (s) | Compiles (Fails) | Edits | Errores / Códigos | Diagnóstico Causa Raíz |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- | :--- |
| **Shard Author shard_04** | `211.0s` | `92.0s` | `119.0s` | `2 (1)` | `0` | `[TPL-ORPHAN-VARS], [TPL-ADJACENT-PLACEHOLDERS], [INVARIANT]` | Remediación (1 fallos) |
| **Shard Author shard_05** | `192.0s` | `90.0s` | `102.0s` | `3 (2)` | `1` | `[TPL-STEM-EQUATION-PARITY], [INVARIANT], [TPL-PLACEHOLDER-ANSWER-LEAK]` | Remediación (2 fallos) |
| **Shard Author shard_02** | `186.0s` | `108.0s` | `78.0s` | `2 (1)` | `5` | `[TPL-AD-HOC-PERTURBATION], [TPL-UNBOUNDED-LOOP], [INVARIANT]` | Remediación (1 fallos) |
| **Shard Author shard_03** | `186.0s` | `8.0s` | `178.0s` | `2 (1)` | `0` | `[TPL-AD-HOC-PERTURBATION], [TPL-UNBOUNDED-LOOP], [INVARIANT]` | Remediación (1 fallos) |
| **Shard Author shard_07** | `166.0s` | `93.0s` | `73.0s` | `2 (1)` | `0` | `[TPL-STEM-SYMBOL-PARITY], [INVARIANT], [TPL-PLACEHOLDER-ANSWER-LEAK]` | Remediación (1 fallos) |
| **Shard Author shard_06** | `149.0s` | `94.0s` | `55.0s` | `2 (1)` | `3` | `[INVARIANT], [TPL-PLACEHOLDER-ANSWER-LEAK]` | Remediación (1 fallos) |
| **Shard Author shard_01** | `140.0s` | `108.0s` | `32.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_08** | `133.0s` | `80.0s` | `53.0s` | `2 (1)` | `2` | `[TPL-DYNAMIC-RATIONALE], [TPL-ORPHAN-VARS], [INVARIANT]` | Remediación (1 fallos) |
| **Shard Author shard_15** | `129.0s` | `106.0s` | `23.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_14** | `123.0s` | `78.0s` | `45.0s` | `2 (1)` | `5` | `[TPL-AD-HOC-PERTURBATION], [TPL-UNBOUNDED-LOOP], [TPL-ORPHAN-VARS]` | Remediación (1 fallos) |
| **Shard Author shard_12** | `111.0s` | `98.0s` | `13.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_18** | `104.0s` | `68.0s` | `36.0s` | `2 (1)` | `3` | `[TPL-DYNAMIC-RATIONALE]` | Remediación (1 fallos) |
| **Shard Author shard_17** | `101.0s` | `88.0s` | `13.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_13** | `97.0s` | `82.0s` | `15.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_09** | `92.0s` | `78.0s` | `14.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_16** | `90.0s` | `73.0s` | `17.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_10** | `90.0s` | `74.0s` | `16.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_11** | `79.0s` | `67.0s` | `12.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |

---

### Descomposición Temporal y Forense de Repair Engineers (Stage 3B Remediación)
- **Total Repair Engineers Auditados:** `4` | **Mediana de Pared:** `48.0s`

| Repair Engineer | Duración Total (s) | Pre-1st-Compile (s) | Post-1st-Compile (s) | Compiles (Fails) | Edits | Errores / Códigos | Diagnóstico Causa Raíz |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- | :--- |
| **Repair Engineer Hab-06** | `77.0s` | `44.0s` | `33.0s` | `1 (0)` | `5` | `0 errores` | Parche aplicado exitosamente |
| **Repair Engineer C-10** | `48.0s` | `35.0s` | `13.0s` | `1 (0)` | `2` | `0 errores` | Parche aplicado exitosamente |
| **Repair Engineer Hab-08** | `43.0s` | `28.0s` | `15.0s` | `1 (0)` | `2` | `0 errores` | Parche aplicado exitosamente |
| **Repair Engineer C-02** | `41.0s` | `26.0s` | `15.0s` | `1 (0)` | `1` | `0 errores` | Parche aplicado exitosamente |