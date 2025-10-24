"""API routes for climate data and predictions."""

from flask import Blueprint, jsonify, request
from datetime import datetime, timedelta
import numpy as np
import pandas as pd
from pathlib import Path

api_bp = Blueprint('api', __name__)


@api_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint for Docker and monitoring."""
    import sys
    import os

    health_status = {
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'version': '1.0.0',
        'python_version': sys.version.split()[0],
        'dependencies': {
            'flask': True,
            'pandas': True,
            'numpy': True,
        }
    }

    # Check if ML dependencies are available
    try:
        import tensorflow
        health_status['dependencies']['tensorflow'] = True
    except ImportError:
        health_status['dependencies']['tensorflow'] = False

    try:
        import google.generativeai
        health_status['dependencies']['gemini'] = True
    except ImportError:
        health_status['dependencies']['gemini'] = False

    # Check if models directory exists
    models_dir = Path(__file__).parent.parent.parent / 'models'
    health_status['models_directory'] = models_dir.exists()

    # Check if data directory exists
    data_dir = Path(__file__).parent.parent.parent / 'data'
    health_status['data_directory'] = data_dir.exists()

    return jsonify(health_status), 200


@api_bp.route('/climate-data', methods=['GET'])
def get_climate_data():
    """
    Get historical climate data.

    Query params:
        start_date: Start date (YYYY-MM-DD)
        end_date: End date (YYYY-MM-DD)
        metric: Climate metric (temperature, precipitation, etc.)
    """
    # Parse query parameters
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    metric = request.args.get('metric', 'temperature')

    # TODO: Replace with actual data loading
    # For now, generate sample data
    data = generate_sample_climate_data(start_date, end_date, metric)

    return jsonify({
        'success': True,
        'data': data,
        'metric': metric
    })


@api_bp.route('/predictions', methods=['POST'])
def get_predictions():
    """
    Get climate predictions.

    Request body:
        {
            "start_date": "2024-01-01",
            "end_date": "2024-12-31",
            "metric": "temperature"
        }
    """
    data = request.get_json()

    start_date = data.get('start_date')
    end_date = data.get('end_date')
    metric = data.get('metric', 'temperature')

    # TODO: Load model and make actual predictions
    # For now, generate sample predictions
    predictions = generate_sample_predictions(start_date, end_date, metric)

    return jsonify({
        'success': True,
        'predictions': predictions,
        'metric': metric
    })


@api_bp.route('/statistics', methods=['GET'])
def get_statistics():
    """
    Get climate statistics summary.
    """
    # TODO: Calculate from actual data
    stats = {
        'temperature': {
            'mean': 18.5,
            'min': -2.0,
            'max': 35.0,
            'trend': 'increasing',
            'change_rate': 0.15  # degrees per decade
        },
        'precipitation': {
            'mean': 1200,  # mm per year
            'min': 800,
            'max': 1600,
            'trend': 'stable',
            'change_rate': 0.02
        }
    }

    return jsonify({
        'success': True,
        'statistics': stats
    })


@api_bp.route('/trends', methods=['GET'])
def get_trends():
    """
    Get long-term climate trends.
    """
    metric = request.args.get('metric', 'temperature')

    # TODO: Calculate from actual data
    trends = generate_sample_trends(metric)

    return jsonify({
        'success': True,
        'trends': trends,
        'metric': metric
    })


def generate_sample_climate_data(start_date, end_date, metric):
    """Generate sample climate data for demonstration."""
    if not start_date:
        start_date = '2020-01-01'
    if not end_date:
        end_date = '2023-12-31'

    start = pd.to_datetime(start_date)
    end = pd.to_datetime(end_date)

    dates = pd.date_range(start=start, end=end, freq='D')

    # Generate sample data based on metric
    if metric == 'temperature':
        # Simulate temperature with seasonal pattern
        base = 18
        seasonal = 8 * np.sin(2 * np.pi * np.arange(len(dates)) / 365.25)
        noise = np.random.normal(0, 2, len(dates))
        values = base + seasonal + noise
    elif metric == 'precipitation':
        # Simulate precipitation
        values = np.random.gamma(2, 3, len(dates))
    else:
        values = np.random.randn(len(dates)) * 10 + 50

    data = [
        {
            'date': date.strftime('%Y-%m-%d'),
            'value': float(value)
        }
        for date, value in zip(dates, values)
    ]

    return data


def generate_sample_predictions(start_date, end_date, metric):
    """Generate sample predictions for demonstration."""
    if not start_date:
        start_date = '2024-01-01'
    if not end_date:
        end_date = '2024-12-31'

    start = pd.to_datetime(start_date)
    end = pd.to_datetime(end_date)

    dates = pd.date_range(start=start, end=end, freq='D')

    # Generate predictions with confidence intervals
    if metric == 'temperature':
        base = 19  # Slightly higher than historical
        seasonal = 8 * np.sin(2 * np.pi * np.arange(len(dates)) / 365.25)
        values = base + seasonal
        uncertainty = 1.5
    else:
        values = np.random.randn(len(dates)) * 10 + 52
        uncertainty = 3.0

    predictions = [
        {
            'date': date.strftime('%Y-%m-%d'),
            'predicted': float(value),
            'lower_bound': float(value - uncertainty),
            'upper_bound': float(value + uncertainty)
        }
        for date, value in zip(dates, values)
    ]

    return predictions


def generate_sample_trends(metric):
    """Generate sample trend data."""
    years = list(range(1990, 2024))

    if metric == 'temperature':
        # Simulate increasing temperature trend
        base_values = 17 + 0.015 * np.arange(len(years))
        values = base_values + np.random.normal(0, 0.3, len(years))
    else:
        # Simulate stable precipitation
        values = 1200 + np.random.normal(0, 100, len(years))

    trends = [
        {
            'year': year,
            'value': float(value)
        }
        for year, value in zip(years, values)
    ]

    return trends
