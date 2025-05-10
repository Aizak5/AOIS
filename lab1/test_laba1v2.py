import unittest
from unittest.mock import patch
from laba1v2 import (
    int_to_binary, direct_to_reverse, reverse_to_additional,
    direct_to_additional, binary_to_int, binary_addition,
    binary_subtraction, binary_multiplication, binary_division,
    float_to_ieee754, ieee754_to_float, float_addition,input_int,input_float
)

class TestLaba1v2(unittest.TestCase):

    def test_int_to_binary(self):
        self.assertEqual(int_to_binary(5), '00000101')
        self.assertEqual(int_to_binary(-5), '10000101')

    def test_direct_to_reverse(self):
        self.assertEqual(direct_to_reverse('00000101'), '00000101')
        self.assertEqual(direct_to_reverse('11111111'), '10000000')

    def test_reverse_to_additional(self):
        self.assertEqual(reverse_to_additional('00000101'), '00000101')
        self.assertEqual(reverse_to_additional('11111111'), '10000000')

    def test_direct_to_additional(self):
        self.assertEqual(direct_to_additional('00000101'), '00000101')
        self.assertEqual(direct_to_additional('11111111'), '10000001')

    def test_binary_to_int(self):
        self.assertEqual(binary_to_int('00000101'), 5)

    def test_binary_addition(self):self.assertEqual(binary_addition('00000101', '00000001', 8, 8), '00000110')


    def test_binary_subtraction(self):self.assertEqual(binary_subtraction('00000110', '00000001', 8, 8), '00000101')


    def test_binary_multiplication(self):self.assertEqual(binary_multiplication('00000001', '00000010'), '0000000000000010')


    def test_binary_division(self):self.assertEqual(binary_division('00000100', '00000010'), '010.00000')


    def test_float_to_ieee754(self):
        self.assertEqual(float_to_ieee754(1.0), '00111111100000000000000000000000')

    def test_ieee754_to_float(self):
        self.assertEqual(ieee754_to_float('00111111100000000000000000000000'), 1.0)

    def test_float_addition(self):
        self.assertEqual(float_addition('00111111100000000000000000000000', '00111111100000000000000000000000'),
                         '01000000000000000000000000000000')
        
    @patch('builtins.input', side_effect=['a', '5'])
    def test_input_int_invalid_then_valid(self, mock_input):
        self.assertEqual(input_int("Введите число: "), 5)
if __name__ == '__main__':
    unittest.main()
