import requests
import datetime

API_URL = "https://api.open-meteo.com/v1/forecast?latitude=10.3157&longitude=123.8854&current=temperature_2m,wind_speed_10m"


def fetch_weather():
    response = requests.get(API_URL, timeout=10)
    response.raise_for_status()

    raw = response.json()

    data = {
        "fetched_at": datetime.datetime.now().isoformat(),
        "temperature_c": raw["current"]["temperature_2m"],
        "wind_speed_kmh": raw["current"]["wind_speed_10m"],
    }

    return data


if __name__ == "__main__":
    result = fetch_weather()
    print(result)
