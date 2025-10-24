import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

const mlApi = axios.create({
  baseURL: `${API_BASE_URL}/ml`,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const getLSTMForecast = async (recentTemperatures, forecastDays = 30) => {
  try {
    const response = await mlApi.post('/lstm-forecast', {
      recent_temperatures: recentTemperatures,
      forecast_days: forecastDays,
    });
    return response.data;
  } catch (error) {
    console.error('Error fetching LSTM forecast:', error);
    throw error;
  }
};

export const getProphetForecast = async (days = 365) => {
  try {
    const response = await mlApi.get('/prophet-forecast', {
      params: { days },
    });
    return response.data;
  } catch (error) {
    console.error('Error fetching Prophet forecast:', error);
    throw error;
  }
};

export const detectAnomalies = async (data) => {
  try {
    const response = await mlApi.post('/detect-anomalies', { data });
    return response.data;
  } catch (error) {
    console.error('Error detecting anomalies:', error);
    throw error;
  }
};

export const classifyPatterns = async (data) => {
  try {
    const response = await mlApi.post('/classify-patterns', { data });
    return response.data;
  } catch (error) {
    console.error('Error classifying patterns:', error);
    throw error;
  }
};

export const getModelStatus = async () => {
  try {
    const response = await mlApi.get('/model-status');
    return response.data;
  } catch (error) {
    console.error('Error fetching model status:', error);
    throw error;
  }
};

export default mlApi;
