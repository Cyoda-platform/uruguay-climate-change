"""Model prediction and inference."""

import pandas as pd
import joblib


def load_model(file_path: str):
    """
    Load a trained model from disk.

    Args:
        file_path: Path to the saved model

    Returns:
        Loaded model
    """
    return joblib.load(file_path)


def make_predictions(model, X: pd.DataFrame):
    """
    Make predictions using a trained model.

    Args:
        model: Trained model
        X: Feature DataFrame

    Returns:
        Array of predictions
    """
    return model.predict(X)


def predict_with_confidence(model, X: pd.DataFrame):
    """
    Make predictions with confidence intervals if supported.

    Args:
        model: Trained model
        X: Feature DataFrame

    Returns:
        Predictions and confidence intervals
    """
    predictions = model.predict(X)

    # Add confidence interval logic if model supports it
    # e.g., for sklearn ensemble models

    return predictions
