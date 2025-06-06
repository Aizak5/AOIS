import unittest
import numpy as np
from random import randint
from laba7 import DiagonalMatrix16x16

class TestDiagonalMatrix16x16(unittest.TestCase):
    def setUp(self):
        np.random.seed(42)  
        self.dm = DiagonalMatrix16x16()
    
    def test_matrix_size(self):
        """Проверка размера матрицы"""
        self.assertEqual(self.dm.matrix.shape, (16, 16))
    
    def test_words_count(self):
        """Проверка количества слов"""
        self.assertEqual(len(self.dm.words), 16)
    
    def test_word_structure(self):
        """Проверка структуры слова"""
        word = self.dm.words[0]
        self.assertIn('V', word)
        self.assertIn('A', word)
        self.assertIn('B', word)
        self.assertGreaterEqual(word['V'], 0)
        self.assertLessEqual(word['V'], 7)
        self.assertGreaterEqual(word['A'], 0)
        self.assertLessEqual(word['A'], 15)
        self.assertGreaterEqual(word['B'], 0)
        self.assertLessEqual(word['B'], 15)
    
    def test_get_column(self):
        """Проверка получения столбца"""
        col = self.dm.get_column(0)
        self.assertEqual(len(col), 16)
        
        col = self.dm.get_column(-1)
        self.assertTrue(np.all(col == np.zeros(16, dtype=np.uint8)))
        col = self.dm.get_column(16)
        self.assertTrue(np.all(col == np.zeros(16, dtype=np.uint8)))
    
    def test_get_word(self):
        """Проверка получения слова"""
        word = self.dm.get_word(0)
        self.assertIsNotNone(word)
        self.assertIn('V', word)
        self.assertIn('A', word)
        self.assertIn('B', word)
        
        self.assertIsNone(self.dm.get_word(-1))
        self.assertIsNone(self.dm.get_word(16))
    
    def test_logical_functions(self):
        """Проверка логических функций"""
        # f1 = x1 AND x2
        self.assertEqual(self.dm.logical_function(0, 0, 'f1'), 0)
        self.assertEqual(self.dm.logical_function(0, 1, 'f1'), 0)
        self.assertEqual(self.dm.logical_function(1, 0, 'f1'), 0)
        self.assertEqual(self.dm.logical_function(1, 1, 'f1'), 1)
        
        # f14 = NOT (x1 AND x2)
        self.assertEqual(self.dm.logical_function(0, 0, 'f14'), 1)
        self.assertEqual(self.dm.logical_function(0, 1, 'f14'), 1)
        self.assertEqual(self.dm.logical_function(1, 0, 'f14'), 1)
        self.assertEqual(self.dm.logical_function(1, 1, 'f14'), 0)
        
        # f3 = x1
        self.assertEqual(self.dm.logical_function(0, 0, 'f3'), 0)
        self.assertEqual(self.dm.logical_function(0, 1, 'f3'), 0)
        self.assertEqual(self.dm.logical_function(1, 0, 'f3'), 1)
        self.assertEqual(self.dm.logical_function(1, 1, 'f3'), 1)
        
        # f12 = NOT x1
        self.assertEqual(self.dm.logical_function(0, 0, 'f12'), 1)
        self.assertEqual(self.dm.logical_function(0, 1, 'f12'), 1)
        self.assertEqual(self.dm.logical_function(1, 0, 'f12'), 0)
        self.assertEqual(self.dm.logical_function(1, 1, 'f12'), 0)
        
        # Неизвестная функция
        self.assertEqual(self.dm.logical_function(1, 1, 'unknown'), 0)
    
    def test_search_nearest(self):
        """Проверка поиска ближайшего слова"""
        dm = DiagonalMatrix16x16()
        idx, word = dm.search_nearest(0, 'above')
        if idx != -1:
            self.assertIsNotNone(word)
            self.assertEqual(word['V'], 0)
        
        idx, word = dm.search_nearest(0, 'below')
        if idx != -1:
            self.assertIsNotNone(word)
            self.assertEqual(word['V'], 0)
    
    def test_add_fields(self):
        """Проверка сложения полей A и B"""
        dm = DiagonalMatrix16x16()
        
        v_value = dm.words[0]['V']
        results = dm.add_fields(v_value)
        
        for i, word, sum_ab in results:
            self.assertEqual(word['V'], v_value)
            self.assertEqual(sum_ab, word['A'] + word['B'])
    
    def test_diagonal_storage(self):
        """Проверка диагонального хранения слов"""
        for word_idx in range(16):
            original_word = self.dm.words[word_idx]
            stored_word = self.dm.get_word(word_idx)
            
            self.assertIn('V', stored_word)
            self.assertIn('A', stored_word)
            self.assertIn('B', stored_word)
    
    def test_display_methods(self):
        """Проверка методов отображения (просто проверяем, что не падают)"""
        self.dm.display_matrix()
        self.dm.display_words()

if __name__ == '__main__':
    unittest.main()
