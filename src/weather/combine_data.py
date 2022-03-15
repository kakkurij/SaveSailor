def combine_data(conn):
    cur = conn.cursor()

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

    print("Combine data added")