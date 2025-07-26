import random
import time
import threading
import multiprocessing
from concurrent.futures import ThreadPoolExecutor

import numpy as np
from mistune.renderers.markdown import fenced_re

total_points_inside_circle = 0

# def monte_carlo_pi(n):
#     point_inside_circle = 0
#
#     for _ in range(n):
#         x = random.uniform(-1, 1)
#         y = random.uniform(-1, 1)
#
#         if x ** 2 + y **2 <= 1:
#             point_inside_circle += 1
#
#     return 4 * (point_inside_circle /n)


def monte_carlo_pi(num_sample):
    x = np.random.uniform(-1, 1, num_sample).astype(np.float32)
    y = np.random.uniform(-1, 1, num_sample).astype(np.float32)

    inside_circle = x ** 2 + y ** 2 <= 1
    num_inside_circle = np.sum(inside_circle)
    pi_estimate = 4 * num_inside_circle / num_sample

    return pi_estimate

def no_threads(iterations):
    start = time.time()
    pi = monte_carlo_pi(iterations)
    end = time.time()
    print(f"Bez wątku: {pi}, czas: {end - start}")

def with_treads(iterations):
    num_tread = 8
    iterations_per_treads = iterations // num_tread
    threads = []

    def thread_monte_carlo_pi():
        global total_points_inside_circle
        total_points_inside_circle_th = monte_carlo_pi(iterations_per_treads)
        with lock:
            total_points_inside_circle += total_points_inside_circle_th

    lock = threading.Lock()
    stat = time.time()
    for _ in range(num_tread):
        thread = threading.Thread(target=thread_monte_carlo_pi)
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    pi = (total_points_inside_circle / num_tread)
    end = time.time()
    print(f"Z watkami: {pi}, czas: {end - stat}")

def with_processes(iterations):
    num_processes = 8
    iterations_per_process = iterations // num_processes

    start = time.time()
    with multiprocessing.Pool(num_processes) as pool:
        result = pool.map(monte_carlo_pi, [iterations_per_process] * num_processes)

        pi = sum(result) / num_processes
        end = time.time()
        print(f"Z procesami: {pi}, czas {end - start}")


def with_thread_pool_executor(iterations):
    num_threads = 8
    iterations_per_thread = iterations // num_threads

    start = time.time()
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        result = list(executor.map(monte_carlo_pi, [iterations_per_thread] * num_threads))
        pi = sum(result) / num_threads

    end = time.time()
    print(f"Z ThreadPoolExecutor: {pi}, czas: {end - start}")






iterations = 50_000_000
if __name__ == '__main__':
    no_threads(iterations)
    with_treads(iterations)
    with_processes(iterations)
    with_thread_pool_executor(iterations)