import numpy as np
import unittest
from laba7 import DiagonalMatrix16x16

class TestDiagonalMatrix16x16(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.simple_matrix = np.zeros((16, 16), dtype=np.uint8)
        for i in range(16):
            cls.simple_matrix[i, i] = 1

    def setUp(self):
        self.dm = DiagonalMatrix16x16(self.simple_matrix.copy())

    def test_get_word_fields(self):
        clean_matrix = np.zeros((16, 16), dtype=np.uint8)
        for i in range(16):
            clean_matrix[i, i] = 1
        
        self.dm = DiagonalMatrix16x16(clean_matrix)
        word0 = self.dm.get_word(0)
        
        self.assertEqual(int(word0['V']), 7)   
        self.assertEqual(int(word0['A']), 15) 
        self.assertEqual(int(word0['B']), 15)  
        self.assertEqual(int(word0['S']), 31)  

    def test_set_word_bits(self):
        new_bits = [1]*16
        self.assertTrue(self.dm.set_word_bits(0, new_bits))
        word0 = self.dm.get_word(0)
        self.assertTrue(all(word0['bits']))

    def test_update_s_field(self):
        self.dm.update_s_field(0, 0b10101)
        word0 = self.dm.get_word(0)
        self.assertEqual(int(word0['S']), 0b10101)

    def test_get_address_column(self):
        col = self.dm.get_address_column(0)
        self.assertEqual(len(col), 13) 
        self.assertEqual(sum(col), 13)  

    def test_logical_functions(self):
        temp_dm = DiagonalMatrix16x16(np.zeros((16, 16), dtype=np.uint8))
        
        self.assertEqual(temp_dm.logical_function(1, 1, 'f1'), 1)
        self.assertEqual(temp_dm.logical_function(1, 0, 'f1'), 0)
        
        self.assertEqual(temp_dm.logical_function(1, 1, 'f14'), 0)
        self.assertEqual(temp_dm.logical_function(1, 0, 'f14'), 1)
        
        self.assertEqual(temp_dm.logical_function(1, 0, 'f3'), 1)
        
        self.assertEqual(temp_dm.logical_function(1, 0, 'f12'), 0)

    def test_apply_logical_to_words(self):
        self.dm.set_word_bits(0, [1]*16)
        self.dm.set_word_bits(1, [0]*16)
        self.assertTrue(self.dm.apply_logical_to_words('f1', 0, 1, 2))
        word2 = self.dm.get_word(2)
        self.assertTrue(all(b == 0 for b in word2['bits']))

    def test_binary_sum_manual(self):
        temp_dm = DiagonalMatrix16x16(np.zeros((16, 16), dtype=np.uint8))
        result = temp_dm.binary_sum_manual(0b0111, 0b1001, 4)
        self.assertEqual(result, [0, 0, 0, 0, 1])

    def test_sum_ab_for_v(self):
        matrix = np.zeros((16, 16), dtype=np.uint8)
        for i in range(16):
            matrix[i, (0 + i) % 16] = 1
        
        test_dm = DiagonalMatrix16x16(matrix)
        results = test_dm.sum_ab_for_v(7)
        
        self.assertEqual(len(results), 1)
        i, word, sum_bits = results[0]
        self.assertEqual(i, 0)
        
        s_str = ''.join(str(int(b)) for b in sum_bits)
        s_val = int(s_str, 2)
        self.assertEqual(test_dm.get_word(0)['S'], s_val)

if __name__ == '__main__':
    unittest.main()