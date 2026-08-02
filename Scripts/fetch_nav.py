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


def save_all_data(all_metadata: list, all_history: list):
    """
    Save all metadata and NAV history.
    If the CSV already exists, append new data.
    """
    if not all_metadata or not all_history:
        print("No data to save.")
        return

    meta_df = pd.DataFrame(all_metadata)
    history_df = pd.DataFrame(all_history)

    RAW_DATA_PATH.mkdir(parents=True, exist_ok=True)

    metadata_file = RAW_DATA_PATH / "fund_metadata.csv"
    history_file = RAW_DATA_PATH / "nav_history.csv"

    # ---------- FUND METADATA ----------
    if metadata_file.exists():
        existing = pd.read_csv(metadata_file)
        meta_df = pd.concat([existing, meta_df], ignore_index=True)
        # remove duplicates
        meta_df.drop_duplicates(subset=["scheme_code"], inplace=True)

    meta_df.to_csv(metadata_file, index=False)

    # ---------- NAV HISTORY ----------
    if history_file.exists():
        existing = pd.read_csv(history_file)
        history_df = pd.concat([existing, history_df], ignore_index=True)

    history_df.to_csv(history_file, index=False)


def main():
    all_metadata = []
    all_history = []

    for code in SCHEME_CODES:
        print(f"Downloading {code}")
        try:
            data = fetch_scheme_data(code)
            meta = data["meta"]
            history = data["data"]

            all_metadata.append(meta)

            for record in history:
                record["scheme_code"] = meta["scheme_code"]
                
            all_history.extend(history)
            
            print(f"Processed scheme {meta['scheme_code']}")
        except Exception as e:
            print(f"Failed to fetch {code}: {e}")

    print("Saving all data...")
    save_all_data(all_metadata, all_history)
    print("Done!")


if __name__ == "__main__":
    main()