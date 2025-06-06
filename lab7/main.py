from laba7 import DiagonalMatrix16x16
import numpy as np
from random import randint

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