"""Inspect the ten canonical raw datasets and write a data-quality report."""

import logging
from pathlib import Path

import pandas as pd

from config import CANONICAL_DATASETS, RAW_DATA_PATH, REPORT_PATH

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")
logger = logging.getLogger(__name__)


def load_dataset(file_path: Path) -> pd.DataFrame:
    """Load a CSV dataset."""
    return pd.read_csv(file_path)


def analyze_data_quality(df: pd.DataFrame) -> dict:
    """Return basic quality statistics for a dataframe."""
    return {
        "rows": len(df),
        "columns": len(df.columns),
        "column_names": df.columns.tolist(),
        "data_types": {str(k): str(v) for k, v in df.dtypes.items()},
        "missing_values": df.isna().sum().to_dict(),
        "duplicate_rows": int(df.duplicated().sum()),
        "memory_kb": round(df.memory_usage(deep=True).sum() / 1024, 2),
    }


def main() -> None:
    """Inspect all required datasets."""
    REPORT_PATH.mkdir(parents=True, exist_ok=True)

    missing_files = [
        name for name in CANONICAL_DATASETS
        if not (RAW_DATA_PATH / name).exists()
    ]
    if missing_files:
        raise FileNotFoundError(
            "Missing required raw datasets:\n- " + "\n- ".join(missing_files)
        )

    report = []
    for name in CANONICAL_DATASETS:
        path = RAW_DATA_PATH / name
        df = load_dataset(path)
        q = analyze_data_quality(df)

        logger.info("%s | rows=%s | columns=%s | duplicates=%s",
                    name, q["rows"], q["columns"], q["duplicate_rows"])

        report.extend([
            "=" * 70,
            f"Dataset: {name}",
            f"Rows: {q['rows']}",
            f"Columns: {q['columns']}",
            f"Duplicate rows: {q['duplicate_rows']}",
            f"Columns: {q['column_names']}",
            f"Missing values: {q['missing_values']}",
            "",
        ])

    report_path = REPORT_PATH / "data_quality_report.txt"
    report_path.write_text("\n".join(report), encoding="utf-8")
    logger.info("Data-quality report saved to %s", report_path)


if __name__ == "__main__":
    main()
