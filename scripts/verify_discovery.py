#!/usr/bin/env python3
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import run_platform

courses = run_platform.scan_courses()
print("Discovered courses:")
for c in courses:
    print(f" - {c['id']}: {c['title']} (status={c['status']}, competencies={c['total_competencies']}, questions={c['total_questions']})")
