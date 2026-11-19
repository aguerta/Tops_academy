import React, { useCallback, useEffect, useLayoutEffect, useRef, useState } from 'react';
import { createPortal } from 'react-dom';
import { Delete, X } from 'lucide-react';

export type MathKeypadTab = '123' | 'vars' | 'ops' | 'trig';

export interface MathKeypadPopoverProps {
  variables?: string[];
  disabled?: boolean;
  onInsert: (token: string, cursorOffsetBack?: number) => void;
  onBackspace: () => void;
}

interface PopoverCoords {
  top: number;
  left: number;
  caretLeft: number;
  placement: 'above' | 'below';
  showCaret: boolean;
  ready: boolean;
}

const ECON_GREEK_KEYS: Array<{ id: string; sym: string; label: string }> = [
  { id: 'alpha', sym: 'α', label: 'Alfa (α)' },
  { id: 'beta', sym: 'β', label: 'Beta (β)' },
  { id: 'gamma', sym: 'γ', label: 'Gamma (γ)' },
  { id: 'delta', sym: 'δ', label: 'Delta (δ)' },
  { id: 'epsilon', sym: 'ε', label: 'Épsilon (ε)' },
  { id: 'lambda', sym: 'λ', label: 'Lambda (λ)' },
  { id: 'mu', sym: 'μ', label: 'Mu (μ)' },
  { id: 'sigma', sym: 'σ', label: 'Sigma (σ)' },
  { id: 'rho', sym: 'ρ', label: 'Rho (ρ)' },
  { id: 'theta', sym: 'θ', label: 'Theta (θ)' },
  { id: 'omega', sym: 'ω', label: 'Omega (ω)' },
  { id: 'eta', sym: 'η', label: 'Eta (η)' },
  { id: 'tau', sym: 'τ', label: 'Tau (τ)' },
  { id: 'phi', sym: 'φ', label: 'Phi (φ)' },
  { id: 'pi', sym: 'π', label: 'Pi (π)' },
  { id: 'Delta', sym: 'Δ', label: 'Delta mayúscula (Δ)' },
];

const KEY_BTN_CLS =
  'h-9 sm:h-10 rounded-md bg-white hover:bg-slate-50 active:translate-y-px border border-slate-200/90 shadow-2xs flex items-center justify-center text-sm sm:text-[15px] font-medium text-slate-800 transition-all cursor-pointer select-none';

const OP_KEY_CLS =
  'h-9 sm:h-10 rounded-md bg-white hover:bg-blue-50 active:translate-y-px border border-slate-200/90 shadow-2xs flex items-center justify-center text-base font-medium text-slate-800 transition-all cursor-pointer select-none';

export const MathKeypadPopover: React.FC<MathKeypadPopoverProps> = ({
  variables = [],
  disabled = false,
  onInsert,
  onBackspace,
}) => {
  const [open, setOpen] = useState(false);
  const [activeTab, setActiveTab] = useState<MathKeypadTab>('123');
  const [coords, setCoords] = useState<PopoverCoords>({
    top: 0,
    left: 0,
    caretLeft: 24,
    placement: 'below',
    showCaret: true,
    ready: false,
  });
  const rootRef = useRef<HTMLDivElement>(null);
  const triggerRef = useRef<HTMLButtonElement>(null);
  const popoverRef = useRef<HTMLDivElement>(null);

  const updatePlacement = useCallback(() => {
    const btn = triggerRef.current;
    if (!btn) return;
    const btnRect = btn.getBoundingClientRect();
    const MARGIN = 12;
    const GAP = 10;
    const vw = window.innerWidth;
    const vh = window.innerHeight;
    const popEl = popoverRef.current;
    const popW = popEl?.offsetWidth || Math.min(vw - MARGIN * 2, vw >= 640 ? 374 : 332);
    const popH = popEl?.offsetHeight || 285;

    const idealLeft = btnRect.right - popW + 8;
    const left = Math.max(MARGIN, Math.min(idealLeft, Math.max(MARGIN, vw - popW - MARGIN)));
    const triggerCenterX = btnRect.left + btnRect.width / 2;
    const caretLeft = Math.max(16, Math.min(triggerCenterX - left - 6, popW - 28));

    const spaceBelow = vh - btnRect.bottom - MARGIN;
    const spaceAbove = btnRect.top - MARGIN;
    const placement: 'above' | 'below' =
      spaceBelow >= popH + GAP
        ? 'below'
        : spaceAbove >= popH + GAP
          ? 'above'
          : spaceAbove > spaceBelow
            ? 'above'
            : 'below';

    const rawTop = placement === 'below' ? btnRect.bottom + GAP : btnRect.top - popH - GAP;
    const top = Math.max(MARGIN, Math.min(rawTop, Math.max(MARGIN, vh - popH - MARGIN)));
    const showCaret = Math.abs(top - rawTop) <= 12;

    setCoords({ top, left, caretLeft, placement, showCaret, ready: true });
  }, []);

  useLayoutEffect(() => {
    if (!open || disabled) {
      setCoords((prev) => (prev.ready ? { ...prev, ready: false } : prev));
      return;
    }
    updatePlacement();
    const raf = requestAnimationFrame(updatePlacement);
    const popEl = popoverRef.current;
    const ro = typeof ResizeObserver !== 'undefined' && popEl ? new ResizeObserver(updatePlacement) : null;
    if (ro && popEl) ro.observe(popEl);
    window.addEventListener('resize', updatePlacement);
    window.addEventListener('scroll', updatePlacement, true);
    return () => {
      cancelAnimationFrame(raf);
      ro?.disconnect();
      window.removeEventListener('resize', updatePlacement);
      window.removeEventListener('scroll', updatePlacement, true);
    };
  }, [open, disabled, activeTab, updatePlacement]);

  useEffect(() => {
    if (!open) return;

    const onDocClick = (e: MouseEvent) => {
      const target = e.target as Node;
      if (rootRef.current?.contains(target) || popoverRef.current?.contains(target)) {
        return;
      }
      setOpen(false);
    };
    const onKey = (e: KeyboardEvent) => {
      if (e.key === 'Escape') {
        e.preventDefault();
        e.stopPropagation();
        e.stopImmediatePropagation();
        setOpen(false);
      }
    };
    window.addEventListener('mousedown', onDocClick);
    window.addEventListener('keydown', onKey, true);
    return () => {
      window.removeEventListener('mousedown', onDocClick);
      window.removeEventListener('keydown', onKey, true);
    };
  }, [open]);

  const keepFocus = (e: React.MouseEvent) => e.preventDefault();

  const renderFractionGlyph = () => (
    <span className="inline-flex flex-col items-center leading-none text-[8px] font-bold">
      <span className="w-2.5 h-2 border border-slate-700 rounded-[1px]" />
      <span className="w-3.5 h-[1.5px] bg-slate-800 my-[1.5px]" />
      <span className="w-2.5 h-2 border border-slate-700 rounded-[1px]" />
    </span>
  );

  const renderOperatorRail = () => (
    <div className="grid grid-cols-3 gap-1.5 shrink-0 w-[124px] sm:w-[138px]">
      <button
        type="button"
        onMouseDown={keepFocus}
        onClick={() => onInsert('/')}
        title="Fracción / División"
        aria-label="División"
        className={OP_KEY_CLS}
      >
        {renderFractionGlyph()}
      </button>
      <button
        type="button"
        onMouseDown={keepFocus}
        onClick={() => onInsert('+')}
        title="Suma"
        aria-label="Más"
        className={OP_KEY_CLS}
      >
        +
      </button>
      <button
        type="button"
        onMouseDown={keepFocus}
        onClick={() => onInsert('-')}
        title="Resta"
        aria-label="Menos"
        className={OP_KEY_CLS}
      >
        −
      </button>

      <div />
      <button
        type="button"
        onMouseDown={keepFocus}
        onClick={() => onInsert('*')}
        title="Multiplicación"
        aria-label="Por"
        className={OP_KEY_CLS}
      >
        ·
      </button>
      <div />

      <div />
      <button
        type="button"
        onMouseDown={keepFocus}
        onClick={() => onInsert('(')}
        title="Paréntesis izquierdo"
        aria-label="Abrir paréntesis"
        className={OP_KEY_CLS}
      >
        (
      </button>
      <button
        type="button"
        onMouseDown={keepFocus}
        onClick={() => onInsert(')')}
        title="Paréntesis derecho"
        aria-label="Cerrar paréntesis"
        className={OP_KEY_CLS}
      >
        )
      </button>

      <div />
      <div />
      <button
        type="button"
        data-testid="math-keypad-backspace-btn"
        onMouseDown={keepFocus}
        onClick={onBackspace}
        title="Borrar último carácter"
        aria-label="Retroceso"
        className={OP_KEY_CLS}
      >
        <Delete className="w-4 h-4 text-slate-700" />
      </button>
    </div>
  );

  return (
    <div ref={rootRef} className="inline-block">
      <button
        ref={triggerRef}
        type="button"
        data-testid="math-keypad-toggle-btn"
        disabled={disabled}
        onMouseDown={keepFocus}
        onClick={() => setOpen((o) => !o)}
        aria-expanded={open}
        aria-label="Abrir teclado matemático"
        title="Teclado matemático y letras griegas de economía"
        className={`w-8 h-8 rounded flex items-center justify-center transition-colors shadow-xs ${
          disabled
            ? 'bg-slate-200 text-slate-400 cursor-not-allowed'
            : open
              ? 'bg-ka-blue text-white cursor-pointer'
              : 'bg-slate-600 hover:bg-slate-700 text-white cursor-pointer'
        }`}
      >
        <span className="grid grid-cols-2 gap-x-1 leading-[9px] text-[9px] font-bold">
          <span>−</span>
          <span>×</span>
          <span>+</span>
          <span>=</span>
        </span>
      </button>

      {open && !disabled && typeof document !== 'undefined' && createPortal(
        <div
          ref={popoverRef}
          data-testid="math-keypad-popover"
          role="dialog"
          aria-label="Teclado matemático estilo Khan Academy"
          style={{
            top: `${coords.top}px`,
            left: `${coords.left}px`,
            visibility: coords.ready ? 'visible' : 'hidden',
          }}
          className="fixed z-[60] w-[332px] sm:w-[374px] max-w-[calc(100vw-24px)] rounded-xl border border-slate-300 bg-white shadow-2xl"
        >
          {/* Caret pointer */}
          {coords.showCaret && (
            <div
              aria-hidden="true"
              style={{ left: `${coords.caretLeft}px` }}
              className={`absolute w-3 h-3 border-slate-300 rotate-45 ${
                coords.placement === 'above'
                  ? '-bottom-1.5 border-r border-b bg-[#f1f3f5]'
                  : '-top-1.5 border-l border-t bg-white'
              }`}
            />
          )}

          {/* 4-Tab Header Bar */}
          <div className="flex items-center justify-between px-2.5 pt-1 bg-white rounded-t-xl border-b border-slate-200">
            <div className="flex items-center gap-1 sm:gap-2" role="tablist">
              <button
                type="button"
                role="tab"
                aria-selected={activeTab === '123'}
                data-testid="math-keypad-tab-123"
                onMouseDown={keepFocus}
                onClick={() => setActiveTab('123')}
                className={`px-2.5 py-2 text-xs font-extrabold tracking-tight border-b-2 transition-colors cursor-pointer ${
                  activeTab === '123'
                    ? 'text-ka-blue border-ka-blue'
                    : 'text-slate-500 border-transparent hover:text-slate-800'
                }`}
              >
                123
              </button>

              <button
                type="button"
                role="tab"
                aria-selected={activeTab === 'vars'}
                data-testid="math-keypad-tab-vars"
                onMouseDown={keepFocus}
                onClick={() => setActiveTab('vars')}
                title="Variables y letras griegas de economía (α, β, γ, ω, ...)"
                className={`px-2.5 py-2 text-sm font-serif italic font-bold border-b-2 transition-colors cursor-pointer ${
                  activeTab === 'vars'
                    ? 'text-ka-blue border-ka-blue'
                    : 'text-slate-500 border-transparent hover:text-slate-800'
                }`}
              >
                xπ
              </button>

              <button
                type="button"
                role="tab"
                aria-selected={activeTab === 'ops'}
                data-testid="math-keypad-tab-ops"
                onMouseDown={keepFocus}
                onClick={() => setActiveTab('ops')}
                title="Potencias, raíces, subíndices y desigualdades"
                className={`px-2.5 py-2 text-xs font-bold border-b-2 transition-colors cursor-pointer ${
                  activeTab === 'ops'
                    ? 'text-ka-blue border-ka-blue'
                    : 'text-slate-500 border-transparent hover:text-slate-800'
                }`}
              >
                √□²&lt;
              </button>

              <button
                type="button"
                role="tab"
                aria-selected={activeTab === 'trig'}
                data-testid="math-keypad-tab-trig"
                onMouseDown={keepFocus}
                onClick={() => setActiveTab('trig')}
                title="Funciones trigonométricas, logaritmos y exponenciales"
                className={`px-2.5 py-2 text-xs font-bold border-b-2 transition-colors cursor-pointer ${
                  activeTab === 'trig'
                    ? 'text-ka-blue border-ka-blue'
                    : 'text-slate-500 border-transparent hover:text-slate-800'
                }`}
              >
                ⊿
              </button>
            </div>

            <button
              type="button"
              data-testid="math-keypad-close-btn"
              onMouseDown={keepFocus}
              onClick={() => setOpen(false)}
              aria-label="Cerrar teclado matemático"
              className="p-1.5 rounded-md text-slate-400 hover:text-slate-700 hover:bg-slate-100 cursor-pointer"
            >
              <X className="w-4 h-4" />
            </button>
          </div>

          {/* Tab Key Matrix */}
          <div className="bg-[#f1f3f5] p-2.5 rounded-b-xl max-h-[calc(100vh-88px)] overflow-y-auto">
            {activeTab === '123' && (
              <div className="grid grid-cols-6 gap-1.5">
                {['7', '8', '9'].map((d) => (
                  <button
                    key={d}
                    type="button"
                    data-testid={`math-keypad-key-${d}`}
                    onMouseDown={keepFocus}
                    onClick={() => onInsert(d)}
                    className={KEY_BTN_CLS}
                  >
                    {d}
                  </button>
                ))}
                <button
                  type="button"
                  onMouseDown={keepFocus}
                  onClick={() => onInsert('/100')}
                  title="Porcentaje (/100)"
                  className={KEY_BTN_CLS}
                >
                  %
                </button>
                <button type="button" onMouseDown={keepFocus} onClick={() => onInsert('+')} className={OP_KEY_CLS}>
                  +
                </button>
                <button type="button" onMouseDown={keepFocus} onClick={() => onInsert('-')} className={OP_KEY_CLS}>
                  −
                </button>

                {['4', '5', '6'].map((d) => (
                  <button
                    key={d}
                    type="button"
                    data-testid={`math-keypad-key-${d}`}
                    onMouseDown={keepFocus}
                    onClick={() => onInsert(d)}
                    className={KEY_BTN_CLS}
                  >
                    {d}
                  </button>
                ))}
                <button type="button" onMouseDown={keepFocus} onClick={() => onInsert('/')} className={OP_KEY_CLS} title="Fracción">
                  {renderFractionGlyph()}
                </button>
                <button type="button" onMouseDown={keepFocus} onClick={() => onInsert('*')} className={OP_KEY_CLS} title="Multiplicación">
                  ·
                </button>
                <div />

                {['1', '2', '3'].map((d) => (
                  <button
                    key={d}
                    type="button"
                    data-testid={`math-keypad-key-${d}`}
                    onMouseDown={keepFocus}
                    onClick={() => onInsert(d)}
                    className={KEY_BTN_CLS}
                  >
                    {d}
                  </button>
                ))}
                <div />
                <button type="button" onMouseDown={keepFocus} onClick={() => onInsert('(')} className={OP_KEY_CLS}>
                  (
                </button>
                <button type="button" onMouseDown={keepFocus} onClick={() => onInsert(')')} className={OP_KEY_CLS}>
                  )
                </button>

                <button
                  type="button"
                  data-testid="math-keypad-key-0"
                  onMouseDown={keepFocus}
                  onClick={() => onInsert('0')}
                  className={KEY_BTN_CLS}
                >
                  0
                </button>
                <button type="button" onMouseDown={keepFocus} onClick={() => onInsert('.')} className={KEY_BTN_CLS}>
                  .
                </button>
                <button
                  type="button"
                  onMouseDown={keepFocus}
                  onClick={() => onInsert('-')}
                  title="Signo negativo"
                  className={KEY_BTN_CLS}
                >
                  (−)
                </button>
                <div />
                <div />
                <button
                  type="button"
                  data-testid="math-keypad-backspace-btn"
                  onMouseDown={keepFocus}
                  onClick={onBackspace}
                  aria-label="Retroceso"
                  className={OP_KEY_CLS}
                >
                  <Delete className="w-4 h-4 text-slate-700" />
                </button>
              </div>
            )}

            {activeTab === 'vars' && (
              <div className="flex items-start gap-2">
                <div className="flex-1 min-w-0 space-y-2">
                  {variables.length > 0 && (
                    <div>
                      <div className="text-[10px] font-bold uppercase tracking-wider text-slate-500 mb-1">
                        Del ejercicio
                      </div>
                      <div className="grid grid-cols-3 gap-1">
                        {variables.map((v) => (
                          <button
                            key={v}
                            type="button"
                            data-testid={`math-keypad-var-${v}`}
                            onMouseDown={keepFocus}
                            onClick={() => onInsert(v)}
                            className={`${KEY_BTN_CLS} !h-8 font-serif italic text-ka-blue`}
                          >
                            {v}
                          </button>
                        ))}
                      </div>
                    </div>
                  )}

                  <div>
                    <div className="text-[10px] font-bold uppercase tracking-wider text-slate-500 mb-1">
                      Griegas (Economía)
                    </div>
                    <div className="grid grid-cols-4 gap-1">
                      {ECON_GREEK_KEYS.map((g) => (
                        <button
                          key={g.id}
                          type="button"
                          data-testid={`math-keypad-key-${g.id}`}
                          title={g.label}
                          aria-label={g.label}
                          onMouseDown={keepFocus}
                          onClick={() => onInsert(g.sym)}
                          className={`${KEY_BTN_CLS} !h-8 font-serif italic`}
                        >
                          {g.sym}
                        </button>
                      ))}
                    </div>
                  </div>
                </div>
                {renderOperatorRail()}
              </div>
            )}

            {activeTab === 'ops' && (
              <div className="flex items-start gap-2">
                <div className="flex-1 min-w-0 grid grid-cols-3 gap-1.5">
                  <button
                    type="button"
                    data-testid="math-keypad-key-sq"
                    onMouseDown={keepFocus}
                    onClick={() => onInsert('^2')}
                    title="Al cuadrado"
                    className={KEY_BTN_CLS}
                  >
                    □²
                  </button>
                  <button
                    type="button"
                    data-testid="math-keypad-key-pow"
                    onMouseDown={keepFocus}
                    onClick={() => onInsert('^')}
                    title="Exponente"
                    className={KEY_BTN_CLS}
                  >
                    □ⁿ
                  </button>
                  <button
                    type="button"
                    data-testid="math-keypad-key-sqrt"
                    onMouseDown={keepFocus}
                    onClick={() => onInsert('sqrt()', 1)}
                    title="Raíz cuadrada"
                    className={KEY_BTN_CLS}
                  >
                    √□
                  </button>
                  <button
                    type="button"
                    onMouseDown={keepFocus}
                    onClick={() => onInsert('^(1/)', 1)}
                    title="Raíz n-ésima"
                    className={KEY_BTN_CLS}
                  >
                    ⁿ√□
                  </button>
                  <button
                    type="button"
                    onMouseDown={keepFocus}
                    onClick={() => onInsert('_')}
                    title="Subíndice"
                    className={KEY_BTN_CLS}
                  >
                    x_□
                  </button>
                  <button
                    type="button"
                    onMouseDown={keepFocus}
                    onClick={() => onInsert('abs()', 1)}
                    title="Valor absoluto"
                    className={KEY_BTN_CLS}
                  >
                    |□|
                  </button>
                  <button type="button" onMouseDown={keepFocus} onClick={() => onInsert('<')} className={KEY_BTN_CLS}>
                    &lt;
                  </button>
                  <button type="button" onMouseDown={keepFocus} onClick={() => onInsert('<=')} className={KEY_BTN_CLS}>
                    ≤
                  </button>
                  <button type="button" onMouseDown={keepFocus} onClick={() => onInsert('>')} className={KEY_BTN_CLS}>
                    &gt;
                  </button>
                  <button type="button" onMouseDown={keepFocus} onClick={() => onInsert('>=')} className={KEY_BTN_CLS}>
                    ≥
                  </button>
                </div>
                {renderOperatorRail()}
              </div>
            )}

            {activeTab === 'trig' && (
              <div className="flex items-start gap-2">
                <div className="flex-1 min-w-0 grid grid-cols-3 gap-1.5">
                  <button type="button" onMouseDown={keepFocus} onClick={() => onInsert('sin()', 1)} className={KEY_BTN_CLS}>
                    sin
                  </button>
                  <button type="button" onMouseDown={keepFocus} onClick={() => onInsert('cos()', 1)} className={KEY_BTN_CLS}>
                    cos
                  </button>
                  <button type="button" onMouseDown={keepFocus} onClick={() => onInsert('tan()', 1)} className={KEY_BTN_CLS}>
                    tan
                  </button>
                  <button type="button" onMouseDown={keepFocus} onClick={() => onInsert('ln()', 1)} className={KEY_BTN_CLS}>
                    ln
                  </button>
                  <button type="button" onMouseDown={keepFocus} onClick={() => onInsert('log()', 1)} className={KEY_BTN_CLS}>
                    log
                  </button>
                  <button type="button" onMouseDown={keepFocus} onClick={() => onInsert('exp()', 1)} className={KEY_BTN_CLS}>
                    exp
                  </button>
                  <button type="button" onMouseDown={keepFocus} onClick={() => onInsert('e')} className={`${KEY_BTN_CLS} font-serif italic`}>
                    e
                  </button>
                </div>
                {renderOperatorRail()}
              </div>
            )}
          </div>
        </div>,
        document.body
      )}
    </div>
  );
};
