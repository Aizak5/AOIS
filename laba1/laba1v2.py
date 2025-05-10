from typing import Tuple, List, Optional, Union

def input_int(prompt: str) -> int:
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("")

def input_float(prompt: str) -> float:
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Ошибка: введите число")

def int_to_binary(n: int, bits: int = 8) -> str:
    if n == 0:
        return '0' * bits
    sign = '1' if n < 0 else '0'
    n_abs = abs(n)
    binary = ''
    while n_abs > 0:
        binary = str(n_abs % 2) + binary
        n_abs = n_abs // 2
    binary = binary.zfill(bits - 1)
    return sign + binary

def direct_to_reverse(direct: str) -> str:
    if direct[0] == '0':
        return direct
    reverse = direct[0]
    for bit in direct[1:]:
        reverse += '1' if bit == '0' else '0'
    return reverse

def reverse_to_additional(reverse: str) -> str:
    if reverse[0] == '0':
        return reverse
    additional = list(reverse)
    carry = 1
    for i in range(len(additional)-1, 0, -1):
        if additional[i] == '0' and carry == 1:
            additional[i] = '1'
            carry = 0
            break
        elif additional[i] == '1' and carry == 1:
            additional[i] = '0'
    return ''.join(additional)

def direct_to_additional(direct: str) -> str:
    return reverse_to_additional(direct_to_reverse(direct))

def binary_to_int(binary_str: str, is_additional: bool = True) -> int:
    if not is_additional:
        sign = -1 if binary_str[0] == '1' else 1
        value = int(binary_str[1:], 2)
        return sign * value
    else:
        if binary_str[0] == '0':
            return int(binary_str, 2)
        inverted = ''.join('1' if bit == '0' else '0' for bit in binary_str[1:])
        return -(int(inverted, 2) + 1)

def binary_addition(a: str, b: str, input_bits: int = 8, output_bits: int = 16) -> str:
    a = a.zfill(input_bits)
    b = b.zfill(input_bits)
    a_ext = a[0] * (output_bits - input_bits) + a
    b_ext = b[0] * (output_bits - input_bits) + b
    result = []
    carry = 0
    for i in range(output_bits - 1, -1, -1):
        sum_bits = int(a_ext[i]) + int(b_ext[i]) + carry
        result.append(str(sum_bits % 2))
        carry = sum_bits // 2
    result = ''.join(reversed(result))
    return result[-output_bits:] 

def binary_subtraction(a: str, b: str, input_bits: int = 8, output_bits: int = 16) -> str:
    if len(b) == 0:
        return a.zfill(output_bits)
    inverted = ''.join('1' if bit == '0' else '0' for bit in b)
    neg_b = binary_addition(inverted, '1'.zfill(len(b)), len(b), len(b))
    return binary_addition(a, neg_b, input_bits, output_bits)

def binary_multiplication(a: str, b: str) -> str:
    a_sign = a[0]
    b_sign = b[0]
    a_val = a[1:]
    b_val = b[1:]
    product = '0'.zfill(len(a_val) + len(b_val))
    for i in range(len(b_val) - 1, -1, -1):
        if b_val[i] == '1':
            shifted_a = a_val + '0' * (len(b_val) - 1 - i)
            product = binary_addition(product, shifted_a, len(product), len(product))
    result_sign = '1' if a_sign != b_sign else '0'
    product = product.lstrip('0') or '0'
    result_len = len(a) + len(b) - 1
    product = product.zfill(result_len)
    return result_sign + product

def binary_division(dividend: str, divisor: str, precision: int = 5) -> str:
    result_sign = '1' if dividend[0] != divisor[0] else '0'
    a = dividend[1:]
    b = divisor[1:]
    if all(bit == '0' for bit in b):
        raise ZeroDivisionError("Division by zero")
    max_len = max(len(a), len(b))
    a = a.zfill(max_len)
    b = b.zfill(max_len)
    quotient = '0'
    remainder = '0' * max_len
    
    def is_greater_or_equal(a_bin: str, b_bin: str) -> bool:
        for a_bit, b_bit in zip(a_bin, b_bin):
            if a_bit > b_bit:
                return True
            elif a_bit < b_bit:
                return False
        return True
    
    for i in range(max_len):
        remainder = remainder[1:] + a[i]
        if is_greater_or_equal(remainder, b):
            remainder = binary_subtraction(remainder, b, max_len, max_len)
            quotient += '1'
        else:
            quotient += '0'
    
    fractional = ''
    for _ in range(precision):
        remainder = remainder[1:] + '0'
        if is_greater_or_equal(remainder, b):
            remainder = binary_subtraction(remainder, b, len(remainder), len(remainder))
            fractional += '1'
        else:
            fractional += '0'
    
    quotient = quotient.lstrip('0') or '0'
    result_value = quotient + ('.' + fractional if fractional else '')
    return result_sign + result_value

def float_to_ieee754(f: float) -> str:
    sign = '0' if f >= 0 else '1'
    f_abs = abs(f)
    if f_abs == 0:
        return sign + '0' * 31
    exponent = 0
    if f_abs >= 1:
        while f_abs >= 2:
            f_abs /= 2
            exponent += 1
    else:
        while f_abs < 1:
            f_abs *= 2
            exponent -= 1
    exponent_bias = exponent + 127
    exponent_bits = bin(exponent_bias)[2:].zfill(8)
    mantissa = f_abs - 1
    mantissa_bits = ''
    for _ in range(23):
        mantissa *= 2
        bit = '1' if mantissa >= 1 else '0'
        mantissa_bits += bit
        if mantissa >= 1:
            mantissa -= 1
    return sign + exponent_bits + mantissa_bits

def ieee754_to_float(ieee: str) -> float:
    sign = -1 if ieee[0] == '1' else 1
    exponent_bits = ieee[1:9]
    mantissa_bits = ieee[9:]
    if exponent_bits == '0' * 8:
        if mantissa_bits == '0' * 23:
            return 0.0 * sign
        exponent = -126
        mantissa = 0.0
        for i, bit in enumerate(mantissa_bits):
            mantissa += int(bit) * 2**(-i-1)
        return sign * mantissa * 2**exponent
    elif exponent_bits == '1' * 8:
        if mantissa_bits == '0' * 23:
            return float('inf') * sign
        else:
            return float('nan')
    exponent = int(exponent_bits, 2) - 127
    mantissa = 1.0
    for i, bit in enumerate(mantissa_bits):
        mantissa += int(bit) * 2**(-i-1)
    return sign * mantissa * 2**exponent

def float_addition(a: str, b: str) -> str:
    a_float = ieee754_to_float(a)
    b_float = ieee754_to_float(b)
    sum_float = a_float + b_float
    return float_to_ieee754(sum_float)