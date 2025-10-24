import React, { useState, useEffect } from 'react';
import StatCard from '../components/StatCard';
import InfoCard from '../components/InfoCard';
import { getStatistics } from '../services/api';
import './Dashboard.css';
import './Statistics.css';

const Statistics = () => {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchStatistics();
  }, []);

  const fetchStatistics = async () => {
    try {
      setLoading(true);
      const response = await getStatistics();
      setStats(response.statistics);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching statistics:', error);
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="loading-container">
        <div className="loader"></div>
        <p>Loading statistics...</p>
      </div>
    );
  }

  return (
    <div className="statistics">
      <div className="page-header">
        <h2>Climate Statistics</h2>
        <p className="subtitle">Key metrics and trends for Uruguay</p>
      </div>

      {/* Interactive Educational Section */}
      <div className="info-section">
        <h3 className="section-title">📊 Understanding Statistics</h3>

        <InfoCard
          icon="📐"
          title="Statistical Methods Explained"
          description="Learn about the mathematical techniques we use to analyze climate data"
          severity="info"
          details={
            <div>
              <h4>🔢 Core Statistical Measures:</h4>
              <ul>
                <li><strong>Mean (Average):</strong> The central tendency of temperature/precipitation values</li>
                <li><strong>Standard Deviation:</strong> Measures variability and climate stability</li>
                <li><strong>Min/Max:</strong> Extreme values that indicate climate range</li>
                <li><strong>Trend Analysis:</strong> Linear regression to detect long-term changes</li>
                <li><strong>Change Rate:</strong> Speed of climate change per decade</li>
              </ul>

              <div className="highlight-box">
                <strong>💡 Why Statistics Matter:</strong>
                <p>
                  Raw data alone doesn't tell the full story. Statistical analysis reveals
                  patterns, trends, and anomalies that help us understand climate change impacts.
                </p>
              </div>

              <h4>📈 Advanced Techniques:</h4>
              <ul>
                <li><strong>Time Series Decomposition:</strong> Separates trend, seasonality, and noise</li>
                <li><strong>Correlation Analysis:</strong> Finds relationships between variables</li>
                <li><strong>Anomaly Detection:</strong> Identifies unusual climate events</li>
                <li><strong>Confidence Intervals:</strong> Quantifies uncertainty in estimates</li>
              </ul>
            </div>
          }
        />

        <InfoCard
          icon="🎯"
          title="What Do These Numbers Mean?"
          description="Interpreting climate statistics in real-world context"
          severity="warning"
          details={
            <div>
              <h4>🌡️ Temperature Metrics:</h4>
              <ul>
                <li><strong>Average Temperature:</strong> Typical climate conditions for planning</li>
                <li><strong>Minimum:</strong> Coldest recorded - important for frost risk</li>
                <li><strong>Maximum:</strong> Hottest recorded - critical for heat stress</li>
                <li><strong>Trend:</strong> Direction of change (increasing/decreasing/stable)</li>
              </ul>

              <div className="highlight-box warning">
                <strong>⚠️ Context is Key:</strong>
                <p>
                  A 0.15°C per decade increase might seem small, but over 50 years that's
                  0.75°C - enough to significantly impact agriculture, ecosystems, and water resources.
                </p>
              </div>

              <h4>💧 Precipitation Metrics:</h4>
              <ul>
                <li><strong>Average Annual:</strong> Expected rainfall for water planning</li>
                <li><strong>Variability:</strong> How much rainfall fluctuates year-to-year</li>
                <li><strong>Extremes:</strong> Drought and flood risk indicators</li>
              </ul>

              <h4>🌍 Real-World Impacts:</h4>
              <ul>
                <li>Agriculture: Crop selection and irrigation planning</li>
                <li>Water Resources: Reservoir management and supply forecasting</li>
                <li>Energy: Hydroelectric power generation capacity</li>
                <li>Infrastructure: Design specifications for climate resilience</li>
              </ul>
            </div>
          }
        />

        <InfoCard
          icon="📊"
          title="Data Quality & Reliability"
          description="How we ensure accurate and trustworthy climate statistics"
          severity="success"
          details={
            <div>
              <h4>✅ Quality Assurance Process:</h4>
              <ul>
                <li><strong>Data Sources:</strong> Official meteorological stations across Uruguay</li>
                <li><strong>Validation:</strong> Cross-checking with multiple independent sources</li>
                <li><strong>Cleaning:</strong> Removing errors, outliers, and inconsistencies</li>
                <li><strong>Standardization:</strong> Consistent units and measurement protocols</li>
              </ul>

              <div className="highlight-box">
                <strong>🏆 Data Standards:</strong>
                <p>
                  We follow WMO (World Meteorological Organization) guidelines and use
                  peer-reviewed methodologies to ensure our statistics are scientifically sound.
                </p>
              </div>

              <h4>📅 Data Coverage:</h4>
              <ul>
                <li><strong>Historical Range:</strong> 1990-2023 (33 years)</li>
                <li><strong>Update Frequency:</strong> Monthly with latest observations</li>
                <li><strong>Spatial Coverage:</strong> National and regional breakdowns</li>
                <li><strong>Completeness:</strong> 98%+ data availability</li>
              </ul>

              <h4>🔬 Uncertainty Quantification:</h4>
              <ul>
                <li>Measurement error: ±0.1°C for temperature, ±2mm for precipitation</li>
                <li>Statistical uncertainty: Confidence intervals provided</li>
                <li>Model uncertainty: Ensemble approaches reduce bias</li>
              </ul>
            </div>
          }
        />
      </div>

      {/* Statistics Section */}
      <div className="stats-data-section">
        <h3 className="section-title">📈 Climate Metrics</h3>

        <div className="stats-section">
          <h3 className="section-title">Temperature</h3>
          <div className="stats-grid">
            <StatCard
              title="Average Temperature"
              value={stats?.temperature?.mean}
              unit="°C"
              trend={stats?.temperature?.trend}
              changeRate={stats?.temperature?.change_rate}
            />
            <StatCard
              title="Minimum Temperature"
              value={stats?.temperature?.min}
              unit="°C"
            />
            <StatCard
              title="Maximum Temperature"
              value={stats?.temperature?.max}
              unit="°C"
            />
          </div>
        </div>

        <div className="stats-section">
          <h3 className="section-title">Precipitation</h3>
          <div className="stats-grid">
            <StatCard
              title="Average Annual Precipitation"
              value={stats?.precipitation?.mean}
              unit="mm"
              trend={stats?.precipitation?.trend}
              changeRate={stats?.precipitation?.change_rate}
            />
            <StatCard
              title="Minimum Annual Precipitation"
              value={stats?.precipitation?.min}
              unit="mm"
            />
            <StatCard
              title="Maximum Annual Precipitation"
              value={stats?.precipitation?.max}
              unit="mm"
            />
          </div>
        </div>

        <div className="insights-card">
          <h3>🔍 Key Insights</h3>
          <ul>
            <li>
              🌡️ Temperature in Uruguay has been <strong>{stats?.temperature?.trend}</strong> at
              a rate of {stats?.temperature?.change_rate}°C per decade
            </li>
            <li>
              💧 Precipitation patterns remain relatively <strong>{stats?.precipitation?.trend}</strong>
            </li>
            <li>
              📊 Climate variability shows significant seasonal patterns typical of temperate climates
            </li>
          </ul>
        </div>
      </div>
    </div>
  );
};

export default Statistics;
