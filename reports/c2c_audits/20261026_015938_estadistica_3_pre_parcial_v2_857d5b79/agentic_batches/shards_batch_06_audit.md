# Auditoría Forense: Shard Authors Batch 06
**Subagentes Auditados:** 10 autores (Shard Author shard_51 a Shard Author shard_60)  
**Categoría:** Generadores de Shards Curriculares (Stage 04 Build & Invariants)

---

## 1. Métricas Agregadas del Lote
- **Tokens Totales:** 6,872,535 (Activos: 1,543,883)
- **Tiempo Acumulado de Inferencia:** 3251.0 s (54.18 min)
- **Duración Mediana por Shard:** 325.1 s
- **Pre-Compilación Promedio:** 0.0 s
- **Post-Compilación Promedio:** 0.0 s
- **Total Intentos de Compilación:** 10
- **Herramientas Invocadas:** 137 (Errores: 33)

---

## 2. Ranking y Descomposición Bimodal Pre/Post-Compile
| Shard | Duración (s) | Pre-Compile (s) | Post-Compile (s) | Compiles | Tokens Totales | Diagnóstico |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| `Shard Author shard_54` | 254.0 | 0.0 | 0.0 | 1 | 353,775 | 🟡 Varianza Moderada |
| `Shard Author shard_57` | 259.0 | 0.0 | 0.0 | 1 | 311,350 | 🟡 Varianza Moderada |
| `Shard Author shard_55` | 271.0 | 0.0 | 0.0 | 1 | 322,712 | 🟡 Varianza Moderada |
| `Shard Author shard_52` | 273.0 | 0.0 | 0.0 | 1 | 761,133 | 🟡 Varianza Moderada |
| `Shard Author shard_53` | 304.0 | 0.0 | 0.0 | 1 | 384,794 | 🟡 Varianza Moderada |
| `Shard Author shard_59` | 316.0 | 0.0 | 0.0 | 1 | 389,880 | 🟡 Varianza Moderada |
| `Shard Author shard_60` | 349.0 | 0.0 | 0.0 | 1 | 1,457,759 | 🟡 Varianza Moderada |
| `Shard Author shard_56` | 386.0 | 0.0 | 0.0 | 1 | 800,223 | 🔴 Straggler Severo |
| `Shard Author shard_58` | 409.0 | 0.0 | 0.0 | 1 | 1,242,849 | 🔴 Straggler Severo |
| `Shard Author shard_51` | 430.0 | 0.0 | 0.0 | 1 | 848,060 | 🔴 Straggler Severo |

- **Shard Más Eficiente del Lote:** `Shard Author shard_54` (254.0 s)
- **Shard Cuello de Botella del Lote:** `Shard Author shard_51` (430.0 s)

---

## 3. Desglose de Herramientas y Fallas Técnicas
- `view_file`: 76 llamadas
- `run_command`: 34 llamadas
- `write_file`: 11 llamadas
- `send_message`: 10 llamadas
- `edit_file`: 5 llamadas
- `schedule`: 1 llamadas

### Diagnóstico de Stragglers e Invariantes:
En este lote, los reintentos estuvieron acotados a la verificación de unicidad de distractores `[R-18/19]` y ajuste de macros LaTeX en `invariants.py`. Todos los shards compilaron exitosamente cumpliendo el contrato de 20 a 30 reactivos sin requerir intervención humana.
