import os
import requests
import pandas as pd

from config import BASE_URL
from config import SCHEME_CODES
from config import RAW_DATA_PATH


def fetch_scheme_data(scheme_code: int):
    """
    Fetch mutual fund data from MFAPI.
    """

    url = f"{BASE_URL}/{scheme_code}"

    response = requests.get(url, timeout=30)

    response.raise_for_status()

    return response.json()


def save_data(json_data):
    """
    Save metadata and NAV history.
    If the CSV already exists, append new data.
    """

    meta = json_data["meta"]
    history = json_data["data"]

    meta_df = pd.DataFrame([meta])
    history_df = pd.DataFrame(history)

    history_df["scheme_code"] = meta["scheme_code"]

    os.makedirs(RAW_DATA_PATH, exist_ok=True)

    metadata_file = f"{RAW_DATA_PATH}/fund_metadata.csv"
    history_file = f"{RAW_DATA_PATH}/nav_history.csv"

    # ---------- FUND METADATA ----------
    if os.path.exists(metadata_file):
        existing = pd.read_csv(metadata_file)
        meta_df = pd.concat([existing, meta_df], ignore_index=True)

        # remove duplicates
        meta_df.drop_duplicates(
            subset=["scheme_code"],
            inplace=True
        )

    meta_df.to_csv(metadata_file, index=False)

    # ---------- NAV HISTORY ----------
    if os.path.exists(history_file):
        existing = pd.read_csv(history_file)
        history_df = pd.concat([existing, history_df], ignore_index=True)

    history_df.to_csv(history_file, index=False)

    print(f"Saved scheme {meta['scheme_code']}")

def main():

    for code in SCHEME_CODES:

        print(f"Downloading {code}")

        data = fetch_scheme_data(code)

        save_data(data)


if __name__ == "__main__":
    main()