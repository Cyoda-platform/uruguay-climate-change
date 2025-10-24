"""ML model API routes."""

import sys
from pathlib import Path
from flask import Blueprint, jsonify, request
import numpy as np
import pandas as pd

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.models.lstm_model import LSTMTemperatureForecaster
from src.models.prophet_model import ProphetSeasonalAnalyzer
from src.models.anomaly_detector import ClimateAnomalyDetector
from src.models.climate_classifier import ClimatePatternClassifier

ml_bp = Blueprint('ml', __name__)

# Global model instances (loaded on demand)
lstm_model = None
prophet_model = None
anomaly_detector = None
climate_classifier = None


def load_lstm_model():
    """Load LSTM model if not already loaded."""
    global lstm_model
    if lstm_model is None:
        try:
            lstm_model = LSTMTemperatureForecaster()
            lstm_model.load_model('models/lstm_temperature.keras', 'models/lstm_scaler.pkl')
        except Exception as e:
            print(f"LSTM model not found: {e}")
    return lstm_model


def load_prophet_model():
    """Load Prophet model if not already loaded."""
    global prophet_model
    if prophet_model is None:
        try:
            prophet_model = ProphetSeasonalAnalyzer()
            prophet_model.load_model('models/prophet_seasonal.pkl')
        except Exception as e:
            print(f"Prophet model not found: {e}")
    return prophet_model


def load_anomaly_detector():
    """Load anomaly detector if not already loaded."""
    global anomaly_detector
    if anomaly_detector is None:
        try:
            anomaly_detector = ClimateAnomalyDetector()
            anomaly_detector.load_model('models/anomaly_model.pkl', 'models/anomaly_scaler.pkl')
        except Exception as e:
            print(f"Anomaly detector not found: {e}")
    return anomaly_detector


def load_climate_classifier():
    """Load climate classifier if not already loaded."""
    global climate_classifier
    if climate_classifier is None:
        try:
            climate_classifier = ClimatePatternClassifier()
            climate_classifier.load_model('models/climate_classifier.pkl')
        except Exception as e:
            print(f"Climate classifier not found: {e}")
    return climate_classifier


@ml_bp.route('/lstm-forecast', methods=['POST'])
def lstm_forecast():
    """
    Get LSTM temperature forecast.

    Request body:
        {
            "recent_temperatures": [18.5, 19.2, ...],  # Last 60 days
            "forecast_days": 30
        }
    """
    try:
        data = request.get_json()
        recent_temps = data.get('recent_temperatures', [])
        forecast_days = data.get('forecast_days', 30)

        # Load model
        model = load_lstm_model()
        if model is None:
            return jsonify({
                'success': False,
                'error': 'LSTM model not trained yet. Run train_ml_models.py first.'
            }), 503

        # Generate forecast
        if len(recent_temps) < 60:
            # Generate sample data if not enough provided
            recent_temps = 18 + 8 * np.sin(2 * np.pi * np.arange(60) / 365.25) + np.random.normal(0, 1, 60)

        predictions, lower, upper = model.predict(
            recent_data=np.array(recent_temps),
            steps=forecast_days
        )

        # Format response
        forecast_dates = pd.date_range(start=pd.Timestamp.now(), periods=forecast_days, freq='D')

        forecast_data = [
            {
                'date': date.strftime('%Y-%m-%d'),
                'predicted': float(pred),
                'lower_bound': float(low),
                'upper_bound': float(up)
            }
            for date, pred, low, up in zip(forecast_dates, predictions, lower, upper)
        ]

        return jsonify({
            'success': True,
            'forecast': forecast_data,
            'model': 'LSTM',
            'forecast_days': forecast_days
        })

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@ml_bp.route('/prophet-forecast', methods=['GET'])
def prophet_forecast():
    """Get Prophet seasonal forecast."""
    try:
        forecast_days = int(request.args.get('days', 365))

        # Load model
        model = load_prophet_model()
        if model is None:
            return jsonify({
                'success': False,
                'error': 'Prophet model not trained yet. Run train_ml_models.py first.'
            }), 503

        # Generate forecast
        forecast = model.forecast(periods=forecast_days, freq='D')
        summary = model.get_forecast_summary(forecast, last_n=min(90, forecast_days))

        return jsonify({
            'success': True,
            'forecast': summary['predictions'][:100],  # Limit to 100 days for response size
            'trend_direction': summary['trend_direction'],
            'mean_prediction': summary['mean_prediction'],
            'uncertainty_range': summary['uncertainty_range'],
            'model': 'Prophet'
        })

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@ml_bp.route('/detect-anomalies', methods=['POST'])
def detect_anomalies():
    """
    Detect anomalies in climate data.

    Request body:
        {
            "data": [
                {"date": "2024-01-01", "value": 18.5},
                ...
            ]
        }
    """
    try:
        data = request.get_json()
        climate_data = data.get('data', [])

        if not climate_data:
            return jsonify({'success': False, 'error': 'No data provided'}), 400

        # Load model
        detector = load_anomaly_detector()
        if detector is None:
            return jsonify({
                'success': False,
                'error': 'Anomaly detector not trained yet. Run train_ml_models.py first.'
            }), 503

        # Prepare dataframe
        df = pd.DataFrame(climate_data)

        # Detect anomalies
        results = detector.detect(df, value_column='value')
        summary = detector.get_anomaly_summary(results)

        # Format response
        anomalies = results[results['is_anomaly'] == True]

        return jsonify({
            'success': True,
            'total_anomalies': summary['total_anomalies'],
            'anomaly_percentage': summary['anomaly_percentage'],
            'anomalies': anomalies[['date', 'value', 'anomaly_score']].to_dict('records'),
            'model': 'IsolationForest'
        })

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@ml_bp.route('/classify-patterns', methods=['POST'])
def classify_patterns():
    """
    Classify climate patterns.

    Request body:
        {
            "data": [
                {"date": "2024-01-01", "temperature": 18.5, "precipitation": 2.3},
                ...
            ]
        }
    """
    try:
        data = request.get_json()
        climate_data = data.get('data', [])

        if not climate_data:
            return jsonify({'success': False, 'error': 'No data provided'}), 400

        # Load model
        classifier = load_climate_classifier()
        if classifier is None:
            return jsonify({
                'success': False,
                'error': 'Climate classifier not trained yet. Run train_ml_models.py first.'
            }), 503

        # Prepare dataframe
        df = pd.DataFrame(climate_data)

        # Classify
        predictions, probabilities = classifier.predict(
            df,
            temp_column='temperature',
            precip_column='precipitation'
        )

        # Format response
        results = []
        for i, (pred, prob) in enumerate(zip(predictions, probabilities)):
            results.append({
                'date': climate_data[i].get('date'),
                'pattern': pred,
                'confidence': float(prob.max())
            })

        return jsonify({
            'success': True,
            'classifications': results[:100],  # Limit response size
            'model': 'RandomForest'
        })

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@ml_bp.route('/model-status', methods=['GET'])
def model_status():
    """Check which ML models are available."""
    import os

    models_dir = Path('models')
    models_dir.mkdir(exist_ok=True)

    status = {
        'lstm': os.path.exists('models/lstm_temperature.keras'),
        'prophet': os.path.exists('models/prophet_seasonal.pkl'),
        'anomaly_detector': os.path.exists('models/anomaly_model.pkl'),
        'classifier': os.path.exists('models/climate_classifier.pkl')
    }

    return jsonify({
        'success': True,
        'models': status,
        'all_trained': all(status.values())
    })
