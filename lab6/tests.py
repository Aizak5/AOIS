import unittest
from hash_table import HashTable
class TestHashTable(unittest.TestCase):
    def setUp(self):
        self.ht = HashTable(10)
        
    def test_insert_and_search(self):
        """Тест добавления и поиска элементов"""
        self.assertTrue(self.ht.insert("яблоко", 10))
        self.assertTrue(self.ht.insert("банан", 20))
        self.assertTrue(self.ht.insert("апельсин", 30))
        
        self.assertEqual(self.ht.search("яблоко"), 10)
        self.assertEqual(self.ht.search("банан"), 20)
        self.assertEqual(self.ht.search("апельсин"), 30)
        self.assertIsNone(self.ht.search("несуществующий"))
    
    def test_insert_duplicate(self):
        """Тест добавления дубликата"""
        self.assertTrue(self.ht.insert("яблоко", 10))
        self.assertFalse(self.ht.insert("яблоко", 20)) 
        
    def test_update(self):
        """Тест обновления значений"""
        self.ht.insert("яблоко", 10)
        self.assertTrue(self.ht.update("яблоко", 15))
        self.assertEqual(self.ht.search("яблоко"), 15)
        
        self.assertFalse(self.ht.update("несуществующий", 100))
    
    def test_delete(self):
        """Тест удаления элементов"""
        self.ht.insert("яблоко", 10)
        self.ht.insert("банан", 20)
        
        self.assertTrue(self.ht.delete("яблоко"))
        self.assertIsNone(self.ht.search("яблоко"))
        self.assertEqual(self.ht.search("банан"), 20)
        self.assertFalse(self.ht.delete("несуществующий"))
    
    def test_collision_handling(self):
        """Тест обработки коллизий"""
        small_ht = HashTable(3)
        
        self.assertTrue(small_ht.insert("аб", 1))
        self.assertTrue(small_ht.insert("ба", 2))  
        self.assertTrue(small_ht.insert("вг", 3))  
        self.assertEqual(small_ht.search("аб"), 1)
        self.assertEqual(small_ht.search("ба"), 2)
        self.assertEqual(small_ht.search("вг"), 3)
        
        with self.assertRaises(Exception):
            small_ht.insert("гд", 4)
    
    def test_delete_with_rehashing(self):
        """Тест удаления с последующим рехешированием"""
        small_ht = HashTable(5)
        small_ht.insert("аб", 1)
        small_ht.insert("ба", 2)
        small_ht.insert("вг", 3)
        
        self.assertTrue(small_ht.delete("ба"))
        
        self.assertEqual(small_ht.search("аб"), 1)
        self.assertEqual(small_ht.search("вг"), 3)
        
        self.assertTrue(small_ht.insert("гд", 4))
        self.assertEqual(small_ht.search("гд"), 4)
    
    def test_edge_cases(self):
        """Тест граничных случаев"""
        self.assertIsNone(self.ht.search("любой"))
        self.assertFalse(self.ht.update("любой", 1))
        self.assertFalse(self.ht.delete("любой"))
        
        self.assertTrue(self.ht.insert("а", 100))
        self.assertEqual(self.ht.search("а"), 100)
        
        self.assertTrue(self.ht.insert("123", 200))
        self.assertEqual(self.ht.search("123"), 200)

if __name__ == '__main__':
    unittest.main()