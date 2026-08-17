"""Clean the ten canonical raw datasets and write processed CSV files."""

import logging
from pathlib import Path

import pandas as pd

from config import CANONICAL_DATASETS, PROCESSED_DATA_PATH, RAW_DATA_PATH

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")
logger = logging.getLogger(__name__)

PROCESSED_DATA_PATH.mkdir(parents=True, exist_ok=True)


def basic_cleaning(df: pd.DataFrame) -> pd.DataFrame:
    """Apply common cleaning operations."""
    df = df.copy()
    df.columns = (
        df.columns.astype(str)
        .str.strip()
        .str.lower()
        .str.replace(" ", "_", regex=False)
        .str.replace("-", "_", regex=False)
    )
    for col in df.select_dtypes(include=["object", "string"]).columns:
        df[col] = df[col].astype("string").str.strip()
        df[col] = df[col].replace("", pd.NA)
    return df.drop_duplicates().reset_index(drop=True)


def clean_fund_metadata(df):
    df = basic_cleaning(df)
    if "scheme_code" in df:
        df["scheme_code"] = pd.to_numeric(df["scheme_code"], errors="coerce").astype("Int64")
        df = df.drop_duplicates("scheme_code")
    return df


def clean_nav_history(df):
    df = basic_cleaning(df)
    df["scheme_code"] = pd.to_numeric(df["scheme_code"], errors="coerce").astype("Int64")
    df["nav"] = pd.to_numeric(df["nav"], errors="coerce")
    df["date"] = pd.to_datetime(df["date"], errors="coerce", dayfirst=True)
    df = df.dropna(subset=["scheme_code", "date", "nav"])
    df = df[df["nav"] > 0]
    return (
        df.drop_duplicates(["scheme_code", "date"], keep="last")
        .sort_values(["scheme_code", "date"])
        .reset_index(drop=True)
    )


def clean_aum(df):
    df = basic_cleaning(df)
    if "date" in df:
        df["date"] = pd.to_datetime(df["date"], errors="coerce")
    for col in df.columns:
        if col not in {"fund_house", "date"}:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    return df


def clean_monthly_sip(df):
    df = basic_cleaning(df)
    for col in df.columns:
        if "date" in col or "month" in col:
            df[col] = pd.to_datetime(df[col], errors="coerce")
        elif col not in {"fund_house"}:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    return df


def clean_category_inflows(df):
    df = basic_cleaning(df)
    for col in df.columns:
        if "date" in col or "month" in col:
            df[col] = pd.to_datetime(df[col], errors="coerce")
        elif col != "category":
            df[col] = pd.to_numeric(df[col], errors="coerce")
    return df


def clean_industry_folio(df):
    df = basic_cleaning(df)
    for col in df.columns:
        if "date" in col:
            df[col] = pd.to_datetime(df[col], errors="coerce")
        elif col not in {"category"}:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    return df


def clean_scheme_performance(df):
    df = basic_cleaning(df)
    if "amfi_code" in df:
        df["amfi_code"] = pd.to_numeric(df["amfi_code"], errors="coerce").astype("Int64")

    text_cols = {"scheme_name", "fund_house", "category", "plan", "risk_grade", "risk_category"}
    for col in df.columns:
        if col not in text_cols and col != "amfi_code":
            df[col] = pd.to_numeric(df[col], errors="coerce")
    return df.drop_duplicates("amfi_code").reset_index(drop=True)


def clean_investor_transactions(df):
    df = basic_cleaning(df)
    for col in df.columns:
        if "date" in col:
            df[col] = pd.to_datetime(df[col], errors="coerce", dayfirst=True)
        elif col in {"amount_inr", "annual_income_lakh"}:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    return df


def clean_portfolio_holdings(df):
    df = basic_cleaning(df)
    for col in df.columns:
        if col in {"weight_pct", "market_value_cr", "current_price_inr"}:
            df[col] = pd.to_numeric(df[col], errors="coerce")
        elif col == "portfolio_date":
            df[col] = pd.to_datetime(df[col], errors="coerce")
    return df


def clean_benchmark_indices(df):
    df = basic_cleaning(df)
    df["date"] = pd.to_datetime(df["date"], errors="coerce", dayfirst=True)
    df["close_value"] = pd.to_numeric(df["close_value"], errors="coerce")
    return df.dropna(subset=["date", "index_name", "close_value"])


CLEANERS = {
    "01_fund_metadata.csv": clean_fund_metadata,
    "02_nav_history.csv": clean_nav_history,
    "03_aum_by_fund_house.csv": clean_aum,
    "04_monthly_sip_inflows.csv": clean_monthly_sip,
    "05_category_inflows.csv": clean_category_inflows,
    "06_industry_folio_count.csv": clean_industry_folio,
    "07_scheme_performance.csv": clean_scheme_performance,
    "08_investor_transactions.csv": clean_investor_transactions,
    "09_portfolio_holdings.csv": clean_portfolio_holdings,
    "10_benchmark_indices.csv": clean_benchmark_indices,
}


def process_file(file_path: Path) -> None:
    """Clean one canonical dataset."""
    logger.info("Processing %s", file_path.name)
    df = pd.read_csv(file_path)
    cleaned = CLEANERS[file_path.name](df)
    output = PROCESSED_DATA_PATH / file_path.name
    cleaned.to_csv(output, index=False)
    logger.info("%s: %s -> %s rows", file_path.name, len(df), len(cleaned))


def main() -> None:
    """Clean all ten canonical datasets."""
    missing = [f for f in CANONICAL_DATASETS if not (RAW_DATA_PATH / f).exists()]
    if missing:
        raise FileNotFoundError("Missing raw datasets:\n- " + "\n- ".join(missing))

    for name in CANONICAL_DATASETS:
        process_file(RAW_DATA_PATH / name)

    logger.info("All canonical datasets processed successfully.")


if __name__ == "__main__":
    main()
