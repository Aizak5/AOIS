import itertools


class LogicFunctionCalculator:
    def __init__(self):
        self.operations = {
            '∧': ' and ',
            '∨': ' or ',
            '!': ' not ',
            '~': ' == ',
            '->': ' <= '
        }

    def parse_expression(self, expr):
        """Полностью изолированная обработка выражения"""
        for op, replacement in self.operations.items():
            expr = expr.replace(op, replacement)
        return expr

    def get_variables(self, expr):
        """Получаем переменные в строгом порядке a-e без повторов"""
        variables = []
        for var in 'abcde':
            if var in expr and var not in variables:
                variables.append(var)
        return variables

    def compute_truth_table(self, expr):
        """Вычисляем таблицу истинности в чистом контексте"""
        variables = self.get_variables(expr)
        truth_table = []

        for values in itertools.product([0, 1], repeat=len(variables)):
            context = dict(zip(variables, values))
            try:
                result = int(eval(self.parse_expression(expr), {'__builtins__': None}, context))
            except:
                result = 0
            truth_table.append({**context, 'result': result})

        return truth_table, variables

    def generate_normal_forms(self, truth_table, variables):
        """Генерируем СДНФ и СКНФ"""
        sdnf, sknf = [], []
        sdnf_nums, sknf_nums = [], []

        for i, row in enumerate(truth_table):
            if row['result']:
                term = [var if row[var] else f'¬{var}' for var in variables]
                sdnf.append(f"({'∧'.join(term)})")
                sdnf_nums.append(i)
            else:
                term = [var if not row[var] else f'¬{var}' for var in variables]
                sknf.append(f"({'∨'.join(term)})")
                sknf_nums.append(i)

        return (
            ' ∨ '.join(sdnf) if sdnf else '0',
            ' ∧ '.join(sknf) if sknf else '1',
            sorted(sdnf_nums),
            sorted(sknf_nums))

    def calculate_index_form(self, truth_table):
        """Вычисляем индексную форму"""
        binary = ''.join(str(row['result']) for row in truth_table)
        return int(binary, 2), binary

    def process_expression(self, expr):
        allowed = set('abcde∧∨!~->() ')
        if any(c not in allowed for c in expr):
            raise ValueError("Недопустимые символы в выражении")

        variables = self.get_variables(expr)
        parsed_expr = self.parse_expression(expr)

        # Пробуем выполнить eval один раз, чтобы отловить синтаксические ошибки
        try:
            # Используем фиктивный контекст с 0 и 1
            test_context = {var: 0 for var in variables}
            eval(parsed_expr, {'__builtins__': None}, test_context)
        except Exception:
            raise ValueError("Синтаксическая ошибка в выражении")

        truth_table, _ = self.compute_truth_table(expr)

        # Формируем результаты
        results = {
            'variables': variables,
            'truth_table': truth_table,
            'sdnf': None,
            'sknf': None,
            'numeric_forms': None,
            'index_form': None
        }

        results['sdnf'], results['sknf'], sdnf_nums, sknf_nums = self.generate_normal_forms(truth_table, variables)
        results['numeric_forms'] = (sknf_nums, sdnf_nums)
        results['index_form'] = self.calculate_index_form(truth_table)

        return results

def main():
    calculator = LogicFunctionCalculator()

    print("Введите логическое выражение (например, (a∨b)∧!c):")
    user_expr = input().strip()

    try:
        results = calculator.process_expression(user_expr)



        print("\nТаблица истинности:")
        header = results['variables'] + ['F']
        print(" | ".join(header))
        print("-" * (len(" | ".join(header)) + 2))
        for row in results['truth_table']:
            print(" | ".join(str(row[var]) for var in results['variables']) + f" | {row['result']}")

        print("\nСДНФ:", results['sdnf'])
        print("СКНФ:", results['sknf'])

        print("\nЧисловые формы:")
        print(f"({', '.join(map(str, results['numeric_forms'][0]))}) ∧")
        print(f"({', '.join(map(str, results['numeric_forms'][1]))}) ∨")

        decimal, binary = results['index_form']
        print(f"\nИндексная форма: {decimal} - {binary}")

    except ValueError as e:
        print(f"Ошибка: {e}")


if __name__ == "__main__":
    main()