
def get_stations_data():

    # Name, id, lat, lon
    # Note that not all stations have all data. This may cause that the
    # station is closest, but the data doesn't
    # include temperatures for example.
    stations = [
        ["Varkaus Kosulanniemi", 101421, 62.32, 27.91],
        ["Tampere Siilinkari", 101311, 61.52, 23.75],
        ["Helsinki Harmaja", 100996, 60.11, 24.98],
        ["Lappeenranta Hiekkapakka", 101252, 61.2, 28.47],
        ["Turku Rajakari ", 100947, 60.38, 	22.1],
        ["Kemiönsaari Vänö ", 100945, 59.87, 22.19],
        ["Hanko Russarö ", 100932, 59.77, 22.95],
        ["Hailuoto Marjaniemi", 101784, 65.04, 24.56],
        ["Kuopio Ritoniemi", 101580, 62.8, 27.9]
    ]

    stations_data = []

    for station in stations:
        d = {}
        d["name"] = station[0]
        d["fmisid"] = station[1]
        d["lat"] = station[2]
        d["lon"] = station[3]

        stations_data.append(d)

    return stations_data


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
