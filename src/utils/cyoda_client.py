"""Cyoda MCP client for climate alert management."""

import os
from typing import Dict, List, Optional, Any
from datetime import datetime


class CyodaAlertClient:
    """
    Client for managing climate alerts in Cyoda.

    Uses MCP tools for entity management. This class provides
    a Python interface that wraps the MCP tool calls.
    """

    ENTITY_MODEL = "climate_alert"
    ENTITY_VERSION = "1"

    def __init__(self):
        """Initialize Cyoda alert client."""
        # MCP tools are called directly via the tool system
        # This client provides structured methods for alert operations
        pass

    def create_alert(
        self,
        alert_type: str,
        severity: str,
        value: float,
        date: str,
        anomaly_score: float,
        location: str = "Uruguay",
        metric: str = "temperature",
        description: Optional[str] = None,
        ai_analysis: Optional[Dict] = None,
        recommendations: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Create a new climate alert entity in Cyoda.

        Args:
            alert_type: Type of alert (heat_wave, cold_snap, extreme_precipitation, etc.)
            severity: Alert severity (low, medium, high, critical)
            value: The measured value that triggered the alert
            date: ISO date string when alert was triggered
            anomaly_score: ML anomaly score (0-1)
            location: Geographic location (default: Uruguay)
            metric: Climate metric (temperature, precipitation, etc.)
            description: Optional human-readable description
            ai_analysis: Optional Gemini AI analysis results
            recommendations: Optional list of recommendations

        Returns:
            Dict with success status, entity_id, and created entity data
        """
        entity_data = {
            "alert_type": alert_type,
            "severity": severity,
            "value": value,
            "date": date,
            "anomaly_score": anomaly_score,
            "location": location,
            "metric": metric,
            "status": "active",
            "created_at": datetime.utcnow().isoformat(),
            "acknowledged": False,
            "resolved": False
        }

        if description:
            entity_data["description"] = description

        if ai_analysis:
            entity_data["ai_analysis"] = ai_analysis

        if recommendations:
            entity_data["recommendations"] = recommendations

        # This method should be called via MCP tool: mcp__cyoda__entity_create_entity_tool
        # Return the entity data that should be passed to the tool
        return {
            "entity_model": self.ENTITY_MODEL,
            "entity_version": self.ENTITY_VERSION,
            "entity_data": entity_data
        }

    def get_alert(self, alert_id: str) -> Dict[str, Any]:
        """
        Retrieve an alert by ID.

        Args:
            alert_id: Technical UUID of the alert entity

        Returns:
            Dict for mcp__cyoda__entity_get_entity_tool call
        """
        return {
            "entity_model": self.ENTITY_MODEL,
            "entity_id": alert_id,
            "entity_version": self.ENTITY_VERSION
        }

    def list_all_alerts(self) -> Dict[str, str]:
        """
        List all climate alerts.

        Returns:
            Dict for mcp__cyoda__entity_list_entities_tool call
        """
        return {
            "entity_model": self.ENTITY_MODEL,
            "entity_version": self.ENTITY_VERSION
        }

    def search_alerts(
        self,
        status: Optional[str] = None,
        severity: Optional[str] = None,
        alert_type: Optional[str] = None,
        min_anomaly_score: Optional[float] = None,
        date_from: Optional[str] = None,
        date_to: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Search alerts with filters using Cyoda search conditions.

        Args:
            status: Filter by status (active, acknowledged, resolved)
            severity: Filter by severity (low, medium, high, critical)
            alert_type: Filter by type (heat_wave, cold_snap, etc.)
            min_anomaly_score: Minimum anomaly score threshold
            date_from: Start date for date range filter
            date_to: End date for date range filter

        Returns:
            Dict for mcp__cyoda__search_search tool call with search conditions
        """
        conditions = []

        if status:
            conditions.append({
                "type": "simple",
                "jsonPath": "$.status",
                "operatorType": "EQUALS",
                "value": status
            })

        if severity:
            conditions.append({
                "type": "simple",
                "jsonPath": "$.severity",
                "operatorType": "EQUALS",
                "value": severity
            })

        if alert_type:
            conditions.append({
                "type": "simple",
                "jsonPath": "$.alert_type",
                "operatorType": "EQUALS",
                "value": alert_type
            })

        if min_anomaly_score is not None:
            conditions.append({
                "type": "simple",
                "jsonPath": "$.anomaly_score",
                "operatorType": "GREATER_THAN",
                "value": min_anomaly_score
            })

        if date_from:
            conditions.append({
                "type": "simple",
                "jsonPath": "$.date",
                "operatorType": "GREATER_THAN",
                "value": date_from
            })

        if date_to:
            conditions.append({
                "type": "simple",
                "jsonPath": "$.date",
                "operatorType": "LESS_THAN",
                "value": date_to
            })

        # Build search condition structure
        if len(conditions) == 0:
            # No filters, return all
            search_conditions = {}
        elif len(conditions) == 1:
            search_conditions = conditions[0]
        else:
            search_conditions = {
                "type": "group",
                "operator": "AND",
                "conditions": conditions
            }

        return {
            "entity_model": self.ENTITY_MODEL,
            "entity_version": self.ENTITY_VERSION,
            "search_conditions": search_conditions
        }

    def update_alert_status(
        self,
        alert_id: str,
        status: str,
        acknowledged: bool = False,
        resolved: bool = False,
        resolution_notes: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Update alert status (acknowledge, resolve, etc.).

        Args:
            alert_id: Technical UUID of the alert
            status: New status
            acknowledged: Mark as acknowledged
            resolved: Mark as resolved
            resolution_notes: Optional notes about resolution

        Returns:
            Dict for mcp__cyoda__entity_update_entity_tool call
        """
        entity_data = {
            "status": status,
            "acknowledged": acknowledged,
            "resolved": resolved,
            "updated_at": datetime.utcnow().isoformat()
        }

        if resolved:
            entity_data["resolved_at"] = datetime.utcnow().isoformat()

        if acknowledged and not resolved:
            entity_data["acknowledged_at"] = datetime.utcnow().isoformat()

        if resolution_notes:
            entity_data["resolution_notes"] = resolution_notes

        return {
            "entity_model": self.ENTITY_MODEL,
            "entity_id": alert_id,
            "entity_version": self.ENTITY_VERSION,
            "entity_data": entity_data
        }

    def delete_alert(self, alert_id: str) -> Dict[str, str]:
        """
        Delete an alert entity.

        Args:
            alert_id: Technical UUID of the alert

        Returns:
            Dict for mcp__cyoda__entity_delete_entity_tool call
        """
        return {
            "entity_model": self.ENTITY_MODEL,
            "entity_id": alert_id,
            "entity_version": self.ENTITY_VERSION
        }

    @staticmethod
    def classify_severity(anomaly_score: float, value: float, metric: str) -> str:
        """
        Classify alert severity based on anomaly score and value.

        Args:
            anomaly_score: ML anomaly score (0-1)
            value: Measured value
            metric: Climate metric

        Returns:
            Severity level: low, medium, high, critical
        """
        if metric == "temperature":
            if anomaly_score > 0.9 or value > 40 or value < -10:
                return "critical"
            elif anomaly_score > 0.7 or value > 35 or value < -5:
                return "high"
            elif anomaly_score > 0.5:
                return "medium"
            else:
                return "low"

        elif metric == "precipitation":
            if anomaly_score > 0.9 or value > 100:  # >100mm in a day
                return "critical"
            elif anomaly_score > 0.7 or value > 50:
                return "high"
            elif anomaly_score > 0.5:
                return "medium"
            else:
                return "low"

        # Default classification based only on anomaly score
        if anomaly_score > 0.85:
            return "critical"
        elif anomaly_score > 0.7:
            return "high"
        elif anomaly_score > 0.5:
            return "medium"
        else:
            return "low"

    @staticmethod
    def determine_alert_type(value: float, metric: str, seasonal_context: Optional[Dict] = None) -> str:
        """
        Determine the type of climate alert.

        Args:
            value: Measured value
            metric: Climate metric
            seasonal_context: Optional seasonal information

        Returns:
            Alert type string
        """
        if metric == "temperature":
            if value > 35:
                return "heat_wave"
            elif value < 0:
                return "freeze_event"
            elif value < 5:
                return "cold_snap"
            else:
                return "temperature_anomaly"

        elif metric == "precipitation":
            if value > 50:
                return "extreme_precipitation"
            elif value < 0.1:
                return "drought_indicator"
            else:
                return "precipitation_anomaly"

        return "climate_anomaly"
