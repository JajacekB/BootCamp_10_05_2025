import psycopg2
import asyncio
import asyncpg


async def run():
    conn = await asyncpg.connect(
    host="localhost",
    port=5432,
    database="mydatabase",
    user="myuser",
    password="mypassword"
    )

    await conn.fetch("CREATE TABLE IF NOT EXISTS person(id SERIAL PRIMARY KEY, name TEXT);")
    await conn.execute("""
    INSERT INTO person (name) VALUES ($1)
    """, "Radek")
    await conn.close()

# loop = asyncio.get_event_loop()
# loop.run_until_complete(run())

if __name__ == '__main__':
    asyncio.run(run())