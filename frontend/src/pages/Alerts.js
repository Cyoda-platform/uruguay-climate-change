import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './Alerts.css';

const Alerts = () => {
  const [alerts, setAlerts] = useState([]);
  const [summary, setSummary] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [filter, setFilter] = useState({ severity: '', status: '', alert_type: '' });
  const [detectionRunning, setDetectionRunning] = useState(false);
  const [modal, setModal] = useState({ show: false, title: '', message: '' });
  const [resolveModal, setResolveModal] = useState({ show: false, alertId: null, notes: '' });

  // Sample climate data for detection
  const sampleData = generateSampleClimateData();

  useEffect(() => {
    // Load alerts from Cyoda via MCP
    loadAlerts();
  }, []);

  const loadAlerts = async () => {
    setLoading(true);
    try {
      // Get MCP specification for listing alerts
      const response = await axios.get('/api/alerts/list');

      if (response.data.success) {
        // Check if alerts were directly provided by backend
        if (response.data.alerts && response.data.alerts.length > 0) {
          setAlerts(response.data.alerts);
          updateSummary(response.data.alerts);
        } else {
          // Backend returned MCP spec - need Claude Code to fetch
          const mcpSpec = response.data.mcp_spec;
          console.log('MCP tools must be executed by Claude Code:', mcpSpec);

          // Show empty state with instructions for now
          setAlerts([]);
          updateSummary([]);
          console.info('Alerts are stored in Cyoda. Claude Code needs to fetch them using MCP tools.');
          console.info('Run: mcp__cyoda__entity_list_entities_tool("climate_alert", "1")');
        }
      }
    } catch (err) {
      console.error('Error loading alerts:', err);
      setError(err.message);
      setAlerts([]);
      updateSummary([]);
    } finally {
      setLoading(false);
    }
  };

  const detectAlerts = async () => {
    setDetectionRunning(true);
    setError(null);

    try {
      // First, try to get real climate data
      let climateData = sampleData; // Fallback to sample data
      console.log('🔍 Starting alert detection...');

      try {
        const statsResponse = await axios.get('/api/statistics');
        if (statsResponse.data.success && statsResponse.data.data) {
          // Use real temperature data from the last 90 days
          const realData = statsResponse.data.data.slice(-90).map(item => ({
            date: item.date || new Date().toISOString().split('T')[0],
            value: item.temperature || item.temp_avg || item.value || 20
          }));

          if (realData.length > 0) {
            climateData = realData;
            console.log('✅ Using real climate data:', realData.length, 'records');
          }
        }
      } catch (statsErr) {
        console.warn('⚠️ Could not fetch real data, using sample data:', statsErr);
      }

      console.log('🤖 Running ML anomaly detection on', climateData.length, 'data points...');

      // Run anomaly detection (AI analysis disabled for performance)
      const response = await axios.post('/api/alerts/detect', {
        data: climateData,
        metric: 'temperature',
        value_column: 'value',
        use_ai_analysis: false  // Disabled: takes ~14s per alert with Gemini
      });

      if (response.data.success) {
        const alertCount = response.data.alerts_detected || 0;
        const specifications = response.data.alert_specifications || [];

        console.log(`✅ Detection complete! Found ${alertCount} alert(s)`);

        setModal({
          show: true,
          title: '✅ Detection Complete',
          message: `Detected ${alertCount} new alert${alertCount !== 1 ? 's' : ''}!\n\n${alertCount > 0 ? 'MCP tool specifications logged to console.\nExecute the MCP tools to create alerts in Cyoda.' : 'No anomalies detected in the data.'}`
        });

        // Display alert specifications for MCP tool execution
        if (specifications.length > 0) {
          console.log('=== ALERT SPECIFICATIONS FOR MCP TOOLS ===');
          specifications.forEach((spec, index) => {
            console.log(`\nAlert ${index + 1}:`, spec);
            console.log('Execute MCP tool: mcp__cyoda__entity_create_entity_tool');
            console.log('With params:', spec);
          });
          console.log('===========================================');

          // Reload alerts after a short delay to show newly created ones
          setTimeout(() => loadAlerts(), 2000);
        }
      }
    } catch (err) {
      setError(err.response?.data?.error || err.message);
    } finally {
      setDetectionRunning(false);
    }
  };

  const acknowledgeAlert = async (alertId) => {
    try {
      const response = await axios.put(`/api/alerts/update/${alertId}`, {
        status: 'acknowledged',
        acknowledged: true,
        resolved: false
      });

      if (response.data.success) {
        // Update local state
        setAlerts(alerts.map(a =>
          a.technical_id === alertId
            ? { ...a, acknowledged: true, status: 'acknowledged' }
            : a
        ));
        setModal({
          show: true,
          title: '✅ Alert Acknowledged',
          message: 'Alert acknowledged! Use MCP tool to update in Cyoda.'
        });
      }
    } catch (err) {
      setError(err.response?.data?.error || err.message);
    }
  };

  const openResolveModal = (alertId) => {
    setResolveModal({ show: true, alertId, notes: '' });
  };

  const resolveAlert = async () => {
    if (!resolveModal.notes.trim()) {
      setError('Resolution notes are required');
      return;
    }

    try {
      const response = await axios.put(`/api/alerts/update/${resolveModal.alertId}`, {
        status: 'resolved',
        acknowledged: true,
        resolved: true,
        resolution_notes: resolveModal.notes
      });

      if (response.data.success) {
        setAlerts(alerts.filter(a => a.technical_id !== resolveModal.alertId));
        setResolveModal({ show: false, alertId: null, notes: '' });
        setModal({
          show: true,
          title: '✅ Alert Resolved',
          message: 'Alert resolved! Use MCP tool to update in Cyoda.'
        });
      }
    } catch (err) {
      setError(err.response?.data?.error || err.message);
    }
  };

  const updateSummary = (alertList) => {
    const summaryData = {
      total: alertList.length,
      critical: alertList.filter(a => a.severity === 'critical').length,
      high: alertList.filter(a => a.severity === 'high').length,
      medium: alertList.filter(a => a.severity === 'medium').length,
      low: alertList.filter(a => a.severity === 'low').length,
      active: alertList.filter(a => a.status === 'active').length,
      acknowledged: alertList.filter(a => a.acknowledged).length
    };
    setSummary(summaryData);
  };

  const filteredAlerts = alerts.filter(alert => {
    if (filter.severity && alert.severity !== filter.severity) return false;
    if (filter.status && alert.status !== filter.status) return false;
    if (filter.alert_type && alert.alert_type !== filter.alert_type) return false;
    return true;
  });

  const getSeverityColor = (severity) => {
    const colors = {
      critical: '#dc2626',
      high: '#ea580c',
      medium: '#f59e0b',
      low: '#10b981'
    };
    return colors[severity] || '#6b7280';
  };

  const getSeverityIcon = (severity) => {
    const icons = {
      critical: '🔴',
      high: '🟠',
      medium: '🟡',
      low: '🟢'
    };
    return icons[severity] || '⚪';
  };

  return (
    <div className="alerts-container">
      <h1>Climate Alert System</h1>
      <p className="subtitle">Cyoda MCP + Gemini Integration</p>

      {error && (
        <div className="error-banner">
          <strong>Error:</strong> {error}
        </div>
      )}

      {/* Summary Cards */}
      {summary && (
        <div className="summary-grid">
          <div className="summary-card">
            <div className="summary-value">{summary.total}</div>
            <div className="summary-label">Total Alerts</div>
          </div>
          <div className="summary-card critical">
            <div className="summary-value">{summary.critical}</div>
            <div className="summary-label">Critical</div>
          </div>
          <div className="summary-card high">
            <div className="summary-value">{summary.high}</div>
            <div className="summary-label">High</div>
          </div>
          <div className="summary-card active">
            <div className="summary-value">{summary.active}</div>
            <div className="summary-label">Active</div>
          </div>
        </div>
      )}

      {/* Detection Button */}
      <div className="action-bar">
        <button
          onClick={detectAlerts}
          disabled={detectionRunning}
          className="detect-button"
        >
          {detectionRunning ? 'Detecting...' : '🔍 Detect New Alerts'}
        </button>
        <div className="filter-info">
          Showing {filteredAlerts.length} of {alerts.length} alerts
        </div>
      </div>

      {/* Filters */}
      <div className="filters">
        <select
          value={filter.severity}
          onChange={(e) => setFilter({...filter, severity: e.target.value})}
          className="filter-select"
        >
          <option value="">All Severities</option>
          <option value="critical">Critical</option>
          <option value="high">High</option>
          <option value="medium">Medium</option>
          <option value="low">Low</option>
        </select>

        <select
          value={filter.status}
          onChange={(e) => setFilter({...filter, status: e.target.value})}
          className="filter-select"
        >
          <option value="">All Statuses</option>
          <option value="active">Active</option>
          <option value="acknowledged">Acknowledged</option>
          <option value="resolved">Resolved</option>
        </select>

        <select
          value={filter.alert_type}
          onChange={(e) => setFilter({...filter, alert_type: e.target.value})}
          className="filter-select"
        >
          <option value="">All Types</option>
          <option value="heat_wave">Heat Wave</option>
          <option value="cold_snap">Cold Snap</option>
          <option value="extreme_precipitation">Extreme Precipitation</option>
          <option value="drought_indicator">Drought</option>
        </select>
      </div>

      {/* Alerts List */}
      <div className="alerts-list">
        {loading ? (
          <div className="no-alerts">
            <h3>⏳ Loading alerts from Cyoda...</h3>
            <p>Fetching alert entities via MCP integration</p>
          </div>
        ) : filteredAlerts.length === 0 ? (
          <div className="no-alerts">
            <h3>📭 {alerts.length === 0 ? 'No alerts found' : 'No alerts match filters'}</h3>
            <p>
              {alerts.length === 0
                ? 'Run "Detect New Alerts" to analyze climate data and create alerts in Cyoda.'
                : 'Try adjusting your filters to see more alerts.'
              }
            </p>
          </div>
        ) : (
          filteredAlerts.map(alert => (
            <div
              key={alert.technical_id}
              className="alert-card"
              style={{ borderLeft: `4px solid ${getSeverityColor(alert.severity)}` }}
            >
              <div className="alert-header">
                <div className="alert-title">
                  <span className="severity-badge" style={{ background: getSeverityColor(alert.severity) }}>
                    {getSeverityIcon(alert.severity)} {alert.severity.toUpperCase()}
                  </span>
                  <h3>{alert.alert_type.replace('_', ' ').toUpperCase()}</h3>
                </div>
                <div className="alert-date">{new Date(alert.date).toLocaleDateString()}</div>
              </div>

              <div className="alert-body">
                <p className="alert-description">{alert.description}</p>

                <div className="alert-metrics">
                  <div className="metric">
                    <strong>Value:</strong> {alert.value.toFixed(1)} {alert.metric === 'temperature' ? '°C' : 'mm'}
                  </div>
                  <div className="metric">
                    <strong>Anomaly Score:</strong> {(alert.anomaly_score * 100).toFixed(0)}%
                  </div>
                  <div className="metric">
                    <strong>Status:</strong> {alert.status}
                  </div>
                </div>

                {alert.recommendations && alert.recommendations.length > 0 && (
                  <div className="recommendations">
                    <strong>🤖 AI Recommendations:</strong>
                    <ul>
                      {alert.recommendations.map((rec, idx) => (
                        <li key={idx}>{rec}</li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>

              <div className="alert-actions">
                {!alert.acknowledged && (
                  <button
                    onClick={() => acknowledgeAlert(alert.technical_id)}
                    className="action-button ack"
                  >
                    ✓ Acknowledge
                  </button>
                )}
                {alert.acknowledged && !alert.resolved && (
                  <button
                    onClick={() => openResolveModal(alert.technical_id)}
                    className="action-button resolve"
                  >
                    ✓ Resolve
                  </button>
                )}
                {alert.acknowledged && (
                  <span className="acknowledged-badge">✓ Acknowledged</span>
                )}
              </div>
            </div>
          ))
        )}
      </div>

      {/* Info Banner */}
      <div className="info-banner">
        <h4>📡 Cyoda MCP Integration</h4>
        <p>
          This alert system integrates ML anomaly detection, Cyoda entity management, and Gemini analysis.
          Alert entities are stored in Cyoda using MCP tools for full lifecycle tracking.
        </p>
        <p style={{ marginTop: '0.5rem', fontSize: '0.9rem' }}>
          <strong>How it works:</strong> Click "Detect Anomalies" to run ML analysis on climate data.
          The system will generate MCP tool specifications (logged to console).
          Execute the MCP tools to create alert entities in Cyoda, then refresh this page to see them.
        </p>
      </div>

      {/* Modal */}
      {modal.show && (
        <div className="modal-overlay" onClick={() => setModal({ show: false, title: '', message: '' })}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <h3>{modal.title}</h3>
            <p style={{ whiteSpace: 'pre-line' }}>{modal.message}</p>
            <button onClick={() => setModal({ show: false, title: '', message: '' })} className="modal-button">
              Close
            </button>
          </div>
        </div>
      )}

      {/* Resolve Modal */}
      {resolveModal.show && (
        <div className="modal-overlay" onClick={() => setResolveModal({ show: false, alertId: null, notes: '' })}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <h3>Resolve Alert</h3>
            <p>Please provide resolution notes:</p>
            <textarea
              value={resolveModal.notes}
              onChange={(e) => setResolveModal({ ...resolveModal, notes: e.target.value })}
              placeholder="Enter resolution details..."
              className="modal-textarea"
              rows="4"
            />
            <div className="modal-buttons">
              <button onClick={resolveAlert} className="modal-button primary">
                Resolve
              </button>
              <button onClick={() => setResolveModal({ show: false, alertId: null, notes: '' })} className="modal-button">
                Cancel
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

// Helper function to generate sample climate data (fallback only)
function generateSampleClimateData() {
  const data = [];
  const startDate = new Date();
  startDate.setDate(startDate.getDate() - 90); // Last 90 days

  for (let i = 0; i < 90; i++) {
    const date = new Date(startDate);
    date.setDate(date.getDate() + i);

    // Generate temperature with seasonal variation
    let temp = 18 + 8 * Math.sin(2 * Math.PI * i / 365.25) + (Math.random() - 0.5) * 3;

    // Inject some anomalies for testing
    if (i === 15) temp = 41.2; // Heat wave
    if (i === 45) temp = -3.5; // Cold snap
    if (i === 60) temp = 39.8; // Another heat event

    data.push({
      date: date.toISOString().split('T')[0],
      value: parseFloat(temp.toFixed(2))
    });
  }

  return data;
}

export default Alerts;
