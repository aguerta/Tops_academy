### Descomposición Temporal y Forense Multi-Shard (`Pre` vs `Post` 1st Compile)
- **Total Shards Auditados:** `6` | **Mediana de Pared:** `644.0s`
- **Gold Standard Clean-Room:** `Shard Author shard_06` (`337.0s`, 0 fallos, 0 ediciones post-escritura)

| Shard | Duración Total (s) | Pre-1st-Compile (s) | Post-1st-Compile (s) | Compiles (Fails) | Edits | Errores / Códigos | Diagnóstico Causa Raíz |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- | :--- |
| **Shard Author shard_04** | `1038.0s` | `246.0s` | `800.0s` | `8 (7)` | `23` | `[R-15], [TPL-VAR], NameError: name '_MSG' is not defined. No se pudieron generar los reactivos requeridos debido a colisiones o parámetros estrechos. | Acción: Ampliar los rangos de las variables aleatorias en generate_py.` | Overthinking / Exploración lenta Pre-Compile; Remediación (7 fallos) |
| **Shard Author shard_05** | `676.0s` | `208.0s` | `476.0s` | `6 (5)` | `14` | `[TPL-DRY]` | Remediación (5 fallos) |
| **Shard Author shard_01** | `644.0s` | `134.0s` | `515.0s` | `6 (5)` | `14` | `[R-19], ValueError'. Las funciones generadoras de ítems deben retornar un diccionario de variables y opciones, sin sentencias 'raise' de depuración. | Acción: Corregir el archivo infractor., [R-16]` | Remediación (5 fallos) |
| **Shard Author shard_02** | `636.0s` | `161.0s` | `482.0s` | `4 (3)` | `16` | `[TPL-VAR]` | Remediación (3 fallos) |
| **Shard Author shard_03** | `389.0s` | `182.0s` | `214.0s` | `2 (1)` | `6` | `0 errores` | Remediación (1 fallos) |
| **Shard Author shard_06** | `337.0s` | `163.0s` | `184.0s` | `4 (3)` | `1` | `[TPL-DRY], [R-15], [TPL-VAR]` | Remediación (3 fallos) |

---

### Descomposición Temporal y Forense de Repair Engineers (Stage 3B Remediación)
- **Total Repair Engineers Auditados:** `2` | **Mediana de Pared:** `98.0s`

| Repair Engineer | Duración Total (s) | Pre-1st-Compile (s) | Post-1st-Compile (s) | Compiles (Fails) | Edits | Errores / Códigos | Diagnóstico Causa Raíz |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- | :--- |
| **Repair Engineer (HAB07)** | `98.0s` | `48.0s` | `53.0s` | `2 (1)` | `2` | `0 errores` | Re-intento tras fallo (1 fallos) |
| **Repair Engineer (C26)** | `67.0s` | `31.0s` | `39.0s` | `2 (1)` | `2` | `[R-19]` | Re-intento tras fallo (1 fallos) |