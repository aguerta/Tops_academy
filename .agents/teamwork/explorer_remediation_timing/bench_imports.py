import time
import subprocess
import sys
import statistics
import os

def bench(name, cmd, trials=5):
    timings = []
    for i in range(trials):
        t0 = time.perf_counter()
        r = subprocess.run([sys.executable, "-c", cmd], capture_output=True, text=True)
        if r.returncode != 0:
            print(f"Error in {name}: {r.stderr}")
            return
        dt = (time.perf_counter() - t0) * 1000
        timings.append(dt)
    print(f"{name:45s} | min: {min(timings):6.1f}ms | median: {statistics.median(timings):6.1f}ms | max: {max(timings):6.1f}ms")

if __name__ == "__main__":
    print(f"Python version: {sys.version.split()[0]}")
    print(f"Platform: {sys.platform}")
    print("=" * 80)
    bench("python null process spawn", "pass")
    bench("import stdlib (math, fractions, stat, rand)", "import math, fractions, statistics, random")
    bench("import numpy", "import numpy")
    bench("import sympy", "import sympy")
    bench("import scipy", "import scipy")
    bench("import scipy.stats", "import scipy.stats")
    
    skill_path = os.path.abspath(".agents/skills/content-to-course").replace("\\", "/")
    bench("import engine.render", f"import sys; sys.path.insert(0, '{skill_path}'); from engine.render import bmatrix")
    
    bench("Stdlib + render (no np/sp/scipy)", f"import sys; sys.path.insert(0, '{skill_path}'); import math, fractions, statistics, random; from engine.render import bmatrix, table_array, fmt, latex_frac")
    bench("Stdlib + render + numpy", f"import sys; sys.path.insert(0, '{skill_path}'); import math, fractions, statistics, random, numpy as np; from engine.render import bmatrix, table_array, fmt, latex_frac")
    bench("Stdlib + render + numpy + sympy", f"import sys; sys.path.insert(0, '{skill_path}'); import math, fractions, statistics, random, sympy, numpy as np; from engine.render import bmatrix, table_array, fmt, latex_frac")
    bench("FULL build_sandbox_globals (all libs)", f"import sys; sys.path.insert(0, '{skill_path}'); import math, fractions, statistics, sympy, numpy as np, scipy, scipy.stats, random; from engine.render import bmatrix, table_array, fmt, latex_frac")
