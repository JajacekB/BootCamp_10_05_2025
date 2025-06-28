import threading

def thread_id():
    print("Thread id: ", threading.get_ident())


def worker(number):
    print(f"Worker number {number}")



threads = []
for i in range(5):
    t = threading.Thread(target=worker, args=(i,))
    threads.append(t)
    t.start()

