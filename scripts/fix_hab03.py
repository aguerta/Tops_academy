import json

path = 'work/templates/Hab-03.json'
with open(path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# T-Hab03-01
t1 = data['templates'][0]
t1['generate_py'] = """def generate(rng):
    alpha_choices = [(1, 3), (2, 3), (1, 4), (3, 4), (2, 5), (3, 5), (1, 5), (4, 5)]
    num, den = rng.choice(alpha_choices)
    alpha_frac = latex_frac(num, den)
    one_minus_alpha_frac = latex_frac(den - num, den)
    one_minus_alpha = (den - num) / den
    alpha_val = num / den
    s_val = rng.choice([0.15, 0.20, 0.25, 0.30, 0.35, 0.40])
    lambda_val = rng.choice([0.02, 0.03, 0.04, 0.05, 0.06, 0.08, 0.10])
    a_num = round(one_minus_alpha * lambda_val, 5)
    b_num = round(one_minus_alpha * s_val, 5)
    a_str = fmt(a_num, 4)
    b_str = fmt(b_num, 4)
    s_str = fmt(s_val, 4)
    lam_str = fmt(lambda_val, 4)
    correct_val = f'La ecuación lineal es $\\\\dot{{z}} + {a_str} z = {b_str}$.'
    d1 = f'La ecuación lineal es $\\\\dot{{z}} + {lam_str} z = {s_str}$.'
    d2 = f'La ecuación lineal es $\\\\dot{{z}} + {a_str} z = {s_str}$.'
    d3 = f'La ecuación lineal es $\\\\dot{{z}} + {fmt(round(alpha_val * lambda_val, 5), 4)} z = {b_str}$.'
    d4 = f'La ecuación lineal es $\\\\dot{{z}} + {b_str} z = {a_str}$.'
    d5 = f'La ecuación lineal es $\\\\dot{{z}} + {lam_str} z = {b_str}$.'
    d6 = f'La ecuación lineal es $\\\\dot{{z}} - {a_str} z = {b_str}$.'
    return {
        'vars': {'alpha_frac': alpha_frac, 'one_minus_alpha_frac': one_minus_alpha_frac, 's_val': s_str, 'lambda_val': lam_str, 'a_str': a_str, 'b_str': b_str},
        'correct': correct_val,
        'distractors': [
            {'value': d1, 'distractor_id': 'D-Hab03-01'},
            {'value': d2, 'distractor_id': 'D-Hab03-02'},
            {'value': d3, 'distractor_id': 'D-Hab03-03'},
            {'value': d4, 'distractor_id': 'D-Hab03-04'},
            {'value': d5, 'distractor_id': 'D-Hab03-05'},
            {'value': d6, 'distractor_id': 'D-Hab03-06'}
        ]
    }"""

# T-Hab03-02
t2 = data['templates'][1]
t2['generate_py'] = """def generate(rng):
    alpha_choices = [(1, 3), (2, 3), (1, 4), (3, 4), (2, 5), (3, 5), (1, 5), (4, 5)]
    num, den = rng.choice(alpha_choices)
    alpha_frac = latex_frac(num, den)
    one_minus_alpha_frac = latex_frac(den - num, den)
    one_minus_alpha = (den - num) / den
    alpha_val = num / den
    s_val = rng.choice([0.15, 0.20, 0.25, 0.30, 0.35, 0.40])
    lambda_val = rng.choice([0.02, 0.03, 0.04, 0.05, 0.06, 0.08, 0.10])
    a_num = round(one_minus_alpha * lambda_val, 5)
    b_num = round(one_minus_alpha * s_val, 5)
    a_str = fmt(a_num, 4)
    b_str = fmt(b_num, 4)
    s_str = fmt(s_val, 4)
    lam_str = fmt(lambda_val, 4)
    correct_val = f'Se define $z = k^{{{one_minus_alpha_frac}}}$, obteniéndose $\\\\dot{{z}} + {a_str} z = {b_str}$.'
    d1 = f'Se define $z = k^{{{one_minus_alpha_frac}}}$, obteniéndose $\\\\dot{{z}} + {lam_str} z = {s_str}$.'
    d2 = f'Se define $z = k^{{{one_minus_alpha_frac}}}$, obteniéndose $\\\\dot{{z}} + {a_str} z = {s_str}$.'
    d3 = f'Se define $z = k^{{{alpha_frac}}}$, obteniéndose $\\\\dot{{z}} + {a_str} z = {b_str}$.'
    d4 = f'Se define $z = k^{{{one_minus_alpha_frac}}}$, obteniéndose $\\\\dot{{z}} + {b_str} z = {a_str}$.'
    d5 = f'Se define $z = k^{{{one_minus_alpha_frac}}}$, obteniéndose $\\\\dot{{z}} + {lam_str} z = {b_str}$.'
    d6 = f'Se define $z = k^{{{one_minus_alpha_frac}}}$, obteniéndose $\\\\dot{{z}} - {a_str} z = {b_str}$.'
    return {
        'vars': {'alpha_frac': alpha_frac, 'one_minus_alpha_frac': one_minus_alpha_frac, 's_val': s_str, 'lambda_val': lam_str, 'a_str': a_str, 'b_str': b_str},
        'correct': correct_val,
        'distractors': [
            {'value': d1, 'distractor_id': 'D-Hab03-01'},
            {'value': d2, 'distractor_id': 'D-Hab03-02'},
            {'value': d3, 'distractor_id': 'D-Hab03-03'},
            {'value': d4, 'distractor_id': 'D-Hab03-04'},
            {'value': d5, 'distractor_id': 'D-Hab03-05'},
            {'value': d6, 'distractor_id': 'D-Hab03-06'}
        ]
    }"""

# T-Hab03-05
t5 = data['templates'][4]
t5_code = t5['generate_py']
t5_code = t5_code.replace(", omitiendo el factor (1-\\alpha)", "")
t5_code = t5_code.replace(", utilizando el exponente directo de la función de producción", "")
t5_code = t5_code.replace(", invirtiendo el signo de dilución", "")
t5['generate_py'] = t5_code

# T-Hab03-06
t6 = data['templates'][5]
t6_code = t6['generate_py']
t6_code = t6_code.replace(", prescindiendo de multiplicar por (1-\\alpha)", "")
t6_code = t6_code.replace(", alterando la no linealidad del modelo", "")
t6_code = t6_code.replace(", omitiendo el factor (1-\\alpha)", "")
t6['generate_py'] = t6_code

with open(path, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print('Successfully cleaned Hab-03.json without 1/2 collision')
