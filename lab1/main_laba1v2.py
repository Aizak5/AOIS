from laba1v2 import (
    input_int,
    input_float,
    int_to_binary,
    direct_to_additional,
    float_to_ieee754,
    ieee754_to_float,
    float_addition,
    binary_addition,
    binary_subtraction,
    binary_multiplication,
    binary_to_int,
    direct_to_reverse,
    binary_division
)

from typing import Tuple, List, Optional, Union
def print_operation(title: str, a: str, b: Optional[str] = None, operation: Optional[str] = None) -> str:
    output = f"\n--- {title} ---\n"
    if b is not None and operation is not None:
        if operation == '+':
            result = binary_addition(a, b)
            output += f"A: {a} ({binary_to_int(a)})\n"
            output += f"B: {b} ({binary_to_int(b)})\n"
            output += f"Результат сложения: {result} ({binary_to_int(result)})\n"
        elif operation == '-':
            result = binary_subtraction(a, b)
            output += f"A: {a} ({binary_to_int(a)})\n"
            output += f"B: {b} ({binary_to_int(b)})\n"
            output += f"Результат вычитания: {result} ({binary_to_int(result)})\n"
        elif operation == '*':
            result = binary_multiplication(a, b)
            output += f"A: {a} ({binary_to_int(a, False)})\n"
            output += f"B: {b} ({binary_to_int(b, False)})\n"
            output += f"Результат умножения: {result} ({binary_to_int(result, False)})\n"
        elif operation == '/':
            try:
                result = binary_division(a, b)
                sign = -1 if result[0] == '1' else 1
                num_parts = result[1:].split('.')
                int_part = int(num_parts[0], 2)
                frac_part = int(num_parts[1], 2) / (2 ** len(num_parts[1])) if len(num_parts) > 1 else 0
                decimal_result = sign * (int_part + frac_part)
                output += f"A: {a} ({binary_to_int(a, False)})\n"
                output += f"B: {b} ({binary_to_int(b, False)})\n"
                output += f"Результат деления: {result} ({decimal_result})\n"
            except ZeroDivisionError as e:
                output += f"Ошибка: {e}\n"
    else:
        a_bin = int_to_binary(a)
        output += f"Число: {a}\n"
        output += f"Прямой код: {a_bin}\n"
        output += f"Обратный код: {direct_to_reverse(a_bin)}\n"
        output += f"Дополнительный код: {direct_to_additional(a_bin)}\n"
    return output


def main() -> None:
    print("Лабораторная работа 1: Представление чисел в памяти компьютера")
    print("\nВведите два целых числа для операций:")
    num1 = input_int("Первое число: ")
    num2 = input_int("Второе число: ")
    a_direct = int_to_binary(num1)
    b_direct = int_to_binary(num2)
    a_additional = direct_to_additional(a_direct)
    b_additional = direct_to_additional(b_direct)
    
    print(print_operation(f"Представление числа {num1}", num1))
    print(print_operation(f"Представление числа {num2}", num2))
    
    print("\nОперации с целыми числами:")
    print(print_operation("Сложение в дополнительном коде", a_additional, b_additional, '+'))
    print(print_operation("Вычитание через сложение", a_additional, b_additional, '-'))
    print(print_operation("Умножение в прямом коде", a_direct, b_direct, '*'))
    print(print_operation("Деление в прямом коде", a_direct, b_direct, '/'))
    
    print("\nВведите два положительных числа с плавающей точкой:")
    float1 = input_float("Первое число: ")
    while float1 <= 0:
        print("Число должно быть положительным!")
        float1 = input_float("Первое число: ")
    float2 = input_float("Второе число: ")
    while float2 <= 0:
        print("Число должно быть положительным!")
        float2 = input_float("Второе число: ")
    
    a_ieee = float_to_ieee754(float1)
    b_ieee = float_to_ieee754(float2)
    sum_ieee = float_addition(a_ieee, b_ieee)
    
    print("\n--- Сложение чисел с плавающей точкой ---")
    print(f"A: {a_ieee} ({ieee754_to_float(a_ieee)})")
    print(f"B: {b_ieee} ({ieee754_to_float(b_ieee)})")
    print(f"Результат: {sum_ieee} ({ieee754_to_float(sum_ieee)})")


if __name__ == "__main__":
    main()
