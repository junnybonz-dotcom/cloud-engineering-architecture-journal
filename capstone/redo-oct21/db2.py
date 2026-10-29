import sqlite3

DB_PATH = "/home/ubuntu/capstone2/weather2.db"


def create_table():
    conn = sqlite3.connect(DB_PATH)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS weather_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fetched_at TEXT NOT NULL,
            temperature_c REAL,
            wind_speed_kmh REAL
        )
    """)

    conn.commit()
    conn.close()


def insert_weather(data):
    conn = sqlite3.connect(DB_PATH)

    conn.execute(
        """INSERT INTO weather_log
        (fetched_at, temperature_c, wind_speed_kmh)
        VALUES (?, ?, ?)""",
        (
            data["fetched_at"],
            data["temperature_c"],
            data["wind_speed_kmh"],
        ),
    )

    conn.commit()
    conn.close()
