import psycopg2
from fmiopendata.wfs import download_stored_query
import datetime
import numpy as np
import calendar
from create_weather_data_tables import create_tables, read_secrets
from combine_data import combine_data
from time import sleep
from psycopg2.extras import execute_values

FMISID = "fmisid=101311" # Tampere Siilinkari 


def get_dates(year):
    last_days = [datetime.datetime(year, x, (calendar.monthrange(year, x)[1])) for x in range(1, 13)]

    first_days = [datetime.datetime(year, x, 1) for x in range(1, 13)]

    first_last = list(zip(first_days, last_days))

    return first_last


def create_query_times():
    pairs_by_year = [get_dates(y) for y in range(2010, 2011)] 
    query_time_pairs = []

    for pairs in pairs_by_year:
        for pair in pairs:
            start = pair[0]
            end = pair[1]

            first = True
            to_start_from = start

            while True:
                if first:
                    end_datetime = to_start_from + datetime.timedelta(days=7)

                    start_time = to_start_from.strftime("%Y-%m-%dT%H:%M:%SZ")
                    end_time = end_datetime.strftime("%Y-%m-%dT%H:%M:%SZ")

                    to_start_from = end_datetime
                    query_time_pairs.append((start_time, end_time))
                    first = False
                else:
                    start_datetime = to_start_from + datetime.timedelta(hours=1)
                    end_datetime = to_start_from + datetime.timedelta(days=7)

                    if end_datetime > end:
                        end_datetime = end_datetime.replace(day=1)
                        start_time = start_datetime.strftime("%Y-%m-%dT%H:%M:%SZ")
                        end_time = end_datetime.strftime("%Y-%m-%dT%H:%M:%SZ")
                        query_time_pairs.append((start_time, end_time))
                        break

                    to_start_from = end_datetime    
                    start_time = start_datetime.strftime("%Y-%m-%dT%H:%M:%SZ")
                    end_time = end_datetime.strftime("%Y-%m-%dT%H:%M:%SZ")

                    query_time_pairs.append((start_time, end_time))

    return query_time_pairs


def query_fmi_data():
    query_time_pairs = create_query_times()

    fmi_data = []

    for pair in query_time_pairs:
        start_time = f"starttime={pair[0]}"
        end_time = f"endtime={pair[1]}"

        args= [start_time, end_time, "timestep=60", FMISID]

        res = download_stored_query("fmi::observations::weather::multipointcoverage", args=args)

        for k, v in res.data.items():
            fmi_data_list = []
            fmi_data_list.append(k)
            for station, station_values in v.items():
                for key, station_value in station_values.items():
                    value = station_value.get("value")

                    if np.isnan(value):
                        value = None
                    else:
                        value = value.item()

                    fmi_data_list.append(value)
            
            fmi_data.append(fmi_data_list)

    return fmi_data


def insert_fmi_data_to_db(fmi_data):
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

    execute_values(cur, """INSERT INTO WEATHER_DATA (ts, air_temperature, wind_speed, gust_speed, wind_direction, relative_humidity, dew_point_temperature, precipitation_amount,
    precipitation_intensity, snow_depth, pressure_msl, horizontal_visibility, cloud_amount, present_weather) VALUES %s""", fmi_data)

    conn.commit()
    conn.close()


if __name__ == "__main__":
    create_tables()
    fmi_data = query_fmi_data()
    insert_fmi_data_to_db(fmi_data)
    print("FMI data added")

    print("Combining data")
    combine_data()
