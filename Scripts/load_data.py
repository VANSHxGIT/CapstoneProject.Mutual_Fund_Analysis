"""Load the ten processed datasets into SQLite and verify every table."""

import logging
import sqlite3
from contextlib import closing

import pandas as pd

from config import CANONICAL_DATASETS, DATABASE_PATH, PROCESSED_DATA_PATH

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")
logger = logging.getLogger(__name__)


def table_name(file_name: str) -> str:
    """Convert a dataset filename to its SQLite table name."""
    return file_name[:-4] if file_name.endswith(".csv") else file_name


def connect_database():
    """Open the SQLite database."""
    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(DATABASE_PATH)


def load_table(df: pd.DataFrame, name: str, connection: sqlite3.Connection) -> int:
    """Replace a SQLite table and return its row count."""
    df.to_sql(name, connection, if_exists="replace", index=False)
    quoted = '"' + name.replace('"', '""') + '"'
    count = connection.execute(f"SELECT COUNT(*) FROM {quoted}").fetchone()[0]
    return int(count)


def main() -> None:
    """Load all canonical processed CSV files into SQLite."""
    missing = [f for f in CANONICAL_DATASETS if not (PROCESSED_DATA_PATH / f).exists()]
    if missing:
        raise FileNotFoundError("Missing processed datasets:\n- " + "\n- ".join(missing))

    with closing(connect_database()) as connection:
        for file_name in CANONICAL_DATASETS:
            path = PROCESSED_DATA_PATH / file_name
            name = table_name(file_name)

            logger.info("Loading %s -> %s", file_name, name)
            df = pd.read_csv(path)
            count = load_table(df, name, connection)
            logger.info("Verified %s: %s rows", name, count)

        connection.commit()

    logger.info("SQLite loading completed successfully: %s", DATABASE_PATH)


if __name__ == "__main__":
    main()
