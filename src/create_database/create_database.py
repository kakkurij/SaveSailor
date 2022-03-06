from os import getenv
import pandas as pd
from sqlalchemy import create_engine

def read_secrets():
    results = {}
    results["POSTGRES_DB"] = getenv("POSTGRES_DB")
    results["POSTGRES_USER"] = getenv("POSTGRES_USER")
    results["POSTGRES_PASSWORD"] = getenv("POSTGRES_PASSWORD")
    return results


def create_database():
    secrets = read_secrets()
    df = pd.read_excel("./data/tehtavat.xlsx")

    # Make headers lowercase
    df.columns = map(str.lower, df.columns)

    engine = create_engine("postgresql+psycopg2://%s:%s@database/%s" % (secrets["POSTGRES_USER"], secrets["POSTGRES_PASSWORD"], secrets["POSTGRES_DB"]))

    with engine.begin() as conn:
        conn.execute("drop table if exists rescue_data")

    df.to_sql("rescue_data", con=engine)

if __name__ == "__main__":
    create_database()
