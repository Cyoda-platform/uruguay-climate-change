import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const getClimateData = async (startDate, endDate, metric = 'temperature') => {
  try {
    const response = await api.get('/climate-data', {
      params: { start_date: startDate, end_date: endDate, metric },
    });
    return response.data;
  } catch (error) {
    console.error('Error fetching climate data:', error);
    throw error;
  }
};

export const getPredictions = async (startDate, endDate, metric = 'temperature') => {
  try {
    const response = await api.post('/predictions', {
      start_date: startDate,
      end_date: endDate,
      metric,
    });
    return response.data;
  } catch (error) {
    console.error('Error fetching predictions:', error);
    throw error;
  }
};

export const getStatistics = async () => {
  try {
    const response = await api.get('/statistics');
    return response.data;
  } catch (error) {
    console.error('Error fetching statistics:', error);
    throw error;
  }
};

export const getTrends = async (metric = 'temperature') => {
  try {
    const response = await api.get('/trends', {
      params: { metric },
    });
    return response.data;
  } catch (error) {
    console.error('Error fetching trends:', error);
    throw error;
  }
};

export default api;
