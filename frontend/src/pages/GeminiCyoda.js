import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './GeminiCyoda.css';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

const GeminiCyoda = () => {
  const [geminiStatus, setGeminiStatus] = useState(null);
  const [climateData, setClimateData] = useState({
    value: '',
    metric: 'temperature',
    date: new Date().toISOString().split('T')[0],
    context: ''
  });
  const [analysis, setAnalysis] = useState(null);
  const [mcpSpec, setMcpSpec] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [nlQuery, setNlQuery] = useState('');
  const [searchResult, setSearchResult] = useState(null);
  const [activeTab, setActiveTab] = useState('analyze');
  const [modal, setModal] = useState({ show: false, title: '', message: '' });

  useEffect(() => {
    checkGeminiStatus();
  }, []);

  const checkGeminiStatus = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/gemini-cyoda/status`);
      setGeminiStatus(response.data);
    } catch (err) {
      console.error('Failed to check status:', err);
    }
  };

  const analyzeWithGemini = async () => {
    setLoading(true);
    setError(null);
    setAnalysis(null);
    setMcpSpec(null);

    try {
      const response = await axios.post(`${API_BASE_URL}/gemini-cyoda/analyze-and-alert`, {
        climate_data: {
          value: parseFloat(climateData.value),
          metric: climateData.metric,
          date: climateData.date,
          location: 'Uruguay',
          context: climateData.context || 'Climate monitoring data'
        }
      });

      if (response.data.success) {
        setAnalysis(response.data.gemini_analysis);
        setMcpSpec(response.data.cyoda_mcp_spec);
      }
    } catch (err) {
      setError(err.response?.data?.error || err.message);
    } finally {
      setLoading(false);
    }
  };

  const naturalLanguageSearch = async () => {
    setLoading(true);
    setError(null);
    setSearchResult(null);

    try {
      const response = await axios.post(`${API_BASE_URL}/gemini-cyoda/nl-search`, {
        query: nlQuery,
        entity_type: 'climate_alert'
      });

      if (response.data.success) {
        setSearchResult(response.data);
      }
    } catch (err) {
      setError(err.response?.data?.error || err.message);
    } finally {
      setLoading(false);
    }
  };

  const copyToClipboard = (data) => {
    navigator.clipboard.writeText(JSON.stringify(data, null, 2));
    setModal({
      show: true,
      title: '📋 Copied!',
      message: 'Specification copied to clipboard! Paste to Claude Code.'
    });
  };

  if (!geminiStatus) {
    return <div className="loading">Loading Gemini status...</div>;
  }

  if (!geminiStatus.integration_working) {
    return (
      <div className="gemini-cyoda-container">
        <div className="error-banner">
          <h2>⚠️ Gemini-Cyoda Integration Not Available</h2>
          <p>Please configure your Gemini API key:</p>
          <pre>export GEMINI_API_KEY="your-api-key"</pre>
          <p>Then restart the backend server.</p>
          <a href="https://makersuite.google.com/app/apikey" target="_blank" rel="noopener noreferrer">
            Get API Key →
          </a>
        </div>
      </div>
    );
  }

  return (
    <div className="gemini-cyoda-container">
      <header className="page-header">
        <h1>🤖 Gemini + Cyoda MCP Integration</h1>
        <p className="subtitle">Intelligent climate analysis powered by Gemini</p>
      </header>

      {/* Status Banner */}
      <div className="status-banner success">
        <div className="status-item">
          <span className="status-icon">✓</span>
          <span>Gemini Connected</span>
        </div>
        <div className="status-item">
          <span className="status-icon">✓</span>
          <span>Cyoda MCP Ready</span>
        </div>
        <div className="status-item">
          <span className="status-icon">✓</span>
          <span>Integration Active</span>
        </div>
      </div>

      {/* Tabs */}
      <div className="tabs">
        <button
          className={`tab ${activeTab === 'analyze' ? 'active' : ''}`}
          onClick={() => setActiveTab('analyze')}
        >
          🔬 Analyze Data
        </button>
        <button
          className={`tab ${activeTab === 'search' ? 'active' : ''}`}
          onClick={() => setActiveTab('search')}
        >
          🔍 Natural Language Search
        </button>
      </div>

      {error && (
        <div className="error-message">
          <strong>Error:</strong> {error}
        </div>
      )}

      {/* Analyze Tab */}
      {activeTab === 'analyze' && (
        <div className="tab-content">
          <div className="input-section">
            <h2>📊 Climate Data Input</h2>
            <p className="help-text">Enter climate measurements for Gemini to analyze</p>

            <div className="form-grid">
              <div className="form-group">
                <label>Value *</label>
                <input
                  type="number"
                  value={climateData.value}
                  onChange={(e) => setClimateData({...climateData, value: e.target.value})}
                  placeholder="e.g., 42.5"
                  step="0.1"
                />
              </div>

              <div className="form-group">
                <label>Metric</label>
                <select
                  value={climateData.metric}
                  onChange={(e) => setClimateData({...climateData, metric: e.target.value})}
                >
                  <option value="temperature">Temperature (°C)</option>
                  <option value="precipitation">Precipitation (mm)</option>
                </select>
              </div>

              <div className="form-group">
                <label>Date</label>
                <input
                  type="date"
                  value={climateData.date}
                  onChange={(e) => setClimateData({...climateData, date: e.target.value})}
                />
              </div>

              <div className="form-group full-width">
                <label>Context (optional)</label>
                <input
                  type="text"
                  value={climateData.context}
                  onChange={(e) => setClimateData({...climateData, context: e.target.value})}
                  placeholder="e.g., Unusually high for this time of year"
                />
              </div>
            </div>

            <button
              onClick={analyzeWithGemini}
              disabled={loading || !climateData.value}
              className="analyze-button"
            >
              {loading ? '🔄 Analyzing with Gemini...' : '🚀 Analyze with Gemini'}
            </button>
          </div>

          {/* Gemini Analysis Results */}
          {analysis && (
            <div className="results-section">
              <h2>🧠 Gemini Analysis</h2>

              {/* Should Create Alert */}
              <div className={`alert-decision ${analysis.should_create_alert ? 'create' : 'no-create'}`}>
                <div className="decision-icon">
                  {analysis.should_create_alert ? '🚨' : '✅'}
                </div>
                <div className="decision-text">
                  <h3>{analysis.should_create_alert ? 'Alert Recommended' : 'No Alert Needed'}</h3>
                  <p>{analysis.summary}</p>
                </div>
              </div>

              {analysis.should_create_alert && (
                <>
                  {/* Alert Details */}
                  <div className="analysis-grid">
                    <div className="analysis-card">
                      <div className="card-label">Alert Type</div>
                      <div className="card-value">{analysis.alert_type?.replace('_', ' ').toUpperCase()}</div>
                    </div>

                    <div className="analysis-card">
                      <div className="card-label">Severity</div>
                      <div className={`card-value severity-${analysis.severity}`}>
                        {analysis.severity?.toUpperCase()}
                      </div>
                    </div>

                    <div className="analysis-card">
                      <div className="card-label">Confidence</div>
                      <div className="card-value">
                        {(analysis.confidence * 100).toFixed(0)}%
                      </div>
                    </div>
                  </div>

                  {/* Detailed Analysis */}
                  <div className="analysis-detail">
                    <h3>📝 Detailed Analysis</h3>
                    <p>{analysis.detailed_analysis}</p>
                  </div>

                  {/* Recommendations */}
                  {analysis.recommendations && analysis.recommendations.length > 0 && (
                    <div className="recommendations">
                      <h3>💡 AI Recommendations</h3>
                      <ul>
                        {analysis.recommendations.map((rec, idx) => (
                          <li key={idx}>{rec}</li>
                        ))}
                      </ul>
                    </div>
                  )}

                  {/* MCP Specification */}
                  {mcpSpec && (
                    <div className="mcp-spec">
                      <h3>📡 Cyoda MCP Specification</h3>
                      <p className="help-text">
                        Ask Claude Code to create this entity in Cyoda using MCP tools
                      </p>
                      <pre>{JSON.stringify(mcpSpec, null, 2)}</pre>
                      <div className="mcp-actions">
                        <button
                          onClick={() => copyToClipboard(mcpSpec)}
                          className="copy-button"
                        >
                          📋 Copy MCP Spec
                        </button>
                        <div className="claude-instruction">
                          <strong>Next step:</strong> Tell Claude Code:
                          <div className="instruction-box">
                            "Create this alert in Cyoda using the MCP spec above"
                          </div>
                        </div>
                      </div>
                    </div>
                  )}
                </>
              )}
            </div>
          )}
        </div>
      )}

      {/* Natural Language Search Tab */}
      {activeTab === 'search' && (
        <div className="tab-content">
          <div className="input-section">
            <h2>🔍 Natural Language Search</h2>
            <p className="help-text">Ask Gemini to search Cyoda in plain English</p>

            <div className="search-box">
              <input
                type="text"
                value={nlQuery}
                onChange={(e) => setNlQuery(e.target.value)}
                placeholder="e.g., Show me all critical heat waves from last month"
                className="nl-input"
                onKeyPress={(e) => e.key === 'Enter' && naturalLanguageSearch()}
              />
              <button
                onClick={naturalLanguageSearch}
                disabled={loading || !nlQuery}
                className="search-button"
              >
                {loading ? '🔄 Processing...' : '🔍 Search'}
              </button>
            </div>

            <div className="example-queries">
              <strong>Example queries:</strong>
              <div className="examples">
                <button onClick={() => setNlQuery('Show me all critical alerts')}>
                  All critical alerts
                </button>
                <button onClick={() => setNlQuery('Find heat waves from January 2024')}>
                  Heat waves in January
                </button>
                <button onClick={() => setNlQuery('Show active alerts with high severity')}>
                  Active high severity
                </button>
              </div>
            </div>
          </div>

          {/* Search Results */}
          {searchResult && (
            <div className="results-section">
              <h2>🎯 Search Results</h2>

              <div className="search-info">
                <div className="info-item">
                  <strong>Your Query:</strong> {searchResult.natural_language_query}
                </div>
              </div>

              {/* Generated Search Specification */}
              {searchResult.cyoda_search_spec && (
                <div className="mcp-spec">
                  <h3>📡 Generated Cyoda Search Specification</h3>
                  <p className="help-text">
                    Gemini converted your plain English query into Cyoda search conditions
                  </p>
                  <pre>{JSON.stringify(searchResult.cyoda_search_spec, null, 2)}</pre>
                  <div className="mcp-actions">
                    <button
                      onClick={() => copyToClipboard(searchResult.cyoda_search_spec)}
                      className="copy-button"
                    >
                      📋 Copy Search Spec
                    </button>
                    <div className="claude-instruction">
                      <strong>Next step:</strong> Tell Claude Code:
                      <div className="instruction-box">
                        "Search Cyoda using this specification"
                      </div>
                    </div>
                  </div>
                </div>
              )}
            </div>
          )}
        </div>
      )}

      {/* Info Section */}
      <div className="info-section">
        <h3>ℹ️ How It Works</h3>
        <div className="workflow">
          <div className="workflow-step">
            <div className="step-number">1</div>
            <div className="step-content">
              <strong>Enter Data</strong>
              <p>Provide climate measurements</p>
            </div>
          </div>
          <div className="workflow-arrow">→</div>
          <div className="workflow-step">
            <div className="step-number">2</div>
            <div className="step-content">
              <strong>Gemini Analyzes</strong>
              <p>AI makes intelligent decisions</p>
            </div>
          </div>
          <div className="workflow-arrow">→</div>
          <div className="workflow-step">
            <div className="step-number">3</div>
            <div className="step-content">
              <strong>MCP Spec Generated</strong>
              <p>Specification for Cyoda</p>
            </div>
          </div>
          <div className="workflow-arrow">→</div>
          <div className="workflow-step">
            <div className="step-number">4</div>
            <div className="step-content">
              <strong>Claude Code Executes</strong>
              <p>Entity created in Cyoda</p>
            </div>
          </div>
        </div>
      </div>

      {/* Modal */}
      {modal.show && (
        <div className="modal-overlay" onClick={() => setModal({ show: false, title: '', message: '' })}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <h3>{modal.title}</h3>
            <p style={{ whiteSpace: 'pre-line' }}>{modal.message}</p>
            <button onClick={() => setModal({ show: false, title: '', message: '' })} className="modal-button primary">
              Close
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default GeminiCyoda;
