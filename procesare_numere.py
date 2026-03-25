import math

def is_prime(n):
    if n < 2: return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0: return False
    return True

def filter_odd_task(input_list, queue):
    res = [x for x in input_list if x % 2 != 0]
    queue.put(f"Impare: {res}")

def filter_prime_task(input_list, queue):
    res = [x for x in input_list if is_prime(x)]
    queue.put(f"Prime: {res}")

def sum_numbers_task(input_list, queue):
    res = sum(input_list)
    queue.put(f"Suma: {res}")