import axios from 'axios';

const instance = axios.create({
  baseURL: 'http://localhost:8000', // Базовый URL вашего backend API
  headers: {
    'Content-Type': 'application/json'
    // Дополнительные заголовки, если нужны
  }
});

export default instance;
