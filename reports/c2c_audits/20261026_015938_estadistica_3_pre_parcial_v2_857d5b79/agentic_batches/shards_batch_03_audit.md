# Auditoría Forense: Shard Authors Batch 03
**Subagentes Auditados:** 10 autores (Shard Author shard_21 a Shard Author shard_30)  
**Categoría:** Generadores de Shards Curriculares (Stage 04 Build & Invariants)

---

## 1. Métricas Agregadas del Lote
- **Tokens Totales:** 4,066,482 (Activos: 1,244,720)
- **Tiempo Acumulado de Inferencia:** 2599.0 s (43.32 min)
- **Duración Mediana por Shard:** 259.9 s
- **Pre-Compilación Promedio:** 0.0 s
- **Post-Compilación Promedio:** 0.0 s
- **Total Intentos de Compilación:** 10
- **Herramientas Invocadas:** 90 (Errores: 25)

---

## 2. Ranking y Descomposición Bimodal Pre/Post-Compile
| Shard | Duración (s) | Pre-Compile (s) | Post-Compile (s) | Compiles | Tokens Totales | Diagnóstico |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| `Shard Author shard_28` | 192.0 | 0.0 | 0.0 | 1 | 280,120 | 🟢 Clean-Room |
| `Shard Author shard_23` | 218.0 | 0.0 | 0.0 | 1 | 286,928 | 🟢 Clean-Room |
| `Shard Author shard_21` | 237.0 | 0.0 | 0.0 | 1 | 461,838 | 🟢 Clean-Room |
| `Shard Author shard_22` | 247.0 | 0.0 | 0.0 | 1 | 307,798 | 🟢 Clean-Room |
| `Shard Author shard_25` | 250.0 | 0.0 | 0.0 | 1 | 692,470 | 🟢 Clean-Room |
| `Shard Author shard_29` | 262.0 | 0.0 | 0.0 | 1 | 310,335 | 🟡 Varianza Moderada |
| `Shard Author shard_24` | 267.0 | 0.0 | 0.0 | 1 | 362,997 | 🟡 Varianza Moderada |
| `Shard Author shard_26` | 301.0 | 0.0 | 0.0 | 1 | 383,564 | 🟡 Varianza Moderada |
| `Shard Author shard_30` | 306.0 | 0.0 | 0.0 | 1 | 367,555 | 🟡 Varianza Moderada |
| `Shard Author shard_27` | 319.0 | 0.0 | 0.0 | 1 | 612,877 | 🟡 Varianza Moderada |

- **Shard Más Eficiente del Lote:** `Shard Author shard_28` (192.0 s)
- **Shard Cuello de Botella del Lote:** `Shard Author shard_27` (319.0 s)

---

## 3. Desglose de Herramientas y Fallas Técnicas
- `view_file`: 57 llamadas
- `run_command`: 13 llamadas
- `write_file`: 10 llamadas
- `send_message`: 10 llamadas

### Diagnóstico de Stragglers e Invariantes:
En este lote, los reintentos estuvieron acotados a la verificación de unicidad de distractores `[R-18/19]` y ajuste de macros LaTeX en `invariants.py`. Todos los shards compilaron exitosamente cumpliendo el contrato de 20 a 30 reactivos sin requerir intervención humana.
