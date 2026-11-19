import React, { useMemo, useRef } from 'react';
import katex from 'katex';
import { SymbolicConfig } from '../types';
import { checkSymbolicSyntax } from '../services/symbolicValidator';
import { MathKeypadPopover } from './MathKeypadPopover';

interface SymbolicInputProps {
  value: string;
  config?: SymbolicConfig;
  disabled?: boolean;
  isChecked?: boolean;
  isCorrect?: boolean | null;
  onChange: (value: string) => void;
  placeholder?: string;
}

export const SymbolicInput: React.FC<SymbolicInputProps> = ({
  value,
  config,
  disabled = false,
  isChecked = false,
  isCorrect = null,
  onChange,
  placeholder,
}) => {
  const inputRef = useRef<HTMLInputElement>(null);

  const syntax = useMemo(
    () => checkSymbolicSyntax(value, config?.variables),
    [value, config?.variables]
  );

  const renderedKatexHtml = useMemo(() => {
    if (!value.trim()) return '';
    try {
      const texSrc = syntax.valid && syntax.latexPreview ? syntax.latexPreview : value;
      return katex.renderToString(texSrc, { throwOnError: false, displayMode: false });
    } catch {
      return '';
    }
  }, [value, syntax.valid, syntax.latexPreview]);

  const insertToken = (token: string, cursorOffsetBack = 0) => {
    if (disabled) return;
    const el = inputRef.current;
    if (!el) {
      onChange(`${value}${token}`);
      return;
    }
    const start = el.selectionStart ?? value.length;
    const end = el.selectionEnd ?? value.length;
    const next = `${value.slice(0, start)}${token}${value.slice(end)}`;
    onChange(next);
    requestAnimationFrame(() => {
      el.focus();
      const pos = Math.max(0, start + token.length - cursorOffsetBack);
      el.setSelectionRange(pos, pos);
    });
  };

  const handleBackspace = () => {
    if (disabled || !value) return;
    const el = inputRef.current;
    if (!el) {
      onChange(value.slice(0, -1));
      return;
    }
    const start = el.selectionStart ?? value.length;
    const end = el.selectionEnd ?? value.length;
    let next = value;
    let nextPos = start;
    if (start !== end) {
      next = `${value.slice(0, start)}${value.slice(end)}`;
      nextPos = start;
    } else if (start > 0) {
      next = `${value.slice(0, start - 1)}${value.slice(end)}`;
      nextPos = start - 1;
    }
    onChange(next);
    requestAnimationFrame(() => {
      el.focus();
      el.setSelectionRange(nextPos, nextPos);
    });
  };

  return (
    <div data-testid="symbolic-input-root" className="space-y-2.5 max-w-xl w-full">
      {config?.variables && config.variables.length > 0 && (
        <div className="flex flex-wrap items-center gap-1.5 text-xs text-slate-600">
          <span className="font-semibold text-slate-500">Variables permitidas:</span>
          {config.variables.map((v) => (
            <button
              key={v}
              type="button"
              disabled={disabled}
              onClick={() => insertToken(v)}
              className="px-2 py-0.5 bg-slate-100 hover:bg-slate-200 border border-slate-300 rounded font-mono text-xs text-slate-800 cursor-pointer disabled:opacity-50"
            >
              {v}
            </button>
          ))}
        </div>
      )}

      <div className="relative">
        <input
          ref={inputRef}
          type="text"
          data-testid="symbolic-input"
          aria-label="Expresión simbólica"
          value={value}
          disabled={disabled}
          onChange={(e) => onChange(e.target.value)}
          placeholder={placeholder || config?.placeholder || 'Escribe una expresión simbólica (ej: m*g*sin(theta))...'}
          className={`w-full p-3 pr-12 font-mono text-sm sm:text-base border-2 rounded-lg outline-none transition-all ${
            disabled && isCorrect
              ? 'border-ka-green-border bg-emerald-50/40 text-ka-green-text'
              : isChecked && isCorrect === false
              ? 'border-red-500 bg-red-50/40 text-red-800'
              : 'border-slate-300 focus:border-ka-blue focus:ring-2 focus:ring-blue-100 bg-white'
          }`}
        />
        <div className="absolute right-2 top-1/2 -translate-y-1/2">
          <MathKeypadPopover
            variables={config?.variables}
            disabled={disabled}
            onInsert={insertToken}
            onBackspace={handleBackspace}
          />
        </div>
      </div>

      {value.trim() && (
        <div className="flex flex-wrap items-center justify-between gap-2 p-2.5 bg-slate-50 border border-slate-200 rounded-lg text-sm">
          <div className="min-w-0 flex items-center gap-2 overflow-x-auto">
            <span className="text-[11px] font-bold text-slate-400 uppercase tracking-wider shrink-0">
              Vista previa:
            </span>
            <span
              data-testid="symbolic-preview"
              className="text-slate-800"
              dangerouslySetInnerHTML={{ __html: renderedKatexHtml }}
            />
          </div>
          <span
            data-testid="symbolic-syntax-badge"
            className={`text-[11px] font-bold px-2 py-0.5 rounded-full shrink-0 ${
              syntax.valid
                ? 'bg-emerald-100 text-emerald-800 border border-emerald-300'
                : 'bg-amber-100 text-amber-900 border border-amber-300'
            }`}
          >
            {syntax.valid ? 'Sintaxis válida' : syntax.error || 'Revisar sintaxis'}
          </span>
        </div>
      )}
    </div>
  );
};
