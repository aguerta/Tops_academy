"""
Test regex scanner for LaTeX single backslash corruption on raw JSON text.
"""
import re

with open('system_prompts/output_example_exercises.json', 'r', encoding='utf-8') as f:
    raw_text = f.read()

# Pattern for single backslash in raw file:
# A backslash that is not preceded by a backslash, and not followed by a backslash.
# In Python regex on raw_text:
# We look for backslashes:
corruptions = []
for m in re.finditer(r'(?<!\\)\\(?!\\)([a-zA-Z]+)', raw_text):
    cmd = m.group(1)
    span = m.span()
    line_no = raw_text[:span[0]].count('\n') + 1
    corruptions.append((line_no, cmd, raw_text[max(0, span[0]-15):min(len(raw_text), span[1]+15)]))

print(f"Total single-backslash LaTeX commands found in raw text: {len(corruptions)}")
from collections import Counter
cmd_counts = Counter([c[1] for c in corruptions])
print("\nTop corrupted commands:")
for cmd, count in cmd_counts.most_common(20):
    print(f"  \\{cmd}: {count}")

