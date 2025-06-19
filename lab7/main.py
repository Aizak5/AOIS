from laba7 import DiagonalMatrix16x16
import numpy as np

def create_matrix():
    pattern = [
        [1,1,1,1,1,0,0,0,0,1,1,1,0,0,0,0],
        [1,1,1,1,0,0,0,0,1,1,1,0,0,0,0,1],
        [1,1,1,0,0,0,0,1,1,1,0,0,0,0,1,1],
        [1,1,0,0,0,0,1,1,1,0,0,0,0,1,1,1],
        [1,0,0,0,0,1,1,1,0,0,0,0,1,1,1,1],
        [0,0,0,0,1,1,1,0,0,0,0,1,1,1,1,1],
        [0,0,0,1,1,1,0,0,0,0,1,1,1,1,1,0],
        [0,0,1,1,1,0,0,0,0,1,1,1,1,1,0,0],
        [0,1,1,1,0,0,0,0,1,1,1,1,1,0,0,0],
        [1,1,1,0,0,0,0,1,1,1,1,1,0,0,0,0],
        [1,1,0,0,0,0,1,1,1,1,1,0,0,0,0,1],
        [1,0,0,0,0,1,1,1,1,1,0,0,0,0,1,1],
        [0,0,0,0,1,1,1,1,1,0,0,0,0,1,1,1],
        [0,0,0,1,1,1,1,1,0,0,0,0,1,1,1,0],
        [0,0,1,1,1,1,1,0,0,0,0,1,1,1,0,0],
        [0,1,1,1,1,1,0,0,0,0,1,1,1,0,0,0]
    ]
    return np.array(pattern, dtype=np.uint8)

def main():
    matrix = create_matrix()
    dm = DiagonalMatrix16x16(matrix)
    
    while True:
        print("\n" + "="*50)
        print("Меню:")
        print("1. Считать слово")
        print("2. Считать адресный столбец")
        print("3. Применить логическую операцию")
        print("4. Сложение A и B для заданного V (результат в S)")
        print("5. Показать матрицу")
        print("0. Выход")
        
        choice = input("Выберите действие: ")
        
        if choice == "1":
            try:
                word_idx = int(input("Введите номер слова (0-15): "))
                if 0 <= word_idx <= 15:
                    dm.display_word(word_idx)
                else:
                    print("Номер слова должен быть от 0 до 15")
            except ValueError:
                print("Ошибка: введите число от 0 до 15")
                
        elif choice == "2":
            try:
                col_idx = int(input("Введите номер адресного столбца (0-15): "))
                if 0 <= col_idx <= 15:
                    bits = [dm.matrix[i, (col_idx + i) % 16] for i in range(16)]
                    bits_str = ''.join(map(str, bits))
                    print(f"\nАдресный столбец #{col_idx}, результат: {bits_str}")
                else:
                    print("Номер адресного столбца должен быть от 0 до 15")
            except ValueError:
                print("Ошибка: введите число от 0 до 15")
                
        elif choice == "3":
            try:
                print("\nДоступные логические операции:")
                
                func_name = input("Выберите операцию (f1/f14/f3/f12): ")
                if func_name not in ['f1', 'f14', 'f3', 'f12']:
                    print("Неверное имя операции!")
                    continue
                
                word1 = int(input("Номер первого слова (0-15): "))
                word2 = int(input("Номер второго слова (0-15): "))
                result_word = int(input("Номер слова для записи результата (0-15): "))
                
                if not (0 <= word1 <= 15 and 0 <= word2 <= 15 and 0 <= result_word <= 15):
                    print("Номера слов должны быть от 0 до 15!")
                    continue
                
                print("\nИсходные слова:")
                dm.display_word(word1)
                dm.display_word(word2)
                
                if dm.apply_logical_to_words(func_name, word1, word2, result_word):
                    print("\nРезультат записан в слово", result_word)
                    dm.display_word(result_word)
                    print("\nОбновленная матрица:")
                    dm.display_matrix()
                else:
                    print("Ошибка при выполнении операции!")
                
            except ValueError:
                print("Ошибка ввода! Вводите только числа от 0 до 15")
                
        elif choice == "4":
            while True:
                v_input = input("Введите значение V (000-111 в двоичном или 0-7 в десятичном): ").strip()
                try:
                    if len(v_input) == 3 and all(c in '01' for c in v_input):
                        v_value = int(v_input, 2)
                    else:
                        v_value = int(v_input)
                    if 0 <= v_value <= 7:
                        results = dm.sum_ab_for_v(v_value)
                        if results:
                            print(f"\nРезультаты для V={v_value:03b} ({v_value}):")
                            for i, _, sum_bits in results:
                                s_str = ''.join(str(int(b)) for b in sum_bits)
                                s_val = int(s_str, 2)
                                word = dm.get_word(i)
                                print(f"Слово {i:2d}: A={word['A']:04b} + B={word['B']:04b} = S={s_str} ({s_val})")
                            print("\nОбновленная матрица:")
                            dm.display_matrix()
                        else:
                            print(f"\nСлова с V={v_value:03b} не найдены")
                        break
                    else:
                        print("Ошибка: V должен быть от 000 до 111 (0-7)")
                except ValueError:
                    print("Ошибка: введите 3 бита (000-111) или число (0-7)")
                
        elif choice == "5":
            dm.display_matrix()
            
        elif choice == "0":
            print("Выход из программы")
            break
            
        else:
            print("Неверный выбор!")

if __name__ == "__main__":
    main()