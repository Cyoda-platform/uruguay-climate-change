#!/usr/bin/env python3
"""
Train all ML models for climate analysis.

This script trains:
1. LSTM for temperature forecasting
2. Prophet for seasonal analysis
3. Anomaly detection models
4. Climate pattern classifier
"""

import sys
from pathlib import Path
import pandas as pd
import numpy as np

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.models.lstm_model import LSTMTemperatureForecaster
from src.models.prophet_model import ProphetSeasonalAnalyzer
from src.models.anomaly_detector import ClimateAnomalyDetector
from src.models.climate_classifier import ClimatePatternClassifier
from src.utils.helpers import ensure_dir, setup_logging

# Setup logging
setup_logging('logs/training.log')
import logging
logger = logging.getLogger(__name__)


def generate_sample_data(n_days=2000):
    """
    Generate sample climate data for training.
    Replace this with actual data loading.
    """
    logger.info("Generating sample climate data...")

    dates = pd.date_range(start='2018-01-01', periods=n_days, freq='D')

    # Temperature: base + seasonal + trend + noise
    base_temp = 18
    seasonal = 8 * np.sin(2 * np.pi * np.arange(n_days) / 365.25)
    trend = 0.002 * np.arange(n_days)  # Warming trend
    noise = np.random.normal(0, 2, n_days)
    temperature = base_temp + seasonal + trend + noise

    # Precipitation: gamma distribution with seasonal variation
    seasonal_precip = 1 + 0.3 * np.sin(2 * np.pi * np.arange(n_days) / 365.25)
    precipitation = np.random.gamma(2, 3, n_days) * seasonal_precip

    df = pd.DataFrame({
        'date': dates,
        'temperature': temperature,
        'precipitation': precipitation
    })

    return df


def train_lstm_model(df):
    """Train LSTM temperature forecasting model."""
    logger.info("Training LSTM model...")

    model = LSTMTemperatureForecaster(lookback=60, forecast_horizon=30)

    # Train
    history = model.train(
        temperature_data=df['temperature'].values,
        epochs=50,
        batch_size=32,
        validation_split=0.2
    )

    # Save model
    ensure_dir('models')
    model.save_model('models/lstm_temperature.keras', 'models/lstm_scaler.pkl')

    logger.info(f"LSTM model trained. Final loss: {history.history['loss'][-1]:.4f}")

    return model


def train_prophet_model(df):
    """Train Prophet seasonal analysis model."""
    logger.info("Training Prophet model...")

    model = ProphetSeasonalAnalyzer(
        yearly_seasonality=True,
        weekly_seasonality=False,
        daily_seasonality=False
    )

    # Train
    model.train(df, date_column='date', value_column='temperature')

    # Save model
    ensure_dir('models')
    model.save_model('models/prophet_seasonal.pkl')

    logger.info("Prophet model trained successfully")

    return model


def train_anomaly_detector(df):
    """Train anomaly detection model."""
    logger.info("Training anomaly detector...")

    detector = ClimateAnomalyDetector(contamination=0.05)

    # Train
    detector.train(df, value_column='temperature')

    # Save model
    ensure_dir('models')
    detector.save_model('models/anomaly_model.pkl', 'models/anomaly_scaler.pkl')

    logger.info("Anomaly detector trained successfully")

    return detector


def train_classifier(df):
    """Train climate pattern classifier."""
    logger.info("Training climate pattern classifier...")

    classifier = ClimatePatternClassifier(n_estimators=100)

    # Train
    metrics = classifier.train(
        df,
        temp_column='temperature',
        precip_column='precipitation',
        test_size=0.2
    )

    # Save model
    ensure_dir('models')
    classifier.save_model('models/climate_classifier.pkl')

    logger.info(f"Classifier trained. Accuracy: {metrics['accuracy']:.4f}")

    return classifier, metrics


def main():
    """Main training pipeline."""
    logger.info("=" * 50)
    logger.info("Starting ML model training pipeline")
    logger.info("=" * 50)

    # Generate/load data
    df = generate_sample_data(n_days=2000)
    logger.info(f"Loaded {len(df)} days of climate data")

    # Train all models
    try:
        # 1. LSTM Temperature Forecaster
        lstm_model = train_lstm_model(df)

        # 2. Prophet Seasonal Analyzer
        prophet_model = train_prophet_model(df)

        # 3. Anomaly Detector
        anomaly_detector = train_anomaly_detector(df)

        # 4. Climate Classifier
        classifier, metrics = train_classifier(df)

        logger.info("=" * 50)
        logger.info("All models trained successfully!")
        logger.info("=" * 50)

        # Print summary
        print("\n" + "=" * 50)
        print("TRAINING SUMMARY")
        print("=" * 50)
        print("\n✓ LSTM Temperature Forecaster - Saved to models/lstm_temperature.keras")
        print("✓ Prophet Seasonal Analyzer - Saved to models/prophet_seasonal.pkl")
        print("✓ Anomaly Detector - Saved to models/anomaly_model.pkl")
        print(f"✓ Climate Classifier - Saved to models/climate_classifier.pkl (Accuracy: {metrics['accuracy']:.2%})")
        print("\n" + "=" * 50)

    except Exception as e:
        logger.error(f"Error during training: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    main()
