"""
Probe mathematical equivalence verification with SymPy.
"""
try:
    import sympy
    from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application
    print("SymPy version:", sympy.__version__)
    
    transformations = (standard_transformations + (implicit_multiplication_application,))
    
    # Test numeric
    e1 = parse_expr("0.5", transformations=transformations)
    e2 = parse_expr("1/2", transformations=transformations)
    print("0.5 == 1/2:", sympy.simplify(e1 - e2) == 0)
    
    # Test algebraic:
    # 1 - (alpha + n)*sigma vs 1 - alpha*sigma - n*sigma
    expr_a = parse_expr("1 - (alpha + n)*sigma", transformations=transformations)
    expr_b = parse_expr("1 - alpha*sigma - n*sigma", transformations=transformations)
    print("1 - (alpha + n)*sigma == 1 - alpha*sigma - n*sigma:", sympy.simplify(expr_a - expr_b) == 0)
    
except Exception as e:
    print("Error:", e)
