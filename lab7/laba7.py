import numpy as np

class DiagonalMatrix16x16:
    def __init__(self, matrix):
        self.size = 16
        self.matrix = matrix.copy()
        self.update_words_cache()
    
    def update_words_cache(self):
        self.words = [self.get_word(i) for i in range(self.size)]
    
    def get_word(self, word_idx):
        if 0 <= word_idx < self.size:
            bits = []
            for row in range(16):
                col = (word_idx + row) % 16
                bits.append(self.matrix[row, col])
            
            v = (bits[0] << 2) | (bits[1] << 1) | bits[2]
            a = (bits[3] << 3) | (bits[4] << 2) | (bits[5] << 1) | bits[6]
            b = (bits[7] << 3) | (bits[8] << 2) | (bits[9] << 1) | bits[10]
            s = (bits[11] << 4) | (bits[12] << 3) | (bits[13] << 2) | (bits[14] << 1) | bits[15]
            
            return {'V': v, 'A': a, 'B': b, 'S': s, 'bits': bits.copy()}
        return None
    
    def set_word_bits(self, word_idx, new_bits):
        if len(new_bits) != 16:
            return False
        
        for row in range(16):
            col = (word_idx + row) % 16
            self.matrix[row, col] = new_bits[row]
        
        self.update_words_cache()
        return True
    
    def update_s_field(self, word_idx, s_value):
        if word_idx < 0 or word_idx >= self.size:
            return False
        
        word = self.get_word(word_idx)
        if not word:
            return False
        
        new_bits = word['bits'].copy()
        for i in range(5):
            new_bits[11 + i] = (s_value >> (4 - i)) & 1
        
        return self.set_word_bits(word_idx, new_bits)
    
    def get_address_column(self, word_idx):
        if 0 <= word_idx < self.size:
            bits = []
            for row in range(3, 16):
                col = (word_idx + row) % 16
                bits.append(self.matrix[row, col])
            return bits
        return []
    
    def logical_function(self, x1, x2, func_name):
        funcs = {
            'f1': lambda x1, x2: x1 & x2,
            'f14': lambda x1, x2: 1 - (x1 & x2),
            'f3': lambda x1, x2: x1,
            'f12': lambda x1, x2: 1 - x1
        }
        return funcs.get(func_name, lambda x1, x2: 0)(x1, x2)
    
    def apply_logical_to_words(self, func_name, word1_idx, word2_idx, result_word_idx):
        word1 = self.get_word(word1_idx)
        word2 = self.get_word(word2_idx)
        
        if not word1 or not word2:
            return False
        
        result_bits = [
            self.logical_function(word1['bits'][i], word2['bits'][i], func_name)
            for i in range(16)
        ]
        
        return self.set_word_bits(result_word_idx, result_bits)
    
    def binary_sum_manual(self, a, b, n_bits=4):
        result = []
        carry = 0
        for i in range(n_bits):
            bit_a = (a >> i) & 1
            bit_b = (b >> i) & 1
            s = bit_a + bit_b + carry
            result.append(s & 1)
            carry = (s >> 1) & 1
        result.append(carry)
        return result

    def sum_ab_for_v(self, v_value):
        results = []
        for i in range(self.size):
            word = self.get_word(i)
            if word['V'] == v_value:
                sum_bits = self.binary_sum_manual(word['A'], word['B'], n_bits=4)
                sum_bits_reversed = sum_bits[::-1]
                new_bits = word['bits'].copy()
                for j in range(5):
                    new_bits[11 + j] = sum_bits_reversed[j]
                self.set_word_bits(i, new_bits)
                results.append((i, word, sum_bits_reversed))
        return results
    
    def display_matrix(self):
        print("\nТекущее состояние матрицы 16x16:")
        for row in self.matrix:
            print(" ".join(str(int(x)) for x in row))
    
    def display_word(self, word_idx, show_bits=True):
        word = self.get_word(word_idx)
        if word:
            print(f"\nСлово {word_idx}:")
            if show_bits:
                print(f"Биты: {' '.join(map(str, word['bits']))}")
            print(f"V (3 бита): {word['V']:03b} ({word['V']})")
            print(f"A (4 бита): {word['A']:04b} ({word['A']})")
            print(f"B (4 бита): {word['B']:04b} ({word['B']})")
            print(f"S (5 бит): {word['S']:05b} ({word['S']})")