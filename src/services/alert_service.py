"""Climate Alert Service integrating ML anomaly detection, Cyoda, and Gemini AI."""

import sys
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
import pandas as pd
import numpy as np

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))


class ClimateAlertService:
    """
    Service for detecting, analyzing, and managing climate alerts.

    Integrates:
    - ML anomaly detection
    - Cyoda entity management
    - Gemini AI analysis
    """

    def __init__(self, anomaly_detector=None, gemini_client=None, cyoda_client=None):
        """
        Initialize alert service.

        Args:
            anomaly_detector: Instance of ClimateAnomalyDetector (optional)
            gemini_client: Instance of GeminiClimateAnalyst (optional)
            cyoda_client: Instance of CyodaAlertClient (optional)
        """
        self.anomaly_detector = anomaly_detector
        self.gemini_client = gemini_client
        self.cyoda_client = cyoda_client

    def detect_and_create_alerts(
        self,
        climate_data: pd.DataFrame,
        value_column: str = 'value',
        metric: str = 'temperature',
        use_ai_analysis: bool = True
    ) -> List[Dict[str, Any]]:
        """
        Detect anomalies in climate data and create alerts in Cyoda.

        Args:
            climate_data: DataFrame with climate measurements
            value_column: Column name containing values
            metric: Climate metric type
            use_ai_analysis: Whether to use Gemini AI for analysis

        Returns:
            List of alert creation parameters for Cyoda
        """
        if self.anomaly_detector is None:
            raise ValueError("Anomaly detector not initialized")

        if self.cyoda_client is None:
            raise ValueError("Cyoda client not initialized")

        # Detect anomalies using ML model
        results = self.anomaly_detector.detect(climate_data, value_column=value_column)

        # Filter for actual anomalies
        anomalies = results[results['is_anomaly'] == True].copy()

        alerts = []

        for _, row in anomalies.iterrows():
            # Extract anomaly details
            date_raw = row.get('date', datetime.utcnow().isoformat())
            # Convert Timestamp to string immediately
            date = date_raw if isinstance(date_raw, str) else date_raw.isoformat()
            value = float(row[value_column])
            anomaly_score = float(row['anomaly_score'])

            # Classify severity and type
            severity = self.cyoda_client.classify_severity(anomaly_score, value, metric)
            alert_type = self.cyoda_client.determine_alert_type(value, metric)

            # Prepare alert data
            alert_params = {
                "alert_type": alert_type,
                "severity": severity,
                "value": value,
                "date": date,
                "anomaly_score": anomaly_score,
                "metric": metric,
                "location": "Uruguay"
            }

            # Add AI analysis if enabled
            if use_ai_analysis and self.gemini_client is not None:
                try:
                    ai_analysis = self._generate_ai_analysis(
                        alert_type=alert_type,
                        severity=severity,
                        value=value,
                        metric=metric,
                        anomaly_score=anomaly_score,
                        date=date
                    )
                    alert_params["ai_analysis"] = ai_analysis.get("analysis", {})
                    alert_params["recommendations"] = ai_analysis.get("recommendations", [])
                    alert_params["description"] = ai_analysis.get("summary", "")
                except Exception as e:
                    print(f"AI analysis failed: {e}")
                    alert_params["description"] = self._generate_basic_description(
                        alert_type, severity, value, metric
                    )
            else:
                alert_params["description"] = self._generate_basic_description(
                    alert_type, severity, value, metric
                )

            # Create alert entity specification
            alert_spec = self.cyoda_client.create_alert(**alert_params)
            alerts.append(alert_spec)

        return alerts

    def _generate_ai_analysis(
        self,
        alert_type: str,
        severity: str,
        value: float,
        metric: str,
        anomaly_score: float,
        date: str
    ) -> Dict[str, Any]:
        """
        Generate AI-powered analysis for an alert.

        Args:
            alert_type: Type of alert
            severity: Severity level
            value: Measured value
            metric: Climate metric
            anomaly_score: Anomaly score
            date: Date of alert

        Returns:
            Dict with analysis, recommendations, and summary
        """
        if self.gemini_client is None:
            return {}

        # Prepare context for Gemini
        anomaly_data = [{
            "date": date,
            "value": value,
            "anomaly_score": anomaly_score,
            "alert_type": alert_type,
            "severity": severity,
            "metric": metric
        }]

        # Generate comprehensive analysis
        try:
            report = self.gemini_client.generate_anomaly_report(anomaly_data)

            # Extract recommendations
            recommendations = self._extract_recommendations_from_report(
                report, alert_type, severity
            )

            # Generate summary
            summary = self._generate_summary(alert_type, severity, value, metric)

            return {
                "analysis": {
                    "full_report": report,
                    "alert_type": alert_type,
                    "severity": severity,
                    "confidence": anomaly_score
                },
                "recommendations": recommendations,
                "summary": summary
            }

        except Exception as e:
            print(f"Gemini analysis error: {e}")
            return {}

    def _extract_recommendations_from_report(
        self,
        report: str,
        alert_type: str,
        severity: str
    ) -> List[str]:
        """
        Extract actionable recommendations from AI report.

        Args:
            report: Full AI-generated report
            alert_type: Type of alert
            severity: Severity level

        Returns:
            List of recommendations
        """
        # Parse report for recommendations section
        recommendations = []

        # Look for recommendation keywords
        lines = report.split('\n')
        in_recommendations = False

        for line in lines:
            line_lower = line.lower()
            if 'recommend' in line_lower or 'action' in line_lower or 'should' in line_lower:
                in_recommendations = True
            if in_recommendations and line.strip() and not line.strip().startswith('#'):
                if any(marker in line for marker in ['•', '-', '*', '1.', '2.', '3.']):
                    clean_line = line.strip().lstrip('•-*123456789. ')
                    if clean_line:
                        recommendations.append(clean_line)

        # Add default recommendations if none found
        if not recommendations:
            recommendations = self._get_default_recommendations(alert_type, severity)

        return recommendations[:5]  # Limit to top 5

    def _get_default_recommendations(self, alert_type: str, severity: str) -> List[str]:
        """Get default recommendations based on alert type and severity."""
        recs = []

        if severity in ['critical', 'high']:
            recs.append("Issue public advisory immediately")
            recs.append("Activate emergency response protocols")

        if alert_type == "heat_wave":
            recs.extend([
                "Increase water reserves monitoring",
                "Advise vulnerable populations to stay indoors",
                "Monitor energy grid for increased cooling demand"
            ])
        elif alert_type == "extreme_precipitation":
            recs.extend([
                "Check drainage systems and flood defenses",
                "Issue flood warnings for low-lying areas",
                "Monitor river levels closely"
            ])
        elif alert_type in ["cold_snap", "freeze_event"]:
            recs.extend([
                "Protect sensitive crops and livestock",
                "Monitor heating fuel supplies",
                "Check on vulnerable populations"
            ])
        elif alert_type == "drought_indicator":
            recs.extend([
                "Implement water conservation measures",
                "Monitor agricultural impacts",
                "Review water allocation policies"
            ])

        return recs

    def _generate_basic_description(
        self,
        alert_type: str,
        severity: str,
        value: float,
        metric: str
    ) -> str:
        """Generate basic description without AI."""
        alert_names = {
            "heat_wave": "Heat Wave",
            "cold_snap": "Cold Snap",
            "freeze_event": "Freeze Event",
            "extreme_precipitation": "Extreme Precipitation",
            "drought_indicator": "Drought Indicator",
            "temperature_anomaly": "Temperature Anomaly",
            "precipitation_anomaly": "Precipitation Anomaly",
            "climate_anomaly": "Climate Anomaly"
        }

        alert_name = alert_names.get(alert_type, "Climate Alert")
        unit = "°C" if metric == "temperature" else "mm"

        return f"{severity.title()} {alert_name} detected: {value:.1f}{unit}"

    def _generate_summary(
        self,
        alert_type: str,
        severity: str,
        value: float,
        metric: str
    ) -> str:
        """Generate concise summary for the alert."""
        return self._generate_basic_description(alert_type, severity, value, metric)

    def get_active_alerts_summary(self, alerts: List[Dict]) -> Dict[str, Any]:
        """
        Generate summary statistics for active alerts.

        Args:
            alerts: List of alert entities from Cyoda

        Returns:
            Summary statistics
        """
        if not alerts:
            return {
                "total": 0,
                "by_severity": {},
                "by_type": {},
                "critical_count": 0
            }

        df = pd.DataFrame(alerts)

        summary = {
            "total": len(alerts),
            "by_severity": df['severity'].value_counts().to_dict() if 'severity' in df else {},
            "by_type": df['alert_type'].value_counts().to_dict() if 'alert_type' in df else {},
            "critical_count": len(df[df['severity'] == 'critical']) if 'severity' in df else 0,
            "active_count": len(df[df['status'] == 'active']) if 'status' in df else 0,
            "acknowledged_count": len(df[df.get('acknowledged', False) == True]) if 'acknowledged' in df else 0,
            "resolved_count": len(df[df.get('resolved', False) == True]) if 'resolved' in df else 0
        }

        return summary

    def prioritize_alerts(self, alerts: List[Dict]) -> List[Dict]:
        """
        Prioritize alerts by severity and recency.

        Args:
            alerts: List of alert entities

        Returns:
            Sorted list of alerts (highest priority first)
        """
        if not alerts:
            return []

        severity_order = {"critical": 4, "high": 3, "medium": 2, "low": 1}

        def priority_score(alert):
            severity_score = severity_order.get(alert.get('severity', 'low'), 0)
            # Boost score for unacknowledged alerts
            ack_penalty = 0 if alert.get('acknowledged', False) else 2
            # Recent alerts get higher priority
            try:
                date = pd.to_datetime(alert.get('date', '2000-01-01'))
                days_ago = (pd.Timestamp.now() - date).days
                recency_score = max(0, 30 - days_ago) / 30  # Normalize to 0-1
            except:
                recency_score = 0

            return severity_score + ack_penalty + recency_score

        sorted_alerts = sorted(alerts, key=priority_score, reverse=True)
        return sorted_alerts
