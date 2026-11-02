# Informe Forense de Casos de Reparación (`c2c_repair`)
## Curso: Estadística 3 S9 vMapReduce12 (`estadistica_3_s9_vmapreduce12`)

**Fecha:** 1 de noviembre de 2026  
**Conversación:** [`aa8cbf32-3892-4628-a164-7a6cfa8f3c70`](conversation://aa8cbf32-3892-4628-a164-7a6cfa8f3c70)  
**Directorio del Curso:** `courses/estadistica_3_s9_vmapreduce12/`  

---

### Resumen General de Incidentes que Requirieron Reparación

Durante la ejecución del pipeline se requirieron **dos olas de reparación especializada (`c2c_repair`)**:

1. **Ola 1 (Resolución de Discordancia en Arbitraje Ciego):** 1 competencia (`C-16` en `shard_20`).
2. **Ola 2 (Compuerta Psicométrica Pre-Publish Quality Gate):** 5 competencias (`C-16, H-03, Hab-04, Hab-05, Hab-09` en los shards `shard_04, shard_05, shard_09, shard_20, shard_23`).

A continuación se detalla cada problema, las causas de su demora y el avance técnico obtenido.

---

### 1. Caso `C-16` (`shard_20`) — Discordancia en Arbitraje Ciego de Jueces

* **Componente Afectado:** Plantilla `T-C16-01` en `courses/estadistica_3_s9_vmapreduce12/work/shards/shard_20_data.py`.
* **Subagente:** `Repair Engineer C-16` (primera intervención).

#### El Problema
En la etapa de arbitraje ciego (`Stage 5`), el subagente independiente `Blind Judge 01` discrepó con el Ground Truth en el reactivo `T-C16-01_judge_1` (convergencia en probabilidad según Chebyshev). 
- El enunciado presentaba una ambigüedad entre desigualdad estricta o no estricta en el evento de concentración: $|X_n(\omega) - c| \le \epsilon$ versus $|X_n(\omega) - c| < \epsilon$.
- Adicionalmente, la cota entera de muestra $N = 5k - m$ en el verificador analítico no coincidía exactamente con el criterio de corte interpretado analíticamente por el juez ciego desde primeros principios.
- La tasa de acuerdo inicial fue de **99.2% (119/120)**, faltando 1 acuerdo para alcanzar la tolerancia cero requerida para publicar.

#### Por Qué Demoró Tanto
1. **Ciclo Completo de Re-Verificación:** Resolver la discordancia no solo requirió corregir el generador y verificador en `shard_20`, sino re-compilar el shard, reconstruir el banco de 1,030 preguntas (`run.py --stage build`) y **despachar una segunda ronda completa de 10 jueces ciegos** (`dispatch-judges`) evaluando 120 reactivos estratificados.
2. **Tiempo de Inferencia de Jueces:** Cada juez ciego resuelve analíticamente sin acceso a soluciones, lo que sumó ~2.5 minutos de pared.

#### Avance Obtenido
* Se unificó la condición de concentración a $|X_n(\omega) - c| \le \epsilon$ a lo largo de todos los stems, hints, generador y verificador analítico.
* En la segunda ronda de jueces ciegos, **se obtuvo un 100.0% de acuerdo (120/120 reactivos)** con 0 discrepancias.

---

### 2. Caso `H-03` (`shard_23`) — Pista Parentética Delatora (`[PSYCHOMETRIC-OPTIONS]`)

* **Componente Afectado:** Función `gen_h03_3` (L188–L207), plantilla `T-H03-03` en `shard_23_data.py`.
* **Subagente:** `Repair Engineer H-03`.

#### El Problema
El linter psicométrico `parenthetical_telltale_linter` de la compuerta de pre-publicación detectó:
```
Metainformación delatora parentética en opción visible: '(sesgo negativo hacia abajo)'
```
- En la Desigualdad de Jensen aplicada a la desviación estándar ($\mathbb{E}[S_n] < \sigma$), la opción correcta incluía el texto explicativo entre paréntesis `(sesgo negativo hacia abajo)`.
- Esto viola la regla `[R-15]` porque:
  1. Le entrega la respuesta al alumno por reconocimiento de texto ("telltale clue") sin necesidad de realizar el razonamiento matemático.
  2. Genera un desbalance de longitud sintáctica (>1.65x) entre la opción correcta y los distractores.

#### Por Qué Demoró Tanto
1. **Bloqueo Involuntario por Hook Guard (`pass_shard_23.json`):** 
   - Cuando el primer `c2c_repair` fue lanzado, ejecutó `compile_shard.py` *antes* de editar el código para "probar el error inicial".
   - Dado que `compile_shard.py` solo valida AST e invariantes numéricos básicos (y no los linters psicométricos de publicación), la compilación arrojó `[+] PASS`.
   - Al detectar `PASS`, el hook de seguridad `c2c_hook_guard.py` bloqueó todas las herramientas de edición (`edit_file`) para evitar ediciones descontroladas.
   - El subagente quedó atascado sin poder guardar cambios y emitió `DONE` sin modificar el archivo.
2. **Ciclo de Desbloqueo:** El orquestador tuvo que purgar `.check_attempts/pass_shard_23.json` y relanzar la reparación con una directiva estricta de orden: *editar primero, compilar después*.

#### Avance Obtenido
* Se reescribió `gen_h03_3` en `shard_23_data.py`, eliminando la coletilla parentética y balanceando todas las opciones con estructuras matemáticas uniformes:
  - Correcta: `$\mathbb{E}[S_n] < @sigma@$`
  - Distractores: `$\mathbb{E}[S_n] > @sigma@$`, `$\mathbb{E}[S_n] \ge @sigma@$`, `$\mathbb{E}[S_n] = @sigma@$`, `$\mathbb{E}[S_n] = @sigma2@$`, etc.
* El shard compiló con éxito y las plantillas quedaron actualizadas en `work/templates/H-03.json`.

---

### 3. Caso `Hab-04` (`shard_04`) — Multiplicadores Mágicos en Jensen (`[DIAG-MAGIC-MULT]`)

* **Componente Afectado:** Función `gen_h04_1` (L1–L24), plantilla `T-Hab04-01` en `shard_04_data.py`.
* **Subagente:** `Repair Engineer Hab-04`.

#### El Problema
El linter `diagnostic_rationale_alignment_linter` detectó distractores numéricos sintéticos calculados por multiplicadores arbitrarios colisionando con razones prohibidas:
```
Distractores numéricos sintéticos por multiplicador arbitrario ([1.333, 1.667]) con error_rationale desconectado del cálculo real.
```
- En lugar de modelar errores algebraicos reales (ej. no sumar la varianza, omitir la constante de convexidad), el generador original escalaba el valor correcto `ans` por constantes o factores empíricos como `ans * 1.333` o `ans * 1.667`.
- Esto desacopla el distractor de su fundamentación diagnóstica (`error_rationale`).

#### Por Qué Demoró Tanto
1. **Derivación de Fórmulas Algebraicas:** El ingeniero de reparación debió formular errores conceptuales reales basados en la desigualdad de Jensen:
   - Error 1: Confundir $\mathbb{E}[X^2]$ con $(\mathbb{E}[X])^2$.
   - Error 2: Omitir el término cuadrático de la constante.
   - Error 3: Invertir el signo de la brecha de Jensen.
2. **Bloqueo Inicial por Hook:** Al igual que en `shard_23`, el subagente inicial compiló antes de editar y fue bloqueado por `pass_shard_04.json`.

#### Avance Obtenido
* Se reemplazaron los factores fijos por fórmulas algebraicas basadas en concepciones erróneas reales interpoladas con `@var@`.
* `shard_04` superó la verificación en 50 semillas dry-run y se actualizó `work/templates/Hab-04.json`.

---

### 4. Caso `Hab-05` (`shard_05`) — Ratio Sintético en Cota de Markov/Chebyshev (`[DIAG-MAGIC-MULT]`)

* **Componente Afectado:** Función `gen_hab05_1` (L6–L33), plantilla `T-Hab05-01` en `shard_05_data.py`.
* **Subagente:** `Repair Engineer Hab-05`.

#### El Problema
El linter reportó una colisión con el multiplicador prohibido `0.667` ($2/3$) entre la respuesta correcta y uno de los distractores:
```
Distractores numéricos sintéticos por multiplicador arbitrario ([0.667]) con error_rationale desconectado del cálculo real.
```
- El generador incluía un bucle de desduplicación aditiva: `ds[i] = round(ds[i] + 0.003 * (i + 1), 4)`.
- En ciertas combinaciones de parámetros aleatorios de varianza $s^2$ y margen $\epsilon$, la razón entre el distractor ajustado y `ans` caía exactamente en el intervalo de exclusión `abs(d / ans - 0.667) <= 0.0015`.

#### Por Qué Demoró Tanto
- La colisión dependía de la semilla del generador, lo que hacía que `compile_shard.py` pasara en pruebas locales con pocas semillas pero fallara en el barrido exhaustivo de 1,030 preguntas del Quality Gate.
- Requirió parametrizar explícitamente las variables aleatorias para que los errores conceptuales mantuvieran separación analítica garantizada.

#### Avance Obtenido
* Se implementaron concepciones erróneas basadas en potencias erradas de $\epsilon$ ($\epsilon$ lineal en vez de cuadrático) y uso de desviación estándar $\sigma$ en vez de varianza $\sigma^2$.
* `shard_05` quedó validado en `work/templates/Hab-05.json`.

---

### 5. Caso `Hab-09` (`shard_09`) — Multiplicadores `0.333` y `1.333` en Desigualdad de Chebyshev

* **Componente Afectado:** Función `gen_hab09_1` (L6–L41), plantilla `T-Hab09-01` en `shard_09_data.py`.
* **Subagente:** `Repair Engineer Hab-09`.

#### El Problema
El código fuente original contenía explícitamente:
```python
d5 = round(ans / 2.0, 4)
```
- Dividir entre 2 o escalar por factores arbitrarios genera razones fijas prohibidas (`0.50`, `0.333`, `1.333`).
- El Quality Gate prohíbe terminantemente crear distractores multiplicando `ans` por fracciones constantes cuando el distractor afirma diagnosticar un error de fórmula.

#### Por Qué Demoró Tanto
- El repairer inicial intentó parches superficiales que seguían produciendo razones cercanas a $1/3$ o $4/3$.
- Requirió una reescritura de los distractores para que cada uno correspondiera a una omisión analítica real:
  - Distractor 1: $\frac{\sigma^2}{\epsilon}$ (omite el cuadrado de $\epsilon$).
  - Distractor 2: $\frac{\sigma}{\epsilon^2}$ (usa desviación en lugar de varianza).
  - Distractor 3: $\frac{\sigma}{\epsilon}$ (doble omisión).
  - Distractor 4: Complemento a 1 de la cota superior.

#### Avance Obtenido
* Se eliminó el factor `ans / 2.0` y se reemplazó por las fórmulas algebraicas directas.
* Se validaron 50 semillas sin colisiones en `work/templates/Hab-09.json`.

---

### 6. Caso `C-16` (`shard_20`) — Ratios en Convergencia Estocástica (`[DIAG-MAGIC-MULT]`)

* **Componente Afectado:** Función `gen_c16_2` (L41–L71), plantilla `T-C16-02` en `shard_20_data.py`.
* **Subagente:** `Repair Engineer C-16` (segunda intervención).

#### El Problema
En `gen_c16_2`, los distractores calculaban:
```python
d1 = round(((n - 2) * s2) / (lam ** 2), 3)
d2 = round(((n + 2) * s2) / (lam ** 2), 3)
```
- Para valores pequeños de $n$ (ej. $n = 4$ o $n = 6$), $(n - 2)/n$ produce exactamente $2/4 = 0.50$ o $4/6 = 0.667$, cayendo en la lista negra de multiplicadores sintéticos.

#### Por Qué Demoró Tanto
- `shard_20` fue el componente con mayor rotación del pipeline:
  1. Primero fue reparado por la discordancia de `Blind Judge 01`.
  2. Luego fue re-abierto por la compuerta de pre-publicación al detectar los ratios de $n \pm 2$.
- Esta duplicidad de causas requirió dos despliegues independientes de ingenieros de reparación.

#### Avance Obtenido
* Se restringieron los rangos del generador para evitar que las perturbaciones de muestra colisionen con fracciones comunes ($2/3, 4/3$) y se garantizó la separación psicométrica de opciones.

---

### Tabla Comparativa de Rendimiento de los Casos de Reparación

| Competencia | Shard | Causa Raíz Principal | Razón de la Demora | Estado / Avance Final |
| :---: | :---: | :--- | :--- | :--- |
| **`C-16`** | `shard_20` | 1. Discordancia de juez ciego en `T-C16-01`<br>2. Ratios $0.667/1.333$ en `T-C16-02` | Requirió 2 rondas completas de arbitraje ciego (20 jueces) y ajuste de dos plantillas distintas | ✅ **100% acuerdo en jueces**; corregido en `work/templates/C-16.json` |
| **`H-03`** | `shard_23` | Pista parentética `(sesgo negativo hacia abajo)` en Jensen | Bloqueo por hook guard (`pass_shard_23.json`) al compilar antes de editar | ✅ Coletillas eliminadas; opciones balanceadas en `work/templates/H-03.json` |
| **`Hab-04`** | `shard_04` | Distractores escalados por constantes (`1.333, 1.667`) | Necesidad de derivar errores de Jensen reales + bloqueo inicial del hook | ✅ Fórmulas algebraicas de error implementadas en `work/templates/Hab-04.json` |
| **`Hab-05`** | `shard_05` | Distractor por razón $0.667$ tras ajuste aditivo de duplicados | Variación sutil dependiente de la semilla en 1,030 preguntas | ✅ Errores basados en potencias de $\epsilon$ implementados en `work/templates/Hab-05.json` |
| **`Hab-09`** | `shard_09` | Distractor sintético explícito `ans / 2.0` | El autor original usó división constante en vez de fórmula diagnóstica | ✅ Reemplazado por fórmulas conceptuales de Chebyshev en `work/templates/Hab-09.json` |

---
*Documento generado por Antigravity en la auditoría forense del pipeline Content-to-Course.*
