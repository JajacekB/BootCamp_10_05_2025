import asyncio
import asyncpg

async def fetch_data():
    conn = await asyncpg.connect(
    host="localhost",
    port=5432,
    database="mydatabase",
    user="myuser",
    password="mypassword"
    )

    try:
        rows = await conn.fetch("SELECT * FROM person;")
        for row in rows:
            print(row)


        single_row = await conn.fetchrow("SELECT * FROM person WHERE id=$1;", 1)
        if single_row:
            print(f"Single ROW -> ID: {single_row['id']}, {single_row}")

    finally:
        await conn.close()


asyncio.run(fetch_data())