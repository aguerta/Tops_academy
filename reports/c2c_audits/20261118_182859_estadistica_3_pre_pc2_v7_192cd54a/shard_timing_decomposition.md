### Descomposición Temporal y Forense Multi-Shard (`Pre` vs `Post` 1st Compile)
- **Total Shards Auditados:** `22` | **Mediana de Pared:** `206.0s`
- **Gold Standard Clean-Room:** `Shard Author shard_12` (`79.0s`, 0 fallos, 0 ediciones post-escritura)

| Shard | Duración Total (s) | Pre-1st-Compile (s) | Post-1st-Compile (s) | Compiles (Fails) | Edits | Errores / Códigos | Diagnóstico Causa Raíz |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- | :--- |
| **Shard Author shard_17** | `415.0s` | `110.0s` | `305.0s` | `7 (6)` | `24` | `[TPL-VAR], [TPL-CONST-DISTRACTOR], [R-15]` | Remediación (6 fallos) |
| **Shard Author shard_16** | `333.0s` | `170.0s` | `163.0s` | `6 (4)` | `13` | `[TPL-STEM-GRAMMAR], [R-15], [TPL-VAR]` | Remediación (4 fallos) |
| **Shard Author shard_22** | `311.0s` | `103.0s` | `208.0s` | `7 (5)` | `12` | `[TPL-AD-HOC-PERTURBATION], [TPL-UNBOUNDED-LOOP], [TPL-VAR]` | Remediación (5 fallos) |
| **Shard Author shard_21** | `303.0s` | `132.0s` | `171.0s` | `5 (3)` | `6` | `[TPL-STEM-GRAMMAR], [TPL-VERIFIER-UNSOUND], [R-15]` | Remediación (3 fallos) |
| **Shard Author shard_13** | `297.0s` | `131.0s` | `166.0s` | `7 (5)` | `18` | `SyntaxError en shard_13_data.py (Línea 13, Columna 56): unexpected character after line continuation character , SyntaxError en shard_13_data.py (Línea 393, Columna 92): unexpected character after line continuation character , [TPL-VERIFIE…` | Remediación (5 fallos) |
| **Shard Author shard_02** | `260.0s` | `108.0s` | `152.0s` | `6 (4)` | `10` | `[TPL-ORPHAN-VARS], [TPL-STEM-GRAMMAR], [VERIFIER-TAUTOLOGY-DETECTED]` | Remediación (4 fallos) |
| **Shard Author shard_19** | `256.0s` | `112.0s` | `144.0s` | `6 (3)` | `9` | `[TPL-AD-HOC-PERTURBATION], [TPL-UNBOUNDED-LOOP], [TPL-ORPHAN-VARS]` | Remediación (3 fallos) |
| **Shard Author shard_03** | `231.0s` | `90.0s` | `141.0s` | `5 (3)` | `9` | `[TPL-ASM], [R-16]` | Remediación (3 fallos) |
| **Shard Author shard_18** | `218.0s` | `105.0s` | `113.0s` | `5 (3)` | `7` | `[R-15], [TPL-VAR], [TPL-KATEX]` | Remediación (3 fallos) |
| **Shard Author shard_20** | `208.0s` | `125.0s` | `83.0s` | `4 (2)` | `8` | `[TPL-DYNAMIC-RATIONALE], [TPL-CONST-DISTRACTOR], [R-15]` | Remediación (2 fallos) |
| **Shard Author shard_14** | `206.0s` | `116.0s` | `90.0s` | `4 (2)` | `6` | `[TPL-DYNAMIC-RATIONALE], [TPL-CONST-DISTRACTOR], [DIAG-MAGIC-MULT]` | Remediación (2 fallos) |
| **Shard Author shard_15** | `195.0s` | `96.0s` | `99.0s` | `5 (3)` | `7` | `[TPL-VERIFIER-UNSOUND], [TPL-STEM-GRAMMAR], [TPL-CONST-DISTRACTOR]` | Remediación (3 fallos) |
| **Shard Author shard_05** | `191.0s` | `84.0s` | `107.0s` | `5 (3)` | `8` | `[VERIFIER-TAUTOLOGY-DETECTED], [TPL-CONST-DISTRACTOR], [TPL-CROSS]` | Remediación (3 fallos) |
| **Shard Author shard_08** | `182.0s` | `94.0s` | `88.0s` | `5 (3)` | `6` | `[TPL-KATEX], [DIAG-MAGIC-MULT], [INVARIANT]` | Remediación (3 fallos) |
| **Shard Author shard_01** | `173.0s` | `99.0s` | `74.0s` | `4 (2)` | `2` | `[TPL-STEM-GRAMMAR], [DIAG-MAGIC-MULT]` | Remediación (2 fallos) |
| **Shard Author shard_09** | `169.0s` | `91.0s` | `78.0s` | `4 (2)` | `3` | `[TPL-ORPHAN-VARS], [VERIFIER-TAUTOLOGY-DETECTED], [R-15]` | Remediación (2 fallos) |
| **Shard Author shard_07** | `165.0s` | `90.0s` | `75.0s` | `4 (2)` | `5` | `[TPL-STEM-GRAMMAR], [TPL-CONST-DISTRACTOR], [INVARIANT]` | Remediación (2 fallos) |
| **Shard Author shard_11** | `160.0s` | `77.0s` | `83.0s` | `5 (3)` | `3` | `[TPL-KATEX], [TPL-VAR], [R-16]` | Remediación (3 fallos) |
| **Shard Author shard_10** | `158.0s` | `86.0s` | `72.0s` | `4 (2)` | `3` | `[TPL-VERIFIER-UNSOUND], [TPL-CONST-DISTRACTOR], [VERIFIER-TAUTOLOGY-DETECTED]` | Remediación (2 fallos) |
| **Shard Author shard_06** | `124.0s` | `93.0s` | `31.0s` | `3 (1)` | `0` | `0 errores` | Remediación (1 fallos) |
| **Shard Author shard_04** | `111.0s` | `86.0s` | `25.0s` | `3 (1)` | `0` | `0 errores` | Remediación (1 fallos) |
| **Shard Author shard_12** | `79.0s` | `59.0s` | `20.0s` | `3 (1)` | `0` | `0 errores` | Remediación (1 fallos) |

---

### Descomposición Temporal y Forense de Repair Engineers (Stage 3B Remediación)
- **Total Repair Engineers Auditados:** `6` | **Mediana de Pared:** `58.0s`

| Repair Engineer | Duración Total (s) | Pre-1st-Compile (s) | Post-1st-Compile (s) | Compiles (Fails) | Edits | Errores / Códigos | Diagnóstico Causa Raíz |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- | :--- |
| **Repair Engineer C-20** | `78.0s` | `36.0s` | `42.0s` | `2 (1)` | `4` | `[VERIFIER-TAUTOLOGY-DETECTED], [TPL-CROSS]` | Re-intento tras fallo (1 fallos) |
| **Repair Engineer Hab-21** | `69.0s` | `55.0s` | `14.0s` | `1 (1)` | `4` | `0 errores` | Re-intento tras fallo (1 fallos) |
| **Repair Engineer shard_14 (C-05, C-04)** | `58.0s` | `39.0s` | `19.0s` | `1 (0)` | `4` | `0 errores` | Parche aplicado exitosamente |
| **Repair Engineer shard_05 (Hab-07, Hab-08)** | `51.0s` | `37.0s` | `14.0s` | `1 (0)` | `2` | `0 errores` | Parche aplicado exitosamente |
| **Repair Engineer Hab-06** | `50.0s` | `37.0s` | `13.0s` | `1 (1)` | `1` | `0 errores` | Re-intento tras fallo (1 fallos) |
| **Repair Engineer C-06** | `20.0s` | `14.0s` | `6.0s` | `0 (0)` | `0` | `0 errores` | Parche aplicado exitosamente |