import time
import requests

url = "https://api.nbp.pl/api/exchangerates/rates/A/EUR/"

def multiple_requests():
    stat_time = time.time()
    for _ in range(100):
        r = requests.get(url)
        # print(r.json())

    elapset_time = time.time() - stat_time
    print(f"Request time: {elapset_time}")


multiple_requests()