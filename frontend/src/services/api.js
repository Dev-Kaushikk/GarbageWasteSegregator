/**
 * AI-Based Smart Garbage Waste Segregator — Frontend API Service Layer
 * Clean, centralized REST client for all backend integrations.
 */
import axios from 'axios';
import { API_BASE_URL } from '../config';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 45000,
});

apiClient.interceptors.response.use(
  (response) => response.data,
  (error) => {
    const errorMsg = error.response?.data?.error || error.message || 'An unexpected error occurred';
    console.error('[API Error]:', errorMsg);
    return Promise.reject(new Error(errorMsg));
  }
);

export default apiClient;

// --- System & Model APIs ---

export const checkHealth = () => apiClient.get('/api/health');

export const getModelInfo = () => apiClient.get('/api/model-info');

export const switchModel = (modelId) => apiClient.post('/api/model/switch', { model_id: modelId });

export const getClasses = () => apiClient.get('/api/classes');

// --- Detection API ---

export const detectWaste = (fileOrBase64, options = {}) => {
  const { conf = 0.20, modelId = null, sampleName = null } = options;
  const formData = new FormData();

  formData.append('conf', String(conf));
  if (modelId) formData.append('model_id', modelId);

  if (sampleName) {
    formData.append('sample_name', sampleName);
  } else if (fileOrBase64 instanceof Blob || fileOrBase64 instanceof File) {
    formData.append('image', fileOrBase64, fileOrBase64.name || 'image.jpg');
  } else if (typeof fileOrBase64 === 'string') {
    let base64Data = fileOrBase64;
    if (base64Data.includes(',')) {
      base64Data = base64Data.split(',')[1];
    }
    const byteCharacters = atob(base64Data);
    const byteNumbers = new Array(byteCharacters.length);
    for (let i = 0; i < byteCharacters.length; i++) {
      byteNumbers[i] = byteCharacters.charCodeAt(i);
    }
    const byteArray = new Uint8Array(byteNumbers);
    const blob = new Blob([byteArray], { type: 'image/jpeg' });
    formData.append('image', blob, 'image.jpg');
  }

  return apiClient.post('/api/detect', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  });
};

export const predictImage = detectWaste;

// --- History APIs ---

export const getHistory = (params = {}) => {
  return apiClient.get('/api/history', { params });
};

export const getHistoryDetail = (sessionId) => {
  return apiClient.get(`/api/history/${sessionId}`);
};

export const deleteHistoryEntry = (sessionId) => {
  return apiClient.delete(`/api/history/${sessionId}`);
};

// --- Analytics API ---

export const getAnalytics = () => apiClient.get('/api/analytics');

// --- Recommendations API ---

export const getRecommendation = (className) => {
  return apiClient.get(`/api/recommendations/${encodeURIComponent(className)}`);
};

// --- Sample Images APIs ---

export const getSampleImages = () => apiClient.get('/api/sample-images');

export const getSampleImageUrl = (filename) => `${API_BASE_URL}/api/sample-images/${filename}`;

export const getUploadUrl = (filename) => `${API_BASE_URL}/api/uploads/${filename}`;

export const getResultUrl = (filename) => `${API_BASE_URL}/api/results/${filename}`;

// --- Dataset & Training APIs for Research Views ---

export const getDatasets = () => apiClient.get('/api/datasets');

export const getDatasetStats = (datasetId) => apiClient.get(`/api/datasets/${datasetId}/stats`);

export const getImageUrl = (datasetId, split, filename) => `${API_BASE_URL}/api/datasets/${datasetId}/images/${split}/${filename}`;

export const getTrainingRuns = () => apiClient.get('/api/training/runs');

export const getRunPlotUrl = (runId, filename) => `${API_BASE_URL}/api/training/runs/${runId}/plots/${filename}`;

export const getTrainingStatus = (runId) => apiClient.get(`/api/training/runs/${runId}/status`);

export const listFiles = (dir) => apiClient.get(`/api/files/list/${dir}`);

export const getFileTree = (dir) => apiClient.get(`/api/files/tree/${dir}`);
