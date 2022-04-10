import psycopg2
from time import sleep
from os import getenv

from weather.stations import add_stations


def read_secrets():
    results = {}
    results["POSTGRES_DB"] = getenv("POSTGRES_DB")
    results["POSTGRES_USER"] = getenv("POSTGRES_USER")
    results["POSTGRES_PASSWORD"] = getenv("POSTGRES_PASSWORD")
    return results


def create_connection():
    connection_attempts = 0
    conn = None
    secrets = read_secrets()
    while connection_attempts < 3:
        try:
            connection_attempts += 1
            conn = psycopg2.connect(
                database=secrets["POSTGRES_DB"],
                user=secrets["POSTGRES_USER"],
                password=secrets["POSTGRES_PASSWORD"],
                host="database",
                port="5432")
            connection_attempts = 0
            break
        except psycopg2.OperationalError:
            # Service might not be fully up yet.
            sleep(2)
    if conn is None:
        assert(False)   # Could not connect to database

    return conn


def drop_all_tables(conn):
    cur = conn.cursor()

    cur.execute('''DROP TABLE IF EXISTS rescue_weather CASCADE''')
    cur.execute('''DROP TABLE IF EXISTS weather_station CASCADE''')
    cur.execute('''DROP TABLE IF EXISTS weather_data CASCADE''')

    print("Dropped all weather tables")

    conn.commit()


def create_tables(conn):
    cur = conn.cursor()

    cur.execute('''CREATE TABLE weather_station(
        fmisid INT PRIMARY KEY,
        lat DOUBLE PRECISION,
        lon DOUBLE PRECISION,
        geom GEOMETRY(Point, 4326)
    );''')

    print("weather_station table created!")

    cur.execute('''CREATE TABLE weather_data(
        id SERIAL PRIMARY KEY,
        fmisid INTEGER,
        ts TIMESTAMP,
        air_temperature DECIMAL,
        wind_speed DECIMAL,
        gust_speed DECIMAL,
        wind_direction DECIMAL,
        relative_humidity DECIMAL,
        dew_point_temperature DECIMAL,
        precipitation_amount DECIMAL,
        precipitation_intensity DECIMAL,
        snow_depth DECIMAL,
        pressure_msl DECIMAL,
        horizontal_visibility DECIMAL,
        cloud_amount DECIMAL,
        present_weather DECIMAL,
        FOREIGN KEY (fmisid) REFERENCES weather_station(fmisid)
        );''')

    print("weather_data table created!")

    cur.execute('''CREATE TABLE rescue_weather(
        index BIGINT,
        id INTEGER,
        PRIMARY KEY (index, id),
        FOREIGN KEY (index) REFERENCES RESCUE_DATA(index),
        FOREIGN KEY (id) REFERENCES WEATHER_DATA(id)
    );''')

    print("rescue_weather table created!")

    conn.commit()


def setup_weather_database(conn):
    drop_all_tables(conn)
    create_tables(conn)
    add_stations(conn)
