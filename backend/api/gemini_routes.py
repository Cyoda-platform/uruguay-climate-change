"""Gemini AI insights API routes."""

import sys
from pathlib import Path
from flask import Blueprint, jsonify, request
import os

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

try:
    from src.utils.gemini_ai import GeminiClimateAnalyst
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

gemini_bp = Blueprint('gemini', __name__)

# Global Gemini client
gemini_client = None


def get_gemini_client():
    """Get or create Gemini client."""
    global gemini_client

    if not GEMINI_AVAILABLE:
        return None

    if gemini_client is None:
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            return None
        try:
            gemini_client = GeminiClimateAnalyst(api_key=api_key)
        except Exception as e:
            print(f"Failed to initialize Gemini: {e}")
            return None

    return gemini_client


@gemini_bp.route('/climate-summary', methods=['POST'])
def climate_summary():
    """
    Generate AI climate summary.

    Request body:
        {
            "climate_data": {
                "temperature": {...},
                "precipitation": {...},
                "trends": {...}
            }
        }
    """
    try:
        client = get_gemini_client()
        if not client:
            return jsonify({
                'success': False,
                'error': 'Gemini AI not configured. Set GEMINI_API_KEY environment variable.'
            }), 503

        data = request.get_json()
        climate_data = data.get('climate_data', {})

        if not climate_data:
            return jsonify({'success': False, 'error': 'No climate data provided'}), 400

        # Generate summary
        summary = client.generate_climate_summary(climate_data)

        return jsonify({
            'success': True,
            'summary': summary,
            'type': 'climate_summary'
        })

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@gemini_bp.route('/ml-insights', methods=['POST'])
def ml_insights():
    """
    Generate insights from ML predictions.

    Request body:
        {
            "ml_results": {
                "lstm_forecast": [...],
                "prophet_forecast": [...],
                "trends": {...}
            }
        }
    """
    try:
        client = get_gemini_client()
        if not client:
            return jsonify({
                'success': False,
                'error': 'Gemini AI not configured. Set GEMINI_API_KEY environment variable.'
            }), 503

        data = request.get_json()
        ml_results = data.get('ml_results', {})

        if not ml_results:
            return jsonify({'success': False, 'error': 'No ML results provided'}), 400

        # Generate insights
        insights = client.generate_ml_insights(ml_results)

        return jsonify({
            'success': True,
            'insights': insights,
            'type': 'ml_insights'
        })

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@gemini_bp.route('/anomaly-report', methods=['POST'])
def anomaly_report():
    """
    Generate anomaly analysis report.

    Request body:
        {
            "anomalies": [
                {"date": "2024-01-15", "value": 35.5, "anomaly_score": 0.95},
                ...
            ]
        }
    """
    try:
        client = get_gemini_client()
        if not client:
            return jsonify({
                'success': False,
                'error': 'Gemini AI not configured.'
            }), 503

        data = request.get_json()
        anomalies = data.get('anomalies', [])

        if not anomalies:
            return jsonify({'success': False, 'error': 'No anomalies provided'}), 400

        # Generate report
        report = client.generate_anomaly_report(anomalies)

        return jsonify({
            'success': True,
            'report': report,
            'type': 'anomaly_report'
        })

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@gemini_bp.route('/recommendations', methods=['POST'])
def recommendations():
    """
    Generate actionable recommendations.

    Request body:
        {
            "analysis_summary": {
                "current_conditions": {...},
                "predictions": {...},
                "anomalies": {...}
            }
        }
    """
    try:
        client = get_gemini_client()
        if not client:
            return jsonify({
                'success': False,
                'error': 'Gemini AI not configured.'
            }), 503

        data = request.get_json()
        analysis_summary = data.get('analysis_summary', {})

        if not analysis_summary:
            return jsonify({'success': False, 'error': 'No analysis data provided'}), 400

        # Generate recommendations
        recs = client.generate_recommendations(analysis_summary)

        return jsonify({
            'success': True,
            'recommendations': recs,
            'type': 'recommendations'
        })

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@gemini_bp.route('/executive-summary', methods=['POST'])
def executive_summary():
    """
    Generate executive summary of full analysis.

    Request body:
        {
            "full_analysis": {
                "statistics": {...},
                "predictions": {...},
                "anomalies": {...},
                "trends": {...}
            }
        }
    """
    try:
        client = get_gemini_client()
        if not client:
            return jsonify({
                'success': False,
                'error': 'Gemini AI not configured.'
            }), 503

        data = request.get_json()
        full_analysis = data.get('full_analysis', {})

        if not full_analysis:
            return jsonify({'success': False, 'error': 'No analysis data provided'}), 400

        # Generate executive summary
        summary = client.generate_executive_summary(full_analysis)

        return jsonify({
            'success': True,
            'executive_summary': summary,
            'type': 'executive_summary'
        })

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@gemini_bp.route('/seasonal-narrative', methods=['POST'])
def seasonal_narrative():
    """Generate seasonal forecast narrative."""
    try:
        client = get_gemini_client()
        if not client:
            return jsonify({
                'success': False,
                'error': 'Gemini AI not configured.'
            }), 503

        data = request.get_json()
        seasonal_data = data.get('seasonal_data', {})

        narrative = client.generate_seasonal_forecast_narrative(seasonal_data)

        return jsonify({
            'success': True,
            'narrative': narrative,
            'type': 'seasonal_narrative'
        })

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@gemini_bp.route('/status', methods=['GET'])
def gemini_status():
    """Check Gemini AI availability."""
    api_key = os.getenv('GEMINI_API_KEY')

    return jsonify({
        'success': True,
        'available': GEMINI_AVAILABLE and api_key is not None,
        'configured': api_key is not None,
        'sdk_installed': GEMINI_AVAILABLE
    })
