# Auditoría Forense: Shard Authors Batch 04
**Subagentes Auditados:** 10 autores (Shard Author shard_31 a Shard Author shard_40)  
**Categoría:** Generadores de Shards Curriculares (Stage 04 Build & Invariants)

---

## 1. Métricas Agregadas del Lote
- **Tokens Totales:** 5,543,825 (Activos: 1,373,745)
- **Tiempo Acumulado de Inferencia:** 2809.0 s (46.82 min)
- **Duración Mediana por Shard:** 280.9 s
- **Pre-Compilación Promedio:** 0.0 s
- **Post-Compilación Promedio:** 0.0 s
- **Total Intentos de Compilación:** 10
- **Herramientas Invocadas:** 127 (Errores: 33)

---

## 2. Ranking y Descomposición Bimodal Pre/Post-Compile
| Shard | Duración (s) | Pre-Compile (s) | Post-Compile (s) | Compiles | Tokens Totales | Diagnóstico |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| `Shard Author shard_35` | 231.0 | 0.0 | 0.0 | 1 | 435,265 | 🟢 Clean-Room |
| `Shard Author shard_38` | 260.0 | 0.0 | 0.0 | 1 | 590,939 | 🟡 Varianza Moderada |
| `Shard Author shard_31` | 263.0 | 0.0 | 0.0 | 1 | 335,594 | 🟡 Varianza Moderada |
| `Shard Author shard_32` | 281.0 | 0.0 | 0.0 | 1 | 495,301 | 🟡 Varianza Moderada |
| `Shard Author shard_36` | 282.0 | 0.0 | 0.0 | 1 | 341,535 | 🟡 Varianza Moderada |
| `Shard Author shard_39` | 290.0 | 0.0 | 0.0 | 1 | 785,000 | 🟡 Varianza Moderada |
| `Shard Author shard_34` | 294.0 | 0.0 | 0.0 | 1 | 646,357 | 🟡 Varianza Moderada |
| `Shard Author shard_40` | 302.0 | 0.0 | 0.0 | 1 | 809,068 | 🟡 Varianza Moderada |
| `Shard Author shard_33` | 303.0 | 0.0 | 0.0 | 1 | 405,775 | 🟡 Varianza Moderada |
| `Shard Author shard_37` | 303.0 | 0.0 | 0.0 | 1 | 698,991 | 🟡 Varianza Moderada |

- **Shard Más Eficiente del Lote:** `Shard Author shard_35` (231.0 s)
- **Shard Cuello de Botella del Lote:** `Shard Author shard_37` (303.0 s)

---

## 3. Desglose de Herramientas y Fallas Técnicas
- `view_file`: 64 llamadas
- `run_command`: 43 llamadas
- `write_file`: 10 llamadas
- `send_message`: 10 llamadas

### Diagnóstico de Stragglers e Invariantes:
En este lote, los reintentos estuvieron acotados a la verificación de unicidad de distractores `[R-18/19]` y ajuste de macros LaTeX en `invariants.py`. Todos los shards compilaron exitosamente cumpliendo el contrato de 20 a 30 reactivos sin requerir intervención humana.
