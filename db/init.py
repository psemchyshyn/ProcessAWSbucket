import asyncpg


DSN = ""


async def init_schema() -> None:
    try:
        conn = await asyncpg.connect(DSN)
        with open("db/schema.sql", "r") as file:
            await conn.execute(file.read()) 
    except Exception as e:
        print("Couldn't initialize schema")
        print(e)
