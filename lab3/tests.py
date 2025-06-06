import unittest
from your_module import (
    Node, preprocess_expression, tokenize, shunting_yard, rpn_to_ast,
    parse_expression, label_sub_expressions, compute_depth, 
    collect_sub_expressions_in_order, evaluate_ast, 
    generate_truth_table_and_forms, minimize_calc_dnf, 
    minimize_calc_cnf, minimize_tab_dnf, minimize_tab_cnf,
    kmap_minimize, print_kmap_table
)

class TestPreprocessing(unittest.TestCase):
    def test_preprocess_expression(self):
        self.assertEqual(preprocess_expression("a & b"), "a&b")
        self.assertEqual(preprocess_expression("(a | b) -> c"), "(a|b)->c")
        self.assertEqual(preprocess_expression("  a  &  b  "), "a&b")
        self.assertEqual(preprocess_expression("!!a"), "!!a")
        self.assertEqual(preprocess_expression("a ~ b"), "a~b")

class TestTokenization(unittest.TestCase):
    def test_simple_tokens(self):
        self.assertEqual(tokenize("a&b"), ['a', '&', 'b'])
        self.assertEqual(tokenize("!a"), ['!', 'a'])
        self.assertEqual(tokenize("a|b"), ['a', '|', 'b'])
    
    def test_complex_tokens(self):
        self.assertEqual(tokenize("!(a|b)"), ['!', '(', 'a', '|', 'b', ')'])
        self.assertEqual(tokenize("a->b"), ['a', '->', 'b'])
        self.assertEqual(tokenize("a~b"), ['a', '~', 'b'])
    
    def test_invalid_tokens(self):
        with self.assertRaises(ValueError):
            tokenize("a @ b")

class TestShuntingYard(unittest.TestCase):
    def test_simple_expressions(self):
        self.assertEqual(shunting_yard(['a', '&', 'b']), ['a', 'b', '&'])
        self.assertEqual(shunting_yard(['!', 'a']), ['a', '!'])
    
    def test_complex_expressions(self):
        self.assertEqual(
            shunting_yard(['(', 'a', '|', 'b', ')', '&', 'c']),
            ['a', 'b', '|', 'c', '&']
        )
        self.assertEqual(
            shunting_yard(['!', '(', 'a', '&', 'b', ')']),
            ['a', 'b', '&', '!']
        )
    
    def test_operator_precedence(self):
        self.assertEqual(
            shunting_yard(['a', '&', 'b', '|', 'c']),
            ['a', 'b', '&', 'c', '|']
        )
        self.assertEqual(
            shunting_yard(['a', '|', 'b', '&', 'c']),
            ['a', 'b', 'c', '&', '|']
        )

class TestASTConstruction(unittest.TestCase):
    def test_simple_ast(self):
        ast = rpn_to_ast(['a', 'b', '&'])
        self.assertEqual(ast.node_type, 'and')
        self.assertEqual(ast.left.var, 'a')
        self.assertEqual(ast.right.var, 'b')
    
    def test_not_ast(self):
        ast = rpn_to_ast(['a', '!'])
        self.assertEqual(ast.node_type, 'not')
        self.assertEqual(ast.left.var, 'a')
    
    def test_complex_ast(self):
        ast = rpn_to_ast(['a', 'b', '&', 'c', '|'])
        self.assertEqual(ast.node_type, 'or')
        self.assertEqual(ast.left.node_type, 'and')
        self.assertEqual(ast.right.var, 'c')

class TestExpressionParsing(unittest.TestCase):
    def test_parse_simple(self):
        ast = parse_expression("a & b")
        self.assertEqual(ast.node_type, 'and')
    
    def test_parse_complex(self):
        ast = parse_expression("!(a | b) & c")
        self.assertEqual(ast.node_type, 'and')
        self.assertEqual(ast.left.node_type, 'not')
        self.assertEqual(ast.right.var, 'c')
    
    def test_parse_invalid(self):
        with self.assertRaises(ValueError):
            parse_expression("a &")

class TestASTEvaluation(unittest.TestCase):
    def test_simple_evaluation(self):
        ast = parse_expression("a & b")
        self.assertTrue(evaluate_ast(ast, {'a': True, 'b': True}))
        self.assertFalse(evaluate_ast(ast, {'a': True, 'b': False}))
    
    def test_not_evaluation(self):
        ast = parse_expression("!a")
        self.assertFalse(evaluate_ast(ast, {'a': True}))
        self.assertTrue(evaluate_ast(ast, {'a': False}))
    
    def test_complex_evaluation(self):
        ast = parse_expression("(a | b) & c")
        self.assertTrue(evaluate_ast(ast, {'a': False, 'b': True, 'c': True}))
        self.assertFalse(evaluate_ast(ast, {'a': True, 'b': True, 'c': False}))

class TestTruthTableGeneration(unittest.TestCase):
    def test_simple_truth_table(self):
        result = generate_truth_table_and_forms("a & b")
        self.assertEqual(result['minterms'], [3])
        self.assertEqual(result['maxterms'], [0, 1, 2])
        self.assertEqual(result['vars_sorted'], ['a', 'b'])
    
    def test_three_var_truth_table(self):
        result = generate_truth_table_and_forms("a & b & c")
        self.assertEqual(len(result['truth_table']), 8)
        self.assertEqual(result['minterms'], [7])
    
    def test_complex_truth_table(self):
        result = generate_truth_table_and_forms("(a | b) & c")
        self.assertEqual(result['minterms'], [3, 5, 7])
        self.assertEqual(result['maxterms'], [0, 1, 2, 4, 6])

class TestMinimization(unittest.TestCase):
    def test_dnf_minimization(self):
        result = generate_truth_table_and_forms("a & b")
        minimized = minimize_calc_dnf(result['minterms'], result['n_vars'], result['vars_sorted'])
        self.assertEqual(minimized, "(a∧b)")
    
    def test_cnf_minimization(self):
        result = generate_truth_table_and_forms("a | b")
        minimized = minimize_calc_cnf(result['maxterms'], result['n_vars'], result['vars_sorted'])
        self.assertTrue("(a∨b)" in minimized)
    
    def test_tabular_minimization(self):
        result = generate_truth_table_and_forms("a & b")
        minimized = minimize_tab_dnf(result['minterms'], result['n_vars'], result['vars_sorted'])
        self.assertEqual(minimized, "(a∧b)")
    
    def test_kmap_minimization(self):
        result = generate_truth_table_and_forms("a ~ b")
        minimized = kmap_minimize(result['minterms'], result['n_vars'], result['vars_sorted'], is_dnf=True)
        self.assertTrue(any("¬a∧b" in term or "a∧¬b" in term for term in minimized))

class TestEdgeCases(unittest.TestCase):
    def test_single_variable(self):
        result = generate_truth_table_and_forms("a")
        self.assertEqual(result['minterms'], [1])
        self.assertEqual(result['maxterms'], [0])
    
    def test_constant_true(self):
        result = generate_truth_table_and_forms("a | !a")
        self.assertEqual(result['minterms'], [0, 1])
        self.assertEqual(result['maxterms'], [])
    
    def test_constant_false(self):
        result = generate_truth_table_and_forms("a & !a")
        self.assertEqual(result['minterms'], [])
        self.assertEqual(result['maxterms'], [0, 1])

class TestErrorHandling(unittest.TestCase):
    def test_invalid_syntax(self):
        with self.assertRaises(ValueError):
            parse_expression("a &")
        with self.assertRaises(ValueError):
            parse_expression("a b")
    
    def test_empty_expression(self):
        with self.assertRaises(ValueError):
            parse_expression("")
    
    def test_invalid_characters(self):
        with self.assertRaises(ValueError):
            parse_expression("a @ b")

if __name__ == "__main__":
    unittest.main()
