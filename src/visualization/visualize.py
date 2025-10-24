"""Plotting and visualization functions."""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from pathlib import Path


# Set default style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)


def plot_time_series(df: pd.DataFrame, date_column: str, value_column: str,
                     title: str = "Time Series Plot", save_path: str = None):
    """
    Plot time series data.

    Args:
        df: DataFrame containing the data
        date_column: Name of the date column
        value_column: Name of the value column
        title: Plot title
        save_path: Optional path to save the figure
    """
    plt.figure(figsize=(14, 6))
    plt.plot(df[date_column], df[value_column], linewidth=2)
    plt.title(title, fontsize=16)
    plt.xlabel('Date', fontsize=12)
    plt.ylabel(value_column, fontsize=12)
    plt.xticks(rotation=45)
    plt.tight_layout()

    if save_path:
        Path(save_path).parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(save_path, dpi=300, bbox_inches='tight')

    plt.show()


def plot_correlation_matrix(df: pd.DataFrame, title: str = "Correlation Matrix",
                            save_path: str = None):
    """
    Plot correlation matrix heatmap.

    Args:
        df: DataFrame containing numeric columns
        title: Plot title
        save_path: Optional path to save the figure
    """
    plt.figure(figsize=(12, 10))
    correlation = df.select_dtypes(include=['float64', 'int64']).corr()

    sns.heatmap(correlation, annot=True, cmap='coolwarm', center=0,
                fmt='.2f', square=True, linewidths=1)
    plt.title(title, fontsize=16)
    plt.tight_layout()

    if save_path:
        Path(save_path).parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(save_path, dpi=300, bbox_inches='tight')

    plt.show()


def plot_feature_importance(feature_names, importance_values,
                           title: str = "Feature Importance",
                           save_path: str = None, top_n: int = 20):
    """
    Plot feature importance.

    Args:
        feature_names: List of feature names
        importance_values: Array of importance values
        title: Plot title
        save_path: Optional path to save the figure
        top_n: Number of top features to display
    """
    importance_df = pd.DataFrame({
        'feature': feature_names,
        'importance': importance_values
    }).sort_values('importance', ascending=False).head(top_n)

    plt.figure(figsize=(10, 8))
    sns.barplot(data=importance_df, x='importance', y='feature', palette='viridis')
    plt.title(title, fontsize=16)
    plt.xlabel('Importance', fontsize=12)
    plt.ylabel('Feature', fontsize=12)
    plt.tight_layout()

    if save_path:
        Path(save_path).parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(save_path, dpi=300, bbox_inches='tight')

    plt.show()


def plot_predictions_vs_actual(y_true, y_pred,
                               title: str = "Predictions vs Actual",
                               save_path: str = None):
    """
    Plot predicted vs actual values.

    Args:
        y_true: True values
        y_pred: Predicted values
        title: Plot title
        save_path: Optional path to save the figure
    """
    plt.figure(figsize=(10, 8))
    plt.scatter(y_true, y_pred, alpha=0.5)

    # Plot perfect prediction line
    min_val = min(y_true.min(), y_pred.min())
    max_val = max(y_true.max(), y_pred.max())
    plt.plot([min_val, max_val], [min_val, max_val], 'r--', linewidth=2, label='Perfect Prediction')

    plt.title(title, fontsize=16)
    plt.xlabel('Actual Values', fontsize=12)
    plt.ylabel('Predicted Values', fontsize=12)
    plt.legend()
    plt.tight_layout()

    if save_path:
        Path(save_path).parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(save_path, dpi=300, bbox_inches='tight')

    plt.show()
