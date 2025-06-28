import asyncio
import httpx


url = "https://naukajava.online"

async def fetch(client, i):
    resp = await client.get(url)
    print(f"{i + 1}: status code: {resp.status_code}")


async def main():
    async with httpx.AsyncClient() as client:
        tasks = [fetch(client, i) for i in range(10)]
        await asyncio.gather(*tasks)



asyncio.run(main())