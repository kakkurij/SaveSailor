import psycopg2
from time import sleep


def test_database():
    connection_attempts = 0
    conn = None
    while connection_attempts < 3:
        try:
            connection_attempts += 1
            conn = psycopg2.connect(database="savesailor_database", user = "username", password = "password", host = "database", port = "5432")
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
