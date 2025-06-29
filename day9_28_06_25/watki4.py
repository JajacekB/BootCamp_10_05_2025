import os
import time
from concurrent.futures import ProcessPoolExecutor


def worker(n):
    print(f"Proces: {n} w PID {os.getpid()}")
    time.sleep(1)

def main():
    with ProcessPoolExecutor(max_workers=5) as executor:
        for i in range(20):
            executor.submit(worker, i)

if __name__ == '__main__':
    main()