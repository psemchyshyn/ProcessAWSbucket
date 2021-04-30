'''
Async web requests + sync db requests
DATABASE schema is expected to be initialized
'''
import aiohttp
import aiopg
import psycopg2
import asyncio
import time
import csv
import sys
from collections import defaultdict
from sync_inserts import INSERTIONS


BASE_URL = "https://data-engineering-interns.macpaw.io/"
FILES_LIST_URL = BASE_URL + "files_list.data"
DSN = os.environ.get('DATABASE_URI') # POSTGRES DATABASE server


async def fetch_file_names(url: str) -> set:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return set((await response.text()).split())


async def fetch_file(url: str) -> list:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json(content_type=None)
            

async def process_file(name: str, cur) -> None:
    data = await fetch_file(BASE_URL + name)
    elements = defaultdict(list)
    for element in data:
        if (typ := element["type"]) in INSERTIONS:
            elements[typ].append(element["data"])
    for typee, val in elements.items():
        INSERTIONS[typee](cur, val)


async def test(n):
    con = psycopg2.connect(DSN)
    # init schema
    cur = con.cursor()
    with open("./db/schema.sql") as file:
        try:
            cur.execute(file.read())
        except Exception as e:
            print(e)
        finally:
            con.commit()

    results = []
    for i in range(1, n + 1): # note here we process all files again (for benchmarking)
        start = time.time()
        obtained = await fetch_file_names(FILES_LIST_URL)
        tasks = []
        for file_name in obtained:
            tasks.append(asyncio.create_task(process_file(file_name, cur)))
        await asyncio.gather(*tasks)
        con.commit()
        end = time.time()
        results.append([i, len(obtained), end - start])
    con.close()

    with open("./benchmarking/partially_sync_results.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Launch id", "Files processed", "Time needed(in seconds)"])
        writer.writerows(results)


if __name__ == "__main__":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(test(int(sys.argv[1]))) # launch program n number of times, given from command line args
