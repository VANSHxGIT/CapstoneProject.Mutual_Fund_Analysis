"""Central configuration for the Mutual Fund Analytics project."""

from pathlib import Path

BASE_URL = "https://api.mfapi.in/mf"

# The capstone specifies five schemes for the live NAV API step.
SCHEME_CODES = [
    119551,  # SBI Bluechip
    120503,  # ICICI Bluechip
    118632,  # Nippon Large Cap
    119092,  # Axis Bluechip
    120841,  # Kotak Bluechip
]

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = PROJECT_ROOT / "data"
RAW_DATA_PATH = DATA_PATH / "raw"
PROCESSED_DATA_PATH = DATA_PATH / "processed"
REPORT_PATH = DATA_PATH / "reports"

SQL_PATH = PROJECT_ROOT / "sql"
DATABASE_PATH = SQL_PATH / "mutual_fund.db"

# Canonical input files. Unnumbered duplicate copies such as
# fund_metadata.csv/nav_history.csv are intentionally ignored.
CANONICAL_DATASETS = [
    "01_fund_metadata.csv",
    "02_nav_history.csv",
    "03_aum_by_fund_house.csv",
    "04_monthly_sip_inflows.csv",
    "05_category_inflows.csv",
    "06_industry_folio_count.csv",
    "07_scheme_performance.csv",
    "08_investor_transactions.csv",
    "09_portfolio_holdings.csv",
    "10_benchmark_indices.csv",
]
