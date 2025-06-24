import multiprocessing
import math
import time
from typing import List


def is_prime(n: int) -> bool:
    if n <= 1:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    
    max_divisor = math.isqrt(n) + 1
    for d in range(3, max_divisor, 2):
        if n % d == 0:
            return False
    return True


def find_primes_in_range(start: int, end: int, result: List[int]) -> None:
    primes = []
    for num in range(start, end + 1):
        if is_prime(num):
            primes.append(num)
    result.extend(primes)


def main():
    print("Программа для поиска простых чисел  использованием мультипроцессинга")

    while True:
        try:
            max_num = int(input("Введите верхнюю границу для поиска простых чисел (>=2): "))
            if max_num >= 2:
                break
            print("Число должно быть больше или равно 2.")
        except ValueError:
            print("Пожалуйста, введите целое число.")

    cpu_count = multiprocessing.cpu_count()
    print(f"\nДоступно ядер процессора: {cpu_count}")
    
    while True:
        try:
            num_processes = int(input(f"Введите количество процессов (1-{cpu_count}): "))
            if 1 <= num_processes <= cpu_count:
                break
            print(f"Число процессов должно быть от 1 до {cpu_count}.")
        except ValueError:
            print("Пожалуйста, введите целое число.")

    range_size = max_num // num_processes
    ranges = []
    for i in range(num_processes):
        start = i * range_size + 1
        end = (i + 1) * range_size if i != num_processes - 1 else max_num
        ranges.append((start, end))
    
    print("\nРаспределение диапазонов по процессам:")
    for i, (start, end) in enumerate(ranges):
        print(f"Процесс {i+1}: от {start} до {end}")

    manager = multiprocessing.Manager()
    prime_numbers = manager.list()
    
    processes = []
    start_time = time.time()
    
    for start, end in ranges:
        p = multiprocessing.Process(
            target=find_primes_in_range,
            args=(start, end, prime_numbers)
        )
        processes.append(p)
        p.start()
    
    for p in processes:
        p.join()
    
    end_time = time.time()
    
    prime_numbers = sorted(list(prime_numbers))
    
    print("\nРезультаты:")
    print(f"Найдено простых чисел: {len(prime_numbers)}")
    print(f"Время выполнения: {end_time - start_time:.4f} секунд")
    
    show_primes = input("Показать все простые числа? (y/n): ").lower()
    if show_primes == 'y':
        print("\nСписок простых чисел:")
        print(prime_numbers)


if __name__ == '__main__':
    main()