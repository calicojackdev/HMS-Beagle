import datetime
import requests
import os

import psycopg2 as pg
from dotenv import load_dotenv

load_dotenv()

db_name = os.environ["POSTGRES_DB_NAME"]
db_user = os.environ["POSTGRES_USER"]
db_pwd = os.environ["POSTGRES_PWD"]


def get_utc_now_timestamp_string() -> str:
    return (datetime.datetime.utcnow()).strftime("%Y-%m-%d %H:%M:%S")


def check_url(url: str, conn):
    response = requests.get(url)
    if response.status_code == 200:
        print(f"{url} is available, check site for updates")
    elif response.status_code == 404:
        print(f"{url} is not found. Updating db...")
        from queries import update_url_activity

        update_url_activity(conn, url, False)
    else:
        print(f"Request to {url} returned status code {response.status_code}")
    return


def connect_to_db():
    conn = pg.connect(f"dbname={db_name} user={db_user} password={db_pwd}")
    return conn
