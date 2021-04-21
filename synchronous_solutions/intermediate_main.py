'''
Async web requests + sync db requests
DATABASE schema is expected to be initialized
'''
import aiohttp
import aiopg
import psycopg2
import asyncio
import time
from collections import defaultdict
from sync_main import INSERTIONS


FILES_LIST_URL = ""
BASE_URL = ""
PROCESSED_FILES = set()


async def fetch_file_names(url: str) -> set:
    async with aiohttp.ClientSession() as session:
        async with session.get(url, ssl=False) as response:
            return set((await response.text()).split())


async def fetch_file(url: str) -> list:
    async with aiohttp.ClientSession() as session:
        async with session.get(url, ssl=False) as response:
            return await response.json(content_type=None)
            

async def process_file(url: str, cur) -> None:
    data = await fetch_file(url)
    elements = defaultdict(list)
    for element in data:
        if (typ := element["type"]) in INSERTIONS:
            elements[typ].append(element["data"])
    for typee, val in elements.items():
        INSERTIONS[typee](cur, val)
    PROCESSED_FILES.add(url)


async def main():
    con = psycopg2.connect(database='AWSdata', user='postgres', password='postgres')
    cur = con.cursor()
    while True:
        obtained = await fetch_file_names(FILES_LIST_URL)
        new = obtained - PROCESSED_FILES
        tasks = []
        for file_name in new:
            tasks.append(asyncio.create_task(process_file(BASE_URL + file_name, cur)))
        await asyncio.gather(*tasks)
        break # to be removed in final
    con.commit()
    cur.close()
    con.close()


if __name__ == "__main__":
    start = time.time()
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
    print(len(PROCESSED_FILES)) # remove soon
    print(time.time() - start)