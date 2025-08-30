import axios from 'axios';

// Base Axios instance for backend API
const API = axios.create({
  baseURL: import.meta.env.VITE_API_BASE || 'http://localhost:5000/api',
});

// Upload a CSV file
export const uploadCSV = (file) => {
  const form = new FormData();
  form.append('file', file);
  return API.post('/upload', form, {
    headers: { 'Content-Type': 'multipart/form-data' },
  });
};

// Fetch all transactions
export const getTransactions = () => API.get('/transactions');

// Fetch summary (e.g., expenses by category)
export const getSummary = () => API.get('/summary');
