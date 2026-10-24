import tempfile
from pathlib import Path
import json
import sys

_proj_root = Path(r"d:\Augusto\personal_portfolio\Tops_academy")
sys.path.insert(0, str(_proj_root))
_skill_root = Path(r"d:\Augusto\personal_portfolio\Tops_academy\.agents\skills\content-to-course")
sys.path.insert(0, str(_skill_root))

from compile_shard import compile_shard
from tests.test_shard_compiler_hardening import _setup_test_workspace

with tempfile.TemporaryDirectory() as td:
    tmp_path = Path(td)
    work_dir, shards_dir = _setup_test_workspace(tmp_path, 'shard_06', ['Hab-03', 'Hab-04'])
    fixes_dir = shards_dir / 'shard_fixes'
    fixes_dir.mkdir(parents=True, exist_ok=True)
    fix_code_template = (
        'import random\n'
        'def gen(rng):\n'
        '    v = rng.randint(1, 100)\n'
        '    return {"vars": {"v": v}, "correct": str(v), "distractors": []}\n'
        'def ver(r): return True\n'
        'TEMPLATES = [\n'
        '    ("CID_TOKEN", "fill_in_the_blank", "Stem CID_TOKEN {v}", gen, ver, "Sol", "KC", [], ("doc.pdf", 1, ""))\n'
        ']\n'
    )
    (fixes_dir / 'Hab-03.py').write_text(fix_code_template.replace('CID_TOKEN', 'Hab-03'), encoding='utf-8')
    (fixes_dir / 'Hab-04.py').write_text(fix_code_template.replace('CID_TOKEN', 'Hab-04'), encoding='utf-8')
    success, errors = compile_shard(work_dir, shard_id='shard_06', strict=False)
    print('Success:', success)
    print('Errors:', errors)
    for f in (work_dir / 'templates').glob('*.json'):
        print('FILE:', f.name)
        print(f.read_text(encoding='utf-8'))
