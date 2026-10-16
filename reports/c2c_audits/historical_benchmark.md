# Content-to-Course: Registro Histórico y Evolución de Rendimiento

> [!NOTE]
> Este documento se actualiza automáticamente con cada auditoría ejecutada. Última actualización: `2026-10-15 22:20:16`. Total de ejecuciones auditadas: **3**.

## 1. Matriz de Evolución Temporal (Normalizada por Carga de Contenido)

| Fecha | Run / Curso | Input (Pág / MB) | Output (Comp / Preg) | Tiempo de Pared | Speedup | Tokens Totales | Tok / Preg | Seg / Preg | Blind Judges (1st) | Intervenciones | Bottlenecks |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `2026-10-16 03:20` | **Tops_academy** | 36 pág (1.49 MB) | 33 comp / 0 preg | 43.5 min (2609.0s) | **3.45x** | 30,268,477 | **0.0** | **0.0s** | ✅ Limpio | 🛠️ 0 | ⚠️ 2 |
| `2026-10-13 22:50` | **solow_growth_model** | 36 pág (0.0 MB) | 25 comp / 0 preg | 1.4 min (86.0s) | **3.52x** | 653,847 | **0.0** | **0.0s** | ✅ Limpio | 🛠️ 0 | ⚠️ 1 |
| `2026-10-10 12:00` | **estadistica3_regresion_v3** | 50 pág (1.2 MB) | 16 comp / 480 preg | 60.0 min (3600.0s) | **2.0x** | 8,645,000 | **18,010.4** | **7.5s** | ✅ Limpio | 🛠️ 0 | ✅ 0 |

---

## 2. Métricas Promedio del Sistema (Baselines Globales)

- **Factor de Aceleración Paralela Promedio**: `2.99x`
- **Densidad de Tokens Promedio por Pregunta**: `18,010.4 tokens/pregunta`
- **Latencia Promedio por Pregunta Validada**: `7.5 s/pregunta`
- **Rendimiento Promedio de Generación**: `8.0 preguntas/minuto`

---
*Generado por el motor forense `c2c-run-auditor`.*