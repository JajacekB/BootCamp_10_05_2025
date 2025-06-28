from concurrent.futures import ProcessPoolExecutor

def worker(i):
    print(f"proces: {i}")

print(__name__)

if __name__ == '__main__':
    with ProcessPoolExecutor(max_workers=5) as executor:
        for i in range(20):
            executor.submit(worker, 1)
