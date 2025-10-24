"""
API routes for Gemini AI + Cyoda MCP integration.

These endpoints allow Gemini to analyze data and automatically generate
MCP specifications for Cyoda entity operations.
"""

import sys
from pathlib import Path
from flask import Blueprint, jsonify, request

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

gemini_cyoda_bp = Blueprint('gemini_cyoda', __name__)

# Try to import integration service
try:
    from src.services.gemini_cyoda_integration import GeminiCyodaIntegration
    INTEGRATION_AVAILABLE = True
except ImportError as e:
    print(f"Gemini-Cyoda integration not available: {e}")
    INTEGRATION_AVAILABLE = False

# Global integration client (cached like gemini_routes.py does)
gemini_cyoda_client = None


def get_integration():
    """Get or create integration instance (with global caching)."""
    global gemini_cyoda_client

    if not INTEGRATION_AVAILABLE:
        return None

    if gemini_cyoda_client is None:
        try:
            gemini_cyoda_client = GeminiCyodaIntegration()
        except Exception as e:
            print(f"Failed to initialize integration: {e}")
            return None

    return gemini_cyoda_client


@gemini_cyoda_bp.route('/analyze-and-alert', methods=['POST'])
def gemini_analyze_and_create_alert():
    """
    Gemini analyzes climate data and generates alert specification for Cyoda.

    Request body:
        {
            "climate_data": {
                "date": "2024-01-15",
                "value": 42.5,
                "metric": "temperature",
                "context": "Additional context"
            }
        }

    Returns:
        {
            "success": true,
            "gemini_analysis": {...},
            "cyoda_mcp_spec": {...},
            "action": "create_alert_entity",
            "message": "Use mcp__cyoda__entity_create_entity_tool with cyoda_mcp_spec"
        }
    """
    integration = get_integration()
    if not integration:
        return jsonify({
            'success': False,
            'error': 'Gemini-Cyoda integration not available',
            'hint': 'Set GEMINI_API_KEY environment variable'
        }), 503

    try:
        data = request.get_json()
        climate_data = data.get('climate_data', {})

        if not climate_data:
            return jsonify({
                'success': False,
                'error': 'No climate data provided'
            }), 400

        # Gemini analyzes and generates MCP spec
        result = integration.analyze_and_create_alert(climate_data)

        return jsonify({
            'success': True,
            'gemini_analysis': result['gemini_analysis'],
            'cyoda_mcp_spec': result.get('cyoda_mcp_spec'),
            'action': result.get('action'),
            'timestamp': result['timestamp'],
            'message': 'Use mcp__cyoda__entity_create_entity_tool with cyoda_mcp_spec'
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@gemini_cyoda_bp.route('/nl-search', methods=['POST'])
def natural_language_search():
    """
    Convert natural language query to Cyoda search conditions using Gemini.

    Request body:
        {
            "query": "Show me all critical heat waves from last month",
            "entity_type": "climate_alert"
        }

    Returns:
        {
            "success": true,
            "natural_language_query": "...",
            "cyoda_search_spec": {...},
            "action": "search_entities",
            "message": "Use mcp__cyoda__search_search with cyoda_search_spec"
        }
    """
    integration = get_integration()
    if not integration:
        return jsonify({
            'success': False,
            'error': 'Gemini-Cyoda integration not available'
        }), 503

    try:
        data = request.get_json()
        query = data.get('query')
        entity_type = data.get('entity_type', 'climate_alert')

        if not query:
            return jsonify({
                'success': False,
                'error': 'No query provided'
            }), 400

        # Gemini converts NL to search spec
        result = integration.query_cyoda_with_nl(query, entity_type)

        return jsonify({
            'success': True,
            'natural_language_query': result['natural_language_query'],
            'cyoda_search_spec': result['cyoda_search_spec'],
            'action': result['action'],
            'explanation': result['explanation'],
            'message': 'Use mcp__cyoda__search_search with cyoda_search_spec'
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@gemini_cyoda_bp.route('/analyze-trends', methods=['POST'])
def analyze_trends_and_store():
    """
    Gemini analyzes historical trends and generates entity spec for Cyoda storage.

    Request body:
        {
            "historical_data": [
                {"date": "2024-01-01", "temp": 28.5},
                ...
            ],
            "analysis_type": "trend_analysis"
        }

    Returns:
        {
            "success": true,
            "gemini_analysis": {...},
            "cyoda_mcp_spec": {...},
            "action": "create_analysis_entity"
        }
    """
    integration = get_integration()
    if not integration:
        return jsonify({
            'success': False,
            'error': 'Gemini-Cyoda integration not available'
        }), 503

    try:
        data = request.get_json()
        historical_data = data.get('historical_data', [])
        analysis_type = data.get('analysis_type', 'trend_analysis')

        if not historical_data:
            return jsonify({
                'success': False,
                'error': 'No historical data provided'
            }), 400

        # Gemini analyzes trends
        result = integration.analyze_trends_and_store(
            historical_data,
            analysis_type
        )

        return jsonify({
            'success': True,
            'gemini_analysis': result['gemini_analysis'],
            'cyoda_mcp_spec': result['cyoda_mcp_spec'],
            'action': result['action'],
            'message': 'Use mcp__cyoda__entity_create_entity_tool with cyoda_mcp_spec'
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@gemini_cyoda_bp.route('/generate-report', methods=['POST'])
def generate_report_and_store():
    """
    Gemini generates comprehensive report and creates storage spec for Cyoda.

    Request body:
        {
            "report_type": "executive_summary",
            "data_context": {
                "alerts": [...],
                "statistics": {...},
                ...
            }
        }

    Returns:
        {
            "success": true,
            "report": {...},
            "cyoda_mcp_spec": {...},
            "action": "create_report_entity"
        }
    """
    integration = get_integration()
    if not integration:
        return jsonify({
            'success': False,
            'error': 'Gemini-Cyoda integration not available'
        }), 503

    try:
        data = request.get_json()
        report_type = data.get('report_type', 'executive_summary')
        data_context = data.get('data_context', {})

        # Gemini generates report
        result = integration.generate_report_and_store(
            report_type,
            data_context
        )

        return jsonify({
            'success': True,
            'report': result['report'],
            'cyoda_mcp_spec': result['cyoda_mcp_spec'],
            'action': result['action'],
            'message': 'Use mcp__cyoda__entity_create_entity_tool with cyoda_mcp_spec'
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@gemini_cyoda_bp.route('/chat', methods=['POST'])
def chat_about_alerts():
    """
    Chat with Gemini about alerts from Cyoda.

    Request body:
        {
            "message": "What are the most critical alerts?",
            "cyoda_alerts": [...],
            "conversation_history": [...]
        }

    Returns:
        {
            "success": true,
            "user_message": "...",
            "gemini_response": "...",
            "suggested_actions": [...],
            "follow_up_questions": [...]
        }
    """
    integration = get_integration()
    if not integration:
        return jsonify({
            'success': False,
            'error': 'Gemini-Cyoda integration not available'
        }), 503

    try:
        data = request.get_json()
        message = data.get('message')
        cyoda_alerts = data.get('cyoda_alerts', [])
        conversation_history = data.get('conversation_history')

        if not message:
            return jsonify({
                'success': False,
                'error': 'No message provided'
            }), 400

        # Gemini chats about alerts
        result = integration.chat_about_alerts(
            message,
            cyoda_alerts,
            conversation_history
        )

        return jsonify({
            'success': True,
            **result
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@gemini_cyoda_bp.route('/status', methods=['GET'])
def integration_status():
    """Check if Gemini-Cyoda integration is available."""
    import os

    api_key_configured = bool(os.getenv('GEMINI_API_KEY'))

    integration = get_integration()
    integration_working = integration is not None

    return jsonify({
        'success': True,
        'integration_available': INTEGRATION_AVAILABLE,
        'api_key_configured': api_key_configured,
        'integration_working': integration_working,
        'features': {
            'analyze_and_alert': integration_working,
            'natural_language_search': integration_working,
            'trend_analysis': integration_working,
            'report_generation': integration_working,
            'chat': integration_working
        }
    })
