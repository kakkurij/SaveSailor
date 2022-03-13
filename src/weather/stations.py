import psycopg2
from create_weather_data_tables import read_secrets
from time import sleep

# statios_data = [[100996, 60.11, 24.98], [101421, 62.32, 27.91], [101800, 64.5, 26.42], [101958, 67.02, 27.22] [101311, 61.52, 23.75]]
stations = [[100971, 60.18, 24.94], [101421, 62.32, 27.91],  [101311, 61.52, 23.75]]

stations_data = []

for l in stations:
    d = {}
    d["fmisid"] = l[0]
    d["lat"] = l[1]
    d["lon"] = l[2]

    stations_data.append(d)


def add_stations():
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

    cur.execute('''DROP TABLE IF EXISTS weather_station CASCADE''')

    cur.execute('''CREATE TABLE weather_station(
        fmisid INT PRIMARY KEY,
        lat DOUBLE PRECISION,
        lon DOUBLE PRECISION,
        geom GEOMETRY(Point, 4326)
    );''')

    cur.executemany('''INSERT INTO weather_station VALUES (%(fmisid)s , %(lat)s, %(lon)s, ST_SetSRID(ST_MakePoint(%(lon)s, %(lat)s), 4326))''', stations_data)

    conn.commit()
    conn.close()

    print("Added weather stations")
