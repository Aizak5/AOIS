from itertools import product
import re

def replace_logical_operators(expr):
    expr = re.sub(r'([a-zA-Z0-1()]+)\s*→\s*([a-zA-Z0-1()]+)', r'(not \1) or \2', expr)
    expr = re.sub(r'([a-zA-Z0-1()]+)\s*⇒\s*([a-zA-Z0-1()]+)', r'(not \1) or \2', expr)
    expr = re.sub(r'([a-zA-Z0-1()]+)\s*↔\s*([a-zA-Z0-1()]+)', r'(\1 == \2)', expr)
    expr = re.sub(r'([a-zA-Z0-1()]+)\s*⇔\s*([a-zA-Z0-1()]+)', r'(\1 == \2)', expr)
    
    expr = (expr.replace('!', ' not ')
            .replace('&', ' and ')
            .replace('|', ' or '))
    
    return expr

def generate_truth_table(expr):
    print("\nТаблица истинности с подвыражениями:\n")
    
    normalized_expr = expr.replace(' ', '')
    variables = sorted(list(set(re.findall(r'\b[a-z]\b', normalized_expr))))
    num_vars = len(variables)
    
    sub_expressions = []
    if '→' in normalized_expr or '⇒' in normalized_expr:
        parts = re.split(r'→|⇒', normalized_expr)
        sub_expressions.append(parts[0])
        sub_expressions.append(parts[1])
    if '↔' in normalized_expr or '⇔' in normalized_expr:
        parts = re.split(r'↔|⇔', normalized_expr)
        sub_expressions.append(parts[0])
        sub_expressions.append(parts[1])
    
    headers = variables.copy()
    for sub in sub_expressions:
        headers.append(sub)
    headers.append(normalized_expr)
    
    header_line = " | ".join(headers)
    print(header_line)
    print("-" * len(header_line) * 2)
    
    truth_table = []
    for values in product([0, 1], repeat=num_vars):
        var_values = dict(zip(variables, values))
        row = []
        
        for var in variables:
            row.append(str(var_values[var]))
        
        sub_values = []
        for sub in sub_expressions:
            try:
                current_sub = sub
                for var in variables:
                    current_sub = current_sub.replace(var, str(var_values[var]))
                current_sub = replace_logical_operators(current_sub)
                sub_values.append(int(eval(current_sub)))
            except:
                sub_values.append(0)
        
        current_expr = normalized_expr
        for var in variables:
            current_expr = current_expr.replace(var, str(var_values[var]))
        current_expr = replace_logical_operators(current_expr)
        try:
            result = int(eval(current_expr))
        except:
            result = 0
        
        row.extend([str(v) for v in sub_values])
        row.append(str(result))
        print(" | ".join(row))
        
        truth_table.append((values, result))
    
    minterms = [term for term, res in truth_table if res == 1]
    maxterms = [term for term, res in truth_table if res == 0]
    
    print("\nСовершенная дизъюнктивная нормальная форма (СДНФ)")
    print(" ∨ ".join(["(" + "∧".join([f"¬{variables[i]}" if not t[i] else variables[i] for i in range(num_vars)]) + ")" for t in minterms]))
    
    print("\nСовершенная конъюнктивная нормальная форма (СКНФ)")
    print(" ∧ ".join(["(" + "∨".join([f"¬{variables[i]}" if t[i] else variables[i] for i in range(num_vars)]) + ")" for t in maxterms]))
    
    return {
        'minterms': minterms,
        'maxterms': maxterms,
        'num_vars': num_vars,
        'variables': variables
    }

def format_term(term, variables, is_dnf=True):
    parts = []
    for val, var in zip(term, variables):
        if val == 'X':
            continue
        if is_dnf:
            parts.append(f"¬{var}" if val == 0 else var)
        else:
            parts.append(var if val == 0 else f"¬{var}")
    return "".join(parts) if is_dnf else f"({'∨'.join(parts)})" if parts else ""

def minimize_dnf_calculus(terms, num_vars, variables):
    return minimize_by_calculus(terms, variables, is_dnf=True)

def minimize_cnf_calculus(terms, num_vars, variables):
    return minimize_by_calculus(terms, variables, is_dnf=False)

def minimize_by_calculus(terms, variables, is_dnf=True):
    if not terms:
        return []

    print("\nИтерации склеивания:")
    current_terms = terms.copy()

    while True:
        new_terms = []
        used = set()

        print("\nТекущие термы:")
        for term in current_terms:
            print(format_term(term, variables, is_dnf), end=" ")
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
                            f"Склеиваем: {format_term(term1, variables, is_dnf)} и {format_term(term2, variables, is_dnf)} -> {format_term(new_term, variables, is_dnf)}")

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
        print(separator.join(format_term(t, variables, is_dnf) for t in essential_terms))
    else:
        print("0" if is_dnf else "1")

    return [format_term(t, variables, is_dnf) for t in essential_terms]

def minimize_dnf_table(terms, num_vars, variables):
    return minimize_by_table(terms, variables, is_dnf=True)

def minimize_cnf_table(terms, num_vars, variables):
    return minimize_by_table(terms, variables, is_dnf=False)

def minimize_by_table(terms, variables, is_dnf=True):
    minimized_terms = minimize_by_calculus(terms, variables, is_dnf)
    if not minimized_terms or not terms:
        return []

    print("\nТаблица покрытия:")
    imp_width = max(len(t) for t in minimized_terms) + 2
    term_width = max(len(format_term(t, variables, is_dnf)) for t in terms) + 2

    header = " " * imp_width
    for term in terms:
        header += f" {format_term(term, variables, is_dnf):^{term_width}}"
    print(header)

    for imp in minimized_terms:
        row = f" {imp:<{imp_width - 1}}"
        for term in terms:
            match = False
            for t in minimize_by_calculus([term], variables, is_dnf):
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

def print_kmap(terms, num_vars, variables, is_dnf=True):
    if not terms:
        print("0 (ложь)" if is_dnf else "1 (истина)")
        return

    if num_vars == 2:
        rows, cols = 2, 2
        row_vars = [variables[0]]
        col_vars = [variables[1]]
    elif num_vars == 3:
        rows, cols = 2, 4
        row_vars = [variables[0]]
        col_vars = variables[1:]
    else:
        rows, cols = 4, 4
        row_vars = variables[:2]
        col_vars = variables[2:]

    k_map = [[0 for _ in range(cols)] for _ in range(rows)]

    for term in terms:
        row = 0
        for var in row_vars:
            row = (row << 1) | term[variables.index(var)]
        col = 0
        for var in col_vars:
            col = (col << 1) | term[variables.index(var)]
        if num_vars >= 3:
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

def minimize_kmap(k_map, variables, row_vars, col_vars):
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

def minimize_by_kmap(terms, num_vars, variables, is_dnf=True):
    if num_vars > 4:
        print("Карты Карно для более чем 4 переменных не поддерживаются")
        return []
    elif num_vars < 2:
        print("Карты Карно требуют как минимум 2 переменных")
        return []
    elif not terms:
        print("0 (ложь)" if is_dnf else "1 (истина)")
        return []

    if num_vars == 2:
        rows, cols = 2, 2
        row_vars = [variables[0]]
        col_vars = [variables[1]]
    elif num_vars == 3:
        rows, cols = 2, 4
        row_vars = [variables[0]]
        col_vars = variables[1:]
    else:
        rows, cols = 4, 4
        row_vars = variables[:2]
        col_vars = variables[2:]

    k_map = [[0 for _ in range(cols)] for _ in range(rows)]

    for term in terms:
        row = 0
        for var in row_vars:
            row = (row << 1) | term[variables.index(var)]
        col = 0
        for var in col_vars:
            col = (col << 1) | term[variables.index(var)]
        if num_vars >= 3:
            col = gray_to_binary(col, len(col_vars))
        k_map[row][col] = 1

    minimized_terms = minimize_kmap(k_map, variables, row_vars, col_vars)

    covered = [[False for _ in range(cols)] for _ in range(rows)]
    for term in minimized_terms:
        for r in range(rows):
            for c in range(cols):
                if all(term[variables.index(var)] == 'X' or term[variables.index(var)] == get_term_from_coords(r, c, variables, row_vars, col_vars)[variables.index(var)] for var in variables):
                    covered[r][c] = True

    uncovered_terms = []
    for term in terms:
        row = 0
        for var in row_vars:
            row = (row << 1) | term[variables.index(var)]
        col = 0
        for var in col_vars:
            col = (col << 1) | term[variables.index(var)]
        if num_vars >= 3:
            col = gray_to_binary(col, len(col_vars))
        if not covered[row][col]:
            uncovered_terms.append(term)

    if uncovered_terms:
        print("Предупреждение: не все термы покрыты в карте Карно!")
        print("Не покрыты:", [format_term(t, variables, is_dnf) for t in uncovered_terms])

    return [format_term(t, variables, is_dnf) for t in minimized_terms if any(v != 'X' for v in t)]

def main():
    expr = input("Введите логическое выражение:\n")
    data = generate_truth_table(expr)
    if data is None:
        return
    
    minterms = data['minterms']
    maxterms = data['maxterms']
    num_vars = data['num_vars']
    variables = data['variables']
    
    print("\n========== Результаты минимизации ==========")
    
    print("\n==== Минимизация СДНФ (расчётный метод) ====\n")
    dnf_calc = minimize_dnf_calculus(minterms, num_vars, variables)
    print("\nРЕЗУЛЬТАТ (расчётный метод, СДНФ):", " ∨ ".join(dnf_calc))
    
    print("\n==== Минимизация СКНФ (расчётный метод) ====\n")
    cnf_calc = minimize_cnf_calculus(maxterms, num_vars, variables)
    print("\nРЕЗУЛЬТАТ (расчётный метод, СКНФ):", " ∧ ".join(cnf_calc))
    
    print("\n==== Минимизация СДНФ (расчётно-табличный метод) ====\n")
    dnf_tab = minimize_dnf_table(minterms, num_vars, variables)
    print("\nРЕЗУЛЬТАТ (табличный метод, СДНФ):", " ∨ ".join(dnf_tab))
    
    print("\n==== Минимизация СКНФ (расчётно-табличный метод) ====\n")
    cnf_tab = minimize_cnf_table(maxterms, num_vars, variables)
    print("\nРЕЗУЛЬТАТ (табличный метод, СКНФ):", " ∧ ".join(cnf_tab))
    
    print("\nКарта для ДНФ:")
    print_kmap(minterms, num_vars, variables, is_dnf=True)
    
    print("\nКарта для КНФ:")
    print_kmap(maxterms, num_vars, variables, is_dnf=False)
    
    print("\n======= Итог =======")
    
    print("\nРезультаты минимизации для СДНФ:")
    print("  1) Расчетный метод:                  ", " ∨ ".join(dnf_calc))
    print("  2) Расчетно-табличный метод:         ", " ∨ ".join(dnf_tab))
    print("  3) Метод Карно:                      ", " ∨ ".join(minimize_by_kmap(minterms, num_vars, variables, is_dnf=True)))
    
    print("\nРезультаты минимизации для СКНФ:")
    print("  1) Расчетный метод:                  ", " ∧ ".join(cnf_calc))
    print("  2) Расчетно-табличный метод:         ", " ∧ ".join(cnf_tab))
    print("  3) Метод Карно:                      ", " ∧ ".join(minimize_by_kmap(maxterms, num_vars, variables, is_dnf=False)))

if __name__ == "__main__":
    main()
