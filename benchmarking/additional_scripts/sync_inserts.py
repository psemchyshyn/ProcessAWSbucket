'''
Defining insert operations to database
'''


from datetime import datetime
from typing import Any

SONGS_INSERT_QUERY = "INSERT INTO songs(artist_name, title, year, release) VALUES(%s, %s, %s, %s)"
MOVIES_INSERT_QUERY = "INSERT INTO movies(original_title, original_language, budget, is_adult, release_date) VALUES(%s, %s, %s, %s, %s)"
APPS_INSERT_QUERY = "INSERT INTO apps(name, genre, rating, version, size_bytes) VALUES(%s, %s, %s, %s, %s)"


def insert_into_songs(cur, songs: list[dict[str, Any]]) -> None:
    data = [(song["artist_name"], song["title"], int(song["year"]), song["release"], ) for song in songs]
    cur.executemany(SONGS_INSERT_QUERY, data)


def insert_into_movies(cur, movies: list[dict[str, Any]]) -> None:
    data = [(movie["original_title"], movie["original_language"], movie["budget"], movie["is_adult"], datetime.strptime(movie["release_date"], "%Y-%m-%d"), ) for movie in movies]
    cur.executemany(MOVIES_INSERT_QUERY, data)


def insert_into_apps(cur, apps: list[dict[str, Any]]) -> None:
    data = [(app["name"], app["genre"], app["rating"], app["version"], app["size_bytes"], ) for app in apps]
    cur.executemany(APPS_INSERT_QUERY, data)


INSERTIONS = {
    "song": insert_into_songs,
    "movie": insert_into_movies,
    "app": insert_into_apps
}
