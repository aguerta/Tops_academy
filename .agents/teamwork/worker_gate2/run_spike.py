import sys
from pathlib import Path
import time
import json
import traceback

sys.path.insert(0, str(Path(".agents/skills/content-to-course").resolve()))

from partition_corpus import partition_corpus

corpus_pdf = Path("content/Solow_model/solow1956.pdf")
work_dir = Path("work")

print(f"[*] Starting Partitioning of {corpus_pdf} into {work_dir}...")
t0 = time.perf_counter()
try:
    parts = partition_corpus(corpus_pdf, work_dir, course_id="solow_model")
    elapsed = time.perf_counter() - t0
    print(f"[+] Partitioning complete in {elapsed:.3f} s. Parts created: {len(parts)}")
    for p in parts:
        print(f"    - Part {p['part_id']}: slice {p['slice_pdf']}, pages {p.get('core_page_range_global')} (local {p.get('valid_page_range')}), weight {p.get('weight', 0):,.0f}")
except Exception as e:
    print(f"[-] Error: {e}")
    traceback.print_exc()
