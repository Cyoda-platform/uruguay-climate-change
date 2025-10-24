"""Tests for feature engineering."""

import pytest
import pandas as pd
from src.features.build_features import create_time_features


def test_create_time_features():
    """Test time feature creation."""
    df = pd.DataFrame({
        'date': ['2023-01-15', '2023-06-20', '2023-12-31'],
        'value': [1, 2, 3]
    })

    result = create_time_features(df, 'date')

    assert 'year' in result.columns
    assert 'month' in result.columns
    assert 'day' in result.columns
    assert result['year'].iloc[0] == 2023
    assert result['month'].iloc[0] == 1
    assert result['day'].iloc[0] == 15


# Add more tests here
