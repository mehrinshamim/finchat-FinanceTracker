
// src/utils/api.js
import axios from 'axios';

export const api = axios.create({
  baseURL: 'https://finchat-financetracker.onrender.com',
  withCredentials: true,
});
