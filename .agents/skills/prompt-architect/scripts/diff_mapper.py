#!/usr/bin/env python3
"""
diff_mapper.py - Explicit change mapping for prompt edits (v2).

Compares an original prompt with a proposed version (which must live in the
conversation scratch directory, never in the repo) and reports:
  - unified diff
  - section-level changes (headings / XML tags added, removed, kept)
  - contract tokens lost (placeholders, paths, output signals, JSON keys)
It never writes to the original file.
"""

import sys
import os
import re
import difflib
import argparse

TOKEN_PATTERNS = {
    "placeholder {x}": r"\{[A-Za-z_][A-Za-z0-9_]*\}",
    "placeholder <x>": r"<[a-z_]+(?:_id|_dir|_path|_XX)?>",
    "placeholder @x@": r"@[A-Za-z_]+@",
    "ruta": r"(?:[\w.-]+/)+[\w.<>*-]+(?:\.\w+)?",
    "señal": r"\b(?:DONE|BLOCKED)\b:?",
    "clave JSON": r"\"([a-z_]{3,})\"\s*:",
    "regla id": r"\b[A-Z]{2,5}-[A-Z]?\d+\b",
}


def extract_tokens(text: str) -> dict:
    out = {}
    for name, pat in TOKEN_PATTERNS.items():
        out[name] = set(m if isinstance(m, str) else m[0] for m in re.findall(pat, text))
    return out


def sections(text: str) -> list:
    heads = [l.strip() for l in text.splitlines() if re.match(r"^#{1,4}\s", l)]
    tags = sorted(set(re.findall(r"^\s*<([a-z_]+)>", text, re.M)))
    return heads + [f"<{t}>" for t in tags]


def build_report(orig_path, orig, prop, reason):
    name = os.path.basename(orig_path)
    diff = "".join(difflib.unified_diff(orig.splitlines(True), prop.splitlines(True),
                                        f"a/{name} (actual)", f"b/{name} (propuesto)", n=2))
    so, sp = sections(orig), sections(prop)
    to, tp = extract_tokens(orig), extract_tokens(prop)
    lost = {k: sorted(to[k] - tp[k]) for k in to if to[k] - tp[k]}
    added_lines = sum(1 for l in diff.splitlines() if l.startswith("+") and not l.startswith("+++"))
    removed_lines = sum(1 for l in diff.splitlines() if l.startswith("-") and not l.startswith("---"))

    r = [f"# Mapeo explícito de cambios: `{name}`\n",
         f"**Archivo objetivo:** `{orig_path}`  ",
         f"**Motivo:** {reason}  ",
         f"**Diff:** `+{added_lines}` / `-{removed_lines}` líneas\n",
         "## 1. Secciones", "| Sección | Estado |", "|:---|:---|"]
    for s in so:
        r.append(f"| {s} | {'conservada' if s in sp else '**eliminada / renombrada**'} |")
    for s in sp:
        if s not in so:
            r.append(f"| {s} | **nueva** |")
    r.append("\n## 2. Contratos y tokens críticos")
    if lost:
        r.append("> [!WARNING]\n> Tokens presentes en el original que no aparecen en la propuesta. Confirmar que la pérdida es intencional:")
        for k, v in lost.items():
            r.append(f"- **{k}:** `{'`, `'.join(v)}`")
    else:
        r.append("Sin pérdida de placeholders, rutas, señales, claves JSON ni IDs de regla.")
    r.append("\n## 3. Diff unificado\n```diff")
    r.append(diff or "(sin diferencias)")
    r.append("```\n\n## 4. Autorización\nNingún cambio se aplica al archivo original hasta que el usuario lo autorice explícitamente.")
    return "\n".join(r), bool(lost)


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:
        pass
    ap = argparse.ArgumentParser()
    ap.add_argument("--original", required=True)
    ap.add_argument("--proposed", required=True, help="Versión propuesta (en scratch/, no en el repo).")
    ap.add_argument("--reason", default="Optimización arquitectónica del prompt")
    a = ap.parse_args()
    with open(a.original, encoding="utf-8-sig") as f:
        orig = f.read().replace("\r\n", "\n")
    with open(a.proposed, encoding="utf-8-sig") as f:
        prop = f.read().replace("\r\n", "\n")
    report, has_loss = build_report(a.original, orig, prop, a.reason)
    print(report)
    sys.exit(2 if has_loss else 0)


if __name__ == "__main__":
    main()
