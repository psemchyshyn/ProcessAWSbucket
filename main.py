'''
Entry point to the program of processing AWS bucket
'''


import aiohttp
import asyncio
import asyncpg
import os
from collections import defaultdict
from db.init import init_schema
from db.inserts import INSERTIONS


BASE_URL = "https://data-engineering-interns.macpaw.io/"
FILES_LIST_URL = BASE_URL + "files_list.data"
DSN = os.environ.get('DATABASE_URI') # POSTGRES DATABASE server

PROCESSED_FILES = set()


async def fetch_file_names(url: str) -> set:
    '''
    Extracts a set of all filenames currently available
    '''
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return set((await response.text()).split())


async def fetch_file(url: str) -> list:
    '''
    Get single file 
    '''
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json(content_type=None) # to disable the check of possible incorrect server repsonse 
            

async def process_file(name: str, pool: asyncpg.Pool) -> None:
    '''
    Awaits for the file. Then, groups all objects by their type
    and feeds those groups(lists) to the corresponding insertion functions  
    '''
    data = await fetch_file(BASE_URL + name)
    objects = defaultdict(list)
    for element in data:
        if (typ := element["type"]) in INSERTIONS: # = if the object type is song, movie or app
            objects[typ].append(element["data"])
    await asyncio.gather(*[asyncio.create_task(INSERTIONS[typee](pool, val)) for (typee, val) in objects.items()])
    PROCESSED_FILES.add(name)


async def main():
    '''
    Entry point to the program. 
    Initializes db schema and starts processing
    '''
    await init_schema(DSN)
    async with asyncpg.create_pool(DSN) as pool:
        while True:
            obtained = await fetch_file_names(FILES_LIST_URL)
            unprocessed = obtained - PROCESSED_FILES
            await asyncio.gather(*[process_file(filename, pool) for filename in unprocessed])


if __name__ == "__main__":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())


# TODO add normalization field trigger/function + env varaibles + docker + sync solutions correction + time plot

# Remove time import, make while true