import asyncpg


async def init_schema(DSN: str) -> None:
    try:
        conn = await asyncpg.connect(DSN)
        with open("db/schema.sql", "r") as file:
            await conn.execute(file.read()) 
    except Exception as e:
        print(e)
