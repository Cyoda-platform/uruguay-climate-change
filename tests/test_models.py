"""Tests for model training and prediction."""

import pytest
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from src.models.train_model import split_data, train_model, evaluate_model


def test_split_data():
    """Test data splitting function."""
    df = pd.DataFrame({
        'feature1': np.arange(100),
        'feature2': np.arange(100) * 2,
        'target': np.arange(100) * 3
    })

    X_train, X_test, y_train, y_test = split_data(df, 'target', test_size=0.2)

    assert len(X_train) == 80
    assert len(X_test) == 20
    assert 'target' not in X_train.columns
    assert 'target' not in X_test.columns


def test_train_model():
    """Test model training."""
    X_train = pd.DataFrame({'feature': np.arange(10)})
    y_train = np.arange(10) * 2

    model = LinearRegression()
    trained_model = train_model(X_train, y_train, model)

    assert hasattr(trained_model, 'coef_')
    assert trained_model.coef_[0] == pytest.approx(2.0, rel=1e-5)


# Add more tests here
