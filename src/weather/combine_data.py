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
    cur.execute('''DROP TABLE IF EXISTS RESCUE_WEATHER''')
    cur.execute('''CREATE TABLE RESCUE_WEATHER(
        index BIGINT,
        id INTEGER,
        PRIMARY KEY (index, id),
        FOREIGN KEY (index) REFERENCES RESCUE_DATA(index),
        FOREIGN KEY (id) REFERENCES WEATHER_DATA(id)
    );''')

    print("RESCUE_WEATHER created")

    cur.execute('''
        INSERT INTO RESCUE_WEATHER (index, id)
        SELECT rd.index, wd.id
        FROM RESCUE_DATA AS rd
        LEFT JOIN  WEATHER_DATA AS wd
        ON TRUE
        WHERE wd.ts BETWEEN rd.kohteessa - interval '1 hours' AND rd.kohteessa
    ''')

    conn.commit()
    conn.close()


