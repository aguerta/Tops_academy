import React, { useEffect, useState } from 'react';

const SECTIONS: { title: string; items: [string, string][] }[] = [
  {
    title: 'During a practice / quiz / test',
    items: [
      ['A – G / 1 – 7', 'Select / toggle options without touching the mouse'],
      ['Enter', 'Reveal options (Blank-First) · Check answer · Next question · Retry'],
      ['Ctrl+S', 'Skip question'],
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

  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      if (e.isComposing) return;
      const t = e.target as HTMLElement | null;
      const typing = !!t && (t.tagName === 'INPUT' || t.tagName === 'TEXTAREA' || t.isContentEditable);
      if (e.key === 'Escape') setOpen(false);
      else if (e.key === '?' && !typing) {
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
      {open && (
        <div
          className="fixed inset-0 z-[70] bg-black/40 flex items-center justify-center p-4"
          onClick={() => setOpen(false)}
          role="dialog"
          aria-modal="true"
          aria-label="Keyboard shortcuts"
        >
          <div
            className="bg-white rounded-xl shadow-2xl w-full max-w-md p-5 max-h-[90vh] overflow-y-auto"
            onClick={(e) => e.stopPropagation()}
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
          </div>
        </div>
      )}
    </>
  );
};
