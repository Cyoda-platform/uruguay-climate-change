import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

const geminiApi = axios.create({
  baseURL: `${API_BASE_URL}/ai`,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const getClimateSummary = async (climateData) => {
  try {
    const response = await geminiApi.post('/climate-summary', {
      climate_data: climateData,
    });
    return response.data;
  } catch (error) {
    console.error('Error getting climate summary:', error);
    throw error;
  }
};

export const getMLInsights = async (mlResults) => {
  try {
    const response = await geminiApi.post('/ml-insights', {
      ml_results: mlResults,
    });
    return response.data;
  } catch (error) {
    console.error('Error getting ML insights:', error);
    throw error;
  }
};

export const getAnomalyReport = async (anomalies) => {
  try {
    const response = await geminiApi.post('/anomaly-report', {
      anomalies,
    });
    return response.data;
  } catch (error) {
    console.error('Error getting anomaly report:', error);
    throw error;
  }
};

export const getRecommendations = async (analysisSummary) => {
  try {
    const response = await geminiApi.post('/recommendations', {
      analysis_summary: analysisSummary,
    });
    return response.data;
  } catch (error) {
    console.error('Error getting recommendations:', error);
    throw error;
  }
};

export const getExecutiveSummary = async (fullAnalysis) => {
  try {
    const response = await geminiApi.post('/executive-summary', {
      full_analysis: fullAnalysis,
    });
    return response.data;
  } catch (error) {
    console.error('Error getting executive summary:', error);
    throw error;
  }
};

export const getGeminiStatus = async () => {
  try {
    const response = await geminiApi.get('/status');
    return response.data;
  } catch (error) {
    console.error('Error checking Gemini status:', error);
    throw error;
  }
};

export default geminiApi;
