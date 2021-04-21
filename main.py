import aiohttp
import asyncio
import asyncpg
import time
from collections import defaultdict
from db.init import init_schema, DSN
from db.inserts import INSERTIONS


PROCESSED_FILES = set()
FILES_LIST_URL = ""
BASE_URL = ""


async def fetch_file_names(url: str) -> set:
    async with aiohttp.ClientSession() as session:
        async with session.get(url, ssl=False) as response:
            return set((await response.text()).split())


async def fetch_file(url: str) -> list:
    async with aiohttp.ClientSession() as session:
        async with session.get(url, ssl=False) as response:
            return await response.json(content_type=None)
            

async def process_file(name: str, pool: asyncpg.Pool) -> None:
    data = await fetch_file(BASE_URL + name)
    elements = defaultdict(list)
    for element in data:
        if (typ := element["type"]) in INSERTIONS:
            elements[typ].append(element["data"])
    await asyncio.gather(*[asyncio.create_task(INSERTIONS[typee](pool, val)) for (typee, val) in elements.items()])
    PROCESSED_FILES.add(name)


async def main():
    await init_schema()
    start = time.time()
    async with asyncpg.create_pool(DSN) as pool:
        processed_files = set()
        while True:
            obtained = await fetch_file_names(FILES_LIST_URL)
            new = obtained - processed_files
            tasks = []
            for file_name in new:
                tasks.append(asyncio.create_task(process_file(file_name, pool)))
            await asyncio.gather(*tasks)
            break
    print(len(PROCESSED_FILES))
    print(time.time() - start)


if __name__ == "__main__":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
