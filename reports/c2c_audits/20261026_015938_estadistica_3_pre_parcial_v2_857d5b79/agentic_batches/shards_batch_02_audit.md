# Auditoría Forense: Shard Authors Batch 02
**Subagentes Auditados:** 10 autores (Shard Author shard_11 a Shard Author shard_20)  
**Categoría:** Generadores de Shards Curriculares (Stage 04 Build & Invariants)

---

## 1. Métricas Agregadas del Lote
- **Tokens Totales:** 5,411,696 (Activos: 1,364,408)
- **Tiempo Acumulado de Inferencia:** 2777.0 s (46.28 min)
- **Duración Mediana por Shard:** 277.7 s
- **Pre-Compilación Promedio:** 0.0 s
- **Post-Compilación Promedio:** 0.0 s
- **Total Intentos de Compilación:** 10
- **Herramientas Invocadas:** 117 (Errores: 27)

---

## 2. Ranking y Descomposición Bimodal Pre/Post-Compile
| Shard | Duración (s) | Pre-Compile (s) | Post-Compile (s) | Compiles | Tokens Totales | Diagnóstico |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| `Shard Author shard_17` | 227.0 | 0.0 | 0.0 | 1 | 655,279 | 🟢 Clean-Room |
| `Shard Author shard_18` | 236.0 | 0.0 | 0.0 | 1 | 316,815 | 🟢 Clean-Room |
| `Shard Author shard_12` | 237.0 | 0.0 | 0.0 | 1 | 286,488 | 🟢 Clean-Room |
| `Shard Author shard_11` | 254.0 | 0.0 | 0.0 | 1 | 279,985 | 🟡 Varianza Moderada |
| `Shard Author shard_15` | 259.0 | 0.0 | 0.0 | 1 | 463,696 | 🟡 Varianza Moderada |
| `Shard Author shard_20` | 285.0 | 0.0 | 0.0 | 1 | 315,400 | 🟡 Varianza Moderada |
| `Shard Author shard_13` | 291.0 | 0.0 | 0.0 | 1 | 461,221 | 🟡 Varianza Moderada |
| `Shard Author shard_19` | 310.0 | 0.0 | 0.0 | 1 | 740,992 | 🟡 Varianza Moderada |
| `Shard Author shard_14` | 324.0 | 0.0 | 0.0 | 1 | 1,072,532 | 🟡 Varianza Moderada |
| `Shard Author shard_16` | 354.0 | 0.0 | 0.0 | 1 | 819,288 | 🔴 Straggler Severo |

- **Shard Más Eficiente del Lote:** `Shard Author shard_17` (227.0 s)
- **Shard Cuello de Botella del Lote:** `Shard Author shard_16` (354.0 s)

---

## 3. Desglose de Herramientas y Fallas Técnicas
- `view_file`: 63 llamadas
- `run_command`: 34 llamadas
- `write_file`: 10 llamadas
- `send_message`: 10 llamadas

### Diagnóstico de Stragglers e Invariantes:
En este lote, los reintentos estuvieron acotados a la verificación de unicidad de distractores `[R-18/19]` y ajuste de macros LaTeX en `invariants.py`. Todos los shards compilaron exitosamente cumpliendo el contrato de 20 a 30 reactivos sin requerir intervención humana.
