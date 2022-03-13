import psycopg2
from os import getenv
from time import sleep

def read_secrets():
    results = {}
    results["POSTGRES_DB"] = getenv("POSTGRES_DB")
    results["POSTGRES_USER"] = getenv("POSTGRES_USER")
    results["POSTGRES_PASSWORD"] = getenv("POSTGRES_PASSWORD")
    return results


def combine_data():
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
    cur.execute('''DROP TABLE IF EXISTS rescue_weather''')
    cur.execute('''CREATE TABLE rescue_weather(
        index BIGINT,
        id INTEGER,
        PRIMARY KEY (index, id),
        FOREIGN KEY (index) REFERENCES RESCUE_DATA(index),
        FOREIGN KEY (id) REFERENCES WEATHER_DATA(id)
    );''')

    cur.execute('''
    INSERT INTO rescue_weather (index, id)
        SELECT DISTINCT ON(rd.index) rd.index, wd.id
        FROM rescue_data AS rd
        LEFT JOIN weather_data AS wd
        ON TRUE
	    WHERE wd.ts BETWEEN rd.kohteessa - interval '1 hours' AND rd.kohteessa AND wd.fmisid = (
            SELECT ws.fmisid
            FROM weather_station AS ws
            ORDER BY ST_SetSRID(ST_MakePoint(rd."koordinaatit (lon)", rd."koordinaatit (lat)"), 4326) <#> ws.geom LIMIT 1
	);
    ''')

    conn.commit()
    conn.close()

    print("Combine data added")


