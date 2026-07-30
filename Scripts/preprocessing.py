"""
=========================================================
Mutual Fund Analytics Project
Preprocessing Module

Author : Vansh Rawat
Description:
    Cleans and preprocesses all raw datasets before
    loading them into SQL and Power BI.
=========================================================
"""
#imports

from pathlib import Path
import logging
import pandas as pd
from config import RAW_DATA_PATH
from config import PROCESSED_DATA_PATH


# =========================================================
# Logging Configuration
# =========================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)

# Create processed folder if it doesn't exist
PROCESSED_DATA_PATH.mkdir(parents=True, exist_ok=True)


# =========================================================
# Generic Cleaning
# =========================================================

def basic_cleaning(df: pd.DataFrame) -> pd.DataFrame:
    """
    Performs common preprocessing steps for every dataset.

    Steps:
        • Remove duplicate rows
        • Standardize column names
        • Trim spaces from text columns
        • Replace empty strings with NaN
    """

    df = df.copy()

    # Remove duplicate rows
    df.drop_duplicates(inplace=True)

    # Standardize column names
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
        .str.replace("-", "_")
    )

    # Trim string columns
    string_columns = df.select_dtypes(include="object").columns

    for column in string_columns:

        df[column] = (
            df[column]
            .astype(str)
            .str.strip()
            .replace("", pd.NA)
        )

    return df


def clean_fund_metadata(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean MF API fund metadata.
    """

    logger.info("Cleaning Fund Metadata")

    df = basic_cleaning(df)

    if "scheme_code" in df.columns:
        df["scheme_code"] = pd.to_numeric(
            df["scheme_code"],
            errors="coerce"
        )

    df.drop_duplicates(
        subset="scheme_code",
        inplace=True
    )

    return df


# =========================================================
# 01_fund_master.csv
# =========================================================

def clean_fund_master(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean Fund Master dataset.
    """

    logger.info("Cleaning Fund Master")

    df = basic_cleaning(df)

    numeric_columns = [
        "scheme_code",
        "expense_ratio_pct"
    ]

    for column in numeric_columns:

        if column in df.columns:

            df[column] = pd.to_numeric(
                df[column],
                errors="coerce"
            )

    # Remove duplicate AMFI Codes if any
    if "scheme_code" in df.columns:

        df = df.drop_duplicates(
            subset="scheme_code"
        )

    return df


# =========================================================
# 02_nav_history.csv
# =========================================================

def clean_nav_history(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean NAV History dataset.
    """

    logger.info("Cleaning NAV History")

    df = basic_cleaning(df)

    # Convert scheme code
    if "scheme_code" in df.columns:
        df["scheme_code"] = pd.to_numeric(
            df["scheme_code"],
            errors="coerce"
        )

    # Convert NAV
    if "nav" in df.columns:
        df["nav"] = pd.to_numeric(
            df["nav"],
            errors="coerce"
        )

    # Convert date
    if "date" in df.columns:
        df["date"] = pd.to_datetime(
            df["date"],
            errors="coerce",
            dayfirst=True
        )

    # Remove invalid NAV values
    if "nav" in df.columns:
        df = df[df["nav"] > 0]

    # Sort data
    sort_columns = []

    if "scheme_code" in df.columns:
        sort_columns.append("scheme_code")

    if "date" in df.columns:
        sort_columns.append("date")

    if sort_columns:
        df = df.sort_values(sort_columns)

    return df

# =========================================================
# 03_aum_by_fund_house.csv
# =========================================================

def clean_aum(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean AUM by Fund House dataset.
    """

    logger.info("Cleaning AUM Dataset")

    df = basic_cleaning(df)

    # Convert date column
    if "date" in df.columns:
        df["date"] = pd.to_datetime(
            df["date"],
            errors="coerce"
        )

    # Convert every numeric column except fund_house
    for column in df.columns:

        if column not in ["fund_house", "date"]:

            df[column] = pd.to_numeric(
                df[column],
                errors="coerce"
            )

    return df


# =========================================================
# 04_monthly_sip_inflows.csv
# =========================================================

def clean_monthly_sip(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean SIP dataset.
    """

    logger.info("Cleaning Monthly SIP Dataset")

    df = basic_cleaning(df)

    for column in df.columns:

        if "date" in column or "month" in column:

            df[column] = pd.to_datetime(
                df[column],
                errors="coerce"
            )

    for column in df.columns:

        if df[column].dtype == "object":
            continue

        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )

    return df


# =========================================================
# 05_category_inflows.csv
# =========================================================

def clean_category_inflows(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean Category Inflows dataset.
    """

    logger.info("Cleaning Category Inflows")

    df = basic_cleaning(df)

    for column in df.columns:

        if "date" in column or "month" in column:

            df[column] = pd.to_datetime(
                df[column],
                errors="coerce"
            )

    numeric_columns = df.select_dtypes(
        include="number"
    ).columns

    for column in numeric_columns:

        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )

    return df


# =========================================================
# 06_industry_folio_count.csv
# =========================================================

def clean_industry_folio(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean Industry Folio dataset.
    """

    logger.info("Cleaning Industry Folio Count")

    df = basic_cleaning(df)

    for column in df.columns:

        if "date" in column:

            df[column] = pd.to_datetime(
                df[column],
                errors="coerce"
            )

    for column in df.columns:

        if column != "date":

            df[column] = pd.to_numeric(
                df[column],
                errors="coerce"
            )

    return df


# =========================================================
# 07_scheme_performance.csv
# =========================================================

def clean_scheme_performance(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean Scheme Performance dataset.
    """

    logger.info("Cleaning Scheme Performance")

    df = basic_cleaning(df)

    # Convert AMFI code
    if "scheme_code" in df.columns:

        df["scheme_code"] = pd.to_numeric(
            df["scheme_code"],
            errors="coerce"
        )

    # Convert every remaining numeric column automatically
    for column in df.columns:

        if column in [
            "scheme_name",
            "fund_house",
            "category",
            "risk_category"
        ]:
            continue

        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )

    return df

# =========================================================
# 08_investor_transactions.csv
# =========================================================

def clean_investor_transactions(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean Investor Transactions dataset.
    """

    logger.info("Cleaning Investor Transactions")

    df = basic_cleaning(df)

    # Convert transaction date columns
    for column in df.columns:
        if "date" in column:
            df[column] = pd.to_datetime(
                df[column],
                errors="coerce",
                dayfirst=True
            )

    # Convert numeric columns
    numeric_keywords = [
        "amount",
        "units",
        "price",
        "nav",
        "value",
        "balance",
        "investment"
    ]

    for column in df.columns:

        if any(keyword in column for keyword in numeric_keywords):

            df[column] = pd.to_numeric(
                df[column],
                errors="coerce"
            )

    # Remove transactions having negative amount
    if "amount" in df.columns:
        df = df[df["amount"] >= 0]

    return df


# =========================================================
# 09_portfolio_holdings.csv
# =========================================================

def clean_portfolio_holdings(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean Portfolio Holdings dataset.
    """

    logger.info("Cleaning Portfolio Holdings")

    df = basic_cleaning(df)

    numeric_keywords = [
        "weight",
        "market",
        "value",
        "holding",
        "allocation"
    ]

    for column in df.columns:

        if any(keyword in column for keyword in numeric_keywords):

            df[column] = pd.to_numeric(
                df[column],
                errors="coerce"
            )

    return df


# =========================================================
# 10_benchmark_indices.csv
# =========================================================

def clean_benchmark_indices(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean Benchmark Indices dataset.
    """

    logger.info("Cleaning Benchmark Indices")

    df = basic_cleaning(df)

    # Convert date
    if "date" in df.columns:

        df["date"] = pd.to_datetime(
            df["date"],
            errors="coerce",
            dayfirst=True
        )

    # Convert index values
    numeric_keywords = [
        "close",
        "index",
        "value",
        "price"
    ]

    for column in df.columns:

        if any(keyword in column for keyword in numeric_keywords):

            if column != "index_name":

                df[column] = pd.to_numeric(
                    df[column],
                    errors="coerce"
                )

    return df


# =========================================================
# Cleaner Dispatcher
# =========================================================

CLEANERS = {

    "fund_metadata.csv":
        clean_fund_metadata,

    "nav_history.csv":
        clean_nav_history,

    "03_aum_by_fund_house.csv":
        clean_aum,

    "04_monthly_sip_inflows.csv":
        clean_monthly_sip,

    "05_category_inflows.csv":
        clean_category_inflows,

    "06_industry_folio_count.csv":
        clean_industry_folio,

    "07_scheme_performance.csv":
        clean_scheme_performance,

    "08_investor_transactions.csv":
        clean_investor_transactions,

    "09_portfolio_holdings.csv":
        clean_portfolio_holdings,

    "10_benchmark_indices.csv":
        clean_benchmark_indices

}

# =========================================================
# Main Processing Function
# =========================================================

def process_file(file_path: Path):
    """
    Process a single CSV file.
    """

    logger.info("=" * 60)
    logger.info(f"Processing: {file_path.name}")

    try:

        df = pd.read_csv(file_path)

        original_rows = len(df)

        cleaner = CLEANERS.get(
            file_path.name,
            basic_cleaning
        )

        cleaned_df = cleaner(df)

        cleaned_rows = len(cleaned_df)

        output_file = (
            PROCESSED_DATA_PATH /
            file_path.name
        )

        cleaned_df.to_csv(
            output_file,
            index=False
        )

        logger.info(
            f"Saved -> {output_file.name}"
        )

        logger.info(
            f"Rows: {original_rows} → {cleaned_rows}"
        )

        logger.info(
            f"Columns: {len(cleaned_df.columns)}"
        )

        logger.info("Completed Successfully\n")

    except Exception as e:

        logger.exception(
            f"Error processing {file_path.name}: {e}"
        )


# =========================================================
# Main
# =========================================================

def main():

    logger.info("=" * 70)
    logger.info("Mutual Fund Analytics")
    logger.info("Starting Data Preprocessing")
    logger.info("=" * 70)

    csv_files = sorted(
        RAW_DATA_PATH.glob("*.csv")
    )

    if not csv_files:

        logger.warning(
            "No CSV files found in data/raw/"
        )

        return

    logger.info(
        f"Found {len(csv_files)} CSV files.\n"
    )

    for file_path in csv_files:

        process_file(file_path)

    logger.info("=" * 70)
    logger.info("All datasets processed successfully.")
    logger.info("=" * 70)


if __name__ == "__main__":
    main()