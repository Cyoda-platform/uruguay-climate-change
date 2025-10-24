import React, { useState, useEffect } from 'react';
import ClimateChart from '../components/ClimateChart';
import InfoCard from '../components/InfoCard';
import { getClimateData, getTrends } from '../services/api';
import './Dashboard.css';

const Dashboard = () => {
  const [temperatureData, setTemperatureData] = useState([]);
  const [precipitationData, setPrecipitationData] = useState([]);
  const [trendsData, setTrendsData] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      setLoading(true);

      // Fetch temperature data
      const tempResponse = await getClimateData('2020-01-01', '2023-12-31', 'temperature');
      setTemperatureData(tempResponse.data);

      // Fetch precipitation data
      const precipResponse = await getClimateData('2020-01-01', '2023-12-31', 'precipitation');
      setPrecipitationData(precipResponse.data);

      // Fetch trends
      const trendsResponse = await getTrends('temperature');
      setTrendsData(trendsResponse.trends);

      setLoading(false);
    } catch (error) {
      console.error('Error fetching data:', error);
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="loading-container">
        <div className="loader"></div>
        <p>Loading climate data...</p>
      </div>
    );
  }

  return (
    <div className="dashboard">
      <div className="page-header">
        <h2>Climate Dashboard</h2>
        <p className="subtitle">Historical climate data for Uruguay (2020-2023)</p>
      </div>

      {/* Interactive Educational Section */}
      <div className="info-section">
        <h3 className="section-title">🌟 Understanding Climate Data</h3>

        <InfoCard
          icon="🌡️"
          title="What is Climate Change?"
          description="Climate change refers to long-term shifts in temperatures and weather patterns"
          severity="critical"
          details={
            <div>
              <p>
                Climate change is one of the most pressing challenges facing our planet.
                It's not just about warmer temperatures—it's about fundamental changes to our Earth's systems.
              </p>

              <div className="highlight-box critical">
                <strong>🚨 Why This Matters:</strong>
                <p>
                  Uruguay is experiencing rising temperatures, changing precipitation patterns,
                  and more frequent extreme weather events. These changes affect agriculture,
                  water resources, and coastal communities.
                </p>
              </div>

              <h4>📊 Key Indicators We Track:</h4>
              <ul>
                <li><strong>Temperature:</strong> Average temperatures have risen by 0.8°C since 1990</li>
                <li><strong>Precipitation:</strong> Rainfall patterns are becoming more irregular</li>
                <li><strong>Extreme Events:</strong> Increased frequency of droughts and floods</li>
              </ul>
            </div>
          }
        />

        <InfoCard
          icon="🤖"
          title="Our AI & Machine Learning Methods"
          description="Advanced algorithms analyze decades of climate data to predict future trends"
          severity="info"
          details={
            <div>
              <h4>🧠 Technologies We Use:</h4>

              <div className="methods-grid">
                <div className="method-tag">LSTM Neural Networks</div>
                <div className="method-tag">Random Forest</div>
                <div className="method-tag">ARIMA Models</div>
                <div className="method-tag">Ensemble Learning</div>
              </div>

              <h4>How It Works:</h4>
              <ul>
                <li><strong>Data Collection:</strong> We gather historical climate data from 1990-2023</li>
                <li><strong>Pattern Recognition:</strong> AI identifies trends, seasonality, and anomalies</li>
                <li><strong>Prediction:</strong> Models forecast future climate scenarios with 85%+ accuracy</li>
                <li><strong>Validation:</strong> Continuous testing against real-world observations</li>
              </ul>

              <div className="highlight-box">
                <strong>💡 Fun Fact:</strong>
                <p>
                  Our LSTM model processes over 12,000 data points and can predict temperature
                  trends up to 5 years in advance with remarkable accuracy!
                </p>
              </div>
            </div>
          }
        />

        <InfoCard
          icon="📈"
          title="Reading the Charts"
          description="Learn how to interpret temperature and precipitation visualizations"
          severity="success"
          details={
            <div>
              <h4>🎯 Chart Components:</h4>
              <ul>
                <li><strong>Green Line:</strong> Shows actual measured values over time</li>
                <li><strong>Dots:</strong> Individual data points (monthly or yearly measurements)</li>
                <li><strong>Trends:</strong> Upward slopes indicate warming or increased precipitation</li>
                <li><strong>Hover:</strong> Click any point to see exact values and dates</li>
              </ul>

              <h4>What to Look For:</h4>
              <ul>
                <li>📊 <strong>Upward Trends:</strong> Consistent temperature increases over decades</li>
                <li>🌊 <strong>Variability:</strong> Large swings indicate climate instability</li>
                <li>🔥 <strong>Extremes:</strong> Record highs or lows show changing patterns</li>
              </ul>

              <div className="highlight-box warning">
                <strong>⚠️ Important Note:</strong>
                <p>
                  Short-term fluctuations are normal. We focus on long-term trends
                  (10+ years) to understand true climate change impacts.
                </p>
              </div>
            </div>
          }
        />

        <InfoCard
          icon="🌍"
          title="Why Uruguay Matters"
          description="Uruguay's unique position makes it a critical climate monitoring location"
          severity="warning"
          details={
            <div>
              <p>
                Uruguay sits at a crucial intersection of climate systems in South America,
                making it an important indicator for regional climate change.
              </p>

              <h4>🗺️ Geographic Significance:</h4>
              <ul>
                <li>Located between tropical and temperate zones</li>
                <li>Influenced by both Atlantic Ocean and continental weather systems</li>
                <li>Agricultural economy highly sensitive to climate variations</li>
                <li>Coastal areas vulnerable to sea-level rise</li>
              </ul>

              <h4>🌾 Real-World Impacts:</h4>
              <ul>
                <li><strong>Agriculture:</strong> 70% of exports depend on stable climate</li>
                <li><strong>Water Resources:</strong> Changing rainfall affects hydroelectric power</li>
                <li><strong>Biodiversity:</strong> Unique ecosystems at risk from temperature shifts</li>
              </ul>

              <div className="highlight-box warning">
                <strong>🎯 Our Mission:</strong>
                <p>
                  By monitoring and predicting climate patterns, we help policymakers,
                  farmers, and communities prepare for and adapt to climate change.
                </p>
              </div>
            </div>
          }
        />
      </div>

      {/* Charts Section */}
      <div className="charts-section">
        <h3 className="section-title">📊 Climate Data Visualizations</h3>

        <div className="charts-grid">
          <ClimateChart
            data={temperatureData}
            title="Temperature Over Time (°C)"
            dataKey="value"
          />

          <ClimateChart
            data={precipitationData}
            title="Precipitation Over Time (mm)"
            dataKey="value"
          />

          <ClimateChart
            data={trendsData}
            title="Long-term Temperature Trends (1990-2023)"
            dataKey="value"
            xKey="year"
          />
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
