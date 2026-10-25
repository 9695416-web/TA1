import math

WORDS = ["ХТО", "ЛЮДЯМ", "ДОБРА", "БАЖАЄ", "ТОЙ", "І", "СОБІ", "МАЄ"]

UKR_ALPHABET = {
    'А': 1,  'Б': 2,  'В': 3,  'Г': 4,  'Ґ': 5,  'Д': 6,  'Е': 7,  'Є': 8,
    'Ж': 9,  'З': 10, 'И': 11, 'І': 12, 'Ї': 13, 'Й': 14, 'К': 15, 'Л': 16,
    'М': 17, 'Н': 18, 'О': 19, 'П': 20, 'Р': 21, 'С': 22, 'Т': 23, 'У': 24,
    'Ф': 25, 'Х': 26, 'Ц': 27, 'Ч': 28, 'Ш': 29, 'Щ': 30, 'Ь': 31, 'Ю': 32,
    'Я': 33
}

A_CONST = (math.sqrt(5) - 1) / 2

def calculate_key(word: str) -> int:
    return sum(UKR_ALPHABET.get(char, 0) for char in word.upper())

def hash_division(k: int, m: int = 13) -> int:
    return k % m

def hash_multiplication(k: int, m: int = 16) -> int:
    product = k * A_CONST
    fractional_part = product - math.floor(product)
    return math.floor(m * fractional_part)

def build_open_table(words: list, m: int, hash_func) -> list:
    table = [[] for _ in range(m)]
    for word in words:
        addr = hash_func(calculate_key(word))
        table[addr].append(word)
    return table

def build_closed_table(words: list, m: int, hash_func) -> list:
    table = [None] * m
    for word in words:
        start_addr = hash_func(calculate_key(word))
        for i in range(m):
            addr = (start_addr + i) % m
            if table[addr] is None:
                table[addr] = word
                break
        else:
            raise OverflowError(f"Хеш-таблиця переповнена при додаванні '{word}'")
    return table

def search_comparisons_open(table: list, word: str, hash_func) -> int:
    addr = hash_func(calculate_key(word))
    chain = table[addr]
    for idx, item in enumerate(chain):
        if item == word:
            return idx + 1
    return len(chain)

def search_comparisons_closed(table: list, word: str, m: int, hash_func) -> int:
    start_addr = hash_func(calculate_key(word))
    for i in range(m):
        addr = (start_addr + i) % m
        if table[addr] == word or table[addr] is None:
            return i + 1
    return m

if __name__ == "__main__":

    print("1. РОЗРАХУНОК КЛЮЧІВ ТА ХЕШ-ЗНАЧЕНЬ СЛІВ")

    print(f"{'№':<3} | {'Слово':<8} | {'Ключ K':<8} | {'h1 (mod 13)':<12} | {'h2 (mult 16)':<12}")

    for i, w in enumerate(WORDS, 1):
        k = calculate_key(w)
        h1 = hash_division(k, 13)
        h2 = hash_multiplication(k, 16)
        print(f"{i:<3} | {w:<8} | {k:<8} | {h1:<12} | {h2:<12}")

    open_t13 = build_open_table(WORDS, 13, lambda k: hash_division(k, 13))
    open_t16 = build_open_table(WORDS, 16, lambda k: hash_multiplication(k, 16))
    closed_t13 = build_closed_table(WORDS, 13, lambda k: hash_division(k, 13))
    closed_t16 = build_closed_table(WORDS, 16, lambda k: hash_multiplication(k, 16))


    print("2. ВІДОБРАЖЕННЯ ТАБЛИЦЬ (M = 13)")

    print(" Відкрита таблиця (ланцюжки) ")
    for idx, chain in enumerate(open_t13):
        print(f"[{idx:02d}]: {' -> '.join(chain) if chain else '(порожньо)'}")

    print("\n Закрита таблиця (відкрита адресація) ")
    for idx, val in enumerate(closed_t13):
        print(f"[{idx:02d}]: {val if val is not None else '(NULL)'}")


    print("3. СТАТИСТИКА ПОРІВНЯНЬ ДЛЯ УСПІШНОГО ПОШУКУ")

    print(f"{'Слово':<8} | {'Open-13':<8} | {'Close-13':<8} | {'Open-16':<8} | {'Close-16':<8}")


    total_o13 = total_c13 = total_o16 = total_c16 = 0
    for w in WORDS:
        c_o13 = search_comparisons_open(open_t13, w, lambda k: hash_division(k, 13))
        c_c13 = search_comparisons_closed(closed_t13, w, 13, lambda k: hash_division(k, 13))
        c_o16 = search_comparisons_open(open_t16, w, lambda k: hash_multiplication(k, 16))
        c_c16 = search_comparisons_closed(closed_t16, w, 16, lambda k: hash_multiplication(k, 16))

        total_o13 += c_o13
        total_c13 += c_c13
        total_o16 += c_o16
        total_c16 += c_c16

        print(f"{w:<8} | {c_o13:<8} | {c_c13:<8} | {c_o16:<8} | {c_c16:<8}")

    n = len(WORDS)
    print("-" * 60)
    print(f"{'Середнє':<8} | {total_o13/n:<8.3f} | {total_c13/n:<8.3f} | {total_o16/n:<8.3f} | {total_c16/n:<8.3f}")
