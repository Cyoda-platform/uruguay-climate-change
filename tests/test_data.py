"""Tests for data loading and preprocessing."""

import pytest
import pandas as pd
from src.data.load_data import load_raw_data
from src.data.preprocess import clean_data


def test_clean_data():
    """Test data cleaning function."""
    # Create sample data with duplicates and missing values
    df = pd.DataFrame({
        'A': [1, 2, 2, 3],
        'B': [4, 5, 5, 6]
    })

    cleaned = clean_data(df)

    # Check duplicates are removed
    assert len(cleaned) == 3
    assert cleaned['A'].tolist() == [1, 2, 3]


# Add more tests here
