from itertools import product
import re

def replace_operators(expr):
    expr = re.sub(r'([a-zA-Z0-1()]+)\s*→\s*([a-zA-Z0-1()]+)', r'(not \1) or \2', expr)
    expr = re.sub(r'([a-zA-Z0-1()]+)\s*⇒\s*([a-zA-Z0-1()]+)', r'(not \1) or \2', expr)
    expr = re.sub(r'([a-zA-Z0-1()]+)\s*↔\s*([a-zA-Z0-1()]+)', r'(\1 == \2)', expr)
    expr = re.sub(r'([a-zA-Z0-1()]+)\s*⇔\s*([a-zA-Z0-1()]+)', r'(\1 == \2)', expr)
    
    expr = (expr.replace('!', ' not ')
            .replace('¬', ' not ')
            .replace('∧', ' and ')
            .replace('&', ' and ')
            .replace('∨', ' or ')
            .replace('|', ' or '))
    
    return expr

def generate_truth_table_and_forms(expr):
    normalized_expr = expr.replace(' ', '').replace('!', '¬').replace('&', '∧').replace('|', '∨')
    vars_ = sorted(list(set(re.findall(r'\b[a-z]\b', normalized_expr))))
    n_vars = len(vars_)

    truth_table = []
    for values in product([0, 1], repeat=n_vars):
        var_values = dict(zip(vars_, values))
        current_expr = normalized_expr

        for var in vars_:
            current_expr = current_expr.replace(var, str(var_values[var]))

        current_expr = replace_operators(current_expr)
        current_expr = ' '.join(current_expr.split())

        try:
            result = eval(current_expr)
            truth_table.append((values, int(bool(result))))
        except Exception as e:
            print(f"Ошибка при вычислении выражения: {e}")
            print(f"Выражение после замен: {current_expr}")
            return None

    minterms = [term for term, res in truth_table if res == 1]
    maxterms = [term for term, res in truth_table if res == 0]

    return {
        'minterms': minterms,
        'maxterms': maxterms,
        'n_vars': n_vars,
        'vars_sorted': vars_
    }

def term_to_str(term, variables, is_dnf=True):
    parts = []
    for val, var in zip(term, variables):
        if val == 'X':
            continue
        if is_dnf:
            parts.append(f"¬{var}" if val == 0 else var)
        else:
            parts.append(var if val == 0 else f"¬{var}")
    return "".join(parts) if is_dnf else f"({'∨'.join(parts)})" if parts else ""

def minimize_calc_dnf(terms, n_vars, vars_):
    return calculate_method(terms, vars_, is_dnf=True)

def minimize_calc_cnf(terms, n_vars, vars_):
    return calculate_method(terms, vars_, is_dnf=False)

def calculate_method(terms, variables, is_dnf=True):
    if not terms:
        return []

    print("\nИтерации склеивания:")
    current_terms = terms.copy()

    while True:
        new_terms = []
        used = set()

        print("\nТекущие термы:")
        for term in current_terms:
            print(term_to_str(term, variables, is_dnf), end=" ")
        print()

        for i in range(len(current_terms)):
            for j in range(i + 1, len(current_terms)):
                term1 = current_terms[i]
                term2 = current_terms[j]
                diff_pos = -1
                diff_count = 0

                for k in range(len(variables)):
                    if term1[k] != term2[k]:
                        diff_pos = k
                        diff_count += 1

                if diff_count == 1:
                    new_term = list(term1)
                    new_term[diff_pos] = 'X'
                    new_term = tuple(new_term)

                    if new_term not in new_terms:
                        new_terms.append(new_term)
                        used.add(i)
                        used.add(j)
                        print(
                            f"Склеиваем: {term_to_str(term1, variables, is_dnf)} и {term_to_str(term2, variables, is_dnf)} -> {term_to_str(new_term, variables, is_dnf)}")

        for i in range(len(current_terms)):
            if i not in used and current_terms[i] not in new_terms:
                new_terms.append(current_terms[i])

        if not new_terms or new_terms == current_terms:
            break

        current_terms = new_terms

    essential_terms = []
    uncovered = set(terms)

    while uncovered:
        best_term = None
        best_coverage = set()
        max_coverage = 0
        max_specificity = -1

        for term in current_terms:
            covered = set()
            for original_term in uncovered:
                if all(p == 'X' or t == p for t, p in zip(original_term, term)):
                    covered.add(original_term)
            specificity = sum(1 for v in term if v != 'X')
            if len(covered) > max_coverage or (len(covered) == max_coverage and specificity > max_specificity):
                max_coverage = len(covered)
                max_specificity = specificity
                best_term = term
                best_coverage = covered

        if best_term:
            essential_terms.append(best_term)
            uncovered -= best_coverage
        else:
            break

    print("\nМинимизированная форма:")
    if essential_terms:
        separator = " ∨ " if is_dnf else " ∧ "
        print(separator.join(term_to_str(t, variables, is_dnf) for t in essential_terms))
    else:
        print("0" if is_dnf else "1")

    return [term_to_str(t, variables, is_dnf) for t in essential_terms]

def minimize_tab_dnf(terms, n_vars, vars_):
    return table_method(terms, vars_, is_dnf=True)

def minimize_tab_cnf(terms, n_vars, vars_):
    return table_method(terms, vars_, is_dnf=False)

def table_method(terms, variables, is_dnf=True):
    minimized_terms = calculate_method(terms, variables, is_dnf)
    if not minimized_terms or not terms:
        return []

    print("\nТаблица покрытия:")
    imp_width = max(len(t) for t in minimized_terms) + 2
    term_width = max(len(term_to_str(t, variables, is_dnf)) for t in terms) + 2

    header = " " * imp_width
    for term in terms:
        header += f" {term_to_str(term, variables, is_dnf):^{term_width}}"
    print(header)

    for imp in minimized_terms:
        row = f" {imp:<{imp_width - 1}}"
        for term in terms:
            match = False
            for t in calculate_method([term], variables, is_dnf):
                if t == imp:
                    match = True
                    break
            row += f" {'X' if match else ' ':^{term_width}}"
        print(row)

    print("\nМинимизированная форма:")
    separator = " ∨ " if is_dnf else " ∧ "
    print(separator.join(minimized_terms))

    return minimized_terms

def gray_to_binary(gray, bits):
    binary = gray & (1 << (bits - 1))
    for i in range(bits - 2, -1, -1):
        binary |= ((gray >> i) & 1) ^ ((binary >> (i + 1)) & 1) << i
    return binary

def get_gray_code(n, bits):
    gray = n ^ (n >> 1)
    return [(gray >> i) & 1 for i in range(bits - 1, -1, -1)]

def find_max_rectangle(k_map, start_row, start_col, covered):
    max_area = 0
    best_rect = None
    
    for rows in range(1, len(k_map) - start_row + 1):
        for cols in range(1, len(k_map[0]) - start_col + 1):
            if is_valid_rectangle(k_map, start_row, start_col, rows, cols, covered):
                area = rows * cols
                if area > max_area:
                    max_area = area
                    best_rect = (start_row, start_col, rows, cols)
    
    return best_rect

def is_valid_rectangle(k_map, row, col, rows, cols, covered):
    for r in range(row, row + rows):
        for c in range(col, col + cols):
            if k_map[r][c] != 1 or covered[r][c]:
                return False
    return True

def get_term_from_rectangle(rect, variables, row_vars, col_vars):
    row, col, rows, cols = rect
    term = ['X'] * len(variables)
    
    row_bits = [get_gray_code(r, len(row_vars)) for r in range(row, row + rows)]
    for i, var in enumerate(row_vars):
        values = set(bits[i] for bits in row_bits)
        if len(values) == 1:
            term[variables.index(var)] = values.pop()

    col_bits = [get_gray_code(c, len(col_vars)) for c in range(col, col + cols)]
    for i, var in enumerate(col_vars):
        values = set(bits[i] for bits in col_bits)
        if len(values) == 1:
            term[variables.index(var)] = values.pop()

    return tuple(term)

def get_term_from_coords(row, col, variables, row_vars, col_vars):
    term = ['X'] * len(variables)
    
    row_bits = get_gray_code(row, len(row_vars))
    for i, var in enumerate(row_vars):
        term[variables.index(var)] = row_bits[i]
    
    col_bits = get_gray_code(col, len(col_vars))
    for i, var in enumerate(col_vars):
        term[variables.index(var)] = col_bits[i]
    
    return tuple(term)

def print_kmap_table(terms, n_vars, vars_, is_dnf=True):
    if not terms:
        print("0 (ложь)" if is_dnf else "1 (истина)")
        return

    if n_vars == 2:
        rows, cols = 2, 2
        row_vars = [vars_[0]]
        col_vars = [vars_[1]]
    elif n_vars == 3:
        rows, cols = 2, 4
        row_vars = [vars_[0]]
        col_vars = vars_[1:]
    else:
        rows, cols = 4, 4
        row_vars = vars_[:2]
        col_vars = vars_[2:]

    k_map = [[0 for _ in range(cols)] for _ in range(rows)]

    for term in terms:
        row = 0
        for var in row_vars:
            row = (row << 1) | term[vars_.index(var)]
        col = 0
        for var in col_vars:
            col = (col << 1) | term[vars_.index(var)]
        if n_vars >= 3:
            col = gray_to_binary(col, len(col_vars))
        k_map[row][col] = 1

    col_width = 3
    header = " " * len(row_vars)
    for col in range(len(k_map[0])):
        col_bits = get_gray_code(col, len(col_vars))
        header += f"  {''.join(str(b) for b in col_bits):^{col_width}}"
    print(header)

    for row in range(len(k_map)):
        row_bits = get_gray_code(row, len(row_vars))
        row_str = "".join(str(b) for b in row_bits)
        row_str = row_str.ljust(len(row_vars))
        for col in range(len(k_map[0])):
            row_str += f"  {k_map[row][col]:^{col_width}}"
        print(row_str)

def minimize_karnaugh(k_map, variables, row_vars, col_vars):
    minimized_terms = []
    covered = [[False for _ in row] for row in k_map]
    ones = [(r, c) for r in range(len(k_map)) for c in range(len(k_map[0])) if k_map[r][c] == 1]

    while ones:
        best_term = None
        best_coverage = []
        max_coverage = 0

        for row in range(len(k_map)):
            for col in range(len(k_map[0])):
                if k_map[row][col] == 1 and not covered[row][col]:
                    rect = find_max_rectangle(k_map, row, col, covered)
                    if rect and rect[2] * rect[3] >= 2:
                        term = get_term_from_rectangle(rect, variables, row_vars, col_vars)
                        coverage = [(r, c) for r in range(rect[0], rect[0] + rect[2]) 
                                    for c in range(rect[1], rect[1] + rect[3]) 
                                    if k_map[r][c] == 1 and not covered[r][c]]
                        if len(coverage) > max_coverage:
                            max_coverage = len(coverage)
                            best_term = term
                            best_coverage = coverage

        if best_term:
            minimized_terms.append(best_term)
            for r, c in best_coverage:
                covered[r][c] = True
                if (r, c) in ones:
                    ones.remove((r, c))
        else:
            break

    return minimized_terms

def kmap_minimize(terms, n_vars, vars_, is_dnf=True):
    if n_vars > 4:
        print("Карты Карно для более чем 4 переменных не поддерживаются")
        return []
    elif n_vars < 2:
        print("Карты Карно требуют как минимум 2 переменных")
        return []
    elif not terms:
        print("0 (ложь)" if is_dnf else "1 (истина)")
        return []

    if n_vars == 2:
        rows, cols = 2, 2
        row_vars = [vars_[0]]
        col_vars = [vars_[1]]
    elif n_vars == 3:
        rows, cols = 2, 4
        row_vars = [vars_[0]]
        col_vars = vars_[1:]
    else:
        rows, cols = 4, 4
        row_vars = vars_[:2]
        col_vars = vars_[2:]

    k_map = [[0 for _ in range(cols)] for _ in range(rows)]

    for term in terms:
        row = 0
        for var in row_vars:
            row = (row << 1) | term[vars_.index(var)]
        col = 0
        for var in col_vars:
            col = (col << 1) | term[vars_.index(var)]
        if n_vars >= 3:
            col = gray_to_binary(col, len(col_vars))
        k_map[row][col] = 1

    minimized_terms = minimize_karnaugh(k_map, vars_, row_vars, col_vars)

    covered = [[False for _ in range(cols)] for _ in range(rows)]
    for term in minimized_terms:
        for r in range(rows):
            for c in range(cols):
                if all(term[vars_.index(var)] == 'X' or term[vars_.index(var)] == get_term_from_coords(r, c, vars_, row_vars, col_vars)[vars_.index(var)] for var in vars_):
                    covered[r][c] = True

    uncovered_terms = []
    for term in terms:
        row = 0
        for var in row_vars:
            row = (row << 1) | term[vars_.index(var)]
        col = 0
        for var in col_vars:
            col = (col << 1) | term[vars_.index(var)]
        if n_vars >= 3:
            col = gray_to_binary(col, len(col_vars))
        if not covered[row][col]:
            uncovered_terms.append(term)

    if uncovered_terms:
        print("Предупреждение: не все термы покрыты в карте Карно!")
        print("Не покрыты:", [term_to_str(t, vars_, is_dnf) for t in uncovered_terms])

    return [term_to_str(t, vars_, is_dnf) for t in minimized_terms if any(v != 'X' for v in t)]

def main():
    expr = input("Введите логическое выражение :\n")
    print("\nТаблица истинности с подвыражениями:\n")
    data = generate_truth_table_and_forms(expr)
    if data is None:
        return
    minterms = data['minterms']
    maxterms = data['maxterms']
    n_vars = data['n_vars']
    vars_ = data['vars_sorted']
    print("\n========== Результаты минимизации ==========")
    dnf_calc = minimize_calc_dnf(minterms, n_vars, vars_)
    cnf_calc = minimize_calc_cnf(maxterms, n_vars, vars_)
    dnf_tab = minimize_tab_dnf(minterms, n_vars, vars_)
    cnf_tab = minimize_tab_cnf(maxterms, n_vars, vars_)
    dnf_kmap = kmap_minimize(minterms, n_vars, vars_, is_dnf=True)
    cnf_kmap = kmap_minimize(maxterms, n_vars, vars_, is_dnf=False)

    print("Карта для DNF (1→единицы):")
    print_kmap_table(minterms, n_vars, vars_, is_dnf=True)
    print("\nКарта для CNF (0→нули):")
    print_kmap_table(maxterms, n_vars, vars_, is_dnf=False)

    print("\n======= Итоговый рез =======")

    print("\nРезультаты минимизации для СДНФ:")
    print("  1) Расчетный метод:", dnf_calc)
    print("  2) Расчетно-табличный метод:         ", dnf_tab)
    print("  3) Метод Карно:                      ", " ∨ ".join(dnf_kmap))
    print("\nРезультаты минимизации для СКНФ:")
    print("  1) Расчетный метод:", cnf_calc)
    print("  2) Расчетно-табличный метод:         ", cnf_tab)
    print("  3) Метод Карно:                      ", " ∧ ".join(cnf_kmap))

if __name__ == "__main__":
    main()