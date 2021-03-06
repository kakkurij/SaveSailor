import pandas as pd
import numpy as np
from weather.database_setup import read_secrets
from sqlalchemy import create_engine

# These columns should be datetime
dt_columns = [
    "päivämäärä",
    "hälytys",
    "matkalla",
    "kohteessa",
    "vapaana / keskeytetty",
    "asemalla"]


def add_rescue_data():
    secrets = read_secrets()
    df = pd.read_excel("./data/tehtavat.xlsx")

    # Make headers lowercase
    df.columns = map(str.lower, df.columns)

    # Convert columns to datetime
    for c in dt_columns:
        if df[c].dtype != np.datetime64:
            df[c] = pd.to_datetime(
                df[c],
                dayfirst=True,
                infer_datetime_format=True,
                errors='coerce')

    engine = create_engine(
        "postgresql+psycopg2://%s:%s@database/%s" %
        (secrets["POSTGRES_USER"],
         secrets["POSTGRES_PASSWORD"],
         secrets["POSTGRES_DB"]))

    with engine.begin() as conn:
        conn.execute("drop table if exists rescue_data cascade")

    df.to_sql("rescue_data", con=engine)

    # Add Primary key to pandas make column index
    with engine.begin() as conn:
        conn.execute("ALTER TABLE rescue_data ADD PRIMARY KEY (index)")

    print("Added rescue data")
