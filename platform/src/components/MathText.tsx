import React, { useMemo } from 'react';
import katex from 'katex';

export interface MathPart {
  type: 'text' | 'inline-math' | 'block-math';
  content: string;
}

interface MathTextProps {
  text: string;
  className?: string;
  inline?: boolean;
}

/**
 * Pure helper function to split LaTeX formulas that contain embedded prose in \text{...} or \mbox{...}.
 * If the inner content has spaces or is long (>15 chars), it is extracted as plain text so it can wrap
 * naturally without KaTeX non-breaking spaces (\u00a0) or nowrap constraints.
 * Short mathematical operators (e.g., \text{plim}, \text{max}, \text{Var}) without spaces are preserved in math.
 */
export function splitMathAndProse(latex: string): Array<{ type: 'inline-math' | 'text'; content: string }> {
  const result: Array<{ type: 'inline-math' | 'text'; content: string }> = [];
  let remaining = latex;
  let mathBuffer = '';

  const textPattern = /\\(text|mbox)(?![a-zA-Z])\s*\{/;

  while (remaining.length > 0) {
    const match = textPattern.exec(remaining);
    if (!match) {
      mathBuffer += remaining;
      break;
    }

    const matchIndex = match.index;
    const braceStart = matchIndex + match[0].length - 1;

    // Balance braces to find corresponding closing brace
    let depth = 1;
    let closeIndex = -1;
    for (let i = braceStart + 1; i < remaining.length; i++) {
      if (remaining[i] === '\\') {
        i++; // skip escaped characters
        continue;
      }
      if (remaining[i] === '{') {
        depth++;
      } else if (remaining[i] === '}') {
        depth--;
        if (depth === 0) {
          closeIndex = i;
          break;
        }
      }
    }

    if (closeIndex === -1) {
      // Unbalanced braces; preserve rest as math
      mathBuffer += remaining;
      break;
    }

    let innerContent = remaining.slice(braceStart + 1, closeIndex);
    const isProse = /\s/.test(innerContent) || innerContent.length > 15;

    if (isProse) {
      const preceding = remaining.slice(0, matchIndex);
      mathBuffer += preceding;
      const cleanedMath = mathBuffer.trim().replace(/[\\~]+$/, '').trim();
      if (cleanedMath.length > 0) {
        result.push({ type: 'inline-math', content: cleanedMath });
      }
      mathBuffer = '';

      // Preserve spaces at boundary if present
      if (/[~\s]$/.test(preceding) && !/^\s/.test(innerContent)) {
        innerContent = ' ' + innerContent;
      }
      if (/^[~\s]/.test(remaining.slice(closeIndex + 1)) && !/\s$/.test(innerContent)) {
        innerContent = innerContent + ' ';
      }

      if (innerContent.length > 0) {
        result.push({ type: 'text', content: innerContent });
      }

      remaining = remaining.slice(closeIndex + 1);
    } else {
      // Keep short operator like \text{plim} in math
      mathBuffer += remaining.slice(0, closeIndex + 1);
      remaining = remaining.slice(closeIndex + 1);
    }
  }

  const finalCleaned = mathBuffer.trim().replace(/[\\~]+$/, '').trim();
  if (finalCleaned.length > 0) {
    result.push({ type: 'inline-math', content: finalCleaned });
  }

  return result;
}

export const MathText: React.FC<MathTextProps> = ({ text, className = '', inline = false }) => {
  const renderedContent = useMemo(() => {
    if (!text) return '';

    // Regex to split by $$...$$ (block) and $...$ (inline)
    const parts: MathPart[] = [];
    let remaining = text;

    while (remaining.length > 0) {
      // Check for block math $$...$$
      const blockStart = remaining.indexOf('$$');
      const inlineStart = remaining.indexOf('$');

      if (blockStart !== -1 && (inlineStart === -1 || blockStart <= inlineStart)) {
        if (blockStart > 0) {
          parts.push({ type: 'text', content: remaining.slice(0, blockStart) });
        }
        const blockEnd = remaining.indexOf('$$', blockStart + 2);
        if (blockEnd !== -1) {
          parts.push({
            type: 'block-math',
            content: remaining.slice(blockStart + 2, blockEnd),
          });
          remaining = remaining.slice(blockEnd + 2);
        } else {
          parts.push({ type: 'text', content: remaining.slice(blockStart) });
          break;
        }
      } else if (inlineStart !== -1) {
        if (inlineStart > 0) {
          parts.push({ type: 'text', content: remaining.slice(0, inlineStart) });
        }
        const inlineEnd = remaining.indexOf('$', inlineStart + 1);
        if (inlineEnd !== -1) {
          const rawInlineMath = remaining.slice(inlineStart + 1, inlineEnd);
          const subParts = splitMathAndProse(rawInlineMath);
          for (const sp of subParts) {
            parts.push(sp);
          }
          remaining = remaining.slice(inlineEnd + 1);
        } else {
          parts.push({ type: 'text', content: remaining.slice(inlineStart) });
          break;
        }
      } else {
        parts.push({ type: 'text', content: remaining });
        break;
      }
    }

    return parts.map((part, index) => {
      if (part.type === 'text') {
        return (
          <span key={index} className="inline break-words">
            {part.content}
          </span>
        );
      }

      const displayMode = part.type === 'block-math';
      try {
        let html = katex.renderToString(part.content, {
          throwOnError: false,
          displayMode,
        });
        if (!displayMode) {
          html = html.replace(/\u00a0/g, ' ');
        }
        return (
          <span
            key={index}
            className={displayMode ? 'block my-2 overflow-x-auto text-center' : 'inline mx-0.5'}
            dangerouslySetInnerHTML={{ __html: html }}
          />
        );
      } catch {
        return <span key={index} className="text-red-500 font-mono">${part.content}$</span>;
      }
    });
  }, [text]);

  const Tag = inline ? 'span' : 'div';
  return <Tag className={`leading-relaxed ${className}`}>{renderedContent}</Tag>;
};
