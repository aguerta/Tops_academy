const LATEX_REPLACEMENTS: Array<[RegExp, string]> = [
  [/\\(?:text|mathrm|mathbf|mathit|operatorname)\{([^{}]*)\}/g, '$1'],
  [/\\frac\{([^{}]+)\}\{([^{}]+)\}/g, '($1)/($2)'],
  [/\\sqrt\{([^{}]+)\}/g, 'sqrt($1)'],
  [/\\bar\{([^{}]+)\}/g, '$1_bar'],
  [/\\hat\{([^{}]+)\}/g, '$1_hat'],
  [/\\leq?/g, '≤'],
  [/\\geq?/g, '≥'],
  [/\\neq?/g, '≠'],
  [/\\approx/g, '≈'],
  [/\\equiv/g, '≡'],
  [/\\infty/g, '∞'],
  [/\\cdot/g, '·'],
  [/\\times/g, '×'],
  [/\\partial/g, '∂'],
  [/\\nabla/g, '∇'],
  [/\\forall/g, '∀'],
  [/\\exists/g, '∃'],
  [/\\in\b/g, '∈'],
  [/\\notin\b/g, '∉'],
  [/\\subset(?:eq)?/g, '⊂'],
  [/\\rightarrow|\\to\b/g, '→'],
  [/\\Rightarrow|\\implies/g, '⇒'],
  [/\\alpha/g, 'α'],
  [/\\beta/g, 'β'],
  [/\\gamma/g, 'γ'],
  [/\\delta/g, 'δ'],
  [/\\Delta/g, 'Δ'],
  [/\\varepsilon|\\epsilon/g, 'ε'],
  [/\\theta/g, 'θ'],
  [/\\lambda/g, 'λ'],
  [/\\mu/g, 'μ'],
  [/\\pi/g, 'π'],
  [/\\rho/g, 'ρ'],
  [/\\sigma/g, 'σ'],
  [/\\phi/g, 'φ'],
  [/\\psi/g, 'ψ'],
  [/\\omega/g, 'ω'],
];

/**
 * Checks whether a string contains raw LaTeX delimiters or commands.
 */
export function hasRawLatex(raw?: string | null): boolean {
  if (!raw) return false;
  return raw.includes('$') || raw.includes('\\');
}

/**
 * Converts a KaTeX string into readable plain text safe for native HTML `<option>` elements
 * (guarantees zero raw `$` or `\` characters).
 */
export function toPlainOptionLabel(raw: string, fallbackLabel?: string): string {
  let out = String(raw || '');
  out = out.replace(/\$\$/g, '').replace(/\$/g, '');
  // Run multiple passes to resolve shallowly nested \frac / \text blocks
  for (let pass = 0; pass < 2; pass++) {
    for (const [pat, repl] of LATEX_REPLACEMENTS) {
      out = out.replace(pat, repl);
    }
  }
  out = out
    .replace(/\\([A-Za-z]+)/g, '$1')
    .replace(/\\/g, '')
    .replace(/[{}]/g, '')
    .replace(/\s+/g, ' ')
    .trim();
  return out || fallbackLabel || 'Opción';
}
