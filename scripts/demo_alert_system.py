"""
Demo script for the Climate Alert System with Cyoda MCP integration.

This script demonstrates how to:
1. Detect anomalies in climate data using ML
2. Generate alert specifications for Cyoda
3. Use MCP tools to create/manage alert entities
4. Get AI-powered analysis and recommendations

Prerequisites:
- Flask backend running on localhost:5000
- ML models trained (run scripts/train_ml_models.py)
- Gemini API key configured (optional, for AI analysis)
- Cyoda MCP tools available

Usage:
    python scripts/demo_alert_system.py
"""

import requests
import json
from datetime import datetime, timedelta
import random

API_BASE = "http://localhost:5000/api"


def generate_sample_data_with_anomalies():
    """Generate sample climate data with intentional anomalies."""
    print("\n📊 Generating sample climate data...")

    data = []
    start_date = datetime.now() - timedelta(days=90)

    for i in range(90):
        date = start_date + timedelta(days=i)

        # Normal seasonal pattern
        temp = 18 + 8 * (i / 365.25) + random.uniform(-2, 2)

        # Inject anomalies
        if i == 15:
            temp = 41.5  # Heat wave
            print(f"  🔴 Injected HEAT WAVE on {date.date()}: {temp:.1f}°C")
        elif i == 45:
            temp = -4.2  # Cold snap
            print(f"  🔵 Injected COLD SNAP on {date.date()}: {temp:.1f}°C")
        elif i == 70:
            temp = 38.8  # Another heat event
            print(f"  🟠 Injected HEAT EVENT on {date.date()}: {temp:.1f}°C")

        data.append({
            "date": date.strftime("%Y-%m-%d"),
            "value": temp
        })

    print(f"  ✓ Generated {len(data)} data points")
    return data


def detect_alerts(climate_data):
    """Detect anomalies and generate alert specifications."""
    print("\n🔍 Running anomaly detection...")

    response = requests.post(
        f"{API_BASE}/alerts/detect",
        json={
            "data": climate_data,
            "metric": "temperature",
            "value_column": "value",
            "use_ai_analysis": True
        }
    )

    if response.status_code == 200:
        result = response.json()
        print(f"  ✓ Detected {result['alerts_detected']} anomalies")
        return result['alert_specifications']
    else:
        print(f"  ✗ Error: {response.json().get('error')}")
        return []


def display_alert_spec(spec, index):
    """Display an alert specification."""
    entity_data = spec['entity_data']

    print(f"\n🚨 Alert #{index + 1}")
    print(f"  Type: {entity_data['alert_type']}")
    print(f"  Severity: {entity_data['severity'].upper()}")
    print(f"  Date: {entity_data['date']}")
    print(f"  Value: {entity_data['value']:.1f}°C")
    print(f"  Anomaly Score: {entity_data['anomaly_score']:.2%}")
    print(f"  Description: {entity_data.get('description', 'N/A')}")

    if 'recommendations' in entity_data:
        print(f"  🤖 AI Recommendations:")
        for rec in entity_data['recommendations'][:3]:
            print(f"    • {rec}")


def show_mcp_instructions(spec):
    """Show how to use MCP tools to create the alert in Cyoda."""
    print("\n📡 To create this alert in Cyoda, use the MCP tool:")
    print(f"\n  Tool: mcp__cyoda__entity_create_entity_tool")
    print(f"  Parameters:")
    print(f"    entity_model: {spec['entity_model']}")
    print(f"    entity_version: {spec['entity_version']}")
    print(f"    entity_data: {json.dumps(spec['entity_data'], indent=6)}")


def demonstrate_search():
    """Demonstrate how to search for alerts."""
    print("\n\n🔎 DEMONSTRATION: Searching for Alerts")
    print("=" * 60)

    # Search for critical alerts
    print("\n1. Search for CRITICAL severity alerts:")
    response = requests.post(
        f"{API_BASE}/alerts/search",
        json={
            "severity": "critical",
            "status": "active"
        }
    )

    if response.status_code == 200:
        search_spec = response.json()['search_specification']
        print(f"\n  MCP Tool: mcp__cyoda__search_search")
        print(f"  Search Conditions:")
        print(json.dumps(search_spec['search_conditions'], indent=4))

    # Search for heat waves in date range
    print("\n\n2. Search for HEAT WAVES in last 30 days:")
    date_from = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")

    response = requests.post(
        f"{API_BASE}/alerts/search",
        json={
            "alert_type": "heat_wave",
            "date_from": date_from,
            "min_anomaly_score": 0.7
        }
    )

    if response.status_code == 200:
        search_spec = response.json()['search_specification']
        print(f"\n  MCP Tool: mcp__cyoda__search_search")
        print(f"  Search Conditions:")
        print(json.dumps(search_spec['search_conditions'], indent=4))


def demonstrate_lifecycle():
    """Demonstrate alert lifecycle management."""
    print("\n\n♻️  DEMONSTRATION: Alert Lifecycle Management")
    print("=" * 60)

    alert_id = "example-alert-uuid-12345"

    # Acknowledge alert
    print(f"\n1. Acknowledging alert {alert_id}:")
    response = requests.put(
        f"{API_BASE}/alerts/update/{alert_id}",
        json={
            "status": "acknowledged",
            "acknowledged": True,
            "resolved": False
        }
    )

    if response.status_code == 200:
        update_spec = response.json()['update_specification']
        print(f"\n  MCP Tool: mcp__cyoda__entity_update_entity_tool")
        print(f"  Entity ID: {update_spec['entity_id']}")
        print(f"  Update Data:")
        print(json.dumps(update_spec['entity_data'], indent=4))

    # Resolve alert
    print(f"\n\n2. Resolving alert {alert_id}:")
    response = requests.put(
        f"{API_BASE}/alerts/update/{alert_id}",
        json={
            "status": "resolved",
            "acknowledged": True,
            "resolved": True,
            "resolution_notes": "Advisory issued, situation normalized"
        }
    )

    if response.status_code == 200:
        update_spec = response.json()['update_specification']
        print(f"\n  MCP Tool: mcp__cyoda__entity_update_entity_tool")
        print(f"  Entity ID: {update_spec['entity_id']}")
        print(f"  Update Data:")
        print(json.dumps(update_spec['entity_data'], indent=4))


def demonstrate_classification():
    """Demonstrate alert classification."""
    print("\n\n🏷️  DEMONSTRATION: Alert Classification")
    print("=" * 60)

    test_cases = [
        {"value": 42.0, "metric": "temperature", "anomaly_score": 0.95},
        {"value": -3.5, "metric": "temperature", "anomaly_score": 0.78},
        {"value": 95.0, "metric": "precipitation", "anomaly_score": 0.88},
    ]

    for i, case in enumerate(test_cases, 1):
        print(f"\n{i}. Classifying: {case['value']}{' °C' if case['metric'] == 'temperature' else 'mm'}")

        response = requests.post(
            f"{API_BASE}/alerts/classify",
            json=case
        )

        if response.status_code == 200:
            result = response.json()
            print(f"   → Type: {result['alert_type']}")
            print(f"   → Severity: {result['severity'].upper()}")


def main():
    """Run the complete demo."""
    print("=" * 60)
    print("🌍 CLIMATE ALERT SYSTEM DEMO")
    print("   Cyoda MCP + ML + Gemini AI Integration")
    print("=" * 60)

    # Check backend health
    try:
        response = requests.get(f"{API_BASE}/../health", timeout=5)
        if response.status_code != 200:
            print("\n❌ Backend not available. Please start the Flask app:")
            print("   python backend/app.py")
            return
    except:
        print("\n❌ Cannot connect to backend at localhost:5000")
        print("   Please start the Flask app: python backend/app.py")
        return

    print("\n✅ Backend is running")

    # Generate test data
    climate_data = generate_sample_data_with_anomalies()

    # Detect alerts
    alert_specs = detect_alerts(climate_data)

    if alert_specs:
        print(f"\n\n📋 ALERT SPECIFICATIONS")
        print("=" * 60)

        # Display each alert
        for i, spec in enumerate(alert_specs):
            display_alert_spec(spec, i)

        # Show MCP instructions for first alert
        if alert_specs:
            print("\n\n💡 EXAMPLE: Creating Alert in Cyoda")
            print("=" * 60)
            show_mcp_instructions(alert_specs[0])

    # Demonstrate other features
    demonstrate_search()
    demonstrate_lifecycle()
    demonstrate_classification()

    # Summary
    print("\n\n" + "=" * 60)
    print("📚 SUMMARY")
    print("=" * 60)
    print("""
This demo showed:
✓ ML-based anomaly detection in climate data
✓ Automatic alert generation with AI analysis
✓ Alert entity specifications for Cyoda
✓ Search capabilities with complex conditions
✓ Alert lifecycle management (acknowledge/resolve)
✓ Automatic severity and type classification

Next Steps:
1. Use MCP tools to create alert entities in Cyoda
2. View alerts in React dashboard: http://localhost:3000/alerts
3. Integrate with real climate data sources
4. Set up automated monitoring workflows
5. Configure alert notifications via Cyoda edge messages

For more info, see CLAUDE.md section: Climate Alert System
    """)


if __name__ == "__main__":
    main()
