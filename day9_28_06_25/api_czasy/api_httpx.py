import time
import httpx
import asyncio


url = "https://api.nbp.pl/api/exchangerates/rates/A/EUR/"


async def fetch_data(client, url, index):
    start_time = time.time()
    response = await client.get(url)
    elapsed_time = time.time() - start_time
    print(f"Request {index}: Status {response.status_code}, Time: {elapsed_time:.4f} s.")

    try:
        json_data = response.json()
        print(f"Request {index}: {json_data}")
    except httpx.HTTPStatusError as e:
        print(f"Request {index}: Failed with status: {response.status_code}:", e)
    except Exception as e:
        print(f"Request {index}: Error {e}")


async def multiple_https():
    stat_time = time.time()
    async with httpx.AsyncClient() as client:
        task = [fetch_data(client, url, i +1) for i in range(100)]
        await asyncio.gather(*task)

    elapsed = time.time() - stat_time
    print(f"HTTPX total time: {elapsed:.4f}")

asyncio.run(multiple_https())
