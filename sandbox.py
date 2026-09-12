import requests
import sys
import datetime
import json

API_URL = "https://api.github.com/repos/python/cpython"
LOG_FILE = "api_log.jsonl"

def fetch_data(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status
        return response.json()
    except requests.exceptions.Timeout:
        print("Time is out")
        return None
    except requests.exceptions.HTTPError as e:
        print(f"Http error: {e}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None
    except json.JSONDecodeError:
        print("Response wasnt valid in JSON")
        return None

def log_entry(data):
    if data is None:
        return
    entry = {
        "timestamp": datetime.datetime.now().isoformat(),
        "repo": data.get("full name"),
        "stars": data.get("stargazers_count"),
        "open_issues": data.get("open_issues_count")
    }    
    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(entry) + "\n")
    print(f"Logged as {f}")

if __name__ == "__main__":
   data = fetch_data(API_URL)
   log_entry(data)