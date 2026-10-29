import datetime
import requests

API_URL = (
    "https://api.open-meteo.com/v1/forecast"
    "?latitude=14.6&longitude=121.0"
    "&current=temperature_2m,wind_speed_10m"
)


def fetch_weather():
    response = requests.get(API_URL, timeout=10)
    response.raise_for_status()

    raw = response.json()

    return {
        "fetched_at": datetime.datetime.now().isoformat(),
        "temperature_c": raw["current"]["temperature_2m"],
        "wind_speed_kmh": raw["current"]["wind_speed_10m"],
    }


if __name__ == "__main__":
    print(fetch_weather())
