
def get_stations_data():
    stations = [[100971, 60.18, 24.94], [101421, 62.32, 27.91],  [101311, 61.52, 23.75]]

    stations_data = []

    for l in stations:
        d = {}
        d["fmisid"] = l[0]
        d["lat"] = l[1]
        d["lon"] = l[2]

        stations_data.append(d)
    
    return stations_data


def add_stations(conn):
    stations_data = get_stations_data()

    cur = conn.cursor()
    
    cur.executemany('''INSERT INTO weather_station VALUES (%(fmisid)s , %(lat)s, %(lon)s, ST_SetSRID(ST_MakePoint(%(lon)s, %(lat)s), 4326))''', stations_data)

    conn.commit()

    print("Added weather stations")
