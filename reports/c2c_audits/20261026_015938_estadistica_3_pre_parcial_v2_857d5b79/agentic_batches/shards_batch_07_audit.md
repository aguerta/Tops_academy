# Auditoría Forense: Shard Authors Batch 07
**Subagentes Auditados:** 10 autores (Shard Author shard_61 a Shard Author shard_70)  
**Categoría:** Generadores de Shards Curriculares (Stage 04 Build & Invariants)

---

## 1. Métricas Agregadas del Lote
- **Tokens Totales:** 4,919,511 (Activos: 1,343,129)
- **Tiempo Acumulado de Inferencia:** 2933.0 s (48.88 min)
- **Duración Mediana por Shard:** 293.3 s
- **Pre-Compilación Promedio:** 0.0 s
- **Post-Compilación Promedio:** 0.0 s
- **Total Intentos de Compilación:** 10
- **Herramientas Invocadas:** 114 (Errores: 28)

---

## 2. Ranking y Descomposición Bimodal Pre/Post-Compile
| Shard | Duración (s) | Pre-Compile (s) | Post-Compile (s) | Compiles | Tokens Totales | Diagnóstico |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| `Shard Author shard_69` | 203.0 | 0.0 | 0.0 | 1 | 280,118 | 🟢 Clean-Room |
| `Shard Author shard_61` | 220.0 | 0.0 | 0.0 | 1 | 375,670 | 🟢 Clean-Room |
| `Shard Author shard_67` | 279.0 | 0.0 | 0.0 | 1 | 369,723 | 🟡 Varianza Moderada |
| `Shard Author shard_70` | 285.0 | 0.0 | 0.0 | 1 | 353,330 | 🟡 Varianza Moderada |
| `Shard Author shard_63` | 290.0 | 0.0 | 0.0 | 1 | 723,425 | 🟡 Varianza Moderada |
| `Shard Author shard_62` | 292.0 | 0.0 | 0.0 | 1 | 351,989 | 🟡 Varianza Moderada |
| `Shard Author shard_64` | 300.0 | 0.0 | 0.0 | 1 | 396,815 | 🟡 Varianza Moderada |
| `Shard Author shard_66` | 337.0 | 0.0 | 0.0 | 1 | 669,692 | 🟡 Varianza Moderada |
| `Shard Author shard_65` | 358.0 | 0.0 | 0.0 | 1 | 626,580 | 🔴 Straggler Severo |
| `Shard Author shard_68` | 369.0 | 0.0 | 0.0 | 1 | 772,169 | 🔴 Straggler Severo |

- **Shard Más Eficiente del Lote:** `Shard Author shard_69` (203.0 s)
- **Shard Cuello de Botella del Lote:** `Shard Author shard_68` (369.0 s)

---

## 3. Desglose de Herramientas y Fallas Técnicas
- `view_file`: 62 llamadas
- `run_command`: 32 llamadas
- `write_file`: 10 llamadas
- `send_message`: 10 llamadas

### Diagnóstico de Stragglers e Invariantes:
En este lote, los reintentos estuvieron acotados a la verificación de unicidad de distractores `[R-18/19]` y ajuste de macros LaTeX en `invariants.py`. Todos los shards compilaron exitosamente cumpliendo el contrato de 20 a 30 reactivos sin requerir intervención humana.
