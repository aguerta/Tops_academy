import sys
from pathlib import Path

# Add content-to-course to sys.path
c2c_path = Path(__file__).resolve().parent.parent.parent.parent / "content-to-course"
if not c2c_path.is_dir():
    c2c_path = Path(r"d:\Augusto\personal_portfolio\Tops_academy\.agents\skills\content-to-course")
sys.path.insert(0, str(c2c_path))

from engine.invariants import check_unrendered_placeholders
from check_templates import check_unrendered_placeholders_in_instance

vars = {"n": 100, "d": 4, "a": 2, "b": 5}
latex_text = r"Calcule $\frac{a}{b}$ cuando $X_n \xrightarrow{d} X$ con $x_{n}$ y ${k}^*$"
errs = check_unrendered_placeholders(latex_text, "stem", variables=vars)
print("LaTeX errs (should be empty):", errs)
assert len(errs) == 0, f"Expected 0 errors, got: {errs}"

# Leaked test
leaked_text = r"El error es tol <= {delta} y @delta@"
leaked_errs = check_unrendered_placeholders(leaked_text, "stem", variables=vars)
print("Leaked errs (should be 2):", leaked_errs)
assert len(leaked_errs) == 2, f"Expected 2 errors, got: {leaked_errs}"

# Leaked single letter in vars without LaTeX:
leaked_var = r"El resultado para {n} es incorrecto"
errs_var = check_unrendered_placeholders(leaked_var, "stem", variables=vars)
print("Leaked var errs (should be 1):", errs_var)
assert len(errs_var) == 1, f"Expected 1 error, got: {errs_var}"

print("ALL CHECK_LEAK TESTS PASSED!")
