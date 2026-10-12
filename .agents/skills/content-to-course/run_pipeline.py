"""Pipeline execution alias pointing to run.py."""
import sys
from pathlib import Path

skill_dir = Path(__file__).parent.resolve()
if str(skill_dir) not in sys.path:
    sys.path.insert(0, str(skill_dir))

from run import main, run_pipeline

if __name__ == "__main__":
    main()
