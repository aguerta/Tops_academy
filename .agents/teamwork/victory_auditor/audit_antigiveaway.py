import sys
sys.path.insert(0, '.')

import json
from src.validator.psychometric_checker import check_psychometrics

for path in ['courses/pde_course.json', 'courses/demo_course.json']:
    with open(path, encoding='utf-8') as f:
        data = json.load(f)
    print("="*60)
    print(f"Auditing Psychometrics for: {path}")
    errs = check_psychometrics(data)
    print(f"Psychometric errors found: {len(errs)}")
    for e in errs:
        print(f"  {e.rule_id} [{e.code}]: {e.message}")
    assert len(errs) == 0, f"Failed with {len(errs)} psychometric errors"
    print("PSYCHOMETRIC CHECK PASSED 100%!")
