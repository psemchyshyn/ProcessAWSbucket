'''
Defines inserts functions to db
'''


from datetime import datetime
from typing import Any
from asyncpg import Pool


SONGS_INSERT_QUERY = "INSERT INTO songs(artist_name, title, year, release) VALUES($1, $2, $3, $4)"
MOVIES_INSERT_QUERY = "INSERT INTO movies(original_title, original_language, budget, is_adult, release_date) VALUES($1, $2, $3, $4, $5)"
APPS_INSERT_QUERY = "INSERT INTO apps(name, genre, rating, version, size_bytes) VALUES($1, $2, $3, $4, $5)"


async def insert_into_songs(pool: Pool, songs: list[dict[str, Any]]) -> None:
    data = [(song["artist_name"], song["title"], int(song["year"]), song["release"], ) for song in songs]
    async with pool.acquire() as conn:
        await conn.executemany(SONGS_INSERT_QUERY, data)


async def insert_into_movies(pool: Pool, movies: list[dict[str, Any]]) -> None:
    data = [(movie["original_title"], movie["original_language"], movie["budget"], movie["is_adult"], datetime.strptime(movie["release_date"], "%Y-%m-%d"), ) for movie in movies]
    async with pool.acquire() as conn:
        await conn.executemany(MOVIES_INSERT_QUERY, data)


async def insert_into_apps(pool: Pool, apps: list[dict[str, Any]]) -> None:
    data = [(app["name"], app["genre"], app["rating"], app["version"], app["size_bytes"], ) for app in apps]
    async with pool.acquire() as conn:
        await conn.executemany(APPS_INSERT_QUERY, data)


INSERTIONS = {
    "song": insert_into_songs,
    "movie": insert_into_movies,
    "app": insert_into_apps
}
