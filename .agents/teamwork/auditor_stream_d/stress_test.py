"""Adversarial stress-testing script for Stream D (R7/P7/P8)."""
import sys
from pathlib import Path

skill_dir = Path(__file__).resolve().parent.parent.parent / "skills" / "content-to-course"
if str(skill_dir) not in sys.path:
    sys.path.insert(0, str(skill_dir))

from prepare import sanitize_cli_arg, sanitize_path, compute_next_ids, is_corrupted_unicode
from course_publisher import CoursePublisher

# 1. Edge cases in compute_next_ids
comps = [
    {"id": "C-01"}, {"id": "C-02"}, {"id": "C-99"},
    {"id": "Hab-1"}, {"id": "Hab-2"},
    {"id": "H-001"}, {"id": "H-002"},
    {"id": "CUSTOM_10"},
    {"id": "MALFORMED_NO_NUM"},
    None,
    {"id": ""},
    {},
]
res = compute_next_ids(comps)
assert res["next_ids_by_prefix"]["C-"] == "C-100", f"Expected C-100, got {res['next_ids_by_prefix']['C-']}"
assert res["next_ids_by_prefix"]["Hab-"] == "Hab-03", f"Expected Hab-03, got {res['next_ids_by_prefix']['Hab-']}"
assert res["next_ids_by_prefix"]["H-"] == "H-003", f"Expected H-003, got {res['next_ids_by_prefix']['H-']}"
assert res["next_ids_by_prefix"]["CUSTOM_"] == "CUSTOM_11", f"Expected CUSTOM_11, got {res['next_ids_by_prefix']['CUSTOM_']}"
assert res["next_competency_index"] == len(comps) + 1

# Empty competencies
res_empty = compute_next_ids([])
assert res_empty["next_ids_by_prefix"]["C-"] == "C-01"
assert res_empty["next_ids_by_prefix"]["Hab-"] == "Hab-01"
assert res_empty["next_ids_by_prefix"]["H-"] == "H-01"
assert res_empty["next_competency_index"] == 1

# 2. Unicode corruption detection
assert is_corrupted_unicode("Estad\ufffdstica") is True
assert is_corrupted_unicode("Estad\uFFFDstica") is True
assert is_corrupted_unicode("Estadística: Regresión") is False
assert is_corrupted_unicode(None) is False
assert is_corrupted_unicode("") is False
assert is_corrupted_unicode("Plain ascii") is False

# 3. Path & CLI quoting sanitization
test_cases = [
    ('"""nested"""', "nested"),
    ("'''single'''", "single"),
    ('  "  spaced  "  ', "spaced"),
    (r'\"D:\Augusto\course\"', r"D:\Augusto\course"),
    (r'\"\"D:\Augusto\course\"\"', r"D:\Augusto\course"),
    ("C:\\", "C:\\"),
    ("D:\\", "D:\\"),
    ("C:\\Folder\\Subfolder\\", "C:\\Folder\\Subfolder"),
    (None, None),
    (12345, 12345),
    ('""', ""),
    ('"', ""),
]
for raw, expected in test_cases:
    cleaned = sanitize_cli_arg(raw)
    assert cleaned == expected, f"Failed for {raw!r}: expected {expected!r}, got {cleaned!r}"

# 4. prepare_course with corrupted existing JSON
from prepare import prepare_course
import json
import tempfile
import shutil

with tempfile.TemporaryDirectory() as td:
    tpath = Path(td)
    cpath = tpath / "courses"
    cpath.mkdir()
    wpath = tpath / "courses" / "corrupted_course" / "work_append"
    
    # Write invalid JSON
    (cpath / "corrupted_course.json").write_text("{invalid json", encoding="utf-8")
    
    # Dummy pdf
    import fitz
    doc = fitz.open()
    page = doc.new_page()
    page.insert_text((50, 50), "Test content")
    pdf_p = tpath / "test.pdf"
    doc.save(str(pdf_p))
    doc.close()
    
    # Should not crash, should log warning and continue
    manifest = prepare_course(
        input_path=pdf_p,
        work_dir=wpath,
        course_id="corrupted_course",
        courses_dir=cpath,
        append=True,
    )
    assert manifest is not None
    assert (wpath / "pre_cta_manifest.json").is_file()

print("All adversarial stress tests passed successfully!")

