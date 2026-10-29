from fetch import fetch_weather
from db import create_table, insert_weather


create_table()

data = fetch_weather()

print(data)

insert_weather(data)

print("Inserted.")
