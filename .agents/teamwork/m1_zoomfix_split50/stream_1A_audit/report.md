# Reporte de Auditoría Forense — Stream 1A: Question Grid & CSS Contract

**Fecha:** 2026-10-26  
**Auditor:** Auditor Forense (Stream 1A)  
**Veredicto Final:** **PASS::** Stream 1A cumple al 100% con los criterios de aceptación, frontera exclusiva, preservación de data-testid, inmutabilidad de lógica de estado y verificación de compilación/tests.

---

## 1. Verificación de Frontera de Código y Cero Residuos

| Archivo en Frontera Declarada | Estado | Verificación |
|---|---|---|
| `platform/src/components/QuestionCard.tsx` | MODIFICADO | Conforme a especificación del stream |
| `platform/src/index.css` | MODIFICADO | Conforme a especificación del stream |

- **Verificación de archivos fuera de frontera:** Stream 1A no modificó ningún archivo fuera de su frontera exclusiva (`QuestionCard.tsx` e `index.css`).
- **Verificación de residuos:** Cero archivos temporales (`*.tmp`, `*.bak`, etc.) ni archivos no rastreados en el árbol de trabajo.

---

## 2. Preservación de `data-testid` y Contratos UI

Se verificó la preservación exacta de todos los identificadores de prueba (`data-testid`) existentes:
- `data-testid="question-card"`: Preservado en el contenedor principal (`div.qc-root`).
- `data-testid="option-${opt.id}"`: Preservado en botones de opción MCQ (`button.qc-option-item`) y labels de multiselect (`label.qc-option-item`).
- `data-testid="multiselect-option"`: Preservado en los checkboxes de `multiple_select`.
- `data-testid="fill-blank-input"`: Preservado en el campo de texto de `fill_in_the_blank`.
- `data-testid="hints-toggle"`: Preservado en el botón del acordeón de pistas.
- `data-testid="hints-container"`: Preservado en el panel desplegable de pistas.
- `data-testid="reveal-hint-btn"`: Preservado en el botón de revelado de pistas.
- `data-testid="hint-item"`: Preservado en los contenedores individuales de pistas reveladas.
- Clases CSS heredadas para pruebas e2e (`option-item`, `answer-option`): Preservadas en cada opción.

---

## 3. Integridad de la Lógica de Estado y Navegación

- **Handlers de interacción intactos:**
  - `onSelectOption(opt.id)` llamado en `onClick`.
  - `onToggleMultiOption(opt.id)` llamado en `onChange`.
  - `onChangeFillBlank(e.target.value)` llamado en `onChange`.
  - `onRevealHint()` llamado en `onClick`.
  - `setShowHintsSection(!showHintsSection)` para alternar la sección de pistas.
- **Condiciones de deshabilitado intactas:**
  - `(isChecked && isCorrect === true) || isExhausted` respetado rigurosamente en opciones, checkboxes e input.
- **Lógica de evaluación intacta:**
  - Estados `isChecked`, `isCorrect`, `isMcqCorrectOpt`, `wrongSelected`, `isSelected` aplicados con exactitud cromática y accesibilidad (`aria-pressed`, `role="radiogroup"`, `role="group"`).

---

## 4. Validación de Criterios de Aceptación (AC)

- **AC-1 (Sin desborde horizontal):**
  - Implementado `.katex-display, .qc-root .katex, .qc-options .katex` con `max-width: 100%; overflow-x: auto; overflow-y: hidden; scrollbar-width: thin;`.
  - Clases `min-w-0` en opciones y contenedores internos para evitar blowout en CSS Grid.
  - Columnas en `minmax(0, 1fr)`.
- **AC-2 (MC7 2 columnas columna-primero 4+3 en ≥600px):**
  - `@container qc (min-width: 600px)` define `grid-auto-flow: column; grid-template-rows: repeat(var(--qc-rows, var(--rows, 4)), auto); grid-template-columns: repeat(2, minmax(0, 1fr));`.
  - Cálculo dinámico: `rowCount = Math.max(1, Math.ceil(optionsCount / 2))`, inyectado vía style inline dual `['--qc-rows']` y `['--rows']`.
  - Para 7 opciones: 4 filas por 2 columnas, distribuyendo A-D a la izquierda y E-G a la derecha. Aplica de forma idéntica a `multiple_select`.
- **AC-3 (Caben sin scroll vertical de página en 768px alto / scroll interno):**
  - Envoltorio `.qc-options-scroll` con `overflow-y: auto; max-height: calc(100vh - var(--qc-chrome, 14rem)); max-height: calc(100dvh - var(--qc-chrome, 14rem)); scrollbar-width: thin;`.
  - Reducción compacta de paddings (`py-3 sm:py-5 px-3 sm:px-4`) y márgenes.
- **AC-4 (<600px a 1 columna):**
  - `.qc-options` por defecto define `grid-template-columns: minmax(0, 1fr); grid-auto-flow: row;`.
- **AC-6 (Tipografía y espaciado elásticos):**
  - Variables CSS `:root`:
    - `--qc-gap: clamp(0.375rem, 1vh, 0.75rem);`
    - `--qc-pad: clamp(0.5rem, 1.5vh, 0.875rem);`
    - `--qc-font: clamp(0.875rem, 1.5vh, 1.125rem);`
    - `--qc-badge: clamp(1.5rem, 3.2vh, 2rem);`
    - `--qc-chrome: 14rem;`
  - Aplicadas a `.qc-stem`, `.qc-option-item`, `.qc-badge` y estilos inline.
- **Contrato Inter-Stream (§3):**
  - Definida la utilidad `.h-dvh-safe { min-height: 100vh; min-height: 100dvh; }` para uso coordinado por 1D y 1E.

---

## 5. Pruebas Automatizadas y Compilación

1. **`npm run build` en `platform/`:**
   - Comando: `tsc && vite build`
   - Salida: `✓ built in 6.17s`
   - Código de salida: 0 (CERO errores TypeScript, compilación exitosa).
2. **Suite Pytest (`.\pytest.cmd -q`):**
   - Ejecutados 1037 tests en 121.82s.
   - 1034 pasados, 1 saltado, 2 fallos preexistentes/ajenos a la frontera de 1A (`test_assemble_sanitize_katex_r23.py` y `test_future_milestones_byte_parity`).
   - CERO regresiones inducidas por Stream 1A.

---

## Veredicto Final

**PASS::** Stream 1A validado y aprobado sin observaciones bloqueantes.
