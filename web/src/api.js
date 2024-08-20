// api.js
import axios from 'axios';

const instance = axios.create({
  baseURL: '/',
});

instance.interceptors.response.use(
  response => response,
  error => {
    if (error.response && error.response.status === 401 ) {
      // 处理未授权情况，例如重定向到登录页面
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export default instance;