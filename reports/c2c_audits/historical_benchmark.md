# Content-to-Course: Registro Histórico y Evolución de Rendimiento

> [!NOTE]
> Este documento se actualiza automáticamente con cada auditoría ejecutada. Última actualización: `2026-10-13 10:32:33`. Total de ejecuciones auditadas: **2**.

## 1. Matriz de Evolución Temporal (Normalizada por Carga de Contenido)

| Fecha | Run / Curso | Input (Pág / MB) | Output (Comp / Preg) | Tiempo de Pared | Speedup | Tokens Totales | Tok / Preg | Seg / Preg | Blind Judges (1st) | Intervenciones | Bottlenecks |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `2026-10-13 15:32` | **solow_growth_model** | 36 pág (0.0 MB) | 22 comp / 0 preg | 28.9 min (1731.0s) | **3.37x** | 18,610,255 | **0.0** | **0.0s** | ✅ Limpio | 🛠️ 0 | ⚠️ 2 |
| `2026-10-10 12:00` | **estadistica3_regresion_v3** | 50 pág (1.2 MB) | 16 comp / 480 preg | 60.0 min (3600.0s) | **2.0x** | 8,645,000 | **18,010.4** | **7.5s** | ✅ Limpio | 🛠️ 0 | ✅ 0 |

---

## 2. Métricas Promedio del Sistema (Baselines Globales)

- **Factor de Aceleración Paralela Promedio**: `2.69x`
- **Densidad de Tokens Promedio por Pregunta**: `18,010.4 tokens/pregunta`
- **Latencia Promedio por Pregunta Validada**: `7.5 s/pregunta`
- **Rendimiento Promedio de Generación**: `8.0 preguntas/minuto`

---
*Generado por el motor forense `c2c-run-auditor`.*