import React, { useState, useEffect } from 'react';
import InfoCard from '../components/InfoCard';
import {
  getGeminiStatus,
  getExecutiveSummary,
  getClimateSummary,
  getRecommendations,
} from '../services/geminiApi';
import { getStatistics, getTrends } from '../services/api';
import './AIInsights.css';

const AIInsights = () => {
  const [geminiStatus, setGeminiStatus] = useState(null);
  const [executiveSummary, setExecutiveSummary] = useState('');
  const [climateSummary, setClimateSummary] = useState('');
  const [recommendations, setRecommendations] = useState('');
  const [loading, setLoading] = useState(true);
  const [generating, setGenerating] = useState(false);

  useEffect(() => {
    checkGeminiStatus();
  }, []);

  const checkGeminiStatus = async () => {
    try {
      const status = await getGeminiStatus();
      setGeminiStatus(status);
      setLoading(false);
    } catch (error) {
      console.error('Error checking Gemini status:', error);
      setLoading(false);
    }
  };

  const generateInsights = async () => {
    try {
      setGenerating(true);

      // Fetch climate data
      const stats = await getStatistics();
      const trends = await getTrends('temperature');

      // Prepare comprehensive analysis
      const fullAnalysis = {
        statistics: stats.statistics,
        trends: {
          temperature: trends.trends,
          direction: 'increasing',
          rate: 0.15,
        },
        time_period: '2020-2023',
        region: 'Uruguay',
      };

      // Generate AI insights
      const [execSummary, climSummary, recs] = await Promise.all([
        getExecutiveSummary(fullAnalysis),
        getClimateSummary(stats.statistics),
        getRecommendations({
          current_conditions: stats.statistics,
          trends: fullAnalysis.trends,
        }),
      ]);

      setExecutiveSummary(execSummary.executive_summary);
      setClimateSummary(climSummary.summary);
      setRecommendations(recs.recommendations);
      setGenerating(false);
    } catch (error) {
      console.error('Error generating insights:', error);
      setGenerating(false);
    }
  };

  if (loading) {
    return (
      <div className="loading-container">
        <div className="loader"></div>
        <p>Checking AI availability...</p>
      </div>
    );
  }

  if (!geminiStatus || !geminiStatus.available) {
    return (
      <div className="ai-insights-page">
        <div className="page-header">
          <h2>🤖 AI-Powered Insights</h2>
          <p className="subtitle">Gemini analysis and recommendations</p>
        </div>

        <div className="gemini-setup-required">
          <h3>⚙️ Gemini Setup Required</h3>
          <p>To enable AI-powered insights, you need to configure Google Gemini API.</p>

          <div className="setup-instructions">
            <h4>Setup Steps:</h4>
            <ol>
              <li>
                Get a free API key from{' '}
                <a
                  href="https://makersuite.google.com/app/apikey"
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  Google AI Studio
                </a>
              </li>
              <li>Install the SDK: <code>pip install google-generativeai</code></li>
              <li>
                Set environment variable:
                <code>export GEMINI_API_KEY="your-api-key-here"</code>
              </li>
              <li>Restart the Flask backend</li>
            </ol>

            <div className="status-grid">
              <div className={`status-item ${geminiStatus?.sdk_installed ? 'ok' : 'error'}`}>
                {geminiStatus?.sdk_installed ? '✅' : '❌'} SDK Installed
              </div>
              <div className={`status-item ${geminiStatus?.configured ? 'ok' : 'error'}`}>
                {geminiStatus?.configured ? '✅' : '❌'} API Key Configured
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="ai-insights-page">
      <div className="page-header">
        <h2>🤖 AI-Powered Insights</h2>
        <p className="subtitle">Gemini analysis and recommendations</p>
        {generating && <span className="generating-badge">✨ Generating insights...</span>}
      </div>

      {/* Interactive Educational Section */}
      <div className="info-section">
        <h3 className="section-title">🌟 Understanding AI Insights</h3>

        <InfoCard
          icon="🤖"
          title="What is Google Gemini?"
          description="Google's most advanced AI model for multimodal understanding and generation"
          severity="info"
          details={
            <div>
              <h4>🌟 Gemini Capabilities:</h4>
              <p>
                Gemini is Google's state-of-the-art large language model (LLM) that can
                understand and generate human-like text, analyze complex data, and provide
                intelligent insights.
              </p>

              <ul>
                <li><strong>Natural Language Understanding:</strong> Comprehends climate data context</li>
                <li><strong>Pattern Recognition:</strong> Identifies trends humans might miss</li>
                <li><strong>Contextual Analysis:</strong> Considers multiple factors simultaneously</li>
                <li><strong>Actionable Recommendations:</strong> Provides practical guidance</li>
              </ul>

              <div className="highlight-box">
                <strong>💡 Why Gemini for Climate?</strong>
                <p>
                  Gemini can synthesize vast amounts of climate data, scientific literature,
                  and domain knowledge to provide nuanced, context-aware insights that go
                  beyond simple statistical analysis.
                </p>
              </div>

              <h4>🎯 Model Specifications:</h4>
              <ul>
                <li><strong>Version:</strong> Gemini Pro (latest)</li>
                <li><strong>Parameters:</strong> Billions of neural network weights</li>
                <li><strong>Training Data:</strong> Diverse internet text + scientific papers</li>
                <li><strong>Context Window:</strong> 32,000+ tokens</li>
              </ul>
            </div>
          }
        />

        <InfoCard
          icon="🔗"
          title="Cyoda MCP Integration"
          description="Model Context Protocol enables seamless AI-to-data communication"
          severity="success"
          details={
            <div>
              <h4>🌐 What is MCP?</h4>
              <p>
                Model Context Protocol (MCP) is a standardized way for AI models to access
                and interact with external data sources, tools, and systems.
              </p>

              <ul>
                <li><strong>Real-time Data Access:</strong> Gemini queries our climate database directly</li>
                <li><strong>Structured Communication:</strong> Standardized data exchange format</li>
                <li><strong>Tool Integration:</strong> AI can use our ML models and APIs</li>
                <li><strong>Context Preservation:</strong> Maintains conversation history</li>
              </ul>

              <div className="highlight-box">
                <strong>🎯 The Power of Integration:</strong>
                <p>
                  Instead of just analyzing static data, Gemini can dynamically query our
                  database, run predictions, and combine multiple data sources to generate
                  comprehensive insights.
                </p>
              </div>

              <h4>🔧 How It Works:</h4>
              <ul>
                <li><strong>Step 1:</strong> User requests insights</li>
                <li><strong>Step 2:</strong> System fetches latest climate data</li>
                <li><strong>Step 3:</strong> Data sent to Gemini via MCP</li>
                <li><strong>Step 4:</strong> Gemini analyzes and generates insights</li>
                <li><strong>Step 5:</strong> Results displayed to user</li>
              </ul>
            </div>
          }
        />

        <InfoCard
          icon="📊"
          title="Types of AI-Generated Insights"
          description="Understanding what Gemini analyzes and how to use the insights"
          severity="warning"
          details={
            <div>
              <h4>📋 Executive Summaries:</h4>
              <ul>
                <li><strong>Purpose:</strong> High-level overview for decision-makers</li>
                <li><strong>Content:</strong> Key trends, risks, and opportunities</li>
                <li><strong>Audience:</strong> Policymakers, business leaders</li>
                <li><strong>Length:</strong> Concise, 2-3 paragraphs</li>
              </ul>

              <h4>🌍 Climate Analysis:</h4>
              <ul>
                <li><strong>Purpose:</strong> Detailed technical assessment</li>
                <li><strong>Content:</strong> Temperature trends, precipitation patterns, anomalies</li>
                <li><strong>Audience:</strong> Scientists, researchers, analysts</li>
                <li><strong>Depth:</strong> Comprehensive with supporting data</li>
              </ul>

              <h4>💡 Actionable Recommendations:</h4>
              <ul>
                <li><strong>Purpose:</strong> Practical steps to address climate challenges</li>
                <li><strong>Content:</strong> Sector-specific guidance (agriculture, water, energy)</li>
                <li><strong>Audience:</strong> Practitioners, planners, managers</li>
                <li><strong>Focus:</strong> Implementation-ready actions</li>
              </ul>

              <div className="highlight-box warning">
                <strong>⚠️ Important Note:</strong>
                <p>
                  AI insights are generated based on available data and should be used
                  alongside human expertise. Always validate critical decisions with
                  domain experts.
                </p>
              </div>
            </div>
          }
        />

        <InfoCard
          icon="🎯"
          title="How to Use AI Insights Effectively"
          description="Best practices for interpreting and acting on Gemini-generated analysis"
          severity="info"
          details={
            <div>
              <h4>✅ Best Practices:</h4>
              <ul>
                <li><strong>Regenerate Regularly:</strong> Update insights as new data arrives</li>
                <li><strong>Cross-Reference:</strong> Compare AI insights with raw data and charts</li>
                <li><strong>Consider Context:</strong> AI doesn't know local conditions - add your knowledge</li>
                <li><strong>Act on Recommendations:</strong> Insights are only valuable if implemented</li>
              </ul>

              <h4>🔍 What to Look For:</h4>
              <ul>
                <li><strong>Trend Identification:</strong> Is climate warming, cooling, or stable?</li>
                <li><strong>Anomaly Alerts:</strong> Unusual patterns that need attention</li>
                <li><strong>Risk Assessment:</strong> Potential threats to agriculture, water, etc.</li>
                <li><strong>Opportunity Spotting:</strong> Favorable conditions for planning</li>
              </ul>

              <div className="highlight-box">
                <strong>💡 Pro Tip:</strong>
                <p>
                  Use executive summaries for quick updates, climate analysis for deep dives,
                  and recommendations for action planning. Each serves a different purpose!
                </p>
              </div>

              <h4>🚀 Advanced Usage:</h4>
              <ul>
                <li>Compare insights across different time periods</li>
                <li>Track how recommendations evolve with changing data</li>
                <li>Share insights with stakeholders for collaborative planning</li>
                <li>Use insights to guide further data exploration</li>
              </ul>
            </div>
          }
        />
      </div>

      {/* AI Insights Generation */}
      <div className="ai-generation-section">
        <h3 className="section-title">✨ Generate Insights</h3>

        <button
          className="refresh-btn"
          onClick={generateInsights}
          disabled={generating}
        >
          {generating ? '⏳ Generating...' : (executiveSummary ? '🔄 Regenerate Insights' : '✨ Generate Insights')}
        </button>

      {executiveSummary && (
        <div className="insight-card executive">
          <div className="card-header">
            <h3>📋 Executive Summary</h3>
            <span className="ai-badge">Gemini</span>
          </div>
          <div className="card-content">
            <p className="ai-text">{executiveSummary}</p>
          </div>
        </div>
      )}

      {climateSummary && (
        <div className="insight-card climate">
          <div className="card-header">
            <h3>🌍 Climate Analysis</h3>
            <span className="ai-badge">Gemini</span>
          </div>
          <div className="card-content">
            <div className="ai-text">{formatText(climateSummary)}</div>
          </div>
        </div>
      )}

      {recommendations && (
        <div className="insight-card recommendations">
          <div className="card-header">
            <h3>💡 Actionable Recommendations</h3>
            <span className="ai-badge">Gemini</span>
          </div>
          <div className="card-content">
            <div className="ai-text">{formatText(recommendations)}</div>
          </div>
        </div>
      )}

      <div className="ai-features-grid">
        <div className="feature-box">
          <h4>🎯 What Gemini Analyzes</h4>
          <ul>
            <li>Temperature and precipitation trends</li>
            <li>Seasonal patterns and anomalies</li>
            <li>ML model prediction confidence</li>
            <li>Historical comparisons</li>
            <li>Climate change indicators</li>
          </ul>
        </div>

        <div className="feature-box">
          <h4>📊 Types of Insights</h4>
          <ul>
            <li>Executive summaries for decision-makers</li>
            <li>Detailed climate analysis</li>
            <li>Anomaly severity assessments</li>
            <li>Sector-specific recommendations</li>
            <li>Seasonal forecast narratives</li>
          </ul>
        </div>

        <div className="feature-box">
          <h4>🚀 Powered By</h4>
          <ul>
            <li>Google Gemini Pro LLM</li>
            <li>Real climate data from Uruguay</li>
            <li>LSTM & Prophet ML models</li>
            <li>Statistical analysis engines</li>
            <li>Anomaly detection algorithms</li>
          </ul>
        </div>
      </div>
      </div>
    </div>
  );
};

// Helper function to format AI text with paragraphs
const formatText = (text) => {
  return text.split('\n').map((paragraph, index) => (
    <p key={index} className="paragraph">
      {paragraph}
    </p>
  ));
};

export default AIInsights;
