import requests
import sqlite3

from fetch import fetch_weather
from db import create_table, insert_weather


def run_once():
    try:
        create_table()

        data = fetch_weather()

    except requests.exceptions.Timeout:
        print("API call timed out — skipping this run.")
        return

    except requests.exceptions.HTTPError as e:
        print(f"API returned an error status: {e}")
        return

    except requests.exceptions.RequestException as e:
        print(f"Network problem reaching the API: {e}")
        return

    except KeyError as e:
        print(f"API response was missing an expected field: {e}")
        return

    try:
        insert_weather(data)
        print(f"Logged: {data}")

    except sqlite3.Error as e:
        print(f"Database insert failed: {e}")


if __name__ == "__main__":
    run_once()
