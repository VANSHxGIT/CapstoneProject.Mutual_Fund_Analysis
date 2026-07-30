"""
Load all processed CSV files into SQLite database.
"""

import logging
import sqlite3

import pandas as pd

from config import DATABASE_PATH
from config import PROCESSED_DATA_PATH

# -------------------------------------------------------
# Logging
# -------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)

# Create sql folder if it doesn't exist
DATABASE_PATH.parent.mkdir(
    parents=True,
    exist_ok=True
)


# -------------------------------------------------------
# Database Connection
# -------------------------------------------------------

def connect_database():
    """
    Connect to SQLite database.
    """

    connection = sqlite3.connect(DATABASE_PATH)

    logger.info("Connected to SQLite database.")

    return connection


# -------------------------------------------------------
# Load CSV
# -------------------------------------------------------

def load_csv(file_path):
    """
    Read CSV file.
    """

    logger.info(f"Reading {file_path.name}")

    return pd.read_csv(file_path)


# -------------------------------------------------------
# Load Table
# -------------------------------------------------------

def load_table(df, table_name, connection):
    """
    Load dataframe into SQLite.
    """

    df.to_sql(
        table_name,
        connection,
        if_exists="replace",
        index=False
    )

    logger.info(f"Loaded table: {table_name}")


# -------------------------------------------------------
# Verify Table
# -------------------------------------------------------

def verify_table(table_name, connection):

    cursor = connection.cursor()

    cursor.execute(
        f"SELECT COUNT(*) FROM {table_name}"
    )

    count = cursor.fetchone()[0]

    logger.info(f"{table_name}: {count} rows")


# -------------------------------------------------------
# Main
# -------------------------------------------------------

def main():

    logger.info("=" * 60)
    logger.info("Loading processed CSV files into SQLite")
    logger.info("=" * 60)

    connection = connect_database()

    csv_files = sorted(
        PROCESSED_DATA_PATH.glob("*.csv")
    )

    if not csv_files:

        logger.warning(
            "No processed CSV files found."
        )

        return

    for file in csv_files:

        table_name = file.stem

        # Remove numeric prefixes only (01_, 02_, ...)
        if len(table_name) >= 3 and table_name[:2].isdigit() and table_name[2] == "_":
            table_name = table_name[3:]

        try:

            df = load_csv(file)

            load_table(
                df,
                table_name,
                connection
            )

            verify_table(
                table_name,
                connection
            )

        except Exception as e:

            logger.exception(
                f"Failed to load {file.name}: {e}"
            )

    connection.close()

    logger.info("=" * 60)
    logger.info("Database loading completed.")
    logger.info("=" * 60)


if __name__ == "__main__":
    main()