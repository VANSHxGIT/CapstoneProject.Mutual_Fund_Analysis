"""
Master execution script for the Mutual Fund Analytics project.

Runs the main ETL stages in sequence:

1. Data ingestion
2. NAV fetching
3. Data preprocessing
4. Data validation
5. SQLite database loading

Usage:
    python scripts/run_pipeline.py
"""

from __future__ import annotations

import logging
import subprocess
import sys
from pathlib import Path


# =========================================================
# Project Paths
# =========================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = PROJECT_ROOT / "scripts"


# =========================================================
# Logging
# =========================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)


# =========================================================
# Pipeline Stages
# =========================================================

STAGES = [
    ("Data Ingestion", "data_ingestion.py"),
    ("NAV Fetching", "fetch_nav.py"),
    ("Data Preprocessing", "preprocessing.py"),
    ("Data Validation", "data_validation.py"),
    ("SQLite Loading", "load_data.py"),
]


# =========================================================
# Run Script
# =========================================================

def run_stage(stage_name: str, script_name: str) -> None:
    """
    Execute one pipeline stage.

    Parameters
    ----------
    stage_name : str
        Human-readable name of the stage.

    script_name : str
        Python script to execute.

    Raises
    ------
    RuntimeError
        If the stage exits with a non-zero status.
    """

    script_path = SCRIPTS_DIR / script_name

    if not script_path.exists():
        raise FileNotFoundError(
            f"Pipeline script not found: {script_path}"
        )

    logger.info("=" * 70)
    logger.info("STARTING: %s", stage_name)
    logger.info("=" * 70)

    result = subprocess.run(
        [sys.executable, str(script_path)],
        cwd=PROJECT_ROOT,
        check=False
    )

    if result.returncode != 0:
        raise RuntimeError(
            f"{stage_name} failed with exit code "
            f"{result.returncode}."
        )

    logger.info("=" * 70)
    logger.info("COMPLETED: %s", stage_name)
    logger.info("=" * 70)


# =========================================================
# Main Pipeline
# =========================================================

def main() -> None:
    """Run the complete Mutual Fund Analytics ETL pipeline."""

    logger.info("=" * 70)
    logger.info("MUTUAL FUND ANALYTICS — MASTER PIPELINE")
    logger.info("=" * 70)

    logger.info("Project root: %s", PROJECT_ROOT)

    try:
        for stage_name, script_name in STAGES:
            run_stage(stage_name, script_name)

    except Exception:
        logger.exception(
            "PIPELINE FAILED. Please review the error above."
        )
        sys.exit(1)

    logger.info("=" * 70)
    logger.info("ALL PIPELINE STAGES COMPLETED SUCCESSFULLY")
    logger.info("=" * 70)


if __name__ == "__main__":
    main()