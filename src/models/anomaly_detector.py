"""Anomaly detection for climate data."""

import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import joblib


class ClimateAnomalyDetector:
    """Detect anomalies in climate data using Isolation Forest."""

    def __init__(self, contamination=0.1, random_state=42):
        """
        Initialize anomaly detector.

        Args:
            contamination: Expected proportion of anomalies
            random_state: Random seed for reproducibility
        """
        self.model = IsolationForest(
            contamination=contamination,
            random_state=random_state,
            n_estimators=100
        )
        self.scaler = StandardScaler()
        self.fitted = False

    def prepare_features(self, df, value_column='value'):
        """
        Prepare features for anomaly detection.

        Args:
            df: DataFrame with climate data
            value_column: Name of value column

        Returns:
            Feature matrix
        """
        features = pd.DataFrame()

        # Original value
        features['value'] = df[value_column]

        # Rolling statistics
        for window in [7, 14, 30]:
            features[f'rolling_mean_{window}'] = df[value_column].rolling(window=window).mean()
            features[f'rolling_std_{window}'] = df[value_column].rolling(window=window).std()

        # Change from previous day
        features['daily_change'] = df[value_column].diff()

        # Seasonal features (if date column exists)
        if 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date'])
            features['day_of_year'] = df['date'].dt.dayofyear
            features['month'] = df['date'].dt.month

        # Fill NaN values using modern pandas syntax
        features = features.bfill().ffill()

        # If still NaN (e.g., single data point), fill with column mean or 0
        features = features.fillna(0)

        return features

    def train(self, df, value_column='value'):
        """
        Train anomaly detection model.

        Args:
            df: DataFrame with climate data
            value_column: Name of value column

        Returns:
            Fitted model
        """
        # Prepare features
        X = self.prepare_features(df, value_column)

        # Scale features
        X_scaled = self.scaler.fit_transform(X)

        # Train model
        self.model.fit(X_scaled)
        self.fitted = True

        return self.model

    def detect(self, df, value_column='value'):
        """
        Detect anomalies in data.

        Args:
            df: DataFrame with climate data
            value_column: Name of value column

        Returns:
            DataFrame with anomaly labels and scores
        """
        if not self.fitted:
            raise ValueError("Model not trained yet!")

        # Prepare features
        X = self.prepare_features(df, value_column)

        # Scale features
        X_scaled = self.scaler.transform(X)

        # Predict anomalies (-1 for anomaly, 1 for normal)
        predictions = self.model.predict(X_scaled)

        # Get anomaly scores (lower score = more anomalous)
        scores = self.model.score_samples(X_scaled)

        # Add results to dataframe
        result_df = df.copy()
        result_df['is_anomaly'] = predictions == -1
        result_df['anomaly_score'] = -scores  # Invert so higher = more anomalous

        return result_df

    def get_anomaly_summary(self, df_with_anomalies):
        """
        Get summary of detected anomalies.

        Args:
            df_with_anomalies: DataFrame with anomaly detection results

        Returns:
            Dictionary with anomaly summary
        """
        anomalies = df_with_anomalies[df_with_anomalies['is_anomaly'] == True]

        summary = {
            'total_anomalies': int(len(anomalies)),
            'anomaly_percentage': float(len(anomalies) / len(df_with_anomalies) * 100),
            'top_anomalies': anomalies.nlargest(10, 'anomaly_score')[
                ['date', 'value', 'anomaly_score']
            ].to_dict('records') if 'date' in anomalies.columns else [],
            'mean_anomaly_score': float(anomalies['anomaly_score'].mean()) if len(anomalies) > 0 else 0
        }

        return summary

    def save_model(self, model_path, scaler_path):
        """Save model and scaler."""
        joblib.dump(self.model, model_path)
        joblib.dump(self.scaler, scaler_path)

    def load_model(self, model_path, scaler_path):
        """Load model and scaler."""
        self.model = joblib.load(model_path)
        self.scaler = joblib.load(scaler_path)
        self.fitted = True


class TemperatureThresholdDetector:
    """Simple threshold-based anomaly detection for extreme temperatures."""

    def __init__(self, lower_percentile=5, upper_percentile=95):
        """
        Initialize threshold detector.

        Args:
            lower_percentile: Lower percentile for cold anomalies
            upper_percentile: Upper percentile for hot anomalies
        """
        self.lower_percentile = lower_percentile
        self.upper_percentile = upper_percentile
        self.lower_threshold = None
        self.upper_threshold = None

    def fit(self, temperature_data):
        """
        Calculate thresholds from historical data.

        Args:
            temperature_data: Array or Series of temperature values
        """
        self.lower_threshold = np.percentile(temperature_data, self.lower_percentile)
        self.upper_threshold = np.percentile(temperature_data, self.upper_percentile)

    def detect(self, temperature_data):
        """
        Detect extreme temperature events.

        Args:
            temperature_data: Array or Series of temperature values

        Returns:
            Dictionary with anomaly information
        """
        if self.lower_threshold is None or self.upper_threshold is None:
            raise ValueError("Detector not fitted yet!")

        is_cold_anomaly = temperature_data < self.lower_threshold
        is_hot_anomaly = temperature_data > self.upper_threshold

        result = {
            'is_cold_anomaly': is_cold_anomaly,
            'is_hot_anomaly': is_hot_anomaly,
            'is_any_anomaly': is_cold_anomaly | is_hot_anomaly,
            'lower_threshold': self.lower_threshold,
            'upper_threshold': self.upper_threshold
        }

        return result
