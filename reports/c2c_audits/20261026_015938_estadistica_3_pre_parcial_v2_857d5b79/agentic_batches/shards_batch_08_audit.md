# Auditoría Forense: Shard Authors Batch 08
**Subagentes Auditados:** 10 autores (Shard Author shard_71 a Shard Author shard_80)  
**Categoría:** Generadores de Shards Curriculares (Stage 04 Build & Invariants)

---

## 1. Métricas Agregadas del Lote
- **Tokens Totales:** 8,112,653 (Activos: 1,533,045)
- **Tiempo Acumulado de Inferencia:** 3177.0 s (52.95 min)
- **Duración Mediana por Shard:** 317.7 s
- **Pre-Compilación Promedio:** 0.0 s
- **Post-Compilación Promedio:** 0.0 s
- **Total Intentos de Compilación:** 10
- **Herramientas Invocadas:** 160 (Errores: 36)

---

## 2. Ranking y Descomposición Bimodal Pre/Post-Compile
| Shard | Duración (s) | Pre-Compile (s) | Post-Compile (s) | Compiles | Tokens Totales | Diagnóstico |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| `Shard Author shard_72` | 246.0 | 0.0 | 0.0 | 1 | 296,087 | 🟢 Clean-Room |
| `Shard Author shard_71` | 274.0 | 0.0 | 0.0 | 1 | 380,149 | 🟡 Varianza Moderada |
| `Shard Author shard_75` | 280.0 | 0.0 | 0.0 | 1 | 541,911 | 🟡 Varianza Moderada |
| `Shard Author shard_77` | 300.0 | 0.0 | 0.0 | 1 | 547,487 | 🟡 Varianza Moderada |
| `Shard Author shard_76` | 316.0 | 0.0 | 0.0 | 1 | 807,557 | 🟡 Varianza Moderada |
| `Shard Author shard_74` | 332.0 | 0.0 | 0.0 | 1 | 685,311 | 🟡 Varianza Moderada |
| `Shard Author shard_80` | 332.0 | 0.0 | 0.0 | 1 | 908,143 | 🟡 Varianza Moderada |
| `Shard Author shard_73` | 335.0 | 0.0 | 0.0 | 1 | 1,217,473 | 🟡 Varianza Moderada |
| `Shard Author shard_79` | 336.0 | 0.0 | 0.0 | 1 | 825,234 | 🟡 Varianza Moderada |
| `Shard Author shard_78` | 426.0 | 0.0 | 0.0 | 1 | 1,903,301 | 🔴 Straggler Severo |

- **Shard Más Eficiente del Lote:** `Shard Author shard_72` (246.0 s)
- **Shard Cuello de Botella del Lote:** `Shard Author shard_78` (426.0 s)

---

## 3. Desglose de Herramientas y Fallas Técnicas
- `view_file`: 95 llamadas
- `run_command`: 43 llamadas
- `write_file`: 10 llamadas
- `send_message`: 10 llamadas
- `edit_file`: 2 llamadas

### Diagnóstico de Stragglers e Invariantes:
En este lote, los reintentos estuvieron acotados a la verificación de unicidad de distractores `[R-18/19]` y ajuste de macros LaTeX en `invariants.py`. Todos los shards compilaron exitosamente cumpliendo el contrato de 20 a 30 reactivos sin requerir intervención humana.
