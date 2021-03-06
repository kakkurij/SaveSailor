import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from weather.fmi_data import run_fmi    # noqa
from weather.database_setup import create_connection        # noqa
from rescue_data.rescue_data import add_rescue_data         # noqa


if __name__ == "__main__":
    add_rescue_data()

    conn = create_connection()

    if conn is None:
        print("No database connection, exiting")
        sys.exit(1)

    run_fmi(conn)

    conn.close()
