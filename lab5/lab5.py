import re
import itertools

vars = ['Q2', 'Q1', 'Q0']
states = [
    (0,0,0, 1,1,1, 1,1,1),
    (0,0,1, 0,0,0, 0,0,1),
    (0,1,0, 0,0,1, 0,1,1),
    (0,1,1, 0,1,0, 0,0,1),
    (1,0,0, 0,1,1, 1,1,1),
    (1,0,1, 1,0,0, 0,0,1),
    (1,1,0, 1,0,1, 0,1,1),
    (1,1,1, 1,1,0, 0,0,1),
]

def to_bin(n, width):
    return format(n, f'0{width}b')

def count_bits(s, ch):
    return len(re.findall(ch, s))

def combine_terms(a, b):
    diff = 0
    out = []
    for ca, cb in zip(a, b):
        if ca == cb:
            out.append(ca)
        else:
            diff += 1
            out.append('-')
            if diff > 1:
                return None
    return ''.join(out)

def find_prime_implicants(minterms, num_vars):
    groups = {}
    for m in minterms:
        b = to_bin(m, num_vars)
        cnt = count_bits(b, '1')
        groups.setdefault(cnt, set()).add(b)
    primes = set()
    while groups:
        new_groups = {}
        used = set()
        for i in sorted(groups):
            if i+1 not in groups:
                continue
            for a, b in itertools.product(groups[i], groups[i+1]):
                c = combine_terms(a, b)
                if c:
                    used.add(a)
                    used.add(b)
                    k = count_bits(c, '1')
                    new_groups.setdefault(k, set()).add(c)
        for grp in groups.values():
            for term in grp:
                if term not in used:
                    primes.add(term)
        groups = new_groups
    return primes

def covers(imp, m, num_vars):
    b = to_bin(m, num_vars)
    return all(ic=='-' or ic==bc for ic, bc in zip(imp, b))

def select_essential(primes, minterms):
    chart = {imp: {m for m in minterms if covers(imp, m, num_vars)}
             for imp in primes}
    inv = {}
    for imp, cov in chart.items():
        for m in cov:
            inv.setdefault(m, []).append(imp)
    solution = set()
    covered = set()
    for m, imps in inv.items():
        if len(imps) == 1:
            solution.add(imps[0])
            covered |= chart[imps[0]]
    remaining = set(minterms) - covered
    while remaining:
        best = max(chart, key=lambda imp: len(chart[imp] & remaining))
        solution.add(best)
        covered |= chart[best]
        remaining = set(minterms) - covered
    return solution

def implicant_to_term(imp):
    lits = []
    for bit, name in zip(imp, vars):
        if bit == '1':
            lits.append(name)
        elif bit == '0':
            lits.append(f"!{name}")
    return " ∧ ".join(lits) if lits else "1"

def minimize_dnf(minterms, num_vars):
    if not minterms:
        return "0"
    primes = find_prime_implicants(minterms, num_vars)
    essentials = select_essential(primes, minterms)
    terms = [implicant_to_term(imp) for imp in sorted(essentials)]
    return " ∨ ".join(terms)

num_vars = 3
minterms_T2 = []
minterms_T1 = []
minterms_T0 = []
for q2, q1, q0, q2n, q1n, q0n, t2, t1, t0 in states:
    idx = (q2 << 2) | (q1 << 1) | q0
    if t2:
        minterms_T2.append(idx)
    if t1:
        minterms_T1.append(idx)
    if t0:
        minterms_T0.append(idx)

print(f"{'Q2':>2} {'Q1':>2} {'Q0':>2} {'Q2+':>3} {'Q1+':>3} {'Q0+':>3} {'T2':>2} {'T1':>2} {'T0':>2}")
print('-' * 23)
for q2, q1, q0, q2n, q1n, q0n, t2, t1, t0 in states:
    print(f"{q2:>2} {q1:>2} {q0:>2} {q2n:>3} {q1n:>3} {q0n:>3} {t2:>2} {t1:>2} {t0:>2}")

dnf_T2 = minimize_dnf(minterms_T2, num_vars)
dnf_T1 = minimize_dnf(minterms_T1, num_vars)
dnf_T0 = minimize_dnf(minterms_T0, num_vars)

print("\nМинимизированные функции возбуждения (СДНФ, базис НЕ-И-ИЛИ):")
print(f"T2 = {dnf_T2}")
print(f"T1 = {dnf_T1}")
print(f"T0 = {dnf_T0}")