import json
from pathlib import Path


def get_stations_data():
    stations_path = Path(__file__).parent.joinpath("weather_stations.json")

    with open(stations_path) as f:
        stations = json.load(f)

    return stations


def add_stations(conn):
    stations_data = get_stations_data()

    cur = conn.cursor()

    cur.executemany(
        '''
        INSERT INTO weather_station
        VALUES (%(fmisid)s, %(name)s, %(lat)s, %(lon)s,
        ST_SetSRID(ST_MakePoint(%(lon)s, %(lat)s), 4326))
        ''',
        stations_data)

    conn.commit()

    print("Added weather stations")
