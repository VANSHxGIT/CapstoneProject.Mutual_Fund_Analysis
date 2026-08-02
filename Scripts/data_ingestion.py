import os
from pathlib import Path

import pandas as pd
RAW_DATA_PATH = Path("data/raw")
REPORT_PATH = Path("data/reports")
def load_dataset(file_path: Path) -> pd.DataFrame:
    """
    Load a CSV file into a Pandas DataFrame.

    Args:
        file_path (Path): Path to the CSV file.

    Returns:
        pd.DataFrame: Loaded dataset.
    """
    return pd.read_csv(file_path)
def display_dataset_info(df: pd.DataFrame, file_name: str):
    """
    Display basic information about the dataset.
    """

    print("=" * 60)
    print(f"Dataset: {file_name}")
    print("=" * 60)

    print(f"Shape: {df.shape}")

    print("\nColumns:")
    print(df.columns.tolist())

    print("\nData Types:")
    print(df.dtypes)

    print("\nFirst Five Rows:")
    print(df.head())
def analyze_data_quality(df: pd.DataFrame) -> dict:
    """
    Analyze the quality of a dataset.
    """

    report = {
        "Rows": len(df),
        "Columns": len(df.columns),
        "Column Names": df.columns.tolist(),
        "Data Types": df.dtypes.to_dict(),
        "Missing Values": df.isnull().sum().to_dict(),
        "Duplicate Rows": int(df.duplicated().sum()),
        "Memory Usage (KB)": round(
            df.memory_usage(deep=True).sum() / 1024,
            2
        ),
        "Sample Data": df.head().to_string(index=False)
    }

    return report
def save_report(report_text: str):
    """
    Save the data quality report.
    """

    REPORT_PATH.mkdir(parents=True, exist_ok=True)

    report_file = REPORT_PATH / "data_quality_report.txt"

    with open(report_file, "w", encoding="utf-8") as file:
        file.write(report_text)

    print(f"\nReport saved to {report_file}")
def main():

    report_lines = []

    csv_files = list(RAW_DATA_PATH.glob("*.csv"))

    if not csv_files:
        print("No CSV files found.")
        return

    for csv_file in csv_files:

        df = load_dataset(csv_file)

        display_dataset_info(df, csv_file.name)

        quality = analyze_data_quality(df)

        report_lines.append(f"\n{'=' * 60}\n")
        report_lines.append(f"Dataset: {csv_file.name}\n")

        report_lines.append("=" * 70 + "\n")
        report_lines.append(f"Dataset: {csv_file.name}\n")
        report_lines.append("=" * 70 + "\n\n")

        report_lines.append(f"Rows: {quality['Rows']}\n")
        report_lines.append(f"Columns: {quality['Columns']}\n\n")

        report_lines.append("Column Names\n")
        report_lines.append("-" * 30 + "\n")

        for column in quality["Column Names"]:
            report_lines.append(f"- {column}\n")

        report_lines.append("\nData Types\n")
        report_lines.append("-" * 30 + "\n")

        for column, dtype in quality["Data Types"].items():
            report_lines.append(f"{column}: {dtype}\n")

        report_lines.append("\nMissing Values\n")
        report_lines.append("-" * 30 + "\n")

        for column, missing in quality["Missing Values"].items():
            report_lines.append(f"{column}: {missing}\n")

        report_lines.append(f"\nDuplicate Rows: {quality['Duplicate Rows']}\n")
        report_lines.append(f"Memory Usage (KB): {quality['Memory Usage (KB)']}\n")

        report_lines.append("\nSample Records\n")
        report_lines.append("-" * 30 + "\n")
        report_lines.append(quality["Sample Data"])

        report_lines.append("\n\n")

    save_report("".join(report_lines))
if __name__ == "__main__":
    main()