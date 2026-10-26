# Auditoría Forense: Shard Authors Batch 01
**Subagentes Auditados:** 10 autores (Shard Author shard_01 a Shard Author shard_10)  
**Categoría:** Generadores de Shards Curriculares (Stage 04 Build & Invariants)

---

## 1. Métricas Agregadas del Lote
- **Tokens Totales:** 4,990,942 (Activos: 1,537,509)
- **Tiempo Acumulado de Inferencia:** 3035.0 s (50.58 min)
- **Duración Mediana por Shard:** 303.5 s
- **Pre-Compilación Promedio:** 0.0 s
- **Post-Compilación Promedio:** 0.0 s
- **Total Intentos de Compilación:** 10
- **Herramientas Invocadas:** 113 (Errores: 27)

---

## 2. Ranking y Descomposición Bimodal Pre/Post-Compile
| Shard | Duración (s) | Pre-Compile (s) | Post-Compile (s) | Compiles | Tokens Totales | Diagnóstico |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| `Shard Author shard_09` | 238.0 | 0.0 | 0.0 | 1 | 299,161 | 🟢 Clean-Room |
| `Shard Author shard_01` | 258.0 | 0.0 | 0.0 | 1 | 339,958 | 🟡 Varianza Moderada |
| `Shard Author shard_07` | 286.0 | 0.0 | 0.0 | 1 | 313,664 | 🟡 Varianza Moderada |
| `Shard Author shard_03` | 293.0 | 0.0 | 0.0 | 1 | 353,366 | 🟡 Varianza Moderada |
| `Shard Author shard_04` | 302.0 | 0.0 | 0.0 | 1 | 604,787 | 🟡 Varianza Moderada |
| `Shard Author shard_10` | 309.0 | 0.0 | 0.0 | 1 | 697,759 | 🟡 Varianza Moderada |
| `Shard Author shard_02` | 324.0 | 0.0 | 0.0 | 1 | 509,585 | 🟡 Varianza Moderada |
| `Shard Author shard_08` | 325.0 | 0.0 | 0.0 | 1 | 556,839 | 🟡 Varianza Moderada |
| `Shard Author shard_06` | 341.0 | 0.0 | 0.0 | 1 | 661,612 | 🟡 Varianza Moderada |
| `Shard Author shard_05` | 359.0 | 0.0 | 0.0 | 1 | 654,211 | 🔴 Straggler Severo |

- **Shard Más Eficiente del Lote:** `Shard Author shard_09` (238.0 s)
- **Shard Cuello de Botella del Lote:** `Shard Author shard_05` (359.0 s)

---

## 3. Desglose de Herramientas y Fallas Técnicas
- `view_file`: 63 llamadas
- `run_command`: 30 llamadas
- `write_file`: 10 llamadas
- `send_message`: 10 llamadas

### Diagnóstico de Stragglers e Invariantes:
En este lote, los reintentos estuvieron acotados a la verificación de unicidad de distractores `[R-18/19]` y ajuste de macros LaTeX en `invariants.py`. Todos los shards compilaron exitosamente cumpliendo el contrato de 20 a 30 reactivos sin requerir intervención humana.
