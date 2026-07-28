from pathlib import Path
import pandas as pd
import logging
from config import RAW_DATA_PATH
from config import PROCESSED_DATA_PATH

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

PROCESSED_DATA_PATH.mkdir(parents=True, exist_ok=True)

csv_files = list(RAW_DATA_PATH.glob("*.csv"))

def clean_dataset(df: pd.DataFrame) -> pd.DataFrame:
    """
    Perform generic cleaning on a dataset.
    """

    # Remove duplicate rows
    df = df.drop_duplicates()

    # Remove leading/trailing spaces from column names
    df.columns = df.columns.str.strip()

    # Remove leading/trailing spaces from string values
    object_columns = df.select_dtypes(include="object").columns

    for column in object_columns:
        df[column] = df[column].astype(str).str.strip()

    return df

def main():

    for file in csv_files:

        logging.info(f"Processing {file.name}")

        df = pd.read_csv(file)

        cleaned_df = clean_dataset(df)

        output_path = PROCESSED_DATA_PATH / file.name

        cleaned_df.to_csv(output_path, index=False)

        logging.info(f"Saved {output_path.name}")

if __name__ == "__main__":
    main()