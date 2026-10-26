# Auditoría Forense: Shard Authors Batch 05
**Subagentes Auditados:** 10 autores (Shard Author shard_41 a Shard Author shard_50)  
**Categoría:** Generadores de Shards Curriculares (Stage 04 Build & Invariants)

---

## 1. Métricas Agregadas del Lote
- **Tokens Totales:** 5,859,839 (Activos: 1,476,433)
- **Tiempo Acumulado de Inferencia:** 3216.0 s (53.60 min)
- **Duración Mediana por Shard:** 321.6 s
- **Pre-Compilación Promedio:** 0.0 s
- **Post-Compilación Promedio:** 0.0 s
- **Total Intentos de Compilación:** 10
- **Herramientas Invocadas:** 110 (Errores: 27)

---

## 2. Ranking y Descomposición Bimodal Pre/Post-Compile
| Shard | Duración (s) | Pre-Compile (s) | Post-Compile (s) | Compiles | Tokens Totales | Diagnóstico |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| `Shard Author shard_45` | 189.0 | 0.0 | 0.0 | 1 | 287,008 | 🟢 Clean-Room |
| `Shard Author shard_41` | 279.0 | 0.0 | 0.0 | 1 | 398,399 | 🟡 Varianza Moderada |
| `Shard Author shard_42` | 282.0 | 0.0 | 0.0 | 1 | 368,306 | 🟡 Varianza Moderada |
| `Shard Author shard_48` | 295.0 | 0.0 | 0.0 | 1 | 340,930 | 🟡 Varianza Moderada |
| `Shard Author shard_44` | 297.0 | 0.0 | 0.0 | 1 | 349,162 | 🟡 Varianza Moderada |
| `Shard Author shard_46` | 319.0 | 0.0 | 0.0 | 1 | 454,859 | 🟡 Varianza Moderada |
| `Shard Author shard_43` | 368.0 | 0.0 | 0.0 | 1 | 1,146,614 | 🔴 Straggler Severo |
| `Shard Author shard_47` | 382.0 | 0.0 | 0.0 | 1 | 651,250 | 🔴 Straggler Severo |
| `Shard Author shard_50` | 391.0 | 0.0 | 0.0 | 1 | 1,026,920 | 🔴 Straggler Severo |
| `Shard Author shard_49` | 414.0 | 0.0 | 0.0 | 1 | 836,391 | 🔴 Straggler Severo |

- **Shard Más Eficiente del Lote:** `Shard Author shard_45` (189.0 s)
- **Shard Cuello de Botella del Lote:** `Shard Author shard_49` (414.0 s)

---

## 3. Desglose de Herramientas y Fallas Técnicas
- `view_file`: 72 llamadas
- `run_command`: 16 llamadas
- `write_file`: 10 llamadas
- `send_message`: 10 llamadas
- `edit_file`: 2 llamadas

### Diagnóstico de Stragglers e Invariantes:
En este lote, los reintentos estuvieron acotados a la verificación de unicidad de distractores `[R-18/19]` y ajuste de macros LaTeX en `invariants.py`. Todos los shards compilaron exitosamente cumpliendo el contrato de 20 a 30 reactivos sin requerir intervención humana.
