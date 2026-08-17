"""Master execution script for the complete Mutual Fund Analytics ETL pipeline."""

from __future__ import annotations

import logging
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = PROJECT_ROOT / "scripts"

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")
logger = logging.getLogger(__name__)

STAGES = [
    ("Data Ingestion", "data_ingestion.py"),
    ("Live NAV Fetch", "fetch_nav.py"),
    ("Data Preprocessing", "preprocessing.py"),
    ("Data Validation", "data_validation.py"),
    ("SQLite Loading", "load_data.py"),
]


def run_stage(stage_name: str, script_name: str) -> None:
    """Execute one stage and stop the pipeline on failure."""
    script = SCRIPTS_DIR / script_name
    if not script.exists():
        raise FileNotFoundError(f"Required pipeline script not found: {script}")

    logger.info("=" * 70)
    logger.info("STARTING: %s", stage_name)

    result = subprocess.run(
        [sys.executable, str(script)],
        cwd=PROJECT_ROOT,
        check=False,
    )

    if result.returncode != 0:
        raise RuntimeError(
            f"{stage_name} failed with exit code {result.returncode}"
        )

    logger.info("COMPLETED: %s", stage_name)


def main() -> None:
    """Run every ETL stage in order."""
    logger.info("=" * 70)
    logger.info("MUTUAL FUND ANALYTICS — MASTER ETL PIPELINE")
    logger.info("Project root: %s", PROJECT_ROOT)

    try:
        for stage_name, script_name in STAGES:
            run_stage(stage_name, script_name)
    except Exception:
        logger.exception("PIPELINE FAILED")
        sys.exit(1)

    logger.info("=" * 70)
    logger.info("ALL PIPELINE STAGES COMPLETED SUCCESSFULLY")
    logger.info("=" * 70)


if __name__ == "__main__":
    main()
