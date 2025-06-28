import asyncio
import time
import aiohttp


async def fetch(url, sesion, index):
    async with sesion.get(url, ssl=False) as response:
        text = await response.text()
        print(f"Text: {text}")

async def measure_aiohttp():
    url = "https://api.nbp.pl/api/exchangerates/rates/A/EUR/"
    task = []


    overall_start_time = time.time()

    async with aiohttp.ClientSession() as session:
        for i in range(100):
            task.append(fetch(url, session, i+1))


    overall_elapsed_time = time.time() - overall_start_time
    print(f"Overal time for 100 requests: {overall_elapsed_time:.4f} seconds.")


asyncio.run(measure_aiohttp())
