"""Fetch live NAV data for the five configured schemes without destroying existing history."""

import logging

import pandas as pd
import requests

from config import BASE_URL, RAW_DATA_PATH, SCHEME_CODES

logger = logging.getLogger(__name__)


def fetch_scheme_data(scheme_code: int) -> dict:
    """Fetch one scheme from MFAPI."""
    response = requests.get(f"{BASE_URL}/{scheme_code}", timeout=30)
    response.raise_for_status()
    return response.json()


def main() -> None:
    """Fetch configured schemes and merge them into the canonical NAV history."""
    RAW_DATA_PATH.mkdir(parents=True, exist_ok=True)

    history_file = RAW_DATA_PATH / "02_nav_history.csv"
    if not history_file.exists():
        raise FileNotFoundError(f"Required NAV history not found: {history_file}")

    existing = pd.read_csv(history_file)
    existing["scheme_code"] = pd.to_numeric(existing["scheme_code"], errors="coerce")
    existing["date"] = pd.to_datetime(existing["date"], errors="coerce", dayfirst=True)
    existing["nav"] = pd.to_numeric(existing["nav"], errors="coerce")

    fetched = []
    failures = []

    for code in SCHEME_CODES:
        try:
            logger.info("Fetching NAV for scheme %s", code)
            payload = fetch_scheme_data(code)

            history = pd.DataFrame(payload.get("data", []))
            if history.empty:
                raise ValueError("MFAPI returned no NAV observations")

            history["scheme_code"] = int(payload["meta"]["scheme_code"])
            history["date"] = pd.to_datetime(history["date"], errors="coerce", dayfirst=True)
            history["nav"] = pd.to_numeric(history["nav"], errors="coerce")
            history = history[["date", "nav", "scheme_code"]]
            history = history.dropna(subset=["date", "nav", "scheme_code"])
            fetched.append(history)

        except Exception as exc:
            failures.append((code, str(exc)))
            logger.exception("Failed to fetch scheme %s", code)

    if not fetched:
        raise RuntimeError("No configured NAV scheme could be fetched.")

    new_data = pd.concat(fetched, ignore_index=True)
    combined = pd.concat([existing, new_data], ignore_index=True)

    combined = (
        combined
        .dropna(subset=["date", "nav", "scheme_code"])
        .query("nav > 0")
        .drop_duplicates(subset=["scheme_code", "date"], keep="last")
        .sort_values(["scheme_code", "date"])
        .reset_index(drop=True)
    )

    combined.to_csv(history_file, index=False)

    logger.info("NAV history updated: %s rows, %s schemes",
                len(combined), combined["scheme_code"].nunique())

    if failures:
        logger.warning("NAV fetch completed with %s failure(s): %s", len(failures), failures)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")
    main()
