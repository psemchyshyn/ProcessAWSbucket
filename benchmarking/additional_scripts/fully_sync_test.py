'''
Fully synchronous program
'''


import requests
import psycopg2
import ssl
import time
from collections import defaultdict 
import sys
import csv
import os
from typing import Any
from sync_inserts import INSERTIONS


BASE_URL = "https://data-engineering-interns.macpaw.io/"
FILES_LIST_URL = BASE_URL + "files_list.data"
DSN = os.environ.get('DATABASE_URI') # POSTGRES DATABASE server


def fetch_file_names(url: str) -> set:
    return set(requests.get(url).text.split())


def fetch_file(url: str) -> list:
    return requests.get(url).json()


def process_file(data: list, cur) -> None:
    elements = defaultdict(list)
    for element in data:
        if (typ := element["type"]) in INSERTIONS:
            elements[typ].append(element["data"])
    for typee, val in elements.items():
        INSERTIONS[typee](cur, val)


def test(n):
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
    for i in range(1, n + 1):
        start = time.time()
        obtained = fetch_file_names(FILES_LIST_URL)
        tasks = []
        for file_name in obtained:
            process_file(fetch_file(BASE_URL + file_name), cur)
        con.commit()
        end = time.time()
        results.append([i, len(obtained), end - start])
    con.close()

    with open("./benchmarking/fully_sync_results.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Launch id", "Files processed", "Time needed(in seconds)"])
        writer.writerows(results)


if __name__ == "__main__":
    requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)
    test(int(sys.argv[1]))
