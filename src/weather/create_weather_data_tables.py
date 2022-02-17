from venv import create
import psycopg2
from time import sleep
from os import getenv

def read_secrets():
    results = {}
    results["POSTGRES_DB"] = getenv("POSTGRES_DB")
    results["POSTGRES_USER"] = getenv("POSTGRES_USER")
    results["POSTGRES_PASSWORD"] = getenv("POSTGRES_PASSWORD")
    return results

def create_tables():
    connection_attempts = 0
    conn = None
    secrets = read_secrets()
    while connection_attempts < 3:
        try:
            connection_attempts += 1
            conn = psycopg2.connect(database = secrets["POSTGRES_DB"], user = secrets["POSTGRES_USER"], password = secrets["POSTGRES_PASSWORD"], host = "database", port = "5432")
            connection_attempts = 0
            break
        except psycopg2.OperationalError:
            # Service might not be fully up yet.
            sleep(2)
    if conn == None:
        assert(False) # Could not connect to database

    cur = conn.cursor()
    cur.execute('''DROP TABLE IF EXISTS WEATHER_DATA''')
    cur.execute('''CREATE TABLE WEATHER_DATA(
        id serial PRIMARY KEY,
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
        present_weather DECIMAL);''')

    print("Table created!")

    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_tables()
