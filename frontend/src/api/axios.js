import axios from 'axios';

const axiosInstance = axios.create({
  baseURL: 'http://127.0.0.1:8000/api/', // Replace this with your Django backend API base URL
  timeout: 5000,
});

export default axiosInstance;
