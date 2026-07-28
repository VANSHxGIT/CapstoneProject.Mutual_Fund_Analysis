"""
Configuration file for Mutual Fund Analytics
"""

from pathlib import Path

# -----------------------------
# API Configuration
# -----------------------------
BASE_URL = "https://api.mfapi.in/mf"

SCHEME_CODES = [
    119551,  # SBI Bluechip
    120503,  # ICICI Bluechip
    118632,  # Nippon Large Cap
    119092,  # Axis Bluechip
    120841   # Kotak Bluechip
]

# -----------------------------
# Project Paths
# -----------------------------
PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_PATH = PROJECT_ROOT / "data"

RAW_DATA_PATH = DATA_PATH / "raw"
PROCESSED_DATA_PATH = DATA_PATH / "processed"
REPORT_PATH = DATA_PATH / "reports" 