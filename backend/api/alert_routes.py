"""Climate Alert API routes with Cyoda MCP integration."""

import sys
from pathlib import Path
from flask import Blueprint, jsonify, request
import pandas as pd
from datetime import datetime

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.utils.cyoda_client import CyodaAlertClient
from src.services.alert_service import ClimateAlertService

alert_bp = Blueprint('alerts', __name__)

# Initialize clients
cyoda_client = CyodaAlertClient()

# Service instance (will be initialized with dependencies)
alert_service = None


def get_alert_service():
    """Get or create alert service with dependencies."""
    global alert_service

    if alert_service is None:
        # Try to load anomaly detector
        try:
            from src.models.anomaly_detector import ClimateAnomalyDetector
            anomaly_detector = ClimateAnomalyDetector()
            try:
                anomaly_detector.load_model('models/anomaly_model.pkl', 'models/anomaly_scaler.pkl')
            except:
                print("Anomaly model not loaded")
                anomaly_detector = None
        except ImportError:
            anomaly_detector = None

        # Try to load Gemini client
        try:
            import os
            from src.utils.gemini_ai import GeminiClimateAnalyst
            api_key = os.getenv('GEMINI_API_KEY')
            gemini_client = GeminiClimateAnalyst(api_key=api_key) if api_key else None
        except:
            gemini_client = None

        alert_service = ClimateAlertService(
            anomaly_detector=anomaly_detector,
            gemini_client=gemini_client,
            cyoda_client=cyoda_client
        )

    return alert_service


@alert_bp.route('/detect', methods=['POST'])
def detect_alerts():
    """
    Detect anomalies and create alerts in Cyoda.

    Request body:
        {
            "data": [
                {"date": "2024-01-01", "value": 38.5},
                ...
            ],
            "metric": "temperature",
            "value_column": "value",
            "use_ai_analysis": true
        }

    Note: This endpoint prepares alert specifications.
    Actual Cyoda entity creation happens via MCP tools.
    """
    try:
        data = request.get_json()
        climate_data = data.get('data', [])
        metric = data.get('metric', 'temperature')
        value_column = data.get('value_column', 'value')
        use_ai_analysis = data.get('use_ai_analysis', True)

        if not climate_data:
            return jsonify({'success': False, 'error': 'No climate data provided'}), 400

        # Convert to DataFrame
        df = pd.DataFrame(climate_data)

        # Get service
        service = get_alert_service()

        # Detect alerts
        alert_specs = service.detect_and_create_alerts(
            climate_data=df,
            value_column=value_column,
            metric=metric,
            use_ai_analysis=use_ai_analysis
        )

        return jsonify({
            'success': True,
            'alerts_detected': len(alert_specs),
            'alert_specifications': alert_specs,
            'message': 'Alert specifications generated. Use MCP tools to create entities in Cyoda.'
        })

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@alert_bp.route('/create', methods=['POST'])
def create_alert_spec():
    """
    Generate alert specification for Cyoda.

    Request body:
        {
            "alert_type": "heat_wave",
            "severity": "high",
            "value": 39.5,
            "date": "2024-01-15",
            "anomaly_score": 0.85,
            "metric": "temperature",
            "use_ai_analysis": true
        }

    Returns alert specification for mcp__cyoda__entity_create_entity_tool.
    """
    try:
        data = request.get_json()

        # Extract parameters
        alert_type = data.get('alert_type')
        severity = data.get('severity')
        value = data.get('value')
        date = data.get('date')
        anomaly_score = data.get('anomaly_score')
        metric = data.get('metric', 'temperature')
        use_ai = data.get('use_ai_analysis', False)

        # Validate required fields
        if not all([alert_type, severity, value, date, anomaly_score]):
            return jsonify({
                'success': False,
                'error': 'Missing required fields'
            }), 400

        # Prepare alert parameters
        alert_params = {
            "alert_type": alert_type,
            "severity": severity,
            "value": float(value),
            "date": date,
            "anomaly_score": float(anomaly_score),
            "metric": metric
        }

        # Add AI analysis if requested
        if use_ai:
            service = get_alert_service()
            if service.gemini_client:
                ai_analysis = service._generate_ai_analysis(
                    alert_type=alert_type,
                    severity=severity,
                    value=float(value),
                    metric=metric,
                    anomaly_score=float(anomaly_score),
                    date=date
                )
                alert_params.update({
                    "ai_analysis": ai_analysis.get("analysis", {}),
                    "recommendations": ai_analysis.get("recommendations", []),
                    "description": ai_analysis.get("summary", "")
                })

        # Create alert specification
        alert_spec = cyoda_client.create_alert(**alert_params)

        return jsonify({
            'success': True,
            'alert_specification': alert_spec,
            'message': 'Use mcp__cyoda__entity_create_entity_tool with this specification'
        })

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@alert_bp.route('/search', methods=['POST'])
def search_alerts_spec():
    """
    Generate Cyoda search specification for alerts.

    Request body:
        {
            "status": "active",
            "severity": "high",
            "alert_type": "heat_wave",
            "min_anomaly_score": 0.7,
            "date_from": "2024-01-01",
            "date_to": "2024-12-31"
        }

    Returns search specification for mcp__cyoda__search_search tool.
    """
    try:
        data = request.get_json()

        search_spec = cyoda_client.search_alerts(
            status=data.get('status'),
            severity=data.get('severity'),
            alert_type=data.get('alert_type'),
            min_anomaly_score=data.get('min_anomaly_score'),
            date_from=data.get('date_from'),
            date_to=data.get('date_to')
        )

        return jsonify({
            'success': True,
            'search_specification': search_spec,
            'message': 'Use mcp__cyoda__search_search tool with this specification'
        })

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@alert_bp.route('/update/<alert_id>', methods=['PUT'])
def update_alert_spec(alert_id):
    """
    Generate update specification for alert status.

    Path params:
        alert_id: Cyoda entity UUID

    Request body:
        {
            "status": "acknowledged",
            "acknowledged": true,
            "resolved": false,
            "resolution_notes": "Team notified"
        }

    Returns update specification for mcp__cyoda__entity_update_entity_tool.
    """
    try:
        data = request.get_json()

        update_spec = cyoda_client.update_alert_status(
            alert_id=alert_id,
            status=data.get('status', 'active'),
            acknowledged=data.get('acknowledged', False),
            resolved=data.get('resolved', False),
            resolution_notes=data.get('resolution_notes')
        )

        return jsonify({
            'success': True,
            'update_specification': update_spec,
            'message': 'Use mcp__cyoda__entity_update_entity_tool with this specification'
        })

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@alert_bp.route('/get/<alert_id>', methods=['GET'])
def get_alert_spec(alert_id):
    """
    Generate get specification for a specific alert.

    Returns specification for mcp__cyoda__entity_get_entity_tool.
    """
    try:
        get_spec = cyoda_client.get_alert(alert_id)

        return jsonify({
            'success': True,
            'get_specification': get_spec,
            'message': 'Use mcp__cyoda__entity_get_entity_tool with this specification'
        })

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@alert_bp.route('/list', methods=['GET', 'POST'])
def list_alerts():
    """
    Get/Set alerts from Cyoda.

    GET: Returns cached alerts or MCP specification
    POST: Accepts alerts fetched by Claude Code via MCP tools
    """
    # Simple in-memory cache
    if not hasattr(list_alerts, 'cached_alerts'):
        list_alerts.cached_alerts = []

    if request.method == 'POST':
        # Claude Code is injecting alerts fetched from Cyoda
        data = request.get_json()
        if data and 'alerts' in data:
            # Extract and normalize alert data
            alerts = []
            for entity in data['alerts']:
                if isinstance(entity, dict):
                    # Handle both direct alert data and entity wrapper format
                    if 'data' in entity and entity.get('data', {}).get('type') == 'ENTITY':
                        # Entity wrapper format
                        entity_data = entity['data']['data']
                        entity_meta = entity['data']['meta']
                        alert = {
                            'technical_id': entity_meta['id'],
                            **entity_data
                        }
                    else:
                        # Direct alert data
                        alert = entity

                    alerts.append(alert)

            list_alerts.cached_alerts = alerts

            return jsonify({
                'success': True,
                'message': f'Cached {len(alerts)} alerts',
                'count': len(alerts)
            })

    # GET request - return cached alerts
    if list_alerts.cached_alerts:
        return jsonify({
            'success': True,
            'alerts': list_alerts.cached_alerts,
            'count': len(list_alerts.cached_alerts),
            'cached': True
        })
    else:
        # No cached alerts, return MCP spec
        try:
            list_spec = cyoda_client.list_all_alerts()
            return jsonify({
                'success': True,
                'mcp_spec': list_spec,
                'message': 'No cached alerts. Execute MCP tool and POST results to /api/alerts/list',
                'alerts': [],
                'cached': False
            })
        except Exception as e:
            return jsonify({
                'success': False,
                'error': str(e),
                'alerts': []
            }), 500


@alert_bp.route('/summary', methods=['POST'])
def alerts_summary():
    """
    Generate summary statistics for provided alerts.

    Request body:
        {
            "alerts": [
                {"alert_type": "heat_wave", "severity": "high", ...},
                ...
            ]
        }
    """
    try:
        data = request.get_json()
        alerts = data.get('alerts', [])

        service = get_alert_service()
        summary = service.get_active_alerts_summary(alerts)

        return jsonify({
            'success': True,
            'summary': summary
        })

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@alert_bp.route('/prioritize', methods=['POST'])
def prioritize_alerts():
    """
    Prioritize alerts by severity and recency.

    Request body:
        {
            "alerts": [...]
        }
    """
    try:
        data = request.get_json()
        alerts = data.get('alerts', [])

        service = get_alert_service()
        prioritized = service.prioritize_alerts(alerts)

        return jsonify({
            'success': True,
            'prioritized_alerts': prioritized
        })

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@alert_bp.route('/classify', methods=['POST'])
def classify_alert():
    """
    Classify an alert's severity and type.

    Request body:
        {
            "value": 39.5,
            "metric": "temperature",
            "anomaly_score": 0.85
        }
    """
    try:
        data = request.get_json()
        value = data.get('value')
        metric = data.get('metric', 'temperature')
        anomaly_score = data.get('anomaly_score', 0.5)

        severity = cyoda_client.classify_severity(
            anomaly_score=float(anomaly_score),
            value=float(value),
            metric=metric
        )

        alert_type = cyoda_client.determine_alert_type(
            value=float(value),
            metric=metric
        )

        return jsonify({
            'success': True,
            'severity': severity,
            'alert_type': alert_type
        })

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
