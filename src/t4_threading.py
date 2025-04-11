import json
import time
import random
import multiprocessing
from multiprocessing import Process, Queue, cpu_count
import concurrent.futures


def generate_data(n):
    return [random.randint(1, 1000) for _ in range(n)]


# Ищем простое число брутфорсом
def is_prime(n):
    """Проверяет, является ли число простым."""
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    w = 2
    while i * i <= n:
        if n % i == 0:
            return False
        i += w
        w = 6 - w
    return True


def process_number(number):
    factorial = 1
    for i in range(1, 1000):
        factorial *= i
    return (number, is_prime(number))


def single_thread(data):
    return [process_number(num) for num in data]


def variant_a(data):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        return list(executor.map(process_number, data))


def variant_b(data):
    with multiprocessing.Pool() as pool:
        return pool.map(process_number, data)


def variant_c(data):
    manager = multiprocessing.Manager()
    num_processes = cpu_count()
    task_queue = manager.Queue()
    result_queue = manager.Queue()

    for num in data:
        task_queue.put(num)

    for _ in range(num_processes):
        task_queue.put(None)

    processes = []
    for _ in range(num_processes):
        p = Process(target=worker, args=(task_queue, result_queue))
        p.start()
        processes.append(p)

    for p in processes:
        p.join()

    results = []
    while not result_queue.empty():
        results.append(result_queue.get())

    return results


def worker(task_queue, result_queue):
    while True:
        number = task_queue.get(timeout=1)
        if number is None:
            break
        result = process_number(number)
        result_queue.put(result)


def save_results(results, filename):
    with open(filename, "w") as f:
        json.dump([{"number": num, "is_prime": is_p} for num, is_p in results], f)


if __name__ == "__main__":
    data_size = 100000
    data = generate_data(data_size)

    # Используем один поток
    start = time.time()
    results_single = single_thread(data)
    time_single = time.time() - start

    # Пул потоков
    start = time.time()
    results_a = variant_a(data)
    time_a = time.time() - start

    #  multiprocessing.Pool
    start = time.time()
    results_b = variant_b(data)
    time_b = time.time() - start

    # multiprocessing.Pool + очереди
    start = time.time()
    results_c = variant_c(data)
    time_c = time.time() - start

    save_results(results_single, "results_single.json")
    save_results(results_a, "results_a.json")
    save_results(results_b, "results_b.json")
    save_results(results_c, "results_c.json")

    print(f"Однопоточное выполнение: {time_single:.2f} сек")
    print(f"Пул потоков: {time_a:.2f} сек")
    print(f"Пул процессов: {time_b:.2f} сек")
    print(f"Отдельные процессы и очереди: {time_c:.2f} сек")
