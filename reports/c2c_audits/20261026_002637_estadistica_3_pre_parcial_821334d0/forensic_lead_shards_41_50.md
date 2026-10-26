# Informe de Auditoría Forense: Clúster de Shards 41 al 50 (`shard_41` a `shard_50`)
**Curso:** `estadistica_3_pre_parcial` ("Estadistica 3 Pre Parcial")  
**Conversación Orquestadora:** [`821334d0-216d-40c5-8920-dca90c0f0b26`](conversation://821334d0-216d-40c5-8920-dca90c0f0b26)  
**Directorio de Corrida:** `reports/c2c_audits/20261026_002637_estadistica_3_pre_parcial_821334d0`

---

## 1. Resumen Ejecutivo del Clúster 41-50

El clúster 41 al 50 abordó temáticas de variables instrumentales (IV), estimadores bietápicos (2SLS/MC2E) y contrastes de exogeneidad de Hausman. Este clúster ilustra de forma nítida la **divergencia bimodal** entre dos tipologías de stragglers: los dominados por compilación tardía (post-compile heavy) frente a los dominados por sobreanálisis inicial (pre-compile heavy).

### Métricas Clave Agregadas
- **Tiempo de Pared Concurrente en Lote:** Mediana de **`318.0s`**.
- **Tasa de Aprobación al Primer Intento Formal:** **100%** (0 fallos de compilación).
- **Llamadas a `edit_file`:** **2 ediciones totales** en el clúster (`shard_42` y `shard_46`).
- **Total Tokens Activos del Clúster:** **`1,531,242 tokens`**.
- **Thinking Tokens Acumulados:** **`76,825 tokens`**.

---

## 2. Matriz Forense Detallada por Shard

| Shard ID | Pared (s) | Pre-1st (s) | Post-1st (s) | Compiles (Fails) | Edits | Tokens Activos | Thinking Tokens | Diagnóstico Forense |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **`shard_41`** | `269.0s` | `303.0s` | `14.0s` | `1 (0)` | `0` | `124,958` | `7,776` | Inferencia compacta, cierre ágil |
| **`shard_42`** | **`464.0s`** | `125.0s` | **`387.0s`** | `3 (0)` | `1` | `176,628` | **`10,153`** | **STRAGGLER POST-COMPILE: Bucle de validación de 387s** |
| **`shard_43`** | `284.0s` | `316.0s` | `15.0s` | `1 (0)` | `0` | `139,997` | `7,402` | Clean-room ágil, 1 compile limpio |
| **`shard_44`** | `285.0s` | `314.0s` | `17.0s` | `1 (0)` | `0` | `112,202` | `6,002` | Menor consumo de tokens activos del clúster |
| **`shard_45`** | `326.0s` | `114.0s` | `257.0s` | `2 (0)` | `0` | `132,783` | `8,095` | Doble compile, validación estocástica |
| **`shard_46`** | **`417.0s`** | **`334.0s`** | `127.0s` | `2 (0)` | `1` | **`217,577`** | `9,704` | **STRAGGLER MIXTO: 334s pre + 1 edit correctivo** |
| **`shard_47`** | **`260.0s`** | `288.0s` | `15.0s` | `1 (0)` | `0` | `132,202` | `7,088` | **Líder de Velocidad del Clúster** |
| **`shard_48`** | `362.0s` | `388.0s` | `16.0s` | `1 (0)` | `0` | `159,280` | `8,375` | Inferencia densa pre-compile, cierre en 16s |
| **`shard_49`** | `310.0s` | `337.0s` | `15.0s` | `1 (0)` | `0` | `126,615` | `7,331` | Exactamente alineado con la mediana global |
| **`shard_50`** | `369.0s` | `197.0s` | `213.0s` | `2 (0)` | `0` | `207,193` | `6,528` | Alto consumo de tokens activos (+207k) |

---

## 3. Análisis de la Dualidad de Stragglers

1. **`shard_42` (Top-5 Straggler Global - `464.0s`):**
   - Escribió su primer archivo rápidamente (Pre-compile: **125.0s**), pero demoró **387.0s en Post-1st-Compile**.
   - Causa raíz: Ejecutó 3 compilaciones sucesivas para ajustar rangos numéricos de los instrumentos débiles ($F < 10$) en la primera etapa del 2SLS, realizando 1 edición en caliente para asegurar que los distractores mantuvieran la distancia $\epsilon \ge 1.5\%$ respecto a la clave.

2. **`shard_46` (`417.0s`):**
   - Combinó alta latencia de deducción previa (**334.0s**) con una corrección de último minuto (`edits = 1`, Post-compile: **127.0s**), acumulando 217,577 tokens activos y 9,704 thinking tokens.

3. **La Eficiencia de `shard_47` (`260.0s`):**
   - Resolvió de manera limpia la verificación instrumental, compilando una sola vez con 7,088 thinking tokens y cerrando en 15 segundos.
