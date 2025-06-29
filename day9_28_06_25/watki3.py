from concurrent.futures import ProcessPoolExecutor
import os

def worker(i):
    print(f"Proces: {i} w PID {os.getpid()}")


print(__name__)  # __mp_main__

if __name__ == '__main__':
    with ProcessPoolExecutor(max_workers=5) as executor:
        for i in range(20):
            executor.submit(worker, i)
