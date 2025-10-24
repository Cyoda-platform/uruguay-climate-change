"""Model training scripts."""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import joblib
from pathlib import Path


def split_data(df: pd.DataFrame, target_column: str, test_size: float = 0.2, random_state: int = 42):
    """
    Split data into train and test sets.

    Args:
        df: Feature DataFrame
        target_column: Name of the target variable
        test_size: Proportion of test set
        random_state: Random seed for reproducibility

    Returns:
        X_train, X_test, y_train, y_test
    """
    X = df.drop(columns=[target_column])
    y = df[target_column]

    return train_test_split(X, y, test_size=test_size, random_state=random_state)


def train_model(X_train, y_train, model):
    """
    Train a machine learning model.

    Args:
        X_train: Training features
        y_train: Training target
        model: Sklearn-compatible model instance

    Returns:
        Trained model
    """
    model.fit(X_train, y_train)
    return model


def evaluate_model(model, X_test, y_test):
    """
    Evaluate model performance.

    Args:
        model: Trained model
        X_test: Test features
        y_test: Test target

    Returns:
        Dictionary of evaluation metrics
    """
    predictions = model.predict(X_test)

    metrics = {
        'mse': mean_squared_error(y_test, predictions),
        'rmse': np.sqrt(mean_squared_error(y_test, predictions)),
        'r2': r2_score(y_test, predictions)
    }

    return metrics


def save_model(model, file_path: str):
    """
    Save trained model to disk.

    Args:
        model: Trained model
        file_path: Path to save the model
    """
    Path(file_path).parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, file_path)
    print(f"Model saved to {file_path}")
