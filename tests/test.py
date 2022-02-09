import psycopg2
from time import sleep
from os import getenv


def read_secrets():
    results = {}
    results["POSTGRES_DB"] = getenv("POSTGRES_DB")
    results["POSTGRES_USER"] = getenv("POSTGRES_USER")
    results["POSTGRES_PASSWORD"] = getenv("POSTGRES_PASSWORD")
    return results

def test_database():
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
    cur.execute('''DROP TABLE IF EXISTS TEST''')
    cur.execute('''CREATE TABLE TEST
    (ID INT PRIMARY KEY     NOT NULL,
    NAME           TEXT    NOT NULL);''')
    conn.commit()

    cur.execute("INSERT INTO TEST (ID,NAME) \
    VALUES (1, 'First')");
    cur.execute("INSERT INTO TEST (ID,NAME) \
    VALUES (2, 'Second')");
    conn.commit()

    cur.execute("SELECT * FROM TEST ORDER BY ID ASC")
    rows = cur.fetchall()
    assert(rows[0][0] == 1)
    assert(rows[1][1] == "Second")
    cur.execute('''DROP TABLE IF EXISTS TEST''')
    conn.commit()
    conn.close()
