import axios from 'axios';

const API_URL =
  import.meta.env.VITE_API_URL || 'http://localhost:10000/api';

// Create axios instance with default config
const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add auth token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Auth API
export const authAPI = {
  signup: async (email, password) => {
    const response = await api.post('/auth/signup', { email, password });
    return response.data;
  },

  login: async (email, password) => {
    const response = await api.post('/auth/login', { email, password });
    return response.data;
  },

  getCurrentUser: async () => {
    const response = await api.get('/auth/me');
    return response.data;
  },
};

// Blog API
export const blogAPI = {
  generateBlog: async (url, length, tone, includeCta) => {
    const response = await api.post('/blog/generate', {
      url,
      length,
      tone,
      include_cta: includeCta,
    });
    return response.data;
  },

  getHistory: async (limit = 10, skip = 0) => {
    const response = await api.get('/blog/history', {
      params: { limit, skip },
    });
    return response.data;
  },

  getBlogById: async (blogId) => {
    const response = await api.get(`/blog/history/${blogId}`);
    return response.data;
  },

  previewContent: async (url) => {
    const response = await api.post('/blog/preview', { url });
    return response.data;
  },
};

export default api;
