from fmiopendata.wfs import download_stored_query
import datetime
import numpy as np
import calendar
from weather.database_setup import setup_weather_database
from weather.combine_data import combine_data
from psycopg2.extras import execute_values


class FMIData:
    def __init__(self, conn):
        self.conn = conn
        self.end_year = 2014

    def get_dates(self, year):
        """Generate first and last day of each for for given year

        Args:
            year (int): -

        Returns:
            List of tuples: -
        """
        last_days = [
            datetime.datetime(
                year, x, (calendar.monthrange(
                    year, x)[1])) for x in range(
                1, 13)]

        first_days = [datetime.datetime(year, x, 1) for x in range(1, 13)]

        first_last = list(zip(first_days, last_days))

        return first_last

    def create_query_times(self):
        """Generate query steps for FMI API

        Returns:
            _type_: _description_
        """

        pairs_by_year = [
            self.get_dates(y) for y in range(
                2010, self.end_year + 1)]
        query_time_pairs = []

        for pairs in pairs_by_year:
            for pair in pairs:
                start = pair[0]
                end = pair[1]

                first = True
                to_start_from = start

                while True:
                    if first:
                        end_datetime = to_start_from + \
                            datetime.timedelta(days=7)

                        start_time = to_start_from.strftime(
                            "%Y-%m-%dT%H:%M:%SZ")
                        end_time = end_datetime.strftime("%Y-%m-%dT%H:%M:%SZ")

                        to_start_from = end_datetime
                        query_time_pairs.append((start_time, end_time))
                        first = False
                    else:
                        start_datetime = to_start_from + \
                            datetime.timedelta(hours=1)
                        end_datetime = to_start_from + \
                            datetime.timedelta(days=7)

                        if end_datetime > end:
                            end_datetime = end_datetime.replace(day=1)
                            start_time = start_datetime.strftime(
                                "%Y-%m-%dT%H:%M:%SZ")
                            end_time = end_datetime.strftime(
                                "%Y-%m-%dT%H:%M:%SZ")
                            query_time_pairs.append((start_time, end_time))
                            break

                        to_start_from = end_datetime
                        start_time = start_datetime.strftime(
                            "%Y-%m-%dT%H:%M:%SZ")
                        end_time = end_datetime.strftime("%Y-%m-%dT%H:%M:%SZ")

                        query_time_pairs.append((start_time, end_time))

        return query_time_pairs

    def query_fmi_data(self):
        cur = self.conn.cursor()

        query_time_pairs = self.create_query_times()

        fmi_data = []

        cur.execute("SELECT fmisid FROM weather_station;")

        all_stations = [x[0] for x in cur.fetchall()]

        for station_id in all_stations:
            for pair in query_time_pairs:
                start_time = f"starttime={pair[0]}"
                end_time = f"endtime={pair[1]}"

                args = [
                    start_time,
                    end_time,
                    "timestep=60",
                    f"fmisid={station_id}"]

                res = download_stored_query(
                    "fmi::observations::weather::multipointcoverage",
                    args=args)

                for dt, v in res.data.items():
                    fmi_data_list = []
                    fmi_data_list.append(station_id)
                    fmi_data_list.append(dt)

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

    def insert_fmi_data_to_db(self, fmi_data):
        cur = self.conn.cursor()

        execute_values(
            cur,
            """INSERT INTO WEATHER_DATA (fmisid, ts, air_temperature, wind_speed,
            gust_speed, wind_direction, relative_humidity,
            dew_point_temperature, precipitation_amount,
            precipitation_intensity, snow_depth, pressure_msl,
            horizontal_visibility, cloud_amount, present_weather) VALUES %s""",
            fmi_data)

        print("Added fmi data")

        self.conn.commit()

    def run(self):
        fmi_data = self.query_fmi_data()
        self.insert_fmi_data_to_db(fmi_data)


def run_fmi(conn):
    setup_weather_database(conn)

    fmi_data_parser = FMIData(conn)
    fmi_data_parser.run()

    combine_data(conn)
