"""Data loading utilities."""

import pandas as pd
from pathlib import Path


def load_raw_data(file_path: str) -> pd.DataFrame:
    """
    Load raw data from file.

    Args:
        file_path: Path to the data file

    Returns:
        DataFrame containing the raw data
    """
    path = Path(file_path)

    if path.suffix == '.csv':
        return pd.read_csv(file_path)
    elif path.suffix in ['.xlsx', '.xls']:
        return pd.read_excel(file_path)
    elif path.suffix == '.json':
        return pd.read_json(file_path)
    else:
        raise ValueError(f"Unsupported file format: {path.suffix}")


def load_processed_data(file_path: str) -> pd.DataFrame:
    """
    Load processed data from file.

    Args:
        file_path: Path to the processed data file

    Returns:
        DataFrame containing the processed data
    """
    return pd.read_parquet(file_path)
