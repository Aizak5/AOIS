from row import Row
class HashTable():
    def __init__(self, size: int):
        self.size = size
        self.table = [None]*size
    
    def str_to_int(self, char: str):
        cl = char.lower()
        letters = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
        for ch in letters:
            if cl == ch:
                return letters.index(ch)
        return 0
    
    def find_v(self, key: str):
        char_num = 2
        v_value = 0
        for i in range(char_num):
            if i < len(key): 
                char_int = self.str_to_int(key[i])
                v_value += char_int * 33**(char_num-i-1)
        return v_value
    
    def hash1(self, key: str):
        return self.find_v(key) % self.size
    
    def hash2(self, key: str):
        prime = 31 
        hash_val = 0
        for char in key:
            hash_val = (hash_val * prime + self.str_to_int(char)) % self.size
        return (hash_val % (self.size - 2)) + 1
    
    def insert(self, key: str, value) -> bool:
        """Create operation - inserts a new key-value pair"""
        if self.search(key) is not None:
            return False 
        
        index = self.hash1(key)
        step = self.hash2(key)
        
        for _ in range(self.size):
            if self.table[index] is None:
                self.table[index] = Row(key, value)
                return True
            index = (index + step) % self.size
        
        raise Exception("Hash table is full")
    
    def search(self, key: str):
        """Read operation - finds value by key"""
        index = self.hash1(key)
        step = self.hash2(key)
        
        for _ in range(self.size):
            if self.table[index] is not None and self.table[index].key == key:
                return self.table[index].value
            if self.table[index] is None:
                return None
            index = (index + step) % self.size
        
        return None
    
    def update(self, key: str, new_value) -> bool:
        """Update operation - updates value for existing key"""
        index = self.hash1(key)
        step = self.hash2(key)
        
        for _ in range(self.size):
            if self.table[index] is not None and self.table[index].key == key:
                self.table[index].value = new_value
                return True
            if self.table[index] is None:
                return False
            index = (index + step) % self.size
        
        return False
    
    def delete(self, key: str) -> bool:
        """Delete operation - removes key-value pair by key"""
        index = self.hash1(key)
        step = self.hash2(key)
        
        for _ in range(self.size):
            if self.table[index] is not None and self.table[index].key == key:
                self.table[index] = None
                
                next_index = (index + step) % self.size
                while self.table[next_index] is not None:
                    row = self.table[next_index]
                    self.table[next_index] = None
                    self.insert(row.key, row.value)
                    next_index = (next_index + step) % self.size
                
                return True
            if self.table[index] is None:
                return False
            index = (index + step) % self.size
        
        return False