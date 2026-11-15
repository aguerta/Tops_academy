### Descomposición Temporal y Forense Multi-Shard (`Pre` vs `Post` 1st Compile)
- **Total Shards Auditados:** `9` | **Mediana de Pared:** `428.0s`
- **Gold Standard Clean-Room:** `Shard Author shard_09` (`106.0s`, 0 fallos, 0 ediciones post-escritura)

| Shard | Duración Total (s) | Pre-1st-Compile (s) | Post-1st-Compile (s) | Compiles (Fails) | Edits | Errores / Códigos | Diagnóstico Causa Raíz |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- | :--- |
| **Shard Author shard_02** | `1112.0s` | `175.0s` | `944.0s` | `9 (8)` | `34` | `[R-16], [TPL-CROSS], [TPL-DRY]` | Remediación (8 fallos) |
| **Shard Author shard_05** | `751.0s` | `118.0s` | `642.0s` | `7 (6)` | `17` | `[TPL-VAR], [TPL-DRY]` | Remediación (6 fallos) |
| **Shard Author shard_07** | `616.0s` | `132.0s` | `493.0s` | `9 (8)` | `14` | `[TPL-VAR], [TPL-CROSS], [TPL-ASM]` | Remediación (8 fallos) |
| **Shard Author shard_01** | `458.0s` | `112.0s` | `352.0s` | `4 (3)` | `3` | `[TPL-DRY], [TPL-VAR]` | Remediación (3 fallos) |
| **Shard Author shard_06** | `428.0s` | `191.0s` | `246.0s` | `4 (3)` | `7` | `0 errores` | Remediación (3 fallos) |
| **Shard Author shard_03** | `297.0s` | `123.0s` | `181.0s` | `2 (1)` | `5` | `0 errores` | Remediación (1 fallos) |
| **Shard Author shard_04** | `275.0s` | `85.0s` | `202.0s` | `3 (2)` | `4` | `[TPL-DRY], [TPL-VAR]` | Remediación (2 fallos) |
| **Shard Author shard_08** | `185.0s` | `102.0s` | `94.0s` | `3 (2)` | `1` | `SyntaxError en shard_08_data.py (Línea 384, Columna 168): (unicode error) 'unicodeescape' codec can't decode bytes in position 55-56: truncated \xXX escape` | Remediación (2 fallos) |
| **Shard Author shard_09** | `106.0s` | `85.0s` | `34.0s` | `2 (1)` | `2` | `[TPL-DRY], [TPL-VAR]` | Remediación (1 fallos) |

---

### Descomposición Temporal y Forense de Repair Engineers (Stage 3B Remediación)
- **Total Repair Engineers Auditados:** `1` | **Mediana de Pared:** `104.0s`

| Repair Engineer | Duración Total (s) | Pre-1st-Compile (s) | Post-1st-Compile (s) | Compiles (Fails) | Edits | Errores / Códigos | Diagnóstico Causa Raíz |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- | :--- |
| **Repair Engineer (HAB02)** | `104.0s` | `51.0s` | `55.0s` | `2 (1)` | `5` | `0 errores` | Re-intento tras fallo (1 fallos) |