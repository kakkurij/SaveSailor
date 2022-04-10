from weather.fmi_data import run_fmi
from weather.database_setup import create_connection
from rescue_data.rescue_data import add_rescue_data
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


if __name__ == "__main__":
    add_rescue_data()# asdsad

    conn = create_connection()

    if conn is None:
        print("No database connection, exiting")
        sys.exit(1)

    run_fmi(conn)

    conn.close()
