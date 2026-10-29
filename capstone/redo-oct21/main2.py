import sqlite3
import requests

from fetch import fetch_weather
from db2 import create_table, insert_weather


def run_once():
    create_table()

    try:
        data = fetch_weather()

    except requests.exceptions.Timeout:
        print("API call timed out, skipping this run.")
        return

    except requests.exceptions.RequestException as e:
        print(f"API request failed: {e}")
        return

    except KeyError as e:
        print(f"API response was missing a field: {e}")
        return

    try:
        insert_weather(data)
        print(f"Logged: {data}")

    except sqlite3.Error as e:
        print(f"Database insert failed: {e}")


if __name__ == "__main__":
    run_once()
