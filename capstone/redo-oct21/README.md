# Weather Logger — Guided Rebuild

A rebuilt version of the Weather Logger pipeline, created in a separate project folder and tested on an Ubuntu AWS EC2 instance. It fetches current weather data from the Open-Meteo API, selects temperature and wind speed, and stores timestamped readings in SQLite.

This was a **guided recovery and rebuild**, not a completely independent cold attempt. The accompanying [GAPS.md](GAPS.md) records where I needed help and what I plan to practice independently.

## Skills Practiced

- Linux command-line navigation and virtual environments
- Python functions, dictionaries, HTTP requests, and JSON
- SQLite table creation and parameterized inserts
- Exception handling for API and database operations
- Cron scheduling and log redirection
- SQL aggregation with `GROUP BY`
- Git version control and comparison with an earlier implementation

## Architecture

```text
Open-Meteo API
      |
      v
   fetch.py
      |
      v
 Python dictionary
      |
      v
    db2.py
      |
      v
 weather2.db
      ^
      |
   main2.py
      ^
      |
 Cron automation
```

## Project Files

| File | Purpose |
|---|---|
| `fetch.py` | Requests weather data and returns a dictionary containing a timestamp, temperature, and wind speed. |
| `db2.py` | Creates the SQLite table and inserts readings using SQL placeholders. |
| `main2.py` | Coordinates fetching, database insertion, and error reporting. |
| `GAPS.md` | Records what I remembered, where I needed guidance, and what needs further practice. |
| `COMPARISON.patch` | Stores a text comparison between the original scripts and the rebuild. |

## Requirements

- Python 3
- The `requests` package
- Internet access for the public weather API
- SQLite support, included with Python's standard library when available

## How to Run

The tested deployment uses `/home/ubuntu/capstone2`, because `db2.py` defines an absolute database path:

```text
/home/ubuntu/capstone2/weather2.db
```

For a fresh Ubuntu deployment, place the three Python scripts in that directory. From the repository root, the following commands copy the archived rebuild into the deployment directory; use a new or empty directory to avoid overwriting existing work.

```bash
mkdir -p /home/ubuntu/capstone2
cp capstone/redo-oct21/fetch.py \
   capstone/redo-oct21/db2.py \
   capstone/redo-oct21/main2.py \
   /home/ubuntu/capstone2/

cd /home/ubuntu/capstone2
python3 -m venv env
source env/bin/activate
python3 -m pip install requests
python3 -m py_compile fetch.py db2.py main2.py
python3 main2.py
```

The project has been tested on the existing EC2 deployment. Running it from a different directory requires adapting the database path.

## Real Output Example

Captured from a successful run on October 27, 2026:

```text
Logged: {'fetched_at': '2026-10-27T15:44:16.627880', 'temperature_c': 28.5, 'wind_speed_kmh': 0.5}
```

This confirms that the script received the API response and logged the selected values. Weather values change between requests.

## Database and SQL

Each successful run inserts a row into `weather_log` in `weather2.db`.

Example query to summarize readings by hour:

```sql
SELECT
    strftime('%H', fetched_at) AS hour,
    COUNT(*) AS readings,
    ROUND(AVG(temperature_c), 1) AS average_temp
FROM weather_log
GROUP BY hour
ORDER BY hour;
```

This groups readings by hour, counts them, and calculates the average temperature for each group.

## Error Handling

The current implementation handles these conditions:

- API timeouts
- HTTP and other request failures
- Missing JSON fields
- SQLite errors during insertion

One limitation remains: table creation occurs outside the error-handling blocks in `main2.py`, so a table-creation error may still produce a traceback.

## Automation

The tested EC2 deployment runs the script every 15 minutes using cron. The schedule uses the virtual environment's Python interpreter and redirects output and errors to `cron2.log`.

Check the existing crontab before adding a schedule to avoid duplicate jobs.

## What I Learned

The rebuild helped me reconnect Linux commands, Python, API requests, SQLite, exception handling, and cron into one working pipeline. I needed guidance with database functions, coordinating the scripts, and configuring scheduled execution.

The purpose of the rebuild is not to claim perfect recall. It is to identify gaps honestly and make the next practice session more targeted.

See [GAPS.md](GAPS.md) for the gap report and [COMPARISON.patch](COMPARISON.patch) for the original-versus-rebuild comparison.
