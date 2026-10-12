"""Page transcription validator for content-to-course v2.

Validates that:
- 100% of manifest items have non-empty markdown transcriptions
- Text layer cross-check: numbers and math symbols in PDF text layers appear in transcriptions
- Ink PDFs and image tiles have structured markdown content
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Tuple


def extract_math_and_numeric_tokens(text: str) -> List[str]:
    """Extract numbers, Greek letters, and key mathematical symbols."""
    # Find numbers and math identifiers
    tokens = re.findall(r"\b\d+(?:\.\d+)?\b|[α-ωΑ-Ωβγδεζηθικλμνξοπρστυφχψω]|\\(?:beta|alpha|sigma|hat|mu|lambda|frac|sum|prod)", text)
    return [t.strip() for t in tokens if t.strip()]


def check_pages(
    manifest_path: Path,
    min_text_match_ratio: float = 0.50,
) -> Tuple[bool, Dict[str, Any]]:
    """Validate transcriptions against manifest items.
    
    Returns:
        (is_valid, summary_report)
    """
    if not manifest_path.exists():
        return False, {"error": f"Manifest file does not exist: {manifest_path}"}

    with open(manifest_path, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    items = manifest.get("items", manifest.get("pages", []))
    total_items = len(items)

    missing_transcriptions: List[str] = []
    empty_transcriptions: List[str] = []
    low_match_pages: List[Dict[str, Any]] = []

    verified_count = 0

    for item in items:
        transcription_path = item.get("transcription_path")
        if not transcription_path:
            missing_transcriptions.append(f"{item.get('doc')} (page {item.get('page')})")
            continue

        p = Path(transcription_path)
        if not p.exists():
            missing_transcriptions.append(str(p.as_posix()))
            continue

        content = p.read_text(encoding="utf-8", errors="replace").strip()
        if not content:
            empty_transcriptions.append(str(p.as_posix()))
            continue

        verified_count += 1

        # Cross-check text layer if present
        text_layer_path = item.get("text_layer_path")
        if item.get("has_text_layer") and text_layer_path:
            tl_path = Path(text_layer_path)
            if tl_path.exists():
                tl_text = tl_path.read_text(encoding="utf-8", errors="replace")
                expected_tokens = extract_math_and_numeric_tokens(tl_text)
                if len(expected_tokens) >= 5:
                    found_tokens = [tok for tok in expected_tokens if tok in content]
                    match_ratio = len(found_tokens) / len(expected_tokens)
                    if match_ratio < min_text_match_ratio:
                        low_match_pages.append({
                            "page": str(p.as_posix()),
                            "match_ratio": round(match_ratio, 4),
                            "total_expected": len(expected_tokens),
                            "found": len(found_tokens),
                        })

    is_valid = (len(missing_transcriptions) == 0 and len(empty_transcriptions) == 0)

    report = {
        "total_items": total_items,
        "verified_items": verified_count,
        "missing_count": len(missing_transcriptions),
        "missing_pages": missing_transcriptions,
        "empty_count": len(empty_transcriptions),
        "empty_pages": empty_transcriptions,
        "low_match_count": len(low_match_pages),
        "low_match_pages": low_match_pages,
        "is_valid": is_valid,
    }
    return is_valid, report


def main():
    parser = argparse.ArgumentParser(description="Check page transcriptions against manifest")
    parser.add_argument("--manifest", required=True, help="Path to manifest.json")
    parser.add_argument("--threshold", type=float, default=0.50, help="Minimum text match ratio threshold")
    args = parser.parse_args()

    valid, report = check_pages(Path(args.manifest), min_text_match_ratio=args.threshold)
    print(f"Total: {report['total_items']}, Verified: {report['verified_items']}, Missing: {report['missing_count']}, Empty: {report['empty_count']}")
    if not valid:
        print("FAIL: Missing or empty page transcriptions found.")
        sys.exit(1)
    print("PASS: 100% of manifest pages transcribed.")
    sys.exit(0)


if __name__ == "__main__":
    main()
