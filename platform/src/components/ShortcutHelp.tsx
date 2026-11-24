import React, { useEffect, useRef, useState } from 'react';

const SECTIONS: { title: string; items: [string, string][] }[] = [
  {
    title: 'During a practice / quiz / test',
    items: [
      ['A – G / 1 – 7', 'Select / toggle options without touching the mouse'],
      ['Enter', 'Reveal options (Blank-First) · Check answer · Next question · Retry'],
      ['Ctrl+S', 'Skip question'],
      ['P', 'Toggle Scratchpad / Pizarra'],
      ['Ctrl+Z / Ctrl+Y', 'Undo / Redo inside Pizarra'],
      ['Auto-focus', 'Fill-in-the-blank input is focused automatically'],
    ],
  },
  {
    title: 'On the results screen',
    items: [
      ['Enter', 'Next practice / quiz / unit test'],
      ['Ctrl+V', 'Back to the course (at the unit you just did)'],
    ],
  },
  {
    title: 'Anywhere',
    items: [
      ['?', 'Show / hide this help'],
      ['Esc', 'Close this help'],
    ],
  },
];

export const ShortcutHelp: React.FC = () => {
  const [open, setOpen] = useState(false);
  const dialogRef = useRef<HTMLDialogElement>(null);

  useEffect(() => {
    const el = dialogRef.current;
    if (!el) return;
    if (open && !el.open) {
      el.showModal();
    } else if (!open && el.open) {
      el.close();
    }
  }, [open]);

  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      if (e.isComposing) return;
      const t = e.target as HTMLElement | null;
      const typing = !!t && (t.tagName === 'INPUT' || t.tagName === 'TEXTAREA' || t.isContentEditable);
      if (e.key === '?' && !typing) {
        e.preventDefault();
        setOpen((o) => !o);
      }
    };
    window.addEventListener('keydown', onKey);
    return () => window.removeEventListener('keydown', onKey);
  }, []);

  return (
    <>
      <button
        type="button"
        data-testid="shortcut-help-btn"
        aria-label="Keyboard shortcuts"
        title="Keyboard shortcuts (?)"
        onClick={() => setOpen(true)}
        className="fixed bottom-24 right-4 z-[60] w-9 h-9 rounded-full bg-white border border-slate-300 shadow-md text-ka-blue font-bold hover:bg-slate-50"
      >
        ?
      </button>
      <dialog
        ref={dialogRef}
        onCancel={(e) => {
          e.preventDefault();
          setOpen(false);
        }}
        onClick={(e) => {
          if (e.target === e.currentTarget) setOpen(false);
        }}
        aria-label="Keyboard shortcuts"
        className="m-auto w-[calc(100%-2rem)] max-w-md bg-white rounded-xl shadow-2xl p-5 max-h-[90vh] overflow-y-auto border-0 backdrop:bg-black/40"
      >
        <div className="flex items-center justify-between mb-3">
          <h2 className="text-lg font-bold text-ka-text-primary">Keyboard shortcuts</h2>
          <button
            type="button"
            aria-label="Close"
            onClick={() => setOpen(false)}
            className="text-slate-500 hover:text-slate-800 text-xl leading-none"
          >
            ×
          </button>
        </div>
        {SECTIONS.map((s) => (
          <div key={s.title} className="mb-4">
            <h3 className="text-xs font-bold uppercase tracking-wider text-slate-500 mb-1.5">{s.title}</h3>
            <ul className="space-y-1.5">
              {s.items.map(([k, d]) => (
                <li key={k} className="flex items-center justify-between gap-3 text-sm">
                  <span className="text-ka-text-secondary">{d}</span>
                  <kbd className="shrink-0 px-2 py-0.5 text-xs font-bold bg-slate-100 border border-slate-300 rounded text-slate-700">
                    {k}
                  </kbd>
                </li>
              ))}
            </ul>
          </div>
        ))}
      </dialog>
    </>
  );
};
