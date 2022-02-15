import psycopg2
from time import sleep
from os import getenv
import pandas as pd
from sqlalchemy import create_engine

def read_secrets():
    results = {}
    results["POSTGRES_DB"] = getenv("POSTGRES_DB")
    results["POSTGRES_USER"] = getenv("POSTGRES_USER")
    results["POSTGRES_PASSWORD"] = getenv("POSTGRES_PASSWORD")
    return results



df = pd.read_excel('./data/tehtavat.xlsx')

engine = create_engine('postgresql+psycopg2://username:password@database/savesailor_database')

df.to_sql('rescue_data', con=engine)