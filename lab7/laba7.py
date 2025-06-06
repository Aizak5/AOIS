import numpy as np
from random import randint

class DiagonalMatrix16x16:
    def __init__(self):
        self.size = 16
        self.matrix = np.random.randint(0, 2, (self.size, self.size), dtype=np.uint8)
        
        self.words = [{'V': randint(0, 7),  
                      'A': randint(0, 15),   
                      'B': randint(0, 15)}   
                     for _ in range(self.size)]
        
        for word_idx in range(self.size):
            col = word_idx
            v_bits = [(self.words[word_idx]['V'] >> i) & 1 for i in range(2, -1, -1)]
            a_bits = [(self.words[word_idx]['A'] >> i) & 1 for i in range(3, -1, -1)]
            b_bits = [(self.words[word_idx]['B'] >> i) & 1 for i in range(3, -1, -1)]
            
            bits = v_bits + a_bits + b_bits
            
            for row in range(len(bits)):
                if row < self.size and col < self.size:
                    self.matrix[row, col] = bits[row]
                col += 1  
    
    def get_column(self, col):
        """Получение разрядного столбца по индексу"""
        if 0 <= col < self.size:
            return self.matrix[:, col]
        return np.zeros(self.size, dtype=np.uint8)
    
    def get_word(self, word_idx):
        """Получение слова по индексу (диагональное чтение)"""
        if 0 <= word_idx < self.size:
            col = word_idx
            bits = []
            for row in range(11): 
                if row < self.size and col < self.size:
                    bits.append(self.matrix[row, col])
                col += 1
            
            v = (bits[0] << 2) | (bits[1] << 1) | bits[2] if len(bits) >= 3 else 0
            a = (bits[3] << 3) | (bits[4] << 2) | (bits[5] << 1) | bits[6] if len(bits) >= 7 else 0
            b = (bits[7] << 3) | (bits[8] << 2) | (bits[9] << 1) | bits[10] if len(bits) >= 11 else 0
            
            return {'V': v, 'A': a, 'B': b}
        return None
    
    def logical_function(self, x1, x2, func_name):
        """Реализация логических функций f1, f14, f3, f12"""
        if func_name == 'f1':    # f1 = x1 AND x2
            return x1 & x2
        elif func_name == 'f14': # f14 = NOT (x1 AND x2)
            return 1 - (x1 & x2)
        elif func_name == 'f3':  # f3 = x1
            return x1
        elif func_name == 'f12': # f12 = NOT x1
            return 1 - x1
        else:
            return 0
    
    def search_nearest(self, v_value, direction='above'):
        """Поиск значения ближайшего сверху/снизу"""
        if direction == 'above':
            for i in range(self.size):
                word = self.get_word(i)
                if word['V'] == v_value:
                    return i, word
        else:
            for i in range(self.size-1, -1, -1):
                word = self.get_word(i)
                if word['V'] == v_value:
                    return i, word
        return -1, None
    
    def add_fields(self, v_value):
        """Сложение полей Aj и Bj в словах, где Vj совпадает с заданным V"""
        results = []
        for i in range(self.size):
            word = self.get_word(i)
            if word['V'] == v_value:
                sum_ab = word['A'] + word['B']
                results.append((i, word, sum_ab))
        return results
    
    def display_matrix(self):
        """Вывод матрицы на экран"""
        print("Матрица 16x16 (случайное заполнение):")
        for row in self.matrix:
            print(' '.join(map(str, row)))
    
    def display_words(self):
        """Вывод всех слов с их полями"""
        print("\nСлова (V, A, B):")
        for i in range(self.size):
            word = self.get_word(i)
            print(f"Слово {i:2d}: V={word['V']} ({word['V']:03b}), "
                  f"A={word['A']} ({word['A']:04b}), "
                  f"B={word['B']} ({word['B']:04b})")

if __name__ == "__main__":
    np.random.seed(42)  
    dm = DiagonalMatrix16x16()
    
    print("="*50)
    print("Матрица 16x16 со случайным заполнением и диагональной адресацией")
    print("="*50)
    
    dm.display_matrix()
    dm.display_words()
    
    print("\n" + "="*50)
    print("Тестирование логических функций:")
    print("x1 x2 | f1 f14 f3 f12")
    print("-"*20)
    for x1, x2 in [(0,0), (0,1), (1,0), (1,1)]:
        print(f"{x1}  {x2}  | {dm.logical_function(x1, x2, 'f1')}   "
              f"{dm.logical_function(x1, x2, 'f14')}   "
              f"{dm.logical_function(x1, x2, 'f3')}   "
              f"{dm.logical_function(x1, x2, 'f12')}")

    random_v = randint(0, 7)
    print("\n" + "="*50)
    print(f"Поиск слова с V={random_v} ({random_v:03b}):")
    

    idx, word = dm.search_nearest(random_v, 'above')
    if idx != -1:
        print(f"Найдено сверху: слово {idx}, V={word['V']} ({word['V']:03b})")
    else:
        print(f"Слово с V={random_v} не найдено (поиск сверху)")

    idx, word = dm.search_nearest(random_v, 'below')
    if idx != -1:
        print(f"Найдено снизу: слово {idx}, V={word['V']} ({word['V']:03b})")
    else:
        print(f"Слово с V={random_v} не найдено (поиск снизу)")

    random_v = randint(0, 7)
    print("\n" + "="*50)
    print(f"Сложение A и B для слов с V={random_v} ({random_v:03b}):")
    sums = dm.add_fields(random_v)
    if sums:
        for i, word, sum_ab in sums:
            print(f"Слово {i:2d}: A={word['A']:2d} + B={word['B']:2d} = {sum_ab:2d}")
    else:
        print(f"Слов с V={random_v} не найдено")