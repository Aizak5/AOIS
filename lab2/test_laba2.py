import unittest
from unittest.mock import patch
from io import StringIO
import itertools
from laba2 import LogicFunctionCalculator

class TestLogicFunctionCalculator(unittest.TestCase):
    def setUp(self):
        self.calculator = LogicFunctionCalculator()

    def test_parse_expression(self):
        test_cases = [
            ("a∧b", "a and b"),
            ("a∨b", "a or b"),
            ("!a", " not a"),
            ("a~b", "a == b"),
            ("a->b", "a <= b"),
            ("a∧b∨c", "a and b or c"),
            ("!(a∨b)", " not (a or b)"),
        ]
        
        for expr, expected in test_cases:
            with self.subTest(expr=expr):
                self.assertEqual(self.calculator.parse_expression(expr), expected)

    def test_get_variables(self):
        test_cases = [
            ("a", ['a']),
            ("a∧b", ['a', 'b']),
            ("b∨a", ['a', 'b']),
            ("a∧b∨c∧d", ['a', 'b', 'c', 'd']),
            ("a∧a∨a", ['a']),
            ("e∧d∨c∧b∨a", ['a', 'b', 'c', 'd', 'e']),
            ("", []),
        ]
        
        for expr, expected in test_cases:
            with self.subTest(expr=expr):
                self.assertEqual(self.calculator.get_variables(expr), expected)

    def test_compute_truth_table(self):
        test_cases = [
            ("a", 
             [{'a': 0, 'result': 0}, {'a': 1, 'result': 1}],
             ['a']),
            ("!a", 
             [{'a': 0, 'result': 1}, {'a': 1, 'result': 0}],
             ['a']),
            ("a∧b", 
             [
                {'a': 0, 'b': 0, 'result': 0},
                {'a': 0, 'b': 1, 'result': 0},
                {'a': 1, 'b': 0, 'result': 0},
                {'a': 1, 'b': 1, 'result': 1}
             ],
             ['a', 'b']),
            ("a∨b", 
             [
                {'a': 0, 'b': 0, 'result': 0},
                {'a': 0, 'b': 1, 'result': 1},
                {'a': 1, 'b': 0, 'result': 1},
                {'a': 1, 'b': 1, 'result': 1}
             ],
             ['a', 'b']),
        ]
        
        for expr, expected_table, expected_vars in test_cases:
            with self.subTest(expr=expr):
                table, vars = self.calculator.compute_truth_table(expr)
                self.assertEqual(table, expected_table)
                self.assertEqual(vars, expected_vars)

    def test_generate_normal_forms(self):
        test_cases = [
            ("a", 
             ("(a)", "(a)", [1], [0])),
            ("!a", 
             ("(¬a)", "(¬a)", [0], [1])),
            ("a∧b", 
             ("(a∧b)", "(a∨b) ∧ (a∨¬b) ∧ (¬a∨b)", [3], [0, 1, 2])),
            ("a∨b", 
             ("(¬a∧b) ∨ (a∧¬b) ∨ (a∧b)", "(a∨b)", [1, 2, 3], [0])),
        ]
        
        for expr, expected in test_cases:
            with self.subTest(expr=expr):
                table, vars = self.calculator.compute_truth_table(expr)
                sdnf, sknf, sdnf_nums, sknf_nums = self.calculator.generate_normal_forms(table, vars)
                self.assertEqual(sdnf, expected[0])
                self.assertEqual(sknf, expected[1])
                self.assertEqual(sdnf_nums, expected[2])
                self.assertEqual(sknf_nums, expected[3])

    def test_calculate_index_form(self):
        test_cases = [
            ([{'result': 0}], (0, "0")),
            ([{'result': 1}], (1, "1")),
            ([{'result': 0}, {'result': 1}], (1, "01")),
            ([{'result': 1}, {'result': 0}], (2, "10")),
            ([{'result': 0}, {'result': 0}, {'result': 1}, {'result': 1}], (3, "0011")),
        ]
        
        for table, expected in test_cases:
            with self.subTest(table=table):
                self.assertEqual(self.calculator.calculate_index_form(table), expected)

    def test_process_expression_invalid_chars(self):
        invalid_exprs = [
            "a∧f",  
            "a∧g",
            "a∧z",
            "a∧A", 
            "a∧B", 
            "a∧1",  
            "a∧2",
            "a∧"  
        ]
        
        for expr in invalid_exprs:
            with self.subTest(expr=expr):
                with self.assertRaises(ValueError):
                    self.calculator.process_expression(expr)
        valid_exprs = [
            "a∧b",
            "a∨b",
            "!a",
            "a~b",
            "a->b"
        ]
        
        for expr in valid_exprs:
            with self.subTest(expr=expr):
                try:
                    self.calculator.process_expression(expr)
                except ValueError:
                    self.fail(f"Valid expression '{expr}' raised ValueError unexpectedly")

    @patch('sys.stdout', new_callable=StringIO)
    @patch('builtins.input', return_value="a∧b")
    def test_main(self, mock_input, mock_stdout):
        import laba2
        laba2.main()
        output = mock_stdout.getvalue()
        self.assertIn("Таблица истинности:", output)
        self.assertIn("a | b | F", output)
        self.assertIn("СДНФ:", output)
        self.assertIn("СКНФ:", output)
        self.assertIn("Числовые формы:", output)
        self.assertIn("Индексная форма:", output)

    @patch('sys.stdout', new_callable=StringIO)
    @patch('builtins.input', return_value="a∧f")
    def test_main_error(self, mock_input, mock_stdout):
        import laba2
        laba2.main()
        output = mock_stdout.getvalue()
        self.assertIn("Ошибка:", output)

def test_eval_error_handling(self):
    expr = "a∧(b"
    table, _ = self.calculator.compute_truth_table(expr)
    for row in table:
        self.assertEqual(row['result'], 0)

def test_generate_normal_forms_all_zero_all_one(self):
    table_zero = [{'a': 0, 'b': 0, 'result': 0}, {'a': 0, 'b': 1, 'result': 0}]
    sdnf, sknf, _, _ = self.calculator.generate_normal_forms(table_zero, ['a', 'b'])
    self.assertEqual(sdnf, '0')  
    self.assertTrue(sknf.startswith("("))

    table_one = [{'a': 0, 'b': 0, 'result': 1}, {'a': 0, 'b': 1, 'result': 1}]
    sdnf, sknf, _, _ = self.calculator.generate_normal_forms(table_one, ['a', 'b'])
    self.assertEqual(sknf, '1')  
    self.assertTrue(sdnf.startswith("("))

    def test_process_expression_invalid_chars(self):
        invalid_exprs = [
            "a∧A", 
            "a∧B",  
            "a∧1",  
            "a∧",   
        ]

if __name__ == '__main__':
    unittest.main()
