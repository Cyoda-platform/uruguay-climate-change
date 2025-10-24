"""
Gemini AI + Cyoda MCP Integration Service.

This service allows Gemini AI to analyze climate data and automatically
create/update/query entities in Cyoda using MCP tools.
"""

import os
import json
from typing import Dict, List, Optional, Any
from datetime import datetime

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False


class GeminiCyodaIntegration:
    """
    Integration layer between Google Gemini AI and Cyoda MCP.

    Gemini analyzes data and generates insights, then automatically
    stores results as entities in Cyoda.
    """

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Gemini-Cyoda integration.

        Args:
            api_key: Gemini API key (defaults to GEMINI_API_KEY env var)
        """
        if not GEMINI_AVAILABLE:
            raise ImportError("google-generativeai package not installed")

        self.api_key = api_key or os.getenv('GEMINI_API_KEY')
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not configured")

        genai.configure(api_key=self.api_key)
        # Use models/gemini-2.5-flash - the models/ prefix is required!
        self.model = genai.GenerativeModel('models/gemini-2.5-flash')

    def analyze_and_create_alert(
        self,
        climate_data: Dict[str, Any],
        create_in_cyoda: bool = True
    ) -> Dict[str, Any]:
        """
        Use Gemini to analyze climate data and create alert entity in Cyoda.

        Args:
            climate_data: Climate measurements and context
            create_in_cyoda: Whether to return MCP spec for Cyoda creation

        Returns:
            Dict with analysis and MCP specification for entity creation
        """
        # Step 1: Gemini analyzes the data
        analysis_prompt = f"""
        Analyze this climate data for Uruguay and determine if an alert should be created:

        Data: {json.dumps(climate_data, indent=2)}

        Provide your analysis in JSON format with these fields:
        {{
            "should_create_alert": true/false,
            "alert_type": "heat_wave/cold_snap/extreme_precipitation/etc",
            "severity": "low/medium/high/critical",
            "summary": "Brief description",
            "detailed_analysis": "Full analysis",
            "recommendations": ["action1", "action2", ...],
            "confidence": 0.0-1.0
        }}

        Only respond with valid JSON, no other text.
        """

        response = self.model.generate_content(analysis_prompt)
        analysis = self._parse_json_response(response.text)

        result = {
            "gemini_analysis": analysis,
            "timestamp": datetime.utcnow().isoformat()
        }

        # Step 2: Generate Cyoda MCP specification if alert needed
        if analysis.get('should_create_alert') and create_in_cyoda:
            mcp_spec = self._create_alert_entity_spec(climate_data, analysis)
            result['cyoda_mcp_spec'] = mcp_spec
            result['action'] = 'create_alert_entity'

        return result

    def analyze_trends_and_store(
        self,
        historical_data: List[Dict],
        analysis_type: str = "trend_analysis"
    ) -> Dict[str, Any]:
        """
        Use Gemini to analyze trends and store analysis as Cyoda entity.

        Args:
            historical_data: List of historical climate measurements
            analysis_type: Type of analysis to perform

        Returns:
            Dict with analysis and MCP specification
        """
        # Gemini analyzes trends
        prompt = f"""
        Analyze these historical climate trends for Uruguay:

        Data points: {len(historical_data)}
        Sample: {json.dumps(historical_data[:5], indent=2)}

        Provide trend analysis in JSON format:
        {{
            "trend_direction": "increasing/decreasing/stable/volatile",
            "key_findings": ["finding1", "finding2", ...],
            "statistical_summary": {{}},
            "predictions": {{}},
            "confidence": 0.0-1.0
        }}

        Only respond with valid JSON.
        """

        response = self.model.generate_content(prompt)
        analysis = self._parse_json_response(response.text)

        # Create entity specification for storing this analysis
        mcp_spec = {
            "entity_model": "climate_analysis",
            "entity_version": "1",
            "entity_data": {
                "analysis_type": analysis_type,
                "created_at": datetime.utcnow().isoformat(),
                "data_points_analyzed": len(historical_data),
                "trend_direction": analysis.get('trend_direction'),
                "key_findings": analysis.get('key_findings', []),
                "statistical_summary": analysis.get('statistical_summary', {}),
                "predictions": analysis.get('predictions', {}),
                "confidence": analysis.get('confidence', 0.0),
                "full_analysis": analysis,
                "model": "gemini-2.5-flash",
                "status": "completed"
            }
        }

        return {
            "gemini_analysis": analysis,
            "cyoda_mcp_spec": mcp_spec,
            "action": "create_analysis_entity"
        }

    def generate_report_and_store(
        self,
        report_type: str,
        data_context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Use Gemini to generate a comprehensive report and store in Cyoda.

        Args:
            report_type: Type of report (executive_summary, detailed_analysis, etc)
            data_context: All data and context for the report

        Returns:
            Dict with generated report and MCP specification
        """
        prompt = f"""
        Generate a {report_type} report for climate conditions in Uruguay.

        Context: {json.dumps(data_context, indent=2)}

        Provide the report in JSON format:
        {{
            "title": "Report title",
            "executive_summary": "Brief summary",
            "sections": [
                {{"title": "Section 1", "content": "..."}},
                ...
            ],
            "key_metrics": {{}},
            "recommendations": [],
            "risk_level": "low/medium/high/critical"
        }}

        Only respond with valid JSON.
        """

        response = self.model.generate_content(prompt)
        report = self._parse_json_response(response.text)

        # Create entity for report storage
        mcp_spec = {
            "entity_model": "climate_report",
            "entity_version": "1",
            "entity_data": {
                "report_type": report_type,
                "created_at": datetime.utcnow().isoformat(),
                "title": report.get('title'),
                "executive_summary": report.get('executive_summary'),
                "sections": report.get('sections', []),
                "key_metrics": report.get('key_metrics', {}),
                "recommendations": report.get('recommendations', []),
                "risk_level": report.get('risk_level'),
                "full_report": report,
                "generated_by": "gemini-1.5-flash",
                "status": "published"
            }
        }

        return {
            "report": report,
            "cyoda_mcp_spec": mcp_spec,
            "action": "create_report_entity"
        }

    def query_cyoda_with_nl(
        self,
        natural_language_query: str,
        entity_type: str = "climate_alert"
    ) -> Dict[str, Any]:
        """
        Use Gemini to convert natural language to Cyoda search conditions.

        Args:
            natural_language_query: Plain English query
            entity_type: Type of entity to search

        Returns:
            Dict with Cyoda MCP search specification

        Example:
            "Show me all critical heat waves in January 2024"
            → Cyoda search conditions
        """
        prompt = f"""
        Convert this natural language query into Cyoda search conditions:

        Query: "{natural_language_query}"
        Entity Type: {entity_type}

        Generate Cyoda search conditions in this JSON format:
        {{
            "entity_model": "{entity_type}",
            "search_conditions": {{
                "type": "group",
                "operator": "AND",
                "conditions": [
                    {{
                        "type": "simple",
                        "jsonPath": "$.field_name",
                        "operatorType": "EQUALS",
                        "value": "value"
                    }}
                ]
            }}
        }}

        Available operators: EQUALS, CONTAINS, GREATER_THAN, LESS_THAN
        Available fields for climate_alert: alert_type, severity, status, date, value, anomaly_score

        Only respond with valid JSON.
        """

        response = self.model.generate_content(prompt)
        search_spec = self._parse_json_response(response.text)

        return {
            "natural_language_query": natural_language_query,
            "cyoda_search_spec": search_spec,
            "action": "search_entities",
            "explanation": "Use mcp__cyoda__search_search with this specification"
        }

    def chat_about_alerts(
        self,
        user_message: str,
        cyoda_alerts: List[Dict],
        conversation_history: Optional[List[Dict]] = None
    ) -> Dict[str, Any]:
        """
        Chat interface where Gemini can discuss alerts from Cyoda.

        Args:
            user_message: User's question/message
            cyoda_alerts: Current alerts from Cyoda
            conversation_history: Previous messages

        Returns:
            Dict with Gemini's response and any suggested actions
        """
        context = f"""
        Current Climate Alerts in Cyoda:
        {json.dumps(cyoda_alerts, indent=2)}

        Previous conversation:
        {json.dumps(conversation_history or [], indent=2)}

        User question: "{user_message}"

        Respond in JSON format:
        {{
            "response": "Your natural language response to the user",
            "suggested_actions": [
                {{
                    "action": "acknowledge_alert/create_report/etc",
                    "alert_id": "optional",
                    "reason": "why this action is suggested"
                }}
            ],
            "follow_up_questions": ["question1", ...]
        }}

        Only respond with valid JSON.
        """

        response = self.model.generate_content(context)
        chat_response = self._parse_json_response(response.text)

        return {
            "user_message": user_message,
            "gemini_response": chat_response.get('response'),
            "suggested_actions": chat_response.get('suggested_actions', []),
            "follow_up_questions": chat_response.get('follow_up_questions', []),
            "timestamp": datetime.utcnow().isoformat()
        }

    def _create_alert_entity_spec(
        self,
        climate_data: Dict,
        analysis: Dict
    ) -> Dict[str, Any]:
        """Generate Cyoda MCP specification for alert entity."""
        return {
            "entity_model": "climate_alert",
            "entity_version": "1",
            "entity_data": {
                "alert_type": analysis.get('alert_type', 'climate_anomaly'),
                "severity": analysis.get('severity', 'medium'),
                "value": climate_data.get('value'),
                "date": climate_data.get('date', datetime.utcnow().isoformat()),
                "anomaly_score": analysis.get('confidence', 0.5),
                "location": "Uruguay",
                "metric": climate_data.get('metric', 'temperature'),
                "status": "active",
                "acknowledged": False,
                "resolved": False,
                "created_at": datetime.utcnow().isoformat(),
                "description": analysis.get('summary'),
                "ai_analysis": {
                    "full_analysis": analysis.get('detailed_analysis'),
                    "confidence": analysis.get('confidence'),
                    "model": "gemini-1.5-flash"
                },
                "recommendations": analysis.get('recommendations', []),
                "generated_by": "gemini_cyoda_integration"
            }
        }

    def _parse_json_response(self, text: str) -> Dict:
        """Parse JSON from Gemini response, handling markdown code blocks."""
        # Remove markdown code blocks if present
        text = text.strip()
        if text.startswith('```json'):
            text = text[7:]
        if text.startswith('```'):
            text = text[3:]
        if text.endswith('```'):
            text = text[:-3]

        try:
            return json.loads(text.strip())
        except json.JSONDecodeError as e:
            return {
                "error": "Failed to parse JSON",
                "raw_response": text,
                "parse_error": str(e)
            }


# Example usage functions

def example_gemini_analyzes_and_creates_alert():
    """Example: Gemini analyzes data and generates alert for Cyoda."""
    integration = GeminiCyodaIntegration()

    climate_data = {
        "date": "2024-01-15",
        "value": 42.5,
        "metric": "temperature",
        "location": "Montevideo",
        "context": "Unusually high temperature for January"
    }

    result = integration.analyze_and_create_alert(climate_data)

    print("Gemini Analysis:", result['gemini_analysis'])
    print("\nCyoda MCP Spec:", result.get('cyoda_mcp_spec'))

    # Now use Claude Code to execute the MCP tool:
    # mcp__cyoda__entity_create_entity_tool(**result['cyoda_mcp_spec'])


def example_natural_language_search():
    """Example: Natural language query → Cyoda search."""
    integration = GeminiCyodaIntegration()

    result = integration.query_cyoda_with_nl(
        "Show me all critical alerts from the last week"
    )

    print("Search Spec:", result['cyoda_search_spec'])

    # Execute with MCP tool:
    # mcp__cyoda__search_search(**result['cyoda_search_spec'])


def example_trend_analysis_storage():
    """Example: Gemini analyzes trends, stores in Cyoda."""
    integration = GeminiCyodaIntegration()

    historical_data = [
        {"date": "2024-01-01", "temp": 28.5},
        {"date": "2024-01-02", "temp": 29.2},
        # ... more data
    ]

    result = integration.analyze_trends_and_store(historical_data)

    print("Analysis:", result['gemini_analysis'])
    print("\nStore in Cyoda:", result['cyoda_mcp_spec'])

    # Create entity:
    # mcp__cyoda__entity_create_entity_tool(**result['cyoda_mcp_spec'])
