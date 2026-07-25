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
    Save metadata and NAV history separately.
    """

    meta = json_data["meta"]
    history = json_data["data"]

    meta_df = pd.DataFrame([meta])

    history_df = pd.DataFrame(history)

    history_df["scheme_code"] = meta["scheme_code"]

    os.makedirs(RAW_DATA_PATH, exist_ok=True)

    meta_df.to_csv(
        f"{RAW_DATA_PATH}/fund_metadata.csv",
        index=False
    )

    history_df.to_csv(
        f"{RAW_DATA_PATH}/nav_history.csv",
        index=False
    )

    print("Data saved successfully.")


def main():

    for code in SCHEME_CODES:

        print(f"Downloading {code}")

        data = fetch_scheme_data(code)

        save_data(data)


if __name__ == "__main__":
    main()