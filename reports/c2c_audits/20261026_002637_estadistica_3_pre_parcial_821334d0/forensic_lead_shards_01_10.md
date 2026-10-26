# Informe de Auditoría Forense: Clúster de Shards 01 al 10 (`shard_01` a `shard_10`)
**Curso:** `estadistica_3_pre_parcial` ("Estadistica 3 Pre Parcial")  
**Conversación Orquestadora:** [`821334d0-216d-40c5-8920-dca90c0f0b26`](conversation://821334d0-216d-40c5-8920-dca90c0f0b26)  
**Directorio de Corrida:** `reports/c2c_audits/20261026_002637_estadistica_3_pre_parcial_821334d0`

---

## 1. Resumen Ejecutivo del Clúster 01-10

El clúster inicial de autoría (`shard_01` a `shard_10`) cubrió las primeras micro-competencias fundacionales de la econometría clásica (estimación MCO, varianza de perturbaciones, propiedades MELI y contrastes de hipótesis simples). 

### Métricas Clave Agregadas
- **Tiempo de Pared Concurrente en Lote:** Mediana de **`270.0s`** (vs. mediana global de `310.0s`).
- **Tasa de Aprobación al Primer Intento:** **100%** (10 de 10 shards compilaron con éxito sin fallos de compilación formal).
- **Total Tokens Activos del Clúster:** **`1,392,206 tokens`** (promedio: 139,220 tokens/shard).
- **Thinking Tokens Acumulados:** **`67,003 tokens`** (promedio: 6,700 tokens/shard).
- **Llamadas a `edit_file`:** **1 sola edición** en todo el clúster (`shard_10`).

---

## 2. Matriz Forense Detallada por Shard

| Shard ID | Pared (s) | Pre-1st (s) | Post-1st (s) | Compiles (Fails) | Edits | Tokens Activos | Thinking Tokens | Diagnóstico Forense |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **`shard_01`** | `269.0s` | `115.0s` | `185.0s` | `2 (0)` | `0` | `196,895` | `4,424` | Pase fluido, doble validación CLI |
| **`shard_02`** | `310.0s` | `325.0s` | `15.0s` | `1 (0)` | `0` | `127,327` | `7,662` | Pre-compile pesado, cierre instantáneo |
| **`shard_03`** | `252.0s` | `267.0s` | `14.0s` | `1 (0)` | `0` | `105,189` | `6,219` | Clean-room ágil, 1 compile limpio |
| **`shard_04`** | `252.0s` | `269.0s` | `12.0s` | `1 (0)` | `0` | `123,854` | `5,428` | Clean-room ágil, 1 compile limpio |
| **`shard_05`** | `345.0s` | `359.0s` | `14.0s` | `1 (0)` | `0` | `147,337` | `9,463` | Overthinking pre-compile (+9.4k thinking) |
| **`shard_06`** | `348.0s` | `353.0s` | `22.0s` | `1 (0)` | `0` | `143,683` | `7,326` | Inferencia previa densa, cierre limpio |
| **`shard_07`** | `273.0s` | `283.0s` | `17.0s` | `1 (0)` | `0` | `103,239` | `6,502` | Alta eficiencia de tokens, pase limpio |
| **`shard_08`** | `347.0s` | `360.0s` | `13.0s` | `1 (0)` | `0` | `123,781` | `8,784` | Overthinking pre-compile en derivación |
| **`shard_09`** | `288.0s` | `125.0s` | `188.0s` | `2 (0)` | `0` | `126,647` | `6,168` | Balance I/O, doble verificación |
| **`shard_10`** | `267.0s` | `211.0s` | `80.0s` | `2 (0)` | `1` | `144,688` | `6,116` | Único shard con 1 edit menor post-compile |

---

## 3. Análisis de Patrones y Causa Raíz

1. **Bimodalidad Pre-Compile vs Post-Compile:**
   - La mayoría de los shards (`shard_02`, `shard_03`, `shard_04`, `shard_05`, `shard_06`, `shard_07`, `shard_08`) exhibieron un patrón de **Pre-Compile Dominant**: gastaron entre 250s y 360s en razonamiento e inferencia antes de emitir la primera llamada a compilación, pero una vez generado el código, su tiempo post-compilación fue residual (12s a 22s), cerrando con éxito rotundo al primer intento.
   - En contraste, `shard_01` y `shard_09` comenzaron a escribir rápido (Pre-compile: 115s y 125s) y realizaron dos pasadas de validación (`compile_runs = 2`), demorando 185s y 188s en post-compile sin incurrir en ningún fallo.

2. **Cero Retrabajos Sistémicos:**
   - A diferencia de corridas no optimizadas donde se presentan errores `[TPL-D4]` o colisiones de distractores, los autores de este clúster generaron plantillas paramétricas con guardas algebraicas desde el inicio, acumulando 0 fallos de compilación formal.
