import sqlite3
import pandas as pd
import logging
from pathlib import Path
from config import DATABASE_PATH
from config import PROCESSED_DATA_PATH

logging.basicConfig(

    level=logging.INFO,

    format="%(asctime)s | %(levelname)s | %(message)s"

)

logger = logging.getLogger(__name__)
DATABASE_PATH.parent.mkdir(

    parents=True,

    exist_ok=True

)
def connect_database():

    """
    Create SQLite connection.
    """

    connection = sqlite3.connect(DATABASE_PATH)

    logger.info("SQLite Connected.")

    return connection

def load_csv(file_path):

    """
    Read CSV into DataFrame.
    """

    logger.info(

        f"Reading {file_path.name}"

    )

    return pd.read_csv(file_path)

def load_table(

        df,

        table_name,

        connection

):

    """
    Load dataframe into SQLite.
    """

    df.to_sql(

        table_name,

        connection,

        if_exists="replace",

        index=False

    )

    logger.info(

        f"{table_name} loaded."

    )
