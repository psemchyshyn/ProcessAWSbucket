'''
Fully synchronous program
'''


import requests
import psycopg2
import ssl
import time
from collections import defaultdict 
from datetime import datetime
from typing import Any

FILES_LIST_URL = ""
BASE_URL = ""
PROCESSED_FILES = set()



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


def fetch_file_names(url: str) -> set:
    return set(requests.get(url, verify=False).text.split())


def fetch_file(url: str) -> list:
    return requests.get(url, verify=False).json()


def process_file(data: list, cur) -> None:
    elements = defaultdict(list)
    for element in data:
        if (typ := element["type"]) in INSERTIONS:
            elements[typ].append(element["data"])
    for typee, val in elements.items():
        INSERTIONS[typee](cur, val)


    # print("Count", count)
    # print(cur.execute("SELECT COUNT(*) FROM apps, movies, songs"))




def main():
    con = psycopg2.connect(database='AWSdata', user='postgres', password='postgres')
    cursor = con.cursor()
    processed_files = set()
    while True:
        obtained = fetch_file_names(FILES_LIST_URL)
        new = obtained - processed_files
        for file_name in new:
            process_file(fetch_file(BASE_URL + file_name), cursor)
            PROCESSED_FILES.add(file_name)
        break
    con.commit()
    cursor.close()
    con.close()



if __name__ == "__main__":
    start = time.time()
    main()
    print(len(PROCESSED_FILES))
    print(time.time() - start)
