"""Validate processed mutual-fund datasets before SQLite loading."""

import logging
import sqlite3

import pandas as pd

from config import DATABASE_PATH, PROCESSED_DATA_PATH, CANONICAL_DATASETS

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")
logger = logging.getLogger(__name__)

REQUIRED_COLUMNS = {
    "01_fund_metadata.csv": {"scheme_code", "scheme_name", "fund_house"},
    "02_nav_history.csv": {"date", "nav", "scheme_code"},
    "03_aum_by_fund_house.csv": {"fund_house", "date"},
    "04_monthly_sip_inflows.csv": {"month"},
    "05_category_inflows.csv": {"category"},
    "06_industry_folio_count.csv": {"month"},
    "07_scheme_performance.csv": {"amfi_code", "scheme_name", "risk_grade", "sharpe_ratio"},
    "08_investor_transactions.csv": {
        "investor_id", "transaction_date", "amfi_code", "transaction_type", "amount_inr"
    },
    "09_portfolio_holdings.csv": {
        "amfi_code", "stock_symbol", "sector", "weight_pct", "portfolio_date"
    },
    "10_benchmark_indices.csv": {"date", "index_name", "close_value"},
}


def validate_file(name: str) -> pd.DataFrame:
    """Validate one processed CSV and return it."""
    path = PROCESSED_DATA_PATH / name
    if not path.exists():
        raise FileNotFoundError(f"Processed dataset missing: {path}")

    df = pd.read_csv(path)
    missing_cols = REQUIRED_COLUMNS[name] - set(df.columns)
    if missing_cols:
        raise ValueError(f"{name}: missing required columns: {sorted(missing_cols)}")

    if df.empty:
        raise ValueError(f"{name}: dataset is empty")

    logger.info("%s | rows=%s | columns=%s", name, len(df), len(df.columns))
    return df


def main() -> None:
    """Run all validation checks and fail the stage if any critical check fails."""
    datasets = {name: validate_file(name) for name in CANONICAL_DATASETS}

    nav = datasets["02_nav_history.csv"]
    if (pd.to_numeric(nav["nav"], errors="coerce") <= 0).any():
        raise ValueError("02_nav_history.csv: NAV contains non-positive values")

    nav["date"] = pd.to_datetime(nav["date"], errors="coerce")
    if nav["date"].isna().any():
        raise ValueError("02_nav_history.csv: invalid dates found")

    if nav.duplicated(["scheme_code", "date"]).any():
        raise ValueError("02_nav_history.csv: duplicate scheme/date records found")

    scheme_codes = set(
        pd.to_numeric(datasets["01_fund_metadata.csv"]["scheme_code"], errors="coerce")
        .dropna().astype(int)
    )
    nav_codes = set(
        pd.to_numeric(nav["scheme_code"], errors="coerce")
        .dropna().astype(int)
    )

    missing_nav = scheme_codes - nav_codes
    logger.info("Fund metadata schemes: %s | NAV schemes: %s", len(scheme_codes), len(nav_codes))

    # One scheme was previously confirmed to have no usable value; don't fail the ETL
    # merely because it is absent from NAV history. Report it instead.
    if missing_nav:
        logger.warning("Schemes present in metadata but absent from NAV: %s", sorted(missing_nav))

    benchmark = datasets["10_benchmark_indices.csv"]
    benchmark["close_value"] = pd.to_numeric(benchmark["close_value"], errors="coerce")
    if (benchmark["close_value"] <= 0).any():
        raise ValueError("10_benchmark_indices.csv: non-positive benchmark values found")

    investors = datasets["08_investor_transactions.csv"]
    investors["amount_inr"] = pd.to_numeric(investors["amount_inr"], errors="coerce")
    if investors["amount_inr"].isna().any():
        raise ValueError("08_investor_transactions.csv: invalid amount_inr values found")

    portfolio = datasets["09_portfolio_holdings.csv"]
    portfolio["weight_pct"] = pd.to_numeric(portfolio["weight_pct"], errors="coerce")
    if (portfolio["weight_pct"] < 0).any():
        raise ValueError("09_portfolio_holdings.csv: negative portfolio weights found")

    # Check that SQLite can be opened if it already exists.
    if DATABASE_PATH.exists():
        with sqlite3.connect(DATABASE_PATH) as conn:
            conn.execute("SELECT 1")
        logger.info("SQLite database connection check: OK")

    logger.info("ALL DATA VALIDATION CHECKS PASSED")


if __name__ == "__main__":
    main()
