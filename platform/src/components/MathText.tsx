import React, { useMemo } from 'react';
import katex from 'katex';

interface MathTextProps {
  text: string;
  className?: string;
  inline?: boolean;
}

export const MathText: React.FC<MathTextProps> = ({ text, className = '', inline = false }) => {
  const renderedContent = useMemo(() => {
    if (!text) return '';

    // Regex to split by $$...$$ (block) and $...$ (inline)
    const parts: Array<{ type: 'text' | 'inline-math' | 'block-math'; content: string }> = [];
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
          parts.push({
            type: 'inline-math',
            content: remaining.slice(inlineStart + 1, inlineEnd),
          });
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
        return <span key={index}>{part.content}</span>;
      }

      const displayMode = part.type === 'block-math';
      try {
        const html = katex.renderToString(part.content, {
          throwOnError: false,
          displayMode,
        });
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
